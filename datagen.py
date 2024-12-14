from faker import Faker  # To generate synthetic data
import pandas as pd     # For handling tabular data
import random           # For generating random choices
import numpy as np      # For numerical operations

faker = Faker()

# Define Computer Science Domain Skills
cs_skills = [
    "Python", "Java", "C++", "JavaScript", "SQL", "HTML", "CSS", "React.js", "Node.js", 
    "Django", "Flask", "Machine Learning", "Deep Learning", "Data Analysis", 
    "Artificial Intelligence", "Cloud Computing", "Cybersecurity", "DevOps", 
    "Blockchain", "Docker", "Kubernetes", "TensorFlow", "PyTorch", "Scikit-learn", 
    "Natural Language Processing", "Computer Vision", "Linux", "Networking", 
    "Version Control (Git)", "Agile Development", "Database Design", 
    "Big Data", "AWS", "Azure", "Google Cloud", "UI/UX Design", 
    "Data Structures", "Algorithms", "System Design", "Web Development", 
    "Mobile Development", "RESTful APIs", "GraphQL", "Software Testing"
]

# Define the fields and generate data
def generate_data(num_records):
    data = []
    for _ in range(num_records):
        data.append({
            "username": faker.user_name(),
            "email": faker.email(),
            "phone": faker.phone_number(),
            "full_name": faker.name(),
            "gender": random.choice(["Male", "Female", "Other"]),
            "dob": faker.date_of_birth(minimum_age=18, maximum_age=65),
            "zip": faker.zipcode(),
            "city": faker.city(),
            "country": faker.country(),
            "state": faker.state(),
            "address": faker.address(),
            "professional_title": faker.job(),
            "company_name": faker.company(),
            "years_of_experience": random.randint(0, 40),
            "upload_resume": f"{faker.file_path(extension='pdf')}",
            "upload_experience_letter": f"{faker.file_path(extension='pdf')}",
            "industry": faker.bs().title(),
            "employed": random.choice(["Yes", "No"]),
            "unemployed": random.choice(["Yes", "No"]),
            "skills": ", ".join(random.sample(cs_skills, k=random.randint(3, 7))),  # Only Computer Science skills
            "responsibilities": faker.text(max_nb_chars=200),
            "school_name": faker.company(),
            "degree": random.choice(["Bachelors", "Masters", "PhD"]),
            "graduation_year": random.randint(1990, 2023),
            "major": random.choice(["Computer Science", "Information Technology", "Engineering"]),
            "certifications": faker.text(max_nb_chars=50),
            "date_obtained": faker.date(),
            "registration_number": faker.uuid4(),
            "preferred_title": random.choice(["Software Engineer", "Data Analyst", "Manager"]),
            "employment_type": random.choice(["Full-time", "Part-time", "Contract"]),
            "desired_job_location": faker.city(),
            "notice_period": random.choice(["1 Month", "2 Months", "Immediate"]),
            "current_salary": random.randint(30000, 1500000),
            "expected_salary": random.randint(50000, 2000000),
            "preferred_industry": "Technology",
            "reference_name": faker.name(),
            "reference_phone": faker.phone_number(),
            "work_authorization": random.choice(["Authorized", "Not Authorized"]),
            "availability": faker.date_this_month(),
            "linkedin": faker.url(),
            "twitter": faker.url(),
            "instagram": faker.url(),
            "facebook": faker.url(),
            "other_social_media": faker.url()
        })
    return pd.DataFrame(data)

# Generate 1000 sample records
sample_data = generate_data(1000)

# Save synthetic data to CSV
sample_data.to_csv("synthetic_data.csv", index=False)

# Load the saved CSV for preprocessing
data = pd.read_csv("synthetic_data.csv")

# ----------------------------------------------------------
# **2. Preprocessing the Data**
# ----------------------------------------------------------

# **2.1 Handle Missing Values**
# Simulate missing values for realistic scenarios
data.loc[data.sample(frac=0.05).index, 'email'] = np.nan  # 5% missing emails
data.loc[data.sample(frac=0.02).index, 'phone'] = np.nan  # 2% missing phone numbers

# Fill missing values for categorical data
data['email'].fillna('unknown@example.com', inplace=True)
data['phone'].fillna('Not Provided', inplace=True)

# **2.2 Normalize Text**
# Convert all text fields to lowercase for uniformity
text_fields = ['username', 'full_name', 'city', 'state', 'country', 'address', 'professional_title']
for field in text_fields:
    data[field] = data[field].str.lower()

# **2.3 Convert Dates**
# Ensure all date fields are properly formatted
data['dob'] = pd.to_datetime(data['dob'])
data['date_obtained'] = pd.to_datetime(data['date_obtained'], errors='coerce')

# **2.4 Feature Engineering**
# Add new columns such as age and experience categories
data['age'] = (pd.Timestamp.now() - data['dob']).dt.days // 365
data['experience_category'] = pd.cut(
    data['years_of_experience'],
    bins=[0, 5, 10, 20, 40],
    labels=["Beginner", "Intermediate", "Experienced", "Expert"]
)

# **2.5 Remove Duplicates**
# Check and remove duplicate entries
data.drop_duplicates(inplace=True)

# **2.6 Save Cleaned Data**
data.to_csv("preprocessed_data.csv", index=False)

print("Synthetic data generated and preprocessed successfully!")
