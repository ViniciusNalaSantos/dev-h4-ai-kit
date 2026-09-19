# dev-h4-ai-kit

Reusable agent skills for Codex and compatible coding agents.

## Use the skills in another repository

Run `use_agents.py` from anywhere and pass the target repository:

```powershell
python C:\path\to\dev-h4-ai-kit\use_agents.py C:\path\to\another-project
```

On macOS or Linux, the equivalent is:

```bash
python3 /path/to/dev-h4-ai-kit/use_agents.py /path/to/another-project
```

If the target is your current directory, omit the final argument:

```powershell
python C:\path\to\dev-h4-ai-kit\use_agents.py
```

The default mode copies the skills into `.agents/skills` and merges their
metadata into `skills-lock.json`. Existing unrelated skills and lock entries
are preserved.

Useful options:

- `--list`: list the skills supplied by this kit.
- `--dry-run`: preview changes without writing them.
- `--force`: replace same-named skills that differ in the target repository.
- `--mode symlink`: link to this kit so updates are immediately shared. On
  Windows this may require Developer Mode or an elevated terminal.

Run `python use_agents.py --help` for the complete command reference.
