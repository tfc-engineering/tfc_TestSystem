# 6 Running the tests
To run the tests we simply need to do
```bash
./test/run_tests -j 6 -d test/tests/
```
which will produce output that looks like this:
```
Test files identified:
  test/tests/Ztests.yaml
Parsing test/tests/Ztests.yaml
Created test "test/tests/3dflowA" with 1 checks
Created test "test/tests/3dflowB" with 2 checks

***** TFCTestSystem created *****
  Main executable: $RELAP_EXE
  Number of jobs : 1
  Weight classes : ['short']


Running tests ['short']
[1] test/tests/3dflowA.........................Failed 0.2s
[1] test/tests/3dflowB.........................Passed 1s
Done executing tests with class in: ['short']

Elapsed time            : 1.50 seconds
Number of tests run     : 2
Number of failed tests  : 1

Failure reasons:
test/tests/3dflowA:
<class 'tfc_TestSystem.checks.RELAPRanToCompletionCheck.RELAPRanToCompletionCheck'> String "Errors detected during input" found in output.
```
