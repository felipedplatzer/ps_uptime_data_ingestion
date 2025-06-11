from raw_to_bronze import raw_to_bronze
from bronze_to_silver import bronze_to_silver
from silver_to_gold import silver_to_gold

import settings
import pandas as pd




def remove_irrelevant_columns(df):
    cols_to_keep = [x for x in list(df.columns) if x in settings._column_list]
    df = df[cols_to_keep]
    return df


def overwrite(df_customer, company_name, layer_str):
    filepath = settings._filepath_dict[layer_str]
    try:
        df_existing = pd.read_csv(filepath)        
        # Remove existing SUMMA rows
        df_existing = df_existing[df_existing['company_name'] != company_name]
        # Append new SUMMA data
        df_combined = pd.concat([df_existing, df_customer], ignore_index=True)
    except FileNotFoundError:
        # If file doesn't exist, just use the new data
        df_combined = df_customer
    # Save the combined dataframe
    df_combined.to_csv(filepath, index=False)


if __name__ == "__main__":
    # Get customer name and input file
    #company_name = input('Enter the customer name: ')
    company_name = 'christiana'
    company_name = company_name.upper()
    input_file = settings.get_raw_filepath(company_name)
    # Read raw df
    try:
        raw_df = pd.read_csv(input_file, encoding='utf-8')
    except FileNotFoundError:
        print(f'Raw file not found for {company_name}')
    else:
        print(f'# of raw records: {str(len(raw_df))}')

        # Transform raw into bronze data
        bronze_df = raw_to_bronze(raw_df, company_name)
        bronze_df = remove_irrelevant_columns(bronze_df)
        overwrite(bronze_df, company_name, 'bronze') # Overwrite existing records of customer
        print(f'# of bronze records: {str(len(bronze_df))}')
        
        # Transform bronze to silver data
        silver_df = bronze_to_silver(bronze_df)
        silver_df = remove_irrelevant_columns(silver_df) # Overwrite existing records of customer (silver layer)
        overwrite(silver_df, company_name, 'silver')
        print(f'# of silver records: {str(len(silver_df))}')

        # Transform silver to gold data
        gold_df = silver_to_gold(silver_df)
        gold_df = remove_irrelevant_columns(gold_df)
        overwrite(gold_df, company_name, 'gold') # Overwrite existing records of customer (bronze layer)
        print(f'# of gold records: {str(len(gold_df))}')
