"""
🚀 NEXUS UNIFIED CAREER ACCELERATION SYSTEM
===============================================

The complete AI-powered career development system integrating all 4 phases:
- Phase 1: Company Intelligence & Training
- Phase 2: Resume Building & Optimization  
- Phase 3: Assessment & Screening Tests
- Phase 4: AI Interview Simulator

Created by: AI Career Development Team
Version: 4.0 - Complete Integration
Date: September 29, 2025
"""

import os
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
import re

# Import all phase agents
try:
    from .CompanyIntelligenceEngine import company_intelligence_engine
    from .ResumeProcessor import resume_processor  
    from .AssessmentEngine import assessment_engine
    from .InterviewHelper.InterviewAgent import InterviewAgent
    from .InterviewHelper.AIInterviewEngine import AIInterviewEngine
    from .InterviewHelper.InterviewSessionManager import InterviewSessionManager
    from .InterviewHelper.InterviewAnalytics import InterviewAnalytics
    PHASES_AVAILABLE = True
    print("✅ All NEXUS phases imported successfully!")
except ImportError as e:
    PHASES_AVAILABLE = False
    print(f"⚠️ Some NEXUS phases not available: {e}")

class NEXUSAgent:
    """Unified NEXUS Career Acceleration System"""
    
    def __init__(self):
        self.user_profile = {}
        self.career_journey = {}
        self.session_context = {}
        self.active_phase = None
        
        # Initialize phase engines
        self.company_engine = None
        self.resume_processor = None
        self.assessment_engine = None
        self.interview_engine = None
        
        # Performance tracking
        self.metrics = {
            "sessions_completed": 0,
            "assessments_taken": 0,
            "interviews_conducted": 0,
            "resumes_optimized": 0,
            "companies_researched": 0
        }
        
        self.initialize_nexus()
        
    def initialize_nexus(self):
        """Initialize the NEXUS system with all phases"""
        print("🚀 Initializing NEXUS Career Acceleration System...")
        
        if PHASES_AVAILABLE:
            try:
                # Initialize Phase 1: Company Intelligence
                self.company_engine = company_intelligence_engine
                print("✅ Phase 1: Company Intelligence Engine - READY")
                
                # Initialize Phase 2: Resume Processor  
                self.resume_processor = resume_processor
                print("✅ Phase 2: Resume Building System - READY")
                
                # Initialize Phase 3: Assessment Engine
                self.assessment_engine = assessment_engine
                print("✅ Phase 3: Assessment & Testing Engine - READY")
                
                # Initialize Phase 4: AI Interview System
                self.interview_engine = AIInterviewEngine()
                print("✅ Phase 4: AI Interview Simulator - READY")
                
                print("🎯 NEXUS System fully initialized!")
                print("💼 Ready for complete career acceleration!")
                
            except Exception as e:
                print(f"⚠️ Error initializing NEXUS phases: {e}")
        else:
            print("⚠️ Running in limited mode - some phases unavailable")
    
    def process_command(self, query: str) -> str:
        """Process unified NEXUS commands"""
        query_lower = query.lower().strip()
        
        # Command pattern matching
        command_patterns = {
            # Phase 1: Company Intelligence
            'company_research': [
                r'research (.*?) company',
                r'tell me about (.*?) company',
                r'company intel on (.*)',
                r'analyze (.*?) for job',
                r'company culture at (.*)',
                r'prepare for (.*?) interview'
            ],
            
            # Phase 2: Resume Building
            'resume_building': [
                r'build resume for (.*)',
                r'optimize resume for (.*)',
                r'create resume',
                r'improve my resume',
                r'resume analysis',
                r'ats optimize'
            ],
            
            # Phase 3: Assessments
            'assessment': [
                r'start assessment',
                r'take test',
                r'practice coding',
                r'dsa challenge',
                r'aptitude test',
                r'technical mcq'
            ],
            
            # Phase 4: Interview Preparation
            'interview': [
                r'start interview',
                r'practice interview',
                r'interview simulation',
                r'behavioral interview',
                r'technical interview',
                r'mock interview'
            ],
            
            # System commands
            'system': [
                r'nexus status',
                r'career progress',
                r'show metrics',
                r'help',
                r'what can you do'
            ]
        }
        
        # Match command type
        command_type = self.classify_command(query_lower, command_patterns)
        
        # Route to appropriate phase
        if command_type == 'company_research':
            return self.handle_company_research(query)
        elif command_type == 'resume_building':
            return self.handle_resume_building(query)
        elif command_type == 'assessment':
            return self.handle_assessment(query)
        elif command_type == 'interview':
            return self.handle_interview(query)
        elif command_type == 'system':
            return self.handle_system_commands(query)
        else:
            return self.handle_general_career_query(query)
    
    def classify_command(self, query: str, patterns: Dict[str, List[str]]) -> Optional[str]:
        """Classify the command type using pattern matching"""
        for command_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, query):
                    return command_type
        return None
    
    def handle_company_research(self, query: str) -> str:
        """Handle Phase 1: Company Intelligence queries"""
        print("🏢 Processing company intelligence request...")
        self.active_phase = "Phase 1: Company Intelligence"
        
        # Extract company name
        company_patterns = [
            r'research (.*?) company',
            r'tell me about (.*?) company', 
            r'company intel on (.*)',
            r'analyze (.*?) for job',
            r'company culture at (.*)',
            r'prepare for (.*?) interview'
        ]
        
        company_name = None
        for pattern in company_patterns:
            match = re.search(pattern, query.lower())
            if match:
                company_name = match.group(1).strip()
                break
        
        if not company_name:
            return """
🏢 **Company Intelligence System**

Please specify a company name. Examples:
• "Research Google company"
• "Tell me about Microsoft company"  
• "Analyze Amazon for job"
• "Company culture at Netflix"
• "Prepare for Apple interview"

I'll provide comprehensive insights including:
📊 Company overview and culture
💼 Role requirements and skills
📈 Interview process and tips
🎯 Preparation roadmap
            """
        
        try:
            if self.company_engine:
                result = self.company_engine.research_company(company_name)
                self.metrics["companies_researched"] += 1
                return f"""
🏢 **Company Intelligence: {company_name.title()}**

{result}

💡 **Next Steps:**
• Build optimized resume: "build resume for {company_name}"
• Take assessments: "start assessment"  
• Practice interviews: "start interview for {company_name}"
                """
            else:
                return "⚠️ Company intelligence engine not available"
                
        except Exception as e:
            return f"❌ Error researching company: {e}"
    
    def handle_resume_building(self, query: str) -> str:
        """Handle Phase 2: Resume Building queries"""
        print("📄 Processing resume building request...")
        self.active_phase = "Phase 2: Resume Building"
        
        try:
            if self.resume_processor:
                result = self.resume_processor.process_resume_request(query)
                self.metrics["resumes_optimized"] += 1
                return f"""
📄 **Resume Building System**

{result}

💡 **Next Steps:**
• Take skill assessments: "start assessment"
• Practice interviews: "start interview simulation"
• Research target companies: "research [company] company"
                """
            else:
                return """
📄 **Resume Building System**

Resume building features:
• ATS-friendly resume creation
• John Doe template library
• Company-specific optimization
• Existing resume analysis
• Template conversion

To activate: Ensure resume processor is available
                """
                
        except Exception as e:
            return f"❌ Error processing resume request: {e}"
    
    def handle_assessment(self, query: str) -> str:
        """Handle Phase 3: Assessment queries"""
        print("📊 Processing assessment request...")
        self.active_phase = "Phase 3: Assessment & Testing"
        
        try:
            if self.assessment_engine:
                result = self.assessment_engine.start_assessment(query)
                self.metrics["assessments_taken"] += 1
                return f"""
📊 **Assessment & Testing Engine**

{result}

💡 **Next Steps:**
• Practice interviews: "start interview simulation"
• Review performance: "show metrics"
• Build targeted resume: "build resume for [company]"
                """
            else:
                return """
📊 **Assessment & Testing Engine**

Available assessments:
• DSA coding challenges
• Technical MCQ tests  
• Aptitude assessments
• Timed test environments
• Performance analytics

To activate: Ensure assessment engine is available
                """
                
        except Exception as e:
            return f"❌ Error starting assessment: {e}"
    
    def handle_interview(self, query: str) -> str:
        """Handle Phase 4: Interview queries"""
        print("🎬 Processing interview simulation request...")
        self.active_phase = "Phase 4: AI Interview Simulator"
        
        try:
            # Try to import and use the working Phase 4 system
            try:
                from .InterviewHelper.InterviewAgent import InterviewAgent
                from .InterviewHelper.AIInterviewEngine import AIInterviewEngine
                
                # Initialize interview agent for natural language processing
                interview_agent = InterviewAgent()
                result = interview_agent.process_command("nexus_user", query)
                self.metrics["interviews_conducted"] += 1
                
                return f"""
🎬 **AI Interview Simulator - ACTIVE**

{result}

💡 **NEXUS Integration Active:**
• 🎯 Multi-modal behavioral analysis with advanced ML
• 📊 Real-time performance feedback and coaching
• 🎥 Camera-based confidence and eye contact scoring
• 🎤 Audio analysis and speech recognition
• 🤖 AI-powered conversation with company-specific questions

💡 **Next Steps:**
• Review performance: "show metrics"
• Research more companies: "research [company] company"
• Optimize resume: "improve my resume"
• Take skill assessments: "start assessment"
                """
            except ImportError:
                # Fallback if Phase 4 not available
                self.metrics["interviews_conducted"] += 1
                return """
🎬 **AI Interview Simulator - LIMITED MODE**

Interview simulation features available:
• Multi-modal behavioral analysis
• Company-specific questions
• Real-time performance feedback
• Camera-based confidence scoring
• Voice interaction capabilities

💡 **NEXUS Integration:**
• Company insights inform questions
• Resume data guides evaluation  
• Assessment results adjust difficulty

To activate full system: Ensure all Phase 4 components are installed
                """
                
        except Exception as e:
            return f"❌ Error processing interview request: {e}"
    
    def handle_system_commands(self, query: str) -> str:
        """Handle system and status commands"""
        query_lower = query.lower()
        
        if 'status' in query_lower or 'help' in query_lower or 'what can you do' in query_lower:
            return self.get_nexus_status()
        elif 'progress' in query_lower or 'metrics' in query_lower:
            return self.get_career_metrics()
        else:
            return self.get_nexus_help()
    
    def handle_general_career_query(self, query: str) -> str:
        """Handle general career development queries"""
        return f"""
🚀 **NEXUS Career Acceleration System**

I didn't recognize that specific command. Here's what I can help you with:

🏢 **Company Intelligence** (Phase 1)
• "Research Google company"
• "Tell me about Microsoft company"
• "Company culture at Amazon"

📄 **Resume Building** (Phase 2)  
• "Build resume for Netflix"
• "Optimize resume"
• "ATS resume analysis"

📊 **Skill Assessment** (Phase 3)
• "Start assessment"
• "DSA challenge"
• "Technical MCQ test"

🎬 **Interview Practice** (Phase 4)
• "Start interview for Apple"
• "Practice behavioral interview"
• "Mock interview simulation"

🎯 **System Commands**
• "NEXUS status"
• "Career progress" 
• "Show metrics"

💡 Your query: "{query}"
Try being more specific or use one of the examples above!
        """
    
    def get_nexus_status(self) -> str:
        """Get comprehensive NEXUS system status"""
        phase_status = []
        
        # Check Phase 1
        if self.company_engine:
            phase_status.append("✅ Phase 1: Company Intelligence - ACTIVE")
        else:
            phase_status.append("⚠️ Phase 1: Company Intelligence - LIMITED")
            
        # Check Phase 2  
        if self.resume_processor:
            phase_status.append("✅ Phase 2: Resume Building - ACTIVE")
        else:
            phase_status.append("⚠️ Phase 2: Resume Building - LIMITED")
            
        # Check Phase 3
        if self.assessment_engine:
            phase_status.append("✅ Phase 3: Assessments - ACTIVE")
        else:
            phase_status.append("⚠️ Phase 3: Assessments - LIMITED")
            
        # Check Phase 4
        if self.interview_engine:
            phase_status.append("✅ Phase 4: AI Interviews - ACTIVE")
        else:
            phase_status.append("⚠️ Phase 4: AI Interviews - LIMITED")
        
        return f"""
🚀 **NEXUS SYSTEM STATUS**

{''.join(f'{status}' for status in phase_status)}

📊 **Performance Metrics:**
• Companies Researched: {self.metrics['companies_researched']}
• Resumes Optimized: {self.metrics['resumes_optimized']}  
• Assessments Taken: {self.metrics['assessments_taken']}
• Interviews Conducted: {self.metrics['interviews_conducted']}
• Total Sessions: {self.metrics['sessions_completed']}

🎯 **Active Phase:** {self.active_phase or "None"}

💼 **Ready for complete career acceleration!**
        """
    
    def get_career_metrics(self) -> str:
        """Get detailed career progress metrics"""
        total_activities = sum(self.metrics.values())
        
        progress_level = "Beginner"
        if total_activities >= 20:
            progress_level = "Expert"
        elif total_activities >= 10:
            progress_level = "Advanced"
        elif total_activities >= 5:
            progress_level = "Intermediate"
        
        return f"""
📊 **CAREER ACCELERATION METRICS**

🎯 **Progress Level:** {progress_level}

📈 **Activity Breakdown:**
• 🏢 Companies Researched: {self.metrics['companies_researched']}
• 📄 Resumes Optimized: {self.metrics['resumes_optimized']}
• 📊 Assessments Completed: {self.metrics['assessments_taken']}  
• 🎬 Interviews Practiced: {self.metrics['interviews_conducted']}
• 🚀 Total Sessions: {self.metrics['sessions_completed']}

💡 **Recommendations:**
{self.get_personalized_recommendations()}

🎯 **Keep pushing forward! Every session brings you closer to your dream job!**
        """
    
    def get_personalized_recommendations(self) -> str:
        """Get AI-powered personalized recommendations"""
        recommendations = []
        
        if self.metrics['companies_researched'] < 3:
            recommendations.append("• Research 2-3 target companies to focus your preparation")
            
        if self.metrics['resumes_optimized'] < 2:
            recommendations.append("• Optimize your resume for different roles/companies")
            
        if self.metrics['assessments_taken'] < 5:
            recommendations.append("• Take more skill assessments to identify improvement areas")
            
        if self.metrics['interviews_conducted'] < 5:
            recommendations.append("• Practice more mock interviews to build confidence")
        
        if not recommendations:
            recommendations.append("• You're doing great! Consider exploring advanced interview scenarios")
            recommendations.append("• Try practicing for senior-level positions")
            
        return '\n'.join(recommendations)
    
    def get_nexus_help(self) -> str:
        """Get comprehensive NEXUS help"""
        return """
🚀 **NEXUS CAREER ACCELERATION SYSTEM - HELP**

🎯 **Complete Career Development Pipeline:**

**Phase 1: Company Intelligence**  
Research target companies, understand culture, get role requirements
• "Research Google company"
• "Tell me about Amazon culture" 
• "Prepare for Microsoft interview"

**Phase 2: Resume Building**
Create ATS-friendly resumes optimized for specific companies  
• "Build resume for Netflix"
• "Optimize resume for tech role"
• "ATS resume analysis"

**Phase 3: Skill Assessment**
Take comprehensive tests to identify strengths and gaps
• "Start coding assessment"
• "DSA challenge for algorithms" 
• "Technical MCQ for system design"

**Phase 4: Interview Simulation**
Practice with AI interviewer using camera analysis
• "Start interview for Apple"
• "Mock behavioral interview"
• "Technical interview practice"

**🎯 Integrated Workflow:**
1. Research target company → 2. Build optimized resume → 
3. Take skill assessments → 4. Practice interviews → 5. GET HIRED! 

💼 **Ready to accelerate your career? Start with any command above!**
        """

# Global NEXUS instance
nexus_agent = NEXUSAgent()

def NEXUS(query: str) -> str:
    """Main NEXUS entry point"""
    try:
        nexus_agent.metrics["sessions_completed"] += 1
        result = nexus_agent.process_command(query)
        return result
        
    except Exception as e:
        return f"""
❌ **NEXUS Error**

An error occurred while processing your request: {e}

💡 **Try these commands:**
• "NEXUS status" - Check system status
• "Help" - Get full command list  
• "Research Google company" - Start company intelligence
• "Start interview" - Begin interview simulation

🔧 **Support:** If the error persists, please check system dependencies.
        """

if __name__ == "__main__":
    # Test NEXUS system
    print("🧪 Testing NEXUS Integration...")
    
    test_queries = [
        "NEXUS status",
        "Research Google company", 
        "Build resume for Microsoft",
        "Start assessment",
        "Start interview for Amazon",
        "Show career metrics"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        print("=" * 50)
        result = NEXUS(query)
        print(result)
        print("=" * 50)