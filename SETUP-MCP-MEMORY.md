# 🧠 MCP Memory Integration Setup Guide

Enable persistent memory for AI agents with slash command activation in Claude Code.

## What This Enables

✅ **Persistent Agent Memory** - Agents remember decisions, deliverables, and context across sessions
✅ **Slash Command Activation** - Quick `/frontend`, `/backend`, `/qa` shortcuts to activate agents
✅ **Cross-Agent Handoffs** - Seamless context passing between specialized agents
✅ **State Rollback** - Recover to known-good states when changes fail QA

## Quick Start (5 minutes)

### Step 1: Install MCP Memory Server

```bash
# Copy the memory server to Claude Code
cp mcp-memory-server.py ~/.claude/

# Make it executable
chmod +x ~/.claude/mcp-memory-server.py
```

### Step 2: Update Claude Code Settings

```bash
# Copy the enhanced settings file
cp claude-code-settings.json ~/.claude/settings.json

# Or manually update ~/.claude/settings.json to include:
{
  "mcpServers": {
    "memory": {
      "command": "python3",
      "args": ["~/.claude/mcp-memory-server.py"]
    }
  }
}
```

### Step 3: Verify Installation

In any Claude Code session, type:

```
/frontend
```

You should see the Frontend Developer agent activated with memory integration ready.

## Slash Command Reference

### Engineering Division
- `/frontend` - Frontend Developer (UI/UX implementation)
- `/backend` - Backend Architect (system design & APIs)
- `/devops` - DevOps Automator (infrastructure & CI/CD)
- `/ai` - AI Engineer (ML/data systems)
- `/security` - Security Engineer (threat assessment)
- `/lead` - Software Architect (technical leadership)
- `/data` - Data Engineer (data pipelines)
- `/sre` - SRE (reliability engineering)

### Design Division
- `/design` - UX Architect (design systems)
- `/brand` - Brand Guardian (brand identity)

### Quality & Testing
- `/qa` - Evidence Collector (quality assurance)
- `/test` - Tool Evaluator (testing strategy)
- `/api` - API Tester (endpoint validation)

### Business Division
- `/product` - Product Manager (strategy & prioritization)
- `/sales` - Sales Coach (revenue growth)
- `/marketing` - Content Creator (campaigns)
- `/strategy` - Agents Orchestrator (workflow coordination)

## Using Persistent Memory

Once an agent is activated, use these memory operations:

### Remember (Store Context)
When an agent completes important work, it automatically stores context:

```
[Agent remembers decision]
"Remember: Implemented JWT authentication with RS256 signing.
Tags: backend, security, [project-name]
Context: Session ID xyz, decision made at phase-2"
```

### Recall (Retrieve Context)
At the start of a session, agents recall relevant context:

```
Recall from previous sessions:
- JWT authentication pattern established (Session xyz)
- Database schema approved for production (Session abc)
- API rate limiting: 1000 req/min per tier
```

### Handoff (Pass Context to Next Agent)
When handing off to another agent, context flows automatically:

```
Developer → QA handoff:
"Remember: Task #42 implementation complete.
Tags: task-42, frontend, ready-for-qa, [project-name]
Context: Feature branch feature/42, commit abc123def"
```

QA agent immediately recalls this context without manual copy-paste.

### Rollback (Recover Failed State)
If QA fails and feedback requires architectural changes:

```
Rollback to: Memory ID 847 (Last known-good state)
Restore: Design decisions before failed refactor attempt
Recover: All context from phase-1 completion
```

## Complete Workflow Example

### Day 1: Backend Implementation
```
1. Activate: /backend
2. Backend Architect implements API endpoints
3. Remembers: Architecture decisions, database schema, authentication pattern
4. Handoff: Tags context for QA team with task ID
```

### Day 2: QA Validation
```
1. Activate: /qa
2. Evidence Collector recalls context from Day 1
3. Validates implementation against spec
4. If PASS: Remembers successful QA result
5. If FAIL: Provides feedback, Developer rolls back and retries
```

