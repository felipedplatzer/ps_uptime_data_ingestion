#Constants 
_column_mapping_dict = {
    "TAG_NUMBER": "asset_tag", 
    "DESCRIPTN": "description", 
    "TYPE": None, 
    "TYPE_DESC": "modality", 
    "MANUFACTUR": None, 
    "MANUFACTUR_DESC": "make", 
    "MODEL_NUM": "model_number", 
    "INSVC_DATETIME": "in_service_date", 
    "STATUS_DESC": "lifecycle_status", 
    "STAT_DATETIME": "sys_updated_on", 
    "LOCATION": "last_known_location", 
    "LOC_DATETIME": None, 
    "INC_FACTOR": None, 
    "COST_CTR": None, 
    "COST_CTR_DESC": "department", 
    "PO_NUMBER": None, 
    "PURCH_COST": "acquisition_cost", 
    "FACILITY": None, 
    "FACILITY_DESC": "campus_name", 
    "PRIM_TRADE": None, 
    "EQU_MODEL_NAME": "model_name", 
    "CONDITION_DESC": None, 
    "BLD_CODE": None, 
    "BLD_NAME": "building_name",
    "PURCH_DATETIME": None, 
    "SRVC_DEPT_DESC": None, 
    "OWNERSHIP_NAME": "acquisition_method"

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


# Main
def piedmont(df):
    df = rename_cols(df)
    df['asset_sys_id'] = df['asset_tag'] # can't put TAG_NUMBER (which converts to asset_tag) in the dict, because it's a duplicate. Therefore, I have to add it after the rename_cols function
    return df

