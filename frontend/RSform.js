document.addEventListener('DOMContentLoaded', function() {
    const recruitScoreForm = document.getElementById('RSform');
    
    if (recruitScoreForm) {
        recruitScoreForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Get form data
            const feet = parseInt(document.getElementById('player-height-feet').value) || 0;
            const inches = parseInt(document.getElementById('player-height-inches').value) || 0;
            
            const height = `${feet}'${inches}"`;
            
            // Create data object that matches RecruitScoreEngine expectations
            const formData = {
                // Core fields expected by your engine
                gpa: parseFloat(document.getElementById('GPA').value) || 0,
                height: height,
                position: document.getElementById('player-position').value,
                
                // Map to the exact field names expected by backend
                AAU_Circuit: document.getElementById('AAU_Circuit').value,  // Changed from aau_circuit
                HS_league: document.getElementById('HS_league').value,     // Changed from hs_league
                
                // Optional test scores - only include if they have values
                sat: document.getElementById('SAT').value ? parseInt(document.getElementById('SAT').value) : null,
                act: document.getElementById('ACT').value ? parseInt(document.getElementById('ACT').value) : null,
                
                // Extra fields that might be useful for future features
                state: document.getElementById('state').value,
                classification: document.getElementById('Classification').value,
                hs_role: document.getElementById('HS-player-role').value,
                hs_win_percentage: parseInt(document.getElementById('HS-WP').value) || 0,
                aau_role: document.getElementById('AAU-team-role').value,
                aau_win_percentage: parseInt(document.getElementById('AAU-WP').value) || 0
            };
            
            // Show loading state
            const submitButton = document.querySelector('.submit-button');
            submitButton.classList.add('loading');
            submitButton.textContent = 'Calculating...';
            
            // For debugging - remove in production
            console.log('Sending form data:', formData);
            
            // Send data to backend
            fetch('/api/calculate-score', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        throw new Error(errorData.error || 'Network response was not ok');
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log('Received data:', data); // Debug
                
                // Check if we have the expected data structure
                if (!data.recruit_score) {
                    throw new Error('Invalid response format');
                }
                
                // Save results to localStorage (adjusted for new response format)
                localStorage.setItem('recruitScore', data.recruit_score);
                localStorage.setItem('academicScore', data.academic_score);
                localStorage.setItem('schoolMatches', JSON.stringify(data.matches || []));
                
                // Redirect to score page
                window.location.href = 'scorepage.html';
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error: ' + error.message);
            })
            .finally(() => {
                // Reset button state
                submitButton.classList.remove('loading');
                submitButton.textContent = 'Calculate Score';
            });
        });
    }
});