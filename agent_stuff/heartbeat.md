# HEARTBEAT.md - Proactive Background Tasks

## Active Tasks

### Periodic Health Checks
- **Frequency:** Every 5 minutes
- **Action:** Check Ollama connection status
- **On Failure:** Log error, notify user

### Memory Maintenance
- **Frequency:** Every 30 minutes
- **Action:**
  - Summarize old experiences
  - Archive outdated temporary memories
  - Update MEMORY.md with synthesized learnings
- **On Completion:** Log statistics

### Log Rotation
- **Frequency:** Daily at midnight
- **Action:**
  - Rotate agent.log if > 10MB
  - Archive old logs to logs/archive/
  - Create new log file

### Device Status Polling
- **Frequency:** Every 60 seconds
- **Action:**
  - Check registered device states
  - Update device state cache
  - Detect offline devices

---

## Scheduled Routines

### Hourly Tasks
| Time | Task | Description |
|------|------|-------------|
| :00 | Experience Summary | Compile last hour's experiences |
| :00 | Security Log Review | Check for denied operations |

### Daily Tasks
| Time | Task | Description |
|------|------|-------------|
| 00:00 | Log Rotation | Rotate and archive logs |
| 00:00 | Memory Optimization | Vacuum SQLite database |
| 08:00 | Morning Report | Summarize overnight activity |
| 20:00 | Evening Summary | Daily experience synthesis |

### Weekly Tasks
| Day | Time | Task |
|-----|------|------|
| Sunday | 00:00 | Full memory backup |
| Sunday | 00:00 | Review and update MEMORY.md |

---

## Autonomous Behaviors

### When Idle
- Review recent memories for patterns
- Consider self-improvement opportunities
- Check heartbeat tasks for updates
- Update AGENT.md with current state

### On Event Triggers
- **Security Alert:** Immediate security log review
- **Device Offline:** Attempt reconnection
- **Memory Threshold:** Trigger memory optimization
- **Error Spike:** Analyze error patterns

---

## Task Priority Levels

1. **Critical** (Execute immediately)
   - Security violations
   - System errors
   - User emergency requests

2. **High** (Execute within 5 minutes)
   - Connection failures
   - Device malfunctions
   - Memory capacity warnings

3. **Normal** (Execute on schedule)
   - Regular health checks
   - Log maintenance
   - Experience summaries

4. **Low** (Execute when idle)
   - Pattern analysis
   - Self-improvement research
   - Archive cleanup

---

## Task Modification

To add new tasks:
1. Add to "Active Tasks" or "Scheduled Routines"
2. Specify frequency and action
3. Set priority level
4. Agent will pick up on next heartbeat cycle

To mark task complete:
- Move task from "Active Tasks" to "Completed Tasks" section
- Include completion date and outcome

---

## Completed Tasks

<!-- Move completed tasks here:

Example:
- [2026-06-13] Initial heartbeat system setup - COMPLETED
-->

---

## Last Updated
2026-06-13

*This file is checked periodically by the agent. Tasks are executed based on schedule and priority.*
