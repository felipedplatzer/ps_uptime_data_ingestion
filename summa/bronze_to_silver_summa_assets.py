import pandas as pd

bronze_df = pd.read_csv('./bronze_summa_assets.csv')
uptime_column_df = pd.read_csv('./..\\global\\uptime_asset_columns.csv', header=None, names=['column'])
uptime_column_list = list(uptime_column_df['column'])


def standardize_make_model_modality(silver_df):
    map_df = pd.read_csv('./summa_mel_map.csv')
    map_df['MEL_ID'] = pd.to_numeric(map_df['MEL_ID'], errors='coerce').astype('Int64')
    silver_df = silver_df.rename(columns={'make': 'make_source', 'modality': 'modality_source', 'model_name': 'model_name_source'})
    silver_df = pd.merge(silver_df, map_df, on = ['make_source', 'model_name_source', 'modality_source'])
    mel_df = pd.read_csv('./..\\global\\Remi Polaris MEL 2025.06.05 (1).csv')[['New ModelId','New Manufacturer','New Model', 'New Lvl 2 Category']]
    silver_df = pd.merge(silver_df, mel_df, left_on ='MEL_ID', right_on = 'New ModelId')
    #silver_df = silver_df.drop(columns=['make_source','modality_source','model_name_source']) # remove 'old' modality, make, and model , after it's been merged
    silver_df = silver_df.rename(columns={'New Manufacturer': 'make', 'New Lvl 2 Category': 'modality', 'New Model': 'model_name'})
    return silver_df


def standardize_lifecycle_status(silver_df):
    map_df = pd.read_csv('./..\\global\\std_lifecycle_status.csv')
    silver_df = silver_df.rename(columns = {'lifecycle_status': 'lifecycle_status_source'})
    silver_df = pd.merge(silver_df, map_df, on = ['company_name','lifecycle_status_source'])
    return silver_df


def standardize_acquisition_method(silver_df):
    map_df = pd.read_csv('./..\\global\\std_acquisition_method.csv')
    silver_df = silver_df.rename(columns = {'acquisition_method': 'acquisition_method_source'})
    silver_df = pd.merge(silver_df, map_df, on = ['company_name','acquisition_method_source'])
    return silver_df


def standardize_asset_criticality(silver_df):
    map_df = pd.read_csv('./..\\global\\std_asset_criticality.csv')
    silver_df = silver_df.rename(columns = {'asset_criticality': 'asset_criticality_source'})
    silver_df = pd.merge(silver_df, map_df, on = ['company_name','asset_criticality_source'])
    return silver_df


if __name__ == "__main__":
    # Remove all duplicate rows (i.e. rows with all attributes being equal)
    silver_df = bronze_df.drop_duplicates()

    # Remove all rows without asset ID
    silver_df = silver_df[silver_df['asset_sys_id'] != None]

    # Remove rows with duplicate asset ID
    silver_df = silver_df.drop_duplicates(subset=['asset_sys_id'])

    # Remove assets without modality, manufacturer or model
    silver_df = silver_df[(silver_df['modality'] != None) & (silver_df['make'] != None) & (silver_df['model_name'] != None)]

    # Standardize operational_status against master list
    silver_df = standardize_lifecycle_status(silver_df)

    # Standardize acquisition_method against master list
    silver_df = standardize_acquisition_method(silver_df)

    # Standardize asset_criticality against master list
    silver_df = standardize_asset_criticality(silver_df)

    #Post-processing
    cols_to_keep = [x for x in list(silver_df.columns) if x in uptime_column_list]
    silver_df = silver_df[cols_to_keep]
    silver_df.to_csv('./silver_summa_assets.csv')


