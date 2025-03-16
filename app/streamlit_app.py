import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned data
st.set_page_config(layout="wide")
df = pd.read_feather('../data/cleaned_data.feather')

st.sidebar.header('Filters')
# Gender Filer
gender_options = ['All', 'Male', 'Female']
selected_gender = st.sidebar.selectbox('Select Gender', gender_options)

# Age Range Filter
min_age = int(df['BSDAGE'].min())
max_age = int(df['BSDAGE'].max())
age_range = st.sidebar.slider('Select Age Range', min_value=min_age, max_value=max_age, value=(min_age, max_age))

# School Selector
selected_schools = df['IDSCHOOL'].unique().tolist()
selected_schools.insert(0, 'All')
selected_schools = st.sidebar.multiselect('Select Schools', selected_schools, default=selected_schools[:6])

# Mathematics Performance Filter
df['Math_Avg'] = df[['BSMMAT01', 'BSMMAT02', 'BSMMAT03', 'BSMMAT04', 'BSMMAT05']].mean(axis=1)
min_score = int(df['Math_Avg'].min())
max_score = int(df['Math_Avg'].max())
math_score_range = st.sidebar.slider('Select Math Score Range', min_value=min_score, max_value=max_score, value=(min_score, max_score))

# Home Resources Count
home_resources = df[['BSBG05A', 'BSBG05B', 'BSBG05C', 'BSBG05D', 'BSBG05E', 'BSBG05F', 'BSBG05G', 'BSBG05H', 'BSBG05I', 'BSBG05J']].sum(axis=1)
df['Home_Resources_Count'] = home_resources
min_resources = int(df['Home_Resources_Count'].min())
max_resources = int(df['Home_Resources_Count'].max())
resources_range = st.sidebar.slider('Select Home Resources Count', min_value=min_resources, max_value=max_resources, value=(min_resources, max_resources))

# Apply Filters
if selected_gender != 'All':
    gender_filter = 1.0 if selected_gender == 'Male' else 2.0
    filtered_df = df[
        (df['ITSEX'] == gender_filter) &
        (df['BSDAGE'].between(age_range[0], age_range[1])) &
        ((df['IDSCHOOL'].isin(selected_schools)) if 'All' not in selected_schools else True) &
        (df['Math_Avg'].between(math_score_range[0], math_score_range[1])) &
        (df['Home_Resources_Count'].between(resources_range[0], resources_range[1]))
    ]
else:
    filtered_df = df[
        (df['BSDAGE'].between(age_range[0], age_range[1])) &
        ((df['IDSCHOOL'].isin(selected_schools)) if 'All' not in selected_schools else True) &
        (df['Math_Avg'].between(math_score_range[0], math_score_range[1])) &
        (df['Home_Resources_Count'].between(resources_range[0], resources_range[1]))
    ]

# Page selection using tabs
Overview, MathScores, StudentAttitudes, Demographics = st.tabs(['Overview', 'Math Scores', 'Student Attitudes', 'Demographics'])

with Overview:
    st.header('Overview')

    # Count of Unique Schools & Students
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

        fig, ax = plt.subplots(figsize=(5, 5))
        gender_labels = gender_counts.index.tolist()
        wedges, texts, autotexts = ax.pie(
            gender_counts, 
            labels=gender_labels,
            colors=['blue', 'pink'],
            autopct='%1.1f%%', 
            startangle=140
        )
        ax.set_title('Distribution of Male and Female', color="black")
        st.pyplot(fig)
    with col2:
        # Count plot for male and female
        st.subheader("Count Plot for Gender")
        fig, ax = plt.subplots(figsize=(5, 5))
        sns.countplot(x='ITSEX', data=filtered_df, palette=['blue', 'pink'], ax=ax)
        ax.set_xticklabels(['Male', 'Female'])
        ax.set_xlabel('Gender')
        ax.set_ylabel('Count')
        ax.set_title('Count Plot for Gender')
        st.pyplot(fig)
        
    # Bar Chart - Student Count per School
    st.subheader("Student Count per School")
    school_counts = filtered_df["IDSCHOOL"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 3), facecolor="none")
    school_counts.plot(kind="bar", ax=ax, color="blue")
    ax.set_facecolor("none")
    fig.patch.set_alpha(0)

    ax.set_xlabel("School ID")
    ax.set_ylabel("Number of Students")
    ax.set_title("Number of Students per School")
    st.pyplot(fig)
    
