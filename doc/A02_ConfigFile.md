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

Example config file:
```
default_executable: $RELAP_EXE
print_width: 97
num_jobs: 48
weights: 7
```
