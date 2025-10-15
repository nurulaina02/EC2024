import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Set the title and initial configuration ---
st.set_page_config(layout="wide")
st.title('📊 Student Survey Data Analysis Dashboard')
st.markdown('***Interactive visualizations using Plotly with actionable insights.***')

# --- 1. Data Loading ---
url = 'https://raw.githubusercontent.com/nurulaina02/EC2024/refs/heads/main/student_survey_cleaned.csv'

@st.cache_data
def load_data(data_url):
    """Loads and caches the dataframe."""
    try:
        df = pd.read_csv(data_url)
        # Attempt to clean column names for easier access (optional)
        df.columns = df.columns.str.strip() 
        return df
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return pd.DataFrame()

df = load_data(url)

if df.empty:
    st.stop() # Stop execution if data loading failed

st.header('Raw Data Preview')
st.dataframe(df.head())

# --- 2. Data Preparation for Arts Faculty (Simulated) ---
# Assuming a column named 'Faculty' exists based on the original request
FACULTY_COL = 'Faculty'
if FACULTY_COL in df.columns:
    arts_df = df[df[FACULTY_COL].astype(str).str.lower() == 'arts']
    if arts_df.empty:
        st.warning(f"⚠️ No 'Arts' entries found in the '{FACULTY_COL}' column. Using full DataFrame for Gender plots.")
        arts_df = df.copy()
else:
    st.warning(f"⚠️ Column '{FACULTY_COL}' not found for filtering Arts data. Using full DataFrame for Gender plots.")
    arts_df = df.copy()

st.markdown("---")

# --- 3. Visualizations using Plotly ---

## Gender Distribution in Arts Faculty
st.header('1. Gender Distribution in Arts Faculty')
GENDER_COL = 'Gender'

