import pandas as pd
import settings
import all_datasets


def bronze_to_silver(df, company_name):

 # Customer-specific raw_to_bronze processing
    if company_name == 'SUMMA':
        #from parts.scripts.customer_specific_scripts.summa import summa
        #df = summa(df)
        pass
    elif company_name == 'CHRISTIANA':
        from parts.scripts.customer_specific_scripts.christiana import christiana
        df = christiana(df) 

    # Add company name
    df['company_name'] = company_name.upper()

    # Remove all duplicate rows (i.e. rows with all attributes being equal)
    df = all_datasets.remove_duplicate_rows(df)

    # Remove rows with duplicate parts_sys_id
    df = df.drop_duplicates(subset=['parts_sys_id'])

    
    # Handle cost conversion
    cost_columns = ['cost','cost_per_unit']
    for x in cost_columns:
        if x in df.columns:
            # Replace NULL values with NaN to preserve them
            df[x] = df[x].replace('NULL', pd.NA)
            # Convert non-NULL values to numeric, removing '$' and parentheses
            df[x] = pd.to_numeric(
                df[x].astype(str).str.replace('$', '').str.replace('(', '-').str.replace(')', ''),
                errors='coerce'
            )
            # Round to 2 decimals
            df[x] = df[x].round(2)
    
    # Process quantity
    if 'quantity' in list(df.columns):
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').astype('Int64')

    
    # Standardize fields
    std_fields = ['inventoried_part']
    for f in std_fields:
        df = all_datasets.standardize_field(df, f, 'parts')


    #Return
    return df
