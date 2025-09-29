"""
Performance Analytics System for Assessment Results
Provides comprehensive analysis, scoring, and improvement recommendations.
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict, Counter
import statistics

@dataclass
class UserPerformanceProfile:
    """Comprehensive user performance profile"""
    user_id: str
    total_tests: int
    average_score: float
    best_score: float
    worst_score: float
    improvement_trend: float
    strong_categories: List[str]
    weak_categories: List[str]
    time_efficiency: float
    consistency_score: float
    recent_performance: List[Dict[str, Any]]
    skill_levels: Dict[str, str]
    recommendations: List[str]

@dataclass
class CompanyBenchmark:
    """Benchmark data for company-specific assessments"""
    company_name: str
    average_score: float
    passing_threshold: float
    top_percentile_score: float
    common_weak_areas: List[str]
    success_factors: List[str]
    difficulty_distribution: Dict[str, float]

class PerformanceAnalytics:
    """
    Advanced analytics system for assessment performance tracking,
    skill analysis, and personalized improvement recommendations.
    """
    
    def __init__(self):
        self.results_dir = Path("Data/Assessments/Results")
        self.analytics_dir = Path("Data/Assessments/Analytics")
        self.analytics_dir.mkdir(exist_ok=True)
        
        # Performance thresholds
        self.score_thresholds = {
            "excellent": 90,
            "good": 75,
            "average": 60,
            "below_average": 45,
            "poor": 30
        }
        
        # Skill level mapping
        self.skill_levels = {
            "beginner": (0, 40),
            "intermediate": (40, 70), 
            "advanced": (70, 85),
            "expert": (85, 100)
        }
    
    def analyze_user_performance(self, user_id: str, 
                               time_period_days: int = 30) -> UserPerformanceProfile:
        """Generate comprehensive performance analysis for a user"""
        user_results = self._load_user_results(user_id, time_period_days)
        
        if not user_results:
            return self._create_empty_profile(user_id)
        
        # Basic statistics
        scores = [result['overall_percentage'] for result in user_results]
        total_tests = len(user_results)
        average_score = statistics.mean(scores)
        best_score = max(scores)
        worst_score = min(scores)
        
        # Improvement trend analysis
        improvement_trend = self._calculate_improvement_trend(user_results)
        
        # Category analysis
        strong_categories, weak_categories = self._analyze_category_performance(user_results)
        
        # Time efficiency analysis
        time_efficiency = self._calculate_time_efficiency(user_results)
        
        # Consistency analysis
        consistency_score = self._calculate_consistency(scores)
        
        # Recent performance (last 5 tests)
        recent_performance = user_results[-5:] if len(user_results) >= 5 else user_results
        
        # Skill level assessment
        skill_levels = self._assess_skill_levels(user_results)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            user_results, weak_categories, time_efficiency, consistency_score
        )
        
        return UserPerformanceProfile(
            user_id=user_id,
            total_tests=total_tests,
            average_score=round(average_score, 2),
            best_score=round(best_score, 2),
            worst_score=round(worst_score, 2),
            improvement_trend=round(improvement_trend, 2),
            strong_categories=strong_categories,
            weak_categories=weak_categories,
            time_efficiency=round(time_efficiency, 2),
            consistency_score=round(consistency_score, 2),
            recent_performance=recent_performance,
            skill_levels=skill_levels,
            recommendations=recommendations
        )
    
    def analyze_test_result(self, session_id: str) -> Dict[str, Any]:
        """Provide detailed analysis of a specific test result"""
        result_file = self.results_dir / f"{session_id}_results.json"
        
        if not result_file.exists():
            return {"error": "Test result not found"}
        
        with open(result_file, 'r') as f:
            data = json.load(f)
        
        results = data['results']
        session = data['session']
        
        # Detailed analysis
        analysis = {
            "test_summary": {
                "overall_score": results['overall_percentage'],
                "completion_rate": results['completion_rate'],
                "time_utilization": (results['time_taken'] / results['time_limit']) * 100,
                "efficiency_rating": self._rate_efficiency(results)
            },
            "category_analysis": self._analyze_category_performance_detailed(results),
            "time_analysis": self._analyze_time_usage(session, results),
            "difficulty_analysis": self._analyze_difficulty_performance(session, results),
            "strengths_and_weaknesses": self._identify_strengths_weaknesses(results),
            "improvement_areas": self._identify_improvement_areas(results),
            "next_steps": self._suggest_next_steps(results),
            "benchmark_comparison": self._compare_with_benchmarks(results)
        }
        
        return analysis
    
    def generate_company_benchmark(self, company_name: str) -> CompanyBenchmark:
        """Generate benchmark data for a specific company"""
        company_results = self._load_company_results(company_name)
        
        if not company_results:
            return self._create_default_benchmark(company_name)
        
        scores = [result['overall_percentage'] for result in company_results]
        
        return CompanyBenchmark(
            company_name=company_name,
            average_score=round(statistics.mean(scores), 2),
            passing_threshold=self._calculate_passing_threshold(scores),
            top_percentile_score=round(np.percentile(scores, 90), 2),
            common_weak_areas=self._identify_common_weak_areas(company_results),
            success_factors=self._identify_success_factors(company_results),
            difficulty_distribution=self._analyze_difficulty_distribution(company_results)
        )
    
    def create_performance_report(self, user_id: str, 
                                format_type: str = "detailed") -> Dict[str, Any]:
        """Create comprehensive performance report"""
        profile = self.analyze_user_performance(user_id)
        
        if format_type == "summary":
            return self._create_summary_report(profile)
        elif format_type == "detailed":
            return self._create_detailed_report(profile)
        elif format_type == "comparison":
            return self._create_comparison_report(profile)
        else:
            return self._create_detailed_report(profile)
    
    def track_improvement_over_time(self, user_id: str, 
                                  time_period_days: int = 90) -> Dict[str, Any]:
        """Track user improvement over specified time period"""
        user_results = self._load_user_results(user_id, time_period_days)
        
        if len(user_results) < 2:
            return {"error": "Insufficient data for trend analysis"}
        
        # Create time series data
        dates = [datetime.fromisoformat(result['completed_at']) for result in user_results]
        scores = [result['overall_percentage'] for result in user_results]
        
        # Calculate trends
        weekly_averages = self._calculate_weekly_averages(dates, scores)
        monthly_progress = self._calculate_monthly_progress(dates, scores)
        skill_progression = self._track_skill_progression(user_results)
        
        return {
            "time_period": time_period_days,
            "total_tests": len(user_results),
            "score_trend": {
                "start_score": scores[0],
                "end_score": scores[-1],
                "improvement": scores[-1] - scores[0],
                "trend_line": self._calculate_trend_line(scores)
            },
            "weekly_averages": weekly_averages,
            "monthly_progress": monthly_progress,
            "skill_progression": skill_progression,
            "consistency_over_time": self._analyze_consistency_over_time(scores),
            "peak_performance": {
                "best_score": max(scores),
                "best_date": dates[scores.index(max(scores))].isoformat(),
                "recent_peak": self._find_recent_peak(dates, scores)
            }
        }
    
    def generate_study_plan(self, user_id: str) -> Dict[str, Any]:
        """Generate personalized study plan based on performance analysis"""
        profile = self.analyze_user_performance(user_id)
        
        # Prioritize weak areas
        priority_areas = self._prioritize_improvement_areas(profile)
        
        # Generate study schedule
        study_schedule = self._create_study_schedule(priority_areas, profile)
        
        # Recommend resources
        resources = self._recommend_study_resources(priority_areas)
        
        # Set practice goals
        practice_goals = self._set_practice_goals(profile)
        
        return {
            "user_id": user_id,
            "generated_at": datetime.now().isoformat(),
            "current_level": self._determine_overall_level(profile),
            "priority_areas": priority_areas,
            "study_schedule": study_schedule,
            "recommended_resources": resources,
            "practice_goals": practice_goals,
            "timeline": self._create_improvement_timeline(profile),
            "success_metrics": self._define_success_metrics(profile)
        }
    
    # Helper methods
    
    def _load_user_results(self, user_id: str, time_period_days: int) -> List[Dict[str, Any]]:
        """Load user results within specified time period"""
        cutoff_date = datetime.now() - timedelta(days=time_period_days)
        user_results = []
        
        for result_file in self.results_dir.glob("*_results.json"):
            try:
                with open(result_file, 'r') as f:
                    data = json.load(f)
                
                if (data['results']['user_id'] == user_id and 
                    datetime.fromisoformat(data['results']['completed_at']) > cutoff_date):
                    user_results.append(data['results'])
            except Exception as e:
                continue
        
        # Sort by completion date
        user_results.sort(key=lambda x: x['completed_at'])
        return user_results
    
    def _calculate_improvement_trend(self, results: List[Dict[str, Any]]) -> float:
        """Calculate improvement trend over time"""
        if len(results) < 2:
            return 0.0
        
        scores = [result['overall_percentage'] for result in results]
        
        # Use linear regression to find trend
        x = list(range(len(scores)))
        slope = np.polyfit(x, scores, 1)[0]
        
        return slope
    
    def _analyze_category_performance(self, results: List[Dict[str, Any]]) -> Tuple[List[str], List[str]]:
        """Analyze performance by category to identify strengths and weaknesses"""
        category_scores = defaultdict(list)
        
        for result in results:
            for category, data in result.get('category_breakdown', {}).items():
                category_scores[category].append(data['percentage'])
        
        category_averages = {
            category: statistics.mean(scores) 
            for category, scores in category_scores.items()
        }
        
        # Sort categories by performance
        sorted_categories = sorted(category_averages.items(), key=lambda x: x[1], reverse=True)
        
        # Top 3 and bottom 3 categories
        strong_categories = [cat for cat, _ in sorted_categories[:3]]
        weak_categories = [cat for cat, _ in sorted_categories[-3:]]
        
        return strong_categories, weak_categories
    
    def _calculate_time_efficiency(self, results: List[Dict[str, Any]]) -> float:
        """Calculate average time efficiency"""
        if not results:
            return 0.0
        
        efficiencies = []
        for result in results:
            time_used = result['time_taken']
            time_limit = result['time_limit']
            score = result['overall_percentage']
            
            # Efficiency = Score per minute used
            efficiency = score / (time_used / 60) if time_used > 0 else 0
            efficiencies.append(efficiency)
        
        return statistics.mean(efficiencies)
    
    def _calculate_consistency(self, scores: List[float]) -> float:
        """Calculate consistency score (inverse of coefficient of variation)"""
        if len(scores) < 2:
            return 100.0
        
        mean_score = statistics.mean(scores)
        std_dev = statistics.stdev(scores)
        
        if mean_score == 0:
            return 0.0
        
        cv = std_dev / mean_score
        consistency = max(0, 100 - (cv * 100))
        
        return consistency
    
    def _assess_skill_levels(self, results: List[Dict[str, Any]]) -> Dict[str, str]:
        """Assess skill levels by category"""
        category_scores = defaultdict(list)
        
        for result in results:
            for category, data in result.get('category_breakdown', {}).items():
                category_scores[category].append(data['percentage'])
        
        skill_levels = {}
        for category, scores in category_scores.items():
            avg_score = statistics.mean(scores)
            
            for level, (min_score, max_score) in self.skill_levels.items():
                if min_score <= avg_score < max_score:
                    skill_levels[category] = level
                    break
            else:
                skill_levels[category] = "expert"
        
        return skill_levels
    
    def _generate_recommendations(self, results: List[Dict[str, Any]], 
                                weak_categories: List[str],
                                time_efficiency: float,
                                consistency_score: float) -> List[str]:
        """Generate personalized improvement recommendations"""
        recommendations = []
        
        if len(results) == 0:
            return ["Take your first assessment to get personalized recommendations!"]
        
        latest_result = results[-1]
        avg_score = statistics.mean([r['overall_percentage'] for r in results])
        
        # Score-based recommendations
        if avg_score < 40:
            recommendations.append("Focus on fundamental concepts and basic problem-solving techniques")
        elif avg_score < 60:
            recommendations.append("Practice medium-difficulty problems to build confidence")
        elif avg_score < 80:
            recommendations.append("Challenge yourself with advanced problems and time optimization")
        else:
            recommendations.append("Maintain excellence by solving complex, real-world problems")
        
        # Category-specific recommendations
        for category in weak_categories:
            if category == "DSA":
                recommendations.append("Practice data structures and algorithms daily using LeetCode or HackerRank")
            elif category == "DATABASES":
                recommendations.append("Study SQL queries, database design, and ACID properties")
            elif category == "SYSTEM_DESIGN":
                recommendations.append("Learn about scalability, load balancing, and distributed systems")
            elif category == "MATHEMATICS":
                recommendations.append("Review mathematical concepts and practice quantitative problems")
        
        # Time efficiency recommendations
        if time_efficiency < 0.5:
            recommendations.append("Work on solving problems more quickly - practice timed exercises")
        elif time_efficiency > 2.0:
            recommendations.append("Take more time to ensure accuracy - focus on quality over speed")
        
        # Consistency recommendations
        if consistency_score < 60:
            recommendations.append("Focus on consistent preparation and regular practice to reduce performance variance")
        
        return recommendations[:8]  # Limit to top 8 recommendations
    
    def _create_empty_profile(self, user_id: str) -> UserPerformanceProfile:
        """Create empty profile for users with no test history"""
        return UserPerformanceProfile(
            user_id=user_id,
            total_tests=0,
            average_score=0.0,
            best_score=0.0,
            worst_score=0.0,
            improvement_trend=0.0,
            strong_categories=[],
            weak_categories=[],
            time_efficiency=0.0,
            consistency_score=0.0,
            recent_performance=[],
            skill_levels={},
            recommendations=["Take your first assessment to start tracking your progress!"]
        )
    
    def _create_summary_report(self, profile: UserPerformanceProfile) -> Dict[str, Any]:
        """Create summary performance report"""
        return {
            "report_type": "summary",
            "generated_at": datetime.now().isoformat(),
            "user_id": profile.user_id,
            "overall_grade": self._calculate_performance_grade(profile),
            "total_tests": profile.total_tests,
            "average_score": profile.average_score,
            "improvement_trend": profile.improvement_trend,
            "skill_level": self._determine_overall_level(profile),
            "top_recommendations": profile.recommendations[:3] if profile.recommendations else [],
            "strong_areas": profile.strong_categories[:3] if profile.strong_categories else [],
            "areas_for_improvement": profile.weak_categories[:3] if profile.weak_categories else []
        }
    
    def _create_detailed_report(self, profile: UserPerformanceProfile) -> Dict[str, Any]:
        """Create detailed performance report"""
        return {
            "report_type": "detailed",
            "generated_at": datetime.now().isoformat(),
            "user_profile": asdict(profile),
            "performance_grade": self._calculate_performance_grade(profile),
            "improvement_analysis": {
                "trend_direction": "improving" if profile.improvement_trend > 0 else "declining" if profile.improvement_trend < 0 else "stable",
                "trend_strength": abs(profile.improvement_trend),
                "consistency_rating": self._rate_consistency(profile.consistency_score)
            },
            "skill_assessment": {
                "overall_level": self._determine_overall_level(profile),
                "category_levels": profile.skill_levels,
                "growth_potential": self._assess_growth_potential(profile)
            },
            "action_plan": {
                "immediate_actions": profile.recommendations[:3],
                "medium_term_goals": profile.recommendations[3:6],
                "long_term_objectives": profile.recommendations[6:]
            }
        }
    
    def _calculate_performance_grade(self, profile: UserPerformanceProfile) -> str:
        """Calculate overall performance grade"""
        if profile.total_tests == 0:
            return "N/A"
        
        score = profile.average_score
        
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C+"
        elif score >= 55:
            return "C"
        elif score >= 50:
            return "C-"
        else:
            return "D"
    
    def _determine_overall_level(self, profile: UserPerformanceProfile) -> str:
        """Determine overall skill level"""
        if profile.total_tests == 0:
            return "beginner"
        
        score = profile.average_score
        
        for level, (min_score, max_score) in self.skill_levels.items():
            if min_score <= score < max_score:
                return level
        
        return "expert"
    
    def _rate_consistency(self, consistency_score: float) -> str:
        """Rate consistency based on score"""
        if consistency_score >= 80:
            return "excellent"
        elif consistency_score >= 60:
            return "good"
        elif consistency_score >= 40:
            return "fair"
        else:
            return "needs_improvement"
    
    def _assess_growth_potential(self, profile: UserPerformanceProfile) -> str:
        """Assess user's growth potential"""
        if profile.improvement_trend > 2:
            return "high"
        elif profile.improvement_trend > 0:
            return "moderate"
        elif profile.improvement_trend > -1:
            return "stable"
        else:
            return "declining"
    
    def _rate_efficiency(self, results: Dict[str, Any]) -> str:
        """Rate time efficiency based on results"""
        time_used = results.get('time_taken', 0)
        time_limit = results.get('time_limit', 1)
        score = results.get('overall_percentage', 0)
        
        time_utilization = (time_used / time_limit) * 100 if time_limit > 0 else 100
        
        # Efficiency rating based on score vs time used
        if score >= 80 and time_utilization <= 70:
            return "excellent"
        elif score >= 70 and time_utilization <= 80:
            return "good"
        elif score >= 60 and time_utilization <= 90:
            return "fair"
        else:
            return "needs_improvement"
    
    def _load_company_results(self, company_name: str) -> List[Dict[str, Any]]:
        """Load results for specific company assessments"""
        company_results = []
        
        for result_file in self.results_dir.glob("*_results.json"):
            try:
                with open(result_file, 'r') as f:
                    data = json.load(f)
                
                # Check if result is for the specified company
                test_config = data.get('results', {}).get('test_config', {})
                if test_config.get('company', '').lower() == company_name.lower():
                    company_results.append(data['results'])
            except Exception as e:
                continue
        
        return company_results
    
    def _create_default_benchmark(self, company_name: str) -> CompanyBenchmark:
        """Create default benchmark when no data available"""
        return CompanyBenchmark(
            company_name=company_name,
            average_score=65.0,
            passing_threshold=60.0,
            top_percentile_score=85.0,
            common_weak_areas=["algorithms", "system_design"],
            success_factors=["consistent_practice", "problem_solving"],
            difficulty_distribution={"easy": 30.0, "medium": 50.0, "hard": 20.0}
        )
    
    def _prioritize_improvement_areas(self, profile: UserPerformanceProfile) -> List[Dict[str, Any]]:
        """Prioritize improvement areas based on performance analysis"""
        priority_areas = []
        
        # Prioritize weak categories with highest impact
        for category in profile.weak_categories:
            priority_areas.append({
                "category": category,
                "priority": "high",
                "reason": f"Low performance in {category}",
                "improvement_potential": "significant"
            })
        
        # Add consistency improvement if needed
        if profile.consistency_score < 60:
            priority_areas.append({
                "category": "consistency",
                "priority": "medium",
                "reason": "Performance varies significantly between tests",
                "improvement_potential": "moderate"
            })
        
        return priority_areas[:5]  # Top 5 priority areas
    
    def _create_study_schedule(self, priority_areas: List[Dict[str, Any]], 
                              profile: UserPerformanceProfile) -> Dict[str, Any]:
        """Create personalized study schedule"""
        return {
            "daily_practice": "2-3 hours recommended",
            "weekly_focus": priority_areas[0]["category"] if priority_areas else "general_review",
            "practice_tests": "Take 1 assessment per week",
            "review_schedule": "Review weak areas every 2 days"
        }
    
    def _recommend_study_resources(self, priority_areas: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Recommend study resources for priority areas"""
        resource_map = {
            "algorithms": ["LeetCode", "HackerRank", "Cracking the Coding Interview"],
            "data_structures": ["GeeksforGeeks", "Algorithm Design Manual", "Data Structures Course"],
            "system_design": ["System Design Interview", "High Scalability", "AWS Architecture Center"],
            "databases": ["SQL Tutorial", "Database Systems Course", "MongoDB University"],
            "consistency": ["Daily Practice Schedule", "Mock Interview Platform", "Coding Challenges"]
        }
        
        recommendations = {}
        for area in priority_areas:
            category = area["category"]
            recommendations[category] = resource_map.get(category, ["General Programming Resources"])
        
        return recommendations
    
    def _set_practice_goals(self, profile: UserPerformanceProfile) -> Dict[str, Any]:
        """Set practice goals based on current performance"""
        current_level = self._determine_overall_level(profile)
        
        goals = {
            "beginner": {
                "weekly_problems": 10,
                "target_score": 50,
                "focus": "basic_concepts"
            },
            "intermediate": {
                "weekly_problems": 15,
                "target_score": 70,
                "focus": "medium_problems"
            },
            "advanced": {
                "weekly_problems": 20,
                "target_score": 85,
                "focus": "optimization"
            },
            "expert": {
                "weekly_problems": 25,
                "target_score": 95,
                "focus": "complex_problems"
            }
        }
        
        return goals.get(current_level, goals["intermediate"])
    
    def _create_improvement_timeline(self, profile: UserPerformanceProfile) -> Dict[str, str]:
        """Create improvement timeline"""
        return {
            "week_1_2": "Focus on identified weak areas",
            "week_3_4": "Practice mixed difficulty problems",
            "week_5_6": "Take practice assessments",
            "week_7_8": "Review and optimize performance"
        }
    
    def _define_success_metrics(self, profile: UserPerformanceProfile) -> Dict[str, float]:
        """Define success metrics for improvement"""
        current_score = profile.average_score
        target_improvement = min(20, 90 - current_score)  # Max 20 point improvement or up to 90
        
        return {
            "target_score": current_score + target_improvement,
            "consistency_target": min(profile.consistency_score + 15, 95),
            "completion_rate_target": 95.0,
            "time_efficiency_target": max(profile.time_efficiency * 1.2, 2.0)
        }
    
    def save_analytics_report(self, user_id: str, report: Dict[str, Any]):
        """Save analytics report to file"""
        try:
            report_file = self.analytics_dir / f"{user_id}_analytics.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving analytics report: {e}")

# Global instance for use across the application
performance_analytics = PerformanceAnalytics()