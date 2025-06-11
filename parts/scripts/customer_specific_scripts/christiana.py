#Constants 
_column_mapping_dict = {
    "number": "parts_sys_id",
    "work_order": "work_order_id",
    "amount": "cost",
    "price_per_unit": "cost_per_unit",
    "sys_created_on": "service_date",
    "parts": "part_number",
    "quantity": "quantity",
    "part_description": None
}

_primary_key = 'parts_sys_id' #column that serves as primary key (choose a column wiht few duplicates)

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
def christiana(df):
    # Remove parts (keep only labor)
    df = df[df['type'] == 'Parts']
    # Rename cols
    df = rename_cols(df)
    # Remove empty work order id's 
    df = df[(df['parts_sys_id'] != None) & (df['parts_sys_id'].str.strip() != '')]
    # Fill na's in asset sys id
    df['work_order_id'] = df['work_order_id'].fillna('')
    return df