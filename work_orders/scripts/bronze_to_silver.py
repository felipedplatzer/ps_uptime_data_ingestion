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

    # Add company name
    df['company_name'] = company_name.upper()

    # Remove all duplicate rows (i.e. rows with all attributes being equal)
    df = all_datasets.remove_duplicate_rows(df)

    # Remove rows with duplicate work order id (this work order id combines the original work order id and the asset id, so that work order id's that apply to multiple assets are valid)
    df = df.drop_duplicates(subset=['work_order_id'])

    # Standardize fields
    std_fields = ['downtime_impact', 'work_order_status' ,'type'] # MISSING resolution and problem_cause, since these are not yet standardized on uptime
    for f in std_fields:
        df = all_datasets.standardize_field(df, f, 'work_orders')


    #Return
    return df

# MISSING: PARSE FIELDS! like resolution_detail
# Remove "PM Annual - Next Scheduled Date: dd/mm/yyyy" from order_summary
##"Remove dates and names from order_summary. Example (raw data): (TC 01/02/2018 02:01:24 PM, ZELLNER, JASON) 
#"Remove dates from resolution_detail (example raw resolution_detail: MM-MIndray A5 training.-2019-05-13 13:15:08
# Resolution not yet standardized in Uptime -> leave for later
# Problem_cause not yet standardized in Uptime -> leave for later