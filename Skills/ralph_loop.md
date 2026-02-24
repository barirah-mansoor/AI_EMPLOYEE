# Ralph Loop Skill

**Mode:** AUTO-EXECUTE
**Trigger:** Long-running multi-step tasks
**Hook:** Claude Code Stop hook

## Purpose

The Ralph Wiggum pattern prevents Claude Code from stopping mid-task. It uses a Stop hook that checks the current task status before allowing exit.

## How It Works

1. When Claude tries to exit (Stop command), the hook runs `ralph_wiggum.py`
2. The script checks `Plans/CURRENT_TASK.md`
3. If status is `in_progress` → blocks exit, instructs to continue
4. If status is `done` → allows exit, cleans up
5. If file doesn't exist → allows exit

## Usage

### Starting a Task

Before starting a multi-step task, update `Plans/CURRENT_TASK.md`:

```yaml
---
status: in_progress
task: "Build MCP Servers"
iterations: 0
created: "2026-02-24T10:00:00"
---
```

### Working on Task

Work on the task normally. Each iteration is logged.

### Completing a Task

When finished, update the status:

```yaml
---
status: done
task: "Build MCP Servers"
iterations: 3
updated: "2026-02-24T11:30:00"
---
```

### Ralph Wiggum Pattern

The Ralph Wiggum approach means:
- **Never stop mid-task** - keep working until truly done
- **Track iterations** - prevent infinite loops with MAX_ITERATIONS
- **Log progress** - each iteration is logged to `Logs/ralph_wiggum.json`

## Commands

```bash
# Test the Ralph Wiggum hook
python3 ralph_wiggum.py

# Set custom max iterations
MAX_ITERATIONS=20 python3 ralph_wiggum.py
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| MAX_ITERATIONS | 10 | Maximum iterations before allowing exit |
| VAULT_PATH | /mnt/c/Users/Admin/AI_Employee_Vault | Path to vault |

## Ralph Wiggum Philosophy

From The Simpsons: Ralph Wiggum says "I'm in danger!" even when he's not. This pattern is about being overly cautious - blocking exit even when things seem done, until the task is truly complete.

**Remember:** It's better to complete one task than to start three and finish none.
