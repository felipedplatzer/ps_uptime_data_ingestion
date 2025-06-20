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


def parse_work_notes(df):
    # Remove the work notes prefix (yyyy-mm-dd hh:mm:ss - technician name (Work Notes))
    df['work_notes'] = df['work_notes'].str.replace(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} - [A-Za-z]+ [A-Za-z]+ \(Work Notes\)', '', regex=True)
    df['work_notes'] = df['work_notes'].str.strip()
    return df    

# Main
def christiana(df):
    # Parse work notes
    df = parse_work_notes(df)
    # Rename cols
    df = rename_cols(df)
    # Remove empty work order id's 
    df = df[(df['work_order_id'] != None) & (df['work_order_id'].str.strip() != '')]
    # Fill na's in asset sys id
    df['asset_sys_id'] = df['asset_sys_id'].fillna('')
    #df['work_order_id'] = df['work_order_id'].astype(str) + '.' + df['asset_sys_id'].astype(str) 
    # Parse resolution detail
    df = parse_resolution_detail(df)
    return df

    # IN OTHER CUSTOMERS : TRANSFORM SCHEDULED DURATION TO COMMON UNIT!!