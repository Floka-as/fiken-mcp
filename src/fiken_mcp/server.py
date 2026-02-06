import asyncio

from fastmcp import FastMCP

from .client import FikenClient
from .config import settings
from .errors import CompanySlugRequiredError

mcp = FastMCP("fiken-mcp")
client = FikenClient()


def resolve_company_slug(company_slug: str | None) -> str:
    if company_slug:
        return company_slug
    if settings.fiken_default_company_slug:
        return settings.fiken_default_company_slug
    raise CompanySlugRequiredError()


# Import tool modules to register them with the mcp instance.
# Must be after mcp/client/resolve_company_slug are defined.
from .tools import (  # noqa: E402, F401
    accounts,
    company,
    contacts,
    credit_notes,
    invoices,
    journal,
    products,
    projects,
    purchases,
    sales,
    time_tracking,
)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
