# %%
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import os

os.chdir(
    "C:\\Users\\deeks\\Documents\\MIDS\\IDS 720_Practising Data Science\\Mid-Sem project\\Gitdata\\pds2021-opioids-team-2-ids720\\"
)


# %%
popinc = pd.read_csv("./20_intermediate_files/population_2000_2020_inc.csv")
death = pd.read_csv("./20_intermediate_files/vital_stata.csv")


# %%
# Looking at the distribution of Population and Income data
popinc.head()

# %%
# Population Income data types
popinc.info()

# %%
# %%
# Vital Statistics data types
death.info()


# %%
# Dropping the unnamed column
death.drop("Unnamed: 0", axis=1, inplace=True)

# %%

# %%
# Changing columns name for merging
popinc = popinc.rename({"CTYNAME": "County_Name"}, axis=1)
popinc

# %%
death["Deaths"] = death["Deaths"].replace("Missing", np.NaN)
death["Deaths"] = death["Deaths"].astype(float)
death.dropna(subset=["Deaths"], inplace=True)


# %%
deaths_grouped = death.groupby(["Year", "State_Code", "County_Name"], as_index=False)[
    "Deaths"
].apply(lambda x: x.sum())
deaths_grouped.isnull().sum()

# %%
# Merging Population with Deaths
merged = pd.merge(
    deaths_grouped[
        [
            "Year",
            "State_Code",
            "County_Name",
            "Deaths",
        ]
    ],
    popinc[
        [
            "Year",
            "State_Code",
            "County_Name",
            "Population",
            "Median_Income_2010",
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
# Viewing the merged dataset
merged.head()

# %%
# %%
# Verifying whether the data merged correctly
dropped_left = merged[merged["_merge"] != "left_only"]
dropped_left["_merge"].value_counts()
# There are cases where data was only available in left column

# Subsetting the data for the years in our analysis
# %%
years = range(2003, 2016)
dropped_left = dropped_left.loc[dropped_left["Year"].isin(years)]

# Adding column to assess where mortality data is available
# %%
dropped_left["bad_merge"] = np.where(dropped_left["_merge"] == "both", 0, 1)
dropped_left["bad_merge"].value_counts()
dropped_left

# Grouping by county to assess share  of mortality data against popn
# %%
merge_grouped = dropped_left.groupby(["State_Code", "County_Name"], as_index=False)[
    ["Population", "bad_merge"]
].mean()
merge_grouped["bad_merge"].unique()

# %%
merge_grouped


# %%
import altair as alt

alt.Chart(merge_grouped[merge_grouped.Population < 1_000_000]).encode(
    x="Population",
    y=alt.Y("bad_merge", title="Missing Mortality Share", scale=alt.Scale(zero=False)),
).mark_point()

# Based on the plotting taking a cutoff based on population for counties
# %%
subset = merge_grouped.loc[merge_grouped["Population"] >= 400000].copy()
subset["indicator"] = subset["State_Code"] + "-" + subset["County_Name"]
county = list(subset.indicator.unique())

# %%
vs_pop_thresh = dropped_left.copy()
vs_pop_thresh.head()

# %%
vs_pop_thresh["indicator"] = (
    vs_pop_thresh["State_Code"] + "-" + vs_pop_thresh["County_Name"]
)


# %%
vs_pop_thresh = vs_pop_thresh.loc[vs_pop_thresh["indicator"].isin(county)]


# %%
len(vs_pop_thresh)
vs_pop_thresh.State_Code.value_counts()


# %%
vs_pop_thresh.Deaths.isna().sum()

# %%
vs_pop_thresh.to_csv(
    "./20_intermediate_files/mortality_merged_with_pop_thresh.csv",
    encoding="utf-8",
    index=False,
)


# # %%
# mortality = vs_pop_thresh.groupby(
#     ["Year", "State_Code", "County_Name", "Population", "Median_Income_2010"],
#     as_index=False,
# )["Deaths"].apply(lambda x: x.sum())
# mortality.head()

# # %%
# mortality.to_csv(
#     "./20_intermediate_files/mortality_merged_with_pop_thresh.csv",
#     encoding="utf-8",
#     index=False,
# )

# %%