with MathScores:
    st.header('Math Scores')
    
    # Calculate statistics
    mean_math = filtered_df['Math_Avg'].mean()
    median_math = filtered_df['Math_Avg'].median()
    std_math = filtered_df['Math_Avg'].std()
    
    st.subheader("Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Mean", f"{mean_math:.2f}")
    col2.metric("Median", f"{median_math:.2f}")
    col3.metric("Standard Deviation", f"{std_math:.2f}")
    col11, col12 = st.columns(2)
    with col11:
        # Histogram of Math Scores
        st.subheader("Histogram of Math Scores")
        plt.figure(figsize=(5, 5))
        plt.hist(filtered_df['Math_Avg'], bins=20, color='blue', edgecolor='black')
        plt.title('Distribution of Math Scores')
        plt.xlabel('Score')
        plt.ylabel('Frequency')
        st.pyplot(plt)
    with col12:
        # Density plot of Math Scores
        st.subheader("Density Plot of Math Scores")
        plt.figure(figsize=(5, 5))
        sns.kdeplot(filtered_df['Math_Avg'], shade=True, color='blue')
        plt.title('Density of Math Scores')
        plt.xlabel('Score')
        plt.ylabel('Density')
        st.pyplot(plt)
        st.subheader("Numeracy, Algebra, and Geometry Scores")
        
    numeracy_scores = ['BSMNUM01', 'BSMNUM02', 'BSMNUM03', 'BSMNUM04', 'BSMNUM05']
    algebra_scores = ['BSMALG01', 'BSMALG02', 'BSMALG03', 'BSMALG04', 'BSMALG05']
    geometry_scores = ['BSMGEO01', 'BSMGEO02', 'BSMGEO03', 'BSMGEO04', 'BSMGEO05']
    
    filtered_df['Numeracy_Avg'] = filtered_df[numeracy_scores].mean(axis=1)
    filtered_df['Algebra_Avg'] = filtered_df[algebra_scores].mean(axis=1)
    filtered_df['Geometry_Avg'] = filtered_df[geometry_scores].mean(axis=1)
    
    # Histograms for Numeracy, Algebra, and Geometry Scores
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Numeracy Scores")
        plt.figure(figsize=(5, 5))
        plt.hist(filtered_df['Numeracy_Avg'], bins=20, color='blue', edgecolor='black')
        plt.title('Distribution of Numeracy Scores')
        plt.xlabel('Score')
        plt.ylabel('Frequency')
        st.pyplot(plt)
    
    with col2:
        st.subheader("Algebra Scores")
        plt.figure(figsize=(5, 5))
        plt.hist(filtered_df['Algebra_Avg'], bins=20, color='green', edgecolor='black')
        plt.title('Distribution of Algebra Scores')
        plt.xlabel('Score')
        plt.ylabel('Frequency')
        st.pyplot(plt)
    
    with col3:
        st.subheader("Geometry Scores")
        plt.figure(figsize=(5, 5))
        plt.hist(filtered_df['Geometry_Avg'], bins=20, color='red', edgecolor='black')
        plt.title('Distribution of Geometry Scores')
        plt.xlabel('Score')
        plt.ylabel('Frequency')
        st.pyplot(plt)
        
    # Effect of home possessions on average score
    st.subheader("Effect of Home Possessions on Average Math Score")
    home_possessions = ['BSBG05A', 'BSBG05B', 'BSBG05C', 'BSBG05D', 'BSBG05E', 'BSBG05F']
    melted_df = filtered_df.melt(id_vars=['Math_Avg'], value_vars=home_possessions, var_name='Possession', value_name='Has_Possession')
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Possession', y='Math_Avg', hue='Has_Possession', data=melted_df, palette='viridis')
    plt.title('Effect of Home Possessions on Average Math Score')
    plt.xlabel('Home Possession')
    plt.ylabel('Average Math Score')
    plt.xticks(ticks=range(len(home_possessions)), labels=['Owns Computer', 'Shared Computer', 'Smartphone', 'Internet Access', 'Desk', 'Own Room'], rotation=90)
    st.pyplot(plt)
    
    # Parental Involvement in Education
    st.subheader("Parental Involvement in Education")
    parental_involvement_columns = ['BSDGEDUP', 'BSBM23H']
    melted_df = filtered_df.melt(id_vars=['Math_Avg'], value_vars=parental_involvement_columns, var_name='Activity', value_name='Frequency')
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Activity', y='Math_Avg', hue='Frequency', data=melted_df, palette='viridis')
    plt.title('Parental Involvement in Education and Average Math Score')
    plt.xlabel('Parental Involvement Activity')
    plt.ylabel('Average Math Score')
    plt.xticks(ticks=range(len(parental_involvement_columns)), labels=['Parents\' Highest Education Level', 'Parents Think Math Important'], rotation=45)
    st.pyplot(plt)
    
    # Scatter plot - School Size vs Average Math Score
    st.subheader("School Size vs. Average Math Score")
    school_size = filtered_df.groupby('IDSCHOOL')['IDSTUD'].count().reset_index(name='School_Size')
    avg_math_score = filtered_df.groupby('IDSCHOOL')['Math_Avg'].mean().reset_index(name='Avg_Math_Score')
    school_data = pd.merge(school_size, avg_math_score, on='IDSCHOOL')
    plt.figure(figsize=(10, 5))
    sns.scatterplot(x='School_Size', y='Avg_Math_Score', data=school_data)
    plt.title('School Size vs. Average Math Score')
    plt.xlabel('School Size (Number of Students)')
    plt.ylabel('Average Math Score')
    st.pyplot(plt)