### Day 3: Frontend Integration
```
1. Activate: /frontend
2. Frontend Developer recalls:
   - API endpoints and contracts from Day 1
   - Styling standards and design system
   - Authentication pattern decisions
3. Builds UI without manual context copying
```

## Memory Storage

All agent memories are stored in:
```
~/.claude/agent-memory.db
```

View your memory history:
```bash
sqlite3 ~/.claude/agent-memory.db "SELECT timestamp, agent_name, content FROM memories ORDER BY timestamp DESC LIMIT 10;"
```

Search memories:
```bash
sqlite3 ~/.claude/agent-memory.db "SELECT * FROM memories WHERE content LIKE '%JWT%';"
```

## Advanced: Custom Agent Memory

Add memory integration to any agent by including this section:

```markdown
## 🧠 Memory Integration

When you start a session:
- Recall relevant context from previous sessions using search terms: [agent-name], [project-name], [current-task]
- Review decisions and deliverables tagged with your role
- Check for any rollback states if previous attempts failed

When you make key decisions:
- Remember important architectural decisions
- Remember completed deliverables with task IDs
- Tag memories with: [agent-name], [project-name], [task-id]

When handing off to another agent:
- Remember your completion status and what's pending
- Tag for the receiving agent: [receiving-agent-name], [project-name], [task-id]
- Include specific handoff information: what's done, what's blocked, what's next

When a task fails QA:
- Retrieve the last successful state using rollback
- Start improvements from known-good foundations
- Document what changed and why
```

## Troubleshooting

### MCP Server Not Starting
```bash
# Test the server directly
python3 ~/.claude/mcp-memory-server.py
# Should not error when connecting

# Check Python installation
python3 --version
# Should be 3.7+
```

### Memory Database Issues
```bash
# Backup and reset memory
cp ~/.claude/agent-memory.db ~/.claude/agent-memory.db.bak
rm ~/.claude/agent-memory.db

# Fresh database will be created on next agent activation
```

### Slash Commands Not Working
1. Verify settings.json has `agentActivation: { enabled: true }`
2. Check agent config file exists: `.claude-agents-config.json`
3. Restart Claude Code session
4. Try explicit agent name: `/engineering-backend-architect`

## Architecture

The memory system consists of:

```
User Input (/frontend)
    ↓
Slash Command Handler
    ↓
Agent Config Lookup
    ↓
Agent File Loading
    ↓
Agent Activation with Memory Integration
    ↓
MCP Memory Server (~/.claude/agent-memory.db)
    ├─ remember(content, tags, context)
    ├─ recall(search_term, agent_name)
    ├─ search(query)
    └─ rollback(memory_id)
```

## Security & Privacy

- All memories stored locally in `~/.claude/`
- No cloud storage or external APIs
- Database encrypted with SQLite native encryption (optional)
- Memory visible only to your Claude Code sessions
- Can be cleared anytime: `rm ~/.claude/agent-memory.db`

## Integration with NEXUS Pipeline

For full NEXUS workflow automation with memory:

```bash
# Activate orchestrator with full pipeline memory
/strategy

# Create sprint plan with memory persistence
/product

# Implement with developer agent memory
/backend
/frontend

# Validate with QA memory
/qa
/test

# Deploy with DevOps memory
/devops
```

Each agent automatically:
1. Recalls previous decisions and context
2. Executes their phase
3. Remembers deliverables for next agent
4. Hands off with full context preservation

## Next Steps

1. ✅ Install MCP Memory Server
2. ✅ Update Claude Code settings
3. ✅ Try `/frontend` to verify activation
4. ✅ Use an agent and observe memory recall on next session
5. ✅ Create a multi-agent workflow with persistent context

---

**Questions?** See `integrations/mcp-memory/README.md` for detailed documentation.
