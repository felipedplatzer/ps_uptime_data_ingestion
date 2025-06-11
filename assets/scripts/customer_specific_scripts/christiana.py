#Constants 
_column_mapping_dict = {
    "warranty_expiration": "warranty_end_date", 
    "u_site": "building_name", 
    "service_contract_cost": None, 
    "serial_number": "serial_number", 
    "u_region": "campus_name", 
    "manufacture_date": None, 
    "install_date": "in_service_date", 
    "x_nuvo_sh_contract_end": None, 
    "asset_type": "modality", 
    "name": "model_number", 
    "model_name": "model_name", 
    "asset_manufacturer": "make", 
    "acquisition_cost": "acquisition_cost", 
    "acquisition_method": "acquisition_method"
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
def christiana(df):
    df = rename_cols(df)
    df['asset_sys_id'] = df[_primary_key].apply(lambda x: create_id(x))
    return df

