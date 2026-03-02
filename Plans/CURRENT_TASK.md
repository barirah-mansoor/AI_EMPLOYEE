---
status: idle
task: ""
iterations: 0
created: ""
updated: ""
---

# Current Task

No active task. Use this file to track long-running tasks.

## Usage

When starting a multi-step task:

1. Update the frontmatter:
```yaml
---
status: in_progress
task: "Build Gold Tier System"
iterations: 0
created: "2026-02-24T10:00:00"
updated: "2026-02-24T10:00:00"
---
```

2. Work on the task until complete

3. When done, update status:
```yaml
---
status: done
task: "Build Gold Tier System"
iterations: 5
updated: "2026-02-24T12:00:00"
---
```

## Ralph Wiggum Pattern

This file enables the Ralph Wiggum Stop hook. When Claude tries to exit while this file shows `status: in_progress`, it will be blocked and instructed to continue working.

Set `MAX_ITERATIONS=10` environment variable to prevent infinite loops.
