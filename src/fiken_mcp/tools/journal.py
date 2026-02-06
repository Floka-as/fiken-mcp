from ..server import client, mcp, resolve_company_slug


@mcp.tool(annotations={"readOnlyHint": True})
async def list_journal_entries(
    company_slug: str | None = None,
    date: str | None = None,
    date_le: str | None = None,
    date_ge: str | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """List journal entries (posteringer) for a company.

    Args:
        company_slug: Company identifier (uses default if not provided).
        date: Filter by exact date (yyyy-MM-dd).
        date_le: Date less than or equal to.
        date_ge: Date greater than or equal to.
        page: Page number (0-indexed).
        page_size: Number of results per page (max 100).
    """
    slug = resolve_company_slug(company_slug)
    params: dict = {"page": page, "pageSize": page_size}
    if date:
        params["date"] = date
    if date_le:
        params["dateLe"] = date_le
    if date_ge:
        params["dateGe"] = date_ge
    return await client.get_with_pagination(
        f"/companies/{slug}/journalEntries", params=params
    )


@mcp.tool()
async def create_general_journal_entry(
    journal_entries: list[dict],
    company_slug: str | None = None,
    description: str | None = None,
    open: bool = False,
) -> dict:
    """Create a general journal entry (fri postering).

    Args:
        journal_entries: List of journal entry dicts. Each must contain:
            - description: Entry description.
            - date: Entry date (yyyy-MM-dd).
            - lines: List of line dicts, each with:
                - amount: Amount in cents.
                - debitAccount: Debit account code (e.g. '1500').
                - debitVatCode: VAT code number for debit (optional).
                - creditAccount: Credit account code (e.g. '3000').
                - creditVatCode: VAT code number for credit (optional).
        company_slug: Company identifier (uses default if not provided).
        description: Overall description (prefixed with 'Fri postering registrert via API: ').
        open: True for open (deletable) entry, False for closed (default).
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {
        "journalEntries": journal_entries,
        "open": open,
    }
    if description:
        body["description"] = description
    return await client.post(
        f"/companies/{slug}/generalJournalEntries", json=body
    )


@mcp.tool(annotations={"readOnlyHint": True})
async def list_transactions(
    company_slug: str | None = None,
    last_modified: str | None = None,
    last_modified_le: str | None = None,
    last_modified_ge: str | None = None,
    created_date: str | None = None,
    created_date_le: str | None = None,
    created_date_ge: str | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """List transactions for a company.

    Args:
        company_slug: Company identifier (uses default if not provided).
        last_modified: Filter by exact last modified date.
        last_modified_le: Last modified less than or equal to.
        last_modified_ge: Last modified greater than or equal to.
        created_date: Filter by exact created date.
        created_date_le: Created date less than or equal to.
        created_date_ge: Created date greater than or equal to.
        page: Page number (0-indexed).
        page_size: Number of results per page (max 100).
    """
    slug = resolve_company_slug(company_slug)
    params: dict = {"page": page, "pageSize": page_size}
    if last_modified:
        params["lastModified"] = last_modified
    if last_modified_le:
        params["lastModifiedLe"] = last_modified_le
    if last_modified_ge:
        params["lastModifiedGe"] = last_modified_ge
    if created_date:
        params["createdDate"] = created_date
    if created_date_le:
        params["createdDateLe"] = created_date_le
    if created_date_ge:
        params["createdDateGe"] = created_date_ge
    return await client.get_with_pagination(
        f"/companies/{slug}/transactions", params=params
    )
