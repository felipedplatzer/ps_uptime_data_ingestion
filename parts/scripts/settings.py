_filepath_dict = {
    'bronze': './outputs\\bronze_parts.csv',
    'silver': './outputs\\silver_parts.csv',
    'gold': './outputs\\gold_parts.csv'
}

_work_order_filepath = './..\\work_orders\\outputs\\gold_work_orders.csv'
_asset_filepath = './..\\assets\\outputs\\gold_assets.csv'

_column_list = [
    'company_name',
    'parts_sys_id',
    'work_order_id',
    'cost',
    'unit_cost',
    'inventoried_part',
    'part_number'
    'part_manufacturer',
    'part_description',
    'part_vendor',
    'quantity'
    'comments' # added comments field as catch-all for all unmapped fields
]


def get_raw_filepath(company_name):
    return f'./customer_data\\{company_name.lower()}.csv'

def get_mapping_filepath(field_name):
    return f'./mapping_tables\\{field_name}.csv'