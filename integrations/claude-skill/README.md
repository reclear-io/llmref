# llmref Claude skill

A [Claude Code](https://claude.com/claude-code) / Claude Agent skill that teaches
an assistant to fetch **version-pinned** documentation from the LLM Reference
registry (`api.llmref.org`) instead of relying on training data.

It prefers the `llmref` MCP server when connected, and otherwise falls back to
plain `curl` against the public API (no account, key, or install required).

## Install

Copy the skill into a skills directory Claude Code discovers:

```sh
# personal (all projects)
cp -r integrations/claude-skill ~/.claude/skills/llmref

# or per-project
cp -r integrations/claude-skill .claude/skills/llmref
```

Then ask Claude about any indexed library ("look up the Drizzle docs for
0.45.2") and it will resolve the version and pull the docs.

## Optional: connect the MCP server for cleaner tool calls

```sh
claude mcp add --transport http llmref https://api.llmref.org/v1/mcp
```

## Contents

- `SKILL.md` — trigger conditions, surface priority, and the core workflow.
- `references/api-reference.md` — full HTTP API, MCP tools, CLI, and SDK surface.
