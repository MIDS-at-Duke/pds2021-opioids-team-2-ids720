# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
deaths = pd.read_csv('https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-2-ids720/data_merging/20_intermediate_files/mortality_merged.csv?token=AVJP5IV6UR5HNLSRSPYC4DLBR3KRM')


# %%
# Looking at States for analysis for the impact of change in policy in Florida
year = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010]
pre_deaths = deaths.loc[deaths['Year'].isin(year)]
deaths_state = pre_deaths.groupby(['State_Code','Year'], as_index= False)[['Deaths', 'Population']].sum()
deaths_state['deaths_per_cap'] = deaths_state['Deaths']*100/deaths_state['Population']
# The states below are chosen based on the trend of deaths/capita overtime
rel_state = ['FL','MI','NV','SC']
states1 = deaths_state[deaths_state['State_Code'].isin(rel_state)]
import altair as alt

alt.Chart(states1).mark_line().encode(
    x='Year',
    y='deaths_per_cap',
    color='State_Code',
    
).properties(
    width=500,
    height=500
)


# %%
# Looking at States for analysis for the impact of change in policy in Washington
year = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,2011]
pre_deaths = deaths.loc[deaths['Year'].isin(year)]
deaths_state = pre_deaths.groupby(['State_Code','Year'], as_index= False)[['Deaths', 'Population']].sum()
deaths_state['deaths_per_cap'] = deaths_state['Deaths']*100/deaths_state['Population']
# The states below are chosen based on the trend of deaths/capita overtime
rel_state = ['WA','HI','MT','CO']
states1 = deaths_state[deaths_state['State_Code'].isin(rel_state)]
import altair as alt

alt.Chart(states1).mark_line().encode(
    x='Year',
    y='deaths_per_cap',
    color='State_Code',
    
).properties(
    width=500,
    height=500
)


# %%
# Looking at States for analysis for the impact of change in policy in Texas
year = [2003, 2004, 2005, 2006, 2007]
pre_deaths = deaths.loc[deaths['Year'].isin(year)]
deaths_state = pre_deaths.groupby(['State_Code','Year'], as_index= False)[['Deaths', 'Population']].sum()
deaths_state['deaths_per_cap'] = deaths_state['Deaths']*100/deaths_state['Population']
# The states below are chosen based on the trend of deaths/capita overtime
rel_state = ['TX','NY','CA','OR']
states1 = deaths_state[deaths_state['State_Code'].isin(rel_state)]
import altair as alt

alt.Chart(states1).mark_line().encode(
    x='Year',
    y='deaths_per_cap',
    color='State_Code',
    
).properties(
    width=500,
    height=500
)


# %%
deaths_state = deaths.groupby(['State_Code','Year'], as_index= False)[['Deaths', 'Population']].sum()
deaths_state['deaths_per_cap'] = deaths_state['Deaths']*100/deaths_state['Population']

# %% [markdown]
# #  Pre - Post Comparison

# %%
# For the change in effect of policy in Florida
FL_state = ['FL','MI','NV','SC']
states_data = deaths_state[deaths_state['State_Code'].isin(FL_state)]
data = pd.DataFrame({'Year': [2010]})
import altair as alt

chart = alt.Chart(states_data).mark_line().encode(
    x='Year',
    y='deaths_per_cap',
    color='State_Code',
    
)


rule = alt.Chart(data).mark_rule(color='black').encode(
    x = 'Year:Q'
)


(chart + rule).properties(
    width=500,
    height=500,
    title='Policy Change in Florida'
)


# %%
# For the change in effect of policy in Washington
WA_state = ['WA','HI','MT','CO']
states_data = deaths_state[deaths_state['State_Code'].isin(WA_state)]
data = pd.DataFrame({'Year': [2011]})
import altair as alt

chart = alt.Chart(states_data).mark_line().encode(
    x='Year',
    y='deaths_per_cap',
    color='State_Code',
    
)


rule = alt.Chart(data).mark_rule(color='black').encode(
    x = 'Year:Q'
)


(chart + rule).properties(
    width=500,
    height=500,
    title='Policy Change in Washington'
)


# %%
# For the change in effect of policy in Washington
TX_state = ['TX','NY','CA','OR']
states_data = deaths_state[deaths_state['State_Code'].isin(TX_state)]
data = pd.DataFrame({'Year': [2007]})
import altair as alt

chart = alt.Chart(states_data).mark_line().encode(
    x='Year',
    y='deaths_per_cap',
    color='State_Code',
    
)


rule = alt.Chart(data).mark_rule(color='black').encode(
    x = 'Year:Q'
)


(chart + rule).properties(
    width=500,
    height=500,
    title='Policy Change in Texas'
)


# %%



