// Initial story state
let storyState = 0;

// Story data
const story = {
    0: "You find yourself at the edge of a dense forest. Two paths lie ahead: one leading deeper into the woods and another toward a distant mountain.",
    1: "You step onto the journey path, feeling the excitement of an adventure beginning. You soon encounter a traveler who offers you a map. Do you take it?",
    2: "You walk deeper into the forest. The trees grow taller, and you hear the sound of running water. Do you follow the sound or explore deeper?",
    3: "You took the map. It reveals hidden paths and treasures in the forest.",
    4: "You politely decline the offer. The traveler smiles and continues on their way.",
    5: "You follow the sound of water and discover a beautiful waterfall.",
    6: "You explore deeper into the forest and encounter a wild animal."
};

// Handle choice
function makeChoice(choice) {
    storyState = choice;
    document.getElementById('story-text').innerText = story[storyState];

    // Update buttons for the next stage of the story
    if (choice === 1) {
        document.getElementById('choices-section').innerHTML = `
            <button class="choice-button" onclick="makeChoice(3)">Take the map</button>
            <button class="choice-button" onclick="makeChoice(4)">Politely decline</button>
        `;
    } else if (choice === 2) {
        document.getElementById('choices-section').innerHTML = `
            <button class="choice-button" onclick="makeChoice(5)">Follow the sound</button>
            <button class="choice-button" onclick="makeChoice(6)">Explore deeper</button>
        `;
    } else {
        document.getElementById('choices-section').style.display = 'none';
        document.getElementById('input-section').style.display = 'block';
    }
}

// Handle user input for story progression
async function submitInput() {
    const userInput = document.getElementById('user-input').value;
    document.getElementById('story-text').innerText += `\n\nYou decided: ${userInput}`;
    document.getElementById('input-section').style.display = 'none';
    document.getElementById('user-input').value = ''; // Clear the input after submission

    // Send user input to the Flask server
    const response = await fetch('/generate_story', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: userInput })
    });

    const data = await response.json();
    document.getElementById('story-text').innerText += `\n\n${data.story}`;
}


// Initialize the story on page load
window.onload = function() {
    document.getElementById('story-text').innerText = story[storyState];
    document.getElementById('choices-section').style.display = 'block';
};
