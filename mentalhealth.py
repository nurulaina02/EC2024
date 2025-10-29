import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration and Data Loading ---

st.set_page_config(layout="wide", page_title="Mental Health Classification Analysis")

@st.cache_data
def load_data(file_path):
    """Loads the dataset and performs initial transformations."""
    # NOTE: In a real-world scenario, the user would upload the file or it would be
    # in the same directory. Assuming the file is named 'Mental Health Classification.csv'
    # in the same directory as this script.
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found. Please ensure it is in the same directory as the app.py script.")
        st.stop()
    
    # 1. Define Mappings for Clarity
    df['Gender_Label'] = df['Gender'].map({0: 'Female', 1: 'Male'}).fillna('Unknown')
    df['Support_Label'] = df['Mental_Health_Support'].map({0: 'No Support', 1: 'Has Support'}).fillna('Unknown')
    
    # 2. Binning Depression_Score for Severity
    bins = [0, 4, 7, 10]
    labels = ['Low (0-4)', 'Medium (5-7)', 'High (8-10)']
    df['Depression_Severity'] = pd.cut(df['Depression_Score'], bins=bins, labels=labels, right=True, include_lowest=True)
    
    # 3. Binning Sleep_Hours for Category
    max_sleep = df['Sleep_Hours'].max()
    df['Sleep_Hours_Category'] = pd.cut(df['Sleep_Hours'], bins=[0, 5, 8, max_sleep], 
                                       labels=['<5 hrs (Deficient)', '5-8 hrs (Adequate)', f'>8 hrs (High)'], 
                                       right=True, include_lowest=True)
    
    return df

# The user's uploaded file name:
DATA_FILE = 'Mental Health Classification.csv' 
df = load_data(DATA_FILE)

st.title("JIE42403 Scientific Visualisation Report: Mental Health Factors")
st.markdown("---")


# --- Tab Structure ---

tab1, tab2, tab3 = st.tabs([
    "1. Demographic Analysis", 
    "2. Lifestyle Impact", 
    "3. Intervention Analysis"
])


# ----------------------------------------------------------------------
# TAB 1: Demographic and Core Score Analysis (Objective 1)
# ----------------------------------------------------------------------
with tab1:
    st.header("Objective 1: Demographic and Core Score Analysis")
    st.markdown("""
        To explore how **demographic factors** such as `Gender` correlate with the overall severity of mental health as measured by the **Depression Score**.
    """)
    
    # Visualization 1: Depression Score by Gender (Box Plot)
    st.subheader("Depression Score Distribution by Gender")
    fig_gender_box = px.box(
        df,
        x='Gender_Label',
        y='Depression_Score',
        color='Gender_Label',
        title='Depression Score Distribution by Gender',
        labels={'Gender_Label': 'Gender', 'Depression_Score': 'Depression Score'},
        # Order the boxes
        category_orders={"Gender_Label": ["Female", "Male"]}
    )
    fig_gender_box.update_layout(showlegend=False)
    st.plotly_chart(fig_gender_box, use_container_width=True)

    # Placeholder for the other two visualizations for the report page structure
    # (Since the user only specified one visualization per objective in their prompt)
    st.markdown("---")
    st.subheader("Placeholder Visualizations for Full Report (Not Requested in Prompt)")
    st.info("Remember to add two more visualizations here to meet the **three visualizations per page** requirement of the assignment.")


# ----------------------------------------------------------------------
# TAB 2: Lifestyle and Behavioral Impact (Objective 2)
# ----------------------------------------------------------------------
with tab2:
    st.header("Objective 2: Lifestyle and Behavioral Impact")
    st.markdown("""
        To analyze the relationship between key **lifestyle factors**—specifically **sleep patterns**—and the severity of mental health indicators, such as **Nervous Level**.
    """)

    # Visualization 2: Sleep Hours and Nervous Level (Bar Chart)
    st.subheader("Average Nervous Level by Sleep Hours Category")
    
    # Calculate the average Nervous_Level for each Sleep_Hours_Category
    agg_df_sleep = df.groupby('Sleep_Hours_Category', observed=True)['Nervous_Level'].mean().reset_index()
    agg_df_sleep.columns = ['Sleep_Hours_Category', 'Average_Nervous_Level']

    fig_sleep_bar = px.bar(
        agg_df_sleep,
        x='Sleep_Hours_Category',
        y='Average_Nervous_Level',
        color='Sleep_Hours_Category',
        title='Average Nervous Level by Sleep Hours Category',
        labels={'Sleep_Hours_Category': 'Sleep Hours Category', 'Average_Nervous_Level': 'Average Nervous Level'},
        # Ensure correct order for bar categories
        category_orders={"Sleep_Hours_Category": ['<5 hrs (Deficient)', '5-8 hrs (Adequate)', '>8 hrs (High)']}
    )
    st.plotly_chart(fig_sleep_bar, use_container_width=True)

    # Placeholder for the other two visualizations for the report page structure
    st.markdown("---")
    st.subheader("Placeholder Visualizations for Full Report (Not Requested in Prompt)")
    st.info("Remember to add two more visualizations here to meet the **three visualizations per page** requirement of the assignment.")

# ----------------------------------------------------------------------
# TAB 3: Severity and Intervention Analysis (Objective 3)
# ----------------------------------------------------------------------
with tab3:
    st.header("Objective 3: Severity and Intervention Analysis")
    st.markdown("""
        To investigate the relationship between different **Depression Types** and the use of **Mental Health Support**.
    """)

    # Visualization 3: Mental Health Support vs. Depression Type (Stacked Bar Chart)
    st.subheader("Mental Health Support Usage Distribution by Depression Type")
    
    # Count occurrences for the stacked bar chart
    count_df = df.groupby(['Depression_Type', 'Support_Label']).size().reset_index(name='Count')
    
    # Use barmode='stack' for a stacked bar chart
    fig_support_stack = px.bar(
        count_df,
        x='Depression_Type',
        y='Count',
        color='Support_Label',
        title='Mental Health Support Usage Distribution by Depression Type',
        labels={'Depression_Type': 'Depression Type Code', 'Count': 'Count of Individuals', 'Support_Label': 'Mental Health Support'},
        barmode='stack',
        # Ensure 'No Support' is at the bottom of the stack
        category_orders={"Support_Label": ["No Support", "Has Support"]}
    )
    # Improve hover text to show percentage
    fig_support_stack.update_layout(
        xaxis={'categoryorder':'total descending'}, # Order by total count
        legend_title_text='Mental Health Support'
    )
    st.plotly_chart(fig_support_stack, use_container_width=True)

    # Placeholder for the other two visualizations for the report page structure
    st.markdown("---")
    st.subheader("Placeholder Visualizations for Full Report (Not Requested in Prompt)")
    st.info("Remember to add two more visualizations here to meet the **three visualizations per page** requirement of the assignment.")
