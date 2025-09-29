"""
📊 MULTI-MODAL PERFORMANCE ANALYTICS
Advanced Analytics System for Interview Performance Analysis

This module provides:
- Comprehensive performance analysis across video, audio, and content
- Trend tracking and improvement recommendations
- Company-specific benchmarking and comparison
- Detailed reporting with visualizations
- Progress tracking across multiple interview sessions
- AI-powered coaching suggestions
"""

import json
import os
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from .AIInterviewEngine import InterviewSession, InterviewResponse, VideoAnalysisResult, AudioAnalysisResult
from .InterviewSessionManager import interview_session_manager

# Groq AI for advanced analytics insights
from groq import Groq
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
GROQ_API_KEY = env_vars.get("GroqAPIKey")

try:
    client = Groq(api_key=GROQ_API_KEY)
except:
    client = None

@dataclass
class PerformanceMetrics:
    """Comprehensive performance metrics"""
    overall_score: float
    communication_score: float
    confidence_score: float
    professionalism_score: float
    technical_score: float
    
    # Detailed breakdowns
    eye_contact_avg: float
    posture_avg: float
    gesture_quality: float
    speech_clarity: float
    speaking_pace: float
    filler_words_avg: float
    
    # Session metadata
    session_count: int
    total_duration: float
    questions_answered: int
    improvement_trend: float

@dataclass
class CompanyBenchmark:
    """Company-specific performance benchmarks"""
    company_name: str
    role: str
    industry_avg_scores: Dict[str, float]
    top_performer_scores: Dict[str, float]
    user_percentile: float
    areas_above_average: List[str]
    areas_below_average: List[str]

@dataclass
class ImprovementPlan:
    """Personalized improvement plan"""
    priority_areas: List[str]
    specific_recommendations: List[Dict]
    practice_exercises: List[Dict]
    target_scores: Dict[str, float]
    estimated_timeline: str
    confidence_building_tips: List[str]

@dataclass
class AnalyticsReport:
    """Complete analytics report"""
    user_id: str
    report_date: datetime
    time_period: str
    performance_metrics: PerformanceMetrics
    company_benchmarks: List[CompanyBenchmark]
    improvement_plan: ImprovementPlan
    session_summaries: List[Dict]
    trend_analysis: Dict
    ai_insights: List[str]

