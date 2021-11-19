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
print("pre-policy FL sum = " + str(pre_FL_ship["MME"].sum()))
print("post-policy FL sum = " + str(post_FL_ship["MME"].sum()))
print("pre-policy control sum = " + str(pre_crtl_ship["MME"].sum()))
print("post-policy control sum = " + str(post_crtl_ship["MME"].sum()))

# %%
pre_FL_ship.describe()

# %%
post_FL_ship.describe()

# %%
pre_crtl_ship.describe()

# %%
post_crtl_ship.describe()


