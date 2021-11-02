# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"


# %%
import pandas as pd
import numpy as np

pd.set_option("display.max_rows", 200, "display.max_columns", 200)

# %% [markdown]
# Reading in the population files - (i) 2000 - 2009 (ii) 2010 - 2020

# %%
raw_pre_2010 = pd.read_csv(
    "C:\\Users\\deeks\\Documents\\MIDS\\IDS 720_Practising Data Science\\Mid-Sem project\\Gitdata\\pds2021-opioids-team-2-ids720\\00_source_data\\population_data\\2000 - 2010.csv",
    encoding="ISO8859-1",
)
raw_post_2010 = pd.read_csv(
    "C:\\Users\\deeks\\Documents\\MIDS\\IDS 720_Practising Data Science\\Mid-Sem project\\Gitdata\\pds2021-opioids-team-2-ids720\\00_source_data\\population_data\\2010 - 2020.csv",
    encoding="ISO8859-1",
)


# %%
raw_pre_2010.head()


# %%
raw_post_2010.head()


# %%
# raw_post_2010.iloc[:,0:20].columns


# %%
keepcols_pre = [
    "STATE",
    "COUNTY",
    "STNAME",
    "CTYNAME",
    "CENSUS2000POP",
    "POPESTIMATE2001",
    "POPESTIMATE2002",
    "POPESTIMATE2003",
    "POPESTIMATE2004",
    "POPESTIMATE2005",
    "POPESTIMATE2006",
    "POPESTIMATE2007",
    "POPESTIMATE2008",
    "POPESTIMATE2009",
]

keepcols_post = [
    "STATE",
    "COUNTY",
    "STNAME",
    "CTYNAME",
    "CENSUS2010POP",
    "POPESTIMATE2011",
    "POPESTIMATE2012",
    "POPESTIMATE2013",
    "POPESTIMATE2014",
    "POPESTIMATE2015",
    "POPESTIMATE2016",
    "POPESTIMATE2017",
    "POPESTIMATE2018",
    "POPESTIMATE2019",
    "POPESTIMATE2020",
]

raw_pre_2010 = raw_pre_2010.loc[:, raw_pre_2010.columns.isin(keepcols_pre)]
raw_post_2010 = raw_post_2010.loc[:, raw_post_2010.columns.isin(keepcols_post)]


# %%
raw_pre_2010.shape
raw_post_2010.shape


# %%
raw_popn_merged = raw_pre_2010.merge(
    raw_post_2010,
    on=["STATE", "COUNTY", "STNAME", "CTYNAME"],
    how="left",
    validate="1:1",
)
raw_popn_merged.head()


# %%
raw_popn_merged = raw_popn_merged.loc[
    raw_popn_merged["STNAME"] != raw_popn_merged["CTYNAME"]
]
raw_popn_merged.shape


# %%
raw_popn_merged = raw_popn_merged.loc[raw_popn_merged["STNAME"] != "Alaska"]
raw_popn_merged.shape


# %%
# keep_states = ["Florida","Texas","Washington","Maryland","Delaware","New York"]


# %%
raw_popn_merged.info()


# %%
(raw_popn_merged.isna().sum() / len(raw_popn_merged)).apply(
    lambda x: "{:.2%}".format(x)
)


# %%
raw_popn_merged.loc[raw_popn_merged["CENSUS2010POP"].isnull()]


# %%
raw_popn_merged.rename(
    {
        "CENSUS2000POP": "2000",
        "POPESTIMATE2001": "2001",
        "POPESTIMATE2002": "2002",
        "POPESTIMATE2003": "2003",
        "POPESTIMATE2004": "2004",
        "POPESTIMATE2005": "2005",
        "POPESTIMATE2006": "2006",
        "POPESTIMATE2007": "2007",
        "POPESTIMATE2008": "2008",
        "POPESTIMATE2009": "2009",
        "CENSUS2010POP": "2010",
        "POPESTIMATE2011": "2011",
        "POPESTIMATE2012": "2012",
        "POPESTIMATE2013": "2013",
        "POPESTIMATE2014": "2014",
        "POPESTIMATE2015": "2015",
        "POPESTIMATE2016": "2016",
        "POPESTIMATE2017": "2017",
        "POPESTIMATE2018": "2018",
        "POPESTIMATE2019": "2019",
        "POPESTIMATE2020": "2020",
    },
    axis=1,
    inplace=True,
)


# %%
raw_popn_merged.head()


# %%
raw_popn_merged_melted = pd.melt(
    raw_popn_merged,
    id_vars=["STATE", "COUNTY", "STNAME", "CTYNAME"],
    value_vars=[
        "2000",
        "2001",
        "2002",
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
    ],
    var_name="Year",
    value_name="Population",
)
raw_popn_merged_melted.head()


# %%
raw_popn_merged_melted.isna().sum()


# %%
raw_popn_merged_melted["Population"] = np.where(
    raw_popn_merged_melted["Population"] == "X",
    np.nan,
    raw_popn_merged_melted["Population"],
)


# %%
raw_popn_merged_melted.info()


# %%
# Converting dtype of population from object to float
raw_popn_merged_melted["Population"] = pd.to_numeric(
    raw_popn_merged_melted["Population"], errors="coerce"
)
raw_popn_merged_melted.info()

# Fetching state codes
# %%
import requests

response = requests.get(
    "https://gist.githubusercontent.com/mshafrir/2646763/raw/8b0dbb93521f5d6889502305335104218454c2bf/states_hash.json"
)
state_abbrevs = {v: k for k, v in response.json().items()}
state_abbrevs


# %%
raw_popn_merged_melted["State_Code"] = raw_popn_merged_melted["STNAME"].map(
    state_abbrevs
)
raw_popn_merged_melted.head()


# %%
# Checking average population counts for states
# raw_popn_merged_melted.groupby(["STNAME"]).mean("Population").sort_values(by = "Population",ascending=False)

# Writing cleaned population file
# %%
raw_popn_merged_melted.to_csv(
    "C:\\Users\\deeks\\Documents\\MIDS\\IDS 720_Practising Data Science\\Mid-Sem project\\Gitdata\\pds2021-opioids-team-2-ids720\\20_intermediate_files\\population_2000_2020.csv"
)
