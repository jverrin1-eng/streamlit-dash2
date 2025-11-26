import streamlit as st
import pandas as pd

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

# --- Summary metrics ---
st.subheader("📊 Summary Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Avg Productivity Change (%)",
    round(filtered_df["Productivity Change (%)"].mean(), 2)
)

col2.metric(
    "Avg Training Hours",
    round(filtered_df["Training Hours Provided"].mean(), 2)
)

col3.metric(
    "Avg Employees Impacted",
    round(filtered_df["Number of Employees Impacted"].mean(), 2)
)

# --- Charts ---
st.subheader("📉 Productivity Change by Industry")
industry_chart = df.groupby("Industry")["Productivity Change (%)"].mean()
st.bar_chart(industry_chart)

st.subheader("🤖 Productivity Change by AI Tool")
tool_chart = df.groupby("GenAI Tool")["Productivity Change (%)"].mean()
st.bar_chart(tool_chart)

# --- 💡 Data-Driven Recommendation Based on Your Selections ---
st.subheader("💡 Data-Driven Recommendation Based on Your Selections")

rec_industry = st.selectbox(
    "Industry for recommendation",
    options=["All"] + sorted(df["Industry"].unique())
)

rec_country = st.selectbox(
    "Country for recommendation",
    options=["All"] + sorted(df["Country"].unique())
)

rec_df = filtered_df.copy()
if rec_industry != "All":
    rec_df = rec_df[rec_df["Industry"] == rec_industry]
if rec_country != "All":
    rec_df = rec_df[rec_df["Country"] == rec_country]

if rec_df.empty:
    st.info("No records for that industry / country combination under the current filters.")
else:
    by_tool = rec_df.groupby("GenAI Tool")["Productivity Change (%)"].mean().reset_index()
    by_tool = by_tool.sort_values("Productivity Change (%)", ascending=False)
    top_tool = by_tool.iloc[0]["GenAI Tool"]
    top_prod = by_tool.iloc[0]["Productivity Change (%)"]
    n_recs = rec_df[rec_df["GenAI Tool"] == top_tool].shape[0]

    st.success(
        f"Based on your selections, **{top_tool}** has the highest average "
        f"productivity change at **{top_prod:.1f}%** across **{n_recs} records** "
        f"in this subset."
    )

    min_train = int(rec_df["Training Hours Provided"].min())
    max_train = int(rec_df["Training Hours Provided"].max())
    median_train = int(rec_df["Training Hours Provided"].median())

    planned_hours = st.slider(
        "Planned training hours per employee",
        min_value=min_train,
        max_value=max_train,
        value=median_train,
    )

    train_range = max_train - min_train
    window = max(50, int(0.1 * train_range))
    close_df = rec_df[
        (rec_df["Training Hours Provided"] >= planned_hours - window)
        & (rec_df["Training Hours Provided"] <= planned_hours + window)
    ]

    if close_df.empty:
        expected_prod = rec_df["Productivity Change (%)"].mean()
        st.write(
            f"There are no companies with training hours very close to **{planned_hours}**. "
            f"Across this subset in general, average productivity change is about "
            f"**{expected_prod:.1f}%**."
        )
    else:
        expected_prod = close_df["Productivity Change (%)"].mean()
        st.write(
            f"For companies with **≈ {planned_hours}** training hours in this subset, "
            f"average productivity change has been about **{expected_prod:.1f}%**."
        )

# --- Key Insights ---
st.subheader("📝 Key Insights")
st.write("""
- Industries with higher training investment tend to see larger productivity boosts.  
- AI tools like Gemini and Claude often correlate with higher productivity gains.  
- More new roles created is generally associated with more positive employee sentiment.
""")
