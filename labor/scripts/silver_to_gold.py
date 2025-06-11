import pandas as pd
from datetime import datetime
import settings


def remove_ghost_items(df):
    if 'asset_sys_id' in list(df.columns):
        asset_filepath = settings.get_output_filepath('assets', 'gold')
        asset_df = pd.read_csv(asset_filepath)[['company_name','asset_sys_id']]
        df = pd.merge(df, asset_df, on=['company_name','asset_sys_id'], how='inner')
    if 'work_order_id' in list(df.columns):
        work_order_filepath = settings.get_output_filepath('work_orders', 'gold')
        work_order_df = pd.read_csv(work_order_filepath)[['company_name','work_order_id']]
        df = pd.merge(df, work_order_df, on=['company_name','work_order_id'], how='inner')
    return df



def silver_to_gold(df):
    # Remove work orders without work order ID and without asset id
    if 'asset_sys_id' in list(df.columns):
        df = df[(df['asset_sys_id'] != None) & (df['asset_sys_id'].str.strip() != '')]        
    if 'work_order_id' in list(df.columns):
        df = df[(df['work_order_id'] != None) & (df['work_order_id'].str.strip() != '')]
    # Convert date columns to datetime
    date_columns = ['service_date']
    for col in date_columns:
        if col in list(df.columns):
            df[col] = pd.to_datetime(df[col], errors='coerce')
    

    # Remove rows with asset id not in asset table and work order id not in work order table
    df = remove_ghost_items(df)

    # Get today's date
    today = pd.Timestamp(datetime.now().date())
    
    # Filter out invalid dates
    if 'service_date' in list(df.columns):
        df = df[
            ((df['service_date'] >= '1970-01-01') & (df['service_date'] <= today))
            | (df['service_date'].isna())
        ]

    # Remove negative duration
    if 'duration' in list(df.columns):
        df = df[(df['duration'].isna()) | (df['duration'] >= 0)]


    # Remove negative cost
    if 'cost' in list(df.columns):
        df = df[(df['cost'].isna()) | (df['cost'] >= 0)]

    # Return
    return df
    
