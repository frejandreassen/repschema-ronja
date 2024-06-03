import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Set up the Streamlit user interface in Swedish
st.title('Ronja Rövardotter Repschema')

# Hard-coded list of characters
characters_list = [
    'Ronja', 'Mattisrövare', 'Borkarövare', 'Vildvittror', 'Grådvärgar',
    'Mattis', 'Birk', 'De underjordiska', 'Skalle-Per', 'Lovis',
    'Rumpnissar', 'Lillklippen', 'Jutis', 'Joen', 'Knektar'
]

# Load the other necessary data
scenes_df = pd.read_csv('scenes.csv')  # Update this if your CSV uses a different delimiter
schedule_df = pd.read_csv('schedule.csv')

# Calculate today's date
today = datetime.now()
# Calculate yesterday's date to include today's events as upcoming
yesterday = datetime.now() - timedelta(days=1)

# Format the 'Datum' column and filter the schedule to include only upcoming events
schedule_df['Datum'] = pd.to_datetime(schedule_df['Datum']).dt.date
next_week_schedule = schedule_df[(pd.to_datetime(schedule_df['Datum']) >= yesterday)]

# User selects characters from the hard-coded list
selected_characters = st.multiselect('Välj karaktärer:', options=characters_list, placeholder="Välj karaktär:")

# Normalize case for comparison by converting everything to lowercase if any character is selected
normalized_characters = [char.lower() for char in selected_characters] if selected_characters else []

# Filter scenes based on selected characters with case-insensitivity
def filter_scenes(row):
    # Replace plus signs with commas and then split by commas
    participants = row['Medverkande'].replace('+', ',').lower().split(',')
    # Clean up extra spaces and check for character presence
    return any(char.lower().strip() in [p.strip() for p in participants] for char in normalized_characters) or 'alla' in participants

# Apply the filter if any character is selected, otherwise use all scenes
if normalized_characters:
    relevant_scenes = scenes_df[scenes_df.apply(filter_scenes, axis=1)]
    # Merge with the schedule using an inner join
    upcoming_scenes = next_week_schedule.merge(relevant_scenes, on='Scen', how='inner')
else:
    relevant_scenes = scenes_df  # Show all scenes if no character is selected
    # Merge with the schedule using a left join
    upcoming_scenes = next_week_schedule.merge(relevant_scenes, on='Scen', how='left')

st.dataframe(upcoming_scenes[['Datum', 'Tid', 'Scen', 'Beskrivning', 'Medverkande', 'Sidor']])
