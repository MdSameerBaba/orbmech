"""
🤖 NEXUS INTERVIEW AGENT
Natural Language Interface for AI Interview Simulator

This agent provides:
- Natural language commands for interview management
- Conversational interface for starting/managing interviews
- Integration with all Phase 4 components
- Real-time coaching and feedback
- Performance analytics queries
- Company-specific interview preparation
"""

import json
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import asdict

from .AIInterviewEngine import ai_interview_engine, InterviewType, InterviewDifficulty
from .InterviewSessionManager import interview_session_manager, SessionSettings
from .InterviewAnalytics import interview_analytics

# Groq AI for natural language processing
from groq import Groq
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
GROQ_API_KEY = env_vars.get("GroqAPIKey")

try:
    client = Groq(api_key=GROQ_API_KEY)
except:
    client = None

class InterviewAgent:
    """
    NEXUS Interview Agent - Natural Language Interface for AI Interview Simulator
    
    Handles conversational commands for:
    - Starting and managing interview sessions
    - Real-time coaching and feedback
    - Performance analytics and reporting
    - Company-specific preparation
    - Multi-modal analysis control
    """
    
    def __init__(self):
        self.engine = ai_interview_engine
        self.session_manager = interview_session_manager
        self.analytics = interview_analytics
        
        # Current context
        self.current_user_id = None
        self.active_session_id = None
        self.conversation_history = []
        
        # Command patterns
        self.command_patterns = {
            'start_interview': [
                r'start.*interview.*for\s+(.+)\s+at\s+(.+)',
                r'begin.*interview.*(.+).*company.*(.+)',
                r'interview.*practice.*(.+).*role.*(.+)',
                r'simulate.*interview.*(.+)'
            ],
            'check_performance': [
                r'how.*am.*i.*doing',
                r'show.*my.*performance',
                r'performance.*report',
                r'analytics.*dashboard'
            ],
            'get_feedback': [
                r'give.*me.*feedback',
                r'what.*can.*i.*improve',
                r'areas.*for.*improvement',
                r'interview.*tips'
            ],
            'stop_interview': [
                r'stop.*interview',
                r'end.*session',
                r'finish.*interview',
                r'quit.*interview'
            ],
            'company_prep': [
                r'prepare.*for.*(.+).*interview',
                r'tell.*me.*about.*(.+).*company',
                r'(.+).*interview.*tips',
                r'what.*to.*expect.*at.*(.+)'
            ]
        }
        
        print("🤖 NEXUS Interview Agent initialized!")
    
    def process_command(self, user_id: str, message: str) -> str:
        """Process natural language command and return appropriate response"""
        
        self.current_user_id = user_id
        message = message.lower().strip()
        
        # Add to conversation history
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user_id': user_id,
            'message': message,
            'type': 'user_input'
        })
        
        try:
            # Check for specific command patterns
            response = self._match_command_patterns(message)
            
            if response:
                return response
            
            # Use AI for more complex queries
            ai_response = self._process_with_ai(message)
            
            return ai_response
            
        except Exception as e:
            error_response = f"I encountered an error processing your request: {str(e)}. Please try again or ask for help."
            self._add_to_history('agent_response', error_response)
            return error_response
    
    def _match_command_patterns(self, message: str) -> Optional[str]:
        """Match message against predefined command patterns"""
        
        # Start interview commands
        for pattern in self.command_patterns['start_interview']:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                if len(match.groups()) >= 2:
                    role = match.group(1).strip()
                    company = match.group(2).strip()
                else:
                    # Try to extract role and company from single match
                    role = match.group(1).strip() if match.groups() else "Software Engineer"
                    company = self._extract_company_from_message(message)
                
                return self._start_interview_session(role, company)
        
        # Performance check commands
        for pattern in self.command_patterns['check_performance']:
            if re.search(pattern, message, re.IGNORECASE):
                return self._get_performance_summary()
        
        # Feedback commands
        for pattern in self.command_patterns['get_feedback']:
            if re.search(pattern, message, re.IGNORECASE):
                return self._provide_feedback()
        
        # Stop interview commands
        for pattern in self.command_patterns['stop_interview']:
            if re.search(pattern, message, re.IGNORECASE):
                return self._stop_current_interview()
        
        # Company preparation commands
        for pattern in self.command_patterns['company_prep']:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                return self._provide_company_preparation(company)
        
        return None
    
    def _start_interview_session(self, role: str, company: str) -> str:
        """Start a new interview session"""
        
        if not self.current_user_id:
            return "Please provide your user ID to start an interview session."
        
        if self.active_session_id:
            return f"You already have an active interview session. Please end the current session first or say 'stop interview' to finish it."
        
        try:
            # Determine interview type and difficulty based on role
            interview_type = self._determine_interview_type(role)
            difficulty = self._determine_difficulty(role)
            
            # Create interview session
            session_id = self.engine.create_interview_session(
                user_id=self.current_user_id,
                company_name=company,
                role=role,
                interview_type=interview_type,
                difficulty=difficulty
            )
            
            # Configure session settings
            settings = SessionSettings(
                show_live_feedback=True,
                record_session=True,
                enable_hints=True,
                time_limit_per_question=300,
                show_confidence_meter=True,
                enable_voice_commands=True
            )
            
            # Start the session
            success = self.session_manager.start_interview_session(session_id, settings)
            
            if success:
                self.active_session_id = session_id
                response = f"""🎬 **Interview Session Started!**

**Company:** {company}
**Role:** {role}
**Interview Type:** {interview_type.value.title()}
**Difficulty:** {difficulty.value.title()}

Your interview has begun! The AI interviewer will ask you questions, and I'll provide real-time analysis of your:
- 👁️ Eye contact and engagement
- 😊 Facial expressions and confidence
- 🎤 Speech clarity and pace
- 💼 Professional demeanor

**Tips for success:**
- Look directly at your camera
- Speak clearly and at a moderate pace
- Maintain good posture
- Take your time to think before answering

You can say "pause", "repeat question", or "help" during the interview. Good luck! 🍀"""
                
                self._add_to_history('agent_response', response)
                return response
            else:
                return "❌ Failed to start interview session. Please check your camera and try again."
        
        except Exception as e:
            return f"❌ Error starting interview: {str(e)}"
    
    def _get_performance_summary(self) -> str:
        """Get current performance summary"""
        
        if not self.current_user_id:
            return "Please provide your user ID to view performance data."
        
        if self.active_session_id:
            # Get live performance data
            live_data = self.session_manager.get_live_analysis()
            
            response = f"""📊 **Live Performance Analysis**

**Current Scores:**
- Overall Performance: {live_data.overall_performance:.1f}%
- Eye Contact: {live_data.eye_contact_score:.1f}%
- Confidence Level: {live_data.confidence_level:.1f}%
- Professionalism: {live_data.professionalism_score:.1f}%

**Speaking Analysis:**
- Speaking Pace: {live_data.speaking_pace:.0f} WPM
- Filler Words: {live_data.filler_word_count}

**Current Status:**
- Question: {live_data.current_question[:100]}{'...' if len(live_data.current_question) > 100 else ''}
- Time Remaining: {live_data.time_remaining} seconds

**Live Recommendations:**
{chr(10).join(f'• {rec}' for rec in live_data.recommendations)}"""

        else:
            # Get historical performance data
            try:
                report = self.analytics.generate_comprehensive_report(self.current_user_id, "recent")
                
                if report:
                    metrics = report.performance_metrics
                    response = f"""📊 **Performance Summary**

**Overall Metrics:**
- Average Score: {metrics.overall_score:.1f}%
- Communication: {metrics.communication_score:.1f}%
- Confidence: {metrics.confidence_score:.1f}%
- Technical: {metrics.technical_score:.1f}%

**Session Statistics:**
- Total Sessions: {metrics.session_count}
- Questions Answered: {metrics.questions_answered}
- Total Duration: {metrics.total_duration/60:.1f} minutes
- Improvement Trend: {metrics.improvement_trend:+.1f} points per session

**Key Insights:**
{chr(10).join(f'• {insight}' for insight in report.ai_insights[:3])}

💡 **Tip:** Start a new interview session to get real-time performance feedback!"""
                else:
                    response = "No performance data available yet. Start your first interview to begin tracking your progress!"
            
            except Exception as e:
                response = f"Unable to retrieve performance data: {str(e)}"
        
        self._add_to_history('agent_response', response)
        return response
    
    def _provide_feedback(self) -> str:
        """Provide personalized feedback and improvement suggestions"""
        
        if not self.current_user_id:
            return "Please provide your user ID to receive personalized feedback."
        
        try:
            # Get recent performance data
            report = self.analytics.generate_comprehensive_report(self.current_user_id, "recent")
            
            if not report:
                return "🌟 **Getting Started with Interview Practice**\n\nTo receive personalized feedback, start your first interview session! I'll analyze your performance and provide specific recommendations for improvement.\n\nSay something like: 'Start interview for Software Engineer at Google' to begin!"
            
            improvement_plan = report.improvement_plan
            metrics = report.performance_metrics
            
            response = f"""🎯 **Personalized Feedback & Improvement Plan**

**Your Strengths:**
{chr(10).join(f'✅ {strength}' for strength in report.improvement_plan.strengths if hasattr(report.improvement_plan, 'strengths')) if hasattr(report.improvement_plan, 'strengths') else '✅ Communication skills are developing well'}

**Priority Improvement Areas:**
{chr(10).join(f'🎯 {area}' for area in improvement_plan.priority_areas[:3])}

**Specific Recommendations:**
{chr(10).join(f'• {rec.get("recommendation", "Continue practicing regularly")}' for rec in improvement_plan.specific_recommendations[:3])}

**Practice Exercises:**
{chr(10).join(f'🏃 {exercise.get("title", "Mock interview practice")}' for exercise in improvement_plan.practice_exercises[:3])}

**Confidence Building Tips:**
{chr(10).join(f'💪 {tip}' for tip in improvement_plan.confidence_building_tips[:3])}

**Target Timeline:** {improvement_plan.estimated_timeline}

Would you like to start a practice session to work on these areas?"""
            
            self._add_to_history('agent_response', response)
            return response
            
        except Exception as e:
            return f"Unable to generate feedback: {str(e)}"
    
    def _stop_current_interview(self) -> str:
        """Stop the current interview session"""
        
        if not self.active_session_id:
            return "No active interview session to stop."
        
        try:
            # Stop the session and get results
            results = self.session_manager.stop_interview_session()
            
            if results:
                # Analyze the session
                analysis = self.analytics.analyze_session_performance(results)
                
                response = f"""🎬 **Interview Session Completed!**

**Final Scores:**
- Overall Performance: {results.get('overall_score', 0):.1f}%
- Communication: {results.get('communication_score', 0):.1f}%
- Confidence: {results.get('confidence_score', 0):.1f}%
- Technical: {results.get('technical_score', 0):.1f}%

**Session Statistics:**
- Duration: {results.get('session_duration', 0)/60:.1f} minutes
- Questions Answered: {results.get('answered_questions', 0)}/{results.get('total_questions', 0)}

**Key Strengths:**
{chr(10).join(f'✅ {strength}' for strength in results.get('strengths', ['Good effort and participation']))}

**Areas for Improvement:**
{chr(10).join(f'🎯 {area}' for area in results.get('improvement_areas', ['Continue practicing regularly']))}

**Next Steps:**
- Review your detailed performance report
- Practice the recommended areas
- Try another interview when you're ready

Great job completing the interview! 🌟"""

                self.active_session_id = None
                self._add_to_history('agent_response', response)
                return response
            else:
                self.active_session_id = None
                return "Interview session stopped. No results available."
        
        except Exception as e:
            self.active_session_id = None
            return f"Error stopping interview: {str(e)}"
    
    def _provide_company_preparation(self, company: str) -> str:
        """Provide company-specific interview preparation"""
        
        # This would integrate with Phase 1 Company Intelligence
        company_info = {
            'google': {
                'culture': 'Innovation, collaboration, data-driven decisions',
                'focus_areas': ['Technical depth', 'Problem-solving', 'Googleyness'],
                'interview_style': 'Structured behavioral and technical questions',
                'tips': [
                    'Practice system design questions',
                    'Prepare for coding challenges on whiteboard',
                    'Show passion for technology and learning',
                    'Demonstrate analytical thinking'
                ]
            },
            'microsoft': {
                'culture': 'Growth mindset, respect, integrity, accountability',
                'focus_areas': ['Technical skills', 'Collaboration', 'Leadership'],
                'interview_style': 'Behavioral (STAR method) + technical assessment',
                'tips': [
                    'Emphasize learning and growth experiences',
                    'Prepare examples of collaboration and teamwork',
                    'Show customer focus and business impact',
                    'Practice coding in your preferred language'
                ]
            },
            'amazon': {
                'culture': 'Customer obsession, ownership, invent and simplify',
                'focus_areas': ['Leadership principles', 'Technical excellence', 'Scale thinking'],
                'interview_style': 'Leadership principles + technical deep dive',
                'tips': [
                    'Prepare STAR stories for each leadership principle',
                    'Show examples of customer-focused decisions',
                    'Demonstrate ownership and accountability',
                    'Practice system design at scale'
                ]
            }
        }
        
        company_key = company.lower().replace(' ', '')
        info = company_info.get(company_key, {
            'culture': 'Professional, collaborative, results-oriented',
            'focus_areas': ['Technical skills', 'Problem-solving', 'Team fit'],
            'interview_style': 'Mixed behavioral and technical questions',
            'tips': [
                'Research the company thoroughly',
                'Prepare specific examples from your experience',
                'Practice both technical and behavioral questions',
                'Show enthusiasm for the role and company'
            ]
        })
        
        response = f"""🏢 **{company.title()} Interview Preparation**

**Company Culture:**
{info['culture']}

**Interview Focus Areas:**
{chr(10).join(f'• {area}' for area in info['focus_areas'])}

**Interview Style:**
{info['interview_style']}

**Success Tips:**
{chr(10).join(f'✅ {tip}' for tip in info['tips'])}

**Recommended Practice:**
🎯 Start a mock interview specifically for {company} to practice these areas!

Would you like to begin a practice interview for {company}?"""
        
        self._add_to_history('agent_response', response)
        return response
    
    def _process_with_ai(self, message: str) -> str:
        """Process complex queries using AI"""
        
        if not client:
            return "I'm currently unable to process complex queries. Please try a specific command like 'start interview' or 'show performance'."
        
        try:
            # Prepare context for AI
            context = f"""
            User Message: {message}
            Current User ID: {self.current_user_id}
            Active Session: {self.active_session_id is not None}
            
            Available Functions:
            - Start interview sessions for specific companies and roles
            - Provide real-time performance analysis during interviews
            - Generate comprehensive performance reports and analytics
            - Offer company-specific interview preparation
            - Give personalized feedback and improvement recommendations
            
            Conversation History:
            {json.dumps(self.conversation_history[-5:], indent=2, default=str)}
            
            Respond as a helpful AI interview coach. Be encouraging, specific, and actionable.
            If the user wants to start an interview, ask for the role and company.
            If they want performance data, provide what's available or suggest starting an interview.
            """
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are NEXUS Interview Agent, an AI interview coach specializing in multi-modal interview analysis and coaching. Be helpful, encouraging, and specific in your responses."},
                    {"role": "user", "content": context}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            ai_response = response.choices[0].message.content
            self._add_to_history('agent_response', ai_response)
            return ai_response
            
        except Exception as e:
            fallback_response = "I'd be happy to help you with interview practice! Try saying:\n• 'Start interview for [role] at [company]'\n• 'Show my performance'\n• 'Give me feedback'\n• 'Prepare for [company] interview'"
            self._add_to_history('agent_response', fallback_response)
            return fallback_response
    
    def _determine_interview_type(self, role: str) -> InterviewType:
        """Determine interview type based on role"""
        role_lower = role.lower()
        
        if any(term in role_lower for term in ['senior', 'principal', 'architect', 'lead']):
            return InterviewType.SYSTEM_DESIGN
        elif any(term in role_lower for term in ['engineer', 'developer', 'programmer']):
            return InterviewType.MIXED
        elif any(term in role_lower for term in ['manager', 'director', 'vp']):
            return InterviewType.BEHAVIORAL
        else:
            return InterviewType.MIXED
    
    def _determine_difficulty(self, role: str) -> InterviewDifficulty:
        """Determine difficulty based on role seniority"""
        role_lower = role.lower()
        
        if any(term in role_lower for term in ['principal', 'staff', 'director', 'vp']):
            return InterviewDifficulty.PRINCIPAL
        elif any(term in role_lower for term in ['senior', 'lead', 'architect']):
            return InterviewDifficulty.SENIOR
        elif any(term in role_lower for term in ['mid', 'intermediate', '3', '4', '5']):
            return InterviewDifficulty.MID
        else:
            return InterviewDifficulty.JUNIOR
    
    def _extract_company_from_message(self, message: str) -> str:
        """Extract company name from message"""
        # Common company names to look for
        companies = ['google', 'microsoft', 'amazon', 'apple', 'facebook', 'meta', 'netflix', 'uber', 'tesla', 'spotify']
        
        for company in companies:
            if company in message.lower():
                return company.title()
        
        return "Tech Company"
    
    def _add_to_history(self, message_type: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user_id': self.current_user_id,
            'message': content,
            'type': message_type
        })
    
    def get_help(self) -> str:
        """Get help information"""
        return """🤖 **NEXUS Interview Agent - Help**

**Available Commands:**

**🎬 Interview Sessions:**
- "Start interview for [role] at [company]"
- "Begin practice interview for Software Engineer at Google"
- "Stop interview" or "End session"

**📊 Performance & Analytics:**
- "Show my performance" 
- "How am I doing?"
- "Performance report"
- "Analytics dashboard"

**💡 Feedback & Coaching:**
- "Give me feedback"
- "What can I improve?"
- "Areas for improvement"
- "Interview tips"

**🏢 Company Preparation:**
- "Prepare for Google interview"
- "Tell me about Microsoft company"
- "Amazon interview tips"

**🎥 During Interviews:**
- "Pause" - Pause the current interview
- "Repeat" - Repeat the current question
- "Help" - Get interview help
- "Next" - Skip to next question

**Features:**
- Real-time camera and audio analysis
- Live performance feedback
- Company-specific interview simulation
- Comprehensive performance analytics
- Personalized improvement plans

Ready to start practicing? Just tell me the role and company you're interested in! 🚀"""

# Initialize the Interview Agent
interview_agent = InterviewAgent()

print("🤖 NEXUS Interview Agent - READY!")
print("💬 Natural language interface for AI interview simulator")
print("🎯 Conversational interview management and coaching")
print("📊 Real-time performance feedback and analytics")
print("🏢 Company-specific interview preparation")