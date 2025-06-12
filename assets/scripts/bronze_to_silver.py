import pandas as pd
import settings
import all_datasets

def standardize_make_model_modality(df):
    # Read mapping files
    map_df = pd.read_csv(settings._make_model_modality_filepath)
    map_df['MEL_ID'] = pd.to_numeric(map_df['MEL_ID'], errors='coerce').astype('Int64')
    # Rename columns
    if 'make' in list(df.columns): 
        df = df.rename(columns={'make': 'make_source'})
    if 'model_name' in list(df.columns):
        df = df.rename(columns={'model_name': 'model_name_source'})
    if 'modality' in list(df.columns):
        df = df.rename(columns={'modality': 'modality_source'})
    # Map make / model / modality to MEL ID
    if ['make', 'model_name', 'modality'] in list(df.columns):
        # Map make, model, modality to MEL ID
        df = pd.merge(df, map_df, on = ['make_source', 'model_name_source', 'modality_source'], how = 'left') 
        n_mapped_rows = len(df[df['MEL_ID'].notna()])
        print(f'\t{str(n_mapped_rows)} assets mapped to MEL')
        # Map MEL_ID to MEL's make, model, modality
        mel_df = pd.read_csv(settings._mel_filepath)[['New ModelId','New Manufacturer','New Model', 'New Lvl 2 Category']]
        mel_df = mel_df.drop_duplicates(subset='New ModelId') # TBD how to handle duplicates
        df = pd.merge(df, mel_df, left_on ='MEL_ID', right_on = 'New ModelId', how = 'left')
        #df = df.drop(columns=['make_source','modality_source','model_name_source']) # remove 'old' modality, make, and model , after it's been merged
        df = df.rename(columns={'New Manufacturer': 'make', 'New Lvl 2 Category': 'modality', 'New Model': 'model_name', 'company_name_x': 'company_name'})
    return df




# Main
def bronze_to_silver(df, company_name):
    # Customer-specific processing
    if company_name == 'SUMMA':
        from assets.scripts.customer_specific_scripts.summa import summa
        df = summa(df)
    elif company_name == 'CHRISTIANA':
        from assets.scripts.customer_specific_scripts.christiana import christiana
        df = christiana(df)
    elif company_name == 'WAKEMED':
        from assets.scripts.customer_specific_scripts.wakemed import wakemed
        df = wakemed(df)
    elif company_name == 'MARSHFIELD':
        from assets.scripts.customer_specific_scripts.marshfield import marshfield
        df = marshfield(df)
    elif company_name == 'METHODIST':
        from assets.scripts.customer_specific_scripts.methodist import methodist
        df = methodist(df)
    elif company_name == 'PIEDMONT':
        from assets.scripts.customer_specific_scripts.piedmont import piedmont
        df = piedmont(df)
    #Convert fields to string
    for col in ['asset_sys_id', 'modality','make','model_name','model_number']:
        if col in list(df.columns):
            df[col] = df[col].fillna('').astype(str)
    # Remove rows with multiple asset IDs (containing commas)
    len_before = len(df)
    df = df[~df['asset_sys_id'].str.contains(',')]
    len_after = len(df)
    if len_before - len_after > 0:
        print(f"\t{str(len_after)} rows remaining. Removed {str(len_before - len_after)} rows with multiple asset IDs")
    
    # Convert acquisition_cost to numeric, handling NULLs and 0s properly
    if 'acquisition_cost' in df.columns:
        # Replace $ and parentheses, convert to numeric
        df['acquisition_cost'] = df['acquisition_cost'].astype(str).str.replace('$', '').str.replace('(', '-').str.replace(')', '')
        # Convert to numeric, errors='coerce' will set invalid values to NaN
        df['acquisition_cost'] = pd.to_numeric(df['acquisition_cost'], errors='coerce')


    # Add company name
    df['company_name'] = company_name.upper()

    # Remove all duplicate rows (i.e. rows with all attributes being equal)
    len_before = len(df)
    df = all_datasets.remove_duplicate_rows(df)
    len_after = len(df)
    if len_before - len_after > 0:
        print(f"\t{str(len_after)} rows remaining. Removed {str(len_before - len_after)} duplicate rows")

    # Remove all rows without asset ID
    len_before = len(df)
    df = df[(df['asset_sys_id'].str.strip() != '')]
    len_after = len(df)
    if len_before - len_after > 0:
        print(f"\t{str(len_after)} rows remaining. Removed {str(len_before - len_after)} rows without asset ID")

    # Remove rows with duplicate asset ID
    len_before = len(df)
    df = df.drop_duplicates(subset=['asset_sys_id'])
    len_after = len(df)
    if len_before - len_after > 0:
        print(f"\t{str(len_after)} rows remaining. Removed {str(len_before - len_after)} rows with duplicate asset ID")

    # Standardize make, model, modality
    df = standardize_make_model_modality(df)

        # Standardize operational_status, acquisition_method, asset_criticality against master list
    for x in ['lifecycle_status', 'acquisition_method', 'asset_criticality']:
        df = all_datasets.standardize_field(df, x, 'assets')

    #Return
    return df

