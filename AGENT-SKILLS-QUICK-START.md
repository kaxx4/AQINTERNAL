# 🎭 Agent Skills - Quick Start Guide

You now have 189 specialized AI agents with persistent memory enabled through slash commands in Claude Code.

## Installation (2 minutes)

```bash
# 1. Copy memory server to Claude Code
cp mcp-memory-server.py ~/.claude/

# 2. Update Claude Code settings
cp claude-code-settings.json ~/.claude/settings.json

# 3. Restart Claude Code
# Done! Memory is now active
```

## Using Slash Commands

Type any of these in Claude Code to instantly activate an agent with persistent memory:

### Quick Shortcuts

**Engineering** | **Design** | **QA** | **Business**
---|---|---|---
`/frontend` | `/design` | `/qa` | `/product`
`/backend` | `/brand` | `/test` | `/sales`
`/devops` | | `/api` | `/marketing`
`/ai` | | | `/strategy`
`/security` | | |
`/lead` | | |
`/data` | | |
`/sre` | | |

## What This Enables

### ✅ Persistent Memory Across Sessions
```
Session 1: /backend builds API
→ Remembers: API schema, authentication pattern, database decisions

Session 2: /frontend starts
→ Automatically recalls: API contracts from backend work

Session 3: /qa validates
→ Recalls: What should be tested, previous QA feedback
```

### ✅ Cross-Agent Handoffs
```
Backend → Frontend: "API endpoints ready at /api/v1/..."
Frontend → QA: "Feature complete, ready for validation"
QA → Next Phase: "Validated, X issues found, Z fixed"
```

### ✅ Rollback on Failure
```
QA finds critical issue
→ Developer rolls back to last successful state
→ Saves time rebuilding from scratch
```

## Workflow Example: Building a Feature

### Step 1: Design System (Day 1)
```
/design
"Design a product detail page for e-commerce site"

UX Architect creates:
- Component library
- Design tokens
- Responsive breakpoints
```

### Step 2: Backend (Day 2)
```
/backend
"Implement product API endpoints"

Backend Architect:
- Recalls design decisions
- Creates API endpoints
- Documents contracts
```

### Step 3: Frontend (Day 3)
```
/frontend
"Build product detail page using the API"

Frontend Developer:
- Recalls component library
- Recalls API contracts
- Recalls authentication pattern
- Implements without manual copy-paste
```

### Step 4: QA (Day 4)
```
/qa
"Validate product page implementation"

Evidence Collector:
- Recalls what was supposed to be built
- Takes screenshots
- Tests interactions
- Reports issues or approves
```

### Step 5: DevOps (Day 5)
```
/devops
"Deploy to production"

DevOps Automator:
- Recalls deployment specs
- Recalls performance targets
- Sets up monitoring
- Deploys with confidence
```

## All Available Agents by Category

### Engineering (21 agents)
- Backend Architect, Frontend Developer, AI Engineer, Security Engineer
- Data Engineer, DevOps Automator, Mobile Developer, Senior Developer
- SRE, Database Optimizer, Code Reviewer, Technical Writer
- [14 more specialized engineers]

### Design (8 agents)
- UX Architect, UI Designer, Brand Guardian, Visual Storyteller
- UX Researcher, Whimsy Injector, Image Prompt Engineer, Inclusive Visuals Specialist

### Testing (8 agents)
- Evidence Collector (QA), Reality Checker, API Tester, Performance Benchmarker
- Test Results Analyzer, Accessibility Auditor, Tool Evaluator, Workflow Optimizer

### Marketing (27 agents)
- Content Creator, SEO Specialist, Social Media Strategist, Growth Hacker
- TikTok Strategist, Twitter Engager, LinkedIn Creator, Podcast Strategist
- [19 more marketing specialists for every platform]

### Sales (8 agents)
- Sales Coach, Account Strategist, Deal Strategist, Discovery Coach
- Pipeline Analyst, Proposal Strategist, Engineer, Outbound Strategist

### Strategy (4 agents)
- Agents Orchestrator (coordinates all agents)
- NEXUS Strategy (enterprise implementation)
- Phase playbooks (discovery through operations)
- Scenario runbooks (MVP, campaigns, incidents)

### Product (5 agents)
- Product Manager, Sprint Prioritizer, Trend Researcher
- Behavioral Nudge Engine, Feedback Synthesizer

### Project Management (6 agents)
- Project Manager (Senior), Studio Producer, Project Shepherd
- Experiment Tracker, JIRA Workflow Steward, Studio Operations

