# Neo4j Graph Database & Analytics

> Neo4j is a native graph database. Nodes, relationships, and properties are stored directly connected -- traversals are O(1) per hop. Use it when relationships between entities are as important as the entities themselves.

> **AI & Agentic Applications**: GraphRAG on Neo4j outperforms flat vector search on multi-hop questions -- graphs encode connections that vectors discard. Use Neo4j for GraphRAG pipelines, long-term agent memory, reasoning context graphs, and KG construction from unstructured documents.

> **Industry Use Cases**: Cybersecurity (attack paths, lateral movement) - Supply chain (provenance, disruption simulation) - Life sciences (drug-target networks, biomedical KGs) - Financial services (fraud rings, AML, KYC entity resolution) - Government & defense (terrorism networks, signals intelligence) - Infrastructure (CMDB, blast-radius, network topology)

> **Load [llms-full.txt](https://neo4j.com/llms-full.txt) when:** writing non-trivial Cypher, building GraphRAG pipelines, integrating a specific framework (LangChain/LlamaIndex/Spring AI/etc.), needing Java/Go/.NET driver code, or setting up agent memory.
> **Full documentation index (all doc sets, all drivers):** https://neo4j.com/docs/llms.txt

---

## Start Building

### Get a Database

- **Aura Free** (recommended, no credit card): https://neo4j.com/cloud/aura-free/ -- sign up, create instance, download `.env` with credentials
- **Neo4j Desktop** (local, user-friendly): https://neo4j.com/download/ -- GUI app, Neo4j Enterprise Edition with free Developer License, built-in Query, Explore, Dashboards, Import tools; connect via `bolt://localhost:7687`
- **Docker** (local): `docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:enterprise`
- **Docs**: https://neo4j.com/docs/aura/ - https://neo4j.com/docs/desktop-manual/ - https://neo4j.com/docs/operations-manual/installation/

URI schemes: `neo4j+s://` (Aura/TLS) - `bolt://` (local) - `neo4j://` (local with routing)

### Connect with a Driver

One driver per process -- thread-safe and expensive to construct, use as a singleton. Close it when the application exits.

**Python** -- `pip install neo4j` (Python >= 3.10; use `AsyncGraphDatabase` for FastAPI/asyncio)
```python
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()  # reads .env file; never hardcode credentials
URI      = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

# singleton -- create once, reuse across the application
with GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD)) as driver:
    driver.verify_connectivity()
    records, _, _ = driver.execute_query(
        "MATCH (n:Person {name: $name}) RETURN n.email",
        name="Alice", database_=DATABASE
    )
# driver.close() called automatically by context manager
```
[Python docs](https://neo4j.com/docs/python-manual/) - [Simple queries](https://neo4j.com/docs/python-manual/current/query-simple/) - [Advanced transaction management](https://neo4j.com/docs/python-manual/current/transactions/)

**JavaScript** -- `npm install neo4j-driver` (integers return as `neo4j.Integer` -- use `.toNumber()` or `disableLosslessIntegers: true`)
```javascript
const driver = neo4j.driver('neo4j+s://<host>', neo4j.auth.basic('neo4j', '<password>'))
await driver.verifyConnectivity()
const { records } = await driver.executeQuery('MATCH (n:Person {name: $name}) RETURN n.email', { name: 'Alice' }, { database: 'neo4j' })
```
[JS docs](https://neo4j.com/docs/javascript-manual/)

**Java** - **Go** - **.NET** -- full examples in llms-full.txt - [Java](https://neo4j.com/docs/java-manual/) - [Spring Data Neo4j](https://docs.spring.io/spring-data/neo4j/reference/) - [Go](https://neo4j.com/docs/go-manual/) - [.NET](https://neo4j.com/docs/dotnet-manual/)

**Error handling** -- handle these on every connection attempt:
- `neo4j.exceptions.ServiceUnavailable` -- wrong URI or DB not running; check URI scheme and port
- `neo4j.exceptions.AuthError` -- wrong credentials; verify username/password
- `neo4j.exceptions.TransientError` -- temporary failure; `execute_query` retries automatically up to the configured maximum retry time

### HTTP Query API (no driver required)

```bash
curl -X POST https://<instance>.databases.neo4j.io/db/<database|neo4j>/query/v2 \
  -u neo4j:<password> \
  -H "Content-Type: application/json" \
  -d '{"statement": "MATCH (n:Person {name: $name}) RETURN n.email", "parameters": {"name": "Alice"}}'
```
Returns `200 OK` with `{ "data": { "fields": [...], "values": [...] }, "errors": [] }`. Self-managed: `http://localhost:7474/db/neo4j/query/v2`
[Query API docs](https://neo4j.com/docs/query-api/)

### Cypher Essentials

Always use `$parameters` -- never string-interpolate. Full examples in llms-full.txt.

**Cypher 25** is current (Neo4j 2025.x+ and all new Aura databases). Enable with `CYPHER 25` prefix or `ALTER DATABASE neo4j SET DEFAULT LANGUAGE CYPHER 25`. [Full diff vs Cypher 5](https://neo4j.com/docs/cypher-manual/current/deprecations-additions-removals-compatibility/)

**Deprecated patterns -- DO NOT USE (common AI training data is stale):**
- DO NOT USE: `shortestPath((a)-[*]-(b))` -- USE: `SHORTEST 1 (a)-[*]-(b)`
- DO NOT USE: `()-[*1..5]-()` variable-length -- USE: quantified path `()-[]{1,5}-()`
- DO NOT USE: `WITH collect(x)` subquery workaround -- USE: `COLLECT { MATCH ... RETURN ... }`
- DO NOT USE: `WITH count(*)` subquery workaround -- USE: `COUNT { MATCH ... }`
- DO NOT USE: `RETURN exists((n)-[:R]->())` -- USE: `RETURN exists { (n)-[:R]->() }`
- DO NOT USE: `neo4j-driver` Python package -- USE: `neo4j` package (renamed in 6.x)

```cypher
MATCH (p:Person)-[:KNOWS]->(friend) WHERE p.name = $name RETURN friend.name  // read
MATCH (p:Person)-[:KNOWS]->{1,3}(friend) RETURN DISTINCT friend.name          // QPP (Cypher 25)
MERGE (p:Person {id: $id}) ON CREATE SET p.name = $name, p.createdAt = datetime() ON MATCH SET p.updatedAt = datetime()  // upsert
MATCH (a:Person {id: $a}) MATCH (b:Person {id: $b}) MERGE (a)-[:KNOWS]->(b)  // merge rel (match nodes first)
UNWIND $rows AS row CALL (row) { MERGE (p:Person {id: row.id}) SET p.name = row.name } IN TRANSACTIONS OF 10000 ROWS  // batch
MATCH (c) SEARCH c IN (VECTOR INDEX chunk_embedding FOR $embedding LIMIT 5) SCORE AS score  // vector search (Cypher 25, Neo4j 2026.x)
```

**Output shaping -- depends on the consumer:**

For **agent/LLM consumption**: return flat scalars or map projections -- deterministic, serializable, no wrapper objects.
- DO: `RETURN p.name AS name, p.email AS email`
- DO: map projection -- select properties, rename keys, inline pattern comprehensions:
```cypher
RETURN n { .name, .description, date: n.createdDate,
           children: [(n)-[:HAS_CHILD]->(c) | c { .name, .description }] }
```
- DO: full node as clean map, stripping unwanted fields: `RETURN n { .*, id: elementId(n), labels: labels(n), embedding: null }`
- DO NOT: `RETURN n` or `RETURN r` -- raw node/relationship objects wrap properties in an internal structure LLMs misread

For **programmatic consumption** (application code processing results): returning nodes, relationships, or paths is fine and often preferable -- drivers deserialize them into typed objects.

For **visualization** (Neo4j Browser, Bloom, NVL, neo4j-viz): returning raw nodes and relationships is REQUIRED -- visualization libraries need the graph structure, not flat maps.
```cypher
MATCH path = (a:Person)-[:KNOWS*1..3]->(b:Person {name: $name})
RETURN path   // required for graph visualization
```

**Common pitfalls:**
- Filtering on unindexed properties causes full scans -- always create an index for properties used in WHERE
- `MERGE (a)-[:R]->(b)` without first MATCHing both nodes creates duplicate nodes
- Missing `LIMIT` on unbounded traversals will time out on large graphs

[Cypher Manual](https://neo4j.com/docs/cypher-manual/) - [Cheat Sheet](https://neo4j.com/docs/cypher-cheat-sheet/) - [Getting Started](https://neo4j.com/docs/getting-started/)

### MCP Server (AI Agent Integration)

Exposes `get-schema`, `read-cypher`, `write-cypher`, `list-gds-procedures`. Install: `pip install neo4j-mcp-server` - [GitHub Releases](https://github.com/neo4j/mcp/releases) - `docker pull neo4j/mcp`.

```json
{
  "mcpServers": {
    "neo4j": {
      "command": "neo4j-mcp",
      "env": {
        "NEO4J_URI": "neo4j+s://<host>",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "<password>",
        "NEO4J_DATABASE": "neo4j",
        "NEO4J_READ_ONLY": "true"
      }
    }
  }
}
```

Config file: `~/.claude/settings.json` (Claude Code) - `~/Library/Application Support/Claude/claude_desktop_config.json` (Claude Desktop) - `~/.cursor/mcp.json` (Cursor) - `~/.kiro/settings/mcp.json` (Kiro) - `.vscode/mcp.json` with key `servers` (VS Code)

[MCP docs](https://neo4j.com/docs/mcp/) - [All Neo4j MCP servers](https://neo4j.com/developer/genai-ecosystem/model-context-protocol-mcp/) - [Editor setup guide](https://neo4j.com/labs/genai-ecosystem/agent-skills/coding-skills/)

### GraphRAG

`pip install neo4j-graphrag` -- combines vector search, full-text, and graph traversal in one retriever. Full runnable example in llms-full.txt.

```python
from neo4j_graphrag.retrievers import HybridCypherRetriever
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.embeddings import OpenAIEmbeddings

retriever = HybridCypherRetriever(
    driver=driver,
    vector_index_name="chunk_embedding",   # CREATE VECTOR INDEX -- see llms-full.txt
    fulltext_index_name="chunk_fulltext",  # CREATE FULLTEXT INDEX -- see llms-full.txt
    retrieval_query="MATCH (node)<-[:HAS_CHUNK]-(doc) RETURN node.text AS chunk_text, score",
    embedder=OpenAIEmbeddings(),
)
rag = GraphRAG(retriever=retriever, llm=OpenAILLM(model_name="gpt-4o"))
print(rag.search("Who does Alice work for?").answer)
```

[GraphRAG Python docs](https://neo4j.com/docs/neo4j-graphrag-python/) - [Full example + KG construction](https://neo4j.com/llms-full.txt)

### Agent Memory

Neo4j Agent Memory -- graph-native unified short-term, long-term, and reasoning memory for AI agents. Integrates with LangChain, PydanticAI, LlamaIndex, CrewAI, OpenAI Agents.

Node labels -- short-term: `Conversation`, `Message`; long-term: `Entity`, `Preference`, `Fact`; reasoning: `ReasoningTrace`, `ReasoningStep`, `Tool`, `ToolCall`. Key relationships: `(Conversation)-[:HAS_MESSAGE]->(Message)`, `(Message)-[:NEXT_MESSAGE]->(Message)`, `(Message)-[:MENTIONS]->(Entity)`. All memory nodes carry an `embedding` property for vector recall.

```python
from neo4j_agent_memory import MemoryClient, MemorySettings

settings = MemorySettings(neo4j={"uri": "bolt://localhost:7687", "password": "pw"})
async with MemoryClient(settings) as memory:
    await memory.short_term.add_message(session_id="s1", role="user", content="I love Italian food")
    context = await memory.get_context("What restaurant should I recommend?", session_id="s1")
```

[neo4j.com/labs/agent-memory](https://neo4j.com/labs/agent-memory/) - [GitHub](https://github.com/neo4j-labs/agent-memory) - [Full schema + patterns](https://neo4j.com/llms-full.txt)

### Agent Skills

20+ skills teaching coding agents Neo4j-specific patterns: Cypher, GraphRAG, drivers (Python/JS/Java/Go/.NET), GDS, data import, migrations, agent memory, CLI tools. Browse: https://skills.sh/neo4j-contrib/neo4j-skills

| Agent | Install |
|---|---|
| Claude Code | `/plugin marketplace add https://github.com/neo4j-contrib/neo4j-skills.git` then `/plugin install neo4j-skills@neo4j-skills-marketplace` |
| Gemini CLI | `gemini extensions install https://github.com/neo4j-contrib/neo4j-skills` |
| Cursor / Cline / Windsurf | `npx skills add neo4j-contrib/neo4j-skills` |
| Codex | `git clone https://github.com/neo4j-contrib/neo4j-skills.git && cp -R neo4j-skills ~/.codex/plugins/neo4j-skills` |

Skills activate automatically on task description match -- no invocation needed. Exception: `neo4j-getting-started-skill` -- invoke explicitly:

```
/neo4j-getting-started-skill fraud detection for a fintech startup
/neo4j-getting-started-skill healthcare patient graph, local Docker, FastAPI, synthetic data
```

**`neo4j-getting-started-skill`** -- provisions DB, designs schema, loads data, generates app, configures MCP server in one Claude Code session. `db_target`: aura-free - aura-pro - local-docker - local-desktop - existing-cloud. `app_type`: notebook - streamlit - fastapi - graphrag - mcp - explore-only. Resumes from `progress.md` if interrupted.

[All Neo4j Agent Skills](https://neo4j.com/labs/genai-ecosystem/agent-skills/neo4j-skills/)

### CLI Tools

- **`neo4j-cli`** -- unified agent-friendly CLI: Cypher (Bolt), schema inspection, Aura, Docker, credentials, agent skill install - `curl -sSfL https://neo4j.sh/install.sh | bash` - [GitHub](https://github.com/neo4j-labs/neo4j-cli)
  - `neo4j-cli query :schema --format toon` -- inspect schema before writing Cypher
  - `neo4j-cli skill install [skill-name]` -- install self-skill or any skill from `neo4j-contrib/neo4j-skills` catalog into Claude Code, Cursor, Copilot, Gemini CLI, and more
  - `neo4j-cli docker create --name dev --wait --rw` -- spin up a local Neo4j container with a stored credential
  - `--format toon` saves ~40% tokens vs JSON; `--rw` required for writes under agents
- **`cypher-shell`** -- run Cypher from terminal (Java required) - [docs](https://neo4j.com/docs/operations-manual/tools/cypher-shell/)
- **`neo4j-admin`** -- backup, restore, import, user management - [docs](https://neo4j.com/docs/operations-manual/neo4j-admin-neo4j-cli/)
- **`aura-cli`** -- legacy Aura CLI (prefer `neo4j-cli aura` instead) - [docs](https://neo4j.com/docs/aura/aura-cli/)
- **`neo4j-mcp`** -- run the MCP server - [docs](https://neo4j.com/docs/mcp/)

---

## Documentation

Base: `https://neo4j.com/docs/` - Full index: https://neo4j.com/docs/llms.txt

- Getting Started - Cypher Manual - Operations Manual
- Drivers: python-manual - javascript-manual - java-manual - go-manual - dotnet-manual
- query-api - aura - mcp - neo4j-graphrag-python - nvl - python-graph-visualization
- graph-data-science - apoc - graphql
- [Aura Agent](https://neo4j.com/docs/aura/aura-agent/) -- no/low-code GraphRAG agent builder (Cypher templates, similarity search, Text2Cypher; REST API or MCP endpoint)

---

## Labs: GenAI & Agent Integrations

> Full individual integration pages: https://neo4j.com/labs/genai-ecosystem/

- **[MCP Servers](https://neo4j.com/developer/genai-ecosystem/model-context-protocol-mcp/)** -- Neo4j MCP server + memory, data modeling, Aura API, GDS servers
- **GenAI Frameworks** -- LangChain - LlamaIndex - LangGraph - Spring AI - Haystack - MCP Toolbox
- **Agent Frameworks** -- OpenAI Agents - Pydantic AI - AWS Strands - Claude Agent SDK - Google ADK - Microsoft Agent Framework
- **Agent Platforms** -- AWS AgentCore - Azure AI Foundry - Databricks - Google Gemini Enterprise - Salesforce Agentforce

---

## Optional

- `https://neo4j.com/docs/` slugs: bolt - kafka - cdc
- GraphAcademy free courses + full course index: https://graphacademy.neo4j.com/llms.txt
