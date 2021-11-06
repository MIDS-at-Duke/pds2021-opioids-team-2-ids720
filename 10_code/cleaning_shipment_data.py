# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd

# look at just the first 200 rows to get an idea of what the data looks like
shipment = pd.read_csv("/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/arcos_all_washpost.tsv", sep='\t', nrows=200)


# %%
# read the data into a dataframe by chunking and only pulling the columns we need
keep = []
data_iterator = pd.read_csv("/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/arcos_all_washpost.tsv", sep='\t', iterator=True, chunksize=200000,
    usecols=['REPORTER_STATE','REPORTER_COUNTY','BUYER_COUNTY','BUYER_STATE','TRANSACTION_DATE','DOSAGE_UNIT','MME_Conversion_Factor','QUANTITY','UNIT','DRUG_NAME','dos_str'])
 
for chunk in data_iterator:
    keep.append(chunk)
final_shipment = pd.concat(keep)


# %%
final_shipment.shape


# %%
# create a new column to change the date format
final_shipment['DATE'] = pd.to_datetime(final_shipment['TRANSACTION_DATE'], format='%m%d%Y')


# %%
# calculation for Morphine Milligram Equivalent (MME)
final_shipment["MME"] = final_shipment['DOSAGE_UNIT']*final_shipment['MME_Conversion_Factor']*final_shipment['dos_str']


# %%
# pull out only the year from the date field
final_shipment['Year']= final_shipment['DATE'].dt.year


# %%
# check to see if there are any null values in the data
ship_na = final_shipment[final_shipment['BUYER_COUNTY'].isna()]
#2057 rows missing county


# %%
# maybe we could replace the null buyer_county with the popoulated reporter_county.  First check to see if the states match between the two. 
ship_na['matching'] = 1
ship_na.loc[ship_na['BUYER_STATE']== ship_na['REPORTER_STATE'],'matching']=0
ship_na['matching'].sum()
# 1580 rows do not have matching states, therefore we should not replace them and drop these records


# %%
ship_no_na = final_shipment[final_shipment['BUYER_COUNTY'].notna()]


# %%
# group the data by state, county and year
shipment_grouped = ship_no_na.groupby(['BUYER_STATE','BUYER_COUNTY','Year'],as_index=False)['MME'].sum()


# %%
shipment_cleaned = shipment_grouped[shipment_grouped['BUYER_STATE'] != 'AK']


# %%
shipment_cleaned.to_csv('/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/20_intermediate_files/shipment_data_cleaned.csv', encoding='utf-8')


