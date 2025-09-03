from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
import os
import logging
import secrets
from Authdb import init_db, User
from RecruitScoreEngine import RecruitScoreEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../../frontend')
app.secret_key = secrets.token_hex(16)  # Generate a random secret key
CORS(app, supports_credentials=True)  # Enable CORS with credentials support

# Create an instance of the score engine
score_engine = RecruitScoreEngine()

init_db()

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400
        
    if User.create(data['username'], data['email'], data['password']):
        return jsonify({'success': True, 'message': 'User created successfully'}), 201
    else:
        return jsonify({'error': 'Username or email already exists'}), 409

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if not all(k in data for k in ('email', 'password')):
        return jsonify({'error': 'Email and password required'}), 400
        
    user = User.authenticate(data['email'], data['password'])
    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({'success': True, 'user': user}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True}), 200

@app.route('/api/user', methods=['GET'])
def get_user():
    if 'user_id' in session:
        return jsonify({
            'user_id': session['user_id'],
            'username': session['username']
        }), 200
    return jsonify({'error': 'Not logged in'}), 401

@app.route('/api/save-score', methods=['POST'])
def save_score():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
        
    data = request.json
    User.save_score(session['user_id'], data)
    return jsonify({'success': True}), 201

@app.route('/api/calculate-score', methods=['POST'])
def calculate_score():
    data = request.json
    logger.info(f"Received data: {data}")
    
    # Add validation for required fields
    required_fields = ['gpa', 'height']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'error': f"Missing required fields: {', '.join(missing_fields)}"
        }), 400
    
    try:
        calculator = RecruitScoreEngine()
        
        # Calculate score
        score = calculator.calculate_recruit_score(data)

        # Get matching schools
        matches = calculator.get_matching_schools(score)

        return jsonify({
            'score': score,
            'matches': matches
        })
    except Exception as e:
        logger.error(f"Error calculating score: {str(e)}")
        return jsonify({'error': str(e)}), 400
# Serve frontend files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080)) 
    app.run(host='0.0.0.0', port=port, debug=True)