if GENDER_COL in arts_df.columns:
    gender_counts = arts_df[GENDER_COL].value_counts().reset_index()
    gender_counts.columns = [GENDER_COL, 'Count']
    
    col1, col2 = st.columns(2)

    with col1:
        # Pie Chart
        fig_pie = px.pie(
            gender_counts, 
            values='Count', 
            names=GENDER_COL, 
            title='Gender Distribution (Pie Chart)',
            hole=0.3, 
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_pie.update_layout(showlegend=True, title_x=0.5)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Bar Chart
        fig_bar = px.bar(
            gender_counts, 
            x=GENDER_COL, 
            y='Count', 
            title='Gender Distribution (Bar Chart)',
            color=GENDER_COL,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_bar.update_layout(xaxis_title='Gender', yaxis_title='Count', title_x=0.5)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    # Calculate dominant gender for insight
    if not gender_counts.empty:
        dominant_gender = gender_counts.iloc[0][GENDER_COL]
        dominant_count = gender_counts.iloc[0]['Count']
        total_count = gender_counts['Count'].sum()
        dominant_percentage = (dominant_count / total_count) * 100
        
        st.info(f"💡 **Insight:** The Arts Faculty sample shows a strong concentration of **{dominant_gender}** students, accounting for **{dominant_percentage:.1f}%** of the total, indicating a significant gender imbalance.")
else:
    st.info(f"Cannot display Gender Distribution due to missing column: '{GENDER_COL}'.")

st.markdown("---")

## Did students attend a coaching center? (Pie Chart)
COACHING_COL = 'Did you ever attend a Coaching center?'
st.header(f'2. Student Coaching Center Attendance')
if COACHING_COL in df.columns:
    coaching_counts = df[COACHING_COL].value_counts().reset_index()
    coaching_counts.columns = ['Attended', 'Count']
    
    fig_coaching = px.pie(
        coaching_counts, 
        values='Count', 
        names='Attended', 
        title='Did students attend a coaching center?',
        color_discrete_sequence=px.colors.qualitative.D3
    )
    fig_coaching.update_layout(title_x=0.5)
    st.plotly_chart(fig_coaching, use_container_width=True)
    
    # Insight
    yes_count = coaching_counts[coaching_counts['Attended'].astype(str).str.lower().str.contains('yes')]['Count'].sum()
    total_count = coaching_counts['Count'].sum()
    yes_percentage = (yes_count / total_count) * 100
    
    st.info(f"💡 **Insight:** A significant proportion of students, **{yes_percentage:.1f}%**, **have attended** a coaching center. This suggests a high reliance on external or supplementary exam preparation beyond traditional schooling.")
else:
    st.info(f"Cannot display plot for missing column: '{COACHING_COL}'.")

st.markdown("---")

## Distribution of H.S.C or Equivalent Study Medium (Bar Chart)
MEDIUM_COL = 'H.S.C or Equivalent study medium'
st.header(f'3. Distribution of {MEDIUM_COL}')
if MEDIUM_COL in df.columns:
    study_medium_counts = df[MEDIUM_COL].value_counts().reset_index()
    study_medium_counts.columns = ['Study Medium', 'Count']
    
    fig_medium = px.bar(
        study_medium_counts, 
        x='Study Medium', 
        y='Count', 
        title='Distribution of H.S.C or Equivalent Study Medium',
        color='Study Medium',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_medium.update_layout(xaxis_tickangle=-45, title_x=0.5)
    st.plotly_chart(fig_medium, use_container_width=True)
    
    # Insight
    dominant_medium = study_medium_counts.iloc[0]['Study Medium']
    
    st.info(f"💡 **Insight:** The **{dominant_medium}** medium is overwhelmingly the most common for H.S.C or equivalent education, indicating it is the standard language or curriculum of instruction for the majority of the students surveyed.")
else:
    st.info(f"Cannot display plot for missing column: '{MEDIUM_COL}'.")

st.markdown("---")

## Distribution of H.S.C (GPA) and S.S.C (GPA) (Histograms)
st.header('4. Distribution of Academic GPAs')
GPA_HSC_COL = 'H.S.C (GPA)'
GPA_SSC_COL = 'S.S.C (GPA)'

col3, col4 = st.columns(2)

# H.S.C GPA Plot
if GPA_HSC_COL in df.columns:
    with col3:
        fig_hsc_gpa = px.histogram(
            df.dropna(subset=[GPA_HSC_COL]), 
            x=GPA_HSC_COL, 
            title=f'Distribution of {GPA_HSC_COL}',
            nbins=20,
            marginal="box", 
            color_discrete_sequence=['#00aaff']
        )
        fig_hsc_gpa.update_layout(xaxis_title='H.S.C (GPA)', yaxis_title='Frequency', title_x=0.5)
        st.plotly_chart(fig_hsc_gpa, use_container_width=True)
        
        # Insight
        mean_hsc = df[GPA_HSC_COL].mean()
        st.info(f"💡 **Insight (HSC):** The distribution is generally **left-skewed** (or negatively skewed) with a **high mean of approximately {mean_hsc:.2f}**, indicating that the majority of students entering the university achieved high H.S.C scores.")
else:
    with col3:
        st.info(f"Cannot display plot for missing column: '{GPA_HSC_COL}'.")

# S.S.C GPA Plot
if GPA_SSC_COL in df.columns:
    with col4:
        fig_ssc_gpa = px.histogram(
            df.dropna(subset=[GPA_SSC_COL]), 
            x=GPA_SSC_COL, 
            title=f'Distribution of {GPA_SSC_COL}',
            nbins=20,
            marginal="box",
            color_discrete_sequence=['#ff4b4b']
        )
        fig_ssc_gpa.update_layout(xaxis_title='S.S.C (GPA)', yaxis_title='Frequency', title_x=0.5)
        st.plotly_chart(fig_ssc_gpa, use_container_width=True)
        
        # Insight
        mean_ssc = df[GPA_SSC_COL].mean()
        st.info(f"💡 **Insight (SSC):** The S.S.C GPA distribution also exhibits a **strong performance** with a mean around **{mean_ssc:.2f}**. The similarity between SSC and HSC scores suggests consistent, high-level academic achievement across pre-university education.")
else:
    with col4:
        st.info(f"Cannot display plot for missing column: '{GPA_SSC_COL}'.")

st.markdown("---")

## Distribution of Expectation Met Responses (Bar Chart)
EXPECTATION_COL = 'Q5 [To what extent your expectation was met?]'
st.header('5. Extent Expectation Was Met (Scale 1-5)')
if EXPECTATION_COL in df.columns:
    expectation_met_counts = df[EXPECTATION_COL].value_counts().sort_index().reset_index()
    expectation_met_counts.columns = ['Response', 'Count']
    
    # Ensure Response is treated as a categorical/string for proper x-axis labeling
    expectation_met_counts['Response'] = expectation_met_counts['Response'].astype(str)
    
    fig_expectation = px.bar(
        expectation_met_counts, 
        x='Response', 
        y='Count', 
        title='Distribution of Responses to "To what extent your expectation was met?"',
        color='Count',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig_expectation.update_layout(xaxis_title='Response (Scale of 1-5)', yaxis_title='Count', title_x=0.5)
    st.plotly_chart(fig_expectation, use_container_width=True)
    
    # Insight
    highest_rated_score = expectation_met_counts.loc[expectation_met_counts['Count'].idxmax(), 'Response']
    
    st.info(f"💡 **Insight:** The most frequent response is **'{highest_rated_score}'**, indicating a high level of **satisfaction** among the students surveyed, with their expectations generally being met or exceeded since the lower scores (1 and 2) have significantly fewer counts.")
else:
    st.info(f"Cannot display plot for missing column: '{EXPECTATION_COL}'.")

st.markdown("---")
st.success("✅ Dashboard analysis complete!")
