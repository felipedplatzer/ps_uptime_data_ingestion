#Constants 
_input_file = './customer_data\\csvs\\x_nuvo_eam_clinical_devices.csv'
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
    df['company_name'] = 'SUMMA'
    df = df.drop(new_cols, axis=1)
    return df

def standardize(df):
    return df

# Main
if __name__ == "__main__":
    # NOTE: NEED TO CONVERT FILES TO CSV FIRST
    # NOTE: STANDARDIZATION FILE MUST BE CSV UTF-8
    df = pd.read_csv(_input_file, encoding='utf-8')
    df = rename_cols(df)
    df['asset_sys_id'] = df[_primary_key].apply(lambda x: create_id(x), axis=1)
    
    df.to_csv('./bronze_summa_assets.csv')
    



# bronze

# Missing: remove rows with multiple asset ID's (i.e. asset ID contains comma)
# Convert acquisition cost to numeric (e.g., remove '$' sign, parentheses)
# Convert service_contract_annual_cost to numeric (e.g., remove '$' sign, parentheses)
# Save acquisition_cost = NULL as NULL and acquisition_cost = 0 as 0 (i.e. do not confound NULL's with 0)
# Save service_contract_annual_cost = NULL as NULL and service_contract_annual_cost = 0 as 0 (i.e. do not confound NULL's with 0)