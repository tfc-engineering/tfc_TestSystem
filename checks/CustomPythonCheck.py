import pathlib
import os

from tfc_PyFactory.InputParameters import InputParameters
file_path = str(pathlib.Path(__file__).parent.resolve()) + "/"

import sys
sys.path.append(file_path + "../../")

import tfc_PyFactory
from tfc_PyFactory import *

from .CheckBase import *

class CustomPythonCheck(CheckBase):
    '''Compares the test's exit code against a desired value.'''
    @staticmethod
    def getInputParameters() -> InputParameters:
        params = CheckBase.getInputParameters()

        params.addRequiredParam("python_script", ParameterType.STRING,
                                "The path to the python script containing the "
                                "test procedure.")
        params.addOptionalParam("test_procedure_name", "check",
                                "Name of a routine that is supplied with a working directory and " \
                                "returns a boolean value.")
        params.addOptionalParam("invert_check", False,
                                "If true inverts the check.")

        return params


    def __init__(self, params: InputParameters) -> None:
        super().__init__(params)

        self.python_script_ = params.getParam("python_script").getStringValue()
        self.test_procedure_name_ = params.getParam("test_procedure_name").getStringValue()
        self.invert_check_ = params.getParam("invert_check").getBooleanValue()


    def executeCheck(self, config: dict, annotations: list[str]) -> bool:
        test_file_dir = config["test_file_directory"]
        try:
            script_file = open(f'{test_file_dir}/{self.python_script_}', "r")
        except Exception as ex:
            message = f'Error opening file "{self.python_script_}".'
            annotations.append("Python FileIOError")
            self.failed_ = True
            self.fail_reason_ = message
            return False

        procedure_name = self.test_procedure_name_
        namespace = {}
        exec(script_file.read(), namespace)

        if procedure_name in namespace:
            # This retrieves the function object and calls it
            try:
                result = namespace[procedure_name](config) # Pass the whole config so check can access all paths
            except Exception as ex:
                message = f'Error executing custom script "{self.python_script_}".'
                message += f"\n{ex}"
                annotations.append("Python error")
                self.failed_ = True
                self.fail_reason_ = message
                return False

            if not isinstance(result, bool):
                message = f'Custom script procedure returns non-boolean type "{type(result)}".'
                annotations.append("Bad Custom Script")
                self.failed_ = True
                self.fail_reason_ = message
                return False

            if not self.invert_check_:
                if result:
                    return True
                else:
                    self.failed_ = True
                    self.fail_reason_ = message = f'Custom check failed.'
                    return False
            if self.invert_check_:
                if result:
                    self.failed_ = True
                    self.fail_reason_ = message = f'Custom check succeeded.'
                    return False
                else:
                    return True

        else:
            message = f'Custom script procedure {procedure_name} not defined in script.'
            annotations.append("Bad Custom Script")
            self.failed_ = True
            self.fail_reason_ = message
            return False

        return True


PyFactory.register(CustomPythonCheck, "CustomPythonCheck")
