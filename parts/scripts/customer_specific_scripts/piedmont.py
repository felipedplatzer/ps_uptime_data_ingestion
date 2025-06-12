#Constants 
_column_mapping_dict = {
    "WO_NUMBER": "work_order_id",
    "SEQUENCE": None,
    "PART_NUM": "part_number",
    "PART_NAME": "part_description",
    "PART_QTY": "quantity",
    "PART_COST": "unit_cost",
    "WORK_TYPE": None,
    "FACILITY": None,
    "BILLABLE": None,
    "LINE_ITEM_ID": None,
    "COST_AGAINST_CONTRACT": None,
    "PARTSSOURCE_LOG_ID": None,
    "SUPPLIER": "part_vendor",
    "DONE_DATETIME": None

}


# Import libraries
import pandas as pd


#Functions
def rename_cols(df):
    current_uptime_cols = {k: v for k, v in _column_mapping_dict.items() if v != None}
    new_cols =  [k for k, v in _column_mapping_dict.items() if v == None]
    df = df.rename(columns=current_uptime_cols)
    df['comments'] = df[new_cols].to_dict(orient='records')
    df = df.drop(new_cols, axis=1)
    return df

    #Convert duration fields to hours (Christiana and Wakemed record duration in seconds. Piedmont, Marshfield, and Methodist record duration in hours)

# Main
def piedmont(df):
    # Remove empty WO_NUMBER or SEQUENCE
    df = df[df['WO_NUMBER'].notna() & df['SEQUENCE'].notna()]
    # Create primary key
    df['parts_sys_id'] = df['WO_NUMBER'].fillna('').astype(str) + '.' + df['SEQUENCE'].fillna('').astype(str)
    # Rename cols
    df = rename_cols(df)
    # Fill na's in asset sys id
    df['work_order_id'] = df['work_order_id'].fillna('').astype(str)
    return df