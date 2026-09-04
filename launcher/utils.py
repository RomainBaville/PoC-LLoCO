# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import os
import platform
import signal
import subprocess


def start_process( command: list[ str ], title: str ) -> int:
    """Start a process in a new terminal window.

    Args:
        command (list[str]): The command to execute in the new terminal.
        title (str): The title of the terminal to open.

    Returns:
        int: The subprocess PID
    """
    match platform.system():

        case "Windows":
            command_str: str = subprocess.list2cmdline( command )
            process = subprocess.Popen(
                [ "cmd.exe", "/k", f"title { title } && { command_str }" ],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
            return process.pid

        case "Linux":
            terminals: list[ str ] = [ "gnome-terminal", "konsole", "xfce4-terminal", "xterm" ]
            for terminal in terminals:
                try:
                    process = subprocess.Popen( [
                        f"{ terminal }",
                        f"--title={ title }",
                        "--",
                        *command,
                    ] )
                    return process.pid
                except Exception:
                    continue
            raise LookupError( "No Linux terminals fund." )

        case _:
            raise NotImplementedError( f"Unsupported operating system: {platform.system()}" )


def stop_process( process_pid: int ) -> None:
    """Close the process.

    Args:
        process_pid (int): The pid of the Popen subprocess to stop and close.
    """
    match platform.system():

        case "Windows":
            subprocess.run(
                [ "taskkill", "/PID", str( process_pid ), "/T", "/F" ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        case "Linux":
            killpg = getattr( os, "killpg" )  # noqa: B009
            killpg( process_pid, signal.SIGTERM )

        case _:
            raise NotImplementedError( f"Unsupported operating system: { platform.system() }" )
