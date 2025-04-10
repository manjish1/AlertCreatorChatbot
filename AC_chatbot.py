from flask import Flask, request, jsonify, render_template
import json
import logging
from sentence_transformers import SentenceTransformer, util
import string
import docx
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the Sentence Transformer model
model_embeddings = SentenceTransformer('all-mpnet-base-v2')

# Load fine-tuned model if available, otherwise use base model
fine_tuned_model_path = "fine_tuned_model"
if os.path.exists(fine_tuned_model_path):
    model_embeddings = SentenceTransformer(fine_tuned_model_path)
    logging.info("Loaded fine-tuned model.")
else:
    logging.info("Using base model.")

# Function to load and preprocess the training manual file (.docx)
def load_and_preprocess_manual(manual_file):
    try:
        doc = docx.Document(manual_file)
        content = ""
        for paragraph in doc.paragraphs:
            content += paragraph.text + "\n"
        return content.strip()
    except Exception as e:
        logging.error(f"Error processing {manual_file}: {e}")
        return ""

# Function to retrieve relevant chunks from the training manual
def retrieve_relevant_chunks(query, manual_content, model_embeddings):
    query_embedding = model_embeddings.encode([query])
    content_embedding = model_embeddings.encode([manual_content])
    similarity = util.cos_sim(query_embedding, content_embedding).item()
    if similarity > 0.5:  # Adjust similarity threshold as needed
        return [manual_content] # Return the entire content as a single chunk
    else:
        return []

# Function to normalize text for similarity comparison
def normalize_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Function to generate response
def generate_response(query, retrieved_chunks, model_embeddings):
    try:
        with open('qa_dataset.json', 'r') as f:
            data = json.load(f)

        query_normalized = normalize_text(query)

        # 1. Check QA Dataset for Direct Match
        for item in data['train']:
            question_normalized = normalize_text(item['question'])
            if query_normalized == question_normalized:
                print(f"Exact match found in QA dataset: {query}")
                return item['answers']['text'][0]

        # 2. Check QA Dataset for Similarity Match
        query_embedding = model_embeddings.encode([query])
        for item in data['train']:
            dataset_question_embedding = model_embeddings.encode([item['question']])
            similarity = util.cos_sim(query_embedding, dataset_question_embedding).item()
            print(f"Similarity: {similarity} for {item['question']}")

            if similarity > 0.6:
                print(f"Similarity match found in QA dataset: {item['question']}")

                # 3. Combine QA answer with retrieved chunks.
                qa_answer = item['answers']['text'][0]
                #Removed the context from the manual.
                return qa_answer

        # 4. If no good match in QA dataset, use retrieved chunks
        if retrieved_chunks:
            print("Using retrieved chunks from training manual.")
            return "\n".join(retrieved_chunks)
        else:
            return "I'm sorry, I couldn't find relevant information."

    except Exception as e:
        logging.error(f"Error in response generation: {e}", exc_info=True)
        return "I'm sorry, there was an error processing your request."

# Load the training manual
manual_content = load_and_preprocess_manual("training_manual.docx")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        query = data['query']

        retrieved_chunks = retrieve_relevant_chunks(query, manual_content, model_embeddings)
        response = generate_response(query, retrieved_chunks, model_embeddings)

        return jsonify({'response': response})
    except Exception as e:
        logging.error(f"Error processing chat request: {e}", exc_info=True)
        return jsonify({'error': 'An error occurred.'}), 500

# Validation Function
def validate_model(model, validation_data):
    correct = 0
    total = 0
    for item in validation_data['validation']:
        question = item['question']
        expected_answer = item['answers']['text'][0]
        retrieved_chunks = retrieve_relevant_chunks(question, manual_content, model)
        predicted_answer = generate_response(question, retrieved_chunks, model)
        if expected_answer.lower() in predicted_answer.lower():
            correct += 1
        total +=1
    accuracy = correct / total if total > 0 else 0
    print(f"Validation Accuracy: {accuracy}")

if __name__ == '__main__':
    with open('qa_dataset.json', 'r') as f:
        data = json.load(f)
    validate_model(model_embeddings, data)
    app.run(debug=True)