import pandas as pd

pd.set_option("display.max_rows", 100, "display.max_columns", 100)

# %%
raw_df = pd.read_csv(
    "https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-2-ids720/data_merging/00_source_data/Income_data/nhgis0001_ds176_20105_county.csv?token=AQKRUJEOS2B57PNPA2NP4BDBR3MQW",
    encoding="ISO8859-1",
)
raw_df.head()

# %%
keepcols = ["YEAR", "STATE", "STATEA", "COUNTY", "COUNTYA", "JOIE001", "JOIM001"]
raw_df = raw_df.loc[:, raw_df.columns.isin(keepcols)]
raw_df.rename(
    {"JOIE001": "Median_Income_2010", "JOIM001": "Income_Error_Margin"},
    axis=1,
    inplace=True,
)


# %%
# Reading in population data file
popn = pd.read_csv(
    "https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-2-ids720/data_merging/20_intermediate_files/population_2000_2020.csv?token=AQKRUJFLWW77HNRD3MYDCXTBR3MUS"
)
popn.head()

popn["STATE"] = popn["STATE"].astype(str)
popn["COUNTY"] = popn["COUNTY"].astype(str)

for i, row in popn.iterrows():
    if len(row["STATE"]) < 2:
        popn.at[i, "STATE"] = '0' + row["STATE"]
        pass
    if len(row["COUNTY"]) == 1:
        popn.at[i, "COUNTY"] = '00' + row["COUNTY"]
        pass
    elif len(row["COUNTY"]) == 2:
        popn.at[i, "COUNTY"] = '0' + row["COUNTY"]
        pass
    else:
        pass
    pass

popn["fips_code"] = popn["STATE"] + popn["COUNTY"]

# QC
# population["fips_code"].apply(lambda x: len(x) == 5).all()


# %%
merged = (
    popn.merge(
        raw_df[["STATE", "COUNTY", "Median_Income_2010", "Income_Error_Margin"]],
        how="left",
        left_on=["STNAME", "CTYNAME"],
        right_on=["STATE", "COUNTY"],
    )
    .drop(columns=["STATE_y", "COUNTY_y"])
    .rename({"STATE_x": "STATE", "COUNTY_x": "COUNTY"}, axis=1)
)
merged.to_csv(
    "C:\\Users\\deeks\\Documents\\MIDS\\IDS 720_Practising Data Science\\Mid-Sem project\\Gitdata\\pds2021-opioids-team-2-ids720\\20_intermediate_files\\population_2000_2020_inc.csv",
    index=False,
)