### Support (6 agents)
- Executive Summary Generator, Analytics Reporter, Finance Tracker
- Infrastructure Maintainer, Legal Compliance Checker, Support Responder

### Specialized (20+ agents)
- MCP Builder, Workflow Architect, Document Generator, Salesforce Architect
- Blockchain Auditor, Cultural Intelligence Strategist, Developer Advocate
- [12+ more specialized roles]

### Academic (5 agents)
- Anthropologist, Historian, Psychologist, Narratologist, Geographer

### Game Development (13 agents)
- Game Designer, Level Designer, Narrative Designer, Audio Engineer
- Technical Artist, Blender addon engineer, Godot specialists
- Unity specialists, Roblox specialists, Unreal specialists

### Spatial Computing (6 agents)
- XR Immersive Developer, XR Interface Architect, XR Interaction Specialist
- VisionOS Engineer, macOS Spatial Engineer, Terminal Integration Specialist

## How Memory Works (Behind the Scenes)

```
Your input: /frontend
↓
Claude Code looks up "frontend" in agent config
↓
Activates: engineering-frontend-developer.md
↓
MCP Memory Server starts
↓
Agent can now:
- remember() — store decisions & context
- recall() — retrieve previous context
- search() — find memories across sessions
- rollback() — restore to previous state
```

All memories stored locally in: `~/.claude/agent-memory.db`

## Memory Operations (What Agents Do Automatically)

### Remember
Agent completes work → Stores context with tags
```json
{
  "content": "API endpoints designed. Schema: users, products, orders",
  "tags": ["backend-architect", "project-x", "phase-2"],
  "agent_name": "backend-architect",
  "context": "Session completed successfully"
}
```

### Recall
Agent starts session → Retrieves relevant context
```
"Found 3 memories from backend-architect:
- API schema design (2 sessions ago)
- Authentication pattern decision
- Performance targets set to <200ms"
```

### Search
Find memories by keyword
```bash
sqlite3 ~/.claude/agent-memory.db "SELECT * FROM memories WHERE content LIKE '%JWT%';"
```

### Rollback
Restore previous state on failure
```
QA verdict: FAILED
Previous memory: ID #847 (last PASS)
Restore: Architecture from successful phase
```

## Pro Tips

### 💡 Tag Consistently
Every memory gets tags for easy recall:
- Agent name: ["backend-architect"]
- Project: ["ecommerce-site"]
- Phase: ["phase-2"]
- Status: ["ready-for-qa"]

### 💡 Handoff Metadata
When passing work to next agent, include what's done:
```
"Task #42 COMPLETE
- Backend: API endpoints done
- Frontend: Ready for integration
- Tests: 95 passing
- Blocked by: None
Tags: [frontend-developer], [project], [handoff]"
```

### 💡 Reference Previous Work
Don't repeat decisions — recall them:
```
/frontend
"Recall: What design system did UX establish?"
→ Agent automatically recalls design tokens, colors, typography
```

### 💡 Cross-Project Reuse
Agents remember patterns across projects:
```
/backend
"I've built JWT auth 12 times before. Recalling best practices..."
```

## Troubleshooting

### Memory not persisting?
```bash
# Check memory database
ls -la ~/.claude/agent-memory.db

# View memory
sqlite3 ~/.claude/agent-memory.db "SELECT COUNT(*) FROM memories;"
```

### Slash command not working?
```bash
# Verify settings are loaded
cat ~/.claude/settings.json | grep "mcpServers"

# Restart Claude Code session
```

### Agent not found?
```bash
# List all available agents
find . -name "*.md" -path "*/\*/" | grep -v ".git"

# Try full agent name: /engineering-backend-architect
```

## Next Steps

1. ✅ Copy mcp-memory-server.py to ~/.claude/
2. ✅ Copy claude-code-settings.json to ~/.claude/settings.json
3. ✅ Restart Claude Code
4. ✅ Try: `/frontend "Build a landing page"`
5. ✅ Try: `/backend "Create API for that landing page"`
6. Watch context flow automatically between agents!

---

## Documentation

- **Full setup guide**: `SETUP-MCP-MEMORY.md`
- **Memory details**: `integrations/mcp-memory/README.md`
- **Agent activation templates**: `strategy/coordination/agent-activation-prompts.md`
- **Full README**: `README.md`

**You now have 189 specialized agents at your fingertips with persistent memory across sessions! 🚀**
