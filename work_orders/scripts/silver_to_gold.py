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
    len_before = len(df)
    if 'work_order_status' in list(df.columns):
        df = df[df['work_order_status'] == 'Closed Complete']
        len_after = len(df)
        if len_before - len_after > 0:
            print(f"\t{str(len_after)} rows remaining. Removed {str(len_before - len_after)} rows with work order status <> closed complete")

    # Remove rows with asset id not in asset table
    len_before = len(df)
    df = remove_ghost_assets(df)
    len_after = len(df)
    if len_before - len_after > 0:
        print(f"\t{str(len_after)} rows remaining. Removed {str(len_before - len_after)} rows with asset id not in asset table")

    # Get today's date
    today = pd.Timestamp(datetime.now().date())
    
    # Filter out invalid dates  
    len_before = len(df)
    if 'reported_date' in list(df.columns):
        df = df[
            ((df['reported_date'] >= '1970-01-01') & (df['reported_date'] <= today))
            | (df['reported_date'].isna())
        ]
        len_after = len(df)
        if len_before - len_after > 0:
            print(f"\t{str(len_after)} rows remaining. Removed {str(len_before - len_after)} rows with reported date before 1970 or after today")

    len_before = len(df)
    if 'completed_date' in list(df.columns):
        df = df[
            ((df['completed_date'] >= '1970-01-01') & (df['completed_date'] <= today))
            | (df['reported_date'].isna())
        ]
        len_after = len(df)
        if len_before - len_after > 0:
            print(f"\t{str(len_after)} rows remaining. Removed {str(len_before - len_after)} rows with completed date before 1970 or after today")

    # Remove negative scheduled duration
    len_before = len(df)
    if 'scheduled_duration' in list(df.columns):
        df = df[(df['scheduled_duration'].isna()) | (df['scheduled_duration'] >= 0)]
        len_after = len(df)
        if len_before - len_after > 0:
            print(f"\t{str(len_after)} rows remaining. Removed {str(len_before - len_after)} rows with negative scheduled duration")

    # Remove rows with completed date before reported date
    len_before = len(df)
    if 'completed_date' in list(df.columns) and 'reported_date' in list(df.columns):
        df = df[df['completed_date'] >= df['reported_date']]
        len_after = len(df)
        if len_before - len_after > 0:
            print(f"\t{str(len_after)} rows remaining. Removed {str(len_before - len_after)} rows with completed date before reported date")
            
    # Return
    return df
    
