#Constants 
_column_mapping_dict = {
    "Work_Order_Number": "work_order_id",
    "Asset_Number": "asset_sys_id",
    "Type Description": None, # it's work order type, not labor type
    "Problem Description": None, # goes in work orders 
    "Action Description": None, # goes in work orders
    "First Assigned Last Name": None, # goes in work orders
    "Total Hours": None, # goes in labor
    "Total Time Cost": None, # goes in labor
    "Total Material Cost": "cost", # field mapped in parts
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
    "Quantity Issued": "quantity",
    "Average Cost": "unit_cost",
    "Completion Comments": None # goes in labor 
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

    #Convert duration fields to hours (Christiana and Wakemed record duration in seconds. Piedmont, Marshfield, and Methodist record duration in hours)

# Main
def marshfield(df):
    # Rename cols
    df = rename_cols(df)
    # Add primary key
    df['work_order_id'] = df['work_order_id'].fillna('').astype(str)
    df['parts_sys_id'] = df['work_order_id'] # Marshfield has 1 parts record per work order, so WO id can be used as parts item id
    # Remove empty work order id's 
    df = df[(df['parts_sys_id'].str.strip() != '')]
    # Fill na's in asset sys id
    df['work_order_id'] = df['work_order_id'].fillna('')
    return df