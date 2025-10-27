# 4 Built-in checks
Check objects all inherit from the `CheckBase` class, which has no arguments.
Additional checks are implemented in derived classes.

## 4.1 ExitCodeCheck
Compares the test's exit code against a desired value. Arguments:
  - `gold_value`. (Optional, default = 0). The desired exit code.

## 4.2 HasStringCheck
Checks for presence or abscence of a string in the output of a test. Arguments:
  - `line_key`. The string to find in order to identify the line of interest.
  - `reverse_line_traverse`. (Optional, default = False). If true will reverse
  the traversal of file lines. This is useful if you want the first or last
  occurence of a word.
  - `fail_if_present`. (Optional, default = False). Inverts the check. Fails if the line_key is indeed found.

## 4.3 WordFloatCheck
Performs a check on a specific word of type float. Arguments:
  - `line_key`. The string to find in order to identify the line of interest.
  - `word_number`. Which word (zero-based index) to be compared to the gold value.
  - `gold_value`. The float-value required to match.
  - `tolerance`. The tolerance to which the gold-value is evaluated.
  - `reverse_line_traverse`. (Optional, default = False). If true will reverse the traversal of file lines. Useful for using the first or last occurence.
  - `word_delimiters`. (Optional, default = " "). Characters that must be used as delimeters for separating words.

## 4.4 WordIntegerCheck
Performs a check on a specific word of type integer. Arguments:
  - `line_key`. The string to find in order to identify the line of interest.
  - `word_number`. Which word (zero-based index) to be compared to the gold value.
  - `gold_value`. The integer-value required to match.
  - `reverse_line_traverse`. (Optional, default = False). If true will reverse the traversal of file lines. Useful for using the first or last occurence.
  - `word_delimiters`. (Optional, default = " "). Characters that must be used as delimeters for separating words.

## 4.5 WordStringCheck
Performs a check on a specific word of type string. Arguments:
  - `line_key`. The string to find in order to identify the line of interest.
  - `word_number`. Which word (zero-based index) to be compared to the gold value.
  - `gold_value`. The string-value required to match.
  - `reverse_line_traverse`. (Optional, default = False). If true will reverse the traversal of file lines. Useful for using the first or last occurence.
  - `word_delimiters`. (Optional, default = " "). Characters that must be used as delimeters for separating words.

## 4.6 TextFileDiffCheck
Checks that two test files match exactly.
  - `gold_file`. Path to the file who has the golden content.
  - `check_file`. Path to the file that needs to match the gold_file.
  - `inverse`. If true the check will only pass if the files do NOT match.
