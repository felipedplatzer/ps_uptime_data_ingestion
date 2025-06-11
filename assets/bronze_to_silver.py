import pandas as pd
import filepaths



def standardize_make_model_modality(silver_df):
    map_df = pd.read_csv(filepaths._make_model_modality_filepath)
    map_df['MEL_ID'] = pd.to_numeric(map_df['MEL_ID'], errors='coerce').astype('Int64')
    silver_df = silver_df.rename(columns={'make': 'make_source', 'modality': 'modality_source', 'model_name': 'model_name_source'})
    silver_df = pd.merge(silver_df, map_df, on = ['make_source', 'model_name_source', 'modality_source'], how = 'left') 
    mel_df = pd.read_csv(filepaths._mel_filepath)[['New ModelId','New Manufacturer','New Model', 'New Lvl 2 Category']]
    mel_df = mel_df.drop_duplicates(subset='New ModelId') # TBD how to handle duplicates
    silver_df = pd.merge(silver_df, mel_df, left_on ='MEL_ID', right_on = 'New ModelId', how = 'left')
    #silver_df = silver_df.drop(columns=['make_source','modality_source','model_name_source']) # remove 'old' modality, make, and model , after it's been merged
    silver_df = silver_df.rename(columns={'New Manufacturer': 'make', 'New Lvl 2 Category': 'modality', 'New Model': 'model_name', 'company_name_x': 'company_name'})
    return silver_df


def standardize_lifecycle_status(silver_df):
    if 'lifecycle_status' in list(silver_df.columns):
        map_df = pd.read_csv(filepaths._lifecycle_filepath)
        silver_df = silver_df.rename(columns = {'lifecycle_status': 'lifecycle_status_source'})
        silver_df = pd.merge(silver_df, map_df, on = ['company_name','lifecycle_status_source'])
    return silver_df


def standardize_acquisition_method(silver_df):
    if 'acquisition_method' in list(silver_df.columns):
        map_df = pd.read_csv(filepaths._acquisition_method_filepath)
        silver_df = silver_df.rename(columns = {'acquisition_method': 'acquisition_method_source'})
        silver_df = pd.merge(silver_df, map_df, on = ['company_name','acquisition_method_source'])
    return silver_df


def standardize_asset_criticality(silver_df):
    if 'asset_criticality' in list(silver_df.columns):
        map_df = pd.read_csv(filepaths._asset_criticality_filepath)
        silver_df = silver_df.rename(columns = {'asset_criticality': 'asset_criticality_source'})
        silver_df = pd.merge(silver_df, map_df, on = ['company_name','asset_criticality_source'])
    return silver_df


def bronze_to_silver(df):
    # Remove all duplicate rows (i.e. rows with all attributes being equal)
    if 'comments' in list(df.columns):
        df['comments_str'] = df['comments'].astype(str) #workaround because it's not possible to use a dict in drop duplicates
        df = df.drop_duplicates(subset = [x for x in list(df.columns) if x != 'comments'])
        df = df.drop('comments_str', axis=1)

    # Remove all rows without asset ID
    df = df[df['asset_sys_id'] != None]

    # Remove rows with duplicate asset ID
    df = df.drop_duplicates(subset=['asset_sys_id'])

    # Standardize make, model, modality
    df = standardize_make_model_modality(df)

    # Remove assets without modality, manufacturer or model
    df = df[(df['modality_source'] != None) & (df['make_source'] != None) & (df['model_name_source'] != None)]

    # Standardize operational_status against master list
    df = standardize_lifecycle_status(df)

    # Standardize acquisition_method against master list
    df = standardize_acquisition_method(df) # Note: Need to change later!

    # Standardize asset_criticality against master list
    df = standardize_asset_criticality(df)

    #Return
    return df

