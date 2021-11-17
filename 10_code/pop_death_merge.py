# %%
import pandas as pd
import numpy as np

# %%
popinc = pd.read_csv("https://media.githubusercontent.com/media/MIDS-at-Duke/pds2021-opioids-team-2-ids720/main/20_intermediate_files/population_2000_2020_inc.csv?token=AVKGWHZB465MIBQ6V7QXPU3BSQQTG")
death = pd.read_csv("/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/20_intermediate_files/vital_stata.csv")

# %%
# Looking at the distribution of Population and Income data
popinc.head()

# %%
#Population Income data types
popinc.info()

# %%
death.head()

# %%
#Vital Statistics data types
death.info()

# %%
for i in death.Deaths.unique():
    print(i)

# %%
death = death.replace("Missing", np.NaN)

# %%
death.Deaths.value_counts()

# %%
death["Deaths"] = death["Deaths"].astype(float)

# %%
for i in death.Deaths.unique():
    print(i)

# %%
death.info()

# %%
# Collapsing the dataset to get total number of deaths per county per year
mortality = death.groupby(["Year","State_Code","County_Name"], as_index=False)['Deaths'].apply(lambda x: x.sum())
mortality.head()

# %%
# death.Deaths.isnull().sum()
# death.Deaths.isna().sum()
# death[death["Deaths"] == "" ]

# %%
# import re
# # exp = "\s+"
# for i in death["Deaths"].unique():
#     if re.match(exp,i):
#         print(i)

# %%
# for i in death["Deaths"].unique():
#     print(i)

# %%
# Changing columns name for merging
popinc = popinc.rename({"CTYNAME":"County_Name"}, axis =1)
popinc

# %%
# Merging Population with Deaths
merged = pd.merge(
    mortality[
        [
            "Year",
            "State_Code",
            "County_Name",
            "Deaths"
        ]
    ],
    popinc[
        [
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
merged.loc[merged["Population"].isna()]["State_Code"].unique()

# %%
# Verifying whether the data merged correctly
check = merged[merged["_merge"] != "both"]
check
# There are cases where data was only available in left column

# %%
#Checking the counties where we did not have population and income data
check.County_Name.value_counts()

# %%
#Checking how many values by state are unavailable
check.State_Code.value_counts()

# %%
#Checking unavailable values based on year
check.Year.value_counts().sort_values()

# %% [markdown]
# For now we will leave these values as it is, and proceed with calculating deaths per capita to select the states, for our analysis. If the per capita rate for any of these states is close to our Analysis states (TX,FL, WA) we can think of how to impute these values

# %%
# Checking rows where number of deaths is not available
merged[merged["Deaths"]==np.NaN]

# %%
#Checking if there are any missing values in the merged dataset for population
#merged.loc[merged["Population"].isna()]
# Here we see that most of the values are similar to the issue in the left merge column implying that we do not have population and income data for those specific counties 
#However we have 4 rows where the population datat is missing in the population file as well.
#On further review, it is for BEdford City, VA and the poppulation estimate as per google is ~7000 which is pretty irrelevant imo

# %%
# Calculating county wise death per capita
# Replacing the "Missing" value in Death column by Nan
#merged = merged.replace("Missing", np.NaN)
#merged.info() #Checking the datatype of Deaths column


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
        "County_Name",
        "Population",
        "Deaths",
        "Death_per_cap",
        "Median_Income_2010",
        "Income_Error_Margin",
        "_merge",

    ]
]


# %%
# Looking at the death per cap values to shortlist the control states for our analysis
merged.groupby(by=(["State_Code"])).mean().sort_values(by="Death_per_cap")

# %%
# For WA - IL, ID, WI
# For FL - IL, WA, ID
# For TX - UT, CO, KS

# %%
merged.to_csv('/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/20_intermediate_files/mortality_merged.csv', encoding='utf-8', index=False)


# %%



