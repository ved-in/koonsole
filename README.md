# Koonsole

A discord terminal app which can be used to run commands
current commands:
cd, ls, mkdir, nano, grep, cat, upload, get

## Usage

use the format:
`!<command> <params>`

## Changelong since previous commit

- `!get` command added
- Instead of manually importing all functions in `src.executor` from `src.helpers.executor`, now u can just use `from src.helpers.executors import *` for ease


## Current Errors/Bugs/Pending Features

[o] Add rename command
[2] Add rm command... would be risky and need a WHOLEEE lotta tests to see if it aint just a command which would delete files OUTSIDE of the selected user-directory. Could instead also add a "dummy" rm command which is handled manually instead of using subprocess. Would also need to handle prompts like "yes or no"