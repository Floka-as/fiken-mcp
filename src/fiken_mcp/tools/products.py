from ..server import client, mcp, resolve_company_slug


@mcp.tool(annotations={"readOnlyHint": True})
async def list_products(
    company_slug: str | None = None,
    name: str | None = None,
    product_number: str | None = None,
    active: bool | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """List products for a company.

    Args:
        company_slug: Company identifier (uses default if not provided).
        name: Filter by exact product name.
        product_number: Filter by product number (varenummer).
        active: True for active products, False for inactive.
        page: Page number (0-indexed).
        page_size: Number of results per page (max 100).
    """
    slug = resolve_company_slug(company_slug)
    params: dict = {"page": page, "pageSize": page_size}
    if name:
        params["name"] = name
    if product_number:
        params["productNumber"] = product_number
    if active is not None:
        params["active"] = active
    return await client.get_with_pagination(
        f"/companies/{slug}/products", params=params
    )


@mcp.tool(annotations={"readOnlyHint": True})
async def get_product(
    product_id: int,
    company_slug: str | None = None,
) -> dict:
    """Get a specific product by ID.

    Args:
        product_id: The product ID.
        company_slug: Company identifier (uses default if not provided).
    """
    slug = resolve_company_slug(company_slug)
    return await client.get(f"/companies/{slug}/products/{product_id}")


@mcp.tool()
async def create_product(
    name: str,
    income_account: str,
    vat_type: str,
    company_slug: str | None = None,
    unit_price: int | None = None,
    active: bool = True,
    product_number: str | None = None,
    stock: float | None = None,
    note: str | None = None,
) -> dict:
    """Create a new product.

    Args:
        name: Product name.
        income_account: Accounting income account code (e.g. '3000').
        vat_type: VAT type: HIGH, MEDIUM, LOW, EXEMPT, EXEMPT_IMPORT_EXPORT, EXEMPT_REVERSE, OUTSIDE, or NONE.
        company_slug: Company identifier (uses default if not provided).
        unit_price: Net unit price in cents (e.g. 10050 = 100.50 NOK).
        active: Whether the product is active (default True).
        product_number: Custom product number (varenummer).
        stock: Stock quantity (decimal allowed, e.g. 5.5).
        note: Optional note (max 200 chars).
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {
        "name": name,
        "incomeAccount": income_account,
        "vatType": vat_type,
        "active": active,
    }
    if unit_price is not None:
        body["unitPrice"] = unit_price
    if product_number:
        body["productNumber"] = product_number
    if stock is not None:
        body["stock"] = stock
    if note:
        body["note"] = note
    return await client.post(f"/companies/{slug}/products", json=body)


@mcp.tool()
async def update_product(
    product_id: int,
    name: str,
    income_account: str,
    vat_type: str,
    company_slug: str | None = None,
    unit_price: int | None = None,
    active: bool = True,
    product_number: str | None = None,
    stock: float | None = None,
    note: str | None = None,
) -> dict:
    """Update an existing product (full replacement).

    Args:
        product_id: The product ID to update.
        name: Product name.
        income_account: Accounting income account code (e.g. '3000').
        vat_type: VAT type: HIGH, MEDIUM, LOW, EXEMPT, EXEMPT_IMPORT_EXPORT, EXEMPT_REVERSE, OUTSIDE, or NONE.
        company_slug: Company identifier (uses default if not provided).
        unit_price: Net unit price in cents (e.g. 10050 = 100.50 NOK).
        active: Whether the product is active (default True).
        product_number: Custom product number (varenummer).
        stock: Stock quantity (decimal allowed).
        note: Optional note (max 200 chars).
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {
        "name": name,
        "incomeAccount": income_account,
        "vatType": vat_type,
        "active": active,
    }
    if unit_price is not None:
        body["unitPrice"] = unit_price
    if product_number:
        body["productNumber"] = product_number
    if stock is not None:
        body["stock"] = stock
    if note:
        body["note"] = note
    return await client.put(
        f"/companies/{slug}/products/{product_id}", json=body
    )
