# CSV Data Analyzer

## Table of Contents
- [Introduction](#introduction)
   - [Technologies Used](#technologies-used)
- [Features](#features)
- [User Interface](#user-interface)
- [Implementation Details](#implementation-details)
   - [Main Function](#main-function)
   - [Data Visualization](#data-visualization)
   - [Advanced Query](#advanced-query)
   - [Claude AI Insights](#claude-ai-insights)
   - [Helper Functions](#helper-functions)
- [Error Handling and Robustness](#error-handling-and-robustness)
- [Usage](#usage)
- [Demo](#demo)
- [Conclusion](#conclusion)
   - [Impact and Value](#impact-and-value)

## Introduction
The CSV Data Analyzer is a web application developed as a major project for university coursework. This project aims to provide a comprehensive solution for analyzing and visualizing CSV (Comma-Separated Values) data, offering functionalities such as data visualization, advanced querying, and AI-powered data insights. The application is built using Python and leverages various libraries and APIs to enhance data analysis capabilities.

### Technologies Used
1. Streamlit: Used for building the user interface and creating interactive elements.
2. Pandas: Utilized for data manipulation, loading CSV files, and executing custom queries.
3. Plotly Express: Integrated for generating interactive charts and visualizations.
4. Base64: Employed for encoding and decoding binary data, particularly for file downloads.
5. Anthropic API: Integrated to provide AI-powered insights and data analysis capabilities.

## Features
The application offers the following features:
1. Upload CSV File: Users can upload a CSV file containing the data they wish to analyse.
2. Data Visualization: Users can select from various chart types (Scatter Plot, Bar Chart, Line Chart, Histogram, and Box Plot) and choose the columns to represent the x-axis, y-axis, and color. The selected chart is then displayed using Plotly Express.
3. Advanced Query: Users can write custom queries using Pandas syntax and execute them on the uploaded data. The query results are displayed in a tabular format, and users can download the results as a CSV file.
4. Claude AI-powered Data Insights: Users can ask questions about their data in natural language, and the application will leverage the Claude LLM to provide insightful and context-relevant responses based on the data and the user's question.

## User Interface
- The user interface of the CSV Data Analyzer is designed to be intuitive and user-friendly. It features:
- A visually appealing animated title using HTML and CSS styles.
- An upload section where users can upload CSV files for analysis.
- Three main tabs for Data Visualization, Advanced Querying, and Claude AI-powered Insights.
- Interactive elements such as dropdowns, text areas, buttons, and expandable sections for a seamless user experience.

## Implementation Details

### Main Function
The `main()` function is the entry point of the application. It sets up the Streamlit page configuration, displays the title, and handles the file upload process. Based on the user's selection from the tab menu, it calls the respective function for data visualization, advanced query, or Claude AI insights.
```
# Define the main function
def main():
    # Set Streamlit page configuration
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="📊",
        page_title="CSV Data Analyzer"
    )

    # HTML styling for the title
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display&display=swap');
        </style>
        """,
        unsafe_allow_html=True
    )

    # Animation styling for the title
    st.markdown(
        """
        <style>
        @keyframes slideIn {
          from {
            transform: translateX(-100%);
          }
          to {
            transform: translateX(0);
          }
        }
        .animated-title {
          animation: slideIn 2s ease-in-out;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display animated title
    st.markdown(
        """
        <h1 class="animated-title" style='color: #f2d75e; font-family: "Playfair Display"; display: flex; align-items: center;'>
            📊 <span>CSV Data Analyzer</span> 💡
        </h1>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state variables
    if "query_result" not in st.session_state:
        st.session_state.query_result = None

    # File upload section
    with st.expander("Upload a csv file"):
        uploaded_file = st.file_uploader("UPLOAD CSV", type=['csv'])  # Upload CSV file

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)  # Read uploaded CSV file into Pandas DataFrame

        # Main tab selection
        selected_tab = st.selectbox("Select a tab:", ["Data Visualization", "Advanced Query", "Claude Insights"], index=0)

        if selected_tab == "Data Visualization":
            data_visualization(data)  # Call data visualization function
        elif selected_tab == "Advanced Query":
            advanced_query(data)  # Call advanced query function
        elif selected_tab == "Claude Insights":
            claude_insights(data)  # Call Claude Insights function
```

### Data Visualization
The `data_visualization(data)` function allows users to select a chart type and specify the columns to represent the x-axis, y-axis, and color. It then creates the selected chart using Plotly Express and displays it within the Streamlit app.
```
# Function for data visualization tab
def data_visualization(data):
    st.header("Data Visualization")  # Display header
    with st.expander("Select Chart type and Axis to represent"):  # Expandable section
        chart_type = st.selectbox("Select Chart Type", ["Scatter Plot", "Bar Chart", "Line Chart", "Histogram", "Box Plot"])  # Select chart type

        col1, col2, col3 = st.columns([1, 1, 1])  # Divide into three columns

        # Select X, Y axis, and Color By options
        with col1:
            x_axis = st.selectbox("Select X Axis", data.columns)
        with col2:
            y_axis = st.selectbox("Select Y Axis", data.columns)
        with col3:
            color_by = st.selectbox("Color By", data.columns)

    # Display chart based on user selections
    with st.expander("Click here to see the visuals"):
        if chart_type == "Scatter Plot":
            st.plotly_chart(px.scatter(data, x=x_axis, y=y_axis, color=color_by), use_container_width=True)
        elif chart_type == "Bar Chart":
            st.plotly_chart(px.bar(data, x=x_axis, y=y_axis, color=color_by), use_container_width=True)
        elif chart_type == "Line Chart":
            st.plotly_chart(px.line(data, x=x_axis, y=y_axis, color=color_by), use_container_width=True)
        elif chart_type == "Histogram":
            st.plotly_chart(px.histogram(data, x=x_axis), use_container_width=True)
        else:
            st.plotly_chart(px.box(data, x=x_axis, y=y_axis, color=color_by), use_container_width=True)
```

### Advanced Query
The `advanced_query(data)` function provides an interface for users to write custom queries using Pandas syntax. When the user runs a query, the `execute_query(data, query)` function is called, which evaluates the query and stores the result in the session state. The query result is displayed in a tabular format, and users can download the result as a CSV file.
```
# Function for advanced query tab
def advanced_query(data):
    st.header("Advanced Query")  # Display header
    with st.expander("Custom Query"):  # Expandable section
        query = st.text_area("Write your custom query using Pandas syntax:", "data.head(3)", height=150)  # Input area for custom query
        if st.button("Run Query"):
            execute_query(data, query)  # Execute custom query

    # Display query result
    if st.session_state.query_result is not None:
        st.subheader("Query Result")
        result_df = st.session_state.query_result
        with st.container():
            st.table(result_df)

        # Download button for CSV file
        csv = st.session_state.query_result.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="query_result.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)
```

### Claude AI Insights
The `claude_insights(data)` function allows users to ask questions about their data. When the user submits a question, the `get_data_insights(data, question)` function is called, which sends a request to the Anthropic API with the provided data and question. The response from the API, containing the AI-powered insights, is then displayed within the Streamlit app.
```
# Function for Claude Insights tab
def claude_insights(data):
    st.header("Claude AI-powered Data Insights")  # Display header
    with st.expander("Get Insights"):  # Expandable section
        question = st.text_area("Ask questions about your data, and let Claude AI provide insights.")  # Input area for user question
        if st.button("Get Insights"):
            with st.spinner("Fetching insights..."):
                insights = get_data_insights(data, question)  # Get data insights from Anthropics API
                with st.container():
                    st.write(insights)  # Display insights
```

### Helper Functions
The application includes the following helper functions:

- `execute_query(data, query)`: Evaluates the provided query on the data and stores the result in the session state.
```
# Helper function to execute custom query
def execute_query(data, query):
    try:
        result_df = eval(query)  # Execute custom query using eval
        st.session_state.query_result = result_df  # Store query result in session state
    except Exception as e:
        st.error(f"Error: {e}")  # Display error message if query execution fails
```
- `get_data_insights(data, question)`: Sends a request to the Anthropic API with the provided data and question, and returns the AI-powered insights from the response.
```
# Helper function to get data insights from Anthropics API
def get_data_insights(data, question):
    if data.empty:
        return "No data provided for analysis."

    # Prepare question for API call
    full_question = f"Given the following tabular data:\n{data.to_string(index=False)}\n\nQuestion: {question}\n\nInsights:"
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=512,
        messages=[
            {"role": "user", "content": full_question}
        ]
    )

    # Process API response
    if response.content and isinstance(response.content, list) and len(response.content) > 0:
        text_block = response.content[0]
        if hasattr(text_block, 'text'):
            content = text_block.text
            return content  # Return API response
        else:
            return "Error: Unexpected response format."
    else:
        return "Error: No content received from the API."
```

### Error Handling and Robustness
The application incorporates robust error-handling mechanisms to ensure smooth functioning and reliability. It checks for missing API keys, handles exceptions during query execution, and provides informative error messages to users when issues arise. This ensures a seamless user experience and prevents unexpected failures.

## Usage
- To run the application, you must install Python and the required libraries.
```
import streamlit as st  # Import Streamlit for building web apps
import pandas as pd  # Import Pandas for data manipulation
import plotly.express as px  # Import Plotly Express for data visualization
import base64  # Import base64 for encoding and decoding binary data
import anthropic  # Import Anthropics API for data insights
import os  # Import os for interacting with the operating system
```
- Install the required libraries by running `pip install streamlit pandas plotly base64 anthropic`.
- Set the `ANTHROPIC_API_KEY` environment variable on your local machine.
- Run the application with `streamlit run csv_data_analyser.py`.
- Upload a CSV file and explore the various features of the data analyzer.

## Demo
As part of this presentation, I would like to provide a live demonstration of the CSV Data Analyzer web application. Below is a video where I walk through the key features and functionalities of the app, showcasing how users can upload CSV files, visualize data, perform custom queries, and obtain AI-powered insights.
In the demo, you will see:
- Uploading a CSV file and selecting the desired chart type, axes, and color coding for data visualization.
- Writing and executing custom queries using Pandas syntax to perform advanced data analysis.
- Exploring the Claude AI-powered insights feature by asking questions about the data and receiving AI-generated insights.
  
https://github.com/Adineu03/MajorProject/assets/106646056/02f6071d-0f0b-4a0b-a96e-4774e0569ecd

## Conclusion
The CSV Data Analyzer is a dynamic solution that combines cutting-edge technologies and AI-driven insights to facilitate robust data analysis and visualization. Its intuitive interface, coupled with interactive features, caters to a wide range of users, from researchers and analysts to data enthusiasts across various industries. By streamlining data-driven decision-making processes and fostering a culture of innovation, the CSV Data Analyzer empowers users to extract actionable intelligence and drive strategic growth initiatives. Its versatility and adaptability make it a valuable asset in navigating the complexities of data analysis, ensuring that organizations and individuals can harness the full potential of their data resources. As we move towards a data-centric future, the CSV Data Analyzer plays a pivotal role in shaping how data is leveraged to derive meaningful insights, make informed decisions, and achieve transformative outcomes that drive progress and innovation.
