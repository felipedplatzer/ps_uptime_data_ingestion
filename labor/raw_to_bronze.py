import pandas as pd



def raw_to_bronze_allcustomers(df):
    
    # Create a copy of the dataframe to avoid modifying the original
    df_new = df.copy()
    
    # Handle cost conversion
    if 'cost' in df_new.columns:
        # Replace NULL values with NaN to preserve them
        df_new['cost'] = df_new['cost'].replace('NULL', pd.NA)
        # Convert non-NULL values to numeric, removing '$' and parentheses
        df_new['cost'] = pd.to_numeric(
            df_new['cost'].astype(str).str.replace('$', '').str.replace('(', '-').str.replace(')', ''),
            errors='coerce'
        )
    
    # Handle duration conversion
    if 'duration' in df_new.columns:
        # Replace NULL values with NaN to preserve them
        df_new['duration'] = df_new['duration'].replace('NULL', pd.NA)
        # Convert non-NULL values to numeric
        df_new['duration'] = pd.to_numeric(df_new['duration'], errors='coerce')
    
    return df_new


# Main
def raw_to_bronze(df, company_name):
    # Customer-specific raw_to_bronze processing
    if company_name == 'SUMMA':
        #from customer_specific_scripts.raw_to_bronze_summa import raw_to_bronze_summa
        #df_new = raw_to_bronze_summa(df)
        pass
    elif company_name == 'CHRISTIANA':
        from customer_specific_scripts.raw_to_bronze_christiana import raw_to_bronze_christiana
        df_new = raw_to_bronze_christiana(df) 
    # Standard raw-to-bronze processing
    df_new = raw_to_bronze_allcustomers(df_new)
    # Add company name
    df_new['company_name'] = company_name.upper()
    # Return new assets of customer for future processing
    return df_new