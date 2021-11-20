# %%
import pandas as pd
import numpy as np

# %%
# read the data into a dataframe by chunking and only pulling the columns we need
keep = []
data_iterator = pd.read_csv("/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/arcos_all_washpost.tsv", sep='\t', iterator=True, chunksize=200000,
    usecols=['REPORTER_STATE','REPORTER_COUNTY','BUYER_COUNTY','BUYER_STATE','TRANSACTION_DATE','DOSAGE_UNIT','MME_Conversion_Factor','CALC_BASE_WT_IN_GM','QUANTITY','UNIT','DRUG_NAME','dos_str'])
 
for chunk in data_iterator:
    keep.append(chunk)
final_shipment = pd.concat(keep)

# %%
final_shipment.shape

# %%
# create a new column to change the date format
final_shipment['DATE'] = pd.to_datetime(final_shipment['TRANSACTION_DATE'], format='%m%d%Y')

# %%
# pull out only the year from the date field
final_shipment['Year']= final_shipment['DATE'].dt.year

# %%
# check to see if there are any null values in the the two columns we'll use for our MME calculation
final_shipment[final_shipment['CALC_BASE_WT_IN_GM'].isna()]

# %%
final_shipment[final_shipment['MME_Conversion_Factor'].isna()]
# no nulls in either, good to move on to the calculation

# %%
# convert the weight in grams to milligrams
final_shipment["CALC_BASE_WT_IN_MG"] = final_shipment['CALC_BASE_WT_IN_GM']*1000

# %%
# calculation for Morphine Milligram Equivalent (MME)
final_shipment["MME"] = final_shipment['CALC_BASE_WT_IN_MG']*final_shipment['MME_Conversion_Factor']

# %%
# check to see if there are any null values in county
final_shipment[final_shipment['BUYER_COUNTY'].isna()]
#2057 rows missing county

# %%
# assign to a new dataframe
ship_na = final_shipment[final_shipment['BUYER_COUNTY'].isna()]

# %%
# maybe we could replace the null buyer_county with the popoulated reporter_county.  First check to see if the states match between the two. 
ship_na['matching'] = 1
ship_na.loc[ship_na['BUYER_STATE']== ship_na['REPORTER_STATE'],'matching']=0
ship_na['matching'].sum()
# 1580 rows do not have matching states, therefore we should not replace them and drop these records

# %%
# check to see if there are any null values in the data
ship_na = final_shipment[final_shipment['BUYER_COUNTY'].isna()]

# %%
ship_no_na = final_shipment[final_shipment['BUYER_COUNTY'].notna()]

# %%
# group the data by state, county and year
shipment_grouped = ship_no_na.groupby(['BUYER_STATE','BUYER_COUNTY','Year'],as_index=False)['MME'].sum()

# %%
shipment_cleaned = shipment_grouped[shipment_grouped['BUYER_STATE'] != 'AK']

# %%
shipment_cleaned.to_csv('/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/20_intermediate_files/shipment_data_cleaned.csv', encoding='utf-8')


