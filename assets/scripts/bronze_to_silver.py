import pandas as pd
import settings
import all_datasets

def standardize_make_model_modality(silver_df):
    map_df = pd.read_csv(settings._make_model_modality_filepath)
    map_df['MEL_ID'] = pd.to_numeric(map_df['MEL_ID'], errors='coerce').astype('Int64')
    silver_df = silver_df.rename(columns={'make': 'make_source', 'modality': 'modality_source', 'model_name': 'model_name_source'})
    silver_df = pd.merge(silver_df, map_df, on = ['make_source', 'model_name_source', 'modality_source'], how = 'left') 
    mel_df = pd.read_csv(settings._mel_filepath)[['New ModelId','New Manufacturer','New Model', 'New Lvl 2 Category']]
    mel_df = mel_df.drop_duplicates(subset='New ModelId') # TBD how to handle duplicates
    silver_df = pd.merge(silver_df, mel_df, left_on ='MEL_ID', right_on = 'New ModelId', how = 'left')
    #silver_df = silver_df.drop(columns=['make_source','modality_source','model_name_source']) # remove 'old' modality, make, and model , after it's been merged
    silver_df = silver_df.rename(columns={'New Manufacturer': 'make', 'New Lvl 2 Category': 'modality', 'New Model': 'model_name', 'company_name_x': 'company_name'})
    return silver_df




# Main
def bronze_to_silver(df, company_name):
    # Customer-specific processing
    if company_name == 'SUMMA':
        from assets.scripts.customer_specific_scripts.summa import summa
        df = summa(df)
    elif company_name == 'CHRISTIANA':
        from assets.scripts.customer_specific_scripts.christiana import christiana
        df = christiana(df)

    # Remove rows with multiple asset IDs (containing commas)
    df = df[~df['asset_sys_id'].astype(str).str.contains(',')]
    
    # Convert acquisition_cost to numeric, handling NULLs and 0s properly
    if 'acquisition_cost' in df.columns:
        # Replace $ and parentheses, convert to numeric
        df['acquisition_cost'] = df['acquisition_cost'].astype(str).str.replace('$', '').str.replace('(', '-').str.replace(')', '')
        # Convert to numeric, errors='coerce' will set invalid values to NaN
        df['acquisition_cost'] = pd.to_numeric(df['acquisition_cost'], errors='coerce')


    # Add company name
    df['company_name'] = company_name.upper()

    # Remove all duplicate rows (i.e. rows with all attributes being equal)
    df = all_datasets.remove_duplicate_rows(df)

    # Remove all rows without asset ID
    df = df[df['asset_sys_id'] != None]

    # Remove rows with duplicate asset ID
    df = df.drop_duplicates(subset=['asset_sys_id'])

    # Standardize make, model, modality
    df = standardize_make_model_modality(df)

    # Remove assets without modality, manufacturer or model
    df = df[(df['modality_source'] != None) & (df['make_source'] != None) & (df['model_name_source'] != None)]

    # Standardize operational_status, acquisition_method, asset_criticality against master list
    for x in ['lifecycle_status', 'acquisition_method', 'asset_criticality']:
        df = all_datasets.standardize_field(df, x, 'assets')

    #Return
    return df

