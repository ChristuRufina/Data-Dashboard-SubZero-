import streamlit as st 
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
import os
import plotly.express as px
from PIL import Image

load_dotenv()

# OpenAI API Key
openai_api_key = "your api key"

# Set Streamlit page configuration
st.set_page_config(page_title='Data Dashboard', layout='wide')
st.markdown(
    """
    <style>
    body {
        background-color: white;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.header('Data Dashboard 2024 - SubZero')
st.subheader('The data dashboard of the performance of students in the university')

##--file upload
def chat_with_csv(df, prompt):
    openai = OpenAI(api_token=openai_api_key)
    pandas_ai = PandasAI(openai)
    result = pandas_ai.run(df, prompt=prompt)
    return result

st.title("ChatCSV using LLM")

input_csv = st.file_uploader("Upload your CSV file", type=['csv'])

if input_csv is not None:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("CSV Uploaded Successfully")
        data = pd.read_csv(input_csv)
        st.dataframe(data, use_container_width=True)

    with col2:
        st.info("Chat Below")
        input_text = st.text_area("Enter your query")
        
        if input_text is not None:
            if st.button("Chat with CSV"):
                st.info("Your Query: " + input_text)
                result = chat_with_csv(data, input_text)
                st.success(result)

#upload ends

# --- DISPLAY IMAGE & DATAFRAME
# col1, col2 = st.columns(2)
# image = Image.open('images/Stud.jpg')
# col1.image(image,
#             caption='By SubZero',
#             use_column_width=True)


# col1, col2, col3 = st.columns(3)

# with col1:
#     st.write(' ')

# with col2:
#     st.image('images/stud.jpg')

# with col3:
#     st.write(' ')
# col2.dataframe(df[mask])


### --- LOAD DATAFRAME
excel_file = 'Survey_Results.xlsx'  
sheet_name = 'DATA'

df = pd.read_excel(excel_file, sheet_name=sheet_name, usecols='B:D', header=3)

df_participants = pd.read_excel(excel_file, sheet_name=sheet_name, usecols='F:G', header=3)
df_participants.dropna(inplace=True)

# --- STREAMLIT SELECTION
department = df['Department'].unique().tolist()
ages = df['Attendence'].unique().tolist()

age_selection = st.slider('Attendence:',
                        min_value=min(ages),
                        max_value=max(ages),
                        value=(min(ages), max(ages)))

department_selection = st.multiselect('Department:',
                                    department,
                                    default=department)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['Attendence'].between(*age_selection)) & (df['Department'].isin(department_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['CGPA']).count()[['Attendence']]
df_grouped = df_grouped.rename(columns={'Attendence': 'No.of students'})
df_grouped = df_grouped.reset_index()


# # --- PLOT BAR CHART
# bar_chart = px.bar(df_grouped,
#                    x='CGPA',
#                    y='No.of students',
#                    text='CGPA',
#                    color_discrete_sequence=['#e694ff'] * len(df_grouped),
#                    template='plotly_white')
# st.plotly_chart(bar_chart)

# # --- PLOT PIE CHART
# pie_chart = px.pie(df_participants,
#                 title='Total No. of Participants',
#                 values='Students',
#                 names='Departments')

# st.plotly_chart(pie_chart)


st.write('\n\n\n\n')
# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                   x='CGPA',
                   y='No.of students',
                   text='CGPA',
                   color_discrete_sequence=['#e694ff'] * len(df_grouped),
                   template='plotly_white')
bar_chart.update_layout(
    title=dict(text='Bar Chart', font=dict(size=20, color='white')),  # Adjust title font size and color
    margin=dict(l=0, r=0, t=50, b=0),  # Adjust top margin to accommodate the title
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=14)),
    font=dict(size=14),
    height=400,  # Adjust height as needed
)

st.plotly_chart(bar_chart, use_container_width=True)

# Add spacer for 3 line space
st.write('\n\n\n\n')

# --- PLOT PIE CHART
pie_chart = px.pie(df_participants,
                title='Pie-Chart (Total No. of Participants)',
                values='Students',
                names='Departments',
                color='Departments',  # Use 'Departments' column for color encoding
                color_discrete_sequence=px.colors.qualitative.Pastel)  # Set color scheme
pie_chart.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))  # Add labels inside slices and set outline color and width
pie_chart.update_layout(
    margin=dict(l=20, r=20, t=70, b=20),  # Adjust margins for better appearance and to make space for the title
    font=dict(size=16, color='black'),  # Increase font size for better visibility
    height=400,  # Adjust height as needed
    showlegend=True,  # Show legend
    legend_title_text='Departments',  # Set legend title
    legend=dict(
        orientation='v',  # Set legend orientation to vertical
        yanchor='middle',  # Set legend position anchor
        y=0.5,  # Set legend position
        xanchor='right',  # Set legend position anchor
        x=1.05  # Set legend position
    ),
    title_x=0.38,  # Center the title
    title_font=dict(size=20, color='white')  # Title font size and color
)




st.plotly_chart(pie_chart, use_container_width=True)




