# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd

shipment = pd.read_csv('/mnt/c/Users/sdona/Documents/Duke/720IDS/Mid-SemesterProject/pds2021-opioids-team-2-ids720/20_intermediate_files/merged_pop_and_ship_and_fips.csv')


# %%
shipment.head()


# %%
# aggregate the data by state and year
ship_grouped = shipment.groupby(['BUYER_STATE','Year'], as_index= False)[['MME', 'Population']].sum()


# %%
# add a calculation for shipments per capita
ship_grouped['ships_per_cap'] = ship_grouped['MME']/ship_grouped['Population']


# %%
# specify the years needed before the policy change
year = [2003, 2004, 2005, 2006, 2007, 2008, 2009]
# create new dataframe with only data from those years
pre_ship = ship_grouped.loc[ship_states['Year'].isin(year)]


# %%
# The states below are chosen based on the trend of deaths/capita overtime
states = ['FL','MI','NV','SC']
control_states = pre_ship[pre_ship['BUYER_STATE'].isin(states)]
import altair as alt

alt.Chart(control_states).mark_line().encode(
    x='Year',
    y='ships_per_cap',
    color='BUYER_STATE',
    
).properties(
    width=500,
    height=500
)


# %%
# do the same thing but for the entire timeframe
pre_post_ship = ship_grouped[ship_grouped['BUYER_STATE'].isin(states)]
# add a line for when the policy took place
policy = pd.DataFrame({'Year': [2010]})

chart = alt.Chart(pre_post_ship).mark_line().encode(
    x='Year',
    y='ships_per_cap',
    color='BUYER_STATE',
    
)


rule = alt.Chart(policy).mark_rule(color='black').encode(
    x = 'Year:Q'
)


(chart + rule).properties(
    width=500,
    height=500,
    title='Policy Change in Florida'
)


