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
    
    # Filter out invalid dates and costs
    if 'in_service_date' in list(df.columns):
        df = df[
            ((df['in_service_date'] >= '1970-01-01') & (df['in_service_date'] <= today)) 
            | (df['in_service_date'].isna())
        ]

    if 'warranty_end_date' in list(df.columns): 
        df = df[(df['warranty_end_date'].isna()) | (df['warranty_end_date'] >= '1970-01-01')]

    if 'acquisition_cost' in list(df.columns):
        df = df[(df['acquisition_cost'].isna()) | (df['acquisition_cost'] >= 0)]
        df['acquisition_cost'] = df['acquisition_cost'].round(2)

    if 'service_contract_end_date' in list(df.columns): 
        df = df[(df['service_contract_end_date'].isna()) | (df['service_contract_end_date'] >= '1970-01-01')] 

    # Round cost columns to 2 decimal places
    if 'service_contract_annual_cost' in list(df.columns):
        df = df[(df['service_contract_annual_cost'].isna()) | (df['service_contract_annual_cost'] >= 0)]
        df['service_contract_annual_cost'] = df['service_contract_annual_cost'].round(2)
    
    # Return
    return df
    