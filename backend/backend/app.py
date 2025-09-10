from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
import os
import logging
import secrets
import json
from Authdb import init_db, User
from RecruitScoreEngine import RecruitScoreEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../../frontend')
app.secret_key = secrets.token_hex(16)  # Generate a random secret key
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = None  # 'None' allows cookies in cross-site requests
CORS(app, 
     supports_credentials=True, 
     resources={r"/api/*": {"origins": "*"}},
     expose_headers=["Content-Type", "X-CSRFToken"],
     allow_headers=["Content-Type", "X-CSRFToken"],
     methods=["GET", "POST", "OPTIONS"])  # Enable CORS with credentials support

# Create an instance of the score engine
score_engine = RecruitScoreEngine()

# Simple global variable to store the most recent calculation
# This is not ideal for production but works for demonstration
LATEST_RESULTS = {
    'recruit_score': 85,
    'academic_score': 7.5,
    'matches': [
        {'name': 'UCLA', 'match': 95},
        {'name': 'Stanford', 'match': 87},
        {'name': 'Duke', 'match': 82}
    ]
}

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
            'logged_in': True,
            'user_id': session['user_id'],
            'username': session['username']
        }), 200
    return jsonify({'logged_in': False}), 200

@app.route('/api/save-score', methods=['POST'])
def save_score():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
        
    data = request.json
    User.save_score(session['user_id'], data)
    return jsonify({'success': True}), 201

@app.route('/api/calculate-score', methods=['POST'])
def calculate_score():
    global LATEST_RESULTS  # Access the global variable
    
    data = request.json
    logger.info(f"Received data: {data}")
    # Add validation for required fields (using the API field names)
    required_fields = ['gpa', 'height', 'position']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({
            'error': f"Missing required fields: {', '.join(missing_fields)}"
        }), 400
    try:
        # Map the data to what RecruitScoreEngine expects
        engine_data = {
            'gpa': data.get('gpa'),
            'height': data.get('height'),
            'position': data.get('position'),
            'aau_level': data.get('AAU_Circuit', 'Gold'),
            'hs_level': data.get('HS_league', 'State'),
            'sat': data.get('SAT'),
            'act': data.get('ACT')
        }
        logger.info(f"Sending to engine: {engine_data}")
        result = score_engine.calculate_recruit_score(engine_data)
        logger.info(f"Calculated score: {result}")
        matches = score_engine.get_matching_schools(
            result['recruit_score'],
            result['academic_score']
        )
        
        # Store results in the global variable
        LATEST_RESULTS = {
            'recruit_score': result['recruit_score'],
            'academic_score': result['academic_score'],
            'competition_avg': result.get('competition_avg'),
            'position_size_factor': result.get('position_size_factor'),
            'matches': matches
        }
        
        logger.info(f"Stored in global variable: {LATEST_RESULTS}")
        
        # Also store in session as backup
        session['latest_results'] = LATEST_RESULTS
        
        # Also save to file as another backup
        try:
            with open('latest_results.json', 'w') as f:
                json.dump(LATEST_RESULTS, f)
            logger.info("Saved results to file as backup")
        except Exception as e:
            logger.error(f"Failed to save results to file: {str(e)}")
            
        return jsonify(LATEST_RESULTS)
    except Exception as e:
        logger.error(f"Error calculating score: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/latest-results', methods=['GET'])
def get_latest_results():
    global LATEST_RESULTS
    
    logger.info(f"Returning latest results from global variable: {LATEST_RESULTS}")
    return jsonify(LATEST_RESULTS)
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
    # Set debug=False to prevent auto-reloading which can affect sessions
    app.run(host='0.0.0.0', port=port, debug=False)
