// 1. JSON Data: Using an object where keys are the emotions
// This makes it easy for the backend team to add new moods later
const moodData = {
    "happy": { "playlist_name": "Happy Mix", "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1EVJSvZp5AOML2?si=yXy5WADBTGK8GUjntW6Ymg" },
    "sad": { "playlist_name": "CRYING", "spotify_url": "https://open.spotify.com/playlist/1YLrmz057n156hHuiDv9AI" },
    "motivated": { "label": "Motivation Mix", "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1DX1OY2Lp0bIPp" },
    "emotionless": { "label": "Chill Focus", "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO" },
    "lonely": { "label": "Alone Again", "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1DWVV27DiNWxkR" },
    "in-love": { "label": "Love Pop", "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1DX50QitC6Oqtn" },
    "heartbroken": { "label": "Broken Heart", "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1DX7gIoKXt0gmx" },
    "excited": { "label": "Feel-Good Dance", "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1DX0BcQWzuB7ZO" },
    "chill": { "label": "Chill Vibes", "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6" }
};

// Ensure the script runs only after the HTML is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    const tagsContainer = document.getElementById('emotion-tags');
    const searchBar = document.querySelector('.search-bar');
    const cameraBtn = document.querySelector('.icon-btn'); // Moved inside for safety

    // 2. Dynamic Tag Generation
    // Object.keys(moodData) gives us an array: ["happy", "sad", etc.]
    Object.keys(moodData).forEach(emotion => {
        // Create a span for each tag
        const tagElement = document.createElement('span');
        tagElement.classList.add('tag');
        tagElement.textContent = emotion;

        // 3. Click Event for Tags
        tagElement.addEventListener('click', () => {
            // Update the search bar text immediately for visual feedback
            searchBar.value = emotion;

            // Get the specific URL for this mood
            const url = moodData[emotion].spotify_url;

            // Short delay so the user sees the "selected" state before redirecting
            setTimeout(() => {
                window.open(url, '_blank'); // Opens Spotify in a new tab
            }, 300); 
        });

        // Add the finished tag to the HTML container
        tagsContainer.appendChild(tagElement);
    });

    // 3. Search Bar Logic
    /* --- Search Bar Logic --- */

// 1. Live Filtering: Filter tags as the user types
searchBar.addEventListener('input', (e) => {
    const userInput = e.target.value.toLowerCase(); // What the user typed
    const allTags = document.querySelectorAll('.tag'); // Grab all the generated tags

    allTags.forEach(tag => {
        const tagName = tag.textContent.toLowerCase();
        
        // If the tag name includes what the user typed, show it. Otherwise, hide it.
        if (tagName.includes(userInput)) {
            tag.style.display = "inline-block"; 
        } else {
            tag.style.display = "none";
        }
    });
});

// 2. Manual Search: Redirect if the user presses "Enter"
searchBar.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const userInput = searchBar.value.toLowerCase().trim();

        // If the word matches a mood in our JSON, go to that specific playlist
        if (moodData[userInput]) {
            window.open(moodData[userInput].spotify_url, '_blank');
        } else {
            // Otherwise, do a general Spotify search for whatever they typed
            const spotifySearchUrl = `https://open.spotify.com/search/${encodeURIComponent(userInput)}`;
            window.open(spotifySearchUrl, '_blank');
        }
    }
});

    // 4. Camera Button Logic
    cameraBtn.addEventListener('click', () => {
        alert("Camera feature coming soon! Your team can integrate the image recognition backend here.");
    });
});