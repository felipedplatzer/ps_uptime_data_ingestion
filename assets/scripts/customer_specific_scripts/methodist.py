#Constants 
_column_mapping_dict = {
    "ECN": "asset_sys_id",
    "Asset Number": "asset_tag",
    "Manufacturer": "make",
    "Model Number": "model_number",
    "Model Name": "model_name",
    "Equipment Type": "modality",
    "Description": "description",
    "Serial": "serial_number",
    "Nameplate Manufacturer": None,
    "Risk Classification": "risk_score_level",
    "location": None,
    "Facility": "campus_name",
    "Building": "building_name",
    "Free Text Location": None,
    "Location Date": None,
    "Critical Equipment/System": "asset_criticality",
    "Equipment Status": "lifecycle_status",
    "Status Date": None,
    "Equipment Condition": None,
    "Condition Date": None,
    "Ownership": None,
    "Site ID": None,
    "Equipment Service Department": "department",
    "In Service Date": "in_service_date"

}


# Import libraries
import pandas as pd

def create_id(primary_key_value):
    #hash function
    return primary_key_value

#Functions
def rename_cols(df):
    current_uptime_cols = {k: v for k, v in _column_mapping_dict.items() if v != None}
    new_cols =  [k for k, v in _column_mapping_dict.items() if v == None]
    df = df.rename(columns=current_uptime_cols)
    df['comments'] = df[new_cols].to_dict(orient='records')
    df = df.drop(new_cols, axis=1)
    return df


# Main
def methodist(df):
    df = rename_cols(df)
    return df

