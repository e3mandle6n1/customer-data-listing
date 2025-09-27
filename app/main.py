from fastapi import FastAPI, Query
from typing import Optional
from contextlib import asynccontextmanager
from . import data_handler, schemas

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Application starting up...")
    data_handler.load_customer_data(file_path="data/customers.csv")
    yield
    print("👋 Application shutting down...")

app = FastAPI(
    title="Customer Data Listing API",
    description="An API to list, filter, sort, and paginate customer data from a CSV file.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/api/customers", response_model=schemas.PaginatedCustomerResponse)
def read_customers(
    search: Optional[str] = Query(None, description="Search by name and email"),
    isActive: Optional[bool] = Query(None, description="Filter by active status"),
    countryCode: Optional[str] = Query(None, description="Filter by country code"),
    sortBy: Optional[str] = Query("date", description="Sort by: name, email, date, country"),
    sortDirection: Optional[str] = Query("desc", description="Sort direction: asc, desc"),
    page: int = Query(1, ge=1, description="Page number"),
    pageSize: int = Query(10, ge=1, le=100, description="Items per page"),
):
    """
    Retrieves a paginated, sorted, and filtered list of customers.
    """
    return data_handler.get_customers(
        page=page, page_size=pageSize, search=search,
        is_active=isActive, country_code=countryCode,
        sort_by=sortBy, sort_direction=sortDirection,
    )