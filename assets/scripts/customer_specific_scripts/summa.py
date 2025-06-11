#Constants 
_column_mapping_dict = {
    "Contract": None, #Ask Sanaa / Derek
    "Asset Tag": "asset_tag",
    "Asset Type": "modality",
    "Asset Model Name": "model_name", # could be model_number as well -> needs standardization
    "Serial Number": "serial_number",
    "Asset Manufacturer": "make",
    "Owning Department": "department",
    "Device Region": None,
    "Device Campus": "campus_name",
    "Device Building": "building_name",
    "Device Floor": "floor_name",
    "Installation Date": "in_service_date",
    "Risk Score Level": "risk_score_level",
}
_primary_key = 'serial_number' #column that serves as primary key (choose a column wiht few duplicates)


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
def summa(df):
    df = rename_cols(df)
    df['asset_sys_id'] = df[_primary_key].apply(lambda x: create_id(x))
    return df

# Missing standardization of risk score level!!