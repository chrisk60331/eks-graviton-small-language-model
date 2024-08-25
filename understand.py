import pandas as pd
import torch
from transformers import BertTokenizer, BertForTokenClassification
from transformers import pipeline

# Load the preprocessed dataset
file_path = 'preprocessed_train_data.csv'  # Replace with your preprocessed data file path
df = pd.read_csv(file_path)

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('dslim/bert-base-NER')
model = BertForTokenClassification.from_pretrained('dslim/bert-base-NER')

# Initialize a pipeline for Named Entity Recognition (NER)
ner_pipeline = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Function to extract contextually relevant keywords using BERT
def extract_contextual_keywords(text):
    ner_results = ner_pipeline(text)
    keywords = [result['word'] for result in ner_results if result['score'] > 0.5]  # Filter by score if needed
    return ', '.join(keywords)

# Apply the contextual keyword extraction to the job descriptions
df['Contextual Keywords'] = df['Job Description'].apply(extract_contextual_keywords)

# Display the dataframe with contextually extracted keywords
print(df[['Job Title', 'Contextual Keywords']].head())

# Save the results to a new CSV file
df.to_csv('job_descriptions_with_contextual_keywords.csv', index=False)
