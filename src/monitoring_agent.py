import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from collections import defaultdict
import statistics


class StudentAnalyzer:
    
    def __init__(self, alert_thresholds: Dict = None):
        self.thresholds = alert_thresholds or {
            'min_commits_per_week': 2,
            'inactivity_days': 14,
            'procrastination_threshold': 0.6,
            'low_progress_threshold': 0.3,
            'small_commit_ratio': 0.7,
            'late_night_ratio': 0.5
        }
    
    def analyze_student(self, student_data: Dict, course_info: Dict) -> Dict:
        commits = student_data['commits']
        
        if not commits:
            return self._create_alert('inactive', student_data, 
                                     'No commits detected', severity='high')
        
        # Run all analysis functions
        activity_pattern = self._analyze_activity_pattern(commits, course_info)
        commit_quality = self._analyze_commit_quality(commits)
        temporal_analysis = self._analyze_temporal_patterns(commits, course_info)
        progress_tracking = self._track_progress_over_time(commits, course_info)
        
        # Detect concerning patterns
        flags = self._detect_flags(activity_pattern, commit_quality, 
                                   temporal_analysis, progress_tracking)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(flags)
        
        return {
            'student_id': student_data['student_id'],
            'repository': student_data['repository'],
            'analysis_date': datetime.now().isoformat(),
            'total_commits': len(commits),
            'flags': flags,
            'severity': self._calculate_severity(flags),
            'recommendations': recommendations,
            'metrics': {
                'activity_pattern': activity_pattern,
                'commit_quality': commit_quality,
                'temporal_analysis': temporal_analysis,
                'progress_tracking': progress_tracking
            }
        }
    
    def _analyze_activity_pattern(self, commits: List[Dict], course_info: Dict) -> Dict:
        if not commits:
            return {'pattern': 'inactive', 'consistency_score': 0}
        
        timestamps = [datetime.fromisoformat(c['timestamp'].replace('Z', '')) 
                     for c in commits]
        
        # Calculate time gaps between commits
        timestamps.sort()
        gaps = [(timestamps[i+1] - timestamps[i]).days 
                for i in range(len(timestamps) - 1)]
        
        # Metrics
        avg_gap = statistics.mean(gaps) if gaps else 0
        max_gap = max(gaps) if gaps else 0
        
        # Consistency score (0-1, higher is better)
        if len(gaps) > 1:
            gap_variance = statistics.variance(gaps)
            consistency_score = 1 / (1 + gap_variance / 100)
        else:
            consistency_score = 0.5
        
        # Determine pattern
        if max_gap > self.thresholds['inactivity_days']:
            pattern = 'irregular'
        elif avg_gap <= 3:
            pattern = 'consistent'
        elif avg_gap <= 7:
            pattern = 'moderate'
        else:
            pattern = 'sporadic'
        
        return {
            'pattern': pattern,
            'consistency_score': round(consistency_score, 2),
            'average_days_between_commits': round(avg_gap, 1),
            'longest_gap_days': max_gap,
            'total_commits': len(commits)
        }

    def _analyze_commit_quality(self, commits: List[Dict]) -> Dict:
        if not commits:
            return {'average_size': 0, 'quality_score': 0}
        
        commit_sizes = [c['changes']['total_changes'] for c in commits]
        avg_size = statistics.mean(commit_sizes)
        
        # Classify commits by size
        small_commits = sum(1 for size in commit_sizes if size < 50)
        medium_commits = sum(1 for size in commit_sizes if 50 <= size < 150)
        large_commits = sum(1 for size in commit_sizes if size >= 150)
        
        small_ratio = small_commits / len(commits)
        
        # Quality score (heuristic based on commit sizes)
        if 0.3 <= small_ratio <= 0.6 and medium_commits > 0:
            quality_score = 0.8
        elif small_ratio > 0.8:
            quality_score = 0.4
        elif large_commits / len(commits) > 0.5:
            quality_score = 0.6
        else:
            quality_score = 0.7
        
        # Analyze commit messages
        meaningful_messages = sum(1 for c in commits 
                                 if len(c['message']) > 10 and 
                                 not any(word in c['message'].lower() 
                                        for word in ['fix', 'update', 'change']))
        message_quality = meaningful_messages / len(commits)
        
        return {
            'average_commit_size': round(avg_size, 1),
            'small_commits': small_commits,
            'medium_commits': medium_commits,
            'large_commits': large_commits,
            'small_commit_ratio': round(small_ratio, 2),
            'quality_score': round(quality_score, 2),
            'message_quality_ratio': round(message_quality, 2)
        }
    
    def _analyze_temporal_patterns(self, commits: List[Dict], course_info: Dict) -> Dict:
        timestamps = [datetime.fromisoformat(c['timestamp'].replace('Z', '')) 
                     for c in commits]
        
        # Time of day distribution
        hours = [ts.hour for ts in timestamps]
        late_night = sum(1 for h in hours if h < 6 or h >= 23)
        morning = sum(1 for h in hours if 6 <= h < 12)
        afternoon = sum(1 for h in hours if 12 <= h < 18)
        evening = sum(1 for h in hours if 18 <= h < 23)
        
        late_night_ratio = late_night / len(commits)
        
        # Deadline pressure indicator
        start_date = datetime.fromisoformat(course_info['start_date'])
        end_date = datetime.fromisoformat(course_info['end_date'])
        course_duration = (end_date - start_date).days
        
        final_third_start = start_date + timedelta(days=course_duration * 2/3)
        final_third_commits = sum(1 for ts in timestamps if ts >= final_third_start)
        procrastination_ratio = final_third_commits / len(commits)
        
        return {
            'late_night_work_ratio': round(late_night_ratio, 2),
            'time_distribution': {
                'late_night': late_night,
                'morning': morning,
                'afternoon': afternoon,
                'evening': evening
            },
            'procrastination_indicator': round(procrastination_ratio, 2),
            'final_third_commits': final_third_commits
        }
    
    def _track_progress_over_time(self, commits: List[Dict], course_info: Dict) -> Dict:
        start_date = datetime.fromisoformat(course_info['start_date'])
        end_date = datetime.fromisoformat(course_info['end_date'])
        course_weeks = (end_date - start_date).days // 7
        
        # Organize commits by week
        weekly_commits = defaultdict(int)
        weekly_changes = defaultdict(int)
        
        for commit in commits:
            timestamp = datetime.fromisoformat(commit['timestamp'].replace('Z', ''))
            week_num = (timestamp - start_date).days // 7
            if 0 <= week_num < course_weeks:
                weekly_commits[week_num] += 1
                weekly_changes[week_num] += commit['changes']['total_changes']
        
        # Calculate trend
        weeks_with_activity = len(weekly_commits)
        active_weeks_ratio = weeks_with_activity / course_weeks if course_weeks > 0 else 0
        
        # Detect declining trend
        if weeks_with_activity >= 3:
            first_half_weeks = [w for w in weekly_commits.keys() if w < course_weeks // 2]
            second_half_weeks = [w for w in weekly_commits.keys() if w >= course_weeks // 2]
            
            first_half_avg = (sum(weekly_commits[w] for w in first_half_weeks) / 
                            len(first_half_weeks) if first_half_weeks else 0)
            second_half_avg = (sum(weekly_commits[w] for w in second_half_weeks) / 
                             len(second_half_weeks) if second_half_weeks else 0)
            
            if second_half_avg < first_half_avg * 0.5:
                trend = 'declining'
            elif second_half_avg > first_half_avg * 1.5:
                trend = 'increasing'
            else:
                trend = 'stable'
        else:
            trend = 'insufficient_data'
        
        return {
            'active_weeks': weeks_with_activity,
            'active_weeks_ratio': round(active_weeks_ratio, 2),
            'weekly_breakdown': dict(weekly_commits),
            'trend': trend,
            'average_commits_per_week': round(len(commits) / course_weeks, 1) if course_weeks > 0 else 0
        }
    
    def _detect_flags(self, activity: Dict, quality: Dict, 
                     temporal: Dict, progress: Dict) -> List[Dict]:
        flags = []
        
        # Flag 1: Inactivity
        if activity['longest_gap_days'] > self.thresholds['inactivity_days']:
            flags.append({
                'type': 'inactivity',
                'severity': 'high',
                'description': f"Longest gap between commits: {activity['longest_gap_days']} days",
                'metric_value': activity['longest_gap_days']
            })
        
        # Flag 2: Low overall progress
        if progress['active_weeks_ratio'] < self.thresholds['low_progress_threshold']:
            flags.append({
                'type': 'low_progress',
                'severity': 'high',
                'description': f"Active in only {progress['active_weeks']} weeks ({progress['active_weeks_ratio']*100:.0f}%)",
                'metric_value': progress['active_weeks_ratio']
            })
        
        # Flag 3: Procrastination
        if temporal['procrastination_indicator'] > self.thresholds['procrastination_threshold']:
            flags.append({
                'type': 'procrastination',
                'severity': 'medium',
                'description': f"{temporal['procrastination_indicator']*100:.0f}% of commits in final third of course",
                'metric_value': temporal['procrastination_indicator']
            })
        
        # Flag 4: Declining activity trend
        if progress['trend'] == 'declining':
            flags.append({
                'type': 'declining_activity',
                'severity': 'medium',
                'description': "Commit activity has declined significantly over time",
                'metric_value': progress['trend']
            })
        
        # Flag 5: Poor commit quality
        if quality['small_commit_ratio'] > self.thresholds['small_commit_ratio']:
            flags.append({
                'type': 'minimal_progress',
                'severity': 'low',
                'description': f"{quality['small_commit_ratio']*100:.0f}% of commits are very small",
                'metric_value': quality['small_commit_ratio']
            })
        
        # Flag 6: Excessive late-night work
        if temporal['late_night_work_ratio'] > self.thresholds['late_night_ratio']:
            flags.append({
                'type': 'burnout_risk',
                'severity': 'low',
                'description': f"{temporal['late_night_work_ratio']*100:.0f}% of commits between 11pm-6am",
                'metric_value': temporal['late_night_work_ratio']
            })
        
        # Flag 7: Irregular pattern
        if activity['pattern'] == 'irregular':
            flags.append({
                'type': 'irregular_pattern',
                'severity': 'medium',
                'description': "Highly irregular commit pattern detected",
                'metric_value': activity['consistency_score']
            })
        
        return flags
    
    def _calculate_severity(self, flags: List[Dict]) -> str:
        if not flags:
            return 'none'
        
        severity_scores = {'high': 3, 'medium': 2, 'low': 1}
        total_score = sum(severity_scores[f['severity']] for f in flags)
        
        if total_score >= 5:
            return 'high'
        elif total_score >= 3:
            return 'medium'
        else:
            return 'low'
    
    def _generate_recommendations(self, flags: List[Dict]) -> List[str]:
        recommendations = []
        flag_types = {f['type'] for f in flags}
        
        if 'inactivity' in flag_types or 'low_progress' in flag_types:
            recommendations.append(
                "⚠️ Reach out immediately - student may have dropped or be struggling"
            )
        
        if 'declining_activity' in flag_types:
            recommendations.append(
                "📉 Check in with student - activity declining, may need support or clarification"
            )
        
        if 'procrastination' in flag_types:
            recommendations.append(
                "⏰ Encourage earlier start on work - most progress happening near deadline"
            )
        
        if 'minimal_progress' in flag_types:
            recommendations.append(
                "🔍 Review commit content - many small commits may indicate confusion or lack of direction"
            )
        
        if 'burnout_risk' in flag_types:
            recommendations.append(
                "💤 Discuss time management - excessive late-night work may lead to burnout"
            )
        
        if 'irregular_pattern' in flag_types:
            recommendations.append(
                "📅 Suggest setting regular work schedule to maintain steady progress"
            )
        
        if not recommendations:
            recommendations.append("✅ Student shows healthy work patterns - continue monitoring")
        
        return recommendations
    
    def _create_alert(self, alert_type: str, student_data: Dict, 
                     description: str, severity: str) -> Dict:
        return {
            'student_id': student_data['student_id'],
            'repository': student_data['repository'],
            'analysis_date': datetime.now().isoformat(),
            'total_commits': 0,
            'flags': [{
                'type': alert_type,
                'severity': severity,
                'description': description,
                'metric_value': 0
            }],
            'severity': severity,
            'recommendations': [
                "⚠️ URGENT: Reach out to student immediately - no activity detected"
            ],
            'metrics': {}
        }
    
class TeamAnalyzer:
    
    def analyze_team(self, team_data: Dict, course_info: Dict) -> Dict:
        commits = team_data['commits']
        members = team_data['members']
        
        # Analyze individual contributions
        member_contributions = self._analyze_contributions(commits, members)
        
        # Detect imbalances
        imbalance_flags = self._detect_contribution_imbalance(member_contributions)
        
        # Collaboration patterns
        collaboration = self._analyze_collaboration_patterns(commits, course_info)
        
        return {
            'team_id': team_data['team_id'],
            'repository': team_data['repository'],
            'members': members,
            'total_commits': len(commits),
            'member_contributions': member_contributions,
            'collaboration_metrics': collaboration,
            'flags': imbalance_flags,
            'recommendations': self._generate_team_recommendations(imbalance_flags)
        }
    
    def _analyze_contributions(self, commits: List[Dict], members: List[str]) -> Dict:
        contributions = {}
        
        for member in members:
            member_commits = [c for c in commits if c['author'] == member]
            total_changes = sum(c['changes']['total_changes'] for c in member_commits)
            
            contributions[member] = {
                'commit_count': len(member_commits),
                'commit_percentage': len(member_commits) / len(commits) * 100 if commits else 0,
                'total_changes': total_changes,
                'average_commit_size': total_changes / len(member_commits) if member_commits else 0
            }
        
        return contributions
    
    def _detect_contribution_imbalance(self, contributions: Dict) -> List[Dict]:
        flags = []
        
        commit_percentages = [c['commit_percentage'] for c in contributions.values()]
        
        if not commit_percentages:
            return flags
        
        # Check for severe imbalance
        max_contribution = max(commit_percentages)
        min_contribution = min(commit_percentages)
        
        if max_contribution > 60:
            flags.append({
                'type': 'contribution_imbalance',
                'severity': 'high',
                'description': f"One member contributing {max_contribution:.0f}% of commits"
            })
        
        if min_contribution < 10:
            flags.append({
                'type': 'low_contributor',
                'severity': 'medium',
                'description': f"At least one member contributing only {min_contribution:.0f}% of commits"
            })
        
        return flags
    
    def _analyze_collaboration_patterns(self, commits: List[Dict], course_info: Dict) -> Dict:
        timestamps = [datetime.fromisoformat(c['timestamp'].replace('Z', '')) 
                     for c in commits]
        
        # Group commits by day
        daily_commits = defaultdict(list)
        for commit in commits:
            ts = datetime.fromisoformat(commit['timestamp'].replace('Z', ''))
            day_key = ts.date()
            daily_commits[day_key].append(commit['author'])
        
        # Days with multiple members active
        collaborative_days = sum(1 for authors in daily_commits.values() 
                               if len(set(authors)) > 1)
        
        return {
            'collaborative_days': collaborative_days,
            'total_active_days': len(daily_commits),
            'collaboration_ratio': collaborative_days / len(daily_commits) if daily_commits else 0
        }
    
    def _generate_team_recommendations(self, flags: List[Dict]) -> List[str]:
        recommendations = []
        
        if any(f['type'] == 'contribution_imbalance' for f in flags):
            recommendations.append(
                "⚖️ Address contribution imbalance - consider discussing workload distribution"
            )
        
        if any(f['type'] == 'low_contributor' for f in flags):
            recommendations.append(
                "👥 Check in with low-contributing member - may need support or task clarification"
            )
        
        if not recommendations:
            recommendations.append(
                "✅ Team contributions appear balanced - monitor for changes"
            )
        
        return recommendations


class MonitoringAgent:
    
    def __init__(self, alert_thresholds: Dict = None):
        self.student_analyzer = StudentAnalyzer(alert_thresholds)
        self.team_analyzer = TeamAnalyzer()
    
    def analyze_course(self, dataset: Dict) -> Dict:
        print("🔍 Analyzing student commit patterns...\n")
        
        course_info = dataset['course_info']
        
        # Analyze individual students
        individual_analyses = []
        for student_data in dataset['individual_projects']:
            analysis = self.student_analyzer.analyze_student(student_data, course_info)
            individual_analyses.append(analysis)
        
        # Analyze teams
        team_analyses = []
        for team_data in dataset['team_projects']:
            analysis = self.team_analyzer.analyze_team(team_data, course_info)
            team_analyses.append(analysis)
        
        # Generate summary statistics
        summary = self._generate_summary(individual_analyses, team_analyses)
        
        # Prioritize students needing attention
        priority_list = self._prioritize_interventions(individual_analyses)
        
        return {
            'course_info': course_info,
            'analysis_date': datetime.now().isoformat(),
            'summary': summary,
            'individual_analyses': individual_analyses,
            'team_analyses': team_analyses,
            'priority_interventions': priority_list
        }
    
    def _generate_summary(self, individual: List[Dict], teams: List[Dict]) -> Dict:
        # Count flags by severity
        high_priority = sum(1 for a in individual if a['severity'] == 'high')
        medium_priority = sum(1 for a in individual if a['severity'] == 'medium')
        low_priority = sum(1 for a in individual if a['severity'] == 'low')
        no_concerns = sum(1 for a in individual if a['severity'] == 'none')
        
        # Common flag types
        all_flags = [flag for a in individual for flag in a['flags']]
        flag_counts = defaultdict(int)
        for flag in all_flags:
            flag_counts[flag['type']] += 1
        
        return {
            'total_students': len(individual),
            'total_teams': len(teams),
            'students_needing_attention': high_priority + medium_priority,
            'severity_breakdown': {
                'high': high_priority,
                'medium': medium_priority,
                'low': low_priority,
                'none': no_concerns
            },
            'most_common_flags': dict(sorted(flag_counts.items(), 
                                           key=lambda x: x[1], 
                                           reverse=True)[:5])
        }
    
    def _prioritize_interventions(self, analyses: List[Dict]) -> List[Dict]:
        severity_order = {'high': 3, 'medium': 2, 'low': 1, 'none': 0}
        
        students_with_issues = [a for a in analyses if a['severity'] != 'none']
        
        prioritized = sorted(students_with_issues, 
                           key=lambda x: (severity_order[x['severity']], 
                                        len(x['flags'])),
                           reverse=True)
        
        return [{
            'rank': i + 1,
            'student_id': a['student_id'],
            'repository': a['repository'],
            'severity': a['severity'],
            'flag_count': len(a['flags']),
            'primary_concern': a['flags'][0]['type'] if a['flags'] else 'none',
            'recommendations': a['recommendations']
        } for i, a in enumerate(prioritized[:20])]


def main():
    # Load synthetic data - FIXED PATH
    print("Loading synthetic dataset...")
    
    # Try multiple possible paths
    possible_paths = [
        'synthetic_student_commits.json',
        '../data/synthetic_student_commits.json',
        '../data/processed/synthetic_student_commits.json',
        'data/synthetic_student_commits.json'
    ]
    
    dataset = None
    for path in possible_paths:
        try:
            with open(path, 'r') as f:
                dataset = json.load(f)
            print(f"✓ Loaded data from: {path}\n")
            break
        except FileNotFoundError:
            continue
    
    if dataset is None:
        print("❌ Error: Could not find synthetic_student_commits.json")
        print("   Please run generate_synthetic_data.py first")
        print("   Or make sure you're in the correct directory")
        return
    
    # Initialize monitoring agent
    agent = MonitoringAgent()
    
    # Run analysis
    results = agent.analyze_course(dataset)
    
    # Save full results
    with open('analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "="*70)
    print("COURSE MONITORING SUMMARY")
    print("="*70)
    
    summary = results['summary']
    print(f"\n📊 Overall Statistics:")
    print(f"   Total Students: {summary['total_students']}")
    print(f"   Students Needing Attention: {summary['students_needing_attention']}")
    
    print(f"\n🚨 Severity Breakdown:")
    for severity, count in summary['severity_breakdown'].items():
        print(f"   {severity.upper()}: {count} students")
    
    print(f"\n🔍 Most Common Issues:")
    for flag_type, count in list(summary['most_common_flags'].items())[:5]:
        print(f"   {flag_type}: {count} students")
    
    print(f"\n⚠️  Priority Interventions (Top 10):")
    for student in results['priority_interventions'][:10]:
        print(f"\n   {student['rank']}. {student['student_id']} [{student['severity'].upper()}]")
        print(f"      Primary concern: {student['primary_concern']}")
        print(f"      → {student['recommendations'][0]}")
    
    print(f"\n✓ Full analysis saved to: analysis_results.json")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()