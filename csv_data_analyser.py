import streamlit as st  # Import Streamlit for building web apps
import pandas as pd  # Import Pandas for data manipulation
import plotly.express as px  # Import Plotly Express for data visualization
import base64  # Import base64 for encoding and decoding binary data
import anthropic  # Import Anthropics API for data insights
import os  # Import os for interacting with the operating system

# Load API key from environment variable
API_KEY = os.environ.get("ANTHROPIC_API_KEY")  # Get API key from environment variable
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")  # Raise an error if API key is missing

# Initialize Anthropics client with API key
client = anthropic.Anthropic(api_key=API_KEY)

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

# Helper function to execute custom query
def execute_query(data, query):
    try:
        result_df = eval(query)  # Execute custom query using eval
        st.session_state.query_result = result_df  # Store query result in session state
    except Exception as e:
        st.error(f"Error: {e}")  # Display error message if query execution fails

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

# Entry point of the application
if __name__ == "__main__":
    main()  # Call main function to start the Streamlit app
