class RecruitScoreEngine:
    def __init__(self):
        # How important each part is
        self.weights = {
            'gpa': 0.5,            # Grades are 50% of your score
            'height': 0.5,         # Height is 50% of your score
        }
        
        # List of colleges for matching
        self.schools = [
            {'name': 'Kentucky University', 'threshold': 80},
            {'name': 'Duke University', 'threshold': 85},
            {'name': 'UCLA', 'threshold': 75},
            {'name': 'North Carolina', 'threshold': 70},
            {'name': 'Kansas University', 'threshold': 65},
            {'name': 'Michigan State', 'threshold': 60},
            {'name': 'Villanova', 'threshold': 55},
            {'name': 'Gonzaga', 'threshold': 50}
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

    def calculate_academic_score(self, data):
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
    
        # Use best standardized test score
        test_score = max(sat_score, act_score)
        
        # Calculate final score - weight GPA more if both present
        if 'sat' not in data and 'act' not in data:
            final_academic_score = gpa_score
        else:
            final_academic_score = (gpa_score * 0.6) + (test_score * 0.4)
        
        return round(final_academic_score, 1)


    def calculate_height_score(self, height_str):
        """Calculate height score based on standard height"""
        # Convert height from string (like "6'2"") to inches
        feet, inches = map(int, height_str.replace('"', '').split("'"))
        height_inches = (feet * 12) + inches
        
        # Average height baseline (6'3")
        benchmark = 75
        difference = height_inches - benchmark
        
        # Score calculation
        if difference >= 0:
            return min(100, 85 + (difference * 5))
        else:
            return max(60, 85 + (difference * 7))

    def calculate_recruit_score(self, data):
        """Calculate the final recruit score"""
        # Get individual scores
        gpa_score = self.calculate_gpa_score(data['gpa'])
        height_score = self.calculate_height_score(data['height'])
        
        # Calculate final weighted score
        final_score = (
            (gpa_score * self.weights['gpa']) +
            (height_score * self.weights['height'])
        )
        
        return round(final_score, 1)

    def get_matching_schools(self, score):
        matches = []
        
        for school in self.schools:
            # Calculate match percentage
            match_percent = min(100, (score / school['threshold']) * 100)
            
            # Only include if match is reasonable
            if match_percent > 0:
                matches.append({
                    'name': school['name'],
                    'match': round(match_percent)
                })
        
        # Sort by match percentage (highest first)
        matches.sort(key=lambda x: x['match'], reverse=True)
        
        # Return top 3 matches
        return matches[:3]