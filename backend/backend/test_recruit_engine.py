import os
import sqlite3
import random
from RecruitScoreEngine import RecruitScoreEngine

def ensure_test_db():
    """Make sure the test database exists with proper tables"""
    db_path = os.path.join(os.path.dirname(__file__), 'basketball_data.db')
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}. Please create it first.")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if schools table exists and has data
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schools'")
    if not cursor.fetchone():
        print("Schools table doesn't exist in database.")
        conn.close()
        return False
    
    # Check if hs_league_scores table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hs_league_scores'")
    if not cursor.fetchone():
        print("hs_league_scores table doesn't exist in database.")
        conn.close()
        return False
    
    # Check if aau_circuit_scores table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='aau_circuit_scores'")
    if not cursor.fetchone():
        print("aau_circuit_scores table doesn't exist in database.")
        conn.close()
        return False
    
    conn.close()
    return True

def test_db_query():
    """Test querying the database for league scores"""
    engine = RecruitScoreEngine()
    
    # Test HS league score query
    score = engine.HS_league_score('CA', 'CIF', '5')
    print(f"California CIF Division 5 score: {score}")

    # Test missing league score (should return default)
    score = engine.HS_league_score('ZZ', 'NONEXISTENT', 'XXX')
    print(f"Nonexistent league score (should be default): {score}")

def test_school_loading():
    """Test loading schools from database"""
    engine = RecruitScoreEngine()
    print(f"Loaded {len(engine.schools)} schools from database")
    print("First 3 schools:")
    for i, school in enumerate(engine.schools[:3]):
        print(f"{i+1}. {school['name']} - Athletic: {school['athletic_threshold']}, Academic: {school['academic_threshold']}")

def test_recruit_score_calculation():
    """Test calculating recruit scores and matching schools"""
    engine = RecruitScoreEngine()
    
    # Example recruit data
    recruit = {
        'height': 69,  # 5'9"
        'position': 'Guard',
        'state': 'NY',
        'hs_league': 'NYSPHAA',
        'classification': 'AA',
        'hs_role': 'Role Player',
        'hs_wpr': 30,
        'aau_circuit': 'Other',
        'aau_role': 'Contributor',
        'aau_wpr': 40,
        'gpa': 3.4,
        'sat': None,
        'act': None
    }
    
    size_index = engine.SizeIndex_calculator(recruit['height'], recruit['position'])
    print(f"Size Index: {size_index}")
    
    hs_league_score = engine.HS_league_score(recruit['state'], recruit['hs_league'], recruit['classification'])
    hs_comp_score = engine.HS_competition_score_calculator(hs_league_score, recruit['hs_role'], recruit['hs_wpr'])
    print(f"HS Competition Score: {hs_comp_score}")
    
    # Calculate AAU competition score
    aau_circuit_score = engine.AAU_circuit_score(recruit['aau_circuit'])
    aau_comp_score = engine.AAU_competition_score_calculator(aau_circuit_score, recruit['aau_role'], recruit['aau_wpr'])
    print(f"AAU Competition Score: {aau_comp_score}")
    
    # Calculate recruit score
    recruit_score = engine.RecruitScoreCalculator(hs_comp_score, aau_comp_score, size_index)
    print(f"Final Recruit Score: {recruit_score}")
    
    # Calculate academic score
    academic_score = engine.calculate_academic_score(recruit)
    print(f"Academic Score: {academic_score}")
    
    # Get matching schools
    matches = engine.get_matching_schools(recruit_score, academic_score)
    print("\nMatching Schools:")
    for i, match in enumerate(matches):
        print(f"{i+1}. {match['name']} - Overall Match: {match['match']}%, Athletic: {match['athletic_match']}%, Academic: {match['academic_match']}%")

def test_random_school_match():
    """Test match percentage for a randomly selected school"""
    engine = RecruitScoreEngine()
    
    # Example recruit data
    recruit = {
        'height': 73,  # 6'1"
        'position': 'Guard',
        'state': 'NY',
        'hs_league': 'NYSPHAA',
        'classification': 'AA',
        'hs_role': 'Star',
        'hs_wpr': 65,
        'aau_circuit': 'EYCL',
        'aau_role': 'Key',
        'aau_wpr': 60,
        'gpa': 3.0,
        'sat': None,
        'act': None
    }
    
    # Calculate scores
    size_index = engine.SizeIndex_calculator(recruit['height'], recruit['position'])
    
    hs_league_score = engine.HS_league_score(recruit['state'], recruit['hs_league'], recruit['classification'])
    hs_comp_score = engine.HS_competition_score_calculator(hs_league_score, recruit['hs_role'], recruit['hs_wpr'])
    
    aau_circuit_score = engine.AAU_circuit_score(recruit['aau_circuit'])
    aau_comp_score = engine.AAU_competition_score_calculator(aau_circuit_score, recruit['aau_role'], recruit['aau_wpr'])
    
    recruit_score = engine.RecruitScoreCalculator(hs_comp_score, aau_comp_score, size_index)
    academic_score = engine.calculate_academic_score(recruit)
    
    # Select a random school from the database
    if len(engine.schools) > 0:
        random_school = random.choice(engine.schools)
        
        # Calculate match percentages directly (similar to get_matching_schools logic)
        if academic_score == random_school['academic_threshold']:
            academic_match = 100
        else:
            academic_match = 100-(abs((random_school['academic_threshold'] - academic_score)) * 20)
            if academic_match < 0:
                academic_match = 0
        if recruit_score >= random_school['athletic_threshold'] and recruit_score <= random_school['athletic_maximum']:
            athletic_match = 100  # Recruit meets or exceeds the threshold
        elif recruit_score > random_school['athletic_maximum']:
            excess = recruit_score - random_school['athletic_maximum']
            athletic_match = max(0, 100 - (excess * 5))  # Reduce by 5% for each point above maximum
        else:
            excess = random_school['athletic_threshold'] - recruit_score
            athletic_match = 100 - (excess * 5)

        overall_match = (athletic_match * 0.7) + (academic_match * 0.3)
        
        print("\n===== Random School Match Test =====")
        print(f"Random School: {random_school['name']}")
        print(f"Athletic threshold: {random_school['athletic_threshold']}, Recruit score: {recruit_score}")
        print(f"Academic threshold: {random_school['academic_threshold']}, Recruit academic score: {academic_score}")
        print(f"Match percentages - Overall: {round(overall_match)}%, Athletic: {round(athletic_match)}%, Academic: {round(academic_match)}%")
        
        # Show division and conference if available
        if 'division' in random_school:
            print(f"Division: {random_school['division']}")
        if 'conference' in random_school:
            print(f"Conference: {random_school['conference']}")
    else:
        print("\nNo schools available for random testing")

if __name__ == "__main__":
    # Check if database is ready for testing
    if ensure_test_db():
        print("Database is ready for testing")
        
        # Run tests
        print("\n===== Testing Database Queries =====")
        test_db_query()
        
        print("\n===== Testing School Loading =====")
        test_school_loading()
        
        print("\n===== Testing Recruit Score Calculation =====")
        test_recruit_score_calculation()

        test_random_school_match()
    else:
        print("\nDatabase not properly set up. Please check that basketball_data.db exists with the required tables.")