from ..server import client, mcp, resolve_company_slug


@mcp.tool(annotations={"readOnlyHint": True})
async def list_contacts(
    company_slug: str | None = None,
    name: str | None = None,
    email: str | None = None,
    customer: bool | None = None,
    supplier: bool | None = None,
    inactive: bool | None = None,
    group: str | None = None,
    sort_by: str | None = None,
    customer_number: int | None = None,
    supplier_number: int | None = None,
    page: int = 0,
    page_size: int = 25,
) -> dict:
    """List contacts for a company.

    Args:
        company_slug: Company identifier (uses default if not provided).
        name: Filter by exact name match.
        email: Filter by exact email match.
        customer: True to return only customers.
        supplier: True to return only suppliers.
        inactive: True for inactive contacts, False for active.
        group: Filter by contact group name (exact match, customers only).
        sort_by: Sort order, e.g. 'lastModified asc', 'createdDate desc'.
        customer_number: Filter by customer number.
        supplier_number: Filter by supplier number.
        page: Page number (0-indexed).
        page_size: Number of results per page (max 100).
    """
    slug = resolve_company_slug(company_slug)
    params: dict = {"page": page, "pageSize": page_size}
    if name:
        params["name"] = name
    if email:
        params["email"] = email
    if customer is not None:
        params["customer"] = customer
    if supplier is not None:
        params["supplier"] = supplier
    if inactive is not None:
        params["inactive"] = inactive
    if group:
        params["group"] = group
    if sort_by:
        params["sortBy"] = sort_by
    if customer_number is not None:
        params["customerNumber"] = customer_number
    if supplier_number is not None:
        params["supplierNumber"] = supplier_number
    return await client.get_with_pagination(
        f"/companies/{slug}/contacts", params=params
    )


@mcp.tool(annotations={"readOnlyHint": True})
async def get_contact(
    contact_id: int,
    company_slug: str | None = None,
) -> dict:
    """Get a specific contact by ID.

    Args:
        contact_id: The contact ID.
        company_slug: Company identifier (uses default if not provided).
    """
    slug = resolve_company_slug(company_slug)
    return await client.get(f"/companies/{slug}/contacts/{contact_id}")


@mcp.tool()
async def create_contact(
    name: str,
    company_slug: str | None = None,
    email: str | None = None,
    phone_number: str | None = None,
    customer: bool = False,
    supplier: bool = False,
    organization_number: str | None = None,
    bank_account_number: str | None = None,
    currency: str | None = None,
    language: str | None = None,
    days_until_invoicing_due_date: int | None = None,
    street_address: str | None = None,
    street_address_line2: str | None = None,
    city: str | None = None,
    post_code: str | None = None,
    country: str = "Norway",
    member_number_string: str | None = None,
) -> dict:
    """Create a new contact.

    Args:
        name: Contact name (required).
        company_slug: Company identifier (uses default if not provided).
        email: Contact email.
        phone_number: Contact phone number.
        customer: True if contact is a customer.
        supplier: True if contact is a supplier.
        organization_number: Brreg organization number.
        bank_account_number: Bank account number (max 11 digits).
        currency: Default foreign currency code (e.g. 'USD', 'EUR').
        language: Document language: 'NORWEGIAN' or 'ENGLISH'.
        days_until_invoicing_due_date: Default days until invoice due date.
        street_address: Street address.
        street_address_line2: Street address line 2.
        city: City.
        post_code: Postal code.
        country: Country (default 'Norway').
        member_number_string: Custom member number/ID for your own data.
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {
        "name": name,
        "customer": customer,
        "supplier": supplier,
        "address": {"country": country},
    }
    if email:
        body["email"] = email
    if phone_number:
        body["phoneNumber"] = phone_number
    if organization_number:
        body["organizationNumber"] = organization_number
    if bank_account_number:
        body["bankAccountNumber"] = bank_account_number
    if currency:
        body["currency"] = currency
    if language:
        body["language"] = language
    if days_until_invoicing_due_date is not None:
        body["daysUntilInvoicingDueDate"] = days_until_invoicing_due_date
    if member_number_string:
        body["memberNumberString"] = member_number_string
    if street_address:
        body["address"]["streetAddress"] = street_address
    if street_address_line2:
        body["address"]["streetAddressLine2"] = street_address_line2
    if city:
        body["address"]["city"] = city
    if post_code:
        body["address"]["postCode"] = post_code
    return await client.post(f"/companies/{slug}/contacts", json=body)


@mcp.tool()
async def update_contact(
    contact_id: int,
    name: str,
    company_slug: str | None = None,
    email: str | None = None,
    phone_number: str | None = None,
    customer: bool = False,
    supplier: bool = False,
    organization_number: str | None = None,
    bank_account_number: str | None = None,
    currency: str | None = None,
    language: str | None = None,
    inactive: bool | None = None,
    days_until_invoicing_due_date: int | None = None,
    street_address: str | None = None,
    street_address_line2: str | None = None,
    city: str | None = None,
    post_code: str | None = None,
    country: str = "Norway",
    member_number_string: str | None = None,
) -> dict:
    """Update an existing contact (full replacement).

    Args:
        contact_id: The contact ID.
        name: Contact name (required).
        company_slug: Company identifier (uses default if not provided).
        email: Contact email.
        phone_number: Contact phone number.
        customer: True if contact is a customer.
        supplier: True if contact is a supplier.
        organization_number: Brreg organization number.
        bank_account_number: Bank account number.
        currency: Default foreign currency code.
        language: Document language: 'NORWEGIAN' or 'ENGLISH'.
        inactive: True to deactivate the contact.
        days_until_invoicing_due_date: Default days until invoice due date.
        street_address: Street address.
        street_address_line2: Street address line 2.
        city: City.
        post_code: Postal code.
        country: Country (default 'Norway').
        member_number_string: Custom member number/ID for your own data.
    """
    slug = resolve_company_slug(company_slug)
    body: dict = {
        "name": name,
        "customer": customer,
        "supplier": supplier,
        "address": {"country": country},
    }
    if email:
        body["email"] = email
    if phone_number:
        body["phoneNumber"] = phone_number
    if organization_number:
        body["organizationNumber"] = organization_number
    if bank_account_number:
        body["bankAccountNumber"] = bank_account_number
    if currency:
        body["currency"] = currency
    if language:
        body["language"] = language
    if inactive is not None:
        body["inactive"] = inactive
    if days_until_invoicing_due_date is not None:
        body["daysUntilInvoicingDueDate"] = days_until_invoicing_due_date
    if member_number_string:
        body["memberNumberString"] = member_number_string
    if street_address:
        body["address"]["streetAddress"] = street_address
    if street_address_line2:
        body["address"]["streetAddressLine2"] = street_address_line2
    if city:
        body["address"]["city"] = city
    if post_code:
        body["address"]["postCode"] = post_code
    return await client.put(f"/companies/{slug}/contacts/{contact_id}", json=body)


@mcp.tool(annotations={"readOnlyHint": True})
async def list_contact_groups(
    company_slug: str | None = None,
) -> dict:
    """List all customer contact groups for a company.

    Args:
        company_slug: Company identifier (uses default if not provided).
    """
    slug = resolve_company_slug(company_slug)
    return await client.get(f"/companies/{slug}/groups")
