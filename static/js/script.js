document.getElementById('next-step1').addEventListener('click', function() {
    const characterName = document.getElementById('character-name').value;
    if (characterName) {
      document.getElementById('display-name').innerText = characterName;
      document.getElementById('step1').style.display = 'none';
      document.getElementById('step2').style.display = 'block';
    }
  });
  
  document.getElementById('next-step2').addEventListener('click', async function() {
    const genre = document.getElementById('genre-select').value;
    const characterName = document.getElementById('character-name').value;
    try{
    // Make the AI call to generate the initial story
    const initialPrompt = await generateInitialStory(genre, characterName);
  
    if(initialPrompt){
    document.getElementById('story-text').innerText = initialPrompt;
    document.getElementById('step2').style.display = 'none';
    document.getElementById('story-container').style.display = 'block';
    }else{
      console.error('No story prompt received.');
    }
  }catch(error){
    console.error('Erroe generating the initial story:',error);
  }
  });
  
  document.getElementById('submit-decision').addEventListener('click', async function() {
    const userDecision = document.getElementById('user-input').value;
    const currentStory = document.getElementById('story-text').innerText;
    const genre = document.getElementById('genre-select').value;
  
    // Send the user's decision and the current story context to the AI
    const nextScene = await generateNextScene(userDecision, currentStory, genre);
  
    // Append the next scene to the story
    document.getElementById('story-text').innerText += "\n\n" + nextScene;
    document.getElementById('user-input').value = ''; // Clear input field
  });
  
  // Function to generate initial story based on genre
  async function generateInitialStory(genre, characterName){
  try{
    const response = await fetch('/generate-initial', 
    { 
      method: 'POST', headers: { 'Content-Type': 'application/json'}, body: JSON.stringify({ genre, characterName })
    });
    if(!response.ok){
      console.error('Error from server:',response.statusText);
      return null;
    }
    const data = await response.json();
    return data.story;
  }catch(error){
    console.error('Error fetching story from server:',error);
    return null;
  }
}
  
  // Function to generate the next story scene
  async function generateNextScene(userDecision, currentStory, genre) {
    const response = await fetch('/generate-next', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ userDecision, currentStory, genre })
    });
    const data = await response.json();
    return data.story;
  }
  