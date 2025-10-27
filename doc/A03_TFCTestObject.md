# 3 TFCTestObject - A test-handling object

Test objects are based on the `TFCTestObject` class.
This object will load up a test with all
the necessary bells-and-whistles. When executed by the test system, the test will execute the optional prerun script, after which a process will be submitted according to the executable and arguments specified. The test system will then continuously ping the test to ascertain it's completion status, which it does by calling it's checkProgress method. In this method (if the test has completed)  the test will execute its checks, run the optional postrun script and mark itself completed.

The working directory of the test is by default the directory in which it's configuration file lives. A relative offset may be added with the
relative_offset_workdir parameter.
They have the following parameters:
  - `args`. Arguments to pass to the test program.
  - `checks`. An array of check-inputs (See Check objects below).
  - `project_root`. (Semi-Optional, automatically set from TFCTestSystem). The path to the project root directory.
  - `disable_mpi`. (Optional, default = True). Flag to suppress running the application via MPI.
  - `num_procs`. (Optional, default = 1). The number of mpi processes used.
  - `weight_class`. (Optional, default = "short"). The weight class "short"/"intermediate"/"long"
  - `outfileprefix`. (Optional, default = ""). Will default to the test name + .out, otherwise
  outfileprefix+.out.
  - `skip`. (Optional, default = ""). If non-empty, will skip with this message.
  - `pass_flag`. (Optional, default = ""). If non-empty, will pass with this message.
  - `fail_flag`. (Optional, default = ""). If non-empty, will fail with this message.
  - `dependencies`. (Optional, default = []). A list of dependent test names before this test can run.
  - `prerun_script`. (Optional, default = ""). A shell script to run before the test is executed.
  - `precheck_script`. (Optional, default = ""). A shell script to run after the case has been run but before the checks are executed.
  - `postrun_script`. (Optional, default = ""). A shell script to run after the test is executed.
  - `relative_offset_workdir`. (Optional, default = ""). A relative working directory to be added to the default working directory.
  - `debug`. (Optional, default = False). Flag for debug printout. Will print the console output file to the screen for failed tests.
  - `executable`. (Optional, default = ""). Executable to use instead of system wide default.
  - `copy_test`. (Optional, default = []). This parameter provides a way to run a copy of a given test with modifications made by a script. A list of length 3 should be provided specifying the name extension to be added to the copied file name, the path to the script for creating a copy of the test, and the file location of the file to be copied. The script specified should create a copy of the test input file with any number of modifications. Both the original and the new input decks will be included in the test system.
  - `requirements`. (Optional, default = []). An array of strings representing id_tags for requirements that are addressed by this test.
