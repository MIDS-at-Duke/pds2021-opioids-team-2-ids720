# %%
import pandas as pd
import numpy as np

# %%
death = pd.read_csv(
    "https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-2-ids720/data_merging/20_intermediate_files/mortality_merged_imputed.csv?token=AVKGWH6LEJJG337L5JOAWBTBUJRFU"
)

# %%
death.head()

# %%
death.head()

# %%
states_FL=["FL","MI","NV","MO"]
df_FL = death.loc[death["State_Code"].isin(states_FL)]
df_FL.head()

# %%
states_TX=["TX","NY","IL","OR"]
df_TX = death.loc[death["State_Code"].isin(states_TX)]
df_TX.head()

# %%
states_WA=["WA","OR","HI","NY"]
df_WA = death.loc[death["State_Code"].isin(states_WA)]
df_WA.head()

# %%
df_FL_pre = df_FL[df_FL["Year"] < 2010]
df_FL_post = df_FL[df_FL["Year"] >= 2010]

df_TX_pre = df_TX[df_TX["Year"] < 2007]
df_TX_post = df_TX[df_TX["Year"] >= 2007]

df_WA_pre = df_WA[df_WA["Year"] < 2011]
df_WA_post = df_WA[df_WA["Year"] >= 2011]

# %%
pre_FL = df_FL_pre.loc[df_FL_pre["State_Code"] == "FL"]["Imputed_death_per_cap"].describe()
pre_FL_x = df_FL_pre.loc[df_FL_pre["State_Code"] != "FL"]["Imputed_death_per_cap"].describe()

pre_FL_x


# %%
df_FL_post.Death_per_cap.max()

# %%
post_FL = df_FL_post.loc[df_FL_post["State_Code"] == "FL"]["Imputed_death_per_cap"].describe()
post_FL_x = df_FL_post.loc[df_FL_post["State_Code"] != "FL"]["Imputed_death_per_cap"].describe()

post_FL

# %%
pre_WA = df_WA_pre.loc[df_WA_pre["State_Code"] == "WA"]["Imputed_death_per_cap"].describe()
pre_WA_x = df_WA_pre.loc[df_WA_pre["State_Code"] != "WA"]["Imputed_death_per_cap"].describe()

pre_WA_x

# %%
post_WA = df_WA_post.loc[df_WA_post["State_Code"] == "WA"]["Imputed_death_per_cap"].describe()
post_WA_x = df_WA_post.loc[df_WA_post["State_Code"] != "WA"]["Imputed_death_per_cap"].describe()

#post_WA
post_WA_x

# %%
pre_TX = df_TX_pre.loc[df_TX_pre["State_Code"] == "TX"]["Imputed_death_per_cap"].describe()
pre_TX_x = df_TX_pre.loc[df_TX_pre["State_Code"] != "TX"]["Imputed_death_per_cap"].describe()

pre_TX_x

# %%
post_TX = df_TX_post.loc[df_TX_post["State_Code"] == "TX"]["Imputed_death_per_cap"].describe()
post_TX_x = df_TX_post.loc[df_TX_post["State_Code"] != "TX"]["Imputed_death_per_cap"].describe()

post_TX_x

# %%


# %%



