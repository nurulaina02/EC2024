import streamlit as st
import pandas as pd
import plotly.express as px

# --- Corrected Imports ---
import plotly.graph_objects as go # Keep this if you need go, though px handles everything here

# Set Streamlit page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="Mental Health Classification Analysis",
    layout="wide" # Set layout here for consistency
)
visualise = st.Page('mentalhealth.py', title='Mental Health', icon=":material/medicition:")

home = st.Page('app.py', title='Homepage', default=True, icon=":material/home:")

pg = st.navigation(
        {
            "Menu": [home, visualise]
        }
    )

pg.run()
# Page header
st.header("Mental Health Classification Analysis", divider="grey")

col1, col2, col3, col4 = st.columns(4)
    
col1.metric(label="PLO 2", value=f"3.3", help="PLO 2: Cognitive Skill", border=True)
col2.metric(label="PLO 3", value=f"3.5", help="PLO 3: Digital Skill", border=True)
col3.metric(label="PLO 4", value=f"4.0", help="PLO 4: Interpersonal Skill", border=True)
col4.metric(label="PLO 5", value=f"4.3", help="PLO 5: Communication Skill", border=True)

# Load your data
try:
    df2 = pd.read_csv('https://raw.githubusercontent.com/nurulaina02/EC2024/refs/heads/main/Mental%20Health%20Classification.csv', encoding='utf-8')
except UnicodeDecodeError:
    df2 = pd.read_csv('https://raw.githubusercontent.com/nurulaina02/EC2024/refs/heads/main/Mental%20Health%20Classification.csv', encoding='latin-1')
df2
