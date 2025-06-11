import pandas as pd


def raw_to_bronze_allcustomers(df):
    # Remove rows with multiple asset IDs (containing commas)
    df = df[~df['asset_sys_id'].astype(str).str.contains(',')]
    
    # Convert acquisition_cost to numeric, handling NULLs and 0s properly
    if 'acquisition_cost' in df.columns:
        # Replace $ and parentheses, convert to numeric
        df['acquisition_cost'] = df['acquisition_cost'].astype(str).str.replace('$', '').str.replace('(', '-').str.replace(')', '')
        # Convert to numeric, errors='coerce' will set invalid values to NaN
        df['acquisition_cost'] = pd.to_numeric(df['acquisition_cost'], errors='coerce')

    return df




# Main
def raw_to_bronze(df, company_name):
    # Customer-specific raw_to_bronze processing
    if company_name == 'SUMMA':
        from customer_specific_scripts.raw_to_bronze_summa import raw_to_bronze_summa
        df_new = raw_to_bronze_summa(df)
    elif company_name == 'CHRISTIANA':
        from customer_specific_scripts.raw_to_bronze_christiana import raw_to_bronze_christiana
        df_new = raw_to_bronze_christiana(df)
    # Standard raw-to-bronze processing
    df_new = raw_to_bronze_allcustomers(df_new)
    # Add company name
    df_new['company_name'] = company_name.upper()
    # Return new assets of customer for future processing
    return df_new