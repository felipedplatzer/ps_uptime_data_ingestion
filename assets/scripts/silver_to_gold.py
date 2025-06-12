import pandas as pd
from datetime import datetime


def silver_to_gold(df):
    # Convert date columns to datetime
    date_columns = ['in_service_date', 'warranty_end_date', 'service_contract_end_date']
    for col in date_columns:
        if col in list(df.columns):
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Get today's date
    today = pd.Timestamp(datetime.now().date())
    
    # Remove rows with in service date before 1970-01-01 or after today
    if 'in_service_date' in list(df.columns):
        len_before = len(df)
        df = df[
            ((df['in_service_date'] >= '1970-01-01') & (df['in_service_date'] <= today)) 
            | (df['in_service_date'].isna())
        ]
        len_after = len(df)
        if len_before - len_after > 0:
            print(f"\t{str(len_after)} rows remaining. Removed {str(len_before - len_after)} rows with in service date before 1970-01-01 or after today")

    # Remove rows with warranty end date before 1970-01-01
    if 'warranty_end_date' in list(df.columns): 
        len_before = len(df)
        df = df[(df['warranty_end_date'].isna()) | (df['warranty_end_date'] >= '1970-01-01')]
        len_after = len(df)
        if len_before - len_after > 0:
            print(f"\t{str(len_after)} rows remaining. Removed {str(len_before - len_after)} rows with warranty end date before 1970-01-01")
    
    # Remove rows with negative acquisition cost
    if 'acquisition_cost' in list(df.columns):
        len_before = len(df)
        df = df[(df['acquisition_cost'].isna()) | (df['acquisition_cost'] >= 0)]
        len_after = len(df)
        if len_before - len_after > 0:
            print(f"\t{str(len_after)} rows remaining. Removed {str(len_before - len_after)} rows with negative acquisition cost")
        df['acquisition_cost'] = df['acquisition_cost'].round(2)

    if 'service_contract_end_date' in list(df.columns): 
        len_before = len(df)
        df = df[(df['service_contract_end_date'].isna()) | (df['service_contract_end_date'] >= '1970-01-01')] 
        len_after = len(df)
        if len_before - len_after > 0:
            print(f"\t{str(len_after)} rows remaining. Removed {str(len_before - len_after)} rows with service contract end date before 1970-01-01")

    # Remove negative service contract annual cost
    if 'service_contract_annual_cost' in list(df.columns):
        len_before = len(df)
        df = df[(df['service_contract_annual_cost'].isna()) | (df['service_contract_annual_cost'] >= 0)]
        len_after = len(df)
        if len_before - len_after > 0:
            print(f"\t{str(len_after)} rows remaining. Removed {str(len_before - len_after)} rows with negative service contract annual cost")
        #Round to 2 decimal places
        df['service_contract_annual_cost'] = df['service_contract_annual_cost'].round(2)

    # Return
    return df
    