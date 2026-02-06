from ..server import client, mcp, resolve_company_slug


@mcp.tool(annotations={"readOnlyHint": True})
async def list_credit_notes(
    company_slug: str | None = None,
    issue_date: str | None = None,
    issue_date_le: str | None = None,
    issue_date_ge: str | None = None,
    customer_id: int | None = None,
    settled: bool | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """List credit notes for a company.

    Args:
        company_slug: Company identifier (uses default if not provided).
        issue_date: Filter by exact issue date (yyyy-MM-dd).
        issue_date_le: Issue date less than or equal to.
        issue_date_ge: Issue date greater than or equal to.
        customer_id: Filter by customer contact ID.
        settled: True for settled only, False for unsettled.
        page: Page number (0-indexed).
        page_size: Number of results per page (max 100).
    """
    slug = resolve_company_slug(company_slug)
    params: dict = {"page": page, "pageSize": page_size}
    if issue_date:
        params["issueDate"] = issue_date
    if issue_date_le:
        params["issueDateLe"] = issue_date_le
    if issue_date_ge:
        params["issueDateGe"] = issue_date_ge
    if customer_id is not None:
        params["customerId"] = customer_id
    if settled is not None:
        params["settled"] = settled
    return await client.get_with_pagination(
        f"/companies/{slug}/creditNotes", params=params
    )


@mcp.tool()
async def create_full_credit_note(
    invoice_id: int,
    issue_date: str,
    company_slug: str | None = None,
    credit_note_text: str | None = None,
) -> dict:
    """Create a full credit note that covers the full amount of an invoice.

    Args:
        invoice_id: ID of the invoice to credit.
        issue_date: Issue date (yyyy-MM-dd).
        company_slug: Company identifier (uses default if not provided).
        credit_note_text: Text to display on the credit note (max 500 chars).
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {
        "invoiceId": invoice_id,
        "issueDate": issue_date,
    }
    if credit_note_text:
        body["creditNoteText"] = credit_note_text
    return await client.post(f"/companies/{slug}/creditNotes/full", json=body)


@mcp.tool()
async def create_partial_credit_note(
    issue_date: str,
    lines: list[dict],
    company_slug: str | None = None,
    invoice_id: int | None = None,
    contact_id: int | None = None,
    contact_person_id: int | None = None,
    credit_note_text: str | None = None,
    our_reference: str | None = None,
    your_reference: str | None = None,
    order_reference: str | None = None,
    currency: str | None = None,
    project: int | None = None,
) -> dict:
    """Create a partial credit note.

    Args:
        issue_date: Issue date (yyyy-MM-dd).
        lines: Credit note lines. Each dict may contain: quantity, unitPrice (cents),
               vatType (HIGH/MEDIUM/LOW/etc.), description, comment, incomeAccount,
               productId, discount (0-100 percent).
        company_slug: Company identifier (uses default if not provided).
        invoice_id: ID of the associated invoice (optional).
        contact_id: Contact ID for the credit note.
        contact_person_id: Contact person ID (must belong to contact).
        credit_note_text: Text to display on the credit note (max 500 chars).
        our_reference: Your company's reference.
        your_reference: Customer's reference.
        order_reference: EHF order reference.
        currency: ISO 4217 currency code.
        project: Project ID to associate with.
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {
        "issueDate": issue_date,
        "lines": lines,
    }
    if invoice_id is not None:
        body["invoiceId"] = invoice_id
    if contact_id is not None:
        body["contactId"] = contact_id
    if contact_person_id is not None:
        body["contactPersonId"] = contact_person_id
    if credit_note_text:
        body["creditNoteText"] = credit_note_text
    if our_reference:
        body["ourReference"] = our_reference
    if your_reference:
        body["yourReference"] = your_reference
    if order_reference:
        body["orderReference"] = order_reference
    if currency:
        body["currency"] = currency
    if project is not None:
        body["project"] = project
    return await client.post(
        f"/companies/{slug}/creditNotes/partial", json=body
    )
