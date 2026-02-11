"""
Synthetic Student Commit Data Generator

This script generates realistic commit patterns for testing the GitHub monitoring agent.
It simulates various student behaviors: consistent workers, procrastinators, 
struggling students, inactive students, and collaborative teams.
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict
import uuid

class StudentCommitGenerator:
    """Generates synthetic commit data mimicking real student behavior patterns."""
    
    def __init__(self, course_start_date: str, course_duration_weeks: int = 15):
        """
        Initialize the generator.
        
        Args:
            course_start_date: Start date in 'YYYY-MM-DD' format
            course_duration_weeks: Length of course in weeks
        """
        self.start_date = datetime.strptime(course_start_date, '%Y-%m-%d')
        self.end_date = self.start_date + timedelta(weeks=course_duration_weeks)
        self.duration_days = (self.end_date - self.start_date).days
        
    def generate_commit_timestamp(self, day_offset: int, hour_preference: str = 'evening') -> str:
        """
        Generate a realistic commit timestamp.
        
        Args:
            day_offset: Days from course start
            hour_preference: 'morning', 'afternoon', 'evening', or 'late_night'
        """
        commit_date = self.start_date + timedelta(days=day_offset)
        
        # Realistic hour distributions based on student work patterns
        hour_ranges = {
            'morning': (8, 12),
            'afternoon': (13, 17),
            'evening': (18, 23),
            'late_night': (0, 3)
        }
        
        hour_range = hour_ranges.get(hour_preference, (18, 23))
        hour = random.randint(hour_range[0], hour_range[1])
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        commit_datetime = commit_date.replace(hour=hour, minute=minute, second=second)
        return commit_datetime.isoformat() + 'Z'
    
    def generate_commit_message(self, commit_type: str) -> str:
        """Generate realistic commit messages."""
        messages = {
            'initial': [
                'Initial commit',
                'Project setup',
                'Added project files',
                'Started project'
            ],
            'feature': [
                'Implemented {} feature',
                'Added {} functionality',
                'Created {} module',
                'Built {} component'
            ],
            'bugfix': [
                'Fixed bug in {}',
                'Resolved issue with {}',
                'Corrected {} error',
                'Debugged {}'
            ],
            'update': [
                'Updated {}',
                'Modified {}',
                'Improved {}',
                'Refactored {}'
            ],
            'docs': [
                'Added documentation',
                'Updated README',
                'Added comments',
                'Documented code'
            ],
            'desperate': [
                'Trying to fix everything',
                'Please work',
                'Last minute changes',
                'Final updates',
                'Hopefully this works'
            ]
        }
        
        features = ['login', 'database', 'API', 'UI', 'tests', 'validation', 'authentication']
        
        message_template = random.choice(messages[commit_type])
        if '{}' in message_template:
            return message_template.format(random.choice(features))
        return message_template
    
    def generate_file_changes(self, commit_size: str) -> Dict:
        """
        Generate file change statistics.
        
        Args:
            commit_size: 'small', 'medium', 'large'
        """
        size_ranges = {
            'small': (5, 30),
            'medium': (30, 100),
            'large': (100, 500)
        }
        
        additions = random.randint(*size_ranges[commit_size])
        deletions = random.randint(0, additions // 2)
        files_changed = random.randint(1, max(1, additions // 20))
        
        return {
            'additions': additions,
            'deletions': deletions,
            'files_changed': files_changed,
            'total_changes': additions + deletions
        }
    
    def generate_consistent_student(self, student_id: str, repo_name: str) -> List[Dict]:
        """
        Generate commits for a consistently working student.
        Pattern: Regular commits throughout the semester, 2-4 times per week.
        """
        commits = []
        commit_days = []
        
        # Generate regular commit schedule (2-4 commits per week)
        current_day = 0
        while current_day < self.duration_days:
            # Commit every 2-3 days
            current_day += random.randint(2, 4)
            if current_day < self.duration_days:
                commit_days.append(current_day)
        
        # Add initial commit
        commits.append(self._create_commit(
            student_id, repo_name, 0, 'initial', 'small', 'morning'
        ))
        
        # Regular commits
        for day in commit_days:
            commit_type = random.choice(['feature', 'update', 'bugfix'])
            commit_size = random.choice(['small', 'medium'])
            time_pref = random.choice(['afternoon', 'evening'])
            
            commits.append(self._create_commit(
                student_id, repo_name, day, commit_type, commit_size, time_pref
            ))
        
        # Add some documentation commits
        for _ in range(random.randint(2, 4)):
            day = random.randint(0, self.duration_days)
            commits.append(self._create_commit(
                student_id, repo_name, day, 'docs', 'small', 'evening'
            ))
        
        return sorted(commits, key=lambda x: x['timestamp'])
    
    def generate_procrastinator_student(self, student_id: str, repo_name: str) -> List[Dict]:
        """
        Generate commits for a procrastinating student.
        Pattern: Minimal activity early, burst of activity near deadlines.
        """
        commits = []
        
        # Initial commit
        commits.append(self._create_commit(
            student_id, repo_name, random.randint(0, 7), 'initial', 'small', 'late_night'
        ))
        
        # Few commits in first 2/3 of semester
        early_period = int(self.duration_days * 0.66)
        for _ in range(random.randint(2, 5)):
            day = random.randint(10, early_period)
            commits.append(self._create_commit(
                student_id, repo_name, day, 'update', 'small', 'evening'
            ))
        
        # Burst of commits in final third
        late_period_start = early_period
        for _ in range(random.randint(15, 25)):
            day = random.randint(late_period_start, self.duration_days - 1)
            commit_type = random.choice(['feature', 'bugfix', 'desperate'])
            commit_size = random.choice(['medium', 'large'])
            time_pref = random.choice(['late_night', 'late_night', 'evening'])
            
            commits.append(self._create_commit(
                student_id, repo_name, day, commit_type, commit_size, time_pref
            ))
        
        return sorted(commits, key=lambda x: x['timestamp'])
    
    def generate_struggling_student(self, student_id: str, repo_name: str) -> List[Dict]:
        """
        Generate commits for a struggling student.
        Pattern: Initial activity, then declining/erratic commits, small changes.
        """
        commits = []
        
        # Good start
        commits.append(self._create_commit(
            student_id, repo_name, 0, 'initial', 'small', 'morning'
        ))
        
        # Regular activity first 1/3
        early_period = int(self.duration_days * 0.33)
        for day in range(2, early_period, random.randint(3, 5)):
            commits.append(self._create_commit(
                student_id, repo_name, day, 'feature', 'small', 'afternoon'
            ))
        
        # Declining activity middle 1/3 - irregular, small commits
        middle_start = early_period
        middle_end = int(self.duration_days * 0.66)
        for _ in range(random.randint(3, 6)):
            day = random.randint(middle_start, middle_end)
            commits.append(self._create_commit(
                student_id, repo_name, day, 'bugfix', 'small', 'late_night'
            ))
        
        # Minimal activity final 1/3 - desperate attempts
        for _ in range(random.randint(2, 4)):
            day = random.randint(middle_end, self.duration_days - 1)
            commits.append(self._create_commit(
                student_id, repo_name, day, 'desperate', 'small', 'late_night'
            ))
        
        return sorted(commits, key=lambda x: x['timestamp'])
    
    def generate_inactive_student(self, student_id: str, repo_name: str) -> List[Dict]:
        """
        Generate commits for an inactive student.
        Pattern: Very few commits, large gaps in activity.
        """
        commits = []
        
        # Initial commit only
        commits.append(self._create_commit(
            student_id, repo_name, random.randint(0, 14), 'initial', 'small', 'evening'
        ))
        
        # 1-3 sporadic commits throughout semester
        for _ in range(random.randint(1, 3)):
            day = random.randint(14, self.duration_days - 1)
            commits.append(self._create_commit(
                student_id, repo_name, day, 'update', 'small', 'late_night'
            ))
        
        return sorted(commits, key=lambda x: x['timestamp'])
    
    def generate_team_project(self, team_members: List[str], repo_name: str) -> List[Dict]:
        """
        Generate commits for a team project with multiple contributors.
        Pattern: Mixed contribution levels, some overlap in timing.
        """
        all_commits = []
        
        # Assign roles to team members
        roles = ['leader', 'contributor', 'minimal']
        member_roles = {}
        
        for i, member in enumerate(team_members):
            if i == 0:
                member_roles[member] = 'leader'
            elif i < len(team_members) - 1:
                member_roles[member] = 'contributor'
            else:
                member_roles[member] = 'minimal'
        
        # Generate commits based on roles
        for member, role in member_roles.items():
            if role == 'leader':
                # 40-50% of commits
                commit_count = random.randint(25, 35)
            elif role == 'contributor':
                # 30-40% of commits
                commit_count = random.randint(15, 25)
            else:
                # 10-20% of commits
                commit_count = random.randint(5, 12)
            
            for _ in range(commit_count):
                day = random.randint(0, self.duration_days - 1)
                commit_type = random.choice(['feature', 'bugfix', 'update', 'docs'])
                commit_size = random.choice(['small', 'medium', 'large'])
                time_pref = random.choice(['afternoon', 'evening', 'late_night'])
                
                all_commits.append(self._create_commit(
                    member, repo_name, day, commit_type, commit_size, time_pref
                ))
        
        return sorted(all_commits, key=lambda x: x['timestamp'])
    
    def _create_commit(self, author: str, repo: str, day_offset: int, 
                      commit_type: str, commit_size: str, time_pref: str) -> Dict:
        """Helper method to create a single commit object."""
        return {
            'commit_id': str(uuid.uuid4())[:8],
            'repository': repo,
            'author': author,
            'timestamp': self.generate_commit_timestamp(day_offset, time_pref),
            'message': self.generate_commit_message(commit_type),
            'changes': self.generate_file_changes(commit_size),
            'branch': 'main'
        }
    
    def generate_course_dataset(self, num_students: int = 50, 
                               num_teams: int = 5) -> Dict:
        """
        Generate a complete course dataset with various student patterns.
        
        Args:
            num_students: Number of individual student projects
            num_teams: Number of team projects
        """
        dataset = {
            'course_info': {
                'start_date': self.start_date.isoformat(),
                'end_date': self.end_date.isoformat(),
                'duration_weeks': self.duration_days // 7,
                'generated_at': datetime.now().isoformat()
            },
            'individual_projects': [],
            'team_projects': []
        }
        
        # Generate individual student projects
        pattern_distribution = {
            'consistent': int(num_students * 0.35),  # 35%
            'procrastinator': int(num_students * 0.25),  # 25%
            'struggling': int(num_students * 0.20),  # 20%
            'inactive': int(num_students * 0.20)  # 20%
        }
        
        student_count = 0
        for pattern, count in pattern_distribution.items():
            for i in range(count):
                student_id = f'student_{student_count:03d}'
                repo_name = f'{student_id}_project'
                
                if pattern == 'consistent':
                    commits = self.generate_consistent_student(student_id, repo_name)
                elif pattern == 'procrastinator':
                    commits = self.generate_procrastinator_student(student_id, repo_name)
                elif pattern == 'struggling':
                    commits = self.generate_struggling_student(student_id, repo_name)
                else:  # inactive
                    commits = self.generate_inactive_student(student_id, repo_name)
                
                dataset['individual_projects'].append({
                    'student_id': student_id,
                    'repository': repo_name,
                    'pattern_type': pattern,
                    'total_commits': len(commits),
                    'commits': commits
                })
                
                student_count += 1
        
        # Generate team projects
        for team_num in range(num_teams):
            team_size = random.randint(3, 5)
            team_members = [f'team_{team_num}_member_{i}' for i in range(team_size)]
            repo_name = f'team_{team_num}_project'
            
            commits = self.generate_team_project(team_members, repo_name)
            
            dataset['team_projects'].append({
                'team_id': f'team_{team_num}',
                'repository': repo_name,
                'members': team_members,
                'total_commits': len(commits),
                'commits': commits
            })
        
        return dataset


def main():
    """Generate and save synthetic dataset."""
    print("Generating synthetic student commit data...")
    
    # Initialize generator for a typical semester
    generator = StudentCommitGenerator(
        course_start_date='2025-01-15',
        course_duration_weeks=15
    )
    
    # Generate dataset
    dataset = generator.generate_course_dataset(
        num_students=50,
        num_teams=5
    )
    
    # Save to JSON file
    output_file = 'synthetic_student_commits.json'
    with open(output_file, 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"\n✓ Dataset generated successfully!")
    print(f"  - Output file: {output_file}")
    print(f"  - Individual projects: {len(dataset['individual_projects'])}")
    print(f"  - Team projects: {len(dataset['team_projects'])}")
    print(f"  - Total commits: {sum(p['total_commits'] for p in dataset['individual_projects'])} (individual)")
    print(f"                  + {sum(p['total_commits'] for p in dataset['team_projects'])} (team)")
    
    # Print pattern distribution
    print("\n  Pattern distribution:")
    for pattern in ['consistent', 'procrastinator', 'struggling', 'inactive']:
        count = sum(1 for p in dataset['individual_projects'] if p['pattern_type'] == pattern)
        print(f"    - {pattern}: {count} students")


if __name__ == '__main__':
    main()