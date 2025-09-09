class RecruitScoreEngine:
    def __init__(self):
        # List of colleges for matching with athletic and academic thresholds
        self.schools = [
            {'name': 'Kentucky University', 'athletic_threshold': 80, 'academic_threshold': 70},
            {'name': 'Duke University', 'athletic_threshold': 85, 'academic_threshold': 90},
            {'name': 'UCLA', 'athletic_threshold': 75, 'academic_threshold': 80},
            {'name': 'North Carolina', 'athletic_threshold': 70, 'academic_threshold': 75},
            {'name': 'Kansas University', 'athletic_threshold': 65, 'academic_threshold': 70},
            {'name': 'Michigan State', 'athletic_threshold': 60, 'academic_threshold': 75},
            {'name': 'Villanova', 'athletic_threshold': 55, 'academic_threshold': 85},
            {'name': 'Gonzaga', 'athletic_threshold': 50, 'academic_threshold': 75}
        ]
        
        # Position average heights (in inches)
        self.position_heights = {
            'Guard': 74,  # 6'1"
            'Wing': 77,  # 6'3"
            'Forward': 79,  # 6'6"
            'Big': 81,   # 6'9"
        }
        self.gpa_ranges = [
            {'min': 3.8, 'max': 4.0, 'score': 10},
            {'min': 3.5, 'max': 3.79, 'score': 9},
            {'min': 3.2, 'max': 3.49, 'score': 8},
            {'min': 3.0, 'max': 3.19, 'score': 7},
            {'min': 2.8, 'max': 2.99, 'score': 6},
            {'min': 2.5, 'max': 2.79, 'score': 5},
            {'min': 2.3, 'max': 2.49, 'score': 4},
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
    def calculate_aau_quality_score(self, AAU_Circuit):
        """Calculate AAU quality score based on level/division"""
        aau_scores = {
            'Gold': 100,
            'Silver': 80,
            'Bronze': 60,
            'Local': 40,
            'None': 20
        }
        
        return aau_scores.get(AAU_Circuit, 20)  # Default to lowest if not found

    def calculate_hs_quality_score(self, HS_league):
        """Calculate high school quality score based on competition level"""
        hs_scores = {
            'National': 100,
            'State': 80,
            'Regional': 60,
            'Local': 40
        }
        
        return hs_scores.get(HS_league, 40)  # Default to lowest if not found

    def calculate_position_size_factor(self, position, height_str):
        """Calculate position size multiplier based on height vs. position standard"""
        # Convert height from string (like "6'2"") to inches
        feet, inches = map(int, height_str.replace('"', '').split("'"))
        height_inches = (feet * 12) + inches
        
        # Get benchmark height for this position
        benchmark = self.position_heights.get(position, 78)  # Default to SF if position not found
        
        difference = height_inches - benchmark
        
       
        if difference >= 0:
            # Taller than average for position is good
            return min(1.2, 1.0 + (difference * 0.05))  # Cap at 1.5x multiplier
        else:
            # Shorter than average decreases multiplier faster
            return max(0.7, 1.0 + (difference * 0.06))   # Floor at 0.7x multiplier

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
    
        # Use best standardized test score
        test_score = max(sat_score, act_score)
        
        # Calculate final score - weight GPA more if both present
        if 'sat' not in data and 'act' not in data:
            final_academic_score = gpa_score
        else:
            final_academic_score = (gpa_score * 0.6) + (test_score * 0.4)
        
        return round(final_academic_score, 1)

    def calculate_recruit_score(self, data):
        position = data.get('position', 'Guard')
        height = data.get('height', "6'4\"")
        if position == 'Guard':
          aau_score = self.calculate_aau_quality_score("Gold")  # 100
          hs_score = self.calculate_hs_quality_score("National")  # 100
        elif position == 'Wing':
          aau_score = self.calculate_aau_quality_score("Silver")  # 80
          hs_score = self.calculate_hs_quality_score("State")  # 80
        elif position == 'Forward':
          aau_score = self.calculate_aau_quality_score("Bronze")  # 60
          hs_score = self.calculate_hs_quality_score("Regional")  # 60
        else:  # Big
          aau_score = self.calculate_aau_quality_score("Local")  # 40
          hs_score = self.calculate_hs_quality_score("Local")  # 40
    
        # Calculate average
        competition_avg = (aau_score + hs_score) / 2  # 90 instead of 30
        
        position_size_factor = self.calculate_position_size_factor(position, height)
        
        # Calculate recruit score
        recruit_score = competition_avg * position_size_factor
        
        # Get academic score
        academic_score = self.calculate_academic_score(data)
        
        # Return results
        return {
            'recruit_score': round(recruit_score, 1),
            'academic_score': round(academic_score, 1),
            'competition_avg': round(competition_avg, 1),
            'position_size_factor': round(position_size_factor, 2)
        }

    def get_matching_schools(self, recruit_score, academic_score):
        """Find matching schools based on both athletic and academic scores"""
        matches = []
        
        for school in self.schools:
            # Calculate athletic match percentage
            athletic_match = min(100, (recruit_score / school['athletic_threshold']) * 100)
            
            # Calculate academic match percentage
            academic_match = min(100, (academic_score / school['academic_threshold']) * 100)
            
            # Overall match is weighted 70% athletic, 30% academic
            overall_match = (athletic_match * 0.7) + (academic_match * 0.3)
            
            if overall_match > 0:
                matches.append({
                    'name': school['name'],
                    'match': round(overall_match),
                    'athletic_match': round(athletic_match),
                    'academic_match': round(academic_match)
                })
        
        # Sort by overall match percentage (highest first)
        matches.sort(key=lambda x: x['match'], reverse=True)
        
        # Return top 3 matches
        return matches[:3]