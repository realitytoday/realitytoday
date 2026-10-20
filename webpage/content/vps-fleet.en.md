# Your Whole Server Fleet in One Terminal Window: vps-fleet

*A blueprint and the prompts for a keyboard-driven SSH cockpit, plus the finished Go code.*

## Intro

I run a handful of small servers: a web box, a database, a VPN gateway and a few
hobby VPS. Checking them meant one SSH tab each, and the question "is anything full,
overloaded or waiting for a reboot?" took ten tabs and ten commands. Monitoring stacks
answer it, but they are servers of their own that you must run, secure and update.

So I built a cockpit: one terminal window that shows every server's health at a glance,
and the same window is enough to fix what it shows. Look at the live processes, kill the
runaway one, restart the service, move a file. It uses the SSH access you already have and
installs **nothing** on the servers.

I built it in a few days with AI coding agents. Unlike my other blueprints, this one comes
in two parts: the **prompts and reasoning** (this guide and the blueprint repo), and the
**finished code** (the code repo), so you can either use it as it is or have your agent build
a version tuned to your own servers.

**Time:** an evening to read and try it, a weekend to build your own version.
**Skill level:** comfortable with a terminal and SSH keys. The agent writes the code.
**Cost:** nothing but the servers you already have.

## What it does

- **Fleet overview:** every server with CPU, memory and disk bars, load, uptime and alerts for
  failed services, full disks, high load, pending updates and a required reboot. Table or cards,
  groups, live filter, sorting.
- **Dashboard:** five-minute trend lines, disk and network throughput, and a live top-style
  process list beside it.
- **Top view and kill:** a full-screen process list; send any signal to any process.
- **Command runner:** commands with a persistent working directory and aliases, history,
  reverse search and tab completion of remote paths.
- **Systemd manager:** list units, start, stop, restart.
- **File manager:** local and remote side by side, upload and download with progress, view,
  delete, chmod, chown, chgrp.
- **Profiles:** separate server lists for work, home or customers.
- **Add servers in the app:** a form with validation, no file editing needed.

## The decisions that matter

**Agentless.** If you can `ssh` into a server, it can be managed: no daemon, no exporter, no
open port. The price is that every number comes from a shell command on each poll, so the
metrics script is designed carefully: one SSH session, one prefixed line per metric, parsed by
prefix and not by position.

**Never trust the first `top` frame.** Its CPU is averaged since the process started. The tool
runs `top` twice and keeps the second frame, and falls back to `ps` on minimal systems like
Alpine, where it says so.

**Quote everything.** A file called `$(reboot).txt` on a server must not run on your next
delete. Every value that goes into a remote command, including names that came from the server
itself, is single-quoted and preceded by `--`.

**Verify host keys.** My first version skipped the check. It was the first thing I fixed before
publishing: the tool now remembers a server on first contact and refuses it if its key ever changes.

## Build it with your agent

Start with the project brief: put `prompts/00-project-brief.md` into a new repository as
`CLAUDE.md` or `AGENTS.md` and fill in the placeholders. Then give the agent the six prompts in
order, one per session, and run each prompt's acceptance checks against a real server before moving on:

1. Foundation and SSH: config and profiles, the SSH client, host keys, the quoting helper.
2. Metrics and fleet overview: the metrics script, health and alerts, sorting and filtering.
3. Dashboard and processes: trends, process list, the top view and the kill dialog.
4. Command runner and systemd manager.
5. The two-pane file manager.
6. Profiles, settings and the release checklist.

Test on at least two kinds of server (for example Debian and Alpine). Parsers that work on one
distribution's output often break on another's.

## Run the finished version

You need Go to build it. On Linux or macOS:

```sh
git clone https://github.com/realitytoday/vps-fleet-tui.git
cd vps-fleet-tui
go build -o vps-fleet ./cmd/vps-fleet
./vps-fleet
```

On Windows the output file needs the `.exe` ending, otherwise Windows will not run it:

```powershell
go build -o vps-fleet.exe ./cmd/vps-fleet
.\vps-fleet.exe
```

Add your servers from inside the app: press `a` (or open the config screen with `c` and choose
"+ Add a server"), fill in name, host, user, port and key file, and press `ctrl+s`. The server connects
right away. You can also edit `~/.config/vps-fleet/config.yaml` by hand. Prefer SSH keys over the
`password` field, which is stored as plain text.

## What is not finished

The command runner runs single commands, so it is not a full interactive terminal and programs
like `vim` or `htop` do not work in it. Copying whole folders in the file manager is not built,
and neither are a WireGuard plugin, a help overlay or log viewing. There is no history and no
alerting when the window is closed: it is a cockpit, not a monitoring system. Windows servers
are out of scope. Better to say so than to let you rely on something that does not exist.

## Get the blueprint

The prompts, architecture, key map and lessons learned are in the blueprint repo; the finished
Go code is in the code repo.
