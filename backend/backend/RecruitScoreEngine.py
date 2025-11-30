import sqlite3
import csv
import os
import random

class RecruitScoreEngine:
    def __init__(self):
        self.schools = self.load_schools_from_db()
        

        self.height_standards = {
            "Guard": 74,    # 6'2"
            "Wing": 77,     # 6'5"
            "Forward": 79,  # 6'7"
            "Big": 81       # 6'9"
        }
        self.gpa_ranges = [
            {'min': 3.9, 'max': 4.0, 'score': 10},
            {'min': 3.7, 'max': 3.89, 'score': 9},
            {'min': 3.4, 'max': 3.69, 'score': 8},
            {'min': 3.2, 'max': 3.39, 'score': 7},
            {'min': 2.9, 'max': 3.19, 'score': 6},
            {'min': 2.6, 'max': 2.89, 'score': 5},
            {'min': 2.3, 'max': 2.59, 'score': 4},
            {'min': 2.0, 'max': 2.29, 'score': 3},
            {'min': 1.7, 'max': 1.99, 'score': 2},
            {'min': 0.0, 'max': 1.69, 'score': 1}
        ]
        self.sat_ranges = [
            {'min': 1450, 'max': 1600, 'score': 10},
            {'min': 1350, 'max': 1449, 'score': 9},
            {'min': 1250, 'max': 1349, 'score': 8},
            {'min': 1150, 'max': 1249, 'score': 7},
            {'min': 1050, 'max': 1149, 'score': 6},
            {'min': 950, 'max': 1049, 'score': 5},
            {'min': 850, 'max': 949, 'score': 4},
            {'min': 750, 'max': 849, 'score': 3},
            {'min': 650, 'max': 749, 'score': 2},
            {'min': 0, 'max': 649, 'score': 1}
        ]
        self.act_ranges = [
            {'min': 33, 'max': 36, 'score': 10},
            {'min': 30, 'max': 32, 'score': 9},
            {'min': 27, 'max': 29, 'score': 8},
            {'min': 24, 'max': 26, 'score': 7},
            {'min': 21, 'max': 23, 'score': 6},
            {'min': 18, 'max': 20, 'score': 5},
            {'min': 16, 'max': 17, 'score': 4},
            {'min': 14, 'max': 15, 'score': 3},
            {'min': 12, 'max': 13, 'score': 2},
            {'min': 0, 'max': 11, 'score': 1}
        ]
    def load_schools_from_db(self):
        schools = []
        db_path = os.path.join(os.path.dirname(__file__), 'basketball_data.db')
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # Execute query to get schools with their thresholds
            cursor.execute('''
                SELECT name, athletic_threshold, athletic_maximum, academic_threshold, division, conference
                FROM schools
            ''')
            for row in cursor.fetchall():
                schools.append({
                    'name': row[0],
                    'athletic_threshold': row[1],
                    'athletic_maximum': row[2],
                    'academic_threshold': row[3],
                    'division': row[4],
                    'conference': row[5]
                })
            conn.close()
            if not schools:  # If no schools found, return default list
                return [
                    {'name': 'Kentucky University', 'athletic_threshold': 80, 'athletic_maximum': 90, 'academic_threshold': 70},
                    {'name': 'Duke University', 'athletic_threshold': 85, 'athletic_maximum': 95, 'academic_threshold': 90},
                    {'name': 'UCLA', 'athletic_threshold': 75, 'athletic_maximum': 85, 'academic_threshold': 80},
                    {'name': 'North Carolina', 'athletic_threshold': 70, 'athletic_maximum': 80, 'academic_threshold': 75},
                    {'name': 'Kansas University', 'athletic_threshold': 65, 'athletic_maximum': 75, 'academic_threshold': 70},
                    {'name': 'Michigan State', 'athletic_threshold': 60, 'athletic_maximum': 70, 'academic_threshold': 75},
                    {'name': 'Villanova', 'athletic_threshold': 55, 'athletic_maximum': 65, 'academic_threshold': 85},
                    {'name': 'Gonzaga', 'athletic_threshold': 50, 'athletic_maximum': 60, 'academic_threshold': 75}
                ]
            return schools
        
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            # Return the default hardcoded schools as fallback
            return [
                {'name': 'Kentucky University', 'athletic_threshold': 80, 'academic_threshold': 70},
                {'name': 'Duke University', 'athletic_threshold': 85, 'academic_threshold': 90},
                {'name': 'UCLA', 'athletic_threshold': 75, 'academic_threshold': 80},
                {'name': 'North Carolina', 'athletic_threshold': 70, 'academic_threshold': 75},
                {'name': 'Kansas University', 'athletic_threshold': 65, 'academic_threshold': 70},
                {'name': 'Michigan State', 'athletic_threshold': 60, 'academic_threshold': 75},
                {'name': 'Villanova', 'athletic_threshold': 55, 'academic_threshold': 85},
                {'name': 'Gonzaga', 'athletic_threshold': 50, 'academic_threshold': 75}
            ]
    def positional_size_multiplier_calculator(self, height, position):
        height_standard = self.height_standards.get(position)
        if height_standard is None:
            return "1"
        size_diff = height - height_standard
        positional_size_multiplier = (size_diff * 0.05)+1
        max_positional_size_multiplier = 1.15
        if positional_size_multiplier > max_positional_size_multiplier:
            positional_size_multiplier = max_positional_size_multiplier
        min_positional_size_multiplier = 0.85
        if positional_size_multiplier < min_positional_size_multiplier:
            positional_size_multiplier = min_positional_size_multiplier
        return positional_size_multiplier
    def global_size_multiplier_calculator(self, height):
        global_size_diff = height - 78
        global_size_multiplier = (global_size_diff * 0.05)+1
        if global_size_multiplier > 1.25:
            global_size_multiplier = 1.25
        if global_size_multiplier < 0.75:
            global_size_multiplier = 0.75
        return global_size_multiplier
    def SizeIndex_calculator(self, height, position):
        SizeIndex = (self.positional_size_multiplier_calculator(height, position)*(.65) + self.global_size_multiplier_calculator(height)*(.35))
        return SizeIndex

    def HS_league_score(self, state, hs_league, classification):
        db_path = os.path.join(os.path.dirname(__file__), 'basketball_data.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(
        'SELECT score FROM hs_league_scores WHERE state = ? AND league = ? AND classification = ?',
        (state, hs_league, classification)
    )
    
        result = cursor.fetchone()
        conn.close()
    
        if result:
            return result[0]
        else:
            # Return a default value if combination not found
            return 50

    def HS_competition_score_calculator(self, HS_league_score, hs_role, hs_wpr):
        role_scores = {
            'Star' : 1.3,
            'Key' : 1.15,
            'Contributor' : 1.0,
            'Role Player' : 0.85,
            'Practice Player' : 0.7
        }
        hsrole_multiplier = role_scores.get(hs_role, 1.0)
        try:
            wpr = float(hs_wpr)
            if wpr <= 50:
            # Map 0-50 to 0.7-1.0
                hswpr_multiplier = 0.7 + (wpr / 50 * 0.3)
            else:
            # Map 50-100 to 1.0-1.2
                hswpr_multiplier = 1.0 + ((wpr - 50) / 50 * 0.2)
        except (ValueError, TypeError):
        # Default to neutral multiplier if WPR is invalid
            hswpr_multiplier = 1.0
        HS_competition_score = HS_league_score * hswpr_multiplier * hsrole_multiplier
        return int(round(HS_competition_score))
    def AAU_circuit_score(self,aau_circuit):
        db_path = os.path.join(os.path.dirname(__file__), 'basketball_data.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(
            'SELECT score FROM aau_circuit_scores WHERE circuit = ?',
            (aau_circuit,)
        )

        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        else:
            # Return a default value if circuit not found
            return 45
    def AAU_competition_score_calculator(self,AAU_circuit_score, aau_role, aau_wpr):
        role_scores = {
            'Star' : 1.3,
            'Key' : 1.15,
            'Contributor' : 1.0,
            'Role Player' : 0.85,
            'Practice Player' : 0.7,
            'NO AAU' : 0.0
        }
        aaurole_multiplier = role_scores.get(aau_role, 1.0)
        try:
            wpr = float(aau_wpr)
            if wpr <= 50:
                # Map 0-50 to 0.7-1.0
                aauwpr_multiplier = 0.7 + (wpr / 50 * 0.3)
            else:
                # Map 50-100 to 1.0-1.2
                aauwpr_multiplier = 1.0 + ((wpr - 50) / 50 * 0.2)
        except (ValueError, TypeError):
            # Default to neutral multiplier if WPR is invalid
            aauwpr_multiplier = 1.0
        AAU_competition_score = AAU_circuit_score * aauwpr_multiplier * aaurole_multiplier
        return int(round(AAU_competition_score))
    def RecruitScoreCalculator(self, HS_competition_score, AAU_competition_score, SizeIndex):
        HS_WEIGHT = 0.5
        AAU_WEIGHT = 0.5

        # If AAU score is significantly higher (20+ points) than HS score,
        # give more weight to AAU performance
        if AAU_competition_score >= (HS_competition_score + 20):
            HS_WEIGHT = 0.4
            AAU_WEIGHT = 0.6
        if HS_competition_score >= (AAU_competition_score + 20):
            HS_WEIGHT = 0.6
            AAU_WEIGHT = 0.4
        if AAU_competition_score >= (HS_competition_score + 30):
            HS_WEIGHT = 0.3
            AAU_WEIGHT = 0.7
        if AAU_competition_score == 0:
            HS_WEIGHT = 1.0
            AAU_WEIGHT = 0.0
        # Calculate weighted score
        weighted_competition_score = (HS_competition_score * HS_WEIGHT) + (AAU_competition_score * AAU_WEIGHT)

        # Apply positional size multiplier
        raw_RecruitScore = weighted_competition_score * SizeIndex
        if raw_RecruitScore > 160:
            raw_RecruitScore = 160
        RecruitScore = (raw_RecruitScore/160)*100
        return int(round(RecruitScore))
    def calculate_academic_score(self, data):
        """Calculate academic score on a 1-10 scale based on GPA and test scores"""
        # Get GPA score
        if isinstance(data, dict):
            gpa = float(data.get('gpa', '3.0'))
        else:
            # Handle case where data is just a GPA value
            gpa = float(data)
            return min(10, (gpa / 4.0) * 10)  # Scale 0-4 GPA to 0-10 score
        
        # Initialize gpa_score with default value
        gpa_score = 1
        for range_data in self.gpa_ranges:
            if range_data['min'] <= gpa <= range_data['max']:
                gpa_score = range_data['score']
                break
        
        # Get SAT score if provided
        sat_score = 1  # Default lowest score
        if 'sat' in data and data['sat']:
            sat = int(data['sat'])
            for range_data in self.sat_ranges:
                if range_data['min'] <= sat <= range_data['max']:
                    sat_score = range_data['score']
                    break
    
        # Get ACT score if provided
        act_score = 1  # Default lowest score
        if 'act' in data and data['act']:
            act = int(data['act'])
            for range_data in self.act_ranges:
                if range_data['min'] <= act <= range_data['max']:
                    act_score = range_data['score']
                    break
    
        test_score = max(sat_score, act_score)
        
        # Calculate final score - weight GPA more if both present
        if 'sat' not in data and 'act' not in data:
            final_academic_score = gpa_score
        else:
            final_academic_score = (gpa_score * 0.6) + (test_score * 0.4)
        
        return round(final_academic_score)
    
    
    def get_matching_schools(self, RecruitScore, academic_score):
        """Find matching schools based on both athletic and academic scores"""
        matches = []

        for school in self.schools:
            if academic_score == school['academic_threshold']:
                academic_match = 100
            else:
                academic_match = 100-(abs((school['academic_threshold'] - academic_score)) * 20)
                if academic_match < 0:
                    academic_match = 0
            if RecruitScore >= school['athletic_threshold'] and RecruitScore <= school['athletic_maximum']:
                athletic_match = 100  # Recruit meets or exceeds the threshold
            elif RecruitScore > school['athletic_maximum']:
                excess = RecruitScore - school['athletic_maximum']
                athletic_match = max(0, 100 - (excess * 5))  # Reduce by 5% for each point above maximum
            else:
                excess = school['athletic_threshold'] - RecruitScore
                athletic_match = 100 - (excess * 5)
            if athletic_match < 0:
                athletic_match = 0
            if RecruitScore < 45:
                overall_match = (athletic_match * 0.6) + (academic_match * 0.4)
            elif RecruitScore > 80:
                overall_match = (athletic_match * 0.85) + (academic_match * 0.15)
            elif RecruitScore > 65:
                overall_match = (athletic_match * 0.75) + (academic_match * 0.25)
            else:
                overall_match = (athletic_match * 0.7) + (academic_match * 0.3)

            if overall_match > 0:
                matches.append({
                    'name': school['name'],
                    'match': round(overall_match),
                    'athletic_match': round(athletic_match),
                    'academic_match': round(academic_match)
                })
        
        matches.sort(key=lambda x: x['match'], reverse=True)
        # Return top 3 matches
        return matches[:3]