import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Class 9 Performance Tracker", layout="wide")

# 2. Project Header
st.title("🎓 Class 9 Report Card & Performance Tracker")
st.markdown("An interactive web app to track, filter, and analyze student performances across core subjects.")

# 3. Generating Data using NumPy and Pandas
students = ["Aarav", "Bhavna", "Chirag", "Divya", "Esha", "Farhan", "Gaurav", "Ishita", "Kabir", "Meera"]

# Set random seed so the marks stay consistent every time the app reruns
np.random.seed(42)

# Generate random marks between 40 and 100 for core Class 9 subjects using NumPy
math_marks = np.random.randint(40, 101, size=10)
science_marks = np.random.randint(40, 101, size=10)
english_marks = np.random.randint(40, 101, size=10)

# Create a Pandas DataFrame to store student records
data = {
    "Student Name": students,
    "Mathematics": math_marks,
    "Science": science_marks,
    "English": english_marks
}
df = pd.DataFrame(data)

# Calculate Total and Average Marks using Pandas row operations
df["Total Marks"] = df[["Mathematics", "Science", "English"]].sum(axis=1)
df["Percentage (%)"] = round(df[["Mathematics", "Science", "English"]].mean(axis=1), 2)

# Use NumPy conditional mapping (np.select) to award Grades based on Percentage
conditions = [
    (df["Percentage (%)"] >= 90),
    (df["Percentage (%)"] >= 75) & (df["Percentage (%)"] < 90),
    (df["Percentage (%)"] >= 50) & (df["Percentage (%)"] < 75),
    (df["Percentage (%)"] < 50)
]
grades = ["A+ (Excellent)", "A (Very Good)", "B (Good)", "C (Needs Improvement)"]
df["Grade"] = np.select(conditions, grades, default="F")

# Sort students by their performance to calculate Class Rank
df = df.sort_values(by="Percentage (%)", ascending=False).reset_index(drop=True)
df.index = df.index + 1  # Make index start from 1 instead of 0 for easy ranking
df.index.name = "Class Rank"

# 4. Sidebar Interface for Interactive Filtering
st.sidebar.header("🔍 Filter Options")

# Feature A: View individual student report card
selected_student = st.sidebar.selectbox("Select a Student to view Report Card:", df["Student Name"].unique())

# Feature B: Filter class list by minimum percentage threshold
min_pct = st.sidebar.slider("Minimum Percentage Threshold:", min_value=40, max_value=100, value=50)
filtered_df = df[df["Percentage (%)"] >= min_pct]

# 5. Main Dashboard Display
# Section A: Overview Metrics
st.subheader("📊 Class Summary Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Class Average Percentage", value=f"{round(df['Percentage (%)'].mean(), 2)}%")
with col2:
    st.metric(label="Highest Percentage Scored", value=f"{df['Percentage (%)'].max()}%", delta=df.loc[1, 'Student Name'])
with col3:
    st.metric(label="Total Students Tracked", value=len(df))

st.markdown("---")

# Section B: The Filtered Class Standings Data Table
st.subheader(f"🏆 Class Standings (Showing students with ≥ {min_pct}%)")
st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")

# Section C: Individual Student Report Card Generator
st.subheader(f"📄 Report Card: {selected_student}")
student_row = df[df["Student Name"] == selected_student]

r_col1, r_col2, r_col3 = st.columns(3)
r_col1.write(f"**Class Rank:** #{student_row.index[0]}")
r_col2.write(f"**Final Grade:** {student_row['Grade'].values[0]}")
r_col3.write(f"**Aggregate Percentage:** {student_row['Percentage (%)'].values[0]}%")

# Prepare data for visualization
subject_marks = [
    int(student_row["Mathematics"].values[0]),
    int(student_row["Science"].values[0]),
    int(student_row["English"].values[0])
]
chart_data = pd.DataFrame({
    "Subject": ["Mathematics", "Science", "English"],
    "Marks": subject_marks
}).set_index("Subject")

# Display a bar chart of individual performance
st.bar_chart(chart_data)
