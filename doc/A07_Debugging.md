# 7 Debug Functionality
The debug functionality can be activated by setting debug to True. See the example below:

```yaml
# This is a comment
3dflowA: # <-- This is the arbitrary name of the test
  args: "-rgtest -i 3dflowA.i -O 3dflowA.o -tpfdir ../../fluids/"
  checks: [
      {type: RELAPRanToCompletionCheck}
    ]
  debug: True
```

This will print the console output at the end of the test output when the test fails as shown below:
```
Test files identified:
 ['/projects/r5dev/coxbr/relap5-3d-total-coxbr/test/..//test/tests/NCErrMsg//Ztests.yaml']
Parsing test/tests/NCErrMsg/Ztests.yaml
Created test-job "test/tests/NCErrMsg/Test-BR" with 2 checks
Created test-job "test/tests/NCErrMsg/Test-CPRSSR" with 2 checks
Created test-job "test/tests/NCErrMsg/Test-PIPE" with 2 checks
Created test-job "test/tests/NCErrMsg/Test-PUMP" with 2 checks
Created test-job "test/tests/NCErrMsg/Test-SV" with 2 checks

***** TFCTestSystem created *****
  Main executable: $RELAP_EXE
  Number of jobs : 1
  Weight classes : ['short']


Running tests ['short']
[1] test/tests/NCErrMsg/Test-BR............................................................Failed 0.06s
DEBUG: use postrun_script to print useful output here

[1] test/tests/NCErrMsg/Test-CPRSSR........................................................Passed 0.09s
[1] test/tests/NCErrMsg/Test-PIPE..........................................................Passed 0.08s
[1] test/tests/NCErrMsg/Test-PUMP..........................................................Passed 0.07s
[1] test/tests/NCErrMsg/Test-SV............................................................Passed 0.05s
Done executing tests with class in: ['short']

Elapsed time            : 0.66 seconds
Number of tests run     : 5
Number of tests skipped : 0
Number of failed tests  : 1

Failure reasons:
/projects/r5dev/coxbr/relap5-3d-total-coxbr/test/..//test/tests/NCErrMsg/Test-BR:
<class 'tfc_TestSystem.checks.RELAPRanToCompletionCheck.RELAPRanToCompletionCheck'> String "Errors detected during input" found in output.

Output of failed test: testname_
/projects/r5dev/coxbr/relap5-3d-total-coxbr/test/..//test/tests/NCErrMsg/out/Test-BR.cout
$RELAP_EXE  -rgtest -i Test-BR.i -O ../out/Test-BR.o -tpfdir /projects/r5dev/coxbr/relap5-3d-total-coxbr//fluids/
 ________________________________________
|   COPYRIGHT     |  EXPORT CONTROLLED   |
|                 |     INFORMATION      |
| Battelle Energy |  Contains technical  |
|    Alliance     | data whose export is |
|                 |restricted by statute.|
|      2022       |Violations may result |
|                 |  in administrative,  |
|   All Rights    |  civil, or criminal  |
|    Reserved     |      penalties.      |
|_________________|______________________|

               Copyright 2022 Battelle Energy Alliance, LLC
                           ALL RIGHTS RESERVED

                Prepared by Battelle Energy Alliance, LLC
                  under Contract No. DE-AC07-05ID14517
                  with the U. S. Department of Energy

   NOTICE: This computer software, RELAP5-3D, was prepared by
   Battelle Energy Alliance, LLC, hereinafter the Contractor,
   under Contract No. AC07-05ID14517 with the United States
   (U. S.) Department of Energy (DOE). For ten years from
   April 10, 2012, the Government is granted for itself and others
   acting on its behalf a nonexclusive, paid-up, irrevocable
   worldwide license in this data to reproduce, prepare derivative
   works, and perform publicly and display publicly, by or on
   behalf of the Government. There is provision for the possible
   extension of the term of this license. Subsequent to that
   period or any extension granted, the Government is granted for
   itself and others acting on its behalf a nonexclusive, paid-up,
   irrevocable worldwide license in this data to reproduce,
   prepare derivative works, distribute copies to the public,
   perform publicly and display publicly, and to permit others to
   do so. The specific term of the license can be identified by
   inquiry made to Contractor or DOE. NEITHER THE UNITED STATES
   NOR THE UNITED STATES DEPARTMENT OF ENERGY, NOR CONTRACTOR
   MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES ANY
   LIABILITY OR RESPONSIBILITY FOR THE USE, ACCURACY,
   COMPLETENESS, OR USEFULNESS OR ANY INFORMATION, APPARATUS,
   PRODUCT, OR PROCESS DISCLOSED, OR REPRESENTS THAT ITS USE WOULD
   NOT INFRINGE PRIVATELY OWNED RIGHTS.

   EXPORT RESTRICTIONS: The provider of this computer software and
   its employees and its agents are subject to U.S. export control
   laws that prohibit or restrict (i) transactions with certain
   parties, and (ii) the type and level of technologies and
   services that may be exported. You agree to comply fully with
   all laws and regulations of the United States and other
   countries (Export Laws) to assure that neither this computer
   software, nor any direct products thereof are (1) exported,
   directly or indirectly, in violation of Export Laws, or (2) are
   used for any purpose prohibited by Export Laws, including,
   without limitation, nuclear, chemical, or biological weapons
   proliferation.

   None of this computer software or underlying information or
   technology may be downloaded or otherwise exported or
   re-exported (i) into (or to a national or resident of) Cuba,
   North Korea, Iran, Sudan, Syria or any other country to which
   the U.S. has embargoed goods; or (ii) to anyone on the U.S.
   Treasury Department's List of Specially Designated Nationals
   or the U.S. Commerce Department's Denied Persons List,
   Unverified List, Entity List, Nonproliferation Sanctions or
   General Orders. By downloading or using this computer software,
   you are agreeing to the foregoing and you are representing and
   warranting that you are not located in, under the control of,
   or a national or resident of any such country or on any such
   list, and that you acknowledge you are responsible to obtain
   any necessary U.S. government authorization to ensure
   compliance with U.S. law.

   GAIN Licensed Field of Use:
   LICENSED FIELD means, and is limited to, use of SOFTWARE and
   COPYRIGHTED CODE only for simulating the operation of conven-
   tional and non-conventional nuclear energy/reactor systems,
   including associated operational and safety systems, for
   engineering and operating analysis purposes.  The LICENSED
   FIELD specifically excludes any commercial use of the SOFTWARE
   including, but are not limited to, nuclear reactor design for
   plant permitting; formal design calculations; engineering
   calculations supporting operations and reactor maintenance,
   development of plant simulators; assessment of reactor systems,
   structure and reliability.  LICENSED FIELD specifically does
   not allow use of SOFTWARE and COPYRIGHTED CODE in the actual
   operation of nuclear energy/reactor systems or associated
   operational or safety systems

DGMtest1.i Test fluxing of  DGM in all liquid system
 Thermodynamic properties files used by this problem:

 Thermodynamic properties file for h2o is tpfh2o,
 tpfh2o version 1.1.1, tables of thermodynamic properties of light water
RELAP5-3D: Errors detected during input processing.

 $$$$$$$$WARNING: $HOSTNAME environment
 variable does not exist - hostname is unknown.
```

Further output can be printed using the test's postrun_script parameter. For example
the test below will print the output file to the console:
```yaml
# This is a comment
3dflowA: # <-- This is the arbitrary name of the test
  args: "-rgtest -i 3dflowA.i -O 3dflowA.o -tpfdir ../../fluids/"
  checks: [
      {type: RELAPRanToCompletionCheck}
    ]
  debug: True
  postrun_script: "cat 3dflowA.o"
```

If temporary directories are created and deleted by the pre- and post-run scripts
one can also make changes to them to get additional information.
