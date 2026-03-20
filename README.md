# Koonsole

A discord terminal app which can be used to run commands
current commands:
cd, ls, mkdir, nano, grep, cat, upload, get

```bash
Available commands

[Navigation]
  cd <dir>        Change directory
  pwd             Print current directory

[Files]
  ls [dir]        List files
  mkdir <dir>     Create directory
  touch <file>    Create empty file
  rm <file>       Remove file or directory
  cp <src> <dst>  Copy file
  mv <src> <dst>  Move or rename file
  ln <src> <dst>  Create link
  stat <file>     File details
  du [file]       Disk usage
  file <file>     Detect file type

[Reading]
  cat <file>      Print file contents
  head <file>     Print first lines
  tail <file>     Print last lines
  wc <file>       Count lines, words, chars
  diff <f1> <f2>  Compare two files
  xxd <file>      Hex dump

[Text]
  echo <text>     Print text
  printf <fmt>    Print formatted text
  sort            Sort lines
  uniq            Remove duplicate lines
  cut             Extract columns
  tr              Translate characters
  sed             Stream editor
  tee             Read stdin, write to file and stdout
  grep <pat>      Search for pattern

[Editor]
  nano <file>     Edit file contents
                  Send next message as file content
                  Use .cancel to abort

[Upload/Download]
  upload          Upload a Discord attachment to your home dir.
                  Attach a file to the same message
  get <file(s)>   Send file(s) back to user in Discord

[Utils]
  find            Search for files
  tree            List files as tree
  seq <n>         Print sequence of numbers
  sleep <n>       Wait n seconds
  basename <path> Strip directory from path
  dirname <path>  Strip filename from path
  realpath <path> Resolve absolute path
  which <cmd>     Locate a command
  xargs           Build commands from stdin
  date            Print current date and time
  whoami          Print current username

Tip: use !help for this message
```

## Usage

use the format:
`!<command> <params>`

## Changelong since previous commit

- Imported helper executor functions as `execs.<func_name>` to prevent warnings in IDE
- `nano` now sends the file contents as a file both while editing and after u send content

## Current Errors/Bugs/Pending Features

[o] No piping commands support. Honestly no one would really need them in the bot but would see what I can do. Piping does seem to be necessary. `!echo "note content > note.txt` does not work..

[o] `!nano /home/<username>/my_project/note.txt` does not work because nano would consider it to be relative path which does not exist.

[o] Make `nano` accept entire edited file as content instead of triple backticks ORR make it optional through a flag?