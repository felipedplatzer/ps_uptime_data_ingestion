#Constants 
_column_mapping_dict = {
    "number": "labor_sys_id",
    "work_order": "work_order_id",
    "amount": "cost",
    "sys_created_on": "service_date",
    "work_duration": "duration",
    "technician": "technician",
    "summary": "summary",
    "service_activity": None
}

_primary_key = 'labor_sys_id' #column that serves as primary key (choose a column wiht few duplicates)
_duration_denominator = 3600 #duration is stored in seconds for christiana -> need to divide by 3600

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
def raw_to_bronze_christiana(df):
    # Remove parts (keep only labor)
    df = df[df['type'] == 'Labor']
    # Rename cols
    df = rename_cols(df)
    # Remove empty work order id's 
    df = df[(df['labor_sys_id'] != None) & (df['labor_sys_id'].str.strip() != '')]
    # Fill na's in asset sys id
    df['work_order_id'] = df['work_order_id'].fillna('')
    # Convert duration to hours 
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
    df['duration'] = df['duration'] / _duration_denominator
    return df

# MISSING : TRANSFORM DURATION TO COMMON UNIT!!
# MISSING : PARSE SUMMARY FIELD