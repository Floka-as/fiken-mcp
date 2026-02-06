from ..server import client, mcp, resolve_company_slug


@mcp.tool(annotations={"readOnlyHint": True})
async def list_sales(
    company_slug: str | None = None,
    date: str | None = None,
    date_le: str | None = None,
    date_ge: str | None = None,
    contact_id: int | None = None,
    sale_number: str | None = None,
    settled: bool | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """List sales for a company. Use this for 'Annet salg' (other sales, not Fiken-issued invoices).

    Args:
        company_slug: Company identifier (uses default if not provided).
        date: Filter by exact date (yyyy-MM-dd).
        date_le: Date less than or equal to.
        date_ge: Date greater than or equal to.
        contact_id: Filter by customer contact ID.
        sale_number: Filter by sale number.
        settled: True for settled sales only, False for unsettled.
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
    if contact_id is not None:
        params["contactId"] = contact_id
    if sale_number:
        params["saleNumber"] = sale_number
    if settled is not None:
        params["settled"] = settled
    return await client.get_with_pagination(
        f"/companies/{slug}/sales", params=params
    )


@mcp.tool(annotations={"readOnlyHint": True})
async def get_sale(
    sale_id: int,
    company_slug: str | None = None,
) -> dict:
    """Get a specific sale by ID.

    Args:
        sale_id: The sale ID.
        company_slug: Company identifier (uses default if not provided).
    """
    slug = resolve_company_slug(company_slug)
    return await client.get(f"/companies/{slug}/sales/{sale_id}")


@mcp.tool()
async def create_sale(
    date: str,
    kind: str,
    lines: list[dict],
    currency: str = "NOK",
    company_slug: str | None = None,
    sale_number: str | None = None,
    customer_id: int | None = None,
    due_date: str | None = None,
    kid: str | None = None,
    payment_account: str | None = None,
    payment_date: str | None = None,
    payment_fee: int | None = None,
    project_id: int | None = None,
    total_paid: int | None = None,
    total_paid_in_currency: int | None = None,
) -> dict:
    """Create a new sale ('Annet salg'). Use for sales where invoice was created outside Fiken.

    Args:
        date: Sale date (yyyy-MM-dd).
        kind: Sale type: 'cash_sale', 'invoice', or 'external_invoice'.
        lines: Order lines. Each dict must contain: description, vatType, and either
               netPrice (cents in NOK) or netPriceInCurrency (cents in specified currency).
               Optional: account (e.g. '3000'), vat (cents), vatInCurrency (cents).
        currency: ISO 4217 currency code (default 'NOK').
        company_slug: Company identifier (uses default if not provided).
        sale_number: Custom sale identifier.
        customer_id: Contact ID of the customer.
        due_date: Due date for invoice-type sales (yyyy-MM-dd).
        kid: Norwegian KID number (2-25 digits).
        payment_account: Payment account code (e.g. '1920:10001').
        payment_date: Payment date (yyyy-MM-dd).
        payment_fee: Payment fee in cents.
        project_id: Project ID to associate with.
        total_paid: Total amount paid in NOK (cents).
        total_paid_in_currency: Total amount paid in foreign currency (cents).
    """
    slug = resolve_company_slug(company_slug)
    paid = payment_account is not None or kind == "cash_sale"
    body: dict = {
        "date": date,
        "kind": kind,
        "lines": lines,
        "currency": currency,
        "paid": paid,
    }
    if sale_number:
        body["saleNumber"] = sale_number
    if customer_id is not None:
        body["customerId"] = customer_id
    if due_date:
        body["dueDate"] = due_date
    if kid:
        body["kid"] = kid
    if payment_account:
        body["paymentAccount"] = payment_account
    if payment_date:
        body["paymentDate"] = payment_date
    if payment_fee is not None:
        body["paymentFee"] = payment_fee
    if project_id is not None:
        body["projectId"] = project_id
    if total_paid is not None:
        body["totalPaid"] = total_paid
    if total_paid_in_currency is not None:
        body["totalPaidInCurrency"] = total_paid_in_currency
    return await client.post(f"/companies/{slug}/sales", json=body)


@mcp.tool()
async def create_sale_payment(
    sale_id: int,
    date: str,
    account: str,
    amount: int,
    company_slug: str | None = None,
    currency: str | None = None,
    amount_in_nok: int | None = None,
    fee: int | None = None,
) -> dict:
    """Register a payment for an existing sale.

    Args:
        sale_id: The sale ID to register payment for.
        date: Payment date (yyyy-MM-dd).
        account: Payment account code (e.g. '1920:10001').
        amount: Amount paid in cents (e.g. 10050 = 100.50).
        company_slug: Company identifier (uses default if not provided).
        currency: ISO 4217 currency code if not NOK.
        amount_in_nok: Actual NOK amount received for foreign currency payments (cents).
        fee: Additional fee in NOK cents.
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {
        "date": date,
        "account": account,
        "amount": amount,
    }
    if currency:
        body["currency"] = currency
    if amount_in_nok is not None:
        body["amountInNok"] = amount_in_nok
    if fee is not None:
        body["fee"] = fee
    return await client.post(
        f"/companies/{slug}/sales/{sale_id}/payments", json=body
    )
