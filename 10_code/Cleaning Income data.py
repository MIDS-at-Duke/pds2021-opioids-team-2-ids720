import pandas as pd

pd.set_option("display.max_rows", 100, "display.max_columns", 100)

# %%
raw_df = pd.read_csv(
    "C:\\Users\\deeks\\Documents\\MIDS\\IDS 720_Practising Data Science\\Datasets\\nhgis0001_csv\\nhgis0001_csv\\nhgis0001_ds176_20105_county.csv",
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
    "C:\\Users\\deeks\\Documents\\MIDS\\IDS 720_Practising Data Science\\Mid-Sem project\\Gitdata\\pds2021-opioids-team-2-ids720\\20_intermediate_files\\population_2000_2020.csv"
)
popn.head()

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
