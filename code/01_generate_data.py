"""
Project 1.1: Wekruit - A/B Testing for Mock Interview Competitions
Generate simulated user activity data for A/B testing analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_USERS = 5000
START_DATE = datetime(2025, 9, 1)
END_DATE = datetime(2025, 12, 31)
NUM_COMPETITIONS = 16  # Weekly competitions over 4 months

print("Generating Wekruit A/B Testing Data...")

# Generate users table
users = pd.DataFrame({
    'user_id': range(1, NUM_USERS + 1),
    'signup_date': [START_DATE + timedelta(days=random.randint(0, 30)) for _ in range(NUM_USERS)],
    'user_segment': np.random.choice(['student', 'professional', 'career_changer'], NUM_USERS, p=[0.5, 0.3, 0.2]),
    'variant_group': np.random.choice(['control', 'treatment'], NUM_USERS, p=[0.5, 0.5])
})

# Generate competitions table
competitions = pd.DataFrame({
    'competition_id': range(1, NUM_COMPETITIONS + 1),
    'competition_date': [START_DATE + timedelta(weeks=i) for i in range(NUM_COMPETITIONS)],
    'competition_type': np.random.choice(['technical', 'behavioral', 'case_study'], NUM_COMPETITIONS)
})

# Generate user activity data
activities = []
activity_id = 1

for _, user in users.iterrows():
    user_id = user['user_id']
    signup_date = user['signup_date']
    variant = user['variant_group']
    
    # Different engagement rates for control vs treatment
    if variant == 'control':
        engagement_prob = 0.23  # 23% engagement rate
        completion_prob = 0.60  # 60% complete after starting
    else:
        engagement_prob = 0.425  # 42.5% engagement rate (85% increase)
        completion_prob = 0.68  # Higher completion rate
    
    # Iterate through competitions after user signup
    for _, comp in competitions.iterrows():
        comp_date = comp['competition_date']
        
        # Only consider competitions after signup
        if comp_date < signup_date:
            continue
        
        # Determine if user engages with this competition
        if random.random() < engagement_prob:
            # User signs up for competition
            activities.append({
                'activity_id': activity_id,
                'user_id': user_id,
                'competition_id': comp['competition_id'],
                'activity_timestamp': comp_date + timedelta(hours=random.randint(0, 48)),
                'activity_type': 'signup',
                'session_duration': 0
            })
            activity_id += 1
            
            # Funnel: signup -> start_interview
            if random.random() < 0.75:  # 75% start after signup
                start_time = comp_date + timedelta(hours=random.randint(48, 96))
                activities.append({
                    'activity_id': activity_id,
                    'user_id': user_id,
                    'competition_id': comp['competition_id'],
                    'activity_timestamp': start_time,
                    'activity_type': 'start_interview',
                    'session_duration': 0
                })
                activity_id += 1
                
                # Funnel: start_interview -> complete_interview
                if random.random() < completion_prob:
                    duration = random.randint(1800, 3600)  # 30-60 minutes
                    activities.append({
                        'activity_id': activity_id,
                        'user_id': user_id,
                        'competition_id': comp['competition_id'],
                        'activity_timestamp': start_time + timedelta(seconds=duration),
                        'activity_type': 'complete_interview',
                        'session_duration': duration
                    })
                    activity_id += 1
                    
                    # Funnel: complete_interview -> view_feedback
                    if random.random() < 0.85:
                        activities.append({
                            'activity_id': activity_id,
                            'user_id': user_id,
                            'competition_id': comp['competition_id'],
                            'activity_timestamp': start_time + timedelta(seconds=duration + random.randint(300, 1800)),
                            'activity_type': 'view_feedback',
                            'session_duration': random.randint(300, 900)
                        })
                        activity_id += 1
                        
                        # Funnel: view_feedback -> share_result
                        if random.random() < 0.35:
                            activities.append({
                                'activity_id': activity_id,
                                'user_id': user_id,
                                'competition_id': comp['competition_id'],
                                'activity_timestamp': start_time + timedelta(seconds=duration + random.randint(1800, 3600)),
                                'activity_type': 'share_result',
                                'session_duration': random.randint(60, 300)
                            })
                            activity_id += 1

user_activity = pd.DataFrame(activities)

# Save to CSV
users.to_csv('/home/ubuntu/interview_prep/project_1_wekruit/data/users.csv', index=False)
competitions.to_csv('/home/ubuntu/interview_prep/project_1_wekruit/data/competitions.csv', index=False)
user_activity.to_csv('/home/ubuntu/interview_prep/project_1_wekruit/data/user_activity.csv', index=False)

print(f"Generated {len(users)} users")
print(f"Generated {len(competitions)} competitions")
print(f"Generated {len(user_activity)} activity records")
print("\nData saved to:")
print("  - /home/ubuntu/interview_prep/project_1_wekruit/data/users.csv")
print("  - /home/ubuntu/interview_prep/project_1_wekruit/data/competitions.csv")
print("  - /home/ubuntu/interview_prep/project_1_wekruit/data/user_activity.csv")
