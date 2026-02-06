from ..server import client, mcp, resolve_company_slug


@mcp.tool(annotations={"readOnlyHint": True})
async def list_purchases(
    company_slug: str | None = None,
    date: str | None = None,
    date_le: str | None = None,
    date_ge: str | None = None,
    sort_by: str | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """List purchases for a company.

    Args:
        company_slug: Company identifier (uses default if not provided).
        date: Filter by exact date (yyyy-MM-dd).
        date_le: Date less than or equal to.
        date_ge: Date greater than or equal to.
        sort_by: Sort order: 'date asc' or 'date desc'.
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
    if sort_by:
        params["sortBy"] = sort_by
    return await client.get_with_pagination(
        f"/companies/{slug}/purchases", params=params
    )


@mcp.tool(annotations={"readOnlyHint": True})
async def get_purchase(
    purchase_id: int,
    company_slug: str | None = None,
) -> dict:
    """Get a specific purchase by ID.

    Args:
        purchase_id: The purchase ID.
        company_slug: Company identifier (uses default if not provided).
    """
    slug = resolve_company_slug(company_slug)
    return await client.get(f"/companies/{slug}/purchases/{purchase_id}")


@mcp.tool()
async def create_purchase(
    date: str,
    kind: str,
    lines: list[dict],
    currency: str = "NOK",
    company_slug: str | None = None,
    identifier: str | None = None,
    due_date: str | None = None,
    supplier_id: int | None = None,
    kid: str | None = None,
    payment_account: str | None = None,
    payment_date: str | None = None,
    payment_amount_in_nok: int | None = None,
    project_id: int | None = None,
) -> dict:
    """Create a new purchase.

    Args:
        date: Purchase date (yyyy-MM-dd).
        kind: Purchase type: 'cash_purchase' or 'supplier'.
        lines: Order lines. Each dict must contain: description, vatType.
               Also provide: netPrice (cents in NOK) or netPriceInCurrency (cents),
               account (expense account, e.g. '7100').
               Optional: vat (cents), vatInCurrency (cents), projectId.
        currency: ISO 4217 currency code (default 'NOK').
        company_slug: Company identifier (uses default if not provided).
        identifier: Invoice/receipt number from supplier.
        due_date: Due date (yyyy-MM-dd) for supplier purchases.
        supplier_id: Contact ID of the supplier (required for kind='supplier').
        kid: Norwegian KID number (2-25 digits).
        payment_account: Payment account code (e.g. '1920:10001').
        payment_date: Payment date (yyyy-MM-dd).
        payment_amount_in_nok: Actual NOK amount paid for foreign currency (cents).
        project_id: Project ID to associate with.
    """
    slug = resolve_company_slug(company_slug)
    paid = payment_account is not None or kind == "cash_purchase"
    body: dict = {
        "date": date,
        "kind": kind,
        "lines": lines,
        "currency": currency,
        "paid": paid,
    }
    if identifier:
        body["identifier"] = identifier
    if due_date:
        body["dueDate"] = due_date
    if supplier_id is not None:
        body["supplierId"] = supplier_id
    if kid:
        body["kid"] = kid
    if payment_account:
        body["paymentAccount"] = payment_account
    if payment_date:
        body["paymentDate"] = payment_date
    if payment_amount_in_nok is not None:
        body["paymentAmountInNok"] = payment_amount_in_nok
    if project_id is not None:
        body["projectId"] = project_id
    return await client.post(f"/companies/{slug}/purchases", json=body)


@mcp.tool()
async def create_purchase_payment(
    purchase_id: int,
    date: str,
    account: str,
    amount: int,
    company_slug: str | None = None,
    currency: str | None = None,
    amount_in_nok: int | None = None,
    fee: int | None = None,
) -> dict:
    """Register a payment for an existing purchase.

    Args:
        purchase_id: The purchase ID to register payment for.
        date: Payment date (yyyy-MM-dd).
        account: Payment account code (e.g. '1920:10001').
        amount: Amount paid in cents (e.g. 10050 = 100.50).
        company_slug: Company identifier (uses default if not provided).
        currency: ISO 4217 currency code if not NOK.
        amount_in_nok: Actual NOK amount paid for foreign currency payments (cents).
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
        f"/companies/{slug}/purchases/{purchase_id}/payments", json=body
    )
