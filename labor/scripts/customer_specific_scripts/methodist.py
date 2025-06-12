#Constants 
_column_mapping_dict = {



    "Work Order": "work_order_id",
    "Request Date": None,
    "Work Order Status": None,
    "Status Date": None, # assume that completed date is end time, not status date
    "Work Order Type": None,
    "Requester": None,
    "Phone": None,
    "Email": None,
    "Problem": None,
    "Work Order Common Problem": None,
    "Cost Center": None,
    "Cost Center Code": None,
    "Responsible Center": None,
    "Responsible Center Code": None,
    "Priority": "priority",
    "Due Date": "due_date",
    "Estimated Hours": None,
    "Job Type": None,
    "Procedure": None,
    "Vendor Assigned": None,
    "FSR Number": None,
    "Service Department": None,
    "Trade": None,
    "Employees Assigned": None,
    "location": None,
    "Facility": None,
    "Building": None,
    "Free Text Location": None,
    "Location Date": None,
    "Equipment Down": None,
    "Equipment Down Date/Time": None,
    "Equipment Back Online": None,
    "Equipment Back Online Date/Time": None,
    "Failure": "problem_cause",
    "Incident Report": None,
    "PM Preventable": None,
    "PM Result": None,
    "ECN": "asset_sys_id",
    "Manufacturer": None,
    "Nameplate Manufacturer": None,
    "Model Number": None,
    "Model Name": None,
    "Description": None,
    "Serial": None,
    "Asset Number": None,
    "Equipment Type": None,
    "Risk Classification": None,
    "Cost Center": None,
    "Cost Center Code": None,
    "Responsible Center": None,
    "Responsible Center Code": None,
    "In Service Date": None,
    "Equipment Status": None,
    "Status Date": None,
    "Equipment Condition": None,
    "Condition Date": None,
    "Site ID": None,
    "Employee": "technician",
    "Contract": None,
    "Vendor": None,
    "Response": None,
    "Action": "summary",
    "Start DateTime": None,
    "End DateTime": "service_date",
    "Billable": None,
    "Employee Rate": None,
    "Contract Rate": None,
    "Vendor Rate": None,
    "Rate Type": None,
    "Hours": "duration",
    "Charge": None, # No cost per hour recorded
    "Labor Total": "cost",
    "Test Equipment": None,
    "Part": None,
    "Contract": None,
    "Vendor": None,
    "Description": None,
    "Billable": None,
    "Quantity": None,
    "Price": None,
    "Material Extended": None,
    "Part Serial Number": None,
    "Batch Number": None,
    "Old Work Order Number": None
}

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
def methodist(df):
    # Rename cols
    df = rename_cols(df)
    # Add primary key
    df['work_order_id'] = df['work_order_id'].fillna('').astype(str)
    df['labor_sys_id'] = df['work_order_id'] # Methodist has 1 labor record per work order, so WO id can be used as labor item id
    # Remove empty work order id's 
    df = df[(df['labor_sys_id'].str.strip() != '')]

    # Fill na's in asset sys id
    
    # Convert duration to hours 
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
    df['duration'] = df['duration'] / _duration_denominator


    return df

    # IN OTHER CUSTOMERS, PARSE SUMMARY FIELD