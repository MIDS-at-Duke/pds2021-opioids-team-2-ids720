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
df_X = df.loc[:, ["Year", "Deaths", "Median_Income_2010", "Population"]].copy()
df_X.shape

# %%
df_X.isna().sum() / len(df_X)

# %%
imputer = KNNImputer(n_neighbors=3)
imputed_X = imputer.fit_transform(df_X)
# imputed_TX = pd.DataFrame(imputed_TX)
# tx_imputed_values = imputed_TX.iloc[:,1]

# tx_imputed_values

# %%
df_imputed_X = pd.DataFrame(
    imputed_X,
    columns=["Year", "Deaths", "Median_Income_2010", "Population"],
    # index=idx_list,
)
df_imputed_X.isna().sum() / len(df_imputed_X)

# %%
df_imputed_X.head()

# %%


# %%
df["imputed_deaths"] = df_imputed_X["Deaths"]
# merged_TX_X.loc[merged_TX_X["Death_per_cap"].isna()]
# merged_TX_X.set_index(idx_list, inplace=True)
df.head()

# %%
mortality = df.groupby(
    ["Year", "State_Code", "County_Name", "Population", "Median_Income_2010"],
    as_index=False,
)["imputed_deaths"].apply(lambda x: x.sum())
mortality.head()

# %%
mortality["Death_per_cap"] = mortality["imputed_deaths"] / mortality["Population"]

# %%
mortality.to_csv(
    "./20_intermediate_files/mortality_merged_imputed.csv",
    encoding="utf-8",
    index=False,
)

# %%
