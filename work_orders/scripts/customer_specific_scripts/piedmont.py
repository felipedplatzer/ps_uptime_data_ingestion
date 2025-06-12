#Constants 
_column_mapping_dict = {
    "WO_NUMBER": "work_order_id", 
    "TAG_NUMBER": "asset_sys_id", 
    "TYPE": None, 
    "REQST_DATETIME": "reported_date", 
    "WO_TYPE": None, 
    "WO_TYPE_DESC": "type", 
    "WO_STATUS": None, 
    "WO_STATUS_DESC": "work_order_status", 
    "WO_PROBLEM": "problem", 
    "SRVC_DEPT": None, 
    "SRVC_DEPT_DESC": None, 
    "TRADE_EMP": None, 
    "PROC_JOBTY": None, 
    "PROC_JOBTY_DESC": None, 
    "PRIORITY": None, 
    "PRIORITY_DESC": "priority", 
    "DUE_DATETIME": "due_date", 
    "EST_TIME": "scheduled_duration", 
    "FREQ_UNIT": None, 
    "FREQUENCY": None, 
    "STAT_DATETIME": "sys_updated_on", 
    "FAILURE": None, 
    "FAILURE_DESC": "problem_cause", 
    "CHG_CTR": None, 
    "CHG_CTR_DESC": None, 
    "LOCATION": None, 
    "FACILITY_DESC": None, 
    "FSR_TRACKING": None, 
    "TRADE_TYPE": None, 
    "IMPORT": None, 
    "SPEC_CODE": None, 
    "SPEC_NAME": None, 
    "HIPAA": None, 
    "CONDITION": None, 
    "CONDITION_DESC": None, 
    "EQU_DOWNTIME": "downtime_impact", 
    "BLD_CODE": None, 
    "BLD_DESC": None
}


# MISSING STAT_DATETIME = CLOSED DATE FOR ORDERS CLOSED


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




# Main
def piedmont(df):

    # Rename cols
    df = rename_cols(df)
    # Remove empty work order id's 
    df['work_order_id'] = df['work_order_id'].fillna('').astype(str)
    df = df[(df['work_order_id'].str.strip() != '')]
    df['downtime_impact'] = df['downtime_impact'].astype(str)
    # Fill na's in asset sys id
    df['asset_sys_id'] = df['asset_sys_id'].fillna('')
    
    #df['work_order_id'] = df['work_order_id'].astype(str) + '.' + df['asset_sys_id'].astype(str) 
    return df

    # IN OTHER CUSTOMERS : TRANSFORM SCHEDULED DURATION TO COMMON UNIT!!