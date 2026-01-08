const API_BASE_URL = "http://localhost:8000";

const moodData = {
    "happy": { "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1EVJSvZp5AOML2?si=yXy5WADBTGK8GUjntW6Ymg" },
    "sad": { "spotify_url": "https://open.spotify.com/playlist/1YLrmz057n156hHuiDv9AI" },
    "motivated": { "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1DX1OY2Lp0bIPp" },
    "emotionless": { "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO" },
    "lonely": { "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1DWVV27DiNWxkR" },
    "in-love": { "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1DX50QitC6Oqtn" },
    "heartbroken": { "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1DX7gIoKXt0gmx" },
    "excited": { "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1DX0BcQWzuB7ZO" },
    "chill": { "spotify_url": "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6" }
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


    const logo = document.getElementById('musical-logo');
const letters = logo.querySelectorAll('span');

// We use an AudioContext to generate clean, "serene" synth notes
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playNote(frequency) {
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();

    oscillator.type = 'sine'; // Soft, calm sound
    oscillator.frequency.setValueAtTime(frequency, audioCtx.currentTime);
    
    gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 1);

    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    oscillator.start();
    oscillator.stop(audioCtx.currentTime + 1);
}

// Assign different musical notes to each letter
const notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]; // C, D, E, F, G, A, B

letters.forEach((char, index) => {
    char.addEventListener('mouseenter', () => {
        if (audioCtx.state === 'suspended') audioCtx.resume();
        playNote(notes[index]);
    });
});
});
