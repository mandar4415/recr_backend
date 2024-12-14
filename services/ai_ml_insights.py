import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

def rank_candidates_with_insights(job_title, skills, data_path="data/preprocessed_data.csv", output_dir="outputs"):
    """
    Rank candidates based on job title and skills similarity, and generate insights.
    Args:
        job_title (str): Job title to match (e.g., "Web Developer").
        skills (str): Required skills (e.g., "Python, JavaScript").
        data_path (str): Path to the CSV file containing candidate data.
        output_dir (str): Directory to save generated charts.
    Returns:
        tuple: (top candidates as a list of dicts, insights as a dict)
    """
    # Load data
    data = pd.read_csv(data_path)
    data["profile_features"] = data["professional_title"] + " " + data["skills"]
    query = job_title + " " + skills

    # TF-IDF vectorization for similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data["profile_features"])
    query_vec = vectorizer.transform([query])
    data["match_score"] = cosine_similarity(query_vec, tfidf_matrix).flatten()

    # Filter for top matches
    top_candidates = data.sort_values(by="match_score", ascending=False).head(10)

    # Generate insights
    ensure_directory_exists(output_dir)  # Ensure output directory exists
    insights = {
        "skill_distribution": generate_skill_distribution(data, job_title, output_dir),
        "salary_comparison": generate_salary_comparison(data, job_title, output_dir),
        "regional_distribution": generate_regional_distribution(data, job_title, output_dir)
    }

    # Return top candidates and insights
    return top_candidates[["full_name", "city", "skills", "match_score"]].to_dict(orient="records"), insights

def generate_skill_distribution(data, job_title, output_dir):
    """
    Generate skill distribution insights and save as a chart.
    Args:
        data (pd.DataFrame): Candidate data.
        job_title (str): Job title to filter candidates.
        output_dir (str): Directory to save the chart.
    Returns:
        dict: Top 10 skills with their counts.
    """
    # Filter data by job title
    filtered_data = data[data["professional_title"].str.contains(job_title, case=False, na=False)]
    skill_counts = pd.Series(", ".join(filtered_data["skills"]).split(", ")).value_counts()

    # Plot skill distribution
    plt.figure(figsize=(10, 6))
    skill_counts.head(10).plot(kind="bar", color="skyblue")
    plt.title(f"Top Skills for {job_title}")
    plt.xlabel("Skills")
    plt.ylabel("Frequency")
    save_chart_to_file(plt, output_dir, f"{job_title}_skill_distribution.png")
    return skill_counts.head(10).to_dict()

def generate_salary_comparison(data, job_title, output_dir):
    """
    Generate salary comparison insights and save as a chart.
    Args:
        data (pd.DataFrame): Candidate data.
        job_title (str): Job title to filter candidates.
        output_dir (str): Directory to save the chart.
    Returns:
        dict: Summary statistics for current and expected salaries.
    """
    # Filter data by job title
    filtered_data = data[data["professional_title"].str.contains(job_title, case=False, na=False)]

    # Plot salary comparison
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=filtered_data, x="current_salary", y="expected_salary", palette="coolwarm")
    plt.title(f"Current vs Expected Salary for {job_title}")
    plt.xlabel("Salary")
    plt.ylabel("Candidates")
    save_chart_to_file(plt, output_dir, f"{job_title}_salary_comparison.png")

    # Return summary statistics
    return {
        "current_salary_mean": round(filtered_data["current_salary"].mean(), 2),
        "expected_salary_mean": round(filtered_data["expected_salary"].mean(), 2)
    }

def generate_regional_distribution(data, job_title, output_dir):
    """
    Generate regional distribution insights and save as a chart.
    Args:
        data (pd.DataFrame): Candidate data.
        job_title (str): Job title to filter candidates.
        output_dir (str): Directory to save the chart.
    Returns:
        dict: Top 10 cities with their candidate counts.
    """
    # Filter data by job title
    filtered_data = data[data["professional_title"].str.contains(job_title, case=False, na=False)]

    # Count candidates by city
    city_counts = filtered_data["city"].value_counts()

    # Plot regional distribution
    plt.figure(figsize=(10, 6))
    city_counts.head(10).plot(kind="pie", autopct="%1.1f%%", startangle=140)
    plt.title(f"Regional Distribution of {job_title} Candidates")
    save_chart_to_file(plt, output_dir, f"{job_title}_regional_distribution.png")
    return city_counts.head(10).to_dict()

def ensure_directory_exists(directory):
    """
    Ensure a directory exists, creating it if necessary.
    Args:
        directory (str): Directory path.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_chart_to_file(plt, output_dir, filename):
    """
    Save a matplotlib chart to a file.
    Args:
        plt (matplotlib.pyplot): The matplotlib plotting module.
        output_dir (str): Directory to save the chart.
        filename (str): Name of the file.
    """
    file_path = os.path.join(output_dir, filename)
    plt.savefig(file_path)
    plt.close()  # Close the plot to free memory
    print(f"Chart saved to {file_path}")
