import pandas as pd
from slugify import slugify
from typing import Optional
from . import schemas

customer_df = pd.DataFrame()

def load_customer_data(file_path: str):
    """
    Loads and prepares customer data from a CSV file.
    This is called once when the application starts.
    """
    global customer_df
    try:
        df = pd.read_csv(file_path)
        
        # --- Data Cleaning and Type Conversion ---
        df.columns = [col.lower() for col in df.columns]
        df['createddate'] = pd.to_datetime(df['createddate'])
        df['isactive'] = df['isactive'].astype(bool)
        
        customer_df = df
        print(f"✅ Successfully loaded and prepared {len(customer_df)} customer records.")
    except Exception as e:
        print(f"❌ ERROR: Failed to load data from {file_path}. Reason: {e}")
        customer_df = pd.DataFrame()


def get_customers(
    page: int, page_size: int, search: Optional[str] = None,
    is_active: Optional[bool] = None, country_code: Optional[str] = None,
    sort_by: Optional[str] = None, sort_direction: Optional[str] = None,
):
    query_df = customer_df.copy()

    # --- Filtering ---
    if search:
        query_df = query_df[
            query_df['name'].str.contains(search, case=False, na=False) |
            query_df['email'].str.contains(search, case=False, na=False)
        ]
    if is_active is not None:
        query_df = query_df[query_df['isactive'] == is_active]
    if country_code:
        query_df = query_df[query_df['countrycode'].str.upper() == country_code.upper()]

    # Get total count after filtering
    total_count = len(query_df)

    # --- Sorting ---
    if sort_by:
        column_map = {"name": "name", "email": "email", "date": "createddate", "country": "countrycode"}
        sort_column_name = column_map.get(slugify(sort_by))
        
        if sort_column_name:
            is_ascending = not (sort_direction and sort_direction.lower() == "desc")
            query_df = query_df.sort_values(by=sort_column_name, ascending=is_ascending)

    # --- Pagination ---
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_df = query_df.iloc[start_index:end_index]

    # --- Formatting for Response ---
    paginated_df = paginated_df.rename(columns={
        "createddate": "created_date", "isactive": "is_active", "countrycode": "country_code"
    })
    customers_data = paginated_df.to_dict(orient='records')
    
    return schemas.PaginatedCustomerResponse(total_count=total_count, customers=customers_data)