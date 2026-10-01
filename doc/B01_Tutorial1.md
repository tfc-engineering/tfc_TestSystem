# Tutorial 1 - as basic as it gets

## The executable

Suppose you have an executable...something. This can be an actual program or a
script, e.g., a python script or a bash script. For purposes of this tutorial,
let's create the most simplest executable, `test_exe.sh`:

```bash
echo "Hello world"
```

Place this bash script in the folder `example_tests/`. Now let us set up a
specification to run this executable as a test.

## The test specification (.yaml file)

The test system will look for specification files by looking for the pattern
`*tests.yaml`. As can be seen from the extension these files are YAML files.
From many other examples you will notice that we like to name
these specifications something like `Ztests.yaml` so that it sorts to the bottom
of folders. The actual specification filename never really features in the test
system so feel free to name it anything you like as long as it has
`tests.yaml` at the end.

Let us now create the most basic test specification,
`example_tests/basic_tests.yaml`:

```yaml
tutorial1:
  executable: $PROJECT_ROOT/example_tests/test_exe.sh # optional
  args: ""                                            # required
  checks:                                             # required
    - type: ExitCodeCheck
```

In test specification files, top level objects are the test names, so in this
case the test name is `tutorial1`. Test objects can have several parameters
(see [TFCTestObject](./A03_TFCTestObject.md)) but only 2 are required, i.e.,
the arguments to supply to the executable, `args`, and the
list of checks to be run, `checks`. Technically the `executable` parameter is
also required but this can be inherited from a system wide setting (via a
[config file](./A02_ConfigFile.md)) or locally via a
[test specification](./A05_ConfiguringTests.md).

## Test output

For a test specification located in the folder `example_tests/` an output folder
will be created when the test system runs, i.e., `example_tests/out/`. The
console output for particular tests will be stored in this folder with the
convention `<test_name>.cout`. So in this tutorial's case `tutorial1.cout`.

## Checks

The easiest check is the `ExitCodeCheck`, which checks for exit code 0 by default,
but there are many other checks, most of which are extendable,
see [Built-in tests](./A04_Built_in_tests.md).

For this case we want to see if the program actually printed "Hello world". So
let us add the `HasStringCheck`:

```bash
tutorial1:
  executable: $PROJECT_ROOT/example_tests/test_exe.sh
  args: ""
  checks:
    - type: ExitCodeCheck
    - type: HasStringCheck
      line_key: Hello world
```

Now the test would fail if "Hello world" is not printed. Play around with it
a little bit to see the behavior. For example, make the test look for
"Hello world2" instead. The test system will tell you:
```
Number of failed tests            : 1

Failure reasons:
example_tests/tutorial1:
Check  1 type=HasStringCheck Could not find line containing "Hello world2".
```
