# 5 Configuring tests

## 5.1 The `*tests.yaml` file
A test is configured by a file with the general name `*tests.yaml`. The `*` is a
wildcard. Note: We use the convention of calling the configuration files
`Ztests.yaml` because by doing so the file system always, visually, places them
at the bottom of a file listing.

Within a configuration file the syntax for each test follows the
arguments of the `TFCTestObject` class as well as those added by the child check.

An example configuration is shown below:
```yaml
# This is a comment
3dflowA: # <-- This is the arbitrary name of the test
  args: "-rgtest -i 3dflowA.i -O 3dflowA.o -tpfdir ../../fluids/"
  checks: [
      {type: RELAPRanToCompletionCheck}
    ]

3dflowB:
  args: "-rgtest -i 3dflowB.i -O 3dflowB.o -tpfdir ../../fluids/ -R 3dflowB.vrf"
  checks: [
      {type: RELAPRanToCompletionCheck},
      {
        type: CompareVRFFileCheck,
        vrf_file: 3dflowB.vrf,
        gold_file: gold/3dflowB_gold.vrf,
        tolerance: 1.0e-6
      }
    ]
```

With this configuration file in the test directory we now have
```
test/
  doc/
  src/
  tests/
    gold/
    3dflowA.i
    3dflowB.i
    Ztests.yaml  <-- This is the test configuration file (not the system)
  run_tests
```
and we are ready to execute.

## 5.2 Change the executable on a test-file basis.

One can change the default execution on test-config-file basis by including a
test named `--executable:<exe_name>`. By doing this all the tests, specified in
this config-file, will be executed with the specified executable. Example:

```yaml
--executable: Ziemzalabiem.x # All the tests will use this executable

3dflowA: # <-- This is the arbitrary name of the test
  args: "-rgtest -i 3dflowA.i -O 3dflowA.o -tpfdir ../../fluids/"
  checks: [
      {type: RELAPRanToCompletionCheck}
    ]
```

## 5.3 Creating test templates
If a test name starts with `TEMPLATE_` the actual test will not be instantiated
but instead becomes useable by other tests to "copy" its configuration. Example:

```yaml
TEMPLATE_runtest_only:
  prerun_script: "mkdir temp_$TEST_NAME \n cp $TEST_NAME.i temp_$TEST_NAME/"
  args: "-rgtest -i $TEST_NAME.i -O ../out/$TEST_NAME.o -tpfdir $TPF_LOC"
  relative_offset_workdir: "temp_$TEST_NAME/"
  postrun_script: "rm -r temp_$TEST_NAME"
  copy_test: ["_ni","tools/niConv.py", "test/tests/base_cases/"]
  checks: [ {type: RELAPRanToCompletionCheck}, {type: ExitCodeCheck} ]

ans79:
  from_template: TEMPLATE_runtest_only

ans94:
  from_template: TEMPLATE_runtest_only

ans05:
  from_template: TEMPLATE_runtest_only

cstest1:
  from_template: TEMPLATE_runtest_only
  postrun_script: "cp temp_$TEST_NAME/restrt ./$TEST_NAME.r && rm -r temp_$TEST_NAME"
```

Here the only active tests are `ans79`, `ans94`, `ans05` and `cstest1`, all of
which copy from `TEMPLATE_runtest_only`. `ans79`, `ans94` and `ans05` use the
exact template parameters where as `cstest1` overwrites the `postrun_script`
parameter.
