# %%
import pandas as pd

shipment = pd.read_csv('/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/20_intermediate_files/merged_pop_and_ship_and_fips.csv')

# aggregate the data by state and year
ship_grouped = shipment.groupby(['BUYER_STATE','Year'], as_index= False)[['MME', 'Population']].sum()

# add a calculation for shipments per capita
ship_grouped['ships_per_cap'] = ship_grouped['MME']/ship_grouped['Population']

# %%
# subset the data for only Florida
treatment_state = ship_grouped[ship_grouped['BUYER_STATE']=='FL']
# subset the data for only the control states
controls = ['OR','NV','SC']
control_states = ship_grouped[ship_grouped['BUYER_STATE'].isin(controls)]

# %%
# specify the years needed before the policy change
year = [2006, 2007, 2008, 2009]
# create new dataframe with only data from those years
pre_FL_ship = treatment_state.loc[treatment_state['Year'].isin(year)]
post_FL_ship = treatment_state.loc[~treatment_state['Year'].isin(year)]

pre_crtl_ship = control_states.loc[control_states['Year'].isin(year)]
post_crtl_ship = control_states.loc[~control_states['Year'].isin(year)]

# %%
import statsmodels.formula.api as smf
import altair as alt
import numpy as np

# %%
def get_reg_fit(data, color, yvar, xvar, legend, alpha=0.05):
    colour= color
    years = list(np.arange(2006, 2013,1))

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
    reg = alt.Chart(predictions).mark_line().encode(x=xvar, y=alt.Y(yvar), color = alt.value(f"{colour}"), opacity=alt.Opacity("Treat", legend=alt.Legend(title="Legend")))
    ci = (
        alt.Chart(predictions)
        .mark_errorband()
        .encode(
            alt.X(f"{xvar}:Q", axis=alt.Axis(format='.0f', values=years)),
            y=alt.Y("ci_low", title="Opioid Shipments per Capita in Milligrams (MME)", scale=alt.Scale(zero=False)),
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

    years = list(np.arange(2006, 2013, 1))

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
pre_FL_plot = plotting_chart(2010, "blue", pre_FL_ship, "ships_per_cap", "Year","Florida", alpha=0.05)
post_FL_plot = plotting_chart(2010, "blue", post_FL_ship, "ships_per_cap", "Year","Florida", alpha=0.05)


pre_post_final = pre_FL_plot + post_FL_plot
pre_post_final.properties(title = "Pre-Post Analysis of Regulations on Opioid Shipments for Florida")

# %%
pre_crtl_plot = plotting_chart(2010, "#9467bd", pre_crtl_ship, "ships_per_cap", "Year","Control States - NV, SC, OR", alpha=0.05)
post_crtl_plot = plotting_chart(2010, "#9467bd", post_crtl_ship, "ships_per_cap", "Year","Control States - NV, SC, OR", alpha=0.05)


diff_in_diff_final = pre_FL_plot + post_FL_plot + pre_crtl_plot + post_crtl_plot
diff_in_diff_final.properties(title = "Diff-in-Diff Analysis of Regulations on Opioid Shipments for Florida vs Control States")


