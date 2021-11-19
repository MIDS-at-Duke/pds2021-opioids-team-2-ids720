# %%
import pandas as pd
import numpy as np

# %%
popinc = pd.read_csv(
    "https://media.githubusercontent.com/media/MIDS-at-Duke/pds2021-opioids-team-2-ids720/data_merging/20_intermediate_files/population_2000_2020_inc.csv?token=AQKRUJC5VSCD7TZFOIACTCLBS4QLO"
)
death = pd.read_csv(
    "https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-2-ids720/data_merging/20_intermediate_files/vital_stata.csv?token=AQKRUJFEJJGQV7QJDE4SJ2TBUBG2U"
)

# %%
death["Drug/Alcohol Induced Cause"].unique()

# %%
death.head()

# %%
death["Deaths"] = death["Deaths"].replace("Missing", np.NaN)
death["Deaths"] = death["Deaths"].astype(float)

# %%
death.info()

# %%
# Collapsing the dataset to get total number of deaths per county per year
mortality = death.groupby(["Year", "State_Code", "County_Name"], as_index=False)[
    "Deaths"
].apply(lambda x: x.sum())
mortality.head()

# %%
# Changing columns name for merging
popinc = popinc.rename({"CTYNAME": "County_Name"}, axis=1)
# popinc

# %%
# Merging Population with Deaths
merged = pd.merge(
    mortality[["Year", "State_Code", "County_Name", "Deaths"]],
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
# Viewing the merged dataset
merged.head()

# %%
merged.loc[merged["Population"].isna()]["State_Code"].unique()

# %%
merged.loc[merged["Deaths"].isna()]["State_Code"].unique()

# %%
[merged["Deaths"].isna().sum()]

# %%
import sklearn
from sklearn.impute import KNNImputer

# %%
# merged["Deaths"] = merged["Deaths"].apply(lambda x: x if not np.isnan(x) else np.random.randint(0, 10))

# %% [markdown]
# For now we will leave these values as it is, and proceed with calculating deaths per capita to select the states, for our analysis. If the per capita rate for any of these states is close to our Analysis states (TX,FL, WA) we can think of how to impute these values

# %%
# Checking rows where number of deaths is not available
merged["Deaths"] = merged["Deaths"].astype(float)
merged.info()

# %%
merged["Deaths"].isna().sum()

# %%
# Checking if there are any missing values in the merged dataset for population
# merged.loc[merged["Population"].isna()]
# Here we see that most of the values are similar to the issue in the left merge column implying that we do not have population and income data for those specific counties
# However we have 4 rows where the population datat is missing in the population file as well.
# On further review, it is for BEdford City, VA and the poppulation estimate as per google is ~7000 which is pretty irrelevant imo

# %%
# Calculating county wise death per capita
# Replacing the "Missing" value in Death column by Nan
# merged = merged.replace("Missing", np.NaN)
# merged.info() #Checking the datatype of Deaths column


# %%
merged["Death_per_cap"] = merged["Deaths"] / merged["Population"]

# %%
[merged["Death_per_cap"].isna().sum()]

# %%
test = merged.loc[merged["State_Code"] == "TX"].copy()
idx_list = test.index.tolist()
len(idx_list)

# %%
merged_TX = merged.loc[merged["State_Code"] == "TX"].copy().reset_index(drop=True)
merged_TX.head()

# %%
merged_TX_X = merged_TX.loc[
    :, ["Year", "Death_per_cap", "Median_Income_2010", "Population"]
].copy()
merged_TX_X.shape

# %%
merged_TX_X.isna().sum() / len(merged_TX_X)

# %%
imputer = KNNImputer(n_neighbors=3)
imputed_TX = imputer.fit_transform(merged_TX_X)
# imputed_TX = pd.DataFrame(imputed_TX)
# tx_imputed_values = imputed_TX.iloc[:,1]

# tx_imputed_values

# %%
df_imputed_TX = pd.DataFrame(
    imputed_TX,
    columns=["Year", "Death_per_cap", "Median_Income_2010", "Population"],
    index=idx_list,
)
df_imputed_TX.isna().sum() / len(df_imputed_TX)

# %%
df_imputed_TX.head()

# %%
merged_TX_X.index = idx_list
merged_TX_X.head()

# %%
merged_TX_X["imputed_death_per_cap"] = df_imputed_TX["Death_per_cap"]
# merged_TX_X.loc[merged_TX_X["Death_per_cap"].isna()]
# merged_TX_X.set_index(idx_list, inplace=True)
merged_TX_X.head()

# %%
merged2 = merged.merge(
    merged_TX_X["imputed_death_per_cap"], how="left", left_index=True, right_index=True
)
merged2.loc[merged2["State_Code"] == "TX"]

# %%
merged_final = merged2.loc[merged2["Year"].isin(range(2003, 2016))]

# %%
import os

os.chdir("..\\pds2021-opioids-team-2-ids720\\20_intermediate_files")

# %%
merged_final.to_csv("mortality_merged_imputed.csv", encoding="utf-8", index=False)

# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%
