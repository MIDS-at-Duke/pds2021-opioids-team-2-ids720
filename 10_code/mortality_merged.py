# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np


# %%
popinc = pd.read_csv("https://media.githubusercontent.com/media/MIDS-at-Duke/pds2021-opioids-team-2-ids720/data_merging/20_intermediate_files/population_2000_2020_inc.csv?token=AVKGWH74OQFKBHCJNDCRCZLBQMEY4")
death = pd.read_csv("/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/20_intermediate_files/vital_stata.csv")


# %%
# Looking at the distribution of Population and Income data
popinc.head()


# %%
#Population Income data types
popinc.info()


# %%
#Vital Statistics data types
death.info()


# %%
# Dropping the unnamed column
death.drop("Unnamed: 0", axis = 1, inplace=True)


# %%
# Changing columns name for merging
popinc = popinc.rename({"CTYNAME":"County_Name"}, axis =1)
popinc


# %%
# Merging Population with Deaths
merged = pd.merge(
    death[
        [
            "County",
            "Year",
            "Drug/Alcohol Induced Cause",
            "Deaths",
            "State_Code",
            "County_Name",
        ]
    ],
    popinc[
        [
            "STNAME",
            "County_Name",
            "Year",
            "State_Code",
            "Population",
            "Median_Income_2010",
            "Income_Error_Margin",
        ]
    ],
    how="left",
    on=["Year", "State_Code", "County_Name"],
    validate="m:1",
    indicator=True,
)


# %%
#Viewing the merged dataset
merged.head()


# %%
# Verifying whether the data merged correctly
check = merged[merged["_merge"] != "both"]
check
# There are cases where data was only available in left column


# %%
#Checking the counties where we did not have population and income data
check.County.value_counts()


# %%
#Checking how many values by state are unavailable
check.State_Code.value_counts()


# %%
#Checking unavailable values based on year
check.Year.value_counts().sort_values()

# %% [markdown]
# For now we will leave these values as it is, and proceed with calculating deaths per capita to select the states, for our analysis. If the per capita rate for any of these states is close to our Analysis states (TX,FL, WA) we can think of how to impute these values

# %%
# Calculating county wise death per capita
# Replacing the "Missing" value in Death column by Nan
merged = merged.replace("Missing", np.NaN)
merged.info() #Checking the datatype of Deaths column


# %%
#Changing datatype of death column to float to calculate the death per cap
merged["Deaths"]= merged.Deaths.astype(str).astype(float)
merged.info()


# %%
merged["Death_per_cap"] = (merged["Deaths"] / merged ["Population"])


# %%
merged.columns


# %%
#Reordering the columns 
merged = merged[
    [
        "Year",
        "State_Code",
        "STNAME",
        "County_Name",
        "County",
        "Population",
        "Drug/Alcohol Induced Cause",
        "Deaths",
        "Median_Income_2010",
        "Income_Error_Margin",
        "_merge",
        "Death_per_cap",
    ]
]


# %%
#Renaming columns
merged = merged.rename({"STNAME":"State","County":"ST_CT_Name"})


# %%
# Looking at the death per cap values to shortlist the control states for our analysis
merged.groupby(by=(["State_Code"])).mean().sort_values(by="Death_per_cap")


# %%
# For WA - IL, ID, WI
# For FL - IL, WA, ID
# For TX - UT, CO, KS


# %%
merged.to_csv('/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/20_intermediate_files/mortality_merged.csv', encoding='utf-8')


# %%



