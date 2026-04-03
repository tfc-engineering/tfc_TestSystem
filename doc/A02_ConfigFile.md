## 2 The config-file
The configuration file is a simple YAML formatted file read by `TFCTestSystem`.
With this file, any of the test system input parameters can be overridden since
it is processed after command line arguments are assigned. Additionally, it
supports several other input options:
  - `print_width`, The maximum width of the test system message printing. This
    can be used to prevent line-wrapping when running the tests.
  - `default_args`, A set of arguments to be prepended to all tests' arguments.
  - `env_vars`, A list of strings representing the environment variables that
    are registered within the test system. These variables can be used as
    substitutions within test arguments, or pre/post-scripts.
  - `weight_map`, A dictionary of weight keys and corresponding weight time
    limit values in seconds.
  - `weights`, A list of strings that correspond to the weight classes that
   should be executed by the test system.
  - `default_weight`, The weight class that is assigned to uncategorized tests.
  - `requirement_docs`, A list of strings that correspond to the paths to
   test requirements matrix documentation.
  - `requirements_output`, A string path to the test requirements output
    traceability matrix file.

Example config file:
```
default_executable: $RELAP_EXE
print_width: 97
num_jobs: 48
weights: ["short"]
weight_map:
  "short": 5.0
  "intermediate": 30.0
  "long": 60.0
default_weight: "short"
requirement_docs: [path/to/my/requirements.md]
requirements_output: path/to/my/traceability_matrix.md
```