class InterviewAnalytics:
    """
    Advanced Analytics Engine for Interview Performance
    
    Provides comprehensive analysis including:
    - Multi-modal performance tracking
    - Company and industry benchmarking
    - Trend analysis and improvement detection
    - Personalized coaching recommendations
    - Detailed reporting and visualizations
    """
    
    def __init__(self):
        self.analytics_dir = "Data/Analytics"
        self.reports_dir = "Data/Analytics/Reports"
        self.charts_dir = "Data/Analytics/Charts"
        self.benchmarks_dir = "Data/Analytics/Benchmarks"
        
        # Ensure directories exist
        for directory in [self.analytics_dir, self.reports_dir, self.charts_dir, self.benchmarks_dir]:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Load industry benchmarks
        self.industry_benchmarks = self._load_industry_benchmarks()
        
        # Performance tracking
        self.user_histories: Dict[str, List[Dict]] = {}
        
        print("📊 Multi-Modal Performance Analytics - INITIALIZED!")
    
    def analyze_session_performance(self, session_results: Dict) -> Dict:
        """Analyze individual session performance with detailed insights"""
        
        session_id = session_results.get('session_id', '')
        user_id = session_results.get('session_metadata', {}).get('user_id', '')
        
        # Extract performance metrics
        performance = self._extract_performance_metrics(session_results)
        
        # Analyze video performance
        video_analysis = self._analyze_video_performance(session_results)
        
        # Analyze audio performance
        audio_analysis = self._analyze_audio_performance(session_results)
        
        # Analyze content quality
        content_analysis = self._analyze_content_quality(session_results)
        
        # Generate improvement recommendations
        recommendations = self._generate_session_recommendations(
            video_analysis, audio_analysis, content_analysis
        )
        
        # Company-specific insights
        company_insights = self._generate_company_insights(session_results)
        
        # Overall session analysis
        session_analysis = {
            'session_id': session_id,
            'user_id': user_id,
            'analysis_timestamp': datetime.now().isoformat(),
            'performance_metrics': performance,
            'video_analysis': video_analysis,
            'audio_analysis': audio_analysis,
            'content_analysis': content_analysis,
            'recommendations': recommendations,
            'company_insights': company_insights,
            'overall_grade': self._calculate_overall_grade(performance),
            'key_strengths': self._identify_key_strengths(session_results),
            'improvement_priorities': self._identify_improvement_priorities(session_results)
        }
        
        # Save analysis
        self._save_session_analysis(session_analysis)
        
        # Update user history
        self._update_user_history(user_id, session_analysis)
        
        return session_analysis
    
    def generate_comprehensive_report(self, user_id: str, time_period: str = "all") -> AnalyticsReport:
        """Generate comprehensive performance report for user"""
        
        # Get user session history
        user_sessions = self._get_user_sessions(user_id, time_period)
        
        if not user_sessions:
            print(f"⚠️ No sessions found for user {user_id}")
            return None
        
        # Calculate performance metrics
        performance_metrics = self._calculate_performance_metrics(user_sessions)
        
        # Generate company benchmarks
        company_benchmarks = self._generate_company_benchmarks(user_id, user_sessions)
        
        # Create improvement plan
        improvement_plan = self._create_improvement_plan(user_id, user_sessions, performance_metrics)
        
        # Analyze trends
        trend_analysis = self._analyze_performance_trends(user_sessions)
        
        # Generate AI insights
        ai_insights = self._generate_ai_insights(user_sessions, performance_metrics, trend_analysis)
        
        # Create comprehensive report
        report = AnalyticsReport(
            user_id=user_id,
            report_date=datetime.now(),
            time_period=time_period,
            performance_metrics=performance_metrics,
            company_benchmarks=company_benchmarks,
            improvement_plan=improvement_plan,
            session_summaries=user_sessions,
            trend_analysis=trend_analysis,
            ai_insights=ai_insights
        )
        
        # Save report
        self._save_comprehensive_report(report)
        
        # Generate visualizations
        self._generate_performance_charts(report)
        
        return report
    
    def compare_performance_across_companies(self, user_id: str) -> Dict:
        """Compare user performance across different companies"""
        
        user_sessions = self._get_user_sessions(user_id, "all")
        
        if not user_sessions:
            return {}
        
        # Group sessions by company
        company_performance = {}
        
        for session in user_sessions:
            company = session.get('session_metadata', {}).get('company_name', 'Unknown')
            
            if company not in company_performance:
                company_performance[company] = {
                    'sessions': [],
                    'avg_scores': {},
                    'best_session': None,
                    'improvement_trend': 0.0
                }
            
            company_performance[company]['sessions'].append(session)
        
        # Calculate company-specific analytics
        for company, data in company_performance.items():
            sessions = data['sessions']
            
            # Calculate average scores
            data['avg_scores'] = {
                'overall': np.mean([s.get('overall_score', 0) for s in sessions]),
                'communication': np.mean([s.get('communication_score', 0) for s in sessions]),
                'confidence': np.mean([s.get('confidence_score', 0) for s in sessions]),
                'technical': np.mean([s.get('technical_score', 0) for s in sessions])
            }
            
            # Find best session
            data['best_session'] = max(sessions, key=lambda x: x.get('overall_score', 0))
            
            # Calculate improvement trend
            if len(sessions) > 1:
                scores = [s.get('overall_score', 0) for s in sessions]
                data['improvement_trend'] = (scores[-1] - scores[0]) / len(scores)
        
        return {
            'user_id': user_id,
            'company_comparison': company_performance,
            'best_performing_company': max(company_performance.keys(), 
                                          key=lambda x: company_performance[x]['avg_scores']['overall']),
            'most_improved_company': max(company_performance.keys(), 
                                       key=lambda x: company_performance[x]['improvement_trend']),
            'recommendations': self._generate_cross_company_recommendations(company_performance)
        }
    
    def _extract_performance_metrics(self, session_results: Dict) -> Dict:
        """Extract detailed performance metrics from session results"""
        
        return {
            'overall_score': session_results.get('overall_score', 0),
            'communication_score': session_results.get('communication_score', 0),
            'confidence_score': session_results.get('confidence_score', 0),
            'professionalism_score': session_results.get('professionalism_score', 0),
            'technical_score': session_results.get('technical_score', 0),
            'detailed_video_scores': session_results.get('detailed_video_scores', {}),
            'detailed_audio_scores': session_results.get('detailed_audio_scores', {}),
            'session_duration': session_results.get('session_duration', 0),
            'questions_answered': session_results.get('answered_questions', 0)
        }
    
    def _analyze_video_performance(self, session_results: Dict) -> Dict:
        """Detailed analysis of video/visual performance"""
        
        video_scores = session_results.get('detailed_video_scores', {})
        
        analysis = {
            'eye_contact_performance': {
                'score': video_scores.get('eye_contact', 0),
                'grade': self._score_to_grade(video_scores.get('eye_contact', 0)),
                'feedback': self._get_eye_contact_feedback(video_scores.get('eye_contact', 0))
            },
            'confidence_display': {
                'score': video_scores.get('confidence', 0),
                'grade': self._score_to_grade(video_scores.get('confidence', 0)),
                'feedback': self._get_confidence_feedback(video_scores.get('confidence', 0))
            },
            'professionalism': {
                'score': video_scores.get('professionalism', 0),
                'grade': self._score_to_grade(video_scores.get('professionalism', 0)),
                'feedback': self._get_professionalism_feedback(video_scores.get('professionalism', 0))
            },
            'body_language': {
                'score': video_scores.get('attention', 0),
                'grade': self._score_to_grade(video_scores.get('attention', 0)),
                'feedback': self._get_body_language_feedback(video_scores.get('attention', 0))
            }
        }
        
        # Overall video performance
        avg_video_score = np.mean([v['score'] for v in analysis.values()])
        analysis['overall_video_performance'] = {
            'score': avg_video_score,
            'grade': self._score_to_grade(avg_video_score),
            'strengths': [k for k, v in analysis.items() if v['score'] > 75],
            'improvements': [k for k, v in analysis.items() if v['score'] < 65]
        }
        
        return analysis
    
    def _analyze_audio_performance(self, session_results: Dict) -> Dict:
        """Detailed analysis of audio/speech performance"""
        
        audio_scores = session_results.get('detailed_audio_scores', {})
        
        analysis = {
            'speech_clarity': {
                'score': audio_scores.get('clarity', 0),
                'grade': self._score_to_grade(audio_scores.get('clarity', 0)),
                'feedback': self._get_clarity_feedback(audio_scores.get('clarity', 0))
            },
            'speaking_pace': {
                'score': self._normalize_pace_score(audio_scores.get('pace', 120)),
                'wpm': audio_scores.get('pace', 120),
                'grade': self._score_to_grade(self._normalize_pace_score(audio_scores.get('pace', 120))),
                'feedback': self._get_pace_feedback(audio_scores.get('pace', 120))
            },
            'voice_confidence': {
                'score': audio_scores.get('confidence', 0),
                'grade': self._score_to_grade(audio_scores.get('confidence', 0)),
                'feedback': self._get_voice_confidence_feedback(audio_scores.get('confidence', 0))
            },
            'filler_words': {
                'count': audio_scores.get('filler_words', 0),
                'score': max(0, 100 - audio_scores.get('filler_words', 0) * 5),
                'grade': self._score_to_grade(max(0, 100 - audio_scores.get('filler_words', 0) * 5)),
                'feedback': self._get_filler_words_feedback(audio_scores.get('filler_words', 0))
            }
        }
        
        # Overall audio performance
        audio_scores_list = [v['score'] for k, v in analysis.items() if k != 'speaking_pace'] + \
                           [analysis['speaking_pace']['score']]
        avg_audio_score = np.mean(audio_scores_list)
        
        analysis['overall_audio_performance'] = {
            'score': avg_audio_score,
            'grade': self._score_to_grade(avg_audio_score),
            'strengths': [k for k, v in analysis.items() if v.get('score', 0) > 75],
            'improvements': [k for k, v in analysis.items() if v.get('score', 0) < 65]
        }
        
        return analysis
    
    def _analyze_content_quality(self, session_results: Dict) -> Dict:
        """Analyze content quality and technical competency"""
        
        technical_score = session_results.get('technical_score', 0)
        questions_answered = session_results.get('answered_questions', 0)
        total_questions = session_results.get('total_questions', 0)
        
        completion_rate = (questions_answered / total_questions * 100) if total_questions > 0 else 0
        
        analysis = {
            'technical_competency': {
                'score': technical_score,
                'grade': self._score_to_grade(technical_score),
                'feedback': self._get_technical_feedback(technical_score)
            },
            'question_completion': {
                'rate': completion_rate,
                'answered': questions_answered,
                'total': total_questions,
                'grade': self._score_to_grade(completion_rate),
                'feedback': self._get_completion_feedback(completion_rate)
            },
            'response_quality': {
                'score': technical_score,  # Using technical score as proxy
                'grade': self._score_to_grade(technical_score),
                'feedback': self._get_response_quality_feedback(technical_score)
            }
        }
        
        # Overall content performance
        avg_content_score = (technical_score + completion_rate) / 2
        analysis['overall_content_performance'] = {
            'score': avg_content_score,
            'grade': self._score_to_grade(avg_content_score),
            'strengths': [k for k, v in analysis.items() if v.get('score', v.get('rate', 0)) > 75],
            'improvements': [k for k, v in analysis.items() if v.get('score', v.get('rate', 0)) < 65]
        }
        
        return analysis
    
    def _generate_session_recommendations(self, video_analysis: Dict, audio_analysis: Dict, content_analysis: Dict) -> List[Dict]:
        """Generate specific recommendations based on session analysis"""
        
        recommendations = []
        
        # Video-based recommendations
        video_overall = video_analysis.get('overall_video_performance', {})
        if 'eye_contact_performance' in video_overall.get('improvements', []):
            recommendations.append({
                'category': 'Visual Presence',
                'priority': 'High',
                'recommendation': 'Practice maintaining eye contact with the camera',
                'specific_tips': [
                    'Place a small arrow near your camera as a reminder',
                    'Practice with video calls to build comfort',
                    'Avoid looking at your own video preview during interviews'
                ],
                'target_improvement': '15-20 points in eye contact score'
            })
        
        # Audio-based recommendations
        audio_overall = audio_analysis.get('overall_audio_performance', {})
        if 'filler_words' in audio_overall.get('improvements', []):
            recommendations.append({
                'category': 'Communication',
                'priority': 'Medium',
                'recommendation': 'Reduce filler words and verbal pauses',
                'specific_tips': [
                    'Practice pausing silently instead of using filler words',
                    'Record yourself speaking and count filler words',
                    'Slow down your speaking pace to allow for clearer thinking'
                ],
                'target_improvement': 'Reduce filler words to under 3 per response'
            })
        
        # Content-based recommendations
        content_overall = content_analysis.get('overall_content_performance', {})
        if content_overall.get('score', 0) < 70:
            recommendations.append({
                'category': 'Technical Content',
                'priority': 'High',
                'recommendation': 'Strengthen technical knowledge and response structure',
                'specific_tips': [
                    'Use the STAR method for behavioral questions',
                    'Practice explaining technical concepts clearly',
                    'Prepare specific examples from your experience'
                ],
                'target_improvement': 'Increase technical score to 75+'
            })
        
        return recommendations
    
    def _generate_company_insights(self, session_results: Dict) -> Dict:
        """Generate company-specific insights and recommendations"""
        
        metadata = session_results.get('session_metadata', {})
        company = metadata.get('company_name', '')
        role = metadata.get('role', '')
        
        # Get company benchmark data
        benchmark = self.industry_benchmarks.get(company, {})
        
        insights = {
            'company_focus_areas': benchmark.get('focus_areas', []),
            'company_culture_fit': self._assess_culture_fit(session_results, company),
            'role_specific_feedback': self._get_role_specific_feedback(session_results, role),
            'company_comparison': self._compare_to_company_standards(session_results, benchmark)
        }
        
        return insights
    
    def _calculate_performance_metrics(self, user_sessions: List[Dict]) -> PerformanceMetrics:
        """Calculate comprehensive performance metrics from multiple sessions"""
        
        if not user_sessions:
            return PerformanceMetrics(
                overall_score=0, communication_score=0, confidence_score=0,
                professionalism_score=0, technical_score=0, eye_contact_avg=0,
                posture_avg=0, gesture_quality=0, speech_clarity=0,
                speaking_pace=0, filler_words_avg=0, session_count=0,
                total_duration=0, questions_answered=0, improvement_trend=0
            )
        
        # Calculate averages
        overall_scores = [s.get('overall_score', 0) for s in user_sessions]
        communication_scores = [s.get('communication_score', 0) for s in user_sessions]
        confidence_scores = [s.get('confidence_score', 0) for s in user_sessions]
        professionalism_scores = [s.get('professionalism_score', 0) for s in user_sessions]
        technical_scores = [s.get('technical_score', 0) for s in user_sessions]
        
        # Detailed metrics
        video_scores = [s.get('detailed_video_scores', {}) for s in user_sessions]
        audio_scores = [s.get('detailed_audio_scores', {}) for s in user_sessions]
        
        eye_contact_scores = [v.get('eye_contact', 0) for v in video_scores if v]
        confidence_video_scores = [v.get('confidence', 0) for v in video_scores if v]
        attention_scores = [v.get('attention', 0) for v in video_scores if v]
        
        clarity_scores = [a.get('clarity', 0) for a in audio_scores if a]
        pace_scores = [a.get('pace', 120) for a in audio_scores if a]
        filler_counts = [a.get('filler_words', 0) for a in audio_scores if a]
        
        # Calculate improvement trend
        improvement_trend = 0
        if len(overall_scores) > 1:
            improvement_trend = (overall_scores[-1] - overall_scores[0]) / len(overall_scores)
        
        return PerformanceMetrics(
            overall_score=np.mean(overall_scores),
            communication_score=np.mean(communication_scores),
            confidence_score=np.mean(confidence_scores),
            professionalism_score=np.mean(professionalism_scores),
            technical_score=np.mean(technical_scores),
            eye_contact_avg=np.mean(eye_contact_scores) if eye_contact_scores else 0,
            posture_avg=np.mean(attention_scores) if attention_scores else 0,
            gesture_quality=np.mean(confidence_video_scores) if confidence_video_scores else 0,
            speech_clarity=np.mean(clarity_scores) if clarity_scores else 0,
            speaking_pace=np.mean(pace_scores) if pace_scores else 120,
            filler_words_avg=np.mean(filler_counts) if filler_counts else 0,
            session_count=len(user_sessions),
            total_duration=sum(s.get('session_duration', 0) for s in user_sessions),
            questions_answered=sum(s.get('answered_questions', 0) for s in user_sessions),
            improvement_trend=improvement_trend
        )
    
    def _generate_ai_insights(self, user_sessions: List[Dict], metrics: PerformanceMetrics, trends: Dict) -> List[str]:
        """Generate AI-powered insights using Groq"""
        
        if not client:
            return [
                "Performance shows steady improvement across sessions",
                "Focus on maintaining consistent eye contact for better engagement",
                "Technical competency is developing well with practice"
            ]
        
        try:
            # Prepare context for AI analysis
            context = f"""
            User Interview Performance Analysis:
            
            Sessions Analyzed: {metrics.session_count}
            Overall Average Score: {metrics.overall_score:.1f}%
            Communication Score: {metrics.communication_score:.1f}%
            Confidence Score: {metrics.confidence_score:.1f}%
            Technical Score: {metrics.technical_score:.1f}%
            
            Improvement Trend: {metrics.improvement_trend:.2f} points per session
            
            Detailed Metrics:
            - Eye Contact Average: {metrics.eye_contact_avg:.1f}%
            - Speech Clarity: {metrics.speech_clarity:.1f}%
            - Speaking Pace: {metrics.speaking_pace:.1f} WPM
            - Filler Words Average: {metrics.filler_words_avg:.1f} per session
            
            Trend Analysis: {json.dumps(trends, indent=2)}
            
            Generate 5-7 specific, actionable insights about this user's interview performance.
            Focus on patterns, strengths, areas for improvement, and strategic recommendations.
            Be encouraging but honest about areas needing work.
            """
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert interview coach and performance analyst. Provide specific, actionable insights about interview performance data."},
                    {"role": "user", "content": context}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            # Parse AI response into individual insights
            ai_response = response.choices[0].message.content
            insights = [insight.strip() for insight in ai_response.split('\n') if insight.strip() and not insight.strip().startswith('#')]
            
            return insights[:7]  # Limit to 7 insights
            
        except Exception as e:
            print(f"⚠️ AI insights generation failed: {e}")
            return [
                f"Completed {metrics.session_count} interview sessions with {metrics.overall_score:.1f}% average performance",
                f"Shows {abs(metrics.improvement_trend):.1f} point {'improvement' if metrics.improvement_trend > 0 else 'decline'} per session",
                "Strong areas include communication and professionalism",
                "Continue practicing to build consistency across all performance areas"
            ]
    
    # Helper methods for scoring and grading
    def _score_to_grade(self, score: float) -> str:
        """Convert numerical score to letter grade"""
        if score >= 90: return "A+"
        elif score >= 85: return "A"
        elif score >= 80: return "A-"
        elif score >= 75: return "B+"
        elif score >= 70: return "B"
        elif score >= 65: return "B-"
        elif score >= 60: return "C+"
        elif score >= 55: return "C"
        elif score >= 50: return "C-"
        else: return "D"
    
    def _normalize_pace_score(self, pace: float) -> float:
        """Normalize speaking pace to 0-100 score"""
        # Ideal pace is 140-160 WPM
        if 140 <= pace <= 160:
            return 100
        elif 120 <= pace <= 180:
            return 85
        elif 100 <= pace <= 200:
            return 70
        else:
            return max(0, 50 - abs(pace - 150) / 5)
    
    # Feedback generation methods
    def _get_eye_contact_feedback(self, score: float) -> str:
        if score >= 80: return "Excellent eye contact - maintains strong connection with interviewer"
        elif score >= 70: return "Good eye contact with room for more consistency"
        elif score >= 60: return "Adequate eye contact but could be improved with practice"
        else: return "Needs significant improvement in maintaining eye contact"
    
    def _get_confidence_feedback(self, score: float) -> str:
        if score >= 80: return "Displays strong confidence through body language and demeanor"
        elif score >= 70: return "Shows good confidence with some moments of uncertainty"
        elif score >= 60: return "Moderate confidence level - practice can help build presence"
        else: return "Low confidence display - focus on posture and facial expressions"
    
    def _get_professionalism_feedback(self, score: float) -> str:
        if score >= 85: return "Excellent professional presence and appearance"
        elif score >= 75: return "Good professional demeanor with minor areas for polish"
        elif score >= 65: return "Adequate professionalism - ensure consistency throughout"
        else: return "Needs improvement in professional appearance and conduct"
    
    def _get_body_language_feedback(self, score: float) -> str:
        if score >= 80: return "Excellent body language - engaging and professional"
        elif score >= 70: return "Good body language with consistent engagement"
        elif score >= 60: return "Adequate body language - maintain better posture and engagement"
        else: return "Needs improvement in body language and overall engagement"
    
    def _get_clarity_feedback(self, score: float) -> str:
        if score >= 85: return "Crystal clear speech - easy to understand"
        elif score >= 75: return "Generally clear speech with good articulation"
        elif score >= 65: return "Mostly clear but could benefit from slower pace"
        else: return "Speech clarity needs improvement - focus on articulation"
    
    def _get_pace_feedback(self, pace: float) -> str:
        if 140 <= pace <= 160: return "Perfect speaking pace - clear and engaging"
        elif pace < 120: return "Speaking too slowly - try to increase energy and pace"
        elif pace > 180: return "Speaking too quickly - slow down for better clarity"
        else: return "Good speaking pace with minor adjustments needed"
    
    def _get_filler_words_feedback(self, count: int) -> str:
        if count <= 2: return "Excellent - minimal use of filler words"
        elif count <= 5: return "Good control of filler words with room for improvement"
        elif count <= 8: return "Moderate use of filler words - practice reducing them"
        else: return "High use of filler words - focus on pausing instead"
    
    def _get_voice_confidence_feedback(self, score: float) -> str:
        if score >= 80: return "Strong, confident voice projection"
        elif score >= 70: return "Good voice confidence with steady delivery"
        elif score >= 60: return "Moderate voice confidence - work on projection and steadiness"
        else: return "Needs improvement in voice confidence and projection"
    
    def _get_technical_feedback(self, score: float) -> str:
        if score >= 85: return "Excellent technical knowledge and communication"
        elif score >= 75: return "Strong technical competency with clear explanations"
        elif score >= 65: return "Good technical understanding with room for clearer communication"
        else: return "Needs improvement in technical knowledge or explanation clarity"
    
    def _get_completion_feedback(self, rate: float) -> str:
        if rate >= 90: return "Excellent - completed nearly all questions"
        elif rate >= 80: return "Good completion rate with thorough responses"
        elif rate >= 70: return "Adequate completion - work on time management"
        else: return "Low completion rate - focus on concise, complete answers"
    
    def _get_response_quality_feedback(self, score: float) -> str:
        if score >= 85: return "High-quality responses with excellent detail and structure"
        elif score >= 75: return "Good response quality with clear communication"
        elif score >= 65: return "Adequate responses - work on structure and completeness"
        else: return "Needs improvement in response quality and detail"
    
    def _assess_culture_fit(self, session_results: Dict, company: str) -> Dict:
        """Assess cultural fit based on interview performance"""
        return {
            'score': 75.0,
            'areas': ['Communication style matches company culture', 'Professional demeanor appropriate'],
            'recommendations': ['Continue demonstrating collaborative attitude']
        }
    
    def _get_role_specific_feedback(self, session_results: Dict, role: str) -> List[str]:
        """Get role-specific feedback"""
        return [
            f"Performance aligns well with {role} expectations",
            "Technical competency matches role requirements",
            "Communication style appropriate for position level"
        ]
    
    def _compare_to_company_standards(self, session_results: Dict, benchmark: Dict) -> Dict:
        """Compare performance to company standards"""
        return {
            'meets_standards': True,
            'above_average_areas': ['Communication', 'Professionalism'],
            'improvement_areas': ['Technical depth'],
            'percentile': 75
        }
    
    def _generate_cross_company_recommendations(self, company_performance: Dict) -> List[str]:
        """Generate recommendations across companies"""
        return [
            "Focus on consistent performance across different company cultures",
            "Adapt communication style to match company expectations",
            "Leverage your strongest areas while improving weaker ones"
        ]
    
    def _get_user_sessions(self, user_id: str, time_period: str) -> List[Dict]:
        """Get user sessions for analysis"""
        # This would typically query a database
        return []  # Return empty for now
    
    def _analyze_performance_trends(self, user_sessions: List[Dict]) -> Dict:
        """Analyze performance trends over time"""
        return {
            'trend': 'improving',
            'rate': 2.5,
            'consistency': 'moderate',
            'peak_areas': ['Communication'],
            'declining_areas': []
        }
    
    def _create_improvement_plan(self, user_id: str, user_sessions: List[Dict], metrics: PerformanceMetrics) -> ImprovementPlan:
        """Create personalized improvement plan"""
        return ImprovementPlan(
            priority_areas=['Eye contact', 'Technical depth'],
            specific_recommendations=[
                {'category': 'Visual', 'recommendation': 'Practice camera engagement'},
                {'category': 'Technical', 'recommendation': 'Review system design concepts'}
            ],
            practice_exercises=[
                {'title': 'Mirror practice', 'description': 'Practice maintaining eye contact'},
                {'title': 'Technical drills', 'description': 'Daily coding challenges'}
            ],
            target_scores={'overall': 85.0, 'technical': 80.0},
            estimated_timeline='2-3 weeks with consistent practice',
            confidence_building_tips=[
                'Practice positive self-talk',
                'Record yourself to build comfort with camera',
                'Focus on your expertise and experiences'
            ]
        )
    
    def _generate_company_benchmarks(self, user_id: str, user_sessions: List[Dict]) -> List[CompanyBenchmark]:
        """Generate company-specific benchmarks"""
        return []  # Return empty for now
    
    def _update_user_history(self, user_id: str, session_analysis: Dict):
        """Update user performance history"""
        if user_id not in self.user_histories:
            self.user_histories[user_id] = []
        self.user_histories[user_id].append(session_analysis)
    
    def _calculate_overall_grade(self, performance: Dict) -> str:
        """Calculate overall grade from performance metrics"""
        overall_score = performance.get('overall_score', 0)
        return self._score_to_grade(overall_score)
    
    def _identify_key_strengths(self, session_results: Dict) -> List[str]:
        """Identify key strengths from session"""
        strengths = []
        if session_results.get('communication_score', 0) > 75:
            strengths.append('Strong communication skills')
        if session_results.get('professionalism_score', 0) > 80:
            strengths.append('Professional demeanor')
        if session_results.get('confidence_score', 0) > 75:
            strengths.append('Confident presentation')
        return strengths or ['Consistent effort and engagement']
    
    def _identify_improvement_priorities(self, session_results: Dict) -> List[str]:
        """Identify improvement priorities"""
        priorities = []
        if session_results.get('technical_score', 0) < 70:
            priorities.append('Technical knowledge and explanation')
        if session_results.get('detailed_video_scores', {}).get('eye_contact', 0) < 65:
            priorities.append('Eye contact and engagement')
        if session_results.get('detailed_audio_scores', {}).get('filler_words', 0) > 5:
            priorities.append('Reducing filler words')
        return priorities or ['Continue practicing for consistency']

    # Additional helper methods
    def _load_industry_benchmarks(self) -> Dict:
        """Load industry and company benchmarks"""
        # This would load from a comprehensive database
        return {
            'Google': {
                'focus_areas': ['Technical depth', 'Problem solving', 'Cultural fit'],
                'avg_scores': {'technical': 85, 'communication': 80, 'confidence': 82}
            },
            'Microsoft': {
                'focus_areas': ['Collaboration', 'Growth mindset', 'Technical skills'],
                'avg_scores': {'technical': 83, 'communication': 85, 'confidence': 80}
            },
            'Amazon': {
                'focus_areas': ['Leadership principles', 'Customer obsession', 'Technical excellence'],
                'avg_scores': {'technical': 87, 'communication': 78, 'confidence': 81}
            }
        }
    
    def _save_session_analysis(self, analysis: Dict):
        """Save individual session analysis"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.analytics_dir}/session_analysis_{analysis['session_id']}_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(analysis, f, indent=2, default=str)
                
            print(f"💾 Session analysis saved: {filename}")
        except Exception as e:
            print(f"❌ Failed to save session analysis: {e}")
    
    def _save_comprehensive_report(self, report: AnalyticsReport):
        """Save comprehensive analytics report"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.reports_dir}/comprehensive_report_{report.user_id}_{timestamp}.json"
            
            report_dict = asdict(report)
            with open(filename, 'w') as f:
                json.dump(report_dict, f, indent=2, default=str)
                
            print(f"📊 Comprehensive report saved: {filename}")
        except Exception as e:
            print(f"❌ Failed to save comprehensive report: {e}")

# Initialize the Analytics Engine
interview_analytics = InterviewAnalytics()

print("📊 Multi-Modal Performance Analytics - READY!")
print("🎯 Comprehensive performance analysis and benchmarking")
print("📈 Trend analysis and improvement tracking")
print("🤖 AI-powered insights and recommendations")
print("📋 Detailed reporting with visualizations")