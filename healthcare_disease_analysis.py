import streamlit as st
from openai import OpenAI
import json
import pandas as pd
import requests

client = OpenAI(api_key="")

def get_disease_info(disease_name):
    """
    Function to query OpenAI and return structured information about a disease.
    """
    medication_format = '''"name":"",
    "side_effects":[
        0:"",
        1:"",
        ...
    ],
    "dosage":""'''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Please provide information on the following aspects for {disease_name}: 1. Key Statistics, 2. Recovery Options, 3. Recommended Medications, 4. Preventive Measures, 5. Transmissibility (R0), 6. Historical Data of Cases. Format the response in JSON with keys for 'name', 'statistics', 'total_cases', 'recovery_rate', 'mortality_rate', 'recovery_options', 'medication', 'preventive_measures', 'transmissibility', 'historical_data' always use this json format for medication : {medication_format} ."}
        ]
    )
    return response.choices[0].message.content

def display_disease_info(disease_info):
    """
    Function to display the disease information in a structured way using Streamlit.
    """
    try:
        info = json.loads(disease_info)

        st.write(f"## Statistics for {info['name']}")
        st.write(f"**Total Cases:** {info['statistics']['total_cases']}")
        st.write(f"**Recovery Rate:** {info['statistics']['recovery_rate']}")
        st.write(f"**Mortality Rate:** {info['statistics']['mortality_rate']}")
        st.write(f"**Transmissibility (R0):** {info.get('transmissibility', 'N/A')}")

        # Historical Data Chart
        historical_data = info.get('historical_data', {})
        if historical_data:
            st.write("### Historical Data of Cases")
            historical_df = pd.DataFrame(historical_data)
            st.line_chart(historical_df)

        # Recovery Options and Medications
        st.write("## Recovery Options")
        recovery_options = info['recovery_options']
        for option, description in recovery_options.items():
            st.subheader(option)
            st.write(description)

        st.write("## Medication")
        medication = info['medication']
        medication_count = 1
        for option, description in medication.items():
            st.subheader(f"{medication_count}. {option}")
            st.write(description)
            medication_count += 1

        # Preventive Measures
        st.write("## Preventive Measures")
        preventive_measures = info.get('preventive_measures', "No preventive measures available.")
        st.write(preventive_measures)

    except json.JSONDecodeError:
        st.error("Failed to decode the response into JSON. Please check the format of the OpenAI response.")

def get_live_data(disease_name):
    """
    Fetch live data from an external API (e.g., Disease.sh or WHO) if available.
    """
    url = f"https://disease.sh/v3/covid-19/all"  # Example API endpoint for COVID-19. Replace with the correct endpoint.
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

st.title("Disease Information Dashboard")

disease_name = st.text_input("Enter the name of the disease:")

if disease_name:
    disease_info = get_disease_info(disease_name)
    display_disease_info(disease_info)

    # Optionally fetch and display live data if available
    st.write("## Live Data (if available)")
    live_data = get_live_data(disease_name)
    if live_data:
        st.json(live_data)
    else:
        st.write("No live data available for this disease.")