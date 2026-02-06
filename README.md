# fiken-mcp

MCP server wrapping the [Fiken](https://fiken.no) accounting API.

## Setup

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- A Fiken API key (generate one at <https://app.fiken.no/user/api-tokens>)

### Configuration

Copy the example env file and add your API key:

```bash
cp .env.example .env
# Edit .env and set your FIKEN_API_KEY
```

### Add to Claude Code

```bash
claude mcp add fiken -- uv run --directory /path/to/fiken-mcp fiken-mcp
```

Replace `/path/to/fiken-mcp` with the actual path to this repository.

## Available tools

The server exposes 46 tools covering:

- **Companies** — list and get company details
- **Contacts** — CRUD for customers and suppliers
- **Invoices** — create, list, send invoices and drafts
- **Credit notes** — full and partial credit notes
- **Sales** — other sales (not Fiken-issued invoices)
- **Purchases** — register and pay purchases
- **Products** — CRUD for products
- **Accounts** — chart of accounts and balances
- **Bank accounts** — list accounts and balances
- **Projects** — create and list projects
- **Journal entries** — list and create general journal entries
- **Transactions** — list transactions
- **Time tracking** — entries, activities, users, and invoice generation from time entries
