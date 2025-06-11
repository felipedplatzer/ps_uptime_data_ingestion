#Constants 
_column_mapping_dict = {
    "number": "work_order_id",	
    "state": "work_order_status",
    "short_description": "order_summary",
    "sys_created_on": "reported_date",
    "sys_updated_on": "sys_updated_on",	
    "work_order_type": "type",	
    "work_notes": "work_notes",
    "u_substate": "work_order_substate",	
    "resolved": None,	
    "resolution_detail"	: "resolution_detail",
    "resolution_code": "resolution",
    "reported_by": "REPORTED_BY",
    "problem_cause": "problem_cause",
    "description": None,	
    "downtime_start": None,	
    "downtime_end": None,	
    "u_downtime_impact": "downtime_impact",	
    "closed_at": "completed_date", # closed is not the same as completed. closed should only be the same as complet4ed for wo's with stauts = completed 
    "assigned_to": "technician",	
    "asset": "asset_sys_id",	
    "comments": None 
}

_primary_key = 'number' #column that serves as primary key (choose a column wiht few duplicates)


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


# Main
def christiana(df):
    # Rename cols
    df = rename_cols(df)
    # Remove empty work order id's 
    df = df[(df['work_order_id'] != None) & (df['work_order_id'].str.strip() != '')]
    # Fill na's in asset sys id
    df['asset_sys_id'] = df['asset_sys_id'].fillna('')
    #df['work_order_id'] = df['work_order_id'].astype(str) + '.' + df['asset_sys_id'].astype(str) 
    return df

# MISSING : TRANSFORM SCHEDULED DURATION TO COMMON UNIT!!