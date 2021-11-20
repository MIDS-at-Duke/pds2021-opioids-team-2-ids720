# %%
import pandas as pd
import numpy as np

# %%
popinc = pd.read_csv("https://media.githubusercontent.com/media/MIDS-at-Duke/pds2021-opioids-team-2-ids720/data_merging/20_intermediate_files/population_2000_2020_inc.csv?token=AVKGWH4IHMMTY4IFIP4BRBTBS4OUU")
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
print(death.Deaths.min())
print(death.Deaths.max())

# %%
#Vital Statistics data types
death.info()

# %%
death["Drug/Alcohol Induced Cause"].unique()

# %%
death = death.replace("Missing", np.NaN)

# %%
death["Deaths"] = death["Deaths"].astype(float)

# %%
# Collapsing the dataset to get total number of deaths per county per year
mortality = death.groupby(["Year","State_Code","County_Name"], as_index=False)['Deaths'].apply(lambda x: x.sum())
mortality.head()

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
    how="outer",
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
merged.loc[merged["Deaths"].isna()]["State_Code"].unique()

# %%
[merged["Deaths"].isna().sum()]

# %%
# Verifying whether the data merged correctly
check = merged[merged["_merge"] != "both"]
check
# There are cases where data was only available for each respective dataset

# %%
check_right = merged[merged["_merge"] == "right_only"]
check_right

# %%
check[check["_merge"] == "left_only"]

# %%
#Imputing death values where death data is missing
merged["Deaths"] = merged["Deaths"].apply(lambda x: x if not np.isnan(x) else np.random.randint(0, 10))

# %%
[merged["Deaths"].isna().sum()]

# %%
#Checking the counties where we did not have population and income data
check[check["_merge"]=="left_only"].County_Name.value_counts()

# %%
#Checking how many values by state are unavailable
check[check["_merge"]=="left_only"].State_Code.value_counts()

# %%
#Checking unavailable values based on year
check[check["_merge"]=="left_only"].Year.value_counts().sort_values()

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
merged.info()

# %%
# Looking at the death per cap values to shortlist the control states for our analysis
merged.groupby(by=(["Year","State_Code"])).mean().sort_values(by="Death_per_cap")

# %%
merged.duplicated(["Year","State_Code","County_Name"]).sum()

# %%
# For WA - IL, ID, WI
# For FL - IL, WA, ID
# For TX - UT, CO, KS

# %%
print(merged.Year.min())
print(merged.Year.max())

# %%
merged.Year.unique()

# %%
years = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
       2014, 2015]
merged_final = merged[merged["Year"].isin(years)]

# %%
print(merged_final.Year.min())
print(merged_final.Year.max())

# %%
merged_final.to_csv('/Users/Aarushi/Duke/MIDS - Fall 2021/Fall 2021/720_IDS_PDS/pds2021-opioids-team-2-ids720/20_intermediate_files/mortality_merged.csv', encoding='utf-8', index=False)


# %%



