console.log('🚀 forms.js is executing!');
console.log('📍 Current page:', window.location.href);
console.log('⏰ Load time:', new Date().toISOString());

document.addEventListener('DOMContentLoaded', function() {
    // Get stored results
    const score = localStorage.getItem('recruitScore');
    const matches = JSON.parse(localStorage.getItem('schoolMatches') || '[]');
    
    console.log('Retrieved score:', score);
    console.log('Retrieved matches:', matches);
    
    // Display the score
    const scoreElement = document.querySelector('.RS-score');
    if (scoreElement) {
        scoreElement.textContent = score || '?';
    }
      
    const schoolsContainer = document.querySelector('.RS-schools');
    if (schoolsContainer) {
        if (matches && matches.length > 0) {
            schoolsContainer.innerHTML = ''; 
            
            matches.forEach(match => {
                const schoolDiv = document.createElement('div');
                schoolDiv.className = 'RS-school';
                
                schoolDiv.innerHTML = `
                    <h3 class="RS-school-name">${match.name}</h3>
                    <div class="RS-match">Match ${match.match}%</div>
                `;
                
                schoolsContainer.appendChild(schoolDiv);
            });
        } else {
            // Show message if no data
            schoolsContainer.innerHTML = '<p>No scores calculated yet. Please complete the form first.</p>';
        }
    }
    
    // Debug information
    const debugDiv = document.getElementById('debug');
    const debugOutput = document.getElementById('debug-output');
    if (debugDiv && debugOutput) {
        debugDiv.style.display = 'block';
        debugOutput.textContent = JSON.stringify({
            score: score,
            matchesCount: matches ? matches.length : 0,
            matches: matches
        }, null, 2);
    }
});

// Rest of forms.js stays the same...
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('RSform');
    const calculateBtn = document.querySelector('.submit-button');
    console.log('Form found:', form);
    console.log('Button found:', calculateBtn);
    if (form && calculateBtn) {
        calculateBtn.addEventListener('click', async function(e) {
            e.preventDefault();
            console.log('Button clicked!');
            // Collect form data
            const formData = {
                position: document.getElementById('player-position').value,
                height_in: (parseInt(document.getElementById('player-height-feet').value) * 12) + 
                           parseInt(document.getElementById('player-height-inches').value),
                state: document.getElementById('state').value,
                hs_league: document.getElementById('HS-league').value,
                classification: document.getElementById('Classification').value,
                hs_role: document.getElementById('HS-player-role').value,
                hs_wpr: parseFloat(document.getElementById('HS-WP').value),
                aau_circuit: document.getElementById('AAU-circuit').value,
                aau_role: document.getElementById('AAU-team-role').value,
                aau_wpr: parseFloat(document.getElementById('AAU-WP').value),
                gpa: parseFloat(document.getElementById('GPA').value),
                sat: document.getElementById('SAT').value ? parseInt(document.getElementById('SAT').value) : null,
                act: document.getElementById('ACT').value ? parseInt(document.getElementById('ACT').value) : null
            };

            console.log('Form data collected:', formData);
            try {
                // Show loading state
                calculateBtn.textContent = 'Calculating...';
                calculateBtn.disabled = true;
                
                console.log('Sending request to /score endpoint...');

                // Send to FastAPI backend
                const response = await fetch('http://localhost:8040/score', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                console.log('Score response status:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const result = await response.json();
                
                // Store results in localStorage
                localStorage.setItem('recruitScore', result.recruitscore);
                
                // Get matching schools
                const matchesResponse = await fetch('http://localhost:8040/matches', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                if (matchesResponse.ok) {
                    const matches = await matchesResponse.json();
                    localStorage.setItem('schoolMatches', JSON.stringify(matches.matches));
                }
                
                // Redirect to results page
                window.location.href = 'scorepage.html';
                
            } catch (error) {
                console.error('Error calculating score:', error);
                alert('Error calculating your recruit score. Please try again.');
                
                // Reset button
                calculateBtn.textContent = 'Calculate your chances';
                calculateBtn.disabled = false;
            }
        });
    }
});