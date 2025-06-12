#Constants 
_column_mapping_dict = {
    "Site Name": "device_campus",
    "Building Name": "device_building",
    "Location Description": None,
    "Shop Description": None,
    "Asset Number": "asset_sys_id",
    "Account Description": None,
    "Account Code": None,
    "Category Description": "modality",
    "Sub-Category Description": None,
    "Manufacturer Name": "make",
    "Model Number": "model_number",
    "Manufacturer Serial Number": "serial_number",
    "Asset Description": "asset_description",
    "Original Cost": "acquisition_cost",
    "Date Accepted": None,
    "Total Material Cost To Date": None,
    "Total Cost To Date": None,
    "Support Status Description": None,
    "Contract Number": None,
    "Contract Description": None,
    "Budget": None,
    "Effective Date": "in_service_date",
    "Termination Date": None

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


# Main
def marshfield(df):
    df = rename_cols(df)
    return df

