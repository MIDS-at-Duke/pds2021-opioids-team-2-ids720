# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np

#importing the Data
death_03_df = pd.read_csv("/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2003.txt", sep="\t")
death_04_df = pd.read_csv("/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2004.txt", sep="\t")
death_05_df = pd.read_csv("/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2005.txt", sep="\t")
death_06_df = pd.read_csv("/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2006.txt", sep="\t")
death_07_df = pd.read_csv("/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2007.txt", sep="\t")
death_08_df = pd.read_csv("/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2008.txt", sep="\t")
death_09_df = pd.read_csv("/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2009.txt", sep="\t")
death_10_df = pd.read_csv("/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2010.txt", sep="\t")
death_11_df = pd.read_csv("/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2011.txt", sep="\t")
death_12_df = pd.read_csv("/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2012.txt", sep="\t")
death_13_df = pd.read_csv("/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2013.txt", sep="\t")
death_14_df = pd.read_csv("/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2014.txt", sep="\t")
death_15_df = pd.read_csv("/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2015.txt", sep="\t")


# %%
# Looking at the head of the data
death_03_df.head()


# %%
# Combining all the datasets
vital_stats = pd.concat([death_03_df,death_04_df,death_05_df,death_06_df,death_07_df,death_08_df,death_09_df,death_10_df,death_11_df,death_12_df,death_13_df,death_14_df,death_15_df])


# %%
# Checking if all datasets combined correctly
vital_stats.sample(40)


# %%
# Dropping Notes and Year Code columns. Notes has too many null values and Year Code is a redundant column
vital_stats = vital_stats.drop(["Notes","Year Code"], axis = 1)
vital_stats.head()


# %%
# Looking at the dimension of the dataset
vital_stats.shape


# %%
# Checking data types of each column and null values
vital_stats.info()


# %%
# Looking at total null values
vital_stats.isna().sum()


# %%
#Dropping all na values
vital_stats.dropna(inplace=True)


# %%
# Verifying if all null values are removed
vital_stats.isna().sum()


# # %%
# # Changing datatype for the Year column to date time
vital_stats["Year"] = pd.DatetimeIndex(pd.to_datetime(vital_stats["Year"],format="%Y")).year


# %%
# Verifying change in datetime
vital_stats.info()


# %%
# Looking at the unique causes of death
vital_stats["Drug/Alcohol Induced Cause"].value_counts()


# %%
# Filtering the data drug related deaths
cod = [
    "Drug poisonings (overdose) Unintentional (X40-X44)",
    "Drug poisonings (overdose) Suicide (X60-X64)",
    "Drug poisonings (overdose) Undetermined (Y10-Y14)",
    "Drug poisonings (overdose) Homicide (X85)",
    "All other drug-induced causes"
]
vital_stats_new = vital_stats[vital_stats["Drug/Alcohol Induced Cause"].isin(cod)]
vital_stats_new


# %%
#On trying to convert column "Death" to numeric, noted there is a string value called Missing
# Looking at the rows where data for death is not available
vital_stats_new[vital_stats_new["Deaths"]=="Missing"]


# %%
# We will drop the data for Alaska, keep data for VA as is for now
# First we need to separate our state and county values into separate variables


# %%
#Creating State Codes
vital_stats_new["State_Code"] = vital_stats_new["County"].str[-2:].copy()


# %%
#Subsetting for states we require for our analysis
# states = ["FL","MD","DE","NY","TX","SC","NC","UT","PA","NV","NH"]
# vs_states = vital_stats_new[vital_stats_new["State_Code"].isin(states)]
# vs_states


# %%
new = vital_stats_new["County"].str.split(",", n = 1, expand = True)
vital_stats_new["County_Name"] = new[0]


# %%
# Looking at the dataset with the two new columns
vital_stats_new.head()


# %%
# Dropping Alaska from our data set
vital_stats_final = vital_stats_new.loc[vital_stats_new["State_Code"]!="AK"]


# %%
# Checking if AK statecode is still present in the data
vital_stats_final.loc[vital_stats_final["State_Code"] == "AK"]

#%%


# %%
vital_stats_final.to_csv('/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/20_intermediate_files/vital_stata.csv', encoding='utf-8')




# %%
