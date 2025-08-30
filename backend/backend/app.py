from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging

# Import your RecruitScoreEngine
from RecruitScoreEngine import RecruitScoreEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../../frontend')
CORS(app)

# Create a calculator instance
calculator = RecruitScoreEngine()

@app.route('/api/calculate-score', methods=['POST'])
def calculate_score():
    data = request.json
    logger.info(f"Received data: {data}")
    
    try:
        # Validate required fields
        required_fields = ['gpa', 'height']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Calculate score using the engine
        score = calculator.calculate_recruit_score(data)
        
        # Get matching schools
        matches = calculator.get_matching_schools(score)
        
        logger.info(f"Calculated score: {score}, Matches: {matches}")
        
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
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)