
# JEE Mains Strategy and Topic Weightage
# AI-enabled version with intelligent topic recommendations and personalized study plans
# Enhanced with Agentic AI capabilities for dynamic learning optimization
# Create strategy tab

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Define subject weightages
subjects = {
    'Physics': 0.33,
    'Chemistry': 0.33, 
    'Mathematics': 0.34
}

# Define topic weightages within each subject
physics_topics = {
    'Mechanics': 0.25,
    'Electromagnetism': 0.20,
    'Modern Physics': 0.15,
    'Thermodynamics': 0.15,
    'Optics': 0.15,
    'Waves': 0.10
}

chemistry_topics = {
    'Physical Chemistry': 0.35,
    'Organic Chemistry': 0.35,
    'Inorganic Chemistry': 0.30
}

mathematics_topics = {
    'Calculus': 0.25,
    'Algebra': 0.25,
    'Coordinate Geometry': 0.20,
    'Vectors & 3D': 0.15,
    'Statistics': 0.15
}

def generate_study_plan(student_scores):
    """Generate personalized study plan based on student scores"""
    scaler = MinMaxScaler()
    
    # Normalize scores between 0 and 1
    normalized_scores = scaler.fit_transform(np.array(student_scores).reshape(-1,1))
    
    # Calculate study hours needed (inverse relationship with scores)
    study_hours = 1 - normalized_scores
    
    return study_hours.flatten()

def recommend_topics(weak_areas):
    """Recommend topics to focus on based on weak areas"""
    recommendations = []
    for subject, topics in weak_areas.items():
        for topic in topics:
            if subject == 'Physics':
                weight = physics_topics[topic]
            elif subject == 'Chemistry':
                weight = chemistry_topics[topic]
            else:
                weight = mathematics_topics[topic]
                
            recommendations.append({
                'subject': subject,
                'topic': topic,
                'priority': weight
            })
    
    return sorted(recommendations, key=lambda x: x['priority'], reverse=True)

def optimize_strategy(student_data, target_score):
    """Optimize study strategy based on current performance and target score"""
    current_score = student_data['average_score']
    improvement_needed = target_score - current_score
    
    if improvement_needed <= 0:
        return "You're already at or above your target score!"
        
    # Calculate required improvement per subject
    subject_improvements = {}
    for subject, weight in subjects.items():
        subject_improvements[subject] = improvement_needed * weight
        
    return subject_improvements

def create_strategy_tab(student_data, target_score):
    """Create strategy tab with personalized recommendations and study plan"""
    # Get topic recommendations
    topic_recommendations = recommend_topics(student_data['weak_areas'])
    
    # Get optimized strategy
    strategy = optimize_strategy(student_data, target_score)
    
    # Create strategy dataframe
    strategy_df = pd.DataFrame(topic_recommendations)
    
    # Add recommended hours column based on priority
    if isinstance(strategy, dict):
        strategy_df['recommended_hours'] = strategy_df.apply(
            lambda x: strategy[x['subject']] * x['priority'], axis=1)
    else:
        strategy_df['recommended_hours'] = 0
        
    return strategy_df

# Example usage
student_data = {
    'average_score': 85,
    'weak_areas': {
        'Physics': ['Modern Physics', 'Optics'],
        'Chemistry': ['Organic Chemistry'],
        'Mathematics': ['Vectors & 3D']
    }
}

target_score = 95

# Generate recommendations
topic_recommendations = recommend_topics(student_data['weak_areas'])
strategy = optimize_strategy(student_data, target_score)
strategy_tab = create_strategy_tab(student_data, target_score)    
