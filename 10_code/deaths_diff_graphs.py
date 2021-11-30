# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import statsmodels.formula.api as smf
import pandas as pd 
import altair as alt
import numpy as np


# %%
# loading data and filtering for Florida
death_data = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-2-ids720/data_merging/20_intermediate_files/mortality_merged.csv?token=AVJP5IXOCXKCDAV4T73OUJLBTVNLU')

death_FL = death_data.loc[death_data['State_Code']=='FL', ['Year','County_Name','Death_per_cap']]


# %%
# check for death rate between 0 and 1
print(min(death_FL['Death_per_cap']))
print(max(death_FL['Death_per_cap']))

# check for missing values in death rate
print(death_FL['Death_per_cap'].isna().any())


# %%
# filter out for year pre and post
death_FL_pre = death_FL[death_FL['Year'] < 2010]
death_FL_post = death_FL[death_FL['Year'] >= 2010]




# %%
def get_reg_fit(data, color, yvar, xvar, legend, alpha=0.05):
    colour= color
    years = list(np.arange(2003, 2016,1))

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
    predictions['Treat'] = f"{legend}"
    reg = alt.Chart(predictions).mark_line().encode(x=xvar, y=alt.Y(yvar, axis=alt.Axis(format='%')), color = alt.value(f"{colour}"), opacity=alt.Opacity("Treat", legend=alt.Legend(title="Legend")))
    ci = (
        alt.Chart(predictions)
        .mark_errorband()
        .encode(
            alt.X(f"{xvar}:Q", axis=alt.Axis(format='.0f', values=years)),
            y=alt.Y("ci_low", title="Mortality Rate due to Opioid Overdose (by County)", scale=alt.Scale(zero=False)),
            y2="ci_high",
            color=alt.value(f"{color}")
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
    fit, reg_chart = get_reg_fit(color=color, data= data, yvar=yvar, xvar=xvar, legend=legend, alpha=alpha)

    policy = pd.DataFrame({"Year": pol_year})

    rule = (
        alt.Chart(policy)
        .mark_rule(color="black")
        .encode(alt.X("Year:Q", title ="Year",axis=alt.Axis(values=years)))
    )
    return (reg_chart + rule).properties(width=500, height=500)


# %%
pre_fl = plotting_chart(2010, 'blue', death_FL_pre, 'Death_per_cap', 'Year', alpha=0.05)
post_fl = plotting_chart(2010, 'blue', death_FL_post, 'Death_per_cap', 'Year', alpha=0.05)

final = (pre_fl + post_fl)

final.properties(title = "Pre-Post Analysis of Opioid Regulations for Florida")


# %%
death_WA = death_data.loc[death_data['State_Code']=='WA', ['Year','County_Name','Death_per_cap']]
# filter out for year pre and post
death_WA_pre = death_WA[death_WA['Year'] < 2011]
death_TX_post = death_WA[death_WA['Year'] >= 2011]


# %%
pre_wa = plotting_chart(2011, 'blue', death_WA_pre, 'Death_per_cap', 'Year', alpha=0.05)
post_wa = plotting_chart(2011, 'blue', death_WA_post, 'Death_per_cap', 'Year', alpha=0.05)

final = (pre_wa + post_wa)

final.properties(title = "Pre-Post Analysis of Opioid Regulations for Washington")


# %%
death_TX = death_data.loc[death_data['State_Code']=='TX', ['Year','County_Name','Death_per_cap']]
# filter out for year pre and post
death_TX_pre = death_TX[death_TX['Year'] < 2007]
death_TX_post = death_TX[death_TX['Year'] >= 2007]


# %%
pre_TX = plotting_chart(2007, 'blue', death_TX_pre, 'Death_per_cap', 'Year', alpha=0.05)
post_TX = plotting_chart(2007, 'blue', death_TX_post, 'Death_per_cap', 'Year', alpha=0.05)

final = (pre_TX + post_TX)

final.properties(title = "Pre-Post Analysis of Opioid Regulations for Texas")


# %%
diff_FL_data = death_data.loc[death_data['State_Code'].isin(["MI","NV","SC","FL"])].copy()
diff_FL_data['Treat'] = 1
diff_FL_data.loc[diff_FL_data['State_Code'].isin(["MI","NV","SC"]), 'Treat'] = 0


# %%
diff_FL_treat = diff_FL_data.loc[diff_FL_data['Treat'] == 1]
diff_FL_control = diff_FL_data.loc[diff_FL_data['Treat'] == 0]


# %%
diff_FL_treat_pre = diff_FL_treat.loc[diff_FL_treat['Year'] < 2010]
diff_FL_treat_post = diff_FL_treat.loc[diff_FL_treat['Year'] >= 2010]
diff_FL_control_pre = diff_FL_control.loc[diff_FL_control['Year'] < 2010]
diff_FL_control_post = diff_FL_control.loc[diff_FL_control['Year'] >= 2010]


# %%
diff_FL_data


# %%
diff_FL_data.pivot(index=["Year","State_Code","County_Name"],columns=[""])


# %%
pre_FL = plotting_chart(2010, 'blue', diff_FL_treat_pre, 'Death_per_cap', 'Year', alpha=0.05)
post_FL = plotting_chart(2010, 'blue', diff_FL_treat_post, 'Death_per_cap', 'Year', alpha=0.05)
pre_control = plotting_chart(2010, 'orange', diff_FL_control_pre, 'Death_per_cap', 'Year', alpha=0.05)
post_control = plotting_chart(2010, 'orange', diff_FL_control_post, 'Death_per_cap', 'Year', alpha=0.05)


final = pre_FL + post_FL + pre_control + post_control
final.properties(title = "Diff in Diff Analysis of Opioid Regulations for Florida vs Comparison States")


# %%
pre_fl


# %%
base = (
    alt.Chart(death_FL_pre)
    .mark_point()
    .encode(
        x=alt.X("Year", scale=alt.Scale(zero=False)),
        y="Death_per_cap",
        
    )
)
fit = base.transform_regression(
        "Year", "Death_per_cap"
    ).mark_line()

text = (alt.Chart(death_FL_pre)
    .encode(
        alt.X('Year:Q', axis=alt.Axis(format='.0f', values=[2010,2011,2012,2013,2014,2015])),
        y="Death_per_cap",
        
    )
    .mark_text(size=5))

base + fit + text


# %%
fit, reg_chart = get_reg_fit(
    death_FL_pre, yvar="Death_per_cap", xvar="Year", alpha=0.05
)
fit


# %%
years = np.arange(2003, 2016,1)


# %%
policy_FL = pd.DataFrame({'Year': [2010]}) 

rule = alt.Chart(policy_FL).mark_rule(color='black').encode(
alt.X('Year:Q', axis=alt.Axis(values=years))
)


# %%
pre_fl + rule + post_fl


# %%



