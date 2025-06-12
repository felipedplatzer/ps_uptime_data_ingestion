#Constants 
_column_mapping_dict = {
    "Work_Order_Number": "work_order_id",
    "Asset_Number": "asset_sys_id",
    "Type Description": "type",
    "Problem Description": "problem_cause",
    "Action Description": "resolution_code",
    "First Assigned Last Name": "technician",
    "Total Hours": "hours_spent",
    "Total Time Cost": None, # field mapped in labor
    "Total Material Cost": None, # field mapped in parts
    "Total WO Cost": None, # field is sum of cost in labor + parts
    "Date Created": "reported_date",
    "Year": None,
    "Site Name": None,
    "Category Description": None,
    "Sub-Category Description": None,
    "Manufacturer Name": None,
    "First Asset Model Number": None,
    "First Asset Serial Number": None,
    "Item Description": None,
    "Quantity Issued": None,
    "Average Cost": None,
    "Completion Comments": "work_notes"
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



def parse_work_notes(df):
    # Remove the work notes prefix (yyyy-mm-dd hh:mm:ss - technician name (Work Notes))
    df['work_notes'] = df['work_notes'].str.replace(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} - [A-Za-z]+ [A-Za-z]+ \(Work Notes\)', '', regex=True)
    df['work_notes'] = df['work_notes'].str.strip()
    return df    

# Main
def marshfield(df):
    # Rename cols
    df = rename_cols(df)
    # Parse work notes
    df = parse_work_notes(df)
    # Remove empty work order id's 
    df['work_order_id'] = df['work_order_id'].fillna('').astype(str)
    df = df[(df['work_order_id'] != '')]
    # Fill na's in asset sys id
    df['asset_sys_id'] = df['asset_sys_id'].fillna('')
    #df['work_order_id'] = df['work_order_id'].astype(str) + '.' + df['asset_sys_id'].astype(str) 
    # Parse resolution detail
    df = parse_work_notes(df)
    return df

    # IN OTHER CUSTOMERS : TRANSFORM SCHEDULED DURATION TO COMMON UNIT!!