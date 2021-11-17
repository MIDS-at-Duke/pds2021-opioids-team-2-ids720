# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np

population = pd.read_csv('/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/20_intermediate_files/population_2000_2020_inc.csv')

shipment = pd.read_csv('/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/20_intermediate_files/shipment_data_cleaned.csv')

fips = pd.read_csv('https://raw.githubusercontent.com/vmtang11/estimating-impact-of-opioid-prescription-regulations-team-7/master/00_source/county_fips.csv')


# %%
population.head()


# %%
# ensuring the fips code doesn't have anything missing
test = shipment.merge(fips, how="left", validate="m:1",on= ['BUYER_STATE', 'BUYER_COUNTY'], indicator=True)
#looks like there are problems
problems = test.loc[test["_merge"] != "both"]["BUYER_STATE"]
problems.unique()
# the problem is mostly occuring in US territories, plus Arkansas
test[test["BUYER_STATE"] == "AR"]
test.loc[(test["_merge"] != "both") & (test["BUYER_STATE"]== "AR")]["BUYER_COUNTY"].unique()


# %%
# adding Montgomery County, Arkansas since it was missing from the fips data
adding_county={'BUYER_COUNTY':'MONTGOMERY',
        'BUYER_STATE': 'AR',
        'countyfips': 5097}


# %%
fips_new = fips.append(adding_county,ignore_index=True)


# %%
# add fips code to shipment data
fips_new["countyfips"] = fips_new["countyfips"].astype(str)

for i, row in fips_new.iterrows():
    if len(row["countyfips"]) < 5:
        fips_new.at[i,'fips_new'] = '0' + row["countyfips"]
        pass
    else:
        fips_new.at[i,'fips_new'] = row["countyfips"]
        pass
    pass


# %%
# check to make sure length = 5
(fips_new['fips_new'].apply(len) != 5).any()


# %%
# add fips code to population data

population["fips_code"] = population["fips_code"].astype(str)

for i, row in population.iterrows():
    if len(row["fips_code"]) < 5:
        population.at[i,'fips_new'] = '0' + row["fips_code"]
        pass
    else:
        population.at[i,'fips_new'] = row["fips_code"]
        pass
    pass


# %%
# check to make sure length = 5
(population['fips_new'].apply(len) != 5).any()


# %%
# merge the fips with the shipment data
ship_fips_merged = pd.merge(shipment, fips_new, how='left', on=['BUYER_COUNTY','BUYER_STATE'], indicator=True, validate='m:1')


# %%
shipment.head()


# %%
# this shows us the U.S. territories that we did not resolve from earlier
np.unique(ship_fips_merged.loc[ship_fips_merged['_merge']=='left_only','BUYER_STATE'])


# %%
# move forward without U.S. territories 
ship_fips_merged = ship_fips_merged.loc[ship_fips_merged['_merge'] !='left_only']


# %%
# should only see where merge was from both
np.unique(ship_fips_merged['_merge'])


# %%
# drop the _merge column so that we can get a new merge indicator in the next step
ship_fips_merged.drop('_merge', axis=1, inplace=True)


# %%
# merge the shipment data with the population data
ship_pop_merged = pd.merge(ship_fips_merged, population, how='left', on=['fips_new','Year'], indicator=True, validate='m:1')


# %%
ship_pop_merged.head()


# %%
# find out where the merge happens for left only
ship_pop_merged[ship_pop_merged['_merge'] =='left_only']


# %%
# population data was missing for DC, so we can either delete these 7 rows, or try to get the population data for DC
# ship_pop_final = ship_pop_merged[ship_pop_merged['fips_new'] != '11001']


# %%
ship_pop_merged.to_csv('/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/20_intermediate_files/merged_pop_and_ship_and_fips.csv', encoding='utf-8')


