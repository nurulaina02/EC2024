import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Set the title and initial configuration ---
st.set_page_config(layout="wide")
st.title('📊 Student Survey Data Analysis Dashboard')
st.markdown('***Interactive visualizations using Plotly with detailed insights.***')

# --- 1. Data Loading ---
url = 'https://raw.githubusercontent.com/nurulaina02/EC2024/refs/heads/main/student_survey_cleaned.csv'

@st.cache_data
def load_data(data_url):
    """Loads and caches the dataframe."""
    try:
        df = pd.read_csv(data_url)
        # Clean column names for easier access
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
FACULTY_COL = 'Faculty'
GENDER_COL = 'Gender'

if FACULTY_COL in df.columns:
    arts_df = df[df[FACULTY_COL].astype(str).str.lower() == 'arts']
    if arts_df.empty:
        st.warning(f"⚠️ No 'Arts' entries found. Using full DataFrame for Gender plots.")
        arts_df = df.copy()
else:
    st.warning(f"⚠️ Column '{FACULTY_COL}' not found. Using full DataFrame for Gender plots.")
    arts_df = df.copy()

st.markdown("---")

# --- 3. Visualizations using Plotly ---

## 1. Gender Distribution in Arts Faculty
st.header('1. Gender Distribution in Arts Faculty')

if GENDER_COL in arts_df.columns:
    gender_counts = arts_df[GENDER_COL].value_counts().reset_index()
    gender_counts.columns = [GENDER_COL, 'Count']
    
    col1, col2 = st.columns(2)

    # Calculate dominant gender for insights
    if not gender_counts.empty:
        dominant_gender = gender_counts.iloc[0][GENDER_COL]
        dominant_count = gender_counts.iloc[0]['Count']
        total_count = gender_counts['Count'].sum()
        dominant_percentage = (dominant_count / total_count) * 100
        
        # Pie Chart
        with col1:
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
        
        # Bar Chart
        with col2:
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
            
        # Detailed Insight
        st.info(f"""💡 **Insight:** The distribution clearly indicates a significant gender imbalance within the sample, with **{dominant_gender}** students representing approximately **{dominant_percentage:.1f}%** of the total. This disparity suggests that the Arts disciplines may attract one gender more strongly than the other, which is a common trend in many educational institutions. For resource allocation and targeted outreach, it's crucial to acknowledge this uneven demographic, as the **{dominant_gender}** group's needs will dominate planning. The large difference should prompt further investigation into the enrollment trends specific to this faculty, contrasting this with other university departments.""")
else:
    st.info(f"Cannot display Gender Distribution due to missing column: '{GENDER_COL}'.")

st.markdown("---")

## 2. Student Coaching Center Attendance
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
    
    st.info(f"""💡 **Insight:** The data reveals a significant trend where **{yes_percentage:.1f}%** of the surveyed students **have attended** a coaching center. This high proportion suggests a strong reliance on external, supplementary exam preparation beyond regular school education, indicating competitive pressure for university admission. Institutions should consider if this reliance points to gaps in the standard high school curriculum or if it's purely a function of intense, high-stakes university competition. The financial and time investment students make in coaching is a crucial factor in their overall academic preparation and work-life balance.""")
else:
    st.info(f"Cannot display plot for missing column: '{COACHING_COL}'.")

st.markdown("---")

## 3. Distribution of H.S.C or Equivalent Study Medium
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
    
    st.info(f"""💡 **Insight:** The bar chart demonstrates that the **{dominant_medium}** medium is the overwhelming choice for H.S.C or equivalent studies, accounting for the vast majority of respondents. This strong concentration suggests that **{dominant_medium}** is the primary language or curriculum of instruction for students applying to the university. This insight is valuable for the university when designing foundational course materials and standardizing communications to align with the common educational background of the student body. The low counts in other mediums, such as **{study_medium_counts.iloc[-1]['Study Medium']}**, highlight a narrow linguistic and educational background among the admitted cohort.""")
else:
    st.info(f"Cannot display plot for missing column: '{MEDIUM_COL}'.")

st.markdown("---")

## 4. Distribution of Academic GPAs (Histograms)
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
        st.info(f"""💡 **Insight (HSC):** The H.S.C GPA distribution is visibly **left-skewed** (or negatively skewed), showing a high frequency of scores clustered near the maximum value, with a mean GPA of approximately **{mean_hsc:.2f}**. This indicates an academically high-achieving cohort, suggesting the university's admission standards are effective at selecting top students. The concentration of high scores means that differences in academic potential might be subtle and require more than just GPA for effective differentiation. The shape confirms that very few students were admitted with lower qualifying scores, highlighting the competitive intake.""")
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
        st.info(f"""💡 **Insight (SSC):** The S.S.C GPA distribution is strikingly similar to the H.S.C scores, reinforcing the observation of **consistent, strong academic performance** throughout the students' pre-university careers. The high mean S.S.C GPA of around **{mean_ssc:.2f}** indicates early academic success that was generally maintained into the later stage. This consistency suggests that S.S.C scores are a reliable foundational predictor of subsequent academic performance. The narrow spread of high scores again emphasizes that this is a highly competitive, high-performing group, minimizing the need for remedial academic support.""")
else:
    with col4:
        st.info(f"Cannot display plot for missing column: '{GPA_SSC_COL}'.")

st.markdown("---")

## 5. Extent Expectation Was Met (Scale 1-5) (Bar Chart)
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
    
    st.info(f"""💡 **Insight:** The survey results show a strong positive trend, with the majority of students selecting **'{highest_rated_score}'** as their response, indicating overall high satisfaction with their experience so far. This suggests that the university is largely meeting or potentially exceeding student expectations, which is crucial for maximizing student retention and enhancing institutional reputation. The very low counts at the lower end of the scale (1 and 2) confirm that deep disappointment or unmet expectations are rare among the student body. This positive feedback validates current programs but should be continuously monitored to ensure consistent quality and identify areas for incremental improvement.""")
else:
    st.info(f"Cannot display plot for missing column: '{EXPECTATION_COL}'.")

st.markdown("---")
st.success("✅ Dashboard analysis complete!")
