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
    

    # Remove rows with asset id not in asset table and work order id not in work order table
    df = remove_ghost_items(df)

    # Remove negative quantity, cost, or unit_cost
    for x in ['cost','unit_cost','quantity']:
        if x in list(df.columns):
            df = df[(df[x].isna()) | (df[x] >= 0)]


    # Return
    return df
    
