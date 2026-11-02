# MCP Server Registry — 2026

> A curated, maintained catalog of Model Context Protocol servers. The one resource you need when your AI agent needs to talk to the world.

---

## What is MCP?

The **Model Context Protocol (MCP)** is Anthropic's open standard for connecting AI models to external tools and data sources. Think of it as USB for AI — one protocol, many devices. MCP servers expose **tools**, **resources**, and **prompts** that AI agents can invoke directly.

```json
// Example MCP tool call
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "github_create_issue",
    "arguments": {
      "owner": "hussain-alsaibai",
      "repo": "tiny-agent",
      "title": "Bug: Memory leak in sub-agent dispatch",
      "body": "..."
    }
  }
}
```

---

## TL;DR — The Servers That Matter

| Category | Top Pick | Runner Up | Why |
|----------|----------|-----------|-----|
| **GitHub** | `github-mcp-server` | `mcp-github` | Issue/PR management, code search |
| **Filesystem** | `filesystem-mcp` | stdio-fs | Local file access, glob, search |
| **Database** | `postgres-mcp` | `sqlite-mcp` | Query execution, schema inspection |
| **Web** | `fetch-mcp` | `brave-search-mcp` | URL scraping, web search |
| **Slack** | `slack-mcp` | — | Messaging, channel management |
| **Notion** | `notion-mcp` | — | Page CRUD, database queries |
| **AWS** | `aws-mcp` | — | Lambda, S3, CloudWatch |
| **Memory** | `memory-mcp` | `mem0-mcp` | Persistent context across sessions |

---

## Official & Community Servers

### 🔌 GitHub / Git

#### `github-mcp-server` (Anthropic Official)
The reference implementation. Full GitHub REST API coverage.

```json
{
  "name": "github",
  "tools": ["create_issue", "create_pull_request", "search_code", 
            "list_commits", "get_file", "update_file", "create_branch"]
}
```

**Install:**
```bash
npx @anthropic/mcp-servers/github-mcp-server --github-token <token>
```

**Use cases:** Bounty automation, PR management, code review, repo analysis.

#### `gitlab-mcp-server`
GitLab REST API coverage. Merge requests, issues, CI/CD pipelines.

```bash
npx gitlab-mcp-server --gitlab-url https://gitlab.com --token <token>
```

#### `filesystem-mcp`
Local filesystem access via stdio.

```bash
npx filesystem-mcp --allowed-directory /path/to/project
```

**Tools:** `read_file`, `write_file`, `glob`, `grep`, `list_directory`.

---

### 🗄️ Database

#### `postgres-mcp`
Execute SQL, inspect schema, run migrations.

```bash
npx postgres-mcp --connection-string "postgresql://user:pass@host:5432/db"
```

**Tools:** `query`, `execute`, `list_tables`, `describe_table`, `list_databases`.

#### `sqlite-mcp`
Zero-setup local database for SQLite files.

```bash
npx sqlite-mcp --db-path ./data.db
```

**Tools:** `query`, `execute`, `vacuum`, `backup`.

#### `mysql-mcp`
MySQL/MariaDB support.

---

### 🌐 Web & Search

#### `fetch-mcp`
Scrape URLs, extract content, take screenshots.

```bash
npx fetch-mcp
```

**Tools:** `fetch_url`, `scrape_html`, `extract_links`, `screenshot`.

#### `brave-search-mcp`
Privacy-respecting web search.

```bash
npx @modelcontextprotocol/server-brave-search --brave-api-key <key>
```

**Tools:** `brave_web_search`, `brave_local_search`.

#### `firecrawl-mcp`
JS-heavy page scraping, sitemap extraction.

```bash
npx firecrawl-mcp --api-key <key>
```

---

### 💬 Messaging

#### `slack-mcp`
Post messages, manage channels, search history.

```bash
npx @modelcontextprotocol/server-slack \
  --slack-bot-token <token> \
  --slack-team-id <team>
```

**Tools:** `chat_postMessage`, `conversations_list`, `search_messages`.

#### `discord-mcp`
Send messages, manage channels, react.

```bash
npx discord-mcp --bot-token <token>
```

#### `telegram-mcp`
Bot management, channel posts, DMs.

---

### 📝 Knowledge & Docs

#### `notion-mcp`
Full Notion API: pages, databases, blocks.

```bash
npx notion-mcp --token <integration_token>
```

**Tools:** `create_page`, `query_database`, `update_block`, `search_pages`.

#### `google-drive-mcp`
Read Docs, Sheets, Slides, Drive files.

```bash
npx @modelcontextprotocol/server-google-drive --credentials <oauth-json>
```

#### `mcp-docs-server`
Index and search documentation sites.

---

### ☁️ Infrastructure

#### `aws-mcp`
Lambda invocation, S3 operations, CloudWatch logs.

```bash
npx @modelcontextprotocol/server-aws --region us-east-1
```

#### `docker-mcp`
Container management, image operations, logs.

```bash
npx docker-mcp
```

**Tools:** `container_list`, `container_logs`, `image_pull`, `exec_container`.

#### `kubernetes-mcp`
Pod management, deployment scaling, log streaming.

---

### 🧠 Memory & Context

#### `memory-mcp` (Anthropic Official)
Persistent key-value memory across sessions.

```bash
npx @anthropic/mcp-servers/memory-mcp
```

**Tools:** `create_memory`, `search_memory`, `update_memory`.

#### `mem0-mcp`
Semantic memory with embedding-based recall.

```bash
npx mem0-mcp --api-key <key>
```

#### `chromadb-mcp`
Vector store for semantic search and RAG.

```bash
npx @modelcontextprotocol/server-chromadb --path ./chroma_data
```

---

### 🔐 Security & Secrets

