# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import altair as alt

deaths = pd.read_csv(
    "https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-2-ids720/data_merging/20_intermediate_files/mortality_merged_imputed.csv?token=AQKRUJCQO7IGXNJ4JDWA7C3BUENYE"
)


# %%
# Looking at States for analysis for the impact of change in policy in Florida
# We looked at trends in for all in the states in an iterative manner and check for states that had a
# similar trend for death per capita ratio overtime before the analysis.
pre_year_FL = [2003, 2004, 2005, 2006, 2007, 2008, 2009]
pre_policy_FL = deaths.loc[deaths["Year"].isin(pre_year_FL)]
deaths_state = pre_policy_FL.groupby(["State_Code", "Year"], as_index=False)[
    ["Deaths", "Population"]
].sum()
deaths_state["deaths_per_cap"] = deaths_state["Deaths"] / deaths_state["Population"]
# The states below are chosen based on the trend of deaths/capita overtime
FL_similar_state = ["FL", "MI", "NV", "SC"]
states_similar = deaths_state[deaths_state["State_Code"].isin(FL_similar_state)]


alt.Chart(states_similar).mark_line().encode(
    alt.X("Year:Q", axis=alt.Axis(format=".0f", values=pre_year_FL)),
    y="deaths_per_cap",
    color="State_Code",
).properties(
    width=500, height=500, title="Pre-policy Trend for States Similar to Florida"
)

# %%
# Looking at States for analysis for the impact of change in policy in Washington
pre_year_WA = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011]
pre_year_WA = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011]
pre_policy_WA = deaths.loc[deaths["Year"].isin(pre_year_WA)]
deaths_state = pre_policy_WA.groupby(["State_Code", "Year"], as_index=False)[
    ["Deaths", "Population"]
].sum()
deaths_state["deaths_per_cap"] = deaths_state["Deaths"] / deaths_state["Population"]
# The states below are chosen based on the trend of deaths/capita overtime
WL_similar_state = ["WA", "HI", "MT", "CO"]
states_similar = deaths_state[deaths_state["State_Code"].isin(WL_similar_state)]


alt.Chart(states_similar).mark_line().encode(
    alt.X("Year:Q", axis=alt.Axis(format=".0f", values=pre_year_WA)),
    y="deaths_per_cap",
    color="State_Code",
).properties(
    width=500, height=500, title="Pre-policy Trend for States Similar to Washington"
)


# %%
# Looking at States for analysis for the impact of change in policy in Texas
pre_year_TX = [2003, 2004, 2005, 2006, 2007]
pre_policy_TX = deaths.loc[deaths["Year"].isin(pre_year_TX)]
deaths_state = pre_policy_TX.groupby(["State_Code", "Year"], as_index=False)[
    ["Deaths", "Population"]
].sum()

deaths_state["deaths_per_cap"] = deaths_state["Deaths"] / deaths_state["Population"]
# The states below are chosen based on the trend of deaths/capita overtime
TX_similar_state = ["TX", "MO", "OR", "IL"]
states_similar = deaths_state[deaths_state["State_Code"].isin(TX_similar_state)]


alt.Chart(states_similar).mark_line().encode(
    alt.X("Year:Q", axis=alt.Axis(format=".0f", values=pre_year_TX)),
    y="deaths_per_cap",
    color="State_Code",
).properties(
    width=500, height=500, title="Pre-policy Trend for States Similar to Texas"
)


# %%
# we group by states and year as now we are only looking at states over time and not county
deaths_state = deaths.groupby(["State_Code", "Year"], as_index=False)[
    ["Deaths", "Population"]
].sum()
deaths_state["deaths_per_cap"] = deaths_state["Deaths"] / deaths_state["Population"]

# %% [markdown]
# #  Pre - Post Comparison
## Now we do not filter that data for year but rather select data for all the time

# %%
# For the change in effect of policy in Florida
years_total = [
    2003,
    2004,
    2005,
    2006,
    2007,
    2008,
    2009,
    2010,
    2011,
    2012,
    2013,
    2014,
    2015,
]
FL_similar_state = ["FL", "MI", "NV", "SC"]
states_similar_FL = deaths_state[deaths_state["State_Code"].isin(FL_similar_state)]
policy_FL = pd.DataFrame({"Year": [2010]})


chart = (
    alt.Chart(states_similar_FL)
    .mark_line()
    .encode(
        alt.X("Year", axis=alt.Axis(format=".0f", values=years_total)),
        y="deaths_per_cap",
        color="State_Code",
    )
)


rule = (
    alt.Chart(policy_FL)
    .mark_rule(color="black")
    .encode(alt.X("Year:Q", axis=alt.Axis(values=years_total)))
)


(chart + rule).properties(width=500, height=500, title="Policy Change in Florida")


# %%
# For the change in effect of policy in Washington
WA_similar_state = ["WA", "HI", "MT", "CO"]
states_similar_WA = deaths_state[deaths_state["State_Code"].isin(WA_similar_state)]
policy_WA = pd.DataFrame({"Year": [2011]})


chart = (
    alt.Chart(states_similar_WA)
    .mark_line()
    .encode(
        alt.X("Year", axis=alt.Axis(format=".0f", values=years_total)),
        y="deaths_per_cap",
        color="State_Code",
    )
)


rule = (
    alt.Chart(policy_WA)
    .mark_rule(color="black")
    .encode(alt.X("Year:Q", axis=alt.Axis(values=years_total)))
)


(chart + rule).properties(width=500, height=500, title="Policy Change in Washington")


# %%
# For the change in effect of policy in Washington
TX_similar_state = ["TX", "NY", "CA", "OR"]
states_similar_TX = deaths_state[deaths_state["State_Code"].isin(TX_similar_state)]
policy_TX = pd.DataFrame({"Year": [2007]})


chart = (
    alt.Chart(states_similar_TX)
    .mark_line()
    .encode(
        alt.X("Year", axis=alt.Axis(format=".0f", values=years_total)),
        y="deaths_per_cap",
        color="State_Code",
    )
)


rule = (
    alt.Chart(policy_TX)
    .mark_rule(color="black")
    .encode(alt.X("Year:Q", axis=alt.Axis(values=years_total)))
)


(chart + rule).properties(width=500, height=500, title="Policy Change in Texas")


# %%
