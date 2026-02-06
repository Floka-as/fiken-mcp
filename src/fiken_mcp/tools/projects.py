from ..server import client, mcp, resolve_company_slug


@mcp.tool(annotations={"readOnlyHint": True})
async def list_projects(
    company_slug: str | None = None,
    completed: bool | None = None,
    name: str | None = None,
    number: str | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """List projects for a company.

    Args:
        company_slug: Company identifier (uses default if not provided).
        completed: True for completed projects, False for active.
        name: Filter by project name.
        number: Filter by project number.
        page: Page number (0-indexed).
        page_size: Number of results per page (max 100).
    """
    slug = resolve_company_slug(company_slug)
    params: dict = {"page": page, "pageSize": page_size}
    if completed is not None:
        params["completed"] = completed
    if name:
        params["name"] = name
    if number:
        params["number"] = number
    return await client.get_with_pagination(
        f"/companies/{slug}/projects", params=params
    )


@mcp.tool(annotations={"readOnlyHint": True})
async def get_project(
    project_id: int,
    company_slug: str | None = None,
) -> dict:
    """Get a specific project by ID.

    Args:
        project_id: The project ID.
        company_slug: Company identifier (uses default if not provided).
    """
    slug = resolve_company_slug(company_slug)
    return await client.get(f"/companies/{slug}/projects/{project_id}")


@mcp.tool()
async def create_project(
    name: str,
    number: str,
    start_date: str,
    company_slug: str | None = None,
    description: str | None = None,
    end_date: str | None = None,
    contact_id: int | None = None,
    completed: bool = False,
) -> dict:
    """Create a new project.

    Args:
        name: Project name.
        number: Project number (must be unique).
        start_date: Start date (yyyy-MM-dd).
        company_slug: Company identifier (uses default if not provided).
        description: Project description.
        end_date: End date (yyyy-MM-dd).
        contact_id: Contact ID to associate with the project.
        completed: Whether the project is completed (default False).
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {
        "name": name,
        "number": number,
        "startDate": start_date,
        "completed": completed,
    }
    if description:
        body["description"] = description
    if end_date:
        body["endDate"] = end_date
    if contact_id is not None:
        body["contactId"] = contact_id
    return await client.post(f"/companies/{slug}/projects", json=body)
