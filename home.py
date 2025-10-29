col1, col2, col3, col4 = st.columns(4)
 
# 1. Average Depression Score (Overall Severity)
col1.metric(
    label="Avg. Depression Score", 
    value="14.6", 
    help="Average Depression Score across all respondents.", 
    border=True
)

# 2. Mental Health Support Prevalence
col2.metric(
    label="Support Prevalence", 
    value="22.5%", 
    help="Percentage of respondents who utilize Mental Health Support.", 
    border=True
)

# 3. Average Sleep Hours (Key Lifestyle Factor)
col3.metric(
    label="Avg. Sleep Hours", 
    value="6.5 hrs", 
    help="Average reported daily Sleep Hours (Adequate sleep is typically 7-8 hours).", 
    border=True
)

# 4. Prevalence of High Severity
col4.metric(
    label="High Severity (Score ≥ 8)", 
    value="72.4%", 
    help="Percentage of respondents with a Depression Score of 8 or higher (indicating high severity).", 
    border=True
)
