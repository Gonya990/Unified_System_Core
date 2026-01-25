# Commit Message Style

Format: `<type>(<scope>): <description>`

## Types
| Type | Use for |
|------|---------|
| `feat` | New feature or capability |
| `fix` | Bug fix or correction |
| `refactor` | Code restructuring (no behavior change) |
| `chore` | Maintenance, cleanup, dependencies |
| `flake` | Nix flake changes (update, lock) |

## Scope
Optional but preferred. Use module/component name.
- `feat(tailscale):` `fix(rocinante):` `chore(home):`
- Flake updates: `flake(update)`

## Description
- Lowercase, no period, imperative mood ("add" not "added")

## Examples
```
feat(rocinante): enable direnv with nix-direnv
fix(tailscale): use ts.net catch-all for MagicDNS split DNS
refactor: migrate zed-editor to use nixpkgs-unstable
chore: cleanup home.nix aliases
flake(update): nix-ai-tools
```

## Avoid
- Vague: `Update files`, `Fixed bug`, `misc changes`
- WIP commits

---
*Setup: See [SETUP.md](commit-style/SETUP.md)*
