# %%
import statsmodels.formula.api as smf
import pandas as pd
import altair as alt
from altair_saver import save
import numpy as np

# %%
ship_data = pd.read_csv(
    "https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-2-ids720/data_merging/20_intermediate_files/merged_pop_and_ship_and_fips.csv?token=AVJP5IQYBK2OXVDZ53EK7N3BUKQ7Y"
)
ship_data["Ships_per_cap"] = ship_data["MME"] / ship_data["Population"]

# %%
ship_data_FL = ship_data.loc[
    ship_data["BUYER_STATE"] == "FL",
    ["Year", "State_Code", "Median_Income_2010", "Ships_per_cap", "Population"],
]
ship_data_WA = ship_data.loc[
    ship_data["BUYER_STATE"] == "WA",
    ["Year", "State_Code", "Median_Income_2010", "Ships_per_cap", "Population"],
]
ship_data_TX = ship_data.loc[
    ship_data["BUYER_STATE"] == "TX",
    ["Year", "State_Code", "Median_Income_2010", "Ships_per_cap", "Population"],
]

# %%
# %%
average_income_FL = float(ship_data_FL["Median_Income_2010"].mean())
average_income_WA = float(ship_data_WA["Median_Income_2010"].mean())
average_income_TX = float(ship_data_TX["Median_Income_2010"].mean())

# %%
ship_data_FL["Income_Indicator"] = "High Income"
ship_data_WA["Income_Indicator"] = "High Income"
ship_data_TX["Income_Indicator"] = "High Income"
ship_data_FL.loc[
    ship_data_FL["Median_Income_2010"] < average_income_FL, "Income_Indicator"
] = "Low Income"
ship_data_WA.loc[
    ship_data_WA["Median_Income_2010"] < average_income_WA, "Income_Indicator"
] = "Low Income"
ship_data_TX.loc[
    ship_data_TX["Median_Income_2010"] < average_income_TX, "Income_Indicator"
] = "Low Income"

# %%
ship_data_FL_pre = ship_data_FL.loc[ship_data_FL["Year"] < 2010]
ship_data_FL_post = ship_data_FL.loc[ship_data_FL["Year"] >= 2010]

# %%
FL_pre_high = ship_data_FL_pre.loc[
    ship_data_FL_pre["Income_Indicator"] == "High Income"
]
FL_post_high = ship_data_FL_post.loc[
    ship_data_FL_post["Income_Indicator"] == "High Income"
]
FL_pre_low = ship_data_FL_pre.loc[ship_data_FL_pre["Income_Indicator"] == "Low Income"]
FL_post_low = ship_data_FL_post.loc[
    ship_data_FL_post["Income_Indicator"] == "Low Income"
]


# %%
def get_reg_fit(data, color, yvar, xvar, legend, alpha=0.05):
    colour = color
    years = list(np.arange(2003, 2016, 1))

    # Grid for predicted values
    x = data.loc[pd.notnull(data[yvar]), xvar]
    xmin = x.min()
    xmax = x.max()
    step = (xmax - xmin) / 100
    grid = np.arange(xmin, xmax + step, step)
    predictions = pd.DataFrame({xvar: grid})

    # Fit model, get predictions
    model = smf.ols(f"{yvar} ~ {xvar}", data=data).fit()
    model_predict = model.get_prediction(predictions[xvar])
    predictions[yvar] = model_predict.summary_frame()["mean"]
    predictions[["ci_low", "ci_high"]] = model_predict.conf_int(alpha=alpha)

    # Build chart
    predictions["Income_Indicator"] = f"{legend}"
    reg = (
        alt.Chart(predictions)
        .mark_line()
        .encode(
            x=xvar,
            y=alt.Y(yvar),
            color=alt.value(f"{colour}"),
            
        )
    )
    ci = (
        alt.Chart(predictions)
        .mark_errorband()
        .encode(
            alt.X(f"{xvar}:Q", axis=alt.Axis(format=".0f", values=years)),
            y=alt.Y(
                "ci_low",
                title="Shipments per Capita in Milligrams",
                scale=alt.Scale(zero=False),
            ),
            y2="ci_high",
            color=alt.value(f"{color}"),
        )
    )

    chart = ci + reg
    return predictions, chart

# %%
# %%
def plotting_chart(policy_year, color, data, yvar, xvar, legend, alpha=0.05):
    pl_year = policy_year
    pol_year = []
    pol_year.append(int(pl_year))

    years = list(np.arange(2003, 2016, 1))

    # Plotting chart
    fit, reg_chart = get_reg_fit(
        color=color, data=data, yvar=yvar, xvar=xvar, legend=legend, alpha=alpha
    )

    policy = pd.DataFrame({"Year": pol_year})

    rule = (
        alt.Chart(policy)
        .mark_rule(color="black")
        .encode(alt.X("Year:Q", title="Year", axis=alt.Axis(values=years)))
    )
    return (reg_chart + rule).properties(width=500, height=500)

