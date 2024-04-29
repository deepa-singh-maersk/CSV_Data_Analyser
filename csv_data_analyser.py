import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import anthropic
import os

# Load API key from environment variable
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

client = anthropic.Anthropic(api_key=API_KEY)
def main():
    st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_icon="📊", page_title="CSV Data Analyzer")
    # st.title("📊 CSV Data Analyzer")
    st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display&display=swap');
    </style>
    """,
    unsafe_allow_html=True
)
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
    with st.expander("Upload a csv file"):
        # Upload CSV file
        uploaded_file = st.file_uploader("UPLOAD CSV", type=['csv'])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

        # Main tab
        selected_tab = st.selectbox("Select a tab:", ["Data Visualization", "Advanced Query", "Claude Insights"], index=0)

        if selected_tab == "Data Visualization":
            data_visualization(data)
        elif selected_tab == "Advanced Query":
            advanced_query(data)
        elif selected_tab == "Claude Insights":
            claude_insights(data)

def data_visualization(data):
    st.header("Data Visualization")
    with st.expander("Select Chart type and Axis to represent"):
        # Select Chart Type
        chart_type = st.selectbox("Select Chart Type", ["Scatter Plot", "Bar Chart", "Line Chart", "Histogram", "Box Plot"])

        col1, col2, col3 = st.columns([1, 1, 1])

        # Select X Axis and Y Axis
        with col1:
            x_axis = st.selectbox("Select X Axis", data.columns)
        with col2:
            y_axis = st.selectbox("Select Y Axis", data.columns)
        with col3:
            # Select Color By
            color_by = st.selectbox("Color By", data.columns)

    with st.expander("Click here to see the visuals"):
        # Update the chart in the session state
        if chart_type == "Scatter Plot":
            st.plotly_chart(px.scatter(data, x=x_axis, y=y_axis, color=color_by), use_container_width=True)
        elif chart_type == "Bar Chart":
            st.plotly_chart(px.bar(data, x=x_axis, y=y_axis, color=color_by), use_container_width=True)
        elif chart_type == "Line Chart":
            st.plotly_chart(px.line(data, x=x_axis, y=y_axis, color=color_by), use_container_width=True)
        elif chart_type == "Histogram":
            st.plotly_chart(px.histogram(data, x=x_axis), use_container_width=True)
        else:  # Box Plot
            st.plotly_chart(px.box(data, x=x_axis, y=y_axis, color=color_by), use_container_width=True)

def advanced_query(data):
    st.header("Advanced Query")
    with st.expander("Custom Query"):
        query = st.text_area("Write your custom query using Pandas syntax:", "data.head(3)", height=150)
        if st.button("Run Query"):
            execute_query(data, query)

    # Query Result
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

def claude_insights(data):
    st.header("Claude AI-powered Data Insights")
    with st.expander("Get Insights"):
        question = st.text_area("Ask questions about your data, and let Claude AI provide insights.")
        if st.button("Get Insights"):
            with st.spinner("Fetching insights..."):
                insights = get_data_insights(data, question)
                with st.container():
                    st.write(insights)

# Helper function to execute custom query
def execute_query(data, query):
    try:
        result_df = eval(query)
        st.session_state.query_result = result_df
    except Exception as e:
        st.error(f"Error: {e}")

# Helper function to get data insights from Anthropic API
def get_data_insights(data, question):
    if data.empty:
        return "No data provided for analysis."

    full_question = f"Given the following tabular data:\n{data.to_string(index=False)}\n\nQuestion: {question}\n\nInsights:"
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=512,
        messages=[
            {"role": "user", "content": full_question}
        ]
    )

    if response.content and isinstance(response.content, list) and len(response.content) > 0:
        text_block = response.content[0]
        if hasattr(text_block, 'text'):
            content = text_block.text
            return content
        else:
            return "Error: Unexpected response format."
    else:
        return "Error: No content received from the API."

if __name__ == "__main__":
    main()