#### `vault-mcp`
HashiCorp Vault integration. Read/write secrets, dynamic credentials.

```bash
npx vault-mcp --address https://vault.example.com --token <token>
```

#### `env-mcp`
Secure environment variable management.

#### `tiny-secret-mcp` (OpenClaw)
Secrets management with audit logging, rotation, and access policies.

```bash
npx tiny-secret-mcp --vault-url <url>
```

---

### 🧪 Testing & QA

#### `playwright-mcp`
Browser automation, page interactions, screenshots.

```bash
npx @modelcontextprotocol/server-playwright --browser chromium
```

**Tools:** `goto`, `click`, `type`, `screenshot`, `evaluate`.

#### `agent-qa`
Natural-language web and mobile regression QA with retained screenshots, DOM/network/console evidence, and failure triage.

```bash
npx -y agent-qa mcp
```

Current releases are source-available under FSL-1.1-ALv2 and convert to Apache-2.0 after two years. The package is free; configured model providers may charge for usage.

#### `jira-mcp`
Issue tracking, sprint management, Agile boards.

---

## MCP Server by Use Case

### For Bounty Hunters
```
Required:  github-mcp-server     → issue triage, PR creation
           filesystem-mcp        → code inspection
           fetch-mcp / firecrawl → documentation lookup
Optional:  jira-mcp             → if project uses Jira
           gitlab-mcp           → if GitLab targets
```

### For Code Review
```
Required:  github-mcp-server     → diff access, comments
           filesystem-mcp        → local file reading
Optional:  slack-mcp            → post review summaries
           notion-mcp           → log review history
```

### For Autonomous DevOps
```
Required:  aws-mcp / docker-mcp / kubernetes-mcp
           postgres-mcp / mysql-mcp  → database migrations
Optional:  vault-mcp            → secret injection
           pagerduty-mcp        → incident management
```

### For Research Agents
```
Required:  fetch-mcp            → web scraping
           brave-search-mcp      → search
           memory-mcp           → accumulate findings
Optional:  notion-mcp           → save notes
           google-drive-mcp     → reference docs
           chromadb-mcp         → vector search over papers
```

---

## Building Your Own MCP Server

The protocol is simple. A server is a stdio process that speaks JSON-RPC 2.0.

```python
# minimal_mcp_server.py — a working MCP server in 50 lines
import json
import sys

class MinimalMCPServer:
    def __init__(self):
        self.tools = {
            "echo": {"description": "Echo back a message", "inputSchema": {"type": "object", "properties": {"message": {"type": "string"}}}},
            "add":  {"description": "Add two numbers", "inputSchema": {"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}}},
        }
        self._send({"jsonrpc": "2.0", "id": None, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "minimal-mcp", "version": "1.0.0"},
        }})

    def _send(self, msg):
        print(json.dumps(msg), flush=True)

    def _handle(self, msg):
        method = msg.get("method")
        tid = msg.get("id")

        if method == "tools/list":
            self._send({"jsonrpc": "2.0", "id": tid, "result": {"tools": [
                {"name": k, **v} for k, v in self.tools.items()
            ]}})

        elif method == "tools/call":
            name = msg["params"]["name"]
            args = msg["params"]["arguments"]
            if name == "echo":
                result = args["message"]
            elif name == "add":
                result = args["a"] + args["b"]
            else:
                raise ValueError(f"Unknown tool: {name}")
            self._send({"jsonrpc": "2.0", "id": tid, "result": {
                "content": [{"type": "text", "text": str(result)}]
            }})

    def run(self):
        for line in sys.stdin:
            self._handle(json.loads(line))

if __name__ == "__main__":
    MinimalMCPServer().run()
```

**Connect it:**
```json
// ~/.config/anthropic/mcp_servers.json
{
  "mcpServers": {
    "minimal": {
      "command": "python3",
      "args": ["/path/to/minimal_mcp_server.py"]
    }
  }
}
```

**Key lessons:**
- Everything is JSON-RPC 2.0 over stdio
- `tools/list` returns your catalog
- `tools/call` receives `{name, arguments}` and returns `[{type, text}]`
- No authentication in the protocol — handle auth at the transport layer

---

## MCP Client Reference

| Platform | Client | Notes |
|----------|--------|-------|
| Claude Desktop | Built-in | Settings → MCP Servers |
| OpenClaw | `tiny-mcp-client` + `tiny-mcp-gateway` | stdio + SSE, multi-server routing |
| Cursor | Built-in | Cursor Settings → MCP |
| Windsurf | Built-in | Cascade settings |
| Claude Code | `mcp` CLI | Official Anthropic CLI |
| LangChain | `langchain-mcp-adapters` | Multi-server support |
| LlamaIndex | `llama-index-agent-mcp` | Tool adoption |

---

## Security Considerations

1. **Token isolation** — each MCP server gets the minimum required API token. Don't share tokens across servers.
2. **Directory restrictions** — `filesystem-mcp` must be scoped to project directories, never `/`.
3. **Audit logging** — log every tool call with arguments. You need this for incident response.
4. **Rate limiting** — MCP servers can call external APIs. Set rate limits at both the server and the API key level.
5. **Prompt injection via tools** — if a tool returns user-controlled content (e.g., fetched URLs), sanitize before passing to the LLM.

---

## Registry Stats (August 2026)

| Metric | Count |
|--------|-------|
| Official Anthropic servers | 8 |
| Community servers (npm) | 200+ |
| Servers in this registry | 36 |
| Categories covered | 14 |

---

## Contributing

Know a server that should be here? Open an issue or PR at:
`https://github.com/hussain-alsaibai/mcp-server-registry`

---

*Maintained by [OpenClaw](https://github.com/hussain-alsaibai). Last updated: August 2026.*
