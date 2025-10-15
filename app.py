import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set the title of the Streamlit application
st.title('📊 Student Survey Data Analysis')
st.markdown('***Interactive visualizations using Plotly.***')

# --- 1. Data Loading ---
url = 'https://raw.githubusercontent.com/nurulaina02/EC2024/refs/heads/main/student_survey_cleaned.csv'

@st.cache_data
def load_data(data_url):
    """Loads and caches the dataframe."""
    try:
        df = pd.read_csv(data_url)
        return df
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return pd.DataFrame()

df = load_data(url)

if df.empty:
    st.stop() # Stop execution if data loading failed

st.header('Raw Data Preview')
st.dataframe(df.head())
st.markdown('---')


# --- 2. Data Preparation for Arts Faculty (Simulated) ---
# Assuming 'Faculty' column exists and we need to filter for 'Arts'
# Since the original code used 'arts_df', we'll simulate it by assuming a column named 'Faculty'
# If the actual column name is different, this line needs adjustment.
try:
    arts_df = df[df['Faculty'] == 'Arts']
except KeyError:
    st.warning("⚠️ Column 'Faculty' not found for filtering Arts data. Using full DataFrame for Gender plots as a fallback.")
    arts_df = df


# --- 3. Visualizations using Plotly ---

# ## Gender Distribution in Arts Faculty (Pie Chart)
st.header('1. Gender Distribution in Arts Faculty')
if not arts_df.empty and 'Gender' in arts_df.columns:
    gender_counts = arts_df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    
    fig_pie = px.pie(
        gender_counts, 
        values='Count', 
        names='Gender', 
        title='Gender Distribution in Arts Faculty (Pie Chart)',
        hole=0.3, # Optional: makes it a donut chart
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("Cannot display Gender Distribution for Arts Faculty due to missing data or 'Gender' column.")

st.markdown('---')

# ## Gender Distribution in Arts Faculty (Bar Chart)
if not arts_df.empty and 'Gender' in arts_df.columns:
    gender_counts = arts_df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    
    fig_bar = px.bar(
        gender_counts, 
        x='Gender', 
        y='Count', 
        title='Gender Distribution in Arts Faculty (Bar Chart)',
        color='Gender',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_bar.update_layout(xaxis_title='Gender', yaxis_title='Count')
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    # Message already shown above, skip to next section
    pass

st.markdown('---')

# ## Did students attend a coaching center? (Pie Chart)
coaching_col = 'Did you ever attend a Coaching center?'
st.header(f'2. {coaching_col}')
if coaching_col in df.columns:
    coaching_counts = df[coaching_col].value_counts().reset_index()
    coaching_counts.columns = ['Attended', 'Count']
    
    fig_coaching = px.pie(
        coaching_counts, 
        values='Count', 
        names='Attended', 
        title='Did students attend a coaching center?',
        color_discrete_sequence=px.colors.qualitative.D3
    )
    st.plotly_chart(fig_coaching, use_container_width=True)
else:
    st.info(f"Cannot display plot for missing column: '{coaching_col}'.")

st.markdown('---')

# ## Distribution of H.S.C or Equivalent Study Medium (Bar Chart)
medium_col = 'H.S.C or Equivalent study medium'
st.header(f'3. Distribution of {medium_col}')
if medium_col in df.columns:
    study_medium_counts = df[medium_col].value_counts().reset_index()
    study_medium_counts.columns = ['Study Medium', 'Count']
    
    fig_medium = px.bar(
        study_medium_counts, 
        x='Study Medium', 
        y='Count', 
        title='Distribution of H.S.C or Equivalent Study Medium',
        color='Study Medium',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_medium.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_medium, use_container_width=True)
else:
    st.info(f"Cannot display plot for missing column: '{medium_col}'.")

st.markdown('---')

# ## Distribution of H.S.C (GPA) (Histogram)
gpa_hsc_col = 'H.S.C (GPA)'
st.header(f'4. Distribution of {gpa_hsc_col}')
if gpa_hsc_col in df.columns:
    fig_hsc_gpa = px.histogram(
        df.dropna(subset=[gpa_hsc_col]), 
        x=gpa_hsc_col, 
        title='Distribution of H.S.C (GPA)',
        nbins=20,
        marginal="box", # Optional: Adds a box plot for better summary
        color_discrete_sequence=['#00aaff']
    )
    fig_hsc_gpa.update_layout(xaxis_title=gpa_hsc_col, yaxis_title='Frequency')
    st.plotly_chart(fig_hsc_gpa, use_container_width=True)
else:
    st.info(f"Cannot display plot for missing column: '{gpa_hsc_col}'.")

st.markdown('---')

# ## Distribution of S.S.C (GPA) (Histogram)
gpa_ssc_col = 'S.S.C (GPA)'
st.header(f'5. Distribution of {gpa_ssc_col}')
if gpa_ssc_col in df.columns:
    fig_ssc_gpa = px.histogram(
        df.dropna(subset=[gpa_ssc_col]), 
        x=gpa_ssc_col, 
        title='Distribution of S.S.C (GPA)',
        nbins=20,
        marginal="box",
        color_discrete_sequence=['#ff4b4b']
    )
    fig_ssc_gpa.update_layout(xaxis_title=gpa_ssc_col, yaxis_title='Frequency')
    st.plotly_chart(fig_ssc_gpa, use_container_width=True)
else:
    st.info(f"Cannot display plot for missing column: '{gpa_ssc_col}'.")

st.markdown('---')

# ## Distribution of Expectation Met Responses (Bar Chart)
expectation_col = 'Q5 [To what extent your expectation was met?]'
st.header('6. Extent Expectation Was Met (Scale 1-5)')
if expectation_col in df.columns:
    expectation_met_counts = df[expectation_col].value_counts().sort_index().reset_index()
    expectation_met_counts.columns = ['Response', 'Count']
    
    # Ensure Response is treated as a categorical/string for proper x-axis labeling
    expectation_met_counts['Response'] = expectation_met_counts['Response'].astype(str)
    
    fig_expectation = px.bar(
        expectation_met_counts, 
        x='Response', 
        y='Count', 
        title='Distribution of Responses to "To what extent your expectation was met?"',
        color='Count', # Color based on count
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig_expectation.update_layout(xaxis_title='Response (Scale of 1-5)', yaxis_title='Count')
    st.plotly_chart(fig_expectation, use_container_width=True)
else:
    st.info(f"Cannot display plot for missing column: '{expectation_col}'.")
