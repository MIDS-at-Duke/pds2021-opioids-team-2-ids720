import pandas as pd
import numpy as np
import os
import sklearn
from sklearn.impute import KNNImputer

os.chdir(
    "C:\\Users\\deeks\\Documents\\MIDS\\IDS 720_Practising Data Science\\Mid-Sem project\\Gitdata\\pds2021-opioids-team-2-ids720\\"
)

df = pd.read_csv("./20_intermediate_files/mortality_merged_with_pop_thresh.csv")
df.info()

# %%
df.isna().sum()

# %%
df["Death_per_cap"] = df["Deaths"] / df["Population"]


# %%
imputed_all = pd.DataFrame(
    columns=["Year", "Death_per_cap", "Median_Income_2010", "Population"]
)

for state in df["State_Code"].unique():
    state_subset = df.loc[df["State_Code"] == state]
    df_X = state_subset.loc[
        :, ["Year", "Death_per_cap", "Median_Income_2010", "Population"]
    ].copy()
    imputer = KNNImputer(n_neighbors=3)
    imputed_X = imputer.fit_transform(df_X)
    imputed_X = pd.DataFrame(imputed_X, columns=df_X.columns, index=df_X.index)
    imputed_all = pd.concat([imputed_all, imputed_X])

# %%
imputed_all.rename(columns={"Death_per_cap": "Imputed_death_per_cap"}, inplace=True)
df_merged = df.merge(
    imputed_all["Imputed_death_per_cap"], how="left", left_index=True, right_index=True
)
df_merged.head()

# %%
df_merged.to_csv(
    "./20_intermediate_files/mortality_merged_imputed.csv",
    encoding="utf-8",
    index=False,
)

# %%
