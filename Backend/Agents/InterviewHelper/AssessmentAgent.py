"""
🧪 Assessment Agent
Handles assessment-related queries and integrates with the Assessment Engine

This agent processes natural language queries related to assessments and manages
the complete assessment workflow from creation to result analysis.
"""

import json
import os
from typing import Dict, List, Optional, Any
from Backend.Agents.InterviewHelper.AssessmentEngine import (
    AssessmentEngine, AssessmentConfig, AssessmentType, DifficultyLevel
)
from Backend.Agents.InterviewHelper.CompanyIntelligenceEngine import CompanyIntelligenceEngine
from Backend.Agents.InterviewHelper.ResumeBuilder import ResumeBuilder

class AssessmentAgent:
    """Agent for handling assessment-related queries"""
    
    def __init__(self):
        self.assessment_engine = AssessmentEngine()
        self.company_engine = CompanyIntelligenceEngine()
        self.resume_builder = ResumeBuilder()
        
        # Cache for session data
        self.current_assessment = None
        self.user_context = {}
    
    def process_query(self, query: str) -> str:
        """Process assessment-related queries"""
        
        query_lower = query.lower()
        
        # Assessment creation queries
        if any(keyword in query_lower for keyword in ['create assessment', 'start test', 'begin assessment']):
            return self._handle_assessment_creation(query)
        
        # Assessment status queries
        elif any(keyword in query_lower for keyword in ['assessment status', 'test progress', 'current test']):
            return self._handle_assessment_status(query)
        
        # Question-related queries
        elif any(keyword in query_lower for keyword in ['submit answer', 'answer question', 'next question']):
            return self._handle_question_interaction(query)
        
        # Results and analytics
        elif any(keyword in query_lower for keyword in ['results', 'score', 'performance', 'analysis']):
            return self._handle_results_query(query)
        
        # Assessment information
        elif any(keyword in query_lower for keyword in ['assessment info', 'test types', 'available assessments']):
            return self._handle_info_query(query)
        
        # Company-specific assessments
        elif any(keyword in query_lower for keyword in ['company test', 'company assessment', 'prepare for']):
            return self._handle_company_assessment(query)
        
        # DSA practice
        elif any(keyword in query_lower for keyword in ['dsa practice', 'coding practice', 'algorithm practice']):
            return self._handle_dsa_practice(query)
        
        # General help
        else:
            return self._handle_general_help(query)
    
    def _handle_assessment_creation(self, query: str) -> str:
        """Handle assessment creation requests"""
        
        try:
            # Parse company and role from query
            company_name, role = self._extract_company_and_role(query)
            
            if not company_name or not role:
                return self._get_assessment_creation_guide()
            
            # Get company intelligence
            print(f"🔍 Gathering intelligence for {role} at {company_name}...")
            company_intelligence = self.company_engine.research_company(company_name, role)
            
            # Get user's resume data (this would come from Phase 2)
            resume_data = self._get_user_resume_data()
            
            # Create customized assessment
            config = self.assessment_engine.create_company_specific_assessment(
                company_intelligence, resume_data, role
            )
            
            # Start the assessment
            session_info = self.assessment_engine.start_assessment(config)
            self.current_assessment = config.assessment_id
            
            return f"""
🎯 **{config.name} Created Successfully!**

📊 **Assessment Details:**
• **Company**: {company_name}
• **Role**: {role}  
• **Total Questions**: {config.total_questions}
• **Time Limit**: {config.time_limit_minutes} minutes
• **Passing Score**: {config.passing_score}%

📝 **Question Distribution:**
• **DSA Coding**: {config.dsa_questions} questions
• **Technical MCQ**: {config.mcq_questions} questions  
• **Aptitude**: {config.aptitude_questions} questions

🎮 **Assessment Started!**
Assessment ID: `{config.assessment_id}`

Ready to begin? Say "start first question" or "show me question 1" to proceed!

💡 **Tips:**
• Read questions carefully before answering
• Manage your time effectively ({config.time_limit_minutes} minutes total)
• Use hints when available for coding questions
• You can ask for clarification on any question
"""
            
        except Exception as e:
            return f"❌ Error creating assessment: {str(e)}\n\nPlease try again with a specific company and role, e.g., 'Create assessment for Software Engineer at Google'"
    
    def _handle_assessment_status(self, query: str) -> str:
        """Handle assessment status queries"""
        
        if not self.current_assessment:
            return "📋 **No Active Assessment**\n\nYou don't have any active assessments. Say 'create assessment for [role] at [company]' to start a new one!"
        
        # Get current session info
        session = self.assessment_engine.active_assessments.get(self.current_assessment)
        
        if not session:
            return "❌ Assessment session not found. Please start a new assessment."
        
        progress = session['current_question']
        total = len(session['questions'])
        time_elapsed = session.get('time_elapsed', 0)
        
        return f"""
📊 **Assessment Progress**

🎯 **Current Status**: Question {progress + 1} of {total}
⏰ **Time Elapsed**: {time_elapsed} minutes
📈 **Progress**: {(progress / total) * 100:.1f}% complete

🔄 **Next Steps**:
• Say "show current question" to see the active question
• Say "submit answer [your answer]" to answer
• Say "get hint" for coding questions

💪 Keep going! You're doing great!
"""
    
    def _handle_question_interaction(self, query: str) -> str:
        """Handle question interactions (submit, next, hints)"""
        
        if not self.current_assessment:
            return "❌ No active assessment. Please start an assessment first."
        
        session = self.assessment_engine.active_assessments.get(self.current_assessment)
        if not session:
            return "❌ Assessment session not found."
        
        query_lower = query.lower()
        
        # Show current question
        if 'show' in query_lower and ('question' in query_lower or 'current' in query_lower):
            current_idx = session['current_question']
            if current_idx < len(session['questions']):
                question = session['questions'][current_idx]
                return self._format_question_display(question, current_idx + 1, len(session['questions']))
            else:
                return "🎉 Assessment completed! Say 'show results' to see your performance."
        
        # Submit answer
        elif 'submit' in query_lower or 'answer' in query_lower:
            return self._handle_answer_submission(query, session)
        
        # Get hint
        elif 'hint' in query_lower:
            return self._provide_hint(session)
        
        return "❓ I can help you with:\n• 'show current question'\n• 'submit answer [your answer]'\n• 'get hint' (for coding questions)"
    
    def _handle_results_query(self, query: str) -> str:
        """Handle results and performance queries"""
        
        # Get recent assessment results
        stats = self.assessment_engine.get_assessment_stats()
        
        return f"""
📊 **Assessment System Statistics**

📈 **Question Database**:
• DSA Questions: {stats['total_dsa_questions']}
• Technical MCQs: {stats['total_mcq_questions']} 
• Aptitude Questions: {stats['total_aptitude_questions']}

🏢 **Supported Companies**: {len(stats['supported_companies'])}
{', '.join(stats['supported_companies'][:10])}{'...' if len(stats['supported_companies']) > 10 else ''}

🎮 **Active Sessions**: {stats['active_assessments']}

💡 **Available Commands**:
• "show my results" - View recent assessment results
• "create assessment for [role] at [company]" - Start new test
• "assessment analytics" - Detailed performance analysis
"""
    
    def _handle_info_query(self, query: str) -> str:
        """Handle information queries about assessments"""
        
        return """
🧪 **NEXUS Assessment System - Phase 3**

🎯 **Assessment Types Available**:

**1. DSA Coding Challenges** 🧠
• Algorithm implementation problems
• Data structure manipulation
• Time/space complexity optimization
• Real coding interview simulation

**2. Technical MCQs** 💻
• Programming language concepts
• System design principles
• Database management
• Software engineering practices

**3. Aptitude Tests** 📊
• Quantitative reasoning
• Logical puzzles
• Pattern recognition
• Verbal ability

**4. Company-Specific Assessments** 🏢
• Customized based on company intelligence
• Role-specific question selection
• Industry-standard difficulty levels
• Real interview pattern matching

🎮 **Features**:
• ⏰ Timed test environments
• 📊 Real-time progress tracking  
• 💡 Intelligent hint system
• 📈 Detailed performance analytics
• 🎯 Adaptive difficulty based on experience
• 🔄 Seamless integration with Phase 1 & 2 data

📝 **Getting Started**:
Say: "Create assessment for Software Engineer at Google"
"""
    
    def _handle_company_assessment(self, query: str) -> str:
        """Handle company-specific assessment queries"""
        
        company_name, role = self._extract_company_and_role(query)
        
        if company_name:
            # Get company assessment info
            company_info = self.company_engine.get_company_assessment_pattern(company_name)
            
            return f"""
🏢 **{company_name} Assessment Information**

🎯 **Typical Assessment Pattern**:
• **Interview Rounds**: {company_info.get('rounds', '3-4')}
• **Focus Areas**: {', '.join(company_info.get('focus_areas', ['Technical Skills', 'Problem Solving']))}
• **Difficulty Level**: {company_info.get('difficulty', 'Medium to Hard')}

📊 **Question Types**:
• **DSA Problems**: {company_info.get('dsa_percentage', '60')}%
• **Technical MCQs**: {company_info.get('mcq_percentage', '30')}%
• **System Design**: {company_info.get('system_design', '10')}%

⏰ **Time Allocation**:
• **Total Duration**: {company_info.get('duration', '90')} minutes
• **Per Question**: {company_info.get('time_per_question', '4-5')} minutes average

💡 **Preparation Tips**:
• Focus on {', '.join(company_info.get('key_topics', ['Arrays', 'Trees', 'Dynamic Programming']))}
• Practice {company_info.get('recommended_problems', '50-100')} problems
• Review {', '.join(company_info.get('technologies', ['Data Structures', 'Algorithms']))}

🚀 **Ready to Practice?**
Say: "Create assessment for {role or 'Software Engineer'} at {company_name}"
"""
        
        return """
🏢 **Company Assessment Preparation**

To get company-specific assessment information, please specify:

**Format**: "Prepare for [role] at [company]"

**Examples**:
• "Prepare for Software Engineer at Google"  
• "Assessment for Data Scientist at Microsoft"
• "Test for Frontend Developer at Amazon"

I'll provide:
✅ Company-specific question patterns
✅ Difficulty levels and focus areas  
✅ Time allocation strategies
✅ Key topics to prepare
✅ Customized practice assessments
"""
    
    def _handle_dsa_practice(self, query: str) -> str:
        """Handle DSA practice requests"""
        
        # Extract difficulty level or topic from query
        difficulty = self._extract_difficulty(query)
        topic = self._extract_topic(query)
        
        practice_info = {
            'available_topics': [
                'Arrays', 'Strings', 'Linked Lists', 'Trees', 'Graphs',
                'Dynamic Programming', 'Sorting & Searching', 'Stack & Queue'
            ],
            'difficulty_levels': ['Easy', 'Medium', 'Hard'],
            'total_problems': len(self.assessment_engine.dsa_questions)
        }
        
        return f"""
🧠 **DSA Practice System**

📚 **Available Topics** ({practice_info['total_problems']} total problems):
{chr(10).join(['• ' + topic for topic in practice_info['available_topics']])}

🎯 **Difficulty Levels**:
• **Easy**: Foundation building problems
• **Medium**: Interview-level challenges  
• **Hard**: Advanced algorithmic thinking

🎮 **Practice Modes**:
• **Topic-wise**: Focus on specific data structures
• **Company-wise**: Practice problems from target companies
• **Random Practice**: Mixed difficulty and topics
• **Timed Challenges**: Simulate real interview pressure

🚀 **Start Practicing**:
• "Create DSA practice on Arrays"
• "Medium difficulty tree problems"  
• "Google coding questions"
• "Random DSA challenge"

💡 **Features**:
• Real-time code execution
• Multiple test case validation
• Hint system for guidance
• Performance tracking
• Solution explanations
"""
    
    def _handle_general_help(self, query: str) -> str:
        """Handle general help and unknown queries"""
        
        return """
🧪 **NEXUS Assessment Helper - Available Commands**

🎯 **Start Assessment**:
• "Create assessment for [role] at [company]"
• "Start test for Software Engineer at Google"
• "Begin assessment for Data Scientist"

📊 **Assessment Management**:
• "Show current question" 
• "Submit answer [your answer]"
• "Get hint" (for coding questions)
• "Assessment status"

📈 **Results & Analytics**:
• "Show my results"
• "Assessment performance"
• "Strengths and weaknesses"

🏢 **Company Preparation**:
• "Prepare for Google interview"
• "Amazon assessment pattern"
• "Microsoft technical test info"

🧠 **Practice Modes**:  
• "DSA practice on trees"
• "Technical MCQ practice"
• "Aptitude test practice"

❓ **Need Help?**
• "Assessment info" - System overview
• "Available companies" - Supported companies
• "Question types" - Assessment categories

Just ask me anything about assessments, coding practice, or interview preparation!
"""
    
    def _extract_company_and_role(self, query: str) -> tuple:
        """Extract company name and role from query"""
        
        # Common company names
        companies = [
            'Google', 'Microsoft', 'Amazon', 'Facebook', 'Meta', 'Apple',
            'Netflix', 'Tesla', 'IBM', 'Oracle', 'Adobe', 'Salesforce',
            'Uber', 'Lyft', 'Twitter', 'LinkedIn', 'Spotify', 'Airbnb'
        ]
        
        # Common roles
        roles = [
            'Software Engineer', 'Data Scientist', 'Frontend Developer',
            'Backend Developer', 'Full Stack Developer', 'DevOps Engineer',
            'Product Manager', 'UI/UX Designer', 'ML Engineer', 'SDE',
            'Senior Software Engineer', 'Principal Engineer'
        ]
        
        query_lower = query.lower()
        
        # Find company
        found_company = None
        for company in companies:
            if company.lower() in query_lower:
                found_company = company
                break
        
        # Find role
        found_role = None
        for role in roles:
            if role.lower() in query_lower:
                found_role = role
                break
        
        # Try to extract using common patterns
        if ' at ' in query_lower:
            parts = query_lower.split(' at ')
            if len(parts) >= 2:
                # Role should be before 'at', company after
                role_part = parts[0].strip()
                company_part = parts[1].strip()
                
                # Find role in the first part
                for role in roles:
                    if role.lower() in role_part:
                        found_role = role
                        break
                
                # Find company in the second part
                for company in companies:
                    if company.lower() in company_part:
                        found_company = company
                        break
        
        return found_company, found_role
    
    def _extract_difficulty(self, query: str) -> Optional[str]:
        """Extract difficulty level from query"""
        query_lower = query.lower()
        
        if 'easy' in query_lower:
            return 'Easy'
        elif 'medium' in query_lower:
            return 'Medium'
        elif 'hard' in query_lower:
            return 'Hard'
        
        return None
    
    def _extract_topic(self, query: str) -> Optional[str]:
        """Extract topic from query"""
        query_lower = query.lower()
        
        topics_map = {
            'array': 'Arrays',
            'string': 'Strings', 
            'linked list': 'Linked Lists',
            'tree': 'Trees',
            'graph': 'Graphs',
            'dp': 'Dynamic Programming',
            'dynamic programming': 'Dynamic Programming',
            'sort': 'Sorting & Searching',
            'search': 'Sorting & Searching',
            'stack': 'Stack & Queue',
            'queue': 'Stack & Queue'
        }
        
        for keyword, topic in topics_map.items():
            if keyword in query_lower:
                return topic
        
        return None
    
    def _get_user_resume_data(self) -> Dict:
        """Get user's resume data from Phase 2"""
        # This would integrate with the ResumeBuilder to get actual user data
        # For now, return mock data
        
        return {
            'experience_level': 'Mid Level',
            'skills': ['Python', 'JavaScript', 'React', 'Node.js'],
            'years_experience': 4,
            'education': 'Bachelor\'s in Computer Science',
            'previous_roles': ['Software Developer', 'Frontend Developer']
        }
    
    def _get_assessment_creation_guide(self) -> str:
        """Return guide for creating assessments"""
        
        return """
🎯 **Create Your Custom Assessment**

To create a tailored assessment, please provide:

**Format**: "Create assessment for [ROLE] at [COMPANY]"

**Examples**:
✅ "Create assessment for Software Engineer at Google"
✅ "Start test for Data Scientist at Microsoft"  
✅ "Begin assessment for Frontend Developer at Amazon"

🎮 **What I'll Create**:
• **Company-specific questions** based on their interview patterns
• **Role-tailored content** matching job requirements
• **Adaptive difficulty** based on your experience level  
• **Realistic timing** simulating actual screening rounds

💡 **Popular Options**:
• Google Software Engineer Assessment
• Microsoft Data Scientist Test
• Amazon Frontend Developer Challenge
• Facebook Full Stack Engineer Exam

Ready to start? Just tell me the role and company!
"""
    
    def _format_question_display(self, question, current_num: int, total_num: int) -> str:
        """Format question for display"""
        
        if hasattr(question, 'title'):  # DSA Question
            return f"""
🧠 **DSA Coding Challenge** - Question {current_num}/{total_num}

**{question.title}** ({question.difficulty.value})
📂 Category: {question.category.value}

**Problem Statement:**
{question.description}

**Test Cases:**
{chr(10).join([f"Input: {tc.input_data} → Output: {tc.expected_output}" for tc in question.test_cases[:2]])}

💡 **Available Commands**:
• "submit answer [your code/approach]" - Submit your solution
• "get hint" - Get a helpful hint
• "clarify question" - Ask for clarification

⏰ Take your time to understand the problem before coding!
"""
        
        else:  # MCQ Question
            options_text = '\n'.join([f"{opt.id.upper()}. {opt.text}" for opt in question.options])
            
            return f"""
💻 **Technical MCQ** - Question {current_num}/{total_num}

**{question.question}** ({question.difficulty.value})
📂 Category: {question.category.value}

**Options:**
{options_text}

💡 **How to Answer**:
• "submit answer A" (or B, C, D)
• "submit A" (short form)

Choose the best answer and submit when ready!
"""
    
    def _handle_answer_submission(self, query: str, session: Dict) -> str:
        """Handle answer submission"""
        
        # Extract answer from query
        query_lower = query.lower()
        
        # Get current question
        current_idx = session['current_question']
        if current_idx >= len(session['questions']):
            return "🎉 Assessment already completed! Say 'show results' to see your performance."
        
        current_question = session['questions'][current_idx]
        
        # Extract answer based on question type
        if hasattr(current_question, 'title'):  # DSA Question
            # For DSA, extract code or approach after "submit answer"
            if 'submit answer' in query_lower:
                answer = query[query_lower.find('submit answer') + 13:].strip()
            else:
                answer = query.strip()
        else:  # MCQ Question
            # Extract option (A, B, C, D)
            import re
            option_match = re.search(r'\b([ABCD])\b', query.upper())
            if option_match:
                # Convert A,B,C,D to actual option IDs
                option_letter = option_match.group(1)
                option_map = {'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd'}
                answer = option_map.get(option_letter, 'a')
            else:
                return "❓ Please specify your answer (A, B, C, or D). Example: 'submit answer B'"
        
        # Submit answer
        result = self.assessment_engine.submit_answer(
            session['config'].assessment_id,
            current_question.id,
            answer
        )
        
        if 'error' in result:
            return f"❌ Error: {result['error']}"
        
        # Format response
        if result.get('completed'):
            return f"""
🎉 **Assessment Completed!**

✅ **Final Results:**
• **Total Score**: {result['total_score']:.1f}
• **Percentage**: {result['percentage']:.1f}%
• **Status**: {'✅ PASSED' if result['passed'] else '❌ NEEDS IMPROVEMENT'}
• **Time Taken**: {result['time_taken']}

🎯 **Performance Analysis:**

**Strengths** 💪:
{chr(10).join(['• ' + strength for strength in result.get('strengths', ['Great effort!'])])}

**Areas for Improvement** 📚:
{chr(10).join(['• ' + weakness for weakness in result.get('weaknesses', [])])}

**Recommendations** 💡:
{chr(10).join(['• ' + rec for rec in result.get('recommendations', [])])}

🚀 Want to practice more? Say "create new assessment" or "DSA practice"!
"""
        
        else:
            # Show result for current question and next question
            next_q_num = session['current_question'] + 1
            total_q = len(session['questions'])
            
            response = f"""
{'✅' if result['correct'] else '❌'} **Answer {'Correct' if result['correct'] else 'Incorrect'}** 
Score: {result['score']:.1f}/1.0

📊 **Progress**: Question {next_q_num}/{total_q} ({result['progress']['current']}/{result['progress']['total']})

"""
            
            # Add next question
            if 'next_question' in result:
                response += "\n" + self._format_question_display(
                    type('Question', (), result['next_question'])(), 
                    next_q_num, 
                    total_q
                )
            
            return response
    
    def _provide_hint(self, session: Dict) -> str:
        """Provide hint for current question"""
        
        current_idx = session['current_question']
        if current_idx >= len(session['questions']):
            return "🎉 Assessment completed! No more questions."
        
        current_question = session['questions'][current_idx]
        
        if hasattr(current_question, 'hints') and current_question.hints:
            hint = current_question.hints[0]  # Show first hint
            return f"""
💡 **Hint for Current Question:**

{hint}

🧠 **Think About:**
• What data structure would be most efficient?
• Can you solve this step by step?
• Are there any edge cases to consider?

Ready to submit? Say "submit answer [your solution]"
"""
        
        else:
            return "💭 No specific hints available for this question, but here are some general tips:\n\n• Break the problem into smaller parts\n• Consider the constraints and edge cases\n• Think about time and space complexity\n• Start with a simple approach, then optimize"

# Create assessment agent instance
def AssessmentAgent(query: str) -> str:
    """Main function to handle assessment queries"""
    agent = AssessmentAgent()
    return agent.process_query(query)