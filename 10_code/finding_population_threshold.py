# %%
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np


# %%
popinc = pd.read_csv("/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/20_intermediate_files/population_2000_2020_inc.csv")
death = pd.read_csv("/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/20_intermediate_files/vital_stata.csv")


# %%
# Looking at the distribution of Population and Income data
popinc.head()

# %%
#Population Income data types
popinc.info()

# %%
# %%
#Vital Statistics data types
death.info()


# %%
# Dropping the unnamed column
death.drop("Unnamed: 0", axis = 1, inplace=True)

# %%

# %%
# Changing columns name for merging
popinc = popinc.rename({"CTYNAME":"County_Name"}, axis =1)
popinc


# %%

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
    how="outer",
    on=["Year", "State_Code", "County_Name"],
    validate="m:1",
    indicator=True,
)

# %%
merged._merge.value_counts()

# %%
#Viewing the merged dataset
merged.head()

# %%
# %%
# Verifying whether the data merged correctly
dropped_left = merged[merged["_merge"] != "left_only"]
dropped_left['_merge'].value_counts()
# There are cases where data was only available in left column

# %%
years = range(2003, 2016)
dropped_left = dropped_left.loc[dropped_left["Year"].isin(years)]

# %%
dropped_left["bad_merge"] = np.where(dropped_left["_merge"] == "both", 0, 1)
dropped_left['bad_merge'].value_counts()
dropped_left

# %%
merge_grouped = dropped_left.groupby(["State_Code","County_Name"],as_index=False)[['Population','bad_merge']].mean()
merge_grouped["bad_merge"].unique()

# %%
merge_grouped

# %%
import altair as alt

alt.Chart(merge_grouped[merge_grouped.Population < 1_000_000]).encode(x = "Population",y=alt.Y("bad_merge", title = "Missing Mortality Share", scale=alt.Scale(zero=False))).mark_point()


