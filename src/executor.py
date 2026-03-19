import shlex

from src.filesystem import get_user_dir

from src.helpers.executor import *


PASSTHROUGH = [
    "ls", "mkdir", "rm", "cp", "mv", "ln", "touch",
    "cat", "head", "tail", "wc", "file", "diff", "stat", "du",
    "echo", "printf", "sort", "uniq", "cut", "tr", "sed", "tee", "xxd",
    "pwd", "whoami", "date",
    "find", "tree", "basename", "dirname", "realpath", "sleep", "seq",
    "xargs", "which", "type",
]


HELP_TEXT = """Available commands

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

Tip: use !help for this message"""

async def handle_command(raw: str, user_id: str, username: str, message) -> list:
    try:
        parts = shlex.split(raw)
    except Exception as e:
        return ["Send text", f"Error while parsing command: {e}"]

    if not parts:
        return ["Send text", ""]

    cmd = parts[0]
    user_dir = get_user_dir(user_id)

    if cmd == "help":
        return ["Send text", HELP_TEXT]
    elif cmd == "nano":
        return ["Send text", handle_nano(parts, user_dir, user_id)]
    elif cmd == "cd":
        return ["Send text", handle_cd(parts, user_id)]
    elif cmd == "grep":
        return ["Send text", await handle_grep(parts, user_id, username)]
    elif cmd == "upload":
        return ["Send text", await handle_upload(message, user_id)]
    elif cmd == "get":
        return ["Send attachment(s)", await handle_get(user_id, parts[1:])]
    elif cmd in PASSTHROUGH:
        return ["Send text", await run_subprocess(parts, user_id, username)]

    return ["Send text", f"bash: {cmd}: command not found"]