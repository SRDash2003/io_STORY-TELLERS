import os
from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv

# loading environment variables from .env
load_dotenv()

# Set up OpenAI API Key (store in environment variable for security)
openai.api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-initial', methods=['POST'])
def generate_initial():
    data = request.get_json() #using get_json() to parse incoming JSON data
    genre = data.get('genre')
    character_name = data.get('characterName')
    if not genre or not character_name:
        return jsonify({'error':'Missing genre or character name'}),400

    # Generate initial story based on genre and character name
    prompt = f"Start a {genre} story with the character named {character_name}."
    try:
       response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
       )
       story = response.choices[0].text.strip()
       return jsonify({'story': story})
    except Exception as e:
        return jsonify({'error':str(e)}),500

@app.route('/generate-next', methods=['POST'])
def generate_next():
    data = request.json
    user_decision = data['userDecision']
    current_story = data['currentStory']
    genre = data['genre']

    # Generate the next scene based on user input, genre, and current story
    prompt = f"Continue this {genre} story: {current_story}. The user decides to {user_decision}. What happens next?"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    next_scene = response.choices[0].text.strip()

    return jsonify({'story': next_scene})

if __name__ == '__main__':
    app.run(debug=True)
