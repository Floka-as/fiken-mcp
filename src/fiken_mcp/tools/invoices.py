from ..server import client, mcp, resolve_company_slug


@mcp.tool(annotations={"readOnlyHint": True})
async def list_invoices(
    company_slug: str | None = None,
    issue_date: str | None = None,
    issue_date_le: str | None = None,
    issue_date_ge: str | None = None,
    due_date: str | None = None,
    due_date_le: str | None = None,
    due_date_ge: str | None = None,
    customer_id: int | None = None,
    settled: bool | None = None,
    invoice_number: str | None = None,
    order_reference: str | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """List invoices for a company.

    Args:
        company_slug: Company identifier (uses default if not provided).
        issue_date: Filter by exact issue date (yyyy-MM-dd).
        issue_date_le: Issue date less than or equal to.
        issue_date_ge: Issue date greater than or equal to.
        due_date: Filter by exact due date (yyyy-MM-dd).
        due_date_le: Due date less than or equal to.
        due_date_ge: Due date greater than or equal to.
        customer_id: Filter by customer contact ID.
        settled: True for settled invoices only, False for unsettled.
        invoice_number: Filter by invoice number.
        order_reference: Filter by order reference.
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
    if due_date:
        params["dueDate"] = due_date
    if due_date_le:
        params["dueDateLe"] = due_date_le
    if due_date_ge:
        params["dueDateGe"] = due_date_ge
    if customer_id is not None:
        params["customerId"] = customer_id
    if settled is not None:
        params["settled"] = settled
    if invoice_number:
        params["invoiceNumber"] = invoice_number
    if order_reference:
        params["orderReference"] = order_reference
    return await client.get_with_pagination(
        f"/companies/{slug}/invoices", params=params
    )


@mcp.tool(annotations={"readOnlyHint": True})
async def get_invoice(
    invoice_id: int,
    company_slug: str | None = None,
) -> dict:
    """Get a specific invoice by ID.

    Args:
        invoice_id: The invoice ID (not invoice number).
        company_slug: Company identifier (uses default if not provided).
    """
    slug = resolve_company_slug(company_slug)
    return await client.get(f"/companies/{slug}/invoices/{invoice_id}")


@mcp.tool()
async def create_invoice(
    issue_date: str,
    due_date: str,
    customer_id: int,
    bank_account_code: str,
    lines: list[dict],
    company_slug: str | None = None,
    cash: bool = False,
    currency: str = "NOK",
    invoice_text: str | None = None,
    our_reference: str | None = None,
    your_reference: str | None = None,
    order_reference: str | None = None,
    contact_person_id: int | None = None,
    payment_account: str | None = None,
    project_id: int | None = None,
) -> dict:
    """Create a new invoice.

    Each line can be a product line (provide productId) or free text line.
    For free text lines, provide: quantity, unitPrice (cents), vatType, description.

    Args:
        issue_date: Issue date (yyyy-MM-dd).
        due_date: Due date (yyyy-MM-dd).
        customer_id: Contact ID of the customer.
        bank_account_code: Bank account code (e.g. '1920:10002').
        lines: Invoice lines. Each dict may contain: productId, quantity, unitPrice (cents),
               vatType (HIGH/MEDIUM/LOW/EXEMPT/NONE/etc.), description, comment,
               incomeAccount, discount (0-100 percent), net (cents), vat (cents), gross (cents).
        company_slug: Company identifier (uses default if not provided).
        cash: True for cash invoice.
        currency: ISO 4217 currency code (default 'NOK').
        invoice_text: Text printed above invoice lines.
        our_reference: Your company's reference.
        your_reference: Customer's reference.
        order_reference: EHF order reference.
        contact_person_id: Contact person ID (must belong to customer).
        payment_account: Payment account for cash invoices (e.g. '1920:10001').
        project_id: Associate invoice with a project.
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {
        "issueDate": issue_date,
        "dueDate": due_date,
        "customerId": customer_id,
        "bankAccountCode": bank_account_code,
        "lines": lines,
        "cash": cash,
        "currency": currency,
    }
    if invoice_text:
        body["invoiceText"] = invoice_text
    if our_reference:
        body["ourReference"] = our_reference
    if your_reference:
        body["yourReference"] = your_reference
    if order_reference:
        body["orderReference"] = order_reference
    if contact_person_id is not None:
        body["contactPersonId"] = contact_person_id
    if payment_account:
        body["paymentAccount"] = payment_account
    if project_id is not None:
        body["projectId"] = project_id
    return await client.post(f"/companies/{slug}/invoices", json=body)


@mcp.tool()
async def create_invoice_draft(
    customer_id: int,
    days_until_due_date: int,
    company_slug: str | None = None,
    draft_type: str = "invoice",
    issue_date: str | None = None,
    lines: list[dict] | None = None,
    invoice_text: str | None = None,
    our_reference: str | None = None,
    your_reference: str | None = None,
    order_reference: str | None = None,
    currency: str | None = None,
    payment_account: str | None = None,
    contact_person_id: int | None = None,
    project_id: int | None = None,
) -> dict:
    """Create an invoice draft.

    Args:
        customer_id: Contact ID of the customer.
        days_until_due_date: Days until the invoice is due.
        company_slug: Company identifier (uses default if not provided).
        draft_type: Type of draft: 'invoice' or 'cash_invoice'.
        issue_date: Issue date (yyyy-MM-dd).
        lines: Draft lines. Each dict may contain: productId, quantity, unitPrice (cents),
               vatType, description, comment, incomeAccount, discount (0-100 percent).
        invoice_text: Text printed above invoice lines.
        our_reference: Your company's reference.
        your_reference: Customer's reference.
        order_reference: EHF order reference.
        currency: ISO 4217 currency code.
        payment_account: Payment account code.
        contact_person_id: Contact person ID.
        project_id: Project ID to associate with.
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {
        "type": draft_type,
        "customerId": customer_id,
        "daysUntilDueDate": days_until_due_date,
    }
    if issue_date:
        body["issueDate"] = issue_date
    if lines:
        body["lines"] = lines
    if invoice_text:
        body["invoiceText"] = invoice_text
    if our_reference:
        body["ourReference"] = our_reference
    if your_reference:
        body["yourReference"] = your_reference
    if order_reference:
        body["orderReference"] = order_reference
    if currency:
        body["currency"] = currency
    if payment_account:
        body["paymentAccount"] = payment_account
    if contact_person_id is not None:
        body["contactPersonId"] = contact_person_id
    if project_id is not None:
        body["projectId"] = project_id
    return await client.post(f"/companies/{slug}/invoices/drafts", json=body)


@mcp.tool()
async def update_invoice_draft(
    draft_id: int,
    customer_id: int,
    days_until_due_date: int,
    company_slug: str | None = None,
    draft_type: str = "invoice",
    issue_date: str | None = None,
    lines: list[dict] | None = None,
    invoice_text: str | None = None,
    our_reference: str | None = None,
    your_reference: str | None = None,
    order_reference: str | None = None,
    currency: str | None = None,
    payment_account: str | None = None,
    contact_person_id: int | None = None,
    project_id: int | None = None,
) -> dict:
    """Update an existing invoice draft.

    Args:
        draft_id: The draft ID.
        customer_id: Contact ID of the customer.
        days_until_due_date: Days until the invoice is due.
        company_slug: Company identifier (uses default if not provided).
        draft_type: Type of draft: 'invoice' or 'cash_invoice'.
        issue_date: Issue date (yyyy-MM-dd).
        lines: Draft lines (same structure as create_invoice_draft).
        invoice_text: Text printed above invoice lines.
        our_reference: Your company's reference.
        your_reference: Customer's reference.
        order_reference: EHF order reference.
        currency: ISO 4217 currency code.
        payment_account: Payment account code.
        contact_person_id: Contact person ID.
        project_id: Project ID to associate with.
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {
        "type": draft_type,
        "customerId": customer_id,
        "daysUntilDueDate": days_until_due_date,
    }
    if issue_date:
        body["issueDate"] = issue_date
    if lines:
        body["lines"] = lines
    if invoice_text:
        body["invoiceText"] = invoice_text
    if our_reference:
        body["ourReference"] = our_reference
    if your_reference:
        body["yourReference"] = your_reference
    if order_reference:
        body["orderReference"] = order_reference
    if currency:
        body["currency"] = currency
    if payment_account:
        body["paymentAccount"] = payment_account
    if contact_person_id is not None:
        body["contactPersonId"] = contact_person_id
    if project_id is not None:
        body["projectId"] = project_id
    return await client.put(
        f"/companies/{slug}/invoices/drafts/{draft_id}", json=body
    )


@mcp.tool()
async def send_invoice(
    invoice_id: int,
    method: list[str],
    company_slug: str | None = None,
    include_document_attachments: bool = True,
    recipient_name: str | None = None,
    recipient_email: str | None = None,
    message: str | None = None,
    email_send_option: str | None = None,
) -> dict:
    """Send an invoice via the specified method(s).

    Args:
        invoice_id: The invoice ID to send.
        method: Delivery methods in priority order. Options: 'auto', 'email', 'ehf', 'efaktura', 'sms', 'letter'.
        company_slug: Company identifier (uses default if not provided).
        include_document_attachments: Include document attachments when sending (default True).
        recipient_name: Override recipient name.
        recipient_email: Override recipient email.
        message: Additional message to send with the invoice.
        email_send_option: 'document_link', 'attachment', or 'auto'.
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {
        "invoiceId": invoice_id,
        "method": method,
        "includeDocumentAttachments": include_document_attachments,
    }
    if recipient_name:
        body["recipientName"] = recipient_name
    if recipient_email:
        body["recipientEmail"] = recipient_email
    if message:
        body["message"] = message
    if email_send_option:
        body["emailSendOption"] = email_send_option
    return await client.post(f"/companies/{slug}/invoices/send", json=body)
