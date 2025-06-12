#Constants 
_column_mapping_dict = {
    "name": "asset_sys_id",
    "serial_number": "serial_number",
    "install_status": "lifecycle_status",
    "asset_type": "modality",
    "asset_manufacturer": "make",
    "model_name": "model_name",
    "sys_created_on": None,
    "asset_location": None,
    "asset_location.floor.building": None,
    "u_device_building": "building_name",
    "u_device_campus": "campus_name",
    "u_device_floor": "floor_name",
    "department.id": None,
    "department": "department",
    "sys_updated_on": "sys_updated_on",
    "comments": None,
    "u_additional_location": None,
    "short_description": "description",
    "operational_status": "downtime_status",
    "manufacture_date": None,
    "install_date": "in_service_date",
    "critical": "asset_criticality",
    "acquisition_method": "acquisition_method",
    "acquisition_cost": "acquisition_cost",
    "u_contract_end": None,
    "warranty_expiration": "warranty_end_date",
    "service_contract_cost": None


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
def wakemed(df):
    df = rename_cols(df)
    return df

