import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Configuration and Data Loading ---

st.set_page_config(layout="wide", page_title="JIE42403 Scientific Visualisation")

@st.cache_data
def load_data(file_path):
    """Loads the dataset and performs all necessary pre-processing and mapping."""
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found. Please ensure it is in the same directory.")
        st.stop()
    
    # --- Mappings and Transformations ---
    
    # 1. Gender Mappings
    df['Gender_Label'] = df['Gender'].map({0: 'Female', 1: 'Male'}).fillna('Unknown')
    
    # 2. Support Mappings
    df['Support_Label'] = df['Mental_Health_Support'].map({0: 'No Support', 1: 'Has Support'}).fillna('Unknown')
    df['Self_Harm_Label'] = df['Self_Harm'].map({0: 'No', 1: 'Yes'}).fillna('Unknown')

    # 3. Suicide Attempts Mappings (Group 1, 2, 3 as 'Yes')
    df['Suicide_Attempts_Label'] = df['Suicide_Attempts'].apply(lambda x: 'Yes' if x > 0 else 'No')
    
    # 4. Education Level Mappings (assuming codes are 0-4 as labels are unknown)
    edu_map = {0: 'Level 0', 1: 'Level 1', 2: 'Level 2', 3: 'Level 3', 4: 'Level 4'}
    df['Education_Level_Label'] = df['Education_Level'].map(edu_map).fillna('Unknown')
    
    # 5. Binning Depression_Score for Severity
    bins = [0, 4, 7, 10]
    labels = ['Low (0-4)', 'Medium (5-7)', 'High (8-10)']
    df['Depression_Severity'] = pd.cut(df['Depression_Score'], bins=bins, labels=labels, right=True, include_lowest=True)
    
    # 6. Binning Sleep_Hours for Category
    max_sleep = df['Sleep_Hours'].max()
    df['Sleep_Hours_Category'] = pd.cut(df['Sleep_Hours'], bins=[0, 5, 8, max_sleep], 
                                       labels=['<5 hrs (Deficient)', '5-8 hrs (Adequate)', '>8 hrs (High)'], 
                                       right=True, include_lowest=True)
    
    return df

DATA_FILE = 'Mental Health Classification.csv' 
df = load_data(DATA_FILE)

st.title("JIE42403 Scientific Visualisation Report: Mental Health Factors Analysis")
st.markdown("---")

# --- Tab Structure (Three Pages) ---

tab1, tab2, tab3 = st.tabs([
    "Page 1: Demographic Analysis", 
    "Page 2: Lifestyle Impact", 
    "Page 3: Intervention Analysis"
])


# ----------------------------------------------------------------------
# TAB 1: Demographic and Core Score Analysis (Objective 1)
# ----------------------------------------------------------------------
with tab1:
    st.header("Objective 1: Demographic and Core Score Analysis")
    st.markdown("""
        **Objective Statement:** To explore how demographic factors such as Gender, Age, and Education\_Level correlate with the overall severity of depression as measured by the Depression\_Score.
    """)
    st.info("""
        **Summary Box Placeholder:** [100–150 words] The visualizations on this page reveal significant differences in depression score distribution across demographic factors. The box plot shows...
    """)
    st.subheader("Visualizations")
    
    # V1.1: Depression Score by Gender (Box Plot)
    fig1_1 = px.box(
        df, x='Gender_Label', y='Depression_Score', color='Gender_Label',
        title='1.1: Depression Score Distribution by Gender',
        labels={'Gender_Label': 'Gender', 'Depression_Score': 'Depression Score'},
        category_orders={"Gender_Label": ["Female", "Male"]}
    )
    fig1_1.update_layout(showlegend=False)
    st.plotly_chart(fig1_1, use_container_width=True)

    # V1.2: Depression Score vs. Age (Scatter Plot with trend line)
    fig1_2 = px.scatter(
        df, x='Age', y='Depression_Score', trendline="ols",
        title='1.2: Depression Score vs. Age (with OLS Trendline)',
        labels={'Age': 'Age', 'Depression_Score': 'Depression Score'},
        opacity=0.5
    )
    st.plotly_chart(fig1_2, use_container_width=True)

    # V1.3: Education Level vs. Depression Severity (Heatmap)
    heatmap_data = pd.crosstab(df['Education_Level_Label'], df['Depression_Severity'])
    fig1_3 = px.imshow(
        heatmap_data, 
        text_auto=True,
        aspect="auto",
        color_continuous_scale=px.colors.sequential.YlGnBu,
        title='1.3: Education Level vs. Count of Depression Severity',
        labels={'x': 'Depression Severity', 'y': 'Education Level', 'color': 'Count'}
    )
    fig1_3.update_xaxes(side="top")
    st.plotly_chart(fig1_3, use_container_width=True)