with StudentAttitudes:
    st.header('Student Attitudes')
    
    # Calculate averages for each category
    df['Math_Knowledge_Avg'] = df[['BSMKNO01', 'BSMKNO02', 'BSMKNO03', 'BSMKNO04', 'BSMKNO05']].mean(axis=1)
    df['Math_Application_Avg'] = df[['BSMAPP01', 'BSMAPP02', 'BSMAPP03', 'BSMAPP04', 'BSMAPP05']].mean(axis=1)
    df['Math_Reasoning_Avg'] = df[['BSMREA01', 'BSMREA02', 'BSMREA03', 'BSMREA04', 'BSMREA05']].mean(axis=1)
    
    # Bar chart for average scores
    st.subheader("Average Scores for Math and Science Categories")
    categories = ['Math_Knowledge_Avg', 'Math_Application_Avg', 'Math_Reasoning_Avg']
    avg_scores = df[categories].mean()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    avg_scores.plot(kind='bar', ax=ax, color=['blue', 'green', 'red'])
    ax.set_xlabel('Category')
    ax.set_ylabel('Average Score')
    ax.set_title('Average Scores for Math')
    st.pyplot(fig)
    
    # Histograms for each category
    st.subheader("Histograms for Math")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Math Knowledge")
        fig, ax = plt.subplots(figsize=(5, 5))
        sns.histplot(df['Math_Knowledge_Avg'], bins=20, kde=True, ax=ax)
        ax.set_xlabel('Score')
        ax.set_ylabel('Count')
        ax.set_title('Math Knowledge')
        st.pyplot(fig)
        
        
    with col2:
        st.subheader("Math Application")
        fig, ax = plt.subplots(figsize=(5, 5))
        sns.histplot(df['Math_Application_Avg'], bins=20, kde=True, ax=ax)
        ax.set_xlabel('Score')
        ax.set_ylabel('Count')
        ax.set_title('Math Application')
        st.pyplot(fig)
        
    st.subheader("Math Reasoning")
    fig, ax = plt.subplots(figsize=(5, 5))
    sns.histplot(df['Math_Reasoning_Avg'], bins=20, kde=True, ax=ax)
    ax.set_xlabel('Score')
    ax.set_ylabel('Count')
    ax.set_title('Math Reasoning')
    st.pyplot(fig)
    
with Demographics:
    st.header('Demographics')
    col1, col2 = st.columns(2)
    with col1:
        # Age Distribution
        st.subheader("Age Distribution")
        fig, ax = plt.subplots(figsize=(5, 5))
        sns.histplot(filtered_df['BSDAGE'], bins=20, kde=True, ax=ax)
        ax.set_xlabel('Age')
        ax.set_ylabel('Count')
        ax.set_title('Age Distribution')
        st.pyplot(fig)
    with col2:
        # Home Resources Distribution
        st.subheader("Home Resources Distribution")
        fig, ax = plt.subplots(figsize=(5, 5))
        sns.histplot(filtered_df['Home_Resources_Count'], bins=20, kde=True, ax=ax)
        ax.set_xlabel('Home Resources Count')
        ax.set_ylabel('Count')
        ax.set_title('Home Resources Distribution')
        st.pyplot(fig)
    
    # Highest level of education attained by parents
    st.subheader("Highest Level of Education Attained by Parents")
    education_columns = ['BSBG05A', 'BSBG05B', 'BSBG05C', 'BSBG05D', 'BSBG05E', 'BSBG05F', 'BSBG05G', 'BSBG05H', 'BSBG05I', 'BSBG05J']
    education_counts = filtered_df[education_columns].sum()
    fig, ax = plt.subplots(figsize=(10, 5))
    education_counts.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_xlabel('Education Level')
    ax.set_ylabel('Count')
    ax.set_title('Highest Level of Education Attained by Parents')
    st.pyplot(fig)
    
    # Primary languages spoken by students
    st.subheader("Primary Languages Spoken by Students")
    language_column = 'ITLANG_SQ'
    filtered_df['Language'] = filtered_df[language_column].map({1: 'English', 41: 'Irish'})
    language_counts = filtered_df['Language'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 5))
    language_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    ax.set_ylabel('')
    ax.set_title('Primary Languages Spoken by Students')
    st.pyplot(fig)
    
    # Parental Involvement in Education
    st.subheader("Parental Involvement in Education")
    parental_involvement_columns = ['BSDGEDUP', 'BSBM23H']
    melted_df = filtered_df.melt(value_vars=parental_involvement_columns, var_name='Activity', value_name='Response')
    plt.figure(figsize=(12, 6))
    sns.countplot(x='Activity', hue='Response', data=melted_df, palette='viridis')
    plt.title('Parental Involvement in Education')
    plt.xlabel('Parental Involvement Activity')
    plt.ylabel('Count of Responses')
    plt.xticks(ticks=[0, 1], labels=['Parents\' Highest Education Level', 'Parents Think Math is Important'], rotation=45)
    st.pyplot(plt)