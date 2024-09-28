import os
from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env
load_dotenv()

# Set up OpenAI API Key (store in environment variable for security)
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logging.error("OpenAI API key is missing. Please check your .env file.")
else:
    openai.api_key = openai_api_key

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-initial', methods=['POST'])
def generate_initial():
    data = request.json 
    genre = data.get('genre')
    character_name = data.get('characterName')

    if not genre or not character_name:
        return jsonify({'error': 'Invalid Input'}), 400

    # Generate initial story based on genre and character name
    prompt = f"Start a {genre} story with the character named {character_name}."
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        logging.info(f"OpenAI API response: {response}")
        
        story = response.choices[0].text.strip()
        return jsonify({'story': story})
    except Exception as e:
        logging.error(f"Error generating story: {str(e)}")
        return jsonify({'error': 'Failed to generate story. Please try again later.'}), 500

@app.route('/generate-next', methods=['POST'])
def generate_next():
    data = request.json
    user_decision = data['userDecision']
    current_story = data['currentStory']
    genre = data['genre']

    # Generate the next scene based on user input, genre, and current story
    prompt = f"Continue this {genre} story: {current_story}. The user decides to {user_decision}. What happens next?"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        next_scene = response.choices[0].text.strip()
        return jsonify({'story': next_scene})
    except Exception as e:
        logging.error(f"Error generating next scene: {str(e)}")
        return jsonify({'error': 'Failed to generate next scene. Please try again later.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
