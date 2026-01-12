
### Project-Specific Issue Trackers

Some large sub-projects use their own Beads database to keep the root tracker clean.

| Project | Database Path | Access Command |
|---------|---------------|----------------|
| **global1sim** | `Projects/global1sim/.beads/beads.db` | `bd --db Projects/global1sim/.beads/beads.db list` |

**Tip:** To work exclusively on `global1sim` issues, you can set the `BEADS_DB` environment variable:
```bash
export BEADS_DB=Projects/global1sim/.beads/beads.db
bd list
```
