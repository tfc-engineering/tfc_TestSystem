# Design Requirements

## Convention in this document

- We will use a parser to build a requirement database, therefore, a few keywords
  are reserved.
- Using a double hash and the word `Requirement`, i.e., `## Requirement`, at the
  beginning of a line (the hashes must start at column 0) triggers the third
  word as the requirement text name. For example:
  `## Requirement cli1` denotes requirement `cli1` follows.
- The block of requirements is terminated with an html style comment `<!--endreq-->`.

## Requirement cli1 - Command Line Interface

Elke based programs shall support command line arguments (CLAs) in the following form
- Parameter value pairs. I.e., `-p value` and `--param value` where `p` is the
  shorthand version of `param` and is interchangeable with any other.
- Items marked as `value` can start with a `-` or a `--` as long as it does not
  conflict with other command line arguments in the application.
- A CLA does not have to have a value, and can thus be used as a flag.
- Some CLAs could be used multiple times. Functionality should exist to allow for it.

<!--endreq-->

## Requirement utesting - Unit testing
- As a CLA the user can use `basic` to execute unit-testing.

## Requirement input_processing - There shall be a distinct input processing phase
During this phase all possible input processing
shall be performed and all errors shall be collected to be displayed/conveyed at the end of the
phase.
<!--endreq-->

## Requirement cconv - Documented Coding conventions

There shall be a documented set of coding conventions.

<!--endreq-->



## Requirement inparams1 - Object instantiation via input parameters

### Definition of an input parameter
An input parameter can be one of following:
- A string
- A number
- An array of numbers
- An array of strings

<!--endreq-->