# %%
plot_FL_high_pre = plotting_chart(
    2010,
    "blue",
    FL_pre_high,
    "Ships_per_cap",
    "Year",
    legend="High Income",
    alpha=0.05,
)
plot_FL_high_post = plotting_chart(
    2010,
    "blue",
    FL_post_high,
    "Ships_per_cap",
    "Year",
    legend="High Income",
    alpha=0.05,
)

plot_FL_low_post = plotting_chart(
    2010, "#9467bd", FL_post_low, "Ships_per_cap", "Year", legend="Low Income", alpha=0.05
)

plot_FL_low_pre = plotting_chart(
    2010,
    "#9467bd",
    FL_pre_low,
    "Ships_per_cap",
    "Year",
    legend="Low Income",
    alpha=0.05,
)

final = plot_FL_high_pre + plot_FL_low_pre + plot_FL_high_post + plot_FL_low_post
final.properties(
    title="Analysis of Shipments per capita for High Income vs Low Income Counties in Florida"
)

# %%
death_data = pd.read_csv(
    "https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-2-ids720/data_merging/20_intermediate_files/mortality_merged_imputed.csv?token=AVJP5IXEPC23XQSQGCBUOF3BUKGRM"
)


# %%
death_data_FL = death_data.loc[
    death_data["State_Code"].isin(["FL"]),
    ["State_Code", "County_Name", "Year", "Imputed_death_per_cap", "Median_Income_2010"],
]

death_data_WA = death_data.loc[
    death_data["State_Code"].isin(["WA"]),
    ["State_Code", "County_Name", "Year", "Imputed_death_per_cap", "Median_Income_2010"],
]

death_data_TX = death_data.loc[
    death_data["State_Code"].isin(["TX"]),
    ["State_Code", "County_Name", "Year", "Imputed_death_per_cap", "Median_Income_2010"],
]

# %%
death_data_FL["Income_Indicator"] = "High Income"
death_data_WA["Income_Indicator"] = "High Income"
death_data_TX["Income_Indicator"] = "High Income"

death_data_FL.loc[
    death_data_FL["Median_Income_2010"] < average_income_FL, "Income_Indicator"
] = "Low Income"

death_data_WA.loc[
    death_data_WA["Median_Income_2010"] < average_income_WA, "Income_Indicator"
] = "Low Income"

death_data_TX.loc[
    death_data_TX["Median_Income_2010"] < average_income_TX, "Income_Indicator"
] = "Low Income"

# %%
# %%
death_data_FL_pre = death_data_FL.loc[death_data_FL["Year"] < 2010]
death_data_FL_post = death_data_FL.loc[death_data_FL["Year"] >= 2010]


death_data_WA_pre = death_data_WA.loc[death_data_WA["Year"] < 2011]
death_data_WA_post = death_data_WA.loc[death_data_WA["Year"] >= 2011]


death_data_TX_pre = death_data_TX.loc[death_data_TX["Year"] < 2007]
death_data_TX_post = death_data_TX.loc[death_data_TX["Year"] >= 2007]

# %%
# %%
WA_pre_high = death_data_WA_pre.loc[
    death_data_WA_pre["Income_Indicator"] == "High Income"
]
WA_post_high = death_data_WA_post.loc[
    death_data_WA_post["Income_Indicator"] == "High Income"
]
WA_pre_low = death_data_WA_pre.loc[
    death_data_WA_pre["Income_Indicator"] == "Low Income"
]
WA_post_low = death_data_WA_post.loc[
    death_data_WA_post["Income_Indicator"] == "Low Income"
]

# %%
TX_pre_high = death_data_TX_pre.loc[
    death_data_TX_pre["Income_Indicator"] == "High Income"
]
TX_post_high = death_data_TX_post.loc[
    death_data_TX_post["Income_Indicator"] == "High Income"
]
TX_pre_low = death_data_TX_pre.loc[
    death_data_TX_pre["Income_Indicator"] == "Low Income"
]
TX_post_low = death_data_TX_post.loc[
    death_data_TX_post["Income_Indicator"] == "Low Income"
]

# %%
FL_pre_high = death_data_FL_pre.loc[
    death_data_FL_pre["Income_Indicator"] == "High Income"
]
FL_post_high = death_data_FL_post.loc[
    death_data_FL_post["Income_Indicator"] == "High Income"
]
FL_pre_low = death_data_FL_pre.loc[
    death_data_FL_pre["Income_Indicator"] == "Low Income"
]
FL_post_low = death_data_FL_post.loc[
    death_data_FL_post["Income_Indicator"] == "Low Income"
]

