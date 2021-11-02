# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd

ship_06_df = pd.read_csv("/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/00_source_data/shipment_data/buyer_monthly2006.csv")
ship_07_df = pd.read_csv("/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/00_source_data/shipment_data/buyer_monthly2007.csv")
ship_08_df = pd.read_csv("/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/00_source_data/shipment_data/buyer_monthly2008.csv")
ship_09_df = pd.read_csv("/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/00_source_data/shipment_data/buyer_monthly2009.csv")
ship_10_df = pd.read_csv("/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/00_source_data/shipment_data/buyer_monthly2010.csv")
ship_11_df = pd.read_csv("/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/00_source_data/shipment_data/buyer_monthly2011.csv")
ship_12_df = pd.read_csv("/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/00_source_data/shipment_data/buyer_monthly2012.csv")
ship_13_df = pd.read_csv("/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/00_source_data/shipment_data/buyer_monthly2013.csv")
ship_14_df = pd.read_csv("/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/00_source_data/shipment_data/buyer_monthly2014.csv")


# %%
shipment = [ship_06_df,ship_07_df,ship_08_df,ship_09_df,ship_10_df,ship_11_df,ship_12_df,ship_13_df,ship_14_df]
ship_data = pd.concat(shipment)


# %%
#ship_states = ship_data[ship_data['BUYER_STATE'].isin(states_needed)]


# %%
ship_data.dtypes


# %%
ship_data[ship_data['BUYER_COUNTY'].isna()]


# %%
ship_data[ship_data['BUYER_DEA_NO'] == 'AL1901621']


# %%
shipment_cleaned = ship_data.dropna()
shipment_cleaned = shipment_cleaned[shipment_cleaned['BUYER_STATE'] != 'AK']


# %%
shipment_cleaned.to_csv('/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/20_intermediate_files/shipment_data.csv', encoding='utf-8')


