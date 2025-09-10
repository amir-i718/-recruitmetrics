document.addEventListener('DOMContentLoaded', function() {
    const recruitScoreForm = document.getElementById('RSform');
    
    if (recruitScoreForm) {
        recruitScoreForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const feet = parseInt(document.getElementById('player_height-feet').value) || 0;
            const inches = parseInt(document.getElementById('player_height-inches').value) || 0;
            
            const height = `${feet}'${inches}"`;
            
            // Create data object that matches RecruitScoreEngine expectations
            const formData = {
                // Core fields expected by your engine
                gpa: parseFloat(document.getElementById('GPA').value) || 0,
                height: height,
                position: document.getElementById('player_position').value,
                // Map to the exact field names expected by backend
                AAU_Circuit: document.getElementById('AAU_Circuit').value,  // Changed from aau_circuit
                HS_league: document.getElementById('HS_league').value,     // Changed from hs_league
                
                // Optional test scores - only include if they have values
                sat: document.getElementById('SAT').value ? parseInt(document.getElementById('SAT').value) : null,
                act: document.getElementById('ACT').value ? parseInt(document.getElementById('ACT').value) : null,
                
                // Extra fields that might be useful for future features
                state: document.getElementById('state').value,
                classification: document.getElementById('Classification').value,
                hs_role: document.getElementById('HS_player_role').value,
                hs_win_percentage: parseInt(document.getElementById('HS_WP').value) || 0,
                aau_role: document.getElementById('AAU_player_role').value,
                aau_win_percentage: parseInt(document.getElementById('AAU_WP').value) || 0
            };
            
            // Show loading state
            const submitButton = document.querySelector('.submit-button');
            if (submitButton) {
                submitButton.classList.add('loading');
                submitButton.textContent = 'Calculating...';
            }
            
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
                    return response.json().then(errorData => {
                        throw new Error(errorData.error || 'Network response was not ok');
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log('Results received:', data);
                
                // Simple redirect to score page
                window.location.href = 'scorepage.html';
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error: ' + error.message);
            })
            .finally(() => {
                // Reset button state
                if (submitButton) {
                    submitButton.classList.remove('loading');
                    submitButton.textContent = 'Calculate Score';
                }
            });
        });
    }
});