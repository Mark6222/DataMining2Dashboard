import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned data
df = pd.read_feather('../data/cleaned_data.feather')

# Sidebar filters
st.sidebar.header('Filters')

# **1. Gender Filter**
selected_gender = st.sidebar.selectbox('Select Gender', df['ITSEX'].unique())

# **2. Age Range Filter**
min_age, max_age = int(df['BSDAGE'].min()), int(df['BSDAGE'].max())
age_range = st.sidebar.slider('Select Age Range', min_value=min_age, max_value=max_age, value=(min_age, max_age))

# **3. School Selector**
unique_schools = df['IDSCHOOL'].unique()
selected_schools = st.sidebar.multiselect('Select Schools', unique_schools, default=unique_schools[:5])  # Default: first 5

# **4. Mathematics Performance Filter**
df['Math_Avg'] = df[['BSMMAT01', 'BSMMAT02', 'BSMMAT03', 'BSMMAT04', 'BSMMAT05']].mean(axis=1)  # Compute Avg Math Score
min_score, max_score = int(df['Math_Avg'].min()), int(df['Math_Avg'].max())
math_score_range = st.sidebar.slider('Select Math Score Range', min_value=min_score, max_value=max_score, value=(min_score, max_score))

# **5. Home Resources Count (Proxy for Socioeconomic Status)**
home_resources = df[['BSBG05A', 'BSBG05B', 'BSBG05C', 'BSBG05D', 'BSBG05E', 'BSBG05F', 'BSBG05G', 'BSBG05H', 'BSBG05I', 'BSBG05J']].sum(axis=1)
df['Home_Resources_Count'] = home_resources  # Add column
min_resources, max_resources = int(df['Home_Resources_Count'].min()), int(df['Home_Resources_Count'].max())
resources_range = st.sidebar.slider('Select Home Resources Count', min_value=min_resources, max_value=max_resources, value=(min_resources, max_resources))

# **Apply Filters**
filtered_df = df[
    (df['ITSEX'] == selected_gender) &
    (df['BSDAGE'].between(age_range[0], age_range[1])) &
    (df['IDSCHOOL'].isin(selected_schools)) &
    (df['Math_Avg'].between(math_score_range[0], math_score_range[1])) &
    (df['Home_Resources_Count'].between(resources_range[0], resources_range[1]))
]

# Page selection using tabs
tab1, tab2, tab3, tab4 = st.tabs(['Overview', 'Math Scores', 'Science Scores', 'Demographics'])

with tab1:
    st.header('Overview')

    # **1. Count of Unique Schools & Students**
    num_schools = filtered_df['IDSCHOOL'].nunique()
    num_students = filtered_df['IDSTUD'].nunique()
    avg_student_age = filtered_df['BSDAGE'].mean()

    st.subheader("Key Statistics")
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Total Schools", num_schools)
    col2.metric("Total Students", num_students)
    col3.metric("Avg Student Age", f"{avg_student_age:.2f}")

    gender_counts = filtered_df['ITSEX'].value_counts()
    col1, col2 = st.columns([1.5, 2])
    with col1:
        # Plot pie chart For Gender Distribution
        st.subheader("Gender Distribution")

        fig, ax = plt.subplots(figsize=(5, 5), facecolor="none")
        ax.set_facecolor("none")
        gender_labels = gender_counts.index.tolist()
        wedges, texts, autotexts = ax.pie(
            gender_counts, 
            labels=gender_labels,
            colors=['blue', 'pink'][:len(gender_labels)],
            autopct='%1.1f%%', 
            startangle=140
        )
        for text in texts + autotexts:
            text.set_color("black")
        ax.set_title('Distribution of Male and Female', color="black")
        st.pyplot(fig)
    with col2:
        # **4. Bar Chart - Student Count per School**
        st.subheader("Student Count per School")
        school_counts = filtered_df["IDSCHOOL"].value_counts()
        fig, ax = plt.subplots(figsize=(5, 5))
        school_counts.plot(kind="bar", ax=ax, color="skyblue")
        ax.set_xlabel("School ID")
        ax.set_ylabel("Number of Students")
        ax.set_title("Number of Students per School")
        # ax.set_xticks([])
        st.pyplot(fig)

    
with tab2:
    st.header('Math Scores')

with tab3:
    st.header('Science Scores')

with tab4:
    st.header('Demographics')

