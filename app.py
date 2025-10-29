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
