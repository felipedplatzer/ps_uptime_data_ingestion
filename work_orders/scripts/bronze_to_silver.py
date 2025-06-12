import pandas as pd
import settings
import all_datasets



def bronze_to_silver(df, company_name):
    # Customer-specific raw_to_bronze processing
    if company_name == 'SUMMA':
        #from work_orders.scripts.customer_specific_scripts.summa import summa
        #df = summa(df)
        pass
    elif company_name == 'CHRISTIANA':
        from work_orders.scripts.customer_specific_scripts.christiana import christiana
        df = christiana(df) 
    elif company_name == 'WAKEMED':
        from work_orders.scripts.customer_specific_scripts.wakemed import wakemed
        df = wakemed(df)
    elif company_name == 'MARSHFIELD':
        from work_orders.scripts.customer_specific_scripts.marshfield import marshfield
        df = marshfield(df)
    elif company_name == 'METHODIST':
        from work_orders.scripts.customer_specific_scripts.methodist import methodist
        df = methodist(df)
    elif company_name == 'PIEDMONT':
        from work_orders.scripts.customer_specific_scripts.piedmont import piedmont
        df = piedmont(df)
    # Add company name
    df['company_name'] = company_name.upper()

    # Remove all duplicate rows (i.e. rows with all attributes being equal)
    df = all_datasets.remove_duplicate_rows(df)

    # Remove rows with duplicate work order id. 
    df = df.drop_duplicates(subset=['work_order_id'])

    # Standardize fields
    std_fields = ['downtime_impact', 'work_order_status' ,'type'] # MISSING resolution and problem_cause, since these are not yet standardized on uptime
    for f in std_fields:
        df = all_datasets.standardize_field(df, f, 'work_orders')


    #Return
    return df

