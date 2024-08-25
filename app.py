import logging

from flask import Flask, request, jsonify
from transformers import pipeline, BertTokenizer, BertForTokenClassification

# Initialize the Flask application
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
# Load the BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('dslim/bert-base-NER-uncased')
model = BertForTokenClassification.from_pretrained('dslim/bert-base-NER-uncased')
ner_pipeline = pipeline('ner', model=model, tokenizer=tokenizer)


@app.route('/extract_keywords', methods=['POST'])
def extract_keywords():
    data = request.json
    text = data['text']
    print(text)
    ner_results = ner_pipeline(text)
    print(ner_results)
    keywords = [result['word'] for result in ner_results if result['score'] > 0.5]
    return keywords


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
