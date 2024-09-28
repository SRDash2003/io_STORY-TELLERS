import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# loading environment variables from .env
load_dotenv()

# Set up OpenAI API Key
client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY"),
)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-initial', methods=['POST'])
def generate_initial():
    data = request.json 
    print(data)  # Debug: Output incoming data
    genre = data.get('genre')
    character_name = data.get('characterName')

    if not genre or not character_name:
        return jsonify({'error': 'Invalid Input'}), 400

    # Generate initial story based on genre and character name using Chat API
    prompt = f"Start a {genre} story with the character named {character_name}."
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an interactive storytelling AI."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo", 
        )
        print(response)  # Debug: Output API response
        story = response['choices'][0]['message']['content'].strip()
        return jsonify({'story': story})
    except Exception as e:
        print(f"Error: {e}")  # Debug: Output error message
        return jsonify({'error': str(e)}), 500

@app.route('/generate-next', methods=['POST'])
def generate_next():
    data = request.json
    user_decision = data['userDecision']
    current_story = data['currentStory']
    genre = data['genre']

    # Generate the next scene using Chat API
    prompt = f"Continue this {genre} story: {current_story}. The user decides to {user_decision}. What happens next?"
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an interactive storytelling AI."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",  
        )
        print(response)  # Debug: Output API response
        next_scene = response['choices'][0]['message']['content'].strip()
        return jsonify({'story': next_scene})
    except client.error.OpenAIError as e:
        return jsonify({'error': f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({'error': f"General error: {str(e)}"}), 500

print(f"API Key: {client.api_key}") 

if __name__ == '__main__':
    app.run(debug=True)
