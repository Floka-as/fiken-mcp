from ..server import client, mcp, resolve_company_slug


@mcp.tool(annotations={"readOnlyHint": True})
async def list_time_entries(
    company_slug: str | None = None,
    date: str | None = None,
    date_le: str | None = None,
    date_ge: str | None = None,
    project_id: int | None = None,
    activity_id: int | None = None,
    time_user_id: int | None = None,
    invoiced: bool | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """List time entries for a company.

    Args:
        company_slug: Company identifier (uses default if not provided).
        date: Filter by exact date (yyyy-MM-dd).
        date_le: Date less than or equal to.
        date_ge: Date greater than or equal to.
        project_id: Filter by project ID.
        activity_id: Filter by activity ID.
        time_user_id: Filter by time user ID.
        invoiced: Filter by invoiced status (True/False).
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
    if project_id is not None:
        params["projectId"] = project_id
    if activity_id is not None:
        params["activityId"] = activity_id
    if time_user_id is not None:
        params["timeUserId"] = time_user_id
    if invoiced is not None:
        params["invoiced"] = invoiced
    return await client.get_with_pagination(
        f"/companies/{slug}/timeEntries", params=params
    )


@mcp.tool()
async def create_time_entry(
    date: str,
    hours: float,
    activity_id: int,
    time_user_id: int,
    company_slug: str | None = None,
    start_time: str | None = None,
    description: str | None = None,
    internal_note: str | None = None,
    project_id: int | None = None,
) -> dict:
    """Create a new time entry.

    Args:
        date: Date of the time entry (yyyy-MM-dd).
        hours: Number of hours worked (e.g. 7.5).
        activity_id: ID of the activity.
        time_user_id: ID of the person who performed the work.
        company_slug: Company identifier (uses default if not provided).
        start_time: Start time (HH:mm format, optional).
        description: Description of work (visible on invoices).
        internal_note: Internal note (not visible on invoices).
        project_id: Project ID to associate with.
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {
        "date": date,
        "hours": hours,
        "activityId": activity_id,
        "timeUserId": time_user_id,
    }
    if start_time:
        body["startTime"] = start_time
    if description:
        body["description"] = description
    if internal_note:
        body["internalNote"] = internal_note
    if project_id is not None:
        body["projectId"] = project_id
    return await client.post(f"/companies/{slug}/timeEntries", json=body)


@mcp.tool()
async def update_time_entry(
    time_entry_id: int,
    company_slug: str | None = None,
    date: str | None = None,
    hours: float | None = None,
    start_time: str | None = None,
    description: str | None = None,
    internal_note: str | None = None,
    activity_id: int | None = None,
    project_id: int | None = None,
) -> dict:
    """Update a time entry (partial update - only provided fields are changed).

    Args:
        time_entry_id: The time entry ID.
        company_slug: Company identifier (uses default if not provided).
        date: Date of the time entry (yyyy-MM-dd).
        hours: Number of hours worked.
        start_time: Start time (HH:mm format).
        description: Description of work.
        internal_note: Internal note.
        activity_id: Activity ID.
        project_id: Project ID.
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {}
    if date is not None:
        body["date"] = date
    if hours is not None:
        body["hours"] = hours
    if start_time is not None:
        body["startTime"] = start_time
    if description is not None:
        body["description"] = description
    if internal_note is not None:
        body["internalNote"] = internal_note
    if activity_id is not None:
        body["activityId"] = activity_id
    if project_id is not None:
        body["projectId"] = project_id
    return await client.patch(
        f"/companies/{slug}/timeEntries/{time_entry_id}", json=body
    )


@mcp.tool()
async def delete_time_entry(
    time_entry_id: int,
    company_slug: str | None = None,
) -> dict:
    """Delete a time entry. Cannot delete if invoiced or period is closed.

    Args:
        time_entry_id: The time entry ID.
        company_slug: Company identifier (uses default if not provided).
    """
    slug = resolve_company_slug(company_slug)
    return await client.delete(
        f"/companies/{slug}/timeEntries/{time_entry_id}"
    )


@mcp.tool(annotations={"readOnlyHint": True})
async def list_activities(
    company_slug: str | None = None,
    name: str | None = None,
    archived: bool | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """List time tracking activities for a company.

    Args:
        company_slug: Company identifier (uses default if not provided).
        name: Filter by name (partial match).
        archived: Filter by archived status.
        page: Page number (0-indexed).
        page_size: Number of results per page (max 100).
    """
    slug = resolve_company_slug(company_slug)
    params: dict = {"page": page, "pageSize": page_size}
    if name:
        params["name"] = name
    if archived is not None:
        params["archived"] = archived
    return await client.get_with_pagination(
        f"/companies/{slug}/activities", params=params
    )


@mcp.tool(annotations={"readOnlyHint": True})
async def list_time_users(
    company_slug: str | None = None,
    name: str | None = None,
    email: str | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """List persons who can register time entries.

    Args:
        company_slug: Company identifier (uses default if not provided).
        name: Filter by name (partial match).
        email: Filter by email address.
        page: Page number (0-indexed).
        page_size: Number of results per page (max 100).
    """
    slug = resolve_company_slug(company_slug)
    params: dict = {"page": page, "pageSize": page_size}
    if name:
        params["name"] = name
    if email:
        params["email"] = email
    return await client.get_with_pagination(
        f"/companies/{slug}/timeUsers", params=params
    )


@mcp.tool()
async def create_invoice_from_time_entries(
    time_entry_ids: list[int],
    customer_id: int,
    days_until_due_date: int,
    company_slug: str | None = None,
    group_by: str = "activity",
    include_time_entry_descriptions: bool = False,
    issue_date: str | None = None,
    project_id: int | None = None,
    invoice_text: str | None = None,
    your_reference: str | None = None,
    our_reference: str | None = None,
    order_reference: str | None = None,
    currency: str | None = None,
    bank_account_number: str | None = None,
) -> dict:
    """Create an invoice draft from time entries.

    Time entries are converted to invoice lines based on the grouping option.
    After creation, included entries are marked as 'in draft'.

    Args:
        time_entry_ids: List of time entry IDs to include. Must not be already invoiced.
        customer_id: Contact ID of the customer (must be a customer contact).
        days_until_due_date: Number of days until invoice is due.
        company_slug: Company identifier (uses default if not provided).
        group_by: How to group entries: 'activity' (default), 'activityAndPerson', or 'none'.
        include_time_entry_descriptions: Include individual descriptions on invoice lines.
        issue_date: Issue date (yyyy-MM-dd). Defaults to today.
        project_id: Project ID for the invoice draft.
        invoice_text: Text displayed above invoice lines.
        your_reference: Customer's reference person.
        our_reference: Your reference person.
        order_reference: EHF order reference.
        currency: ISO 4217 currency code (default NOK).
        bank_account_number: Bank account number for payment.
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {
        "timeEntryIds": time_entry_ids,
        "customerId": customer_id,
        "daysUntilDueDate": days_until_due_date,
        "groupBy": group_by,
        "includeTimeEntryDescriptions": include_time_entry_descriptions,
    }
    if issue_date:
        body["issueDate"] = issue_date
    if project_id is not None:
        body["projectId"] = project_id
    if invoice_text:
        body["invoiceText"] = invoice_text
    if your_reference:
        body["yourReference"] = your_reference
    if our_reference:
        body["ourReference"] = our_reference
    if order_reference:
        body["orderReference"] = order_reference
    if currency:
        body["currency"] = currency
    if bank_account_number:
        body["bankAccountNumber"] = bank_account_number
    return await client.post(
        f"/companies/{slug}/timeEntries/createInvoiceDraft", json=body
    )
