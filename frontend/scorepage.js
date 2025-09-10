document.addEventListener('DOMContentLoaded', function() {
    console.log("%c===== SCOREPAGE DEBUG =====", "font-size:14px; font-weight:bold; color:orange;");
    console.log("Page loaded at:", new Date().toISOString());
    
    // Get DOM elements
    const scoreElement = document.querySelector('.RS-score');
    const schoolsContainer = document.querySelector('.RS-schools');
    
    console.log("DOM Elements:", {
        scoreElement: !!scoreElement,
        schoolsContainer: !!schoolsContainer
    });
    
    // Show loading screen immediately
    if (scoreElement) {
        scoreElement.innerHTML = `
            <div class="loading-screen">
                <div class="loading-spinner"></div>
                <p>Loading your basketball recruit metrics...</p>
            </div>
        `;
    }
    
    // Fetch from API directly - this should now always work
    console.log("Fetching data from API...");
    fetch('http://localhost:8080/api/latest-results')
        .then(response => {
            console.log("API response status:", response.status);
            if (!response.ok) {
                throw new Error(`API returned ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("API returned data:", data);
            displayScore(data.recruit_score, data.academic_score);
            if (data.matches) {
                displaySchools(data.matches);
            }
        })
        .catch(error => {
            console.error("API error:", error);
            
            // If API fails, show error and test data
            if (scoreElement) {
                const testData = {
                    recruit_score: 85,
                    academic_score: 7.5,
                    matches: [
                        {name: 'UCLA', match: 95},
                        {name: 'Stanford', match: 87},
                        {name: 'Duke', match: 82}
                    ]
                };
                
                displayScore(testData.recruit_score, testData.academic_score);
                displaySchools(testData.matches);
                
                // Show an error indicator
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error-notice';
                errorDiv.innerHTML = 'Note: Using sample data (API connection failed)';
                scoreElement.appendChild(errorDiv);
            }
        });
    
    function displayScore(score, academicScore) {
        if (scoreElement) {
            scoreElement.innerHTML = `
                <div class="score-container">
                    <div class="main-score">
                        <span class="score-value">${score}</span>
                    </div>
                    ${academicScore ? `
                    <div class="academic-score">
                        <span class="score-label">Academic Score:</span>
                        <span class="score-value-small">${academicScore}</span>
                    </div>` : ''}
                </div>
            `;
            console.log("Scores displayed:", { recruit: score, academic: academicScore });
        }
    }
    
    function displaySchools(schools) {
        if (schoolsContainer && schools && schools.length > 0) {
            schoolsContainer.innerHTML = '';
            schools.forEach(school => {
                const schoolDiv = document.createElement('div');
                schoolDiv.className = 'RS-school';
                schoolDiv.innerHTML = `
                    <h3 class="RS-school-name">${school.name}</h3>
                    <div class="RS-match">Match ${school.match}%</div>
                `;
                schoolsContainer.appendChild(schoolDiv);
            });
            console.log("Schools displayed:", schools.length);
        } else if (schoolsContainer) {
            schoolsContainer.innerHTML = '<div class="no-schools">No matching schools found</div>';
        }
    }
});
    
    // Keep the function definitions for future use
    function fetchFromAPI() {
        if (scoreElement) {
            scoreElement.innerHTML = '<span class="loading">Loading...</span>';
        }
        
        console.log("Attempting to fetch from /api/latest-results");
        
        // Use absolute URL
        fetch('http://localhost:8080/api/latest-results', {
            credentials: 'include'  // Include credentials to send cookies
        })
            .then(response => {
                console.log("API response status:", response.status);
                if (!response.ok) {
                    console.log("Failed to fetch latest results, falling back to test results");
                    // If latest-results fails, try test-results
                    return fetch('http://localhost:8080/api/test-results');
                }
                return response;
            })
            .then(response => response.json())
            .then(data => {
                console.log("API returned data:", data);
                displayScore(data.recruit_score);
                if (data.matches) {
                    displaySchools(data.matches);
                }
            })
            .catch(error => {
                console.error("API error:", error);
                if (scoreElement) {
                    scoreElement.innerHTML = `
                        <div class="error">
                            <p>Error loading score data.</p>
                            <a href="RSform.html" class="btn">Calculate Your Score</a>
                        </div>
                    `;
                }
            });
    }
    
    function displayScore(score, academicScore) {
        if (scoreElement) {
            // Determine data source for visual indicator
            const isFromUrl = new URLSearchParams(window.location.search).has('score');
            const dataSource = isFromUrl ? 'url' : (localStorage.getItem('recruitScore') ? 'localStorage' : 'test');
            
            let sourceLabel = '';
            if (dataSource === 'url') {
                sourceLabel = '<div class="data-source real-data">Your calculated results</div>';
            } else if (dataSource === 'localStorage') {
                sourceLabel = '<div class="data-source storage-data">Your saved results</div>';
            } else {
                sourceLabel = '<div class="data-source test-data">Sample data</div>';
            }
            
            scoreElement.innerHTML = `
                <div class="score-container">
                    <div class="main-score">
                        <span class="score-value">${score}</span>
                    </div>
                    ${academicScore ? `
                    <div class="academic-score">
                        <span class="score-label">Academic Score:</span>
                        <span class="score-value-small">${academicScore}</span>
                    </div>` : ''}
                    ${sourceLabel}
                </div>
            `;
            console.log("Scores displayed:", { recruit: score, academic: academicScore, source: dataSource });
        }
    }
    
    function displaySchools(schools) {
        if (schoolsContainer && schools && schools.length > 0) {
            schoolsContainer.innerHTML = '';
            schools.forEach(school => {
                const schoolDiv = document.createElement('div');
                schoolDiv.className = 'RS-school';
                schoolDiv.innerHTML = `
                    <h3 class="RS-school-name">${school.name}</h3>
                    <div class="RS-match">Match ${school.match}%</div>
                `;
                schoolsContainer.appendChild(schoolDiv);
            });
            console.log("Schools displayed:", schools.length);
        } else if (schoolsContainer) {
            schoolsContainer.innerHTML = '<div class="no-schools">No matching schools found</div>';
        }
    }
});