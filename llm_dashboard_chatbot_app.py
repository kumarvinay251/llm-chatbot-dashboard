
import streamlit as st
import pandas as pd
import openai
import matplotlib.pyplot as plt

# Set page layout
st.set_page_config(layout="wide")
st.title("📊 Supply Chain Dashboard + 💬 LLM Chatbot")

# Sidebar: Upload CSV
with st.sidebar:
    st.header("📁 Upload Dashboard Data")
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    api_key = st.text_input("🔐 OpenAI API Key", type="password")
    st.markdown("Example: Ask things like 'Which region has the highest backorders?'")

# If file and API key provided
if uploaded_file and api_key:
    openai.api_key = api_key
    df = pd.read_csv(uploaded_file)

    # Layout: Dashboard (left), Chatbot (right)
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📈 Dashboard View")
        st.dataframe(df.head())

        # Sample visualization
        if "Region" in df.columns and "Backorder_USD" in df.columns:
            st.write("### Backorder USD by Region")
            chart_data = df.groupby("Region")["Backorder_USD"].sum().sort_values(ascending=False)
            st.bar_chart(chart_data)

    with col2:
        st.subheader("🤖 Ask Your Question")
        question = st.text_area("Type your question:")
        if st.button("Ask"):
            try:
                sample_data = df.head(10).to_csv(index=False)
                prompt = f"You are a supply chain assistant. Based on this sample data:
{sample_data}

Answer the question: {question}"

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a data analyst specialized in supply chain."},
                        {"role": "user", "content": prompt}
                    ]
                )

                st.success(response.choices[0].message["content"])
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("Please upload a CSV file and enter your OpenAI API key to begin.")
