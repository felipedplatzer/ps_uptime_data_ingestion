#Constants 
_column_mapping_dict = {
    "WO_NUMBER": "work_order_id",
    "SEQUENCE": None,
    "EMPLOYEE": "technician",
    "RESPONSE": None,
    "HOURS": "duration",
    "ACTION": None,
    "CHG_RATE": None,
    "RATE_MULTI": None,
    "WORK_TYPE": None,
    "LABOR_TYPE": "labor_type",
    "COSTING_TYPE": None,
    "FACILITY": None,
    "CONTRACT_RATE": None,
    "BILLABLE": None,
    "CHARGE": "cost",
    "DONE_DATETIME": "service_date"
}

# break down action into code and description

_primary_key = '' #column that serves as primary key (choose a column wiht few duplicates)
# create parimary key as wo_id + sequence

_duration_denominator = 1 #duration is stored in seconds for christiana -> need to divide by 3600

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
    # Create primary key
    df['labor_sys_id'] = df['WO_NUMBER'].astype(str) + '.' + df['SEQUENCE'].astype(str)
    # Rename cols
    df = rename_cols(df)
    # Remove empty work order id's 
    df = df[(df['labor_sys_id'] != None) & (df['labor_sys_id'].str.strip() != '')]
    # Fill na's in asset sys id
    df['work_order_id'] = df['work_order_id'].fillna('').astype(str)
    # Convert duration to hours 
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
    df['duration'] = df['duration'] / _duration_denominator


    return df

    # IN OTHER CUSTOMERS, PARSE SUMMARY FIELD