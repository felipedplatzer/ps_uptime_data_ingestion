#Constants 
_column_mapping_dict = {
    "Work_Order_Number": "work_order_id",
    "Asset_Number": "asset_sys_id",
    "Type Description": None, # it's work order type, not labor type
    "Problem Description": None, # goes in work orders 
    "Action Description": None, # goes in work orders
    "First Assigned Last Name": None, # goes in work orders
    "Total Hours": "duration",
    "Total Time Cost": "cost", 
    "Total Material Cost": None, # field mapped in parts
    "Total WO Cost": None, # field is sum of cost in labor + parts
    "Date Created": None, # goes in work orders
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
    "Completion Comments": "summary"
}

_duration_denominator = 1 #duration is stored in seconds for christiana -> need to divide by 3600

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

    #Convert duration fields to hours (Christiana and Wakemed record duration in seconds. Piedmont, Marshfield, and Methodist record duration in hours)



# Main
def marshfield(df):
    # Rename cols
    df = rename_cols(df)
    # Fill na's in asset sys id
    df['work_order_id'] = df['work_order_id'].fillna('').astype(str)
    # Add primary key
    df['labor_sys_id'] = df['work_order_id'] # Marshfield has 1 labor record per work order, so WO id can be used as labor item id
    # Remove empty labor id's 
    df = df[(df['labor_sys_id'].str.strip() != '')]
    # Convert duration to hours 
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
    df['duration'] = df['duration'] / _duration_denominator


    return df

    # IN OTHER CUSTOMERS, PARSE SUMMARY FIELD