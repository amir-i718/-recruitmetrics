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

    def calculate_gpa_score(self, gpa):
        """Convert GPA to a 0-100 score"""
        return min(100, (float(gpa) / 4.0) * 100)

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

    # We're not using the skillset score anymore, so this method can be removed

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