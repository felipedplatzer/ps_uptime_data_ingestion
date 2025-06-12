#Constants 
_column_mapping_dict = {
    "Work Order": "work_order_id",
    "Request Date": "reported_date",
    "Work Order Status": "work_order_status",
    "Status Date": "sys_updated_on", # assume that completed date is end time, not status date
    "Work Order Type": "type",
    "Requester": "REPORTED_BY",
    "Phone": None,
    "Email": None,
    "Problem": "problem",
    "Work Order Common Problem": None,
    "Cost Center": None,
    "Cost Center Code": None,
    "Responsible Center": None,
    "Responsible Center Code": None,
    "Priority": "priority",
    "Due Date": "due_date",
    "Estimated Hours": "scheduled_duration",
    "Job Type": None,
    "Procedure": None,
    "Vendor Assigned": "vendor_assigned",
    "FSR Number": None,
    "Service Department": None,
    "Trade": None,
    "Employees Assigned": "technician",
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
    "Employee": None,
    "Contract": None,
    "Vendor": None,
    "Response": None,
    "Action": None,
    "Start DateTime": None,
    "End DateTime": "completed_date",
    "Billable": None,
    "Employee Rate": None,
    "Contract Rate": None,
    "Vendor Rate": None,
    "Rate Type": None,
    "Hours": None,
    "Charge": None,
    "Labor Total": None,
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

_primary_key = '' #column that serves as primary key (choose a column wiht few duplicates)


# Import libraries
import pandas as pd


# CONTRACT -> UNDER CONTRACT MISSING!!

#Functions
def rename_cols(df):
    current_uptime_cols = {k: v for k, v in _column_mapping_dict.items() if v != None}
    new_cols =  [k for k, v in _column_mapping_dict.items() if v == None]
    df = df.rename(columns=current_uptime_cols)
    df['comments'] = df[new_cols].to_dict(orient='records')
    df = df.drop(new_cols, axis=1)
    return df


# Main
def methodist(df):
    # Rename cols
    df = rename_cols(df)

    # Remove empty work order id's 
    df['work_order_id'] = df['work_order_id'].fillna('').astype(str)
    df = df[(df['work_order_id'] != '')]
    # Fill na's in asset sys id
    df['asset_sys_id'] = df['asset_sys_id'].fillna('')
    #df['work_order_id'] = df['work_order_id'].astype(str) + '.' + df['asset_sys_id'].astype(str) 

    return df

    # IN OTHER CUSTOMERS : TRANSFORM SCHEDULED DURATION TO COMMON UNIT!!