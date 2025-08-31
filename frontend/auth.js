document.addEventListener('DOMContentLoaded', function() {
    // Handle signup form
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;
            const messageEl = document.getElementById('signup-message');
            
            // Validation
            if (password !== confirmPassword) {
                messageEl.textContent = "Passwords don't match";
                messageEl.className = "form-message error";
                return;
            }
            const submitBtn = document.querySelector('.auth-submit-btn');
            submitBtn.textContent = 'Creating Account...';
            submitBtn.disabled = true;

            // Submit the form
            fetch('/api/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include', // Add credentials for cookie-based sessions
                body: JSON.stringify({ username, email, password })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    messageEl.textContent = "Account created successfully! Redirecting to login...";
                    messageEl.className = "form-message success";
                    setTimeout(() => {
                        window.location.href = 'login.html';
                    }, 2000);
                } else {
                    messageEl.textContent = data.error || "Error creating account";
                    messageEl.className = "form-message error";
                }
            })
            .catch(error => {
                console.error('Error:', error);
                messageEl.textContent = "Server error. Please try again.";
                messageEl.className = "form-message error";
                submitBtn.disabled = false;
                submitBtn.textContent = 'Sign Up';
            });
        });
    }
    
    // Handle login form
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const messageEl = document.getElementById('login-message');
            
            const submitBtn = document.querySelector('.auth-submit-btn');
            const originalButtonText = submitBtn.textContent;
            submitBtn.textContent = 'Logging in...';
            submitBtn.disabled = true;
            
            // Submit the form
            fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({ email, password })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    messageEl.textContent = "Login successful! Redirecting...";
                    messageEl.className = "form-message success";
                    localStorage.setItem('user', JSON.stringify(data.user));
                    setTimeout(() => {
                        window.location.href = 'index.html';
                    }, 1500);
                } else {
                    messageEl.textContent = data.error || "Invalid credentials";
                    messageEl.className = "form-message error";
                }
            })
            .catch(error => {
                console.error('Error:', error);
                messageEl.textContent = "Server error. Please try again.";
                messageEl.className = "form-message error";
                submitBtn.disabled = false;
                submitBtn.textContent = originalButtonText;
            });
        });
    }
    
    // Check if user is logged in
    fetch('/api/user', {
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (!data.error) {
            // User is logged in
            updateNavForLoggedInUser(data.username);
        }
    })
    .catch(error => {
        console.error('Error checking login status:', error);
    });
    const userStatus = document.getElementById('user-status');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (user.username) {
        userStatus.innerHTML = `
            <span>Welcome, ${user.username}!</span>
            <button id="logout-btn">Logout</button>
        `;
        
        // Add logout functionality
        document.getElementById('logout-btn').addEventListener('click', function() {
            fetch('/api/logout', {
                method: 'POST',
                credentials: 'include'
            })
            .then(() => {
                localStorage.removeItem('user');
                window.location.reload();
            });
        });
    } else {
        userStatus.innerHTML = `
            <a href="login.html" class="auth-btn login-btn">Login</a> 
            <a href="signup.html" class="auth-btn signup-btn">Sign Up</a>
        `;
    }
});

// Update navigation for logged in users

