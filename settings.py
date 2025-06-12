_cols_to_keep_dict = {
    'assets': [
        # The following columns are in uptime
        "company_name",
        "company_id",
        "asset_tag",
        "asset_sys_id",
        "asset_name",
        "serial_number",
        "acquisition_method",
        "in_service_date",
        "modality",
        "department",
        "last_known_location",
        "room_name",
        "floor_name",
        "building_name",
        "campus_name",
        "asset_criticality",
        "make",
        "model_name",
        "warranty_end_date",
        "assigned_vendor",
        "assigned_support_group",
        "assigned_technician",
        "risk_score",
        "risk_score_level",
        "model_number",
        "downtime_status",
        "service_strategy",
        "lifecycle_status",
        "acquisition_cost",
        "description",
        "sys_updated_on",
        "third_party_id",
        "last_pm_date",
        "next_pm_date",
        "in_scope",
        "ID_NO",
        "timezone",
        # The following columns are not currently in uptime
        'comments', 
        'make_source', 
        'model_source', 
        'modality_source' 
    ], 
    'work_orders': [
        # The following columns are in uptime
        "company_name",
        "company_id",
        "work_order_id",
        "reported_date",
        "completed_date",
        "asset_tag",
        "asset_sys_id",
        "type",
        "priority",
        "work_order_status",
        "work_order_substate",
        "technician",
        "vendor_assigned",
        "external_technician",
        "external_technician_name",
        "under_contract",
        "problem",
        "problem_cause",
        "resolution",
        "resolution_detail",
        "work_scheduled_date",
        "planned_end",
        "hours_spent",
        "quantity",
        "downtime_impact",
        "part_name",
        "order_summary",
        "sys_updated_on",
        "total_hours_in_ticket",
        "scheduled_duration",
        "work_order_active",
        "INSERT_DATETIME",
        "work_notes",
        "due_date",
        "ID_NO",
        "REPORTED_BY",
        "reported_by_phone"
        # The following columns are not currently in uptime
        'comments',
        'resolution_detail_source',
        'order_summary_source'
    ],
    'labor': [    
        # The following columns are in uptime
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
        # The following columns are not currently in uptime
        'comments'
    ],
    'parts': [    
        # The following columns are in uptime
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
        'quantity',
        # The following columns are not currently in uptime
        'comments' 
    ]
}

_make_model_modality_filepath = './assets\\mapping_tables\\make_model_modality.csv'
_mel_filepath = './assets\\mapping_tables\\mel.csv'

def get_mapping_filepath(table_str, field_name):
    return f'./{table_str}\\mapping_tables\\{field_name}.csv'

def get_output_filepath(table_str, layer_str):
    return f'./{table_str}\\outputs\\{layer_str}_{table_str}.csv'

def get_raw_filepath(company_name, table_str):
    return f'./{table_str}\\customer_data\\{company_name.lower()}.csv'