import pathlib
file_path = str(pathlib.Path(__file__).parent.resolve()) + "/"

import sys
sys.path.append(file_path + "../")
sys.path.append(file_path + "./")

# from tfc_PyFactory.InputParameters import InputParameters

import tfc_PyFactory
from tfc_PyFactory import *
import TFCTestObject
from TFCTestObject import *
from TFCTraceabilityMatrix import *
from TFCTestResultsDatabase import *

import os
import yaml
import re
import platform

# Blurb to fix yaml.safe_load reading scientific notation floats as strings,
# i.e. 1e5 is seen as a string by default.
loader = yaml.SafeLoader
loader.add_implicit_resolver(
    u'tag:yaml.org,2002:float',
    re.compile(u'''^(?:
     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
    |\\.[0-9_]+(?:[eE][-+][0-9]+)?
    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
    |[-+]?\\.(?:inf|Inf|INF)
    |\\.(?:nan|NaN|NAN))$''', re.X),
    list(u'-+0123456789.'))

import time

# ===================================================================
class TFCTestSystem(TFCObject, TFCTraceabilityMatrix, TFCTestResultsDatabase):
    """Test system to run any type of test with any type of executable.
    The system has a set of input parameters that can be set directly and
    additional options that can be set from a configuration file. By default
    the configuration file will be in the same directory as this file
    and have the name TestSystemCONFIG.yaml (which can be customized)."""
    @staticmethod
    def getInputParameters() -> InputParameters:
        params = TFCObject.getInputParameters()

        params.addRequiredParam("directory", ParameterType.STRING,
                                "The test directory in which to find the tests. "
                                "If this string is a comma separated string, " \
                                "each directory will be scanned.")
        params.addOptionalParam("executable", "python3",
                                "The executable to use for the tests (May be overridden"
                                " from the configuration file).")
        params.addOptionalParam("project_root", "",
                                "Root of the project. If not supplied will revert to " \
                                "current working directoy.")

        params.addOptionalParam("num_jobs", int(4),
                                "The number of jobs that may run at the same time.")
        params.addOptionalParam("weights", int(1),
                                "Weight classes to allow. "
                                "0=None, "
                                "1=Short, "
                                "2=Intermediate, "
                                "3=Short+Intermediate, "
                                "4=Long, "
                                "5=Long+Short, "
                                "6=Long+Intermediate, "
                                "7=All")
        params.addOptionalParam("config_file", "TestSystemCONFIG.yaml",
                                "The name of the default config file")
        params.addOptionalParam("exclude_folders", [],
                                "List of directories to exclude when searching for test files")
        params.addOptionalParam("requirement_docs", [],
                                "List of documents to search for requirements.")
        params.addOptionalParam("requirements_matrix_outputfile", "TraceAbilityMatrix.md",
                                "File to which to write the requirements "
                                "traceability matrix.")
        params.addOptionalParam("test_results_database_outputfile", "TestResults.yaml",
                                "File to which the results database is to be written.")

        return params


    def __init__(self, params: InputParameters) -> None:
        super().__init__(params)

        # Input parameters
        # AFCF = Also From Config File
        self.directory_ = params.getParam("directory").getStringValue()
        self.executable_ = params.getParam("executable").getStringValue() # AFCF
        self.num_jobs_ = params.getParam("num_jobs").getIntegerValue()
        self.weights_ = params.getParam("weights").getIntegerValue()
        self.config_file_ = params.getParam("config_file").getStringValue()
        self.compiler_ = os.getenv("COMPILER")
        self.os_version_ = platform.version()
        self.os_release_ = platform.release()
        self.os_details_ = platform.platform()

        exclude_param = params.getParam("exclude_folders")
        self.exclude_folders_ = []
        for subparam in exclude_param:
            self.exclude_folders_.append(subparam.getStringValue())

        # Requirement Documents
        requirement_docs = params.getParam("requirement_docs")
        self.requirement_docs_ = []
        for subparam in requirement_docs:
            self.requirement_docs_.append(subparam.getStringValue())

        if len(self.requirement_docs_) > 0:
            print("Requirement docs:")
            for req_doc in self.requirement_docs_:
                existence_status = "" if os.path.isfile(req_doc) else " (not found)"
                print(f"  {req_doc}" + existence_status)

        self.requirement_blocks_ = []
        for req_doc in self.requirement_docs_:
            if not os.path.isfile(req_doc):
                continue

            doc_reqs = self.parseRequirementDocument(req_doc)

            self.requirement_blocks_.append(doc_reqs)

            # # Verbose printing for testing
            # print(f'Requirements block for "{doc_reqs["filepath"]}":')
            # for req in doc_reqs["requirements"]:
            #     print(f"  {req["id_tag"]}:")
            #     print("    " + req["basic_title"])
            #     for line in req["text"].splitlines():
            #         print("    " + line.strip())

        self.requirements_matrix_outputfile_ = \
            params.getParam("requirements_matrix_outputfile").getStringValue()

        self.test_results_database_outputfile_ = \
            params.getParam("test_results_database_outputfile").getStringValue()

        # Config file options
        self.print_width_ = 120
        self.default_args_ = ""
        self.env_vars_ = []

        project_root = params.getParam("project_root").getStringValue()
        if project_root == "":
            self.project_root_ = os.getcwd() if project_root == "" else project_root

        print("Project-root", self.project_root_)

        # Init weight map
        weight_class_map = ["long", "intermediate", "short"]
        weight_classes_allowed = []
        if 0 <= self.weights_ <= 7:
            binary_weights = '{0:03b}'.format(self.weights_)
            for k in range(0, 3):
                if binary_weights[k] == '1':
                    weight_classes_allowed.append(weight_class_map[k])
        else:
            raise RuntimeError(
                '\033[31mIllegal value "' + str(self.weights_) + '" supplied ' +
                'for argument -w, --weights\033[0m')

        self.weight_classes_allowed_ = weight_classes_allowed
        self.max_num_procs_ = 1

        self.tests_: list[TFCTestObject] = []

        self.num_init_warnings_ = 0

        directories = []
        if self.directory_.find(",") < 0:
            directories.append(self.directory_)
        else:
            directory_strings = self.directory_.split(",")
            directories = directory_strings

        for directory in directories:
            test_files = self._recursiveFindTestListFiles(directory,
                                                          self.exclude_folders_,
                                                          True)
            self._parseTestFiles(test_files=test_files)

        for test in self.tests_:
            self.max_num_procs_ = max(self.max_num_procs_, test.num_procs_)

        # Process the config file
        config_file_path = ""
        possible_config_file_path1 = file_path + self.config_file_
        possible_config_file_path2 = file_path + "../" + self.config_file_

        if os.path.isfile(possible_config_file_path1):
            config_file_path = possible_config_file_path1
        elif os.path.isfile(possible_config_file_path2):
            config_file_path = possible_config_file_path2
        else:
            print(f'\033[31mWARNING: No config file {self.config_file_} ' +
                  f' found at either {possible_config_file_path1} or '
                  f' {possible_config_file_path2}\033[0m')
            self.num_init_warnings_ += 1

        with open(config_file_path) as yaml_file:
            yaml_dict = yaml.safe_load(yaml_file)

            for param in yaml_dict:
                if param == "default_executable":
                    self.executable_ = yaml_dict[param]
                if param == "print_width":
                    self.print_width_ = yaml_dict[param]
                if param == "default_args":
                    self.default_args_ = yaml_dict[param]
                if param == "env_vars":
                    self.env_vars_ = yaml_dict[param]

        print("\n***** TFCTestSystem created *****")

        print(f" Main executable        : {self.executable_}")
        print(f" Number of jobs         : {self.num_jobs_}")
        print(f" Weight classes         : {self.weight_classes_allowed_}")
        print(f" Compiler               : {os.environ["COMPILER"]}")
        print(f" environment variable   : {self.compiler_}")
        print(f" System details         : {self.os_details_}")
        print(f" System version         : {self.os_version_}")
        print(f" System release         : {self.os_release_}")
        print(f" ")


    def _recursiveFindTestListFiles(self, test_dir: str, exclude_folders: list, verbose: bool = False):
        """Recurses through a directory to find *tests*.yaml files"""

        if not os.path.isdir(test_dir):
            raise Exception('"' + test_dir + '" directory does not exist')

        test_files: list[str] = []  # Map of directories to lua files
        for dir_path, sub_dirs, files in os.walk(test_dir):
            if all([exdir not in dir_path for exdir in exclude_folders]):
                for file_name in files:
                    base_name, extension = os.path.splitext(file_name)
                    if extension == ".yaml" and (base_name.find("tests") > 0):
                        test_files.append(dir_path + "/" + file_name)

        if verbose:
            print("Test files identified:")
            for test_file in test_files:
                print(f"  {test_file}")

        return test_files


    def _parseTestFiles(self, test_files: list[str]):
        """Parses each *tests*.yaml file and creates the tests."""
        for file_name in test_files:
            pretty_name = os.path.relpath(file_name, self.project_root_)
            print("Parsing " + pretty_name)
            with open(file_name) as yaml_file:
                try:
                    yaml_dict = yaml.load(yaml_file, Loader=loader)
                    self.my_dict = yaml_dict
                    # This if check might be redundant
                    if not yaml_dict:
                        print(f"\033[31mWARNING: Error parsing yaml input \"{file_name}\"\033[0m")
                        self.num_init_warnings_ += 1
                        continue
                except Exception as ex:
                    print(f"\033[31mWARNING: Error parsing yaml input \"{file_name}\"\033[0m")
                    self.num_init_warnings_ += 1
                    print(ex)
                    continue

            # ============================== Grab a separate dict of templates only
            templates: dict[dict] = {}
            executable = ""
            for test_name in yaml_dict:
                if test_name.find("TEMPLATE_") >= 0:
                    templates[test_name] = yaml_dict[test_name]
                    continue

            # ============================== Expand all templates and special keys
            executable = ""
            expanded_yaml_dict = {}
            for test_name in yaml_dict:
                temp_dict = yaml_dict[test_name]

                if test_name.find("TEMPLATE_") >= 0: continue
                if test_name == "__executable":
                    executable = self.project_root_ + "/" + yaml_dict[test_name]
                    continue

                # Init the test's parameters dictionary
                test_dict = {}

                # Set to a template if needed
                if "from_template" in temp_dict:
                    template_name = temp_dict["from_template"]
                    if not template_name in templates:
                        print(f"\033[31mWARNING: Error test \"{test_name}\": " +
                        f'template name "{template_name} not found."\033[0m')
                        self.num_init_warnings_ += 1
                        continue
                    else:
                        test_dict = templates[template_name].copy()

                # Copy/overwrite other original parameters
                for param_name in temp_dict:
                    if param_name == "from_template": continue

                    test_dict[param_name] = temp_dict[param_name]

                expanded_yaml_dict[test_name] = test_dict

            # ============================== Handle test copying
            new_yaml_dict = {}
            for test_name in expanded_yaml_dict:
                temp_dict = expanded_yaml_dict[test_name]

                new_yaml_dict[test_name] = temp_dict.copy()

                if 'copy_test' in temp_dict:
                    # if copy parameters are not exactly 3. Do not copy
                    if len(temp_dict['copy_test']) != 3: continue

                    copy_ext,copy_script,input_dir = temp_dict['copy_test']

                    #copy_dict[param] = temp_dict[param]
                    temp_dict['postrun_script'] += ' \n rm $TEST_NAME.i'

                    # check if weight class is allowed
                    if 'weight_class' not in temp_dict:
                        if 'short' not in self.weight_classes_allowed_:
                            continue
                    else:
                        if temp_dict['weight_class'] not in self.weight_classes_allowed_:
                            continue
                    # run script to create copy test file
                    result = subprocess.run([copy_script,input_dir+test_name+'.i'],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
                    # check if subprocess ran correctly
                    if result.returncode != 0:
                        print(f"\033[31mWARNING: Error running copy script \"{copy_script}\"\033[0m")
                        self.num_init_warnings_ += 1
                    # check if subprocess created new file
                    copy_name = f'{test_name+copy_ext}'
                    if str(result.stdout).find('was created') >=0 :
                        new_yaml_dict[copy_name] = temp_dict.copy()

            # make tests
            for test_name in new_yaml_dict:
                temp_dict = new_yaml_dict[test_name]

                if not isinstance(temp_dict, dict):
                    print(f"\033[31mWARNING: Error test \"{test_name}\" is not a dict\033[0m")
                    self.num_init_warnings_ += 1
                    continue

                dir_, name_ = os.path.split(file_name)
                test_true_name = f'{dir_}/{test_name}'
                test_dict = {}

                if "env_var_skip" in temp_dict:
                   env_var_skip_list = temp_dict["env_var_skip"]

                   if isinstance(env_var_skip_list, list):
                       num_items = len(env_var_skip_list)

                       if num_items%2 != 0:
                           print(f'\033[31mWARNING: Number of items in parameter "env_var_skip" ' +
                                 f'of test "{test_name}" is not a factor of 2.\033[0m')
                           self.num_init_warnings_ += 1

                       num_pairs = int(num_items/2)
                       for k in range(0, num_pairs):
                           env_var_name = env_var_skip_list[2*k]
                           env_var_value = env_var_skip_list[2*k+1]

                           envvar_defined = env_var_name in os.environ
                           envvar_isvalue = os.environ[env_var_name] == env_var_value
                           if not "skip" in test_dict:
                               test_dict["skip"] = ""
                           if envvar_defined and envvar_isvalue:
                               test_dict["skip"] += f'{env_var_name}=={env_var_value}'

                test_dict["type"] = "TFCTestObject"
                if not "project_root" in test_dict:
                    test_dict["project_root"] = self.project_root_ + "/"

                for param_name in temp_dict:
                    if param_name == "from_template": continue
                    if param_name == "env_var_skip": continue
                    test_dict[param_name] = temp_dict[param_name]

                if executable != "" and "executable" not in test_dict:
                    test_dict["executable"] = executable

                try:
                    test = PyFactory.makeObject(test_true_name, Parameter("", test_dict))
                    test.setTestSystemReference(self)
                    self.tests_.append(test)
                except Exception as ex:
                    print(f"\033[31mWARNING: Error creating test \"{test_name}\"\033[0m\n" +
                          ex.__str__())
                    self.num_init_warnings_ += 1


    def run(self):
        """Actually executes the test system"""

        start_time = time.perf_counter()

        job_state = {}
        capacity = self.num_jobs_
        system_load = 0
        active_tests: list[TFCTestObject] = []

        # ======================================= Testing phase
        print("\nRunning tests " + self.weight_classes_allowed_.__str__() + "")
        k = 0
        while True:
            k += 1

            done = True  # Assume we are done
            for test in self.tests_:
                if test.ran_ or (test.weight_class_ not in self.weight_classes_allowed_):
                    test.ran_ = True
                    continue
                done = False

                if not test.submitted_ and test.checkDependenciesMet(self.tests_):
                    if test.num_procs_ <= (capacity - system_load):
                        system_load += test.num_procs_

                        test.submit(self)

                        active_tests.append(test)

            # Check test progression
            system_load = 0
            for test in active_tests:
                try:
                    if test.checkProgress(self) == "Running":
                        system_load += test.num_procs_
                except Exception as ex:
                    print(f"\033[31mERROR: Test {test.name_}"
                          " had a Python failure\033[0m\n" + ex.__str__())
                    raise ex

            time.sleep(0.01)

            if done:
                break # from while-loop

        # ======================================= Post-test phase
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        print("Done executing tests with class in: " +
          self.weight_classes_allowed_.__str__())

        num_tests_failed = 0
        num_tests_skipped = 0
        for test in active_tests:
            if not test.passed_:
                num_tests_failed += 1
            if test.skip_:
                num_tests_skipped += 1

        print()
        print("Elapsed time                       : {:.2f} seconds".format(elapsed_time))
        print(f"Number of initialization warnings : {self.num_init_warnings_}")
        print(f"Number of tests run               : {len(active_tests)}")
        print(f"Number of tests skipped           : {num_tests_skipped}")
        if num_tests_failed == 0:
            print(f"Number of failed tests            : {num_tests_failed}")
        else:
            print(f"\033[31mNumber of failed tests            : {num_tests_failed}\033[0m")

        self.writeRequirementsTraceabilityMatrix()
        self.writeResultsDatabase()

        # Printing failure logs
        failure_reasons: list[str] = []
        for test in active_tests:

            if test.passed_:
                continue

            reason = f'{test.name_}:\n' + f'{test.fail_flag_reason_}'

            for check in test.checks_:
                if check.failed_:
                    reason += f'{type(check)} {check.fail_reason_}'

            failure_reasons.append(reason)

        if len(failure_reasons) > 0:
            print("\n\033[31mFailure reasons:")
            for reason in failure_reasons:
                print(reason)
            print("\033[0m")

        for test in active_tests:
            if test.debug_ == True:
                if test.passed_:
                    continue
                dir_, testname_ = os.path.split(test.name_)
                print("Output of failed test: testname_")
                filename = dir_ + f"/out/{testname_}.cout"
                print(filename)
                file = open(filename,"r")
                contents = file.read()
                print(contents)
                file.close()

        if num_tests_failed > 0:
            return 1
        return 0


PyFactory.register(TFCTestSystem, "TFCTestSystem")
