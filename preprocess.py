import pandas as pd
import re
from sklearn.model_selection import train_test_split

# Load the dataset
file_path = 'marketing_sample_for_trulia_com-real_estate__20190901_20191031__30k_data.csv'  # Replace with the actual path to your dataset
df = pd.read_csv(file_path)

# Display basic information about the dataset
print(f"Total Records: {df.shape[0]}")
print(f"Available Fields: {list(df.columns)}")

# Drop columns that are not useful for keyword extraction
columns_to_drop = [
    'Apply Url', 'Apply Email', 'Employer Email', 'Employer Website',
    'Employer Phone', 'Employer Logo', 'Employer Location', 'Employer City',
    'Employer State', 'Employer Country', 'Employer Zip Code', 'Address',
    'Zip Code', 'Crawl Timestamp', 'Uniq Id', 'Employees', 'Companydescription'
]
df.drop(columns=columns_to_drop, inplace=True)

# Handle missing values
df.fillna('', inplace=True)

# Function to clean the job description text
def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    return text

# Apply the text cleaning function to job descriptions
df['Job Description'] = df['Job Description'].apply(clean_text)

# Feature selection: select relevant columns for keyword extraction
df = df[['Job Title', 'Job Description', 'Job Type', 'Categories', 'Location', 'City', 'State', 'Country', 'Industry']]

# Optional: Split data into training and test sets for model development
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Save preprocessed data to CSV files
train_df.to_csv('preprocessed_train_data.csv', index=False)
test_df.to_csv('preprocessed_test_data.csv', index=False)

# Output a preview of the preprocessed data
print("Preprocessing complete. Sample data:")
print(train_df.head())

