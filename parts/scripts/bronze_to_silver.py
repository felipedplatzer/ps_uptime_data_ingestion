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
    elif company_name == 'WAKEMED':
        from parts.scripts.customer_specific_scripts.wakemed import wakemed
        df = wakemed(df)
    elif company_name == 'MARSHFIELD':
        from parts.scripts.customer_specific_scripts.marshfield import marshfield
        df = marshfield(df)
    elif company_name == 'METHODIST':
        from parts.scripts.customer_specific_scripts.methodist import methodist
        df = methodist(df)
    elif company_name == 'PIEDMONT':
        from parts.scripts.customer_specific_scripts.piedmont import piedmont
        df = piedmont(df)
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
        #df['quantity'] = df['quantity'].astype('Int64')
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce') #.astype('Int64')




    # Calculate quantity, cost, or unit_cost if it's missing and the 2 other values are available
    if 'quantity' not in list(df.columns) and 'cost' in list(df.columns) and 'unit_cost' in list(df.columns):
        df['quantity'] = df['cost'] / df['unit_cost']
        df['quantity'] = df['quantity'].round()
    
    if 'cost' not in list(df.columns) and 'quantity' in list(df.columns) and 'unit_cost' in list(df.columns):
        df['cost'] = df['unit_cost'] * df['quantity']
        df['cost'] = df['cost'].round(2)
    
    if 'unit_cost' not in list(df.columns) and 'quantity' in list(df.columns) and 'cost' in list(df.columns):
        df['unit_cost'] = df['cost'] / df['quantity']
        df['unit_cost'] = df['unit_cost'].round(2)
    
    # Standardize fields
    std_fields = ['inventoried_part']
    for f in std_fields:
        df = all_datasets.standardize_field(df, f, 'parts')
    #Return
    return df
