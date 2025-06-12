#Constants 
_column_mapping_dict = {
    "number": "labor_sys_id",
    "amount": "cost",
    "summary": "summary",
    "work_duration": "duration",
    "type": "labor_type",
    "technician": "technician",
    "work_order": "work_order_id",
    "inventoried_part": None,
    "part_description": None,
    "parts": None,
    "price_per_unit": None,
    "quantity": None,
    "service_activity": None

}

_duration_denominator = 3600 #duration is stored in seconds for wakemed -> need to divide by 3600

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
def wakemed(df):
    # Remove parts (keep only labor)
    df = df[df['type'] == 'Labor']
    # Rename cols
    df = rename_cols(df)
    # Remove empty work order id's 
    df['labor_sys_id'] = df['labor_sys_id'].fillna('').astype(str)
    df = df[(df['labor_sys_id'].str.strip() != '')]
    # Fill na's in asset sys id
    df['work_order_id'] = df['work_order_id'].fillna('')
    # Convert duration to hours 
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
    df['duration'] = df['duration'] / _duration_denominator


    return df

    # IN OTHER CUSTOMERS, PARSE SUMMARY FIELD