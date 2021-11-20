# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import altair as alt

# import os

os.chdir(
    "/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/"
)

deaths = pd.read_csv(
    "20_intermediate_files/mortality_merged_imputed.csv"
)


# %%
# Looking at States for analysis for the impact of change in policy in Florida
# We looked at trends in for all in the states in an iterative manner and check for states that had a
# similar trend for death per capita ratio overtime before the analysis.
pre_year_FL = [2003, 2004, 2005, 2006, 2007, 2008, 2009]
pre_policy_FL = deaths.loc[deaths["Year"].isin(pre_year_FL)]
deaths_state = pre_policy_FL.groupby(["State_Code", "Year"], as_index=False)[
    "Imputed_death_per_cap"
].mean()

# The states below are chosen based on the trend of deaths/capita overtime
FL_similar_state = ["FL", "MI", "NV", "MO", "CA", "NY"]
states_similar = deaths_state[deaths_state["State_Code"].isin(FL_similar_state)]


alt.Chart(states_similar).mark_line().encode(
    alt.X("Year:Q", axis=alt.Axis(format=".0f", values=pre_year_FL)),
    y="Imputed_death_per_cap",
    color="State_Code",
).properties(
    width=500, height=500, title="Pre-policy Trend for States Similar to Florida in Deaths per Capita"
)

# %%
# Looking at States for analysis for the impact of change in policy in Washington
pre_year_WA = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011]
pre_policy_WA = deaths.loc[deaths["Year"].isin(pre_year_WA)]
deaths_state = pre_policy_WA.groupby(["State_Code", "Year"], as_index=False)[
    ["Imputed_death_per_cap"]
].mean()

# The states below are chosen based on the trend of deaths/capita overtime
WL_similar_state = ["WA", "HI", "OR", "NY", "CA"]
states_similar = deaths_state[deaths_state["State_Code"].isin(WL_similar_state)]


alt.Chart(states_similar).mark_line().encode(
    alt.X("Year:Q", axis=alt.Axis(format=".0f", values=pre_year_WA)),
    y="Imputed_death_per_cap",
    color="State_Code",
).properties(
    width=500, height=500, title="Pre-policy Trend for States Similar to Washington in Deaths per Capita"
)


# %%
# Looking at States for analysis for the impact of change in policy in Texas
pre_year_TX = [2003, 2004, 2005, 2006, 2007]
pre_policy_TX = deaths.loc[deaths["Year"].isin(pre_year_TX)]
deaths_state = pre_policy_TX.groupby(["State_Code", "Year"], as_index=False)[
    ["Imputed_death_per_cap"]
].mean()

# The states below are chosen based on the trend of deaths/capita overtime
TX_similar_state = ["TX", "NY", "IL", "OR", "MI", "CA"]
states_similar = deaths_state[deaths_state["State_Code"].isin(TX_similar_state)]


alt.Chart(states_similar).mark_line().encode(
    alt.X("Year:Q", axis=alt.Axis(format=".0f", values=pre_year_TX)),
    y="Imputed_death_per_cap",
    color="State_Code",
).properties(
    width=500, height=500, title="Pre-policy Trend for States Similar to Texas in Deaths per Capita"
)

