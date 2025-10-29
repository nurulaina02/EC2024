import streamlit as st

st.set_page_config(
    page_title="Mental Health Classification Analysis"
)
visualise = st.Page('mentalhealth.py', title='Mental Health Classification Analysis', icon=":material/school:")

home = st.Page('home.py', title='Homepage', default=True, icon=":material/home:")

pg = st.navigation(
        {
            "Menu": [home, visualise]
        }
    )

pg.run()

# Load your data
try:
    df2 = pd.read_csv('https://raw.githubusercontent.com/nurulaina02/EC2024/refs/heads/main/Mental%20Health%20Classification.csv', encoding='utf-8')
except UnicodeDecodeError:
    df2 = pd.read_csv('https://raw.githubusercontent.com/nurulaina02/EC2024/refs/heads/main/Mental%20Health%20Classification.csv', encoding='latin-1')
df2
