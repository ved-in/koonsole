def format_output(cmd: str, username: str, result: str) -> str:
    safe_user = username.replace(" ", "").lower()[:20]

    output_body = result if result else ""

    return (
        "```bash\n"
        f"{safe_user}@koonsole:~$ {cmd}\n"
        f"{output_body}\n"
        "```"
    )