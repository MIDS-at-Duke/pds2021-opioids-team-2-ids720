# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import statsmodels.formula.api as smf
import pandas as pd 
import altair as alt
from altair_saver import save
import numpy as np


# %%
# loading data and filtering for TXorida

ship_data = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-2-ids720/data_merging/20_intermediate_files/merged_pop_and_ship_and_fips.csv?token=AVJP5IQQIZOVH246U3U2TY3BTXTJ2')


# %%
# mean county for all data 
median_income_UScounties = float(ship_data['Median_Income_2010'].mean())


# %%
ship_data_rel = ship_data.loc[ship_data['BUYER_STATE'].isin(['WA','TX','FL']), ['BUYER_STATE','BUYER_COUNTY','Year','ships_per_cap','Median_Income_2010']]


# %%
ship_data_rel['Income_Indicator'] = 'High Income Counties'
ship_data_rel.loc[ship_data_rel['Median_Income_2010'] <= median_income_UScounties, 'Income_Indicator'] = 'Low Income Counties'


# %%
ship_data_FL = ship_data_rel.loc[ship_data_rel['BUYER_STATE'] == 'FL']
ship_data_FL


# %%
ship_data_FL_pre = ship_data_FL.loc[ship_data_rel['Year'] < 2010]
ship_data_FL_post = ship_data_FL.loc[ship_data_rel['Year']  >=  2010]


# %%
FL_pre_high = ship_data_FL_pre.loc[ship_data_FL_pre['Income_Indicator'] == 'High Income Counties']
FL_post_high = ship_data_FL_post.loc[ship_data_FL_post['Income_Indicator'] == 'High Income Counties']
FL_pre_low = ship_data_FL_pre.loc[ship_data_FL_pre['Income_Indicator'] == 'Low Income Counties']
FL_post_low = ship_data_FL_post.loc[ship_data_FL_post['Income_Indicator'] == 'Low Income Counties']


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
plot_FL_low_pre = plotting_chart(2010, 'blue', FL_pre_low, 'ships_per_cap', 'Year', legend = 'Low Income', alpha= 0.05)
plot_FL_low_post = plotting_chart(2010, 'blue', FL_post_low, 'ships_per_cap', 'Year', legend = 'Low Income', alpha= 0.05)
plot_FL_high_pre = plotting_chart(2010, '#9467bd', FL_pre_high, 'ships_per_cap', 'Year', legend = 'High Income', alpha= 0.05)
plot_FL_high_post = plotting_chart(2010, '#9467bd', FL_post_high, 'ships_per_cap', 'Year', legend = 'High Income', alpha= 0.05)

final = plot_FL_high_pre + plot_FL_low_pre + plot_FL_high_post + plot_FL_low_post
final


# %%
death_data = pd.read_csv("https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-2-ids720/data_merging/20_intermediate_files/mortality_merged_imputed.csv?token=AVJP5IXD2ZEAXDKNWHM626DBUBNMY")
death_data["Death_per_cap_final"] = np.where(death_data["Death_per_cap"].notna(), death_data["Death_per_cap"],death_data["imputed_death_per_cap"])
death_data_rel = death_data.loc[death_data['State_Code'].isin(['WA','FL','TX']), ['State_Code','County_Name','Year','Death_per_cap_final','Median_Income_2010']]


# %%
death_data_rel['Income_Indicator'] = 'High Income Counties'
death_data_rel.loc[death_data_rel['Median_Income_2010'] <= median_income_UScounties, 'Income_Indicator'] = 'Low Income Counties'


# %%
death_data_FL = death_data_rel.loc[death_data_rel['State_Code'] == 'FL']
death_data_WA = death_data_rel.loc[death_data_rel['State_Code'] == 'WA']
death_data_TX = death_data_rel.loc[death_data_rel['State_Code'] == 'TX']


# %%
death_data_FL_pre = death_data_FL.loc[death_data_rel['Year'] < 2010]
death_data_FL_post = death_data_FL.loc[death_data_rel['Year']  >=  2010]
death_data_WA_pre = death_data_WA.loc[death_data_rel['Year'] < 2011]
death_data_WA_post = death_data_WA.loc[death_data_rel['Year']  >=  2011]
death_data_TX_pre = death_data_TX.loc[death_data_rel['Year'] < 2007]
death_data_TX_post = death_data_TX.loc[death_data_rel['Year']  >=  2007]


