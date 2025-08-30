document.addEventListener('DOMContentLoaded', function() {
    // Get stored results
    const score = localStorage.getItem('recruitScore');
    const matches = JSON.parse(localStorage.getItem('schoolMatches') || '[]');
    
    // Display the score
    const scoreElement = document.querySelector('.RS-score');
    if (scoreElement) {
        scoreElement.textContent = score || '?';
    }
    
    // Display the matching schools
    const schoolsContainer = document.querySelector('.RS-schools');
    if (schoolsContainer && matches.length > 0) {
        schoolsContainer.innerHTML = ''; // Clear existing content
        
        matches.forEach(match => {
            const schoolDiv = document.createElement('div');
            schoolDiv.className = 'RS-school';
            
            schoolDiv.innerHTML = `
                <h3 class="RS-school-name">${match.name}</h3>
                <div class="RS-match">Match ${match.match}%</div>
            `;
            
            schoolsContainer.appendChild(schoolDiv);
        });
    }
})