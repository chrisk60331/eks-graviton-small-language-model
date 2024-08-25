import pandas as pd
from rake_nltk import Rake
import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')
# Load the preprocessed dataset
file_path = 'preprocessed_train_data.csv'  # Replace with your preprocessed data file path
df = pd.read_csv(file_path)

# Initialize RAKE for keyword extraction
rake = Rake()

# Function to extract keywords from job descriptions
def extract_keywords(text):
    rake.extract_keywords_from_text(text)
    return ', '.join(rake.get_ranked_phrases())

# Apply keyword extraction to the job descriptions
df['Keywords'] = df['Job Description'].apply(extract_keywords)

# Display the dataframe with extracted keywords
print(df[['Job Title', 'Keywords']].head())

# Save the results to a new CSV file
df.to_csv('job_descriptions_with_keywords.csv', index=False)