# %%
def get_reg_fit(data, color, yvar, xvar, legend, alpha=0.05):
    colour = color
    years = list(np.arange(2003, 2016, 1))

    # Grid for predicted values
    x = data.loc[pd.notnull(data[yvar]), xvar]
    xmin = x.min()
    xmax = x.max()
    step = (xmax - xmin) / 100
    grid = np.arange(xmin, xmax + step, step)
    predictions = pd.DataFrame({xvar: grid})

    # Fit model, get predictions
    model = smf.ols(f"{yvar} ~ {xvar}", data=data).fit()
    model_predict = model.get_prediction(predictions[xvar])
    predictions[yvar] = model_predict.summary_frame()["mean"]
    predictions[["ci_low", "ci_high"]] = model_predict.conf_int(alpha=alpha)

    # Build chart
    predictions["Income_Indicator"] = f"{legend}"
    reg = (
        alt.Chart(predictions)
        .mark_line()
        .encode(
            x=xvar,
            y=alt.Y(yvar, axis=alt.Axis(format="%")),
            color=alt.value(f"{colour}"),
            
        )
    )
    ci = (
        alt.Chart(predictions)
        .mark_errorband()
        .encode(
            alt.X(f"{xvar}:Q", axis=alt.Axis(format=".0f", values=years)),
            y=alt.Y(
                "ci_low",
                title="Mortality Rate due to Opioid Overdose (by County)",
                scale=alt.Scale(zero=False),
            ),
            y2="ci_high",
            color=alt.value(f"{color}"),
        )
    )

    chart = ci + reg
    return predictions, chart

# %%
# %%
def plotting_chart(policy_year, color, data, yvar, xvar, legend, alpha=0.05):
    pl_year = policy_year
    pol_year = []
    pol_year.append(int(pl_year))

    years = list(np.arange(2003, 2016, 1))

    # Plotting chart
    fit, reg_chart = get_reg_fit(
        color=color, data=data, yvar=yvar, xvar=xvar, legend=legend, alpha=alpha
    )

    policy = pd.DataFrame({"Year": pol_year})

    rule = (
        alt.Chart(policy)
        .mark_rule(color="black")
        .encode(alt.X("Year:Q", title="Year", axis=alt.Axis(values=years)))
    )
    return (reg_chart + rule).properties(width=500, height=500)

# %%
plot_FL_low_pre = plotting_chart(
    2010,
    "#9467bd",
    FL_pre_low,
    "Imputed_death_per_cap",
    "Year",
    legend="Low Income",
    alpha=0.05,
)
plot_FL_high_pre = plotting_chart(
    2010,
    "blue",
    FL_pre_high,
    "Imputed_death_per_cap",
    "Year",
    legend="High Income",
    alpha=0.05,
)
plot_FL_low_post = plotting_chart(
    2010,
    "#9467bd",
    FL_post_low,
    "Imputed_death_per_cap",
    "Year",
    legend="Low Income",
    alpha=0.05,
)
plot_FL_high_post = plotting_chart(
    2010,
    "blue",
    FL_post_high,
    "Imputed_death_per_cap",
    "Year",
    legend="High Income",
    alpha=0.05,
)

final = plot_FL_high_pre + plot_FL_low_pre + plot_FL_high_post + plot_FL_low_post
final.properties(
    title="Analysis of Opioid Regulations on Mortality for High Income vs Low Income Counties in Florida "
)

# %%
# %%
plot_WA_low_pre = plotting_chart(
    2011,
    "#B46A7B",
    WA_pre_low,
    "Imputed_death_per_cap",
    "Year",
    legend="Low Income",
    alpha=0.05,
)
plot_WA_high_pre = plotting_chart(
    2011,
    "maroon",
    WA_pre_high,
    "Imputed_death_per_cap",
    "Year",
    legend="High Income",
    alpha=0.05,
)
plot_WA_low_post = plotting_chart(
    2011,
    "#B46A7B",
    WA_post_low,
    "Imputed_death_per_cap",
    "Year",
    legend="Low Income",
    alpha=0.05,
)
plot_WA_high_post = plotting_chart(
    2011,
    "maroon",
    WA_post_high,
    "Imputed_death_per_cap",
    "Year",
    legend="High Income",
    alpha=0.05,
)

final = plot_WA_high_pre + plot_WA_low_pre + plot_WA_high_post + plot_WA_low_post
final.properties(
    title="Analysis of Opioid Regulations on Mortality for High Income vs Low Income Counties in Washington "
)


# %%
# %%
plot_TX_low_pre = plotting_chart(
    2007,
    "#F8B74F",
    TX_pre_low,
    "Imputed_death_per_cap",
    "Year",
    legend="Low Income",
    alpha=0.05,
)
plot_TX_high_pre = plotting_chart(
    2007,
    "orange",
    TX_pre_high,
    "Imputed_death_per_cap",
    "Year",
    legend="High Income",
    alpha=0.05,
)
plot_TX_low_post = plotting_chart(
    2007,
    "#F8B74F",
    TX_post_low,
    "Imputed_death_per_cap",
    "Year",
    legend="Low Income",
    alpha=0.05,
)
plot_TX_high_post = plotting_chart(
    2007,
    "orange",
    TX_post_high,
    "Imputed_death_per_cap",
    "Year",
    legend="High Income",
    alpha=0.05,
)

final = plot_TX_high_pre + plot_TX_low_pre + plot_TX_high_post + plot_TX_low_post
final.properties(
    title="Analysis of Opioid Regulations on Mortality for High Income vs Low Income Counties in Texas "
)


