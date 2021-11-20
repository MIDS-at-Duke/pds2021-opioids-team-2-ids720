# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import statsmodels.formula.api as smf
import pandas as pd
import altair as alt
import numpy as np
from altair_saver import save
import selenium


# %%
# loading data and filtering for Florida
death_data = pd.read_csv(
    "https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-2-ids720/data_merging/20_intermediate_files/mortality_merged_imputed.csv?token=AVJP5IVA7C3KXGR7JBCKH3DBUJSNI"
)

# death_data["Death_per_cap"] = np.where(death_data["Death_per_cap"].notna(), death_data["Death_per_cap"],death_data["imputed_death_per_cap"])

death_FL = death_data.loc[
    death_data["State_Code"] == "FL", ["Year", "County_Name", "Imputed_death_per_cap"]
]


# %%
# death_FL["Death_per_cap"] = death_FL["Death_per_cap"].apply(lambda x:({:.4%}.format(x)))
# death_FL.head()


# %%
# check for death rate between 0 and 1
print(min(death_FL["Imputed_death_per_cap"]))
print(max(death_FL["Imputed_death_per_cap"]))

# check for missing values in death rate
print(death_FL["Imputed_death_per_cap"].isna().any())


# %%
# filter out for year pre and post
death_FL_pre = death_FL[death_FL["Year"] < 2010]
death_FL_post = death_FL[death_FL["Year"] >= 2010]


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
    predictions["Treat"] = f"{legend}"
    reg = (
        alt.Chart(predictions)
        .mark_line()
        .encode(
            x=xvar,
            y=alt.Y(yvar, axis=alt.Axis(format="%")),
            color=alt.value(f"{colour}"),
            opacity=alt.Opacity("Treat", legend=alt.Legend(title="Legend")),
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
pre_fl = plotting_chart(
    2010, "blue", death_FL_pre, "Imputed_death_per_cap", "Year", legend="Florida", alpha=0.05
)
post_fl = plotting_chart(
    2010, "blue", death_FL_post, "Imputed_death_per_cap", "Year", legend="Florida", alpha=0.05
)

final = pre_fl + post_fl

final.properties(
    title="Pre-Post Analysis of Opioid Regulations on Mortality for Florida"
)





# %%
death_WA = death_data.loc[
    death_data["State_Code"] == "WA", ["Year", "County_Name", "Imputed_death_per_cap"]
]
# filter out for year pre and post
death_WA_pre = death_WA[death_WA["Year"] < 2011]
death_WA_post = death_WA[death_WA["Year"] >= 2011]


# %%
pre_wa = plotting_chart(
    2011, "maroon", death_WA_pre, "Imputed_death_per_cap", "Year", "Washington", alpha=0.05
)
post_wa = plotting_chart(
    2011, "maroon", death_WA_post, "Imputed_death_per_cap", "Year", "Washington", alpha=0.05
)

final = pre_wa + post_wa

final.properties(
    title="Pre-Post Analysis of Opioid Regulations on Mortality for Washington"
)


# %%
death_TX = death_data.loc[
    death_data["State_Code"] == "TX", ["Year", "County_Name", "Imputed_death_per_cap"]
]
# filter out for year pre and post
death_TX_pre = death_TX[death_TX["Year"] < 2007]
death_TX_post = death_TX[death_TX["Year"] >= 2007]


# %%
pre_TX = plotting_chart(
    2007, "green", death_TX_pre, "Imputed_death_per_cap", "Year", "Texas", alpha=0.05
)
post_TX = plotting_chart(
    2007, "green", death_TX_post, "Imputed_death_per_cap", "Year", "Texas", alpha=0.05
)

final = pre_TX + post_TX

final.properties(title="Pre-Post Analysis of Opioid Regulations on Mortality for Texas")


# %%
diff_FL_data = death_data.loc[
    death_data["State_Code"].isin(["FL", "MI", "NV", "MO"])
].copy()
diff_FL_data["Treat"] = 1
diff_FL_data.loc[diff_FL_data["State_Code"].isin(["MI", "NV", "MO"]), "Treat"] = 0


# %%
diff_FL_treat = diff_FL_data.loc[diff_FL_data["Treat"] == 1]
diff_FL_control = diff_FL_data.loc[diff_FL_data["Treat"] == 0]


# %%
diff_FL_treat_pre = diff_FL_treat.loc[diff_FL_treat["Year"] < 2010]
diff_FL_treat_post = diff_FL_treat.loc[diff_FL_treat["Year"] >= 2010]
diff_FL_control_pre = diff_FL_control.loc[diff_FL_control["Year"] < 2010]
diff_FL_control_post = diff_FL_control.loc[diff_FL_control["Year"] >= 2010]


# %%
pre_FL = plotting_chart(
    2010, "blue", diff_FL_treat_pre, "Imputed_death_per_cap", "Year", "Florida", alpha=0.05
)
post_FL = plotting_chart(
    2010, "blue", diff_FL_treat_post, "Imputed_death_per_cap", "Year", "Florida", alpha=0.05
)
pre_control = plotting_chart(
    2010,
    "#9467bd",
    diff_FL_control_pre,
    "Death_per_cap",
    "Year",
    "Comparison States - MI, NV, MO",
    alpha=0.05,
)
post_control = plotting_chart(
    2010,
    "#9467bd",
    diff_FL_control_post,
    "Death_per_cap",
    "Year",
    "Comparison States - MI, NV, MO",
    alpha=0.05,
)


final = pre_FL + post_FL + pre_control + post_control
final.properties(
    title="Diff in Diff Analysis of Opioid Regulations on Mortality for Florida vs Comparison States"
)


# %%
diff_TX_data = death_data.loc[
    death_data["State_Code"].isin(["TX", "NY", "IL", "OR"])
].copy()
diff_TX_data["Treat"] = 1
diff_TX_data.loc[diff_TX_data["State_Code"].isin(["IL", "NY", "OR"]), "Treat"] = 0

diff_TX_treat = diff_TX_data.loc[diff_TX_data["Treat"] == 1]
diff_TX_control = diff_TX_data.loc[diff_TX_data["Treat"] == 0]

diff_TX_treat_pre = diff_TX_treat.loc[diff_TX_treat["Year"] < 2007]
diff_TX_treat_post = diff_TX_treat.loc[diff_TX_treat["Year"].isin(range(2007, 2014))]
diff_TX_control_pre = diff_TX_control.loc[diff_TX_control["Year"] < 2007]
diff_TX_control_post = diff_TX_control.loc[
    diff_TX_control["Year"].isin(range(2007, 2014))
]

pre_TX = plotting_chart(
    2007, "orange", diff_TX_treat_pre, "Imputed_death_per_cap", "Year", "Texas", alpha=0.05
)
post_TX = plotting_chart(
    2007, "orange", diff_TX_treat_post, "Imputed_death_per_cap", "Year", "Texas", alpha=0.05
)
pre_control = plotting_chart(
    2007,
    "#F8B74F",
    diff_TX_control_pre,
    "Death_per_cap",
    "Year",
    "Comparison States - IL, NY, OR",
    alpha=0.05,
)
post_control = plotting_chart(
    2007,
    "#F8B74F",
    diff_TX_control_post,
    "Death_per_cap",
    "Year",
    "Comparison States - IL, NY, OR",
    alpha=0.05,
)


final = pre_TX + post_TX + pre_control + post_control
final.properties(
    title="Diff in Diff Analysis of Opioid Regulations on Mortality for Texas vs Comparison States"
)


# %%
diff_WA_data = death_data.loc[
    death_data["State_Code"].isin(["WA", "HI", "OR", "NY"])
].copy()
diff_WA_data["Treat"] = 1
diff_WA_data.loc[diff_WA_data["State_Code"].isin(["HI", "NY", "OR"]), "Treat"] = 0

diff_WA_treat = diff_WA_data.loc[diff_WA_data["Treat"] == 1]
diff_WA_control = diff_WA_data.loc[diff_WA_data["Treat"] == 0]

diff_WA_treat_pre = diff_WA_treat.loc[diff_WA_treat["Year"] < 2011]
diff_WA_treat_post = diff_WA_treat.loc[diff_WA_treat["Year"] >= 2011]
diff_WA_control_pre = diff_WA_control.loc[diff_WA_control["Year"] < 2011]
diff_WA_control_post = diff_WA_control.loc[diff_WA_control["Year"] >= 2011]

pre_WA = plotting_chart(
    2011, "maroon", diff_WA_treat_pre, "Imputed_death_per_cap", "Year", "Washington", alpha=0.05
)
post_WA = plotting_chart(
    2011, "maroon", diff_WA_treat_post, "Imputed_death_per_cap", "Year", "Washington", alpha=0.05
)
pre_control = plotting_chart(
    2011,
    "#B46A7B",
    diff_WA_control_pre,
    "Death_per_cap",
    "Year",
    "Comparison States - HI, NY, OR",
    alpha=0.05,
)
post_control = plotting_chart(
    2011,
    "#B46A7B",
    diff_WA_control_post,
    "Death_per_cap",
    "Year",
    "Comparison States - HI, NY, OR",
    alpha=0.05,
)


final = pre_WA + post_WA + pre_control + post_control
final.properties(
    title="Diff in Diff Analysis of Opioid Regulations on Mortality for Washington vs Comparison States"
)

# %%
