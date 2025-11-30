from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
import os
import logging
import secrets
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Literal
from Authdb import init_db, User
from RecruitScoreEngine import RecruitScoreEngine
engine = RecruitScoreEngine()
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../../frontend')
app.secret_key = secrets.token_hex(16)  # Generate a random secret key
CORS(app, supports_credentials=True)  # Enable CORS with credentials support
score_app = FastAPI(title="RecruitMetrics Score API", version="0.1.0")
score_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

Position = Literal["Guard", "Wing", "Forward", "Big"]

class ScoreIn(BaseModel):
    # Core athletic inputs
    position: Position
    height_in: int = Field(..., ge=55, le=96)

    # HS inputs
    state: str
    hs_league: str
    classification: str
    hs_role: Literal["Star","Key","Contributor","Role Player","Practice Player"] = "Contributor"
    hs_wpr: float = Field(..., ge=0, le=100)

    # AAU inputs
    aau_circuit: str
    aau_role: Literal["Star","Key","Contributor","Role Player","Practice Player","NO AAU"] = "Contributor"
    aau_wpr: float = Field(..., ge=0, le=100)

    # Academics (optional for /score, required for /matches)
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    sat: Optional[int] = Field(None, ge=400, le=1600)
    act: Optional[int] = Field(None, ge=1, le=36)

    @validator("aau_circuit","hs_league","classification","state")
    def non_empty(cls, v):
        if not str(v).strip():
            raise ValueError("must not be empty")
        return v

class ScoreOut(BaseModel):
    recruitscore: int
    components: dict

class MatchesOut(BaseModel):
    recruitscore: int
    academic_score_1_to_10: int
    matches: list

class SchoolResponse(BaseModel):
    id: int
    name: str
    division: Optional[str] = None
    conference: Optional[str] = None
    athletic_threshold: Optional[int] = None
    athletic_maximum: Optional[int] = None
    academic_threshold: Optional[int] = None
    state: Optional[str] = None
    city: Optional[str] = None
    gpa_min: Optional[float] = None
    gpa_max: Optional[float] = None
    sat_min: Optional[int] = None
    sat_max: Optional[int] = None
    interest_clusters: Optional[List[str]] = None
    size: Optional[str] = None
    region: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    notes: Optional[str] = None

@score_app.get("/health")
def health():
    return {"status": "ok"}

@score_app.post("/score", response_model=ScoreOut)
def score(payload: ScoreIn):
    try:
        # HS competition score
        hs_league_score = engine.HS_league_score(
            payload.state, payload.hs_league, payload.classification
        )
        hs_comp = engine.HS_competition_score_calculator(
            hs_league_score, payload.hs_role, payload.hs_wpr
        )

        # AAU competition score
        aau_circuit_score = engine.AAU_circuit_score(payload.aau_circuit)
        aau_comp = engine.AAU_competition_score_calculator(
            aau_circuit_score, payload.aau_role, payload.aau_wpr
        )

        # Size + RecruitScore
        size_index = engine.SizeIndex_calculator(payload.height_in, payload.position)
        rs = engine.RecruitScoreCalculator(hs_comp, aau_comp, size_index)

        return ScoreOut(
            recruitscore=rs,
            components={
                "hs_league_score": hs_league_score,
                "hs_competition_score": hs_comp,
                "aau_circuit_score": aau_circuit_score,
                "aau_competition_score": aau_comp,
                "size_index": round(size_index, 1),
            },
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@score_app.post("/matches", response_model=MatchesOut)
def matches(payload: ScoreIn):
    try:
        # 1) Compute RecruitScore (reuse /score logic)
        hs_league_score = engine.HS_league_score(
            payload.state, payload.hs_league, payload.classification
        )
        hs_comp = engine.HS_competition_score_calculator(
            hs_league_score, payload.hs_role, payload.hs_wpr
        )
        aau_circuit_score = engine.AAU_circuit_score(payload.aau_circuit)
        aau_comp = engine.AAU_competition_score_calculator(
            aau_circuit_score, payload.aau_role, payload.aau_wpr
        )
        size_index = engine.SizeIndex_calculator(payload.height_in, payload.position)
        rs = engine.RecruitScoreCalculator(hs_comp, aau_comp, size_index)

        # 2) Academic score (require GPA or test)
        if payload.gpa is None and payload.sat is None and payload.act is None:
            raise HTTPException(status_code=422, detail="Provide GPA and/or SAT/ACT for matching.")
        acad = engine.calculate_academic_score(
            {"gpa": payload.gpa, "sat": payload.sat, "act": payload.act}
        )

        # 3) Get top matches
        top = engine.get_matching_schools(rs, acad)

        return MatchesOut(
            recruitscore=rs,
            academic_score_1_to_10=acad,
            matches=top
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@score_app.get("/schools/{school_id}", response_model=SchoolResponse)
async def get_school(school_id: int):
    """Get detailed school information by ID"""
    try:
        import sqlite3
        import os
        
        # Connect to your basketball database
        conn = sqlite3.connect('basketball_data.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                id, name,
                athletic_threshold, athletic_maximum, academic_threshold,
                division, conference,
                state, city, gpa_min, gpa_max, 
                sat_min, sat_max,
                interest_clusters, size, region,
                primary_color, secondary_color, notes
            FROM schools 
            WHERE id = ?
        ''', (school_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="School not found")
            
        school_data = dict(row)
        
        # Parse interest_clusters JSON if present
        if school_data.get('interest_clusters'):
            try:
                import json
                school_data['interest_clusters'] = json.loads(school_data['interest_clusters'])
            except:
                school_data['interest_clusters'] = []
        
        return SchoolResponse(**school_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching school {school_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Server error")

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
