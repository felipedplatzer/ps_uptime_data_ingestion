import pandas as pd
from datetime import datetime

silver_df = pd.read_csv('./silver_summa_assets.csv')



if __name__ == "__main__":
    # Convert date columns to datetime
    date_columns = ['in_service_date', 'warranty_end_date', 'service_contract_end_date']
    for col in date_columns:
        silver_df[col] = pd.to_datetime(silver_df[col], errors='coerce')
    
    # Get today's date
    today = pd.Timestamp(datetime.now().date())
    
    # Filter out invalid dates and costs
    silver_df = silver_df[
        (silver_df['in_service_date'] >= '1970-01-01') &
        (silver_df['in_service_date'] <= today) &
        (silver_df['warranty_end_date'] >= '1970-01-01') &
        #(silver_df['service_contract_end_date'] >= '1970-01-01') &
        (silver_df['acquisition_cost'] >= 0) &
        #(silver_df['service_contract_annual_cost'] >= 0)
    ]
    
    # Round cost columns to 2 decimal places
    silver_df['acquisition_cost'] = silver_df['acquisition_cost'].round(2)
    silver_df['service_contract_annual_cost'] = silver_df['service_contract_annual_cost'].round(2)
    
    # Save the cleaned data
    silver_df.to_csv('./gold_summa_assets.csv', index=False)
    