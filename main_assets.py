from assets.scripts.bronze_to_silver import bronze_to_silver
from assets.scripts.silver_to_gold import silver_to_gold

import all_datasets
import settings
import pandas as pd




if __name__ == "__main__":
    # Get customer name and input file
    company_name = input('Enter the customer name: ')
    #company_name = 'christiana'
    company_name = company_name.upper()
    input_file = settings.get_raw_filepath(company_name, 'assets')
    # Read raw df
    print('Reading raw data...')
    try:
        df = pd.read_csv(input_file, encoding='utf-8')
    except FileNotFoundError:
        print(f'\tRaw file not found for {company_name}')
    else:
        print(f'\t{str(len(df))} raw records found')
        
        # Transform bronze to silver data
        print('Transforming bronze to silver...')
        df = bronze_to_silver(df, company_name)
        df = df[[x for x in list(df.columns) if x in settings._cols_to_keep_dict['assets']]] # Overwrite existing assets of customer (silver layer)
        all_datasets.overwrite(df, company_name, 'silver', 'assets')

        # Transform silver to gold data
        print('Transforming silver to gold...')
        df = silver_to_gold(df)
        df = df[[x for x in list(df.columns) if x in settings._cols_to_keep_dict['assets']]] # Overwrite existing assets of customer (silver layer)
        all_datasets.overwrite(df, company_name, 'gold', 'assets')
