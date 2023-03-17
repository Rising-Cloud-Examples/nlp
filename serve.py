import json
from flask import Flask, request, jsonify
from transformers import pipeline, set_seed

app = Flask(__name__)

# Load model pipeline in background
generator = pipeline('text-generation', model='gpt2')
set_seed(42)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Unpack request
    prompt = data.get("prompt")
    if prompt == None:
        raise Exception("Did not provide a prompt for request")

    # Unpack response size params
    max_length=data.get("max_length", 10)
    num_return_sequences=data.get("num_return_sequences", 1)

    # Generate predictions
    output = generator(
        prompt, 
        max_length=max_length, 
        num_return_sequences=num_return_sequences
    )

    # Write to response
    return jsonify({
            "request": {**data},
            "response": output
        })