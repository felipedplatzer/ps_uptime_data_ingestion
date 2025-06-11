import pandas as pd





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
    #df_new = raw_to_bronze_allcustomers(df_new)
    # Add company name
    df_new['company_name'] = company_name.upper()
    # Return new assets of customer for future processing
    return df_new