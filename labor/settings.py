_filepath_dict = {
    'bronze': './outputs\\bronze_labor.csv',
    'silver': './outputs\\silver_labor.csv',
    'gold': './outputs\\gold_labor.csv'
}

_work_order_filepath = './..\\work_orders\\outputs\\gold_work_orders.csv'
_asset_filepath = './..\\assets\\outputs\\gold_assets.csv'

_column_list = [
    'company_name',
    'asset_sys_id',
    'labor_sys_id',
    'work_order_id',
    'labor_type',
    'cost',
    'service_date',
    'duration',
    'technician',
    'summary',
    'comments' # added comments field as catch-all for all unmapped fields
]

def get_raw_filepath(company_name):
    return f'./customer_data\\{company_name.lower()}.csv'

def get_mapping_filepath(field_name):
    return f'./mapping_tables\\{field_name}.csv'