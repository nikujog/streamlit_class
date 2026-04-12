# Using the Brooklyn Bridge pedestrian dataset in your Codespace repository (Just drop it into you repository),
# build a small Streamlit dashboard that lets a user explore pedestrian traffic patterns.
# The dataset has one row per hour from October 2017 to June 2018,
# with counts of pedestrians going to Manhattan and to Brooklyn.
# You will need to use a pandas function called resample() that we have not covered in class yet.
# Part of this assignment is practicing how to quickly look something up and apply it. an important real-world skill.
# A hint is provided in the requirements below.

# Dataset columns
# hour_beginning — datetime index (one row per hour)
# pedestrians — total pedestrians that hour
# to_manhattan — pedestrians heading toward Manhattan
# to_brooklyn — pedestrians heading toward Brooklyn
# weather_summary — weather description (e.g. Clear, Rain)
# temperature — temperature in °F
# precipitation — precipitation amount

# Requirements
# Complete all four of the following tasks:

# 1.  Title and subheader
# Add a title and a subheader describing the dashboard using st.title() and st.subheader().

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.title('Brooklyn Bridge Crossings')
st.subheader('Pedestrian Traffic Oct 2017 - Jun 2018')
st.subheader('By Niharika Jog')

# 2.  Radio widget for traffic volume
# Add a st.radio() widget that lets the user choose between Hourly, Daily, and Weekly views.
# New function to look up: resample() — this is a pandas method that groups a time-series by a time period and aggregates the values.
# Search for "pandas resample" and look at how to use .resample('D').sum() for daily and .resample('W').sum() for weekly.
# For Hourly, you do not need to resample, just use the original dataframe.

# time = st.radio('Viewing Period',
#          ['Hourly', 'Daily', 'Weekly'])

time = st.sidebar.radio('Viewing Period',
         ['Hourly', 'Daily', 'Weekly'])

bridge = pd.read_csv('brooklyn_bridge_pedestrians.csv')
# st.dataframe(bridge)

weather_opts = bridge['weather_summary'].unique()[0:10].astype(str).tolist()
weather_opts.insert(0, 'none')
weather = st.sidebar.selectbox('Weather Filter', (weather_opts))

bridge['hour_beginning'] = pd.to_datetime(bridge['hour_beginning'])

if weather != 'none':
    bridge = bridge[bridge['weather_summary'] == weather]

grouped = 0

if time == 'Hourly':
    grouped = bridge.set_index('hour_beginning')['pedestrians']
    # grouped = bridge.resample('h', on = 'hour_beginning')['pedestrians'].sum()
elif time == 'Daily':
    grouped = bridge.resample('D', on = 'hour_beginning')['pedestrians'].sum()
elif time == 'Weekly':
    grouped = bridge.resample('W', on = 'hour_beginning')['pedestrians'].sum()

# 3.  Line chart of pedestrian counts
# Plot the pedestrians column as a line chart using matplotlib and display it with st.pyplot(). Label both axes.

fig, ax = plt.subplots()
ax.plot(grouped)
ax.set_xlabel('Time')
ax.set_ylabel('Number of Pedestrians')
ax.tick_params(axis = 'x', labelrotation = 45)

st.pyplot(fig)

# 4.  Two metric cards
# Display two st.metric() cards side by side using st.columns(2). Show the total pedestrian count and the average pedestrian count for the selected view.

col1, col2 = st.columns(2)

with col1:
    st.metric(label = 'Total Pedestrian Count', value = f'{grouped.sum():,}')
with col2:
    st.metric(label = f'Average {time} Pedestrian Count', value = f'{grouped.mean():,.0f}')

# Stretch goals (if you finish early)
# A.  Plot both to_manhattan and to_brooklyn as two lines on the same chart, each with a different color, and add a legend.

if time == 'Hourly':
    brooklyn_grouped = bridge.set_index('hour_beginning')['to_brooklyn']
    manhattan_grouped = bridge.set_index('hour_beginning')['to_manhattan']
elif time == 'Daily':
    brooklyn_grouped = bridge.resample('D', on = 'hour_beginning')['to_brooklyn'].sum()
    manhattan_grouped = bridge.resample('D', on = 'hour_beginning')['to_manhattan'].sum()
elif time == 'Weekly':
    brooklyn_grouped = bridge.resample('W', on = 'hour_beginning')['to_brooklyn'].sum()
    manhattan_grouped = bridge.resample('W', on = 'hour_beginning')['to_manhattan'].sum()

fig2, ax2 = plt.subplots()
ax2.plot(brooklyn_grouped, label = 'To Brooklyn', color = 'r')
ax2.plot(manhattan_grouped, label = 'To Manhattan', color = 'b')
ax2.set_xlabel('Time')
ax2.set_ylabel('Number of Pedestrians')
ax2.legend()
ax2.tick_params(axis = 'x', labelrotation = 45)

st.pyplot(fig2)

# B.  Move your radio widget into the sidebar using st.sidebar.radio().
# Completed above to intialize time variable before other lines of code.

# C.  Add a st.selectbox() to filter by weather summary so the chart only shows rows matching the selected weather type.
# Completed above before resample() function.