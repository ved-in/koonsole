# Koonsole

A discord terminal app which can be used to run commands
current commands:
ls, mkdir, nano, cd

## Usage

use the format:
`!<command> <params>`

## Changelong since previous commit

- Added `!grep` command
- `users_current_dir` gets stored in a json located at `data/cwds.json` to persist if bot crashes at some point of time. The json is updated everytime a user calls a cd command which succeeds
- Refactored code to multiple files per command

(fixed spelling mistake :P)


## Current Errors/Bugs/Pending Features

[o] `!upload`, `!view`

[o] Set particular channels only in which the bot can read messages
