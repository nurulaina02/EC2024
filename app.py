import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Data Loading ---
@st.cache_data
def load_data(url):
    """Loads data from a URL and caches it."""
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return pd.DataFrame() # Return an empty DataFrame on failure

url = 'https://raw.githubusercontent.com/nurulaina02/EC2024/refs/heads/main/student_survey_cleaned.csv'
df = load_data(url)

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="Student Survey Analysis")

st.title('Student Survey Data Analysis with Plotly and Streamlit')

if not df.empty:
    st.subheader('Raw Data Head')
    st.dataframe(df.head())

    # Assuming 'Faculty' column exists and 'Arts' faculty needs to be filtered
    # This block requires the 'Faculty' column which is not explicitly confirmed in the original code,
    # but implied by the use of `arts_df`. I'll create a placeholder for it, or use the full df if filtering is not possible.
    try:
        # Attempt to filter for 'Arts' Faculty data as in the original script
        # Note: The exact column name for Faculty might differ. Assuming it's 'Faculty'.
        arts_df = df[df['Faculty'] == 'Arts']
    except KeyError:
        # Fallback if 'Faculty' column is not found or for simplicity/if the filtering isn't crucial for conversion
        st.warning("Could not find 'Faculty' column to filter 'Arts' data. Using full dataset for 'Gender' plots.")
        arts_df = df
    
    # 1. Gender Distribution (Pie Chart) - Original: Matplotlib Pie Chart on arts_df['Gender']
    st.subheader('1. Gender Distribution (Arts Faculty/Full Data) - Pie Chart')
    if not arts_df.empty:
        gender_counts_arts = arts_df['Gender'].value_counts().reset_index()
        gender_counts_arts.columns = ['Gender', 'Count']
        
        fig_gender_pie = px.pie(
            gender_counts_arts, 
            values='Count', 
            names='Gender', 
            title='Gender Distribution in Arts Faculty (or Full Data)',
            hole=.3 # Add a donut shape for better aesthetics
        )
        st.plotly_chart(fig_gender_pie, use_container_width=True)
    else:
        st.info("No 'Arts' faculty data found.")


    # 2. Gender Distribution (Bar Chart) - Original: Matplotlib Bar Chart on arts_df['Gender']
    st.subheader('2. Gender Distribution (Arts Faculty/Full Data) - Bar Chart')
    if not arts_df.empty:
        # Reuse gender_counts_arts from above
        fig_gender_bar = px.bar(
            gender_counts_arts,
            x='Gender', 
            y='Count', 
            title='Gender Distribution in Arts Faculty (or Full Data)',
            text='Count' # Display count on bars
        )
        fig_gender_bar.update_traces(textposition='outside')
        st.plotly_chart(fig_gender_bar, use_container_width=True)


    # 3. Coaching Center Attendance (Pie Chart) - Original: Matplotlib Pie Chart on df['Did you ever attend a Coaching center?']
    st.subheader('3. Coaching Center Attendance')
    coaching_col = 'Did you ever attend a Coaching center?'
    if coaching_col in df.columns:
        coaching_counts = df[coaching_col].value_counts().reset_index()
        coaching_counts.columns = [coaching_col, 'Count']
        
        fig_coaching = px.pie(
            coaching_counts, 
            values='Count', 
            names=coaching_col, 
            title='Did students attend a coaching center?',
            color=coaching_col # Auto-assign different colors
        )
        st.plotly_chart(fig_coaching, use_container_width=True)
    else:
        st.warning(f"Column '{coaching_col}' not found in data.")


    # 4. Study Medium Distribution (Bar Chart) - Original: Matplotlib Bar Chart on df['H.S.C or Equivalent study medium']
    st.subheader('4. Distribution of H.S.C or Equivalent Study Medium')
    study_medium_col = 'H.S.C or Equivalent study medium'
    if study_medium_col in df.columns:
        study_medium_counts = df[study_medium_col].value_counts().reset_index()
        study_medium_counts.columns = [study_medium_col, 'Count']
        
        fig_study_medium = px.bar(
            study_medium_counts,
            x=study_medium_col, 
            y='Count', 
            title='Distribution of H.S.C or Equivalent Study Medium'
        )
        fig_study_medium.update_layout(xaxis_title='Study Medium', xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig_study_medium, use_container_width=True)
    else:
        st.warning(f"Column '{study_medium_col}' not found in data.")


    # 5. H.S.C (GPA) Distribution (Histogram) - Original: Matplotlib Histogram on df['H.S.C (GPA)']
    st.subheader('5. Distribution of H.S.C (GPA)')
    hsc_gpa_col = 'H.S.C (GPA)'
    if hsc_gpa_col in df.columns:
        # Drop NaN values for the histogram as in the original code
        gpa_data = df[hsc_gpa_col].dropna()
        
        fig_hsc_gpa = px.histogram(
            gpa_data,
            x=hsc_gpa_col,
            nbins=20, # Use nbins parameter for number of bins
            title='Distribution of H.S.C (GPA)'
        )
        fig_hsc_gpa.update_layout(xaxis_title='H.S.C (GPA)', yaxis_title='Frequency')
        st.plotly_chart(fig_hsc_gpa, use_container_width=True)
    else:
        st.warning(f"Column '{hsc_gpa_col}' not found in data.")


    # 6. S.S.C (GPA) Distribution (Histogram) - Original: Matplotlib Histogram on df['S.S.C (GPA)']
    st.subheader('6. Distribution of S.S.C (GPA)')
    ssc_gpa_col = 'S.S.C (GPA)'
    if ssc_gpa_col in df.columns:
        # Drop NaN values for the histogram as in the original code
        gpa_data = df[ssc_gpa_col].dropna()
        
        fig_ssc_gpa = px.histogram(
            gpa_data,
            x=ssc_gpa_col,
            nbins=20, 
            title='Distribution of S.S.C (GPA)'
        )
        fig_ssc_gpa.update_layout(xaxis_title='S.S.C (GPA)', yaxis_title='Frequency')
        st.plotly_chart(fig_ssc_gpa, use_container_width=True)
    else:
        st.warning(f"Column '{ssc_gpa_col}' not found in data.")


    # 7. Bachelor Academic Year Distribution (Bar Chart) - Original: Matplotlib Bar Chart on df['Bachelor Academic Year in EU']
    st.subheader('7. Distribution of Academic Years (Bachelor)')
    academic_year_col = 'Bachelor  Academic Year in EU' # Note the non-standard space
    if academic_year_col in df.columns:
        academic_year_counts = df[academic_year_col].value_counts().reset_index()
        academic_year_counts.columns = [academic_year_col, 'Count']
        
        fig_academic_year = px.bar(
            academic_year_counts,
            x=academic_year_col, 
            y='Count', 
            title='Distribution of Academic Years (Bachelor)'
        )
        fig_academic_year.update_layout(xaxis_title='Academic Year', xaxis={'categoryorder':'category ascending'})
        st.plotly_chart(fig_academic_year, use_container_width=True)
    else:
        st.warning(f"Column '{academic_year_col}' not found in data.")

else:
    st.error("Failed to load data. Please check the URL and file.")

# To run this app:
# 1. Save the code above as a Python file (e.g., app.py).
# 2. Run it from your terminal using: streamlit run app.py
