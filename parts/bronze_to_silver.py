import pandas as pd
import settings


def standardize_field(field_name, silver_df):
    if field_name in list(silver_df.columns):
        filepath = settings.get_mapping_filepath(field_name)
        map_df = pd.read_csv(filepath)
        silver_df = silver_df.rename(columns = {field_name: field_name + '_source'})
        silver_df = pd.merge(silver_df, map_df, on = ['company_name', field_name + '_source'], how = 'inner')
    return silver_df



def bronze_to_silver(df):
    # Remove all duplicate rows (i.e. rows with all attributes being equal)
    if 'comments' in list(df.columns):
        df['comments_str'] = df['comments'].astype(str) #workaround because it's not possible to use a dict in drop duplicates
        df = df.drop_duplicates(subset = [x for x in list(df.columns) if x != 'comments'])
        df = df.drop('comments_str', axis=1)

    # Remove rows with duplicate work order id (this work order id combines the original work order id and the asset id, so that work order id's that apply to multiple assets are valid)
    df = df.drop_duplicates(subset=['parts_sys_id'])

    # Remove 

    # Standardize fields
    std_fields = ['inventoried_part']
    for f in std_fields:
        df = standardize_field(f, df)


    #Return
    return df
