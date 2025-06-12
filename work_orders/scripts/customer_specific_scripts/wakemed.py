#Constants 
_column_mapping_dict = {
    "number": "work_order_id",
    "asset": "asset_sys_id",
    "work_order_type": "type",
    "state": "work_order_status",
    "reported_by": "REPORTED_BY",
    "sys_created_on": "reported_date",
    "substate": "work_order_substate",
    "u_work_campus": None,
    "u_work_building": None,
    "resolved": "completed_date",
    "resolution_detail": "resolution_detail",
    "resolution_code": "resolution",
    "problem_cause": "problem_cause",
    "short_description": "problem",
    "description": None,
    "downtime_start": None,
    "downtime_end": None,
    "u_downtime_impact": None,
    "contract": None,
    "nuvolo_contract": None,
    "closed_at": None,
    "closed_by": None,
    "assigned_to": "technician",
    "asset_type": None

}



# Import libraries
import pandas as pd





#Functions
def rename_cols(df):
    current_uptime_cols = {k: v for k, v in _column_mapping_dict.items() if v != None}
    new_cols =  [k for k, v in _column_mapping_dict.items() if v == None]
    df = df.rename(columns=current_uptime_cols)
    df['comments'] = df[new_cols].to_dict(orient='records')
    df = df.drop(new_cols, axis=1)
    return df


def parse_resolution_detail(df):
    # Create copy 
    df['resolution_detail_source'] = df['resolution_detail']
    # Replace commas by semicolon (commas will be used to distinguish entries from different technicians)

    df['resolution_detail'] = df['resolution_detail'].str.replace(',', ';', regex=False)
    # Remove patterns from resolution_detail        
    df['resolution_detail'] = df['resolution_detail'].str.replace(r'[A-Z]{2}-(.*?)-\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', r', \1,', regex=True)
    # Remove commas at the beginning and end of the string
    df['resolution_detail'] = df['resolution_detail'].str.strip(',')
    # Replace linebreaks with space
    df['resolution_detail'] = df['resolution_detail'].str.replace(r'\n', ' ', regex=True)
    # Replace multiple spaces with single space
    df['resolution_detail'] = df['resolution_detail'].str.replace(r'\s+', ' ', regex=True)
    # Remove whitespace at beginning and end
    df['resolution_detail'] = df['resolution_detail'].str.strip()
    # Replace space + comma + space with comma + space
    df['resolution_detail'] = df['resolution_detail'].str.replace(r' , ', ', ', regex=True)
    # Normalize multiple commas
    df['resolution_detail'] = df['resolution_detail'].str.replace(r',{2,}', ',', regex=True)
    return df


 
# Main
def wakemed(df):

    # Rename cols
    df = rename_cols(df)

    # Remove empty work order id's 
    df['work_order_id'] = df['work_order_id'].fillna('').astype(str)
    df = df[(df['work_order_id'] != '')]
    # Fill na's in asset sys id
    df['asset_sys_id'] = df['asset_sys_id'].fillna('')
    #df['work_order_id'] = df['work_order_id'].astype(str) + '.' + df['asset_sys_id'].astype(str) 
    # Parse resolution detail
    df = parse_resolution_detail(df)
    return df

    # IN OTHER CUSTOMERS : TRANSFORM SCHEDULED DURATION TO COMMON UNIT!!