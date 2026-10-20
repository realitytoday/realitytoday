# Which AI Model and Agent Should You Use?

*Practical guidance for building the blueprints on this site with a coding agent.*

## Why the model matters

The prompts in my blueprints are written for a coding **agent**, not a chat window. The agent has to read a brief, plan changes across several files, run commands, read error messages and keep the project's rules in mind over a long session. Models differ a lot at exactly that. The same prompt can give a working backend with one model and a plausible-looking mess with another.

Model names and rankings change every few months, so this page talks about classes of models, not versions. Check what is current before you start.

## The short recommendation

Use the **strongest frontier model you have access to**: Claude Opus or a comparable top-tier model from another vendor. Spend it where mistakes are expensive: the architecture, the backend, and anything that touches hardware, Linux desktop settings or deployment. For the repetitive parts, such as UI polish, small fixes and the admin page, a mid-tier model (a Sonnet-class or similar model) is usually fine and cheaper. Smaller or open-weight models can work too, but expect to split the work into smaller steps and to check more.

A rule of thumb, based on my own experience and not on a benchmark:

| Part of the Home Information Screen | What it demands of the model | Suggested tier |
|---|---|---|
| Backend and the integration pattern (cache, stale data, fallback) | Consistent design across many files, discipline about constraints | Top tier |
| Integrations (calendar recurrence, presence, webhooks, sensors) | Careful reading of protocols and edge cases | Top or mid tier |
| Pi setup (Wayland, touch mapping, systemd, backlight) | Obscure, version-specific Linux knowledge, debugging from logs | Top tier |
| Screen UI and design system | Following many small style rules at once | Mid tier is often enough |
| Motion/sleep service | Small program, but a reference implementation is provided | Mid tier |
| Docker image and deployment | Well-known patterns, but unforgiving | Mid tier |
| Admin page | Routine forms and CRUD | Mid tier |

## Tips that work with any agent

- **Keep a short project brief** (`CLAUDE.md` or `AGENTS.md`) with the fixed decisions: architecture, stack, security rules and design rules. The blueprint ships a template for both file names. One page that the agent reads every session beats a long wiki it ignores.
- **One prompt per session or task.** Do not paste all prompts at once. Finish a piece, test it on the real device, commit, then continue.
- **Give the agent the reference files.** The `reference/` folder exists because exact scripts and contracts beat descriptions.
- **Make it plan first.** Ask for a short plan and read it before any code is written. Corrections are cheaper at that point.
- **Run things and feed the output back.** Build, test and look at logs yourself or let the agent do it, and paste real error messages instead of describing them.
- **Commit often.** If a session goes wrong, you want a clean point to return to.
- **Keep a decision log.** Dated entries for decisions and mistakes. It becomes the context you can hand to a fresh session.
- **Restart long sessions.** When the agent starts forgetting rules or repeating mistakes, start a new session with the brief and the decision log.
- **Do not let it weaken security to make something work.** The blueprint's rule is: never turn TLS verification off.

## Tips for Mistral Vibe and similar agents

Mistral's agent is a good choice if you prefer a European provider or want to keep options open. I have not tested these blueprints end to end with it, so treat the following as sensible starting points rather than verified results.

- **Check which brief file it reads** (`AGENTS.md` is a common convention) and put the project brief there. The blueprint ships an `AGENTS.md`.
- **Use smaller steps.** Split each blueprint prompt into sub-tasks, for example "data model and storage" first, "calendar integration" second. Give one task, one list of files, one goal.
- **Name the files and the stack explicitly.** Say "Go, standard library only, one YAML file per store" in every task rather than relying on the agent to remember it.
- **Paste or point to the reference material** for anything with exact behaviour, such as the Pi scripts and the API contract.
- **Ask for the plan, then review it.** Weaker models more often start coding on a wrong assumption.
- **Verify more.** Run the tests and the build after every step, and test on the real hardware before moving on.
- **Escalate the hard problems.** If you are stuck on Wayland rotation, touch mapping or a systemd unit, give that one problem to a top-tier model, then continue with your preferred agent.
- **Keep the context small.** Open a fresh session per task and reuse the brief and the decision log.

## If something goes wrong

If the output is plausible but wrong, the cause is usually one of three things: the task was too big, a rule from the brief was lost, or the model lacked knowledge about the specific hardware or software version. Make the task smaller, restate the rule, or switch to a stronger model for that step.
