document.addEventListener('DOMContentLoaded', function() {
    const recruitScoreForm = document.getElementById('RSform');
    
    if (recruitScoreForm) {
        recruitScoreForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Get form data
            const feet = parseInt(document.getElementById('player-height-feet').value) || 0;
            const inches = parseInt(document.getElementById('player-height-inches').value) || 0;
            const height = feet + ' ft ' + inches + ' in'; // Format for backend
            
            const formData = {
                gpa: parseFloat(document.getElementById('GPA').value) || 0,
                height: height,
                // Add other stats that your RecruitScoreEngine expects
                state: document.getElementById('state').value,
                position: document.getElementById('player-position').value,
                hs_league: document.getElementById('HS-league').value,
                classification: document.getElementById('Classification').value,
                hs_role: document.getElementById('HS-player-role').value,
                hs_win_percentage: parseInt(document.getElementById('HS-WP').value) || 0,
                aau_circuit: document.getElementById('AAU-circuit').value,
                aau_role: document.getElementById('AAU-team-role').value,
                aau_win_percentage: parseInt(document.getElementById('AAU-WP').value) || 0,
                sat: parseInt(document.getElementById('SAT').value) || 0,
                act: parseInt(document.getElementById('ACT').value) || 0
            };
            
            // Show loading state
            const submitButton = document.querySelector('.submit-button');
            submitButton.classList.add('loading');
            submitButton.textContent = 'Calculating...';
            
            // Send data to backend
            fetch('http://localhost:8080/api/calculate-score', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Save results to localStorage
                localStorage.setItem('recruitScore', data.score);
                localStorage.setItem('schoolMatches', JSON.stringify(data.matches));
                
                // Redirect to score page
                window.location.href = 'scorepage.html';
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was an error calculating your score. Please try again.');
            })
            .finally(() => {
                // Reset button state
                submitButton.classList.remove('loading');
                submitButton.textContent = 'Calculate Score';
            });
        });
    }
});
