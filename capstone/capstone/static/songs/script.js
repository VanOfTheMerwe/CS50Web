// Pagination variables
let currentPage = 1;
const songsPerPage = 10;
let songs = []; // This will store all the songs

// Function to fetch songs from the server
async function fetchSongs() {
    try {
        const response = await fetch('/songs/list'); // Adjust this URL as needed
        songs = await response.json();
        displaySongs();
        setupPagination();
    } catch (error) {
        console.error('Error fetching songs:', error);
    }
}

// Function to display songs for the current page
function displaySongs() {
    const songList = document.getElementById('song-list');
    songList.innerHTML = ''; // Clear existing songs

    const startIndex = (currentPage - 1) * songsPerPage;
    const endIndex = startIndex + songsPerPage;
    const songsToDisplay = songs.slice(startIndex, endIndex);

    songsToDisplay.forEach(song => {
        const songElement = document.createElement('div');
        songElement.textContent = song.title; // Adjust based on your song object structure
        songList.appendChild(songElement);
    });
}

// Function to set up pagination controls
function setupPagination() {
    const totalPages = Math.ceil(songs.length / songsPerPage);
    const paginationElement = document.getElementById('pagination');
    paginationElement.innerHTML = '';

    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement('button');
        button.textContent = i;
        button.addEventListener('click', () => {
            currentPage = i;
            displaySongs();
        });
        paginationElement.appendChild(button);
    }
}

// Initial fetch when the page loads
document.addEventListener('DOMContentLoaded', fetchSongs);