import pandas as pd
import settings
import all_datasets


def bronze_to_silver(df, company_name):

    # Customer-specific raw_to_bronze processing
    if company_name == 'SUMMA':
        #from labor.scripts.customer_specific_scripts.summa import summa
        #df = summa(df)
        pass
    elif company_name == 'CHRISTIANA':
        from labor.scripts.customer_specific_scripts.christiana import christiana
        df = christiana(df) 
    elif company_name == 'WAKEMED':
        from labor.scripts.customer_specific_scripts.wakemed import wakemed
        df = wakemed(df)
    elif company_name == 'MARSHFIELD':
        from labor.scripts.customer_specific_scripts.marshfield import marshfield
        df = marshfield(df)
    elif company_name == 'METHODIST':
        from labor.scripts.customer_specific_scripts.methodist import methodist
        df = methodist(df)
    elif company_name == 'PIEDMONT':
        from labor.scripts.customer_specific_scripts.piedmont import piedmont
        df = piedmont(df)
    # Add company name
    df['company_name'] = company_name.upper()

    # Remove all duplicate rows (i.e. rows with all attributes being equal)
    df = all_datasets.remove_duplicate_rows(df)

    # Remove rows with duplicate labor_sys_id
    df = df.drop_duplicates(subset=['labor_sys_id'])

    # Convert date columns to datetime
    date_columns = ['service_date']
    for col in date_columns:
        if col in list(df.columns):
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Handle cost conversion
    if 'cost' in df.columns:
        # Replace NULL values with NaN to preserve them
        df['cost'] = df['cost'].replace('NULL', pd.NA)
        # Convert non-NULL values to numeric, removing '$' and parentheses
        df['cost'] = pd.to_numeric(
            df['cost'].astype(str).str.replace('$', '').str.replace('(', '-').str.replace(')', ''),
            errors='coerce'
        )
        # Round to 2 decimals
        df['cost'] = df['cost'].round(2)
    
    # Handle duration conversion
    if 'duration' in df.columns:
        # Replace NULL values with NaN to preserve them
        df['duration'] = df['duration'].replace('NULL', pd.NA)
        # Convert non-NULL values to numeric
        df['duration'] = pd.to_numeric(df['duration'], errors='coerce')


    # Standardize fields
    std_fields = ['labor_type']
    for f in std_fields:
        df = all_datasets.standardize_field(df, f, 'labor')

    #Return
    return df
