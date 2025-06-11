_filepath_dict = {
    'bronze': './outputs\\bronze_assets.csv',
    'silver': './outputs\\silver_assets.csv',
    'gold': './outputs\\gold_assets.csv'
}

_uptime_col_filename = './uptime_columns.csv'

_make_model_modality_filepath = './mapping_tables\\make_model_modality.csv'
_lifecycle_filepath = './mapping_tables\\lifecycle_status.csv'
_acquisition_method_filepath = './mapping_tables\\acquisition_method.csv'
_asset_criticality_filepath = './mapping_tables\\asset_criticality.csv'
_mel_filepath = './mapping_tables\\mel.csv'


def get_raw_filepath(company_name):
    return f'./customer_data\\{company_name.lower()}.csv'