# ----------------------------------------------------------------------
# TAB 2: Lifestyle and Behavioral Impact (Objective 2)
# ----------------------------------------------------------------------
with tab2:
    st.header("Objective 2: Lifestyle and Behavioral Impact")
    st.markdown("""
        **Objective Statement:** To analyze the relationship between key lifestyle and behavioral factors—specifically social media usage and sleep patterns—and the severity of mental health indicators, including Low\_Energy and Nervous\_Level.
    """)
    st.info("""
        **Summary Box Placeholder:** [100–150 words] The lifestyle analysis shows a clear connection between behavioral habits and mental health indicators. Specifically, the relationship between sleep...
    """)
    st.subheader("Visualizations")

    # V2.1: Social Media Hours vs. Depression Score (Scatter Plot)
    fig2_1 = px.scatter(
        df, x='SocialMedia_Hours', y='Depression_Score', 
        color='SocialMedia_Hours',
        title='2.1: Social Media Hours vs. Depression Score',
        labels={'SocialMedia_Hours': 'Social Media Hours', 'Depression_Score': 'Depression Score'},
        opacity=0.6,
        color_continuous_scale=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig2_1, use_container_width=True)

    # V2.2: Sleep Hours and Nervous Level (Bar Chart)
    # Group by Sleep Category and calculate mean Nervous_Level
    agg_df_sleep = df.groupby('Sleep_Hours_Category', observed=True)['Nervous_Level'].mean().reset_index()
    fig2_2 = px.bar(
        agg_df_sleep,
        x='Sleep_Hours_Category',
        y='Nervous_Level',
        color='Sleep_Hours_Category',
        title='2.2: Average Nervous Level by Sleep Hours Category',
        labels={'Sleep_Hours_Category': 'Sleep Hours Category', 'Nervous_Level': 'Average Nervous Level'},
        category_orders={"Sleep_Hours_Category": ['<5 hrs (Deficient)', '5-8 hrs (Adequate)', '>8 hrs (High)']}
    )
    st.plotly_chart(fig2_2, use_container_width=True)

    # V2.3: Low Energy by Social Media While Eating (Bar Chart)
    # Group by SocialMedia_WhileEating and calculate mean Low_Energy
    agg_df_eating = df.groupby('SocialMedia_WhileEating', observed=True)['Low_Energy'].mean().reset_index()
    fig2_3 = px.bar(
        agg_df_eating,
        x='SocialMedia_WhileEating',
        y='Low_Energy',
        color='SocialMedia_WhileEating',
        title='2.3: Average Low Energy by Social Media While Eating Habit (Code)',
        labels={'SocialMedia_WhileEating': 'Social Media While Eating Habit Code', 'Low_Energy': 'Average Low Energy Score'},
    )
    st.plotly_chart(fig2_3, use_container_width=True)


# ----------------------------------------------------------------------
# TAB 3: Severity and Intervention Analysis (Objective 3)
# ----------------------------------------------------------------------
with tab3:
    st.header("Objective 3: Severity and Intervention Analysis")
    st.markdown("""
        **Objective Statement:** To investigate the prevalence of severe mental health outcomes (Self\_Harm, Suicide\_Attempts) and the perceived effectiveness of different coping mechanisms (Coping\_Methods, Mental\_Health\_Support).
    """)
    st.info("""
        **Summary Box Placeholder:** [100–150 words] This analysis explores the relationship between severe outcomes and intervention strategies. The prevalence chart shows that a small but significant...
    """)
    st.subheader("Visualizations")
    
    # V3.1: Prevalence of Self-Harm and Suicide Attempts (Combined Count Plot)
    melted_df = df[['Self_Harm_Label', 'Suicide_Attempts_Label']].melt(var_name='Outcome', value_name='Status')
    count_df = melted_df.groupby(['Outcome', 'Status']).size().reset_index(name='Count')
    
    fig3_1 = px.bar(
        count_df, x='Outcome', y='Count', color='Status',
        barmode='group',
        title='3.1: Prevalence of Self-Harm and Suicide Attempts',
        labels={'Outcome': 'Outcome Type', 'Status': 'Status', 'Count': 'Count'},
        category_orders={"Status": ["No", "Yes"]}
    )
    st.plotly_chart(fig3_1, use_container_width=True)

    # V3.2: Mental Health Support vs. Depression Type (Stacked Bar Chart)
    count_support_df = df.groupby(['Depression_Type', 'Support_Label']).size().reset_index(name='Count')
    
    fig3_2 = px.bar(
        count_support_df,
        x='Depression_Type',
        y='Count',
        color='Support_Label',
        title='3.2: Mental Health Support Usage by Depression Type (Code)',
        labels={'Depression_Type': 'Depression Type Code', 'Count': 'Count of Individuals', 'Support_Label': 'Mental Health Support'},
        barmode='stack',
        category_orders={"Support_Label": ["No Support", "Has Support"]}
    )
    fig3_2.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig3_2, use_container_width=True)

    # V3.3: Coping Methods Used by High Depression Score Group (Ranked Bar Chart)
    high_depression_df = df[df['Depression_Score'] > 7]
    coping_method_counts = high_depression_df['Coping_Methods'].value_counts().reset_index()
    coping_method_counts.columns = ['Coping_Methods', 'Count']
    
    fig3_3 = px.bar(
        coping_method_counts, 
        x='Coping_Methods', 
        y='Count', 
        color='Coping_Methods',
        title='3.3: Coping Methods Used by High Depression Score Group',
        labels={'Coping_Methods': 'Coping Methods Code', 'Count': 'Frequency'},
        category_orders={"Coping_Methods": coping_method_counts['Coping_Methods'].tolist()} # Ensure sorted order
    )
    fig3_3.update_layout(showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig3_3, use_container_width=True)
