# grading-tools
Python functions to help me deal with an awful assignment submission process.

## Usage
`grading-tools.py [--mode MODE] [--points POINTS] [--questions QUESTIONS] [--path PATH]`

- `MODE` should be one of "c" (create) or "s" (score). The default is "c".
- `POINTS` should be an integer > 0 specifying the possible points for the assignment. The default is 60.
- `QUESTIONS` should be an integer > 0 specifying the number of questions in the assignment. The default is 10.
- `PATH` should represent the path to a directory containing a text file with student names and perms. If no path is provided, the current working directory will be used.
