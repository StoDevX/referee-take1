> This folder contains a subfolder for each course that `referee` is expected to referee. Each course folder contains `specs`, which detail what is expected for each assignment.


# The `spec` spec

Specs are YAML files, because it's nice. I will refer you to Eevee's YAML guide for how to write YAML: [https://camel.readthedocs.io/en/latest/yamlref.html][camel]

[camel]: https://camel.readthedocs.io/en/latest/yamlref.html

Read it? Good.

Each spec file has some required keys:

`key`         | purpose
--------------|---------
`assignment`  | The name of the assignment, ie. `hw11` or `lab12`.
`folder`      | The folder to find this assignment in. It defaults to the value of`assignment`.
`compilers`   | A list of compiler aliases for use in the file.
`deadline`    | Reserved for future use.
`due`         | Reserved for future use.
`files`       | A list of files. Files are specced later.
`input_files` | A list of files to copy from sample_files into the user's directory during the tests.
`options`     | Deprecated.
`tests`       | Pairs of (file, tests) to run

There are four really important keys here: `assignment` / `folder`, `compilers`, `files`, and `tests`.

## Assignment / Folder

The system uses `folder` to figure out where the student should have put their submission. If `folder` isn't present, it's assumed to be equal to `assignment`.

## Compilers

`compilers` is a list of YAML references. Each item in the list is a string that can be executed to do something to a file. It's kind of a misnomer; it doesn't have to be a compiler.

YAML references take any item that's prefixed with `&` and make it re-usable in the file. Any time you have the reference prefixed with `*`, you get the value of the reference.

    - &a I'm a string
    - *a

is equivalent to

    - I'm a string
    - I'm a string

## Files

`files` is a list of files that are expected to exist. Each item is an array, where the first item is the filename, and the rest are options that affect how that file is processed. If any options are strings, they are interpreted as compiler commands, and the command is invoked. Any options that are dictionaries are merged into the options object.

Valid options are `timeout`, `truncate_output`, `truncate_contents`, and `optional`.

`key`               | Default   | Description
--------------------|-----------|-------------
`timeout`           | 4 seconds | A timeout for running the submitted code.
`truncate_output`   | 10kb      | How much of the output should be shown?
`truncate_contents` | false     | How much of the content should be shown?
`optional`          | false     | Is the file optional?
`alternate_names`   | []        | What other names might this file be under? Note that the system is case-sensetive, but will log a warning

Examples:

    files:
        - [ file1.cpp, *cpp, optional: true ]


## Tests

Just like `files`, `tests` is a list of lists. The first item in each list is the filename, and the rest of the list is either commands or options.

There are not currently any options for test files.

## Commands

Commands for both `files` and `tests` are kind of special.

- The symbol `$@` is replaced with the current filename, just like in a Makefile.
- I had to implement a few shell features manually. I once piped the commands directly into the shell, but one student managed to break that functionality.
    - You can `|` pipe between command. stdin and stdout redirection are not supported; use `cat` to pipe to stdin, and `tee file` to put stdout in `file`.
    - File globs are supported, I think.


    tests:
      - - stddev.cpp
        - cat firefox.txt | $@.exec
        - cat avg-first-firefox.txt | $@.exec

This will run two tests for `stddev.cpp`: the first one pipes the contents of `firefox.txt` to `stddev.cpp.exec`, and the second test pipes `avg-first-firefox.txt` into `stddev.cpp.exec` (the same file).


# Example

```yaml
---
assignment: hw18

compilers:
  - &cpp 'g++ --std=c++11 $@ -o $@.exec'
  - &cpp-to-obj 'g++ --std=c++11 -c $@'

files:
  - [ DVD.h, null ]
  - [ DVD.cpp, *cpp-to-obj ]
  - - DVDdriver.cpp
    - *cpp-to-obj
    - g++ --std=c++11 DVD.o DVDdriver.o -o $@.exec

tests:
  - [ DVDdriver.cpp, $@.exec ]
```

This is an actual file.

DVD.h will not be compiled; it will existence-checked, style-checked, and linted.

DVD.cpp will also be compiled, with the (fleshed-out) command `g++ --std=c++11 -c DVD.cpp`.

DVDDriver.cpp will have two commands run on it: `g++ --std=c++11 -c DVDDriver.cpp`, and `g++ --std=c++11 DVD.o DVDdriver.o -o DVDDriver.cpp.exec`.

Thus, we can see that the order that files are put into the files array matters.

This assignment also has one test: it runs `DVDDriver.cpp.exec`.