# %%
WA_pre_high = death_data_WA_pre.loc[death_data_WA_pre['Income_Indicator'] == 'High Income Counties']
WA_post_high = death_data_WA_post.loc[death_data_WA_post['Income_Indicator'] == 'High Income Counties']
WA_pre_low = death_data_WA_pre.loc[death_data_WA_pre['Income_Indicator'] == 'Low Income Counties']
WA_post_low = death_data_WA_post.loc[death_data_WA_post['Income_Indicator'] == 'Low Income Counties']


# %%
TX_pre_high = death_data_TX_pre.loc[death_data_TX_pre['Income_Indicator'] == 'High Income Counties']
TX_post_high = death_data_TX_post.loc[death_data_TX_post['Income_Indicator'] == 'High Income Counties']
TX_pre_low = death_data_TX_pre.loc[death_data_TX_pre['Income_Indicator'] == 'Low Income Counties']
TX_post_low = death_data_TX_post.loc[death_data_TX_post['Income_Indicator'] == 'Low Income Counties']


# %%
FL_pre_high = death_data_FL_pre.loc[death_data_FL_pre['Income_Indicator'] == 'High Income Counties']
FL_post_high = death_data_FL_post.loc[death_data_FL_post['Income_Indicator'] == 'High Income Counties']
FL_pre_low = death_data_FL_pre.loc[death_data_FL_pre['Income_Indicator'] == 'Low Income Counties']
FL_post_low = death_data_FL_post.loc[death_data_FL_post['Income_Indicator'] == 'Low Income Counties']


# %%
plot_FL_low_pre = plotting_chart(2010, 'blue', FL_pre_low, 'Death_per_cap_final', 'Year', legend = 'Low Income', alpha= 0.05)
plot_FL_high_pre = plotting_chart(2010, '#9467bd', FL_pre_high, 'Death_per_cap_final', 'Year', legend = 'High Income', alpha= 0.05)
plot_FL_low_post = plotting_chart(2010, 'blue', FL_post_low, 'Death_per_cap_final', 'Year', legend = 'Low Income', alpha= 0.05)
plot_FL_high_post = plotting_chart(2010, '#9467bd', FL_post_high, 'Death_per_cap_final', 'Year', legend = 'High Income', alpha= 0.05)

final = plot_FL_high_pre + plot_FL_low_pre + plot_FL_high_post + plot_FL_low_post
final


# %%
plot_WA_low_pre = plotting_chart(2011, 'blue', WA_pre_low, 'Death_per_cap_final', 'Year', legend = 'Low Income', alpha= 0.05)
plot_WA_high_pre = plotting_chart(2011, '#9467bd', WA_pre_high, 'Death_per_cap_final', 'Year', legend = 'High Income', alpha= 0.05)
plot_WA_low_post = plotting_chart(2011, 'blue', WA_post_low, 'Death_per_cap_final', 'Year', legend = 'Low Income', alpha= 0.05)
plot_WA_high_post = plotting_chart(2011, '#9467bd', WA_post_high, 'Death_per_cap_final', 'Year', legend = 'High Income', alpha= 0.05)

final = plot_WA_high_pre + plot_WA_low_pre + plot_WA_high_post + plot_WA_low_post
final


# %%
plot_TX_low_pre = plotting_chart(2007, 'blue', TX_pre_low, 'Death_per_cap_final', 'Year', legend = 'Low Income', alpha= 0.05)
plot_TX_high_pre = plotting_chart(2007, '#9467bd', TX_pre_high, 'Death_per_cap_final', 'Year', legend = 'High Income', alpha= 0.05)
plot_TX_low_post = plotting_chart(2007, 'blue', TX_post_low, 'Death_per_cap_final', 'Year', legend = 'Low Income', alpha= 0.05)
plot_TX_high_post = plotting_chart(2007, '#9467bd', TX_post_high, 'Death_per_cap_final', 'Year', legend = 'High Income', alpha= 0.05)

final = plot_TX_high_pre + plot_TX_low_pre + plot_TX_high_post + plot_TX_low_post
final


# %%



