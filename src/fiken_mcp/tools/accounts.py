from ..server import client, mcp, resolve_company_slug


@mcp.tool(annotations={"readOnlyHint": True})
async def list_accounts(
    company_slug: str | None = None,
    from_account: str | None = None,
    to_account: str | None = None,
    range: str | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """List bookkeeping accounts for the current year.

    Args:
        company_slug: Company identifier (uses default if not provided).
        from_account: Filter accounts from this account code.
        to_account: Filter accounts up to this account code.
        range: Comma-separated list of account numbers or ranges (e.g. '1000-1500, 2000').
        page: Page number (0-indexed).
        page_size: Number of results per page (max 100).
    """
    slug = resolve_company_slug(company_slug)
    params: dict = {"page": page, "pageSize": page_size}
    if from_account:
        params["fromAccount"] = from_account
    if to_account:
        params["toAccount"] = to_account
    if range:
        params["range"] = range
    return await client.get_with_pagination(
        f"/companies/{slug}/accounts", params=params
    )


@mcp.tool(annotations={"readOnlyHint": True})
async def get_account_balances(
    date: str,
    company_slug: str | None = None,
    from_account: str | None = None,
    to_account: str | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """Get account balances for a given date.

    Args:
        date: Date for balances in yyyy-MM-dd format (required).
        company_slug: Company identifier (uses default if not provided).
        from_account: Filter accounts from this account code.
        to_account: Filter accounts up to this account code.
        page: Page number (0-indexed).
        page_size: Number of results per page (max 100).
    """
    slug = resolve_company_slug(company_slug)
    params: dict = {"date": date, "page": page, "pageSize": page_size}
    if from_account:
        params["fromAccount"] = from_account
    if to_account:
        params["toAccount"] = to_account
    return await client.get_with_pagination(
        f"/companies/{slug}/accountBalances", params=params
    )


@mcp.tool(annotations={"readOnlyHint": True})
async def list_bank_accounts(
    company_slug: str | None = None,
    inactive: bool | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """List bank accounts for a company.

    Args:
        company_slug: Company identifier (uses default if not provided).
        inactive: True for inactive accounts only, False for active only.
        page: Page number (0-indexed).
        page_size: Number of results per page (max 100).
    """
    slug = resolve_company_slug(company_slug)
    params: dict = {"page": page, "pageSize": page_size}
    if inactive is not None:
        params["inactive"] = inactive
    return await client.get_with_pagination(
        f"/companies/{slug}/bankAccounts", params=params
    )


@mcp.tool(annotations={"readOnlyHint": True})
async def get_bank_account_balances(
    company_slug: str | None = None,
    date: str | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """Get bank balances for all bank accounts.

    Args:
        company_slug: Company identifier (uses default if not provided).
        date: Date for balances in yyyy-MM-dd format.
        page: Page number (0-indexed).
        page_size: Number of results per page (max 100).
    """
    slug = resolve_company_slug(company_slug)
    params: dict = {"page": page, "pageSize": page_size}
    if date:
        params["date"] = date
    return await client.get_with_pagination(
        f"/companies/{slug}/bankBalances", params=params
    )
