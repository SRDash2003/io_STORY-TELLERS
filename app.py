from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')  # Ensure "index.html" exists in a "templates" folder

@app.route('/generate_story', methods=['POST'])
def generate_story():
    user_input = request.json.get('input')
    # Generate a story continuation based on user input
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Continue the story based on: {user_input}"}
        ]
    )
    story_segment = response.choices[0].message['content']
    return jsonify({'story': story_segment})

if __name__ == '__main__':
    app.run(debug=True)
