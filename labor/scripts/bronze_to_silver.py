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

    # Add company name
    df['company_name'] = company_name.upper()

    # Remove all duplicate rows (i.e. rows with all attributes being equal)
    df = all_datasets.remove_duplicate_rows(df)

    # Remove rows with duplicate labor_sys_id
    df = df.drop_duplicates(subset=['labor_sys_id'])

    # Handle cost conversion
    if 'cost' in df.columns:
        # Replace NULL values with NaN to preserve them
        df['cost'] = df['cost'].replace('NULL', pd.NA)
        # Convert non-NULL values to numeric, removing '$' and parentheses
        df['cost'] = pd.to_numeric(
            df['cost'].astype(str).str.replace('$', '').str.replace('(', '-').str.replace(')', ''),
            errors='coerce'
        )
    
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

# MISSING: PARSE FIELDS! like resolution_detail
# Remove "PM Annual - Next Scheduled Date: dd/mm/yyyy" from order_summary
##"Remove dates and names from order_summary. Example (raw data): (TC 01/02/2018 02:01:24 PM, ZELLNER, JASON) 
#"Remove dates from resolution_detail (example raw resolution_detail: MM-MIndray A5 training.-2019-05-13 13:15:08
# Resolution not yet standardized in Uptime -> leave for later
# Problem_cause not yet standardized in Uptime -> leave for later