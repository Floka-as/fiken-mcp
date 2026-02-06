from ..server import client, mcp, resolve_company_slug


@mcp.tool(annotations={"readOnlyHint": True})
async def get_user() -> dict:
    """Get information about the authenticated Fiken user."""
    return await client.get("/user")


@mcp.tool(annotations={"readOnlyHint": True})
async def list_companies(
    page: int = 0,
    page_size: int = 25,
    sort_by: str | None = None,
) -> dict:
    """List all companies accessible to the authenticated user.

    Args:
        page: Page number (0-indexed).
        page_size: Number of results per page (max 100).
        sort_by: Sort order, e.g. 'name asc', 'createdDate desc'.
    """
    params: dict = {"page": page, "pageSize": page_size}
    if sort_by:
        params["sortBy"] = sort_by
    return await client.get_with_pagination("/companies", params=params)


@mcp.tool(annotations={"readOnlyHint": True})
async def get_company(company_slug: str | None = None) -> dict:
    """Get details for a specific company.

    Args:
        company_slug: Company identifier (uses default if not provided).
    """
    slug = resolve_company_slug(company_slug)
    return await client.get(f"/companies/{slug}")
