_filepath_dict = {
    'bronze': './outputs\\bronze_work_orders.csv',
    'silver': './outputs\\silver_work_orders.csv',
    'gold': './outputs\\gold_work_orders.csv'
}



_asset_filepath = './..\\assets\\outputs\\gold_assets.csv'

_uptime_col_filename = './uptime_columns.csv'


def get_raw_filepath(company_name):
    return f'./customer_data\\{company_name.lower()}.csv'

def get_mapping_filepath(field_name):
    return f'./mapping_tables\\{field_name}.csv'