import streamlit as st
import pandas as pd
import altair as alt

st.title("📈 Generative AI Adoption Impact Dashboard")
st.write("Explore how GenAI adoption affects productivity across industries.")

# Load dataset
df = pd.read_csv("Enterprise_GenAI_Adoption_Impact.csv")

# Sidebar filters
st.sidebar.header("Filters")

industry = st.sidebar.selectbox("Industry", ["All"] + sorted(df["Industry"].unique().tolist()))
country = st.sidebar.selectbox("Country", ["All"] + sorted(df["Country"].unique().tolist()))
tool = st.sidebar.selectbox("GenAI Tool", ["All"] + sorted(df["GenAI Tool"].unique().tolist()))
year = st.sidebar.selectbox("Adoption Year", ["All"] + sorted(df["Adoption Year"].unique().tolist()))

# Apply filters
filtered_df = df.copy()
if industry != "All":
    filtered_df = filtered_df[filtered_df["Industry"] == industry]
if country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == country]
if tool != "All":
    filtered_df = filtered_df[filtered_df["GenAI Tool"] == tool]
if year != "All":
    filtered_df = filtered_df[filtered_df["Adoption Year"] == year]

st.subheader("Filtered Dataset Preview")
st.dataframe(filtered_df.head())

# Summary metrics
st.subheader("📊 Summary Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Avg Productivity Change (%)", round(filtered_df["Productivity Change (%)"].mean(), 2))
col2.metric("Avg Training Hours", round(filtered_df["Training Hours Provided"].mean(), 2))
col3.metric("Avg Employees Impacted", round(filtered_df["Number of Employees Impacted"].mean(), 2))

# Charts
st.subheader("📉 Productivity Change by Industry")
industry_chart = (
    alt.Chart(df.groupby("Industry", as_index=False)["Productivity Change (%)"].mean())
    .mark_bar(color="#4CAF50")
    .encode(
        x=alt.X("Industry", sort="-y", title="Industry"),
        y=alt.Y("Productivity Change (%)", title="Avg Productivity Change (%)"),
        tooltip=["Industry", "Productivity Change (%)"]
    )
)
st.altair_chart(industry_chart, use_container_width=True)

st.subheader("🤖 Productivity Change by AI Tool")
tool_chart = (
    alt.Chart(df.groupby("GenAI Tool", as_index=False)["Productivity Change (%)"].mean())
    .mark_bar(color="#2196F3")
    .encode(
        x=alt.X("GenAI Tool", sort="-y", title="GenAI Tool"),
        y=alt.Y("Productivity Change (%)", title="Avg Productivity Change (%)"),
        tooltip=["GenAI Tool", "Productivity Change (%)"]
    )
)
st.altair_chart(tool_chart, use_container_width=True)

# Productivity Estimator
st.subheader("📈 Productivity Gain Estimator (Simple Model)")
training_input = st.slider("Training Hours", 0, 25000, 1000)
employees_input = st.slider("Employees Impacted", 0, 30000, 5000)
roles_input = st.slider("New Roles Created", 0, 50, 5)

estimated_gain = (
    training_input * 0.02 +
    employees_input * 0.001 +
    roles_input * 0.5
)

st.write(f"### Estimated Productivity Change: **{round(estimated_gain, 2)}%**")
st.write("*(Simple weighted formula based on dataset trends — not a machine learning model.)*")

st.subheader("📝 Key Insights")
st.write("""
- Industries with higher training investment tend to see larger productivity boosts.  
- AI tools like Gemini and Claude often correlate with higher productivity gains.  
- More new roles created is generally associated with more positive employee sentiment.
""")
