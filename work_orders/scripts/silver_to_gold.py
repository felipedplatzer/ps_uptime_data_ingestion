import pandas as pd
from datetime import datetime
import settings


def remove_ghost_assets(df):
    asset_filepath = settings.get_output_filepath('assets', 'gold')
    asset_df = pd.read_csv(asset_filepath)[['company_name','asset_sys_id']]
    df = pd.merge(df, asset_df, on=['company_name','asset_sys_id'], how='inner')
    return df



def silver_to_gold(df):
    # Convert date columns to datetime
    date_columns = ['reported_date', 'completed_date']
    for col in date_columns:
        if col in list(df.columns):
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Remove work order stauts <> closed complete
    df = df[df['work_order_status'] == 'Closed Complete']

    # Remove rows with asset id not in asset table
    df = remove_ghost_assets(df)

    # Get today's date
    today = pd.Timestamp(datetime.now().date())
    
    # Filter out invalid dates
    if 'reported_date' in list(df.columns):
        df = df[
            ((df['reported_date'] >= '1970-01-01') & (df['reported_date'] <= today))
            | (df['reported_date'].isna())
        ]

    if 'completed_date' in list(df.columns):
        df = df[
            ((df['completed_date'] >= '1970-01-01') & (df['completed_date'] <= today))
            | (df['reported_date'].isna())
        ]

    # Remove negative scheduled duration
    if 'scheduled_duration' in list(df.columns):
        df = df[(df['scheduled_duration'].isna()) | (df['scheduled_duration'] >= 0)]


    # Return
    return df
    
