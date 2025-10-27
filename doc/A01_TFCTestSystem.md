## 1 TFCTestSystem - The main test system object
Named [TFCTestSystem](../src/tfc_TestSystem/TFCTestSystem.py) this object-class
handles all the high-level input related to a single instance of a test-run.
It has the following input parameters:
 - `directory` (or from command-line `-d`). The test directory in which to find the tests.
 - `executable` (or from command-line `-e`). The executable to use for the tests (May be
    overridden from the configuration file).
 - `num_jobs` (or from command-line `-j`). (Optional, default = 4). The number of jobs that
   may run at the same time.
 - `weights` (or from command-line `-w`). (Optional, default = 1). Weight classes to allow:
   - 0=None,
   - 1=Short,
   - 2=Intermediate,
   - 3=Short+Intermediate,
   - 4=Long,
   - 5=Long+Short,
   - 6=Long+Intermediate,
   - 7=All
 - `config_file` (or from command-line `-c`).
   (Optional, default = `TestSystemCONFIG.yaml`). The name of the default config
    file. Defaults to `TestSystemCONFIG.yaml` and will look within the main
    source directory `tfc_TestSystem` (i.e., the directory containing the
    `TFCTestSystem.py` file) or its parent (aka `tfc_TestSystem/..`).
 - `exclude_folders` (Optional, default = `[]`). An array of strings
   representing folders to exclude from searches that try to identify
   `*tests.yaml` files.
 - `requirements_docs` (Optional, default = `[]`). An array of strings that
   point to requirement documents that hold requirements with a specific syntax.
 - `requirements_matrix_outputfile` (Optional, default = "TraceAbilityMatrix.md").
   File to which to write the requirements traceability matrix.
 - `test_results_database_outputfile` (Optional, default = "TestResults.yaml").
   File to which the results database is to be written.

An instance of a `TFCTestSystem` object is instantiated from an executable
script (e.g., [ExampleTestSystemEXE.py](../src/tfc_TestSystem/ExampleTestSystemEXE.py))


