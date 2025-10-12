import pandas as pd

url = 'https://raw.githubusercontent.com/nurulaina02/EC2024/386823d030273aafee874bee9256e4e702b986d4/student_survey_cleaned.csv'
df = pd.read_csv(url)
display(df.head())
