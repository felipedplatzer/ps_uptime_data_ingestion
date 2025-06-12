
import pandas as pd
import settings


def standardize_field(df, field_name, table_str):
    if field_name in list(df.columns):
        map_filepath = settings.get_mapping_filepath(table_str, field_name)
        map_df = pd.read_csv(map_filepath)
        df = df.rename(columns = {field_name: field_name + '_source'})
        df = pd.merge(df, map_df, on = ['company_name',field_name + '_source'], how='left')
        df[field_name] = df[field_name].fillna('Unmapped')
    return df

def remove_duplicate_rows(df):
    if 'comments' in list(df.columns):
        df['comments_str'] = df['comments'].astype(str) #workaround because it's not possible to use a dict in drop duplicates
        df = df.drop_duplicates(subset = [x for x in list(df.columns) if x != 'comments'])
        df = df.drop('comments_str', axis=1)
    return df

def overwrite(df_customer, company_name, layer_str, table_str):
    filepath = settings.get_output_filepath(table_str, layer_str)
    try:
        df_existing = pd.read_csv(filepath)        
        # Remove existing  rows of this company
        company_records = len(df_existing[df_existing['company_name'] == company_name])
        print(f"\t{str(company_records)} old rows removed, {str(len(df_customer))} new rows added to {layer_str} layer by overwriting")
        df_existing = df_existing[df_existing['company_name'] != company_name]
        # Append new rows of this company
        df_combined = pd.concat([df_existing, df_customer], ignore_index=True)
    except FileNotFoundError:
        # If file doesn't exist, just use the new data
        df_combined = df_customer
        print(f"\t{company_name} {layer_str} layer not found. Creating new file.")
    # Save the combined dataframe
    df_combined.to_csv(filepath, index=False)