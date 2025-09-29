"""
🎯 Interview Helper Agent
Main orchestrator for the 4-Phase Interview Helper System

This agent coordinates:
Phase 1: Company Intelligence & Training
Phase 2: Resume Building & Optimization  
Phase 3: Assessment & Screening Tests
Phase 4: AI Interview Simulator

Integrates with NEXUS for natural language interaction
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Import our custom modules
from .CompanyIntelligenceEngine import CompanyIntelligenceEngine, JobRequirement, SkillAnalysis, LearningRoadmap
from .TrainingModulesSystem import TrainingModulesSystem, SubjectType, Difficulty, Problem, UserProgress
from .ResumeBuilder import ResumeBuilder, ResumeTemplate, ResumeData, ResumeOptimization
from .AssessmentAgent import AssessmentAgent

class InterviewPhase(Enum):
    COMPANY_INTELLIGENCE = "Company Intelligence & Training"
    RESUME_BUILDING = "Resume Building & Optimization"
    ASSESSMENTS = "Assessment & Screening Tests"
    AI_INTERVIEW = "AI Interview Simulator"

@dataclass
class InterviewSession:
    """Track user's interview preparation session"""
    session_id: str
    user_id: str
    target_company: str
    target_role: str
    current_phase: InterviewPhase
    created_at: datetime
    last_activity: datetime
    progress_data: Dict[str, Any]
    skills_analysis: Optional[SkillAnalysis] = None
    learning_roadmap: Optional[LearningRoadmap] = None

class InterviewHelperAgent:
    """
    🤖 Main Interview Helper Agent
    
    Coordinates all phases of interview preparation with natural language interaction
    """
    
    def __init__(self):
        # Initialize component systems
        self.company_intelligence = CompanyIntelligenceEngine()
        self.training_system = TrainingModulesSystem()
        self.resume_builder = ResumeBuilder()
        self.assessment_agent = AssessmentAgent()
        
        # Session management
        self.active_sessions = {}
        self.session_counter = 0
        
        # Data storage paths
        self.data_dir = os.path.join("Data", "InterviewHelper")
        os.makedirs(self.data_dir, exist_ok=True)
        
        print("🎯 Interview Helper Agent initialized successfully!")
    
    def handle_natural_language_request(self, user_id: str, query: str) -> str:
        """
        🗣️ Process natural language requests for interview preparation
        
        Args:
            user_id: User identifier
            query: Natural language query
            
        Returns:
            Formatted response string
        """
        
        query_lower = query.lower().strip()
        
        # Detect intent based on keywords
        if any(keyword in query_lower for keyword in ["prepare", "interview", "company", "job", "role"]):
            return self._handle_interview_prep_request(user_id, query)
        
        elif any(keyword in query_lower for keyword in ["practice", "solve", "problem", "dsa", "coding"]):
            return self._handle_practice_request(user_id, query)
        
        elif any(keyword in query_lower for keyword in ["resume", "cv", "build", "optimize"]):
            return self._handle_resume_request(user_id, query)
        
        elif any(keyword in query_lower for keyword in ["test", "assessment", "quiz", "mock", "challenge", "screen", "coding practice"]):
            return self._handle_assessment_request(user_id, query)
        
        elif any(keyword in query_lower for keyword in ["progress", "analytics", "stats", "performance"]):
            return self._handle_progress_request(user_id, query)
        
        else:
            return self._get_help_message()
    
    def _handle_interview_prep_request(self, user_id: str, query: str) -> str:
        """Handle interview preparation setup requests"""
        
        # Extract company and role from query
        company, role = self._extract_company_and_role(query)
        
        if not company or not role:
            return """🎯 **Let's start your interview preparation!**
            
Please provide:
• **Company name**: Which company are you targeting?
• **Role/Position**: What position are you applying for?

**Example**: "I want to prepare for Software Engineer at Google"
**Example**: "Help me prepare for Data Scientist role at Microsoft"
"""
        
        # Create new interview session
        session = self._create_interview_session(user_id, company, role)
        
        # Start Phase 1: Company Intelligence
        return self._start_company_intelligence_phase(session)
    
    def _create_interview_session(self, user_id: str, company: str, role: str) -> InterviewSession:
        """Create a new interview preparation session"""
        
        self.session_counter += 1
        session_id = f"interview_{user_id}_{self.session_counter}"
        
        session = InterviewSession(
            session_id=session_id,
            user_id=user_id,
            target_company=company,
            target_role=role,
            current_phase=InterviewPhase.COMPANY_INTELLIGENCE,
            created_at=datetime.now(),
            last_activity=datetime.now(),
            progress_data={}
        )
        
        self.active_sessions[session_id] = session
        return session
    
    def _start_company_intelligence_phase(self, session: InterviewSession) -> str:
        """Start Phase 1: Company Intelligence & Training"""
        
        try:
            # Search for job requirements
            print(f"🔍 Researching {session.target_role} at {session.target_company}...")
            job_requirements = self.company_intelligence.search_job_requirements(
                session.target_company, 
                session.target_role
            )
            
            # Get company insights
            company_insights = self.company_intelligence.get_company_insights(session.target_company)
            
            response = f"""🎯 **Interview Preparation Started!**

**Target**: {session.target_role} at {session.target_company}
**Session ID**: {session.session_id}

## 🔍 **Phase 1: Company Intelligence & Research**

### 📊 **Job Market Analysis**
• Found **{len(job_requirements)}** relevant job postings
• Analyzing skill requirements and trends
• Identifying key competencies for this role

### 🏢 **Company Insights for {session.target_company}**
• **Culture**: {company_insights.get('culture', 'Innovation-focused')}
• **Interview Process**: {len(company_insights.get('interview_rounds', []))} typical rounds
• **Key Skills**: {', '.join(company_insights.get('key_skills', [])[:4])}

### 📝 **Next Steps**:
1. **Skill Analysis**: Tell me your current skills to identify gaps
2. **Learning Roadmap**: Get personalized study plan
3. **Training Modules**: Start with DSA and core subjects

**How to continue**:
• "My skills are: Python, JavaScript, SQL, Git"
• "Start skill analysis"
• "Show me the learning roadmap"
"""
            
            # Store job requirements in session
            session.progress_data['job_requirements'] = [asdict(job) for job in job_requirements]
            session.progress_data['company_insights'] = company_insights
            
            return response
            
        except Exception as e:
            return f"❌ Error starting company intelligence phase: {e}"
    
    def _extract_company_and_role(self, query: str) -> Tuple[str, str]:
        """Extract company name and role from natural language query"""
        
        query_lower = query.lower()
        
        # Common company names
        companies = [
            "google", "microsoft", "amazon", "apple", "meta", "facebook", 
            "netflix", "uber", "airbnb", "spotify", "twitter", "linkedin",
            "adobe", "salesforce", "oracle", "ibm", "intel", "nvidia"
        ]
        
        # Common role keywords
        roles = [
            "software engineer", "data scientist", "product manager",
            "frontend developer", "backend developer", "full stack developer",
            "devops engineer", "machine learning engineer", "data analyst",
            "software developer", "web developer", "mobile developer"
        ]
        
        # Find company
        found_company = ""
        for company in companies:
            if company in query_lower:
                found_company = company.title()
                break
        
        # Find role
        found_role = ""
        for role in roles:
            if role in query_lower:
                found_role = role.title()
                break
        
        return found_company, found_role
    
    def _handle_practice_request(self, user_id: str, query: str) -> str:
        """Handle practice and problem-solving requests"""
        
        query_lower = query.lower()
        
        # Determine subject type
        if any(keyword in query_lower for keyword in ["array", "string", "tree", "graph", "dp", "dynamic", "algorithm", "dsa"]):
            subject_type = SubjectType.DSA
            
            # Extract topic if specified
            topic = "Arrays"  # Default
            if "tree" in query_lower:
                topic = "Trees & Binary Search Trees"
            elif "graph" in query_lower:
                topic = "Graphs"
            elif "dp" in query_lower or "dynamic" in query_lower:
                topic = "Dynamic Programming"
            elif "linked" in query_lower:
                topic = "Linked Lists"
            
        elif any(keyword in query_lower for keyword in ["database", "sql", "dbms"]):
            subject_type = SubjectType.DBMS
            topic = "SQL"
            
        elif any(keyword in query_lower for keyword in ["aptitude", "quantitative", "logical"]):
            subject_type = SubjectType.APTITUDE
            topic = "Quantitative"
            
        else:
            subject_type = SubjectType.DSA
            topic = "Arrays"
        
        # Get problems
        problems = self.training_system.get_problems_by_topic(subject_type, topic, limit=5)
        
        if not problems:
            return f"❌ No problems found for {topic} in {subject_type.value}"
        
        # Format response with problems
        response = f"📝 **{subject_type.value} - {topic} Practice**\n\n"
        
        for i, problem in enumerate(problems, 1):
            response += f"**{i}. {problem.title}** ({problem.difficulty.value})\n"
            response += f"   {problem.description[:150]}...\n"
            if problem.companies:
                response += f"   🏢 **Asked by**: {', '.join(problem.companies[:3])}\n"
            response += "\n"
        
        response += "**How to proceed**:\n"
        response += "• \"Show me problem 1\" - Get full problem details\n"
        response += "• \"I want to solve Two Sum\" - Start solving specific problem\n"
        response += "• \"Generate personalized practice set\" - Get curated problems\n"
        
        return response
    
    def _handle_resume_request(self, user_id: str, query: str) -> str:
        """Handle resume building requests"""
        
        query_lower = query.lower()
        
        # Check for specific resume actions
        if any(keyword in query_lower for keyword in ["build", "create", "generate", "new"]):
            return self._start_resume_building(user_id, query)
        
        elif any(keyword in query_lower for keyword in ["optimize", "improve", "enhance", "analyze", "upload", "existing"]):
            return self._optimize_existing_resume(user_id, query)
        
        elif any(keyword in query_lower for keyword in ["template", "john doe", "format", "style"]):
            return self._show_resume_templates(user_id)
        
        elif any(keyword in query_lower for keyword in ["example", "sample", "demo"]):
            return self._show_resume_examples(user_id)
        
        else:
            return self._show_resume_help_menu()
    
    def _start_resume_building(self, user_id: str, query: str) -> str:
        """Start the resume building process"""
        
        # Extract role and company if mentioned
        company, role = self._extract_company_and_role(query)
        
        return f"""📄 **Resume Builder - John Doe Templates**

Let's create your professional resume! Choose your preferred template:

### 🎨 **Available John Doe Templates**:

**1. 📋 John Doe Classic** - Clean, professional, ATS-friendly
   Perfect for: Traditional industries, corporate roles

**2. 💻 John Doe Tech** - Technical focus, skills-emphasized
   Perfect for: Software engineering, IT roles

**3. ✨ John Doe Modern** - Contemporary design with visual elements
   Perfect for: Creative roles, startups, modern companies

**4. 👔 John Doe Executive** - Leadership-focused, achievement-oriented
   Perfect for: Senior roles, management positions

### 📝 **Information Needed**:
• Personal details (name, contact, location)
• Work experience and achievements
• Education background
• Technical skills and certifications
• Projects and portfolio links

**Examples**:
• "Create resume using John Doe Classic template for Software Engineer at Google"
• "Build tech resume for Amazon"
• "Generate modern resume for designer role"

{'**Target**: ' + role + ' at ' + company if company and role else '**Next**: Choose a template or provide your details'}
"""
    
    def _optimize_existing_resume(self, user_id: str, query: str) -> str:
        """Optimize an existing resume"""
        
        query_lower = query.lower()
        
        # Check for specific optimization requests
        if any(keyword in query_lower for keyword in ["paste", "content", "text"]):
            return self._handle_resume_content_analysis(user_id, query)
        
        elif any(keyword in query_lower for keyword in ["upload", "file", "pdf", "docx"]):
            return self._handle_resume_file_upload(user_id, query)
        
        elif any(keyword in query_lower for keyword in ["convert", "template", "ats friendly"]):
            return self._handle_resume_conversion(user_id, query)
        
        else:
            return """🔍 **Resume Optimization & Analysis**

I'll help optimize your existing resume for maximum impact and ATS compatibility!

### 🚀 **What I Can Do**:

� **Analyze Your Current Resume**
• Parse and extract data from your resume
• Identify formatting and content issues
• Calculate ATS compatibility score
• Provide detailed improvement suggestions

🔄 **Convert to ATS-Friendly Templates**
• Transform your resume using John Doe templates
• Maintain your content while improving format
• Optimize for applicant tracking systems
• Enhance keyword matching for target roles

�📊 **Advanced Optimization**
• Role-specific keyword optimization
• Achievement quantification suggestions
• Skills alignment with job requirements  
• Company-specific customization

### 📁 **How to Get Started**:

**Option 1 - Paste Resume Content**: 
"Analyze this resume: [paste your resume text]"

**Option 2 - Upload File**:
"I want to upload my resume file" (PDF/DOCX support)

**Option 3 - Convert to Template**:
"Convert my resume to John Doe Classic template"

**Option 4 - Role-Specific Optimization**:
"Optimize my resume for Software Engineer at Google"

### 🎯 **Popular Commands**:
• "Analyze my resume for ATS compatibility"
• "Convert my resume to tech template"
• "Show me improvement suggestions"
• "Optimize for [role] at [company]"

**Ready to enhance your resume?** Choose an option above or tell me what you need help with!
"""
    
    def _handle_resume_content_analysis(self, user_id: str, query: str) -> str:
        """Handle pasted resume content analysis"""
        
        return """📝 **Resume Content Analysis Ready**

Please paste your resume content below, and I'll provide comprehensive analysis:

### 🔍 **What I'll Analyze**:
• **ATS Compatibility Score** - How well your resume passes through ATS systems
• **Content Structure** - Section organization and completeness
• **Keyword Optimization** - Role-specific keyword matching
• **Achievement Quantification** - Opportunities to add metrics
• **Formatting Issues** - Problems that might hurt ATS parsing

### 📊 **Analysis Report Includes**:
• Overall assessment with scores
• Specific improvement recommendations
• Missing keywords for your target role
• Content gaps and how to fill them
• Template conversion recommendations

### 📋 **How to Submit**:
1. Copy your entire resume text
2. Paste it in your next message
3. Optionally specify target role: "for Software Engineer position"

**Example Format**:
```
"Analyze this resume for Data Scientist role:

John Doe
john.doe@email.com
[your complete resume content here...]"
```

**Ready when you are!** Paste your resume content and I'll provide detailed analysis.
"""
    
    def _handle_resume_file_upload(self, user_id: str, query: str) -> str:
        """Handle resume file upload requests"""
        
        return """📁 **Resume File Upload & Processing**

I can help you process resume files for optimization and conversion!

### � **Supported Formats**:
• **PDF Files** - Most common resume format
• **DOCX Files** - Microsoft Word documents  
• **TXT Files** - Plain text resumes
• **HTML Files** - Web-formatted resumes

### 🔄 **Processing Capabilities**:
• **Intelligent Parsing** - Extract text and structure from files
• **Content Analysis** - Comprehensive resume evaluation
• **Template Conversion** - Transform to John Doe templates
• **ATS Optimization** - Improve compatibility scores

### 📋 **Upload Process**:

**Step 1**: Prepare your resume file
**Step 2**: Use one of these methods:

**Method A - Copy-Paste Text**:
"Analyze this resume: [paste extracted text]"

**Method B - Describe Content**:
"I have a software engineer resume with 5 years experience, Python skills, worked at Google and Microsoft"

**Method C - Upload via File System** (if available):
Drag and drop your file or use file browser

### 🎯 **After Upload, I Can**:
• Parse and analyze your resume content
• Convert to any John Doe template
• Optimize for specific roles/companies
• Generate improvement suggestions
• Create ATS-friendly versions

### 💡 **Pro Tip**:
For best results, copy-paste your resume text directly. This ensures accurate parsing and analysis.

**Ready to proceed?** Share your resume content in any format above!
"""
    
    def _handle_resume_conversion(self, user_id: str, query: str) -> str:
        """Handle resume template conversion requests"""
        
        # Extract target template from query
        target_template = "John Doe Classic"  # Default
        
        if "tech" in query.lower():
            target_template = "John Doe Tech"
        elif "modern" in query.lower():
            target_template = "John Doe Modern" 
        elif "executive" in query.lower():
            target_template = "John Doe Executive"
        
        return f"""🔄 **Resume Template Conversion**

I'll convert your existing resume to the **{target_template}** template!

### ✨ **Conversion Benefits**:
• **ATS-Friendly Formatting** - Optimized for applicant tracking systems
• **Professional Structure** - Industry-standard section organization
• **Enhanced Readability** - Clean, modern design
• **Keyword Optimization** - Role-specific improvements
• **Achievement Highlighting** - Better presentation of accomplishments

### 🎨 **{target_template} Features**:
{self._get_template_description(target_template)}

### 📋 **Conversion Process**:

**Step 1**: Share your current resume
- Paste resume text, or
- Describe your background, or  
- Upload file content

**Step 2**: Specify target role (optional)
- "for Software Engineer at Google"
- "targeting Data Scientist positions"

**Step 3**: Get converted resume
- Formatted in {target_template} style
- Optimized for ATS compatibility
- Enhanced with role-specific keywords

### 🔄 **Conversion Options**:
• "Convert to John Doe Classic" - Traditional, professional
• "Convert to John Doe Tech" - Technical roles focus
• "Convert to John Doe Modern" - Contemporary design
• "Convert to John Doe Executive" - Leadership emphasis

### 📊 **You'll Receive**:
• **Before/After Analysis** - Improvement metrics
• **Converted Resume** - Ready-to-use format
• **Optimization Report** - What was enhanced
• **Customization Suggestions** - Role-specific tips

**Ready to convert?** Share your current resume content and any specific requirements!
"""
    
    def _show_resume_templates(self, user_id: str) -> str:
        """Show available John Doe resume templates with examples"""
        
        return """🎨 **John Doe Resume Templates Gallery**

### 📋 **1. John Doe Classic Template**
```
JOHN DOE
john.doe@email.com | +1 (555) 123-4567 | San Francisco, CA
LinkedIn: linkedin.com/in/johndoe | GitHub: github.com/johndoe

PROFESSIONAL SUMMARY
Experienced Software Engineer with 5+ years developing scalable web 
applications. Proven track record of delivering high-quality code...

TECHNICAL SKILLS
Languages: Python, JavaScript, Java, SQL
Tools & Frameworks: React, Django, AWS, Docker
```

### 💻 **2. John Doe Tech Template**
```
JOHN DOE
Software Engineer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TECHNICAL EXPERTISE
Programming Languages: Python, JavaScript, Java
Frameworks & Libraries: React, Django, Express
Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins
```

### ✨ **3. John Doe Modern Template**
```
════════════════════════════════════════════════════════════════
                    JOHN DOE
                 Software Engineer
════════════════════════════════════════════════════════════════
📧 john.doe@email.com  📱 +1 (555) 123-4567  📍 San Francisco, CA

CORE COMPETENCIES
▪ Python    ▪ React      ▪ AWS       ▪ Docker
▪ JavaScript ▪ Node.js   ▪ SQL       ▪ Git
```

### 👔 **4. John Doe Executive Template**
```
JOHN DOE
Senior Engineering Manager

EXECUTIVE SUMMARY
Senior executive with 10+ years of leadership experience driving 
organizational growth and digital transformation...

KEY ACHIEVEMENTS
• Led engineering teams of 50+ developers across 5 product lines
• Delivered $10M+ in cost savings through cloud migration
• Increased development velocity by 300% through process optimization
```

**Ready to build?** Choose: "Create resume with John Doe Classic template"
"""
    
    def _show_resume_examples(self, user_id: str) -> str:
        """Show resume examples for different roles"""
        
        return """📖 **Resume Examples by Role**

### 👨‍💻 **Software Engineer Resume (John Doe Tech)**
**Target**: Senior Software Engineer at Google
**Template**: John Doe Tech Template
**Highlights**: Technical skills emphasis, quantified achievements
**ATS Score**: 92/100

### 👩‍🔬 **Data Scientist Resume (John Doe Classic)**
**Target**: Data Scientist at Microsoft
**Template**: John Doe Classic Template  
**Highlights**: Machine learning projects, statistical analysis
**ATS Score**: 88/100

### 🎨 **Product Designer Resume (John Doe Modern)**
**Target**: UX Designer at Meta
**Template**: John Doe Modern Template
**Highlights**: Design systems, user research, portfolio links
**ATS Score**: 90/100

### 👔 **Engineering Manager Resume (John Doe Executive)**
**Target**: VP of Engineering at Startup
**Template**: John Doe Executive Template
**Highlights**: Leadership achievements, team scaling, business impact
**ATS Score**: 94/100

### 🔍 **Want to See Full Examples?**
• "Show me software engineer resume example"
• "Generate sample data scientist resume"
• "Create demo resume for product manager"

**Ready to start?** Choose a template and role for your custom resume!
"""
    
    def _show_resume_help_menu(self) -> str:
        """Show resume building help menu"""
        
        return """📄 **Resume Building & Optimization** (Phase 2)

### ✨ **What I Can Help You With**:

🏗️ **Build New Resume**
• Create from John Doe templates
• Role-specific customization
• ATS-friendly formatting

🔍 **Optimize Existing Resume**
• ATS compatibility analysis
• Keyword optimization
• Achievement quantification

🎨 **Templates & Examples**
• John Doe template showcase
• Role-specific examples
• Best practice guidelines

### 🚀 **Quick Commands**:
• "Create resume using John Doe Classic template"
• "Optimize my resume for Software Engineer"
• "Show me resume templates"
• "Generate example resume for Data Scientist"

### 🎯 **Pro Tips**:
• Use quantified achievements (e.g., "Improved performance by 40%")
• Include relevant keywords for your target role
• Keep format clean and ATS-friendly
• Tailor content for each application

**What would you like to do?** Choose an option above or ask me anything about resume building!
"""
    
    def _handle_assessment_request(self, user_id: str, query: str) -> str:
        """Handle assessment and test requests - Phase 3"""
        
        try:
            # Use the Assessment Agent to handle the query
            response = self.assessment_agent.process_query(query)
            
            # Add session context if available
            user_sessions = [s for s in self.active_sessions.values() if s.user_id == user_id]
            if user_sessions:
                latest_session = max(user_sessions, key=lambda s: s.last_activity)
                
                # Add context about the user's preparation
                context_info = f"""
🎯 **Your Preparation Context**:
• **Target Company**: {latest_session.target_company}
• **Target Role**: {latest_session.target_role}
• **Current Phase**: {latest_session.current_phase.value}

"""
                response = context_info + response
            
            return response
            
        except Exception as e:
            return f"""
🧪 **Assessment & Screening Tests - Phase 3**

✅ **Now Available!** Our comprehensive assessment system includes:

### 🎯 **Assessment Types**:
• **DSA Coding Challenges** - Algorithm implementation and problem-solving
• **Technical MCQs** - Programming concepts, system design, databases
• **Aptitude Tests** - Quantitative reasoning, logical puzzles, verbal ability
• **Company-Specific Tests** - Customized based on company patterns

### 🚀 **Quick Start**:
• "Create assessment for Software Engineer at Google"
• "Start DSA practice on arrays"
• "Technical MCQ practice"
• "Show assessment options"

### ⚡ **Features**:
• ⏰ Timed test environments simulating real interviews
• 📊 Real-time progress tracking and performance analytics
• 💡 Intelligent hints and detailed explanations
• 🎯 Adaptive difficulty based on your experience level

**Error occurred**: {str(e)}
**Try**: "assessment info" or "create assessment for [role] at [company]"
"""
    
    def _handle_progress_request(self, user_id: str, query: str) -> str:
        """Handle progress and analytics requests"""
        
        # Get user progress from training system
        analytics = self.training_system.get_progress_analytics(user_id)
        
        if "error" in analytics:
            return """📊 **Your Progress Dashboard**

🌟 **Just Getting Started!**

No activity recorded yet. Here's how to begin:

### 🎯 **Start Your Journey**:
1. **Company Research**: "Prepare for Software Engineer at Google"
2. **Practice Problems**: "Show me array problems"
3. **Study Concepts**: "Learn DBMS concepts"

### 📈 **Track Your Progress**:
• Problems solved across different topics
• Time spent learning each subject
• Accuracy scores and improvement trends
• Achievement badges and streaks

**Get Started**: "I want to practice DSA problems"
"""
        
        # Format progress analytics
        response = f"""📊 **Your Progress Dashboard**

### 🎯 **Overall Progress**:
• **Problems Solved**: {analytics['total_problems_solved']}
• **Current Streak**: {analytics['current_streak']} days
• **Total Study Time**: {analytics['total_time_spent']} minutes
• **Achievements**: {len(analytics['achievements'])} badges earned

### 📈 **Subject Breakdown**:
"""
        
        for subject, data in analytics['subject_breakdown'].items():
            response += f"**{subject}**:\n"
            response += f"   • Problems: {data['problems_solved']}\n"
            response += f"   • Time: {data['time_spent']} min\n"
            response += f"   • Accuracy: {data['accuracy']}%\n\n"
        
        if analytics['achievements']:
            response += f"### 🏆 **Recent Achievements**:\n"
            for achievement in analytics['achievements'][-3:]:  # Last 3 achievements
                response += f"• {achievement.replace('_', ' ').title()}\n"
        
        response += "\n**Continue Learning**: \"Show me personalized practice problems\""
        
        return response
    
    def create_resume_with_template(self, user_data: Dict[str, Any], template: str, target_role: str = None, target_company: str = None) -> str:
        """Create a resume using the specified John Doe template"""
        
        # Map template name to enum
        template_mapping = {
            "classic": ResumeTemplate.JOHN_DOE_CLASSIC,
            "tech": ResumeTemplate.JOHN_DOE_TECH,
            "modern": ResumeTemplate.JOHN_DOE_MODERN,
            "executive": ResumeTemplate.JOHN_DOE_EXECUTIVE,
            "john doe classic": ResumeTemplate.JOHN_DOE_CLASSIC,
            "john doe tech": ResumeTemplate.JOHN_DOE_TECH,
            "john doe modern": ResumeTemplate.JOHN_DOE_MODERN,
            "john doe executive": ResumeTemplate.JOHN_DOE_EXECUTIVE
        }
        
        template_enum = template_mapping.get(template.lower(), ResumeTemplate.JOHN_DOE_CLASSIC)
        
        # Generate resume
        resume = self.resume_builder.create_resume_from_template(
            template_enum,
            user_data,
            target_role,
            target_company
        )
        
        # Optimize for role if provided
        if target_role:
            optimization = self.resume_builder.optimize_resume_for_role(resume, target_role)
            
            result = f"""📄 **Resume Generated Successfully!**

### 🎨 **Template**: {template_enum.value}
### 🎯 **Target**: {target_role or 'General'}{' at ' + target_company if target_company else ''}

### 📊 **Optimization Analysis**:
• **ATS Score**: {optimization.ats_score}/100
• **Keyword Match**: {optimization.keyword_match_score}%
• **Role Alignment**: {optimization.role_alignment_score}/100

### 💪 **Strengths**:
{chr(10).join(['• ' + strength for strength in optimization.strengths[:3]])}

### 💡 **Suggestions for Improvement**:
{chr(10).join(['• ' + suggestion for suggestion in optimization.suggested_improvements[:3]])}

### 📝 **Your Resume**:
```
{resume}
```

**Next Steps**:
• Save this resume to a file
• Further customize for specific applications  
• Generate cover letter to match
• "Optimize resume for [specific role]"
"""
            return result
        
        return f"""📄 **Resume Generated Successfully!**

### 🎨 **Template**: {template_enum.value}

### 📝 **Your Resume**:
```
{resume}
```

**Enhance Further**:
• "Optimize this resume for [role] at [company]"
• "Generate cover letter for this resume"
• "Show ATS analysis for this resume"
"""
    
    def analyze_resume_for_ats(self, resume_content: str, target_role: str = None) -> str:
        """Analyze resume for ATS compatibility and optimization"""
        
        if not target_role:
            target_role = "Software Engineer"  # Default role
        
        optimization = self.resume_builder.optimize_resume_for_role(resume_content, target_role)
        
        return f"""🔍 **Resume ATS Analysis Report**

### 📊 **Overall Scores**:
• **ATS Compatibility**: {optimization.ats_score}/100
• **Keyword Match**: {optimization.keyword_match_score}%
• **Role Alignment**: {optimization.role_alignment_score}/100

### 💪 **Strengths** ({len(optimization.strengths)} identified):
{chr(10).join(['• ' + strength for strength in optimization.strengths])}

### ⚠️ **Areas for Improvement** ({len(optimization.weaknesses)} identified):
{chr(10).join(['• ' + weakness for weakness in optimization.weaknesses])}

### 🔑 **Missing Keywords** (Top 10):
{', '.join(optimization.missing_keywords[:10])}

### 💡 **Actionable Recommendations**:
{chr(10).join(['• ' + suggestion for suggestion in optimization.suggested_improvements])}

### 🎯 **Next Steps**:
• Add missing keywords naturally to your experience descriptions
• Quantify achievements with specific numbers and percentages
• Use action verbs that align with the target role
• Ensure consistent formatting for ATS parsing

**Need help implementing these changes?** Ask me: "Help me add [specific keyword] to my resume"
"""
    
    def process_uploaded_resume(self, resume_content: str, target_role: str = None, conversion_template: str = None) -> str:
        """Process uploaded resume content and provide analysis/conversion"""
        
        if not resume_content or len(resume_content.strip()) < 100:
            return "❌ **Invalid Resume Content** - Please provide a complete resume with at least 100 characters."
        
        try:
            # Analyze existing resume
            print("🔍 Analyzing uploaded resume...")
            analysis = self.resume_builder.parse_existing_resume(resume_content)
            suggestions = self.resume_builder.suggest_resume_improvements(resume_content, target_role)
            
            response = f"""📊 **Resume Analysis Complete!**

### 📋 **Parsing Results**:
• **Confidence**: {analysis.parsing_confidence:.1f}%
• **Detected Sections**: {', '.join(analysis.detected_sections)}
• **ATS Readiness**: {analysis.ats_readiness:.1f}/100

### 🎯 **Overall Assessment**:
• **ATS Score**: {suggestions['overall_assessment']['ats_score']:.1f}/100
• **Keyword Match**: {suggestions['overall_assessment']['keyword_match']:.1f}%
• **Role Alignment**: {suggestions['overall_assessment']['role_alignment']:.1f}/100

### ⚠️ **Issues Found**:
{chr(10).join(['• ' + issue for issue in analysis.formatting_issues[:3]])}
{chr(10).join(['• ' + gap for gap in analysis.content_gaps[:3]])}

### 💡 **Top Improvement Suggestions**:
{chr(10).join(['• ' + suggestion for suggestion in suggestions['ai_suggestions'][:3]])}

### 🔑 **Missing Keywords**:
{', '.join(suggestions['content_improvements']['missing_keywords'][:8])}
"""
            
            # If conversion requested, convert to template
            if conversion_template:
                template_map = {
                    "classic": ResumeTemplate.JOHN_DOE_CLASSIC,
                    "tech": ResumeTemplate.JOHN_DOE_TECH, 
                    "modern": ResumeTemplate.JOHN_DOE_MODERN,
                    "executive": ResumeTemplate.JOHN_DOE_EXECUTIVE
                }
                
                template_enum = template_map.get(conversion_template.lower(), ResumeTemplate.JOHN_DOE_CLASSIC)
                
                print(f"🔄 Converting to {template_enum.value}...")
                conversion = self.resume_builder.convert_to_ats_template(
                    resume_content, 
                    template_enum,
                    target_role,
                    "Target Company"
                )
                
                response += f"""

### 🔄 **Template Conversion Results**:

**Template Used**: {conversion.template_used.value}
**Conversion Success**: {'✅ Yes' if conversion.conversion_success else '❌ Needs Review'}

### 📈 **Before vs After Scores**:
• **ATS Score**: {conversion.before_scores.ats_score:.1f} → {conversion.after_scores.ats_score:.1f} (+{conversion.after_scores.ats_score - conversion.before_scores.ats_score:.1f})
• **Keywords**: {conversion.before_scores.keyword_match_score:.1f}% → {conversion.after_scores.keyword_match_score:.1f}% (+{conversion.after_scores.keyword_match_score - conversion.before_scores.keyword_match_score:.1f}%)
• **Role Alignment**: {conversion.before_scores.role_alignment_score:.1f} → {conversion.after_scores.role_alignment_score:.1f} (+{conversion.after_scores.role_alignment_score - conversion.before_scores.role_alignment_score:.1f})

### ✨ **Improvements Made**:
{chr(10).join(['• ' + improvement for improvement in conversion.improvements_made[:5]])}

### 📄 **Your Optimized Resume**:
```
{conversion.converted_resume}
```
"""
            
            response += f"""

### 🎯 **Recommended Next Steps**:
{chr(10).join(['• ' + step for step in suggestions['next_steps'][:4]])}

**Need more help?** Try:
• "Convert my resume to John Doe Tech template"
• "Optimize this resume for [specific role]"
• "Show me more improvement suggestions"
"""
            
            return response
            
        except Exception as e:
            return f"""❌ **Analysis Error**: {str(e)}

### 🔧 **Troubleshooting**:
• Ensure resume content is complete and properly formatted
• Try copying text directly from your resume file
• Check that the resume contains standard sections (experience, education, skills)

**Need help?** Try pasting a smaller section first or ask for formatting guidance.
"""
    
    def _get_template_description(self, template_name: str) -> str:
        """Get description of a specific template"""
        
        descriptions = {
            "John Doe Classic": """
• **Clean Professional Layout** - Traditional format preferred by most ATS systems
• **Balanced Sections** - Equal emphasis on experience, skills, and education
• **High ATS Compatibility** - 95%+ parsing success rate
• **Industry Versatile** - Works well for all industries and roles""",
            
            "John Doe Tech": """
• **Technical Skills Emphasis** - Prominent display of programming languages and tools
• **Project-Focused** - Dedicated section for technical projects and achievements
• **Developer-Friendly** - Optimized for software engineering and IT roles
• **GitHub Integration** - Highlights code repositories and technical contributions""",
            
            "John Doe Modern": """
• **Contemporary Design** - Visual elements and modern formatting
• **Creative Industries** - Perfect for design, marketing, and startup roles
• **Visual Hierarchy** - Icons and formatting enhance readability
• **Stand-Out Appeal** - Memorable design while maintaining professionalism""",
            
            "John Doe Executive": """
• **Leadership Focus** - Emphasizes management experience and business impact
• **Achievement-Oriented** - Highlights quantified business results
• **Executive Summary** - Prominent leadership profile section
• **Senior Roles** - Optimized for director, VP, and C-level positions"""
        }
        
        return descriptions.get(template_name, descriptions["John Doe Classic"])
    
    def _get_help_message(self) -> str:
        """Get help message with available commands"""
        
        return """🎯 **Interview Helper - Your Personal Career Coach**

## 🚀 **4-Phase Interview Preparation System**:

### **Phase 1: Company Intelligence & Training** 🔍
• Research target companies and roles
• Identify skill gaps and trending technologies  
• Get personalized learning roadmaps
• **Try**: "Prepare for Software Engineer at Google"

### **Phase 2: Resume Building** 📄 *(Coming Soon)*
• ATS-friendly resume templates
• Role-specific customization
• **Try**: "Help me build my resume"

### **Phase 3: Assessment Tests** 📝 *(Coming Soon)*  
• Company-specific screening simulations
• Technical MCQs and coding challenges
• **Try**: "Give me a mock test"

### **Phase 4: AI Interview Simulator** 🤖 *(Coming Soon)*
• Role-specific AI interviewer
• Performance metrics and feedback
• **Try**: "Start mock interview"

## 💡 **Available Now**:
• **"Prepare for [Role] at [Company]"** - Start interview prep
• **"Practice [Topic] problems"** - Solve coding problems
• **"Show my progress"** - View analytics dashboard
• **"Learn DBMS concepts"** - Study core CS subjects

**Ready to begin?** Just tell me which company and role you're targeting!
"""
    
    def get_session_info(self, session_id: str) -> Optional[InterviewSession]:
        """Get information about an active session"""
        return self.active_sessions.get(session_id)
    
    def list_active_sessions(self, user_id: str) -> List[InterviewSession]:
        """List all active sessions for a user"""
        return [session for session in self.active_sessions.values() if session.user_id == user_id]

# Integration function for NEXUS
def is_interview_helper_request(query: str) -> bool:
    """
    Check if a query is related to interview preparation
    
    Args:
        query: User's natural language query
        
    Returns:
        Boolean indicating if this is an interview helper request
    """
    
    interview_keywords = [
        "interview", "job", "career", "company", "role", "position",
        "prepare", "preparation", "practice", "resume", "cv",
        "coding", "algorithm", "dsa", "assessment", "test", "mock",
        "behavioral", "technical", "system design", "skills"
    ]
    
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in interview_keywords)

def handle_interview_helper_request(user_id: str, query: str) -> str:
    """
    Handle interview helper requests for NEXUS integration
    
    Args:
        user_id: User identifier
        query: Natural language query
        
    Returns:
        Formatted response string
    """
    
    # Create global instance (in real implementation, this would be managed better)
    global interview_helper_agent
    
    if 'interview_helper_agent' not in globals():
        interview_helper_agent = InterviewHelperAgent()
    
    return interview_helper_agent.handle_natural_language_request(user_id, query)

# Example usage and testing
if __name__ == "__main__":
    # Initialize the Interview Helper Agent
    agent = InterviewHelperAgent()
    
    print("🧪 Testing Interview Helper Agent")
    print("=" * 50)
    
    # Test various natural language requests
    test_queries = [
        "I want to prepare for Software Engineer at Google",
        "My skills are Python, JavaScript, SQL, React",
        "Show me array problems to practice",
        "What's my progress?",
        "Help me with my resume",
        "Give me a mock test"
    ]
    
    user_id = "test_user_123"
    
    for query in test_queries:
        print(f"\n🗣️ User: \"{query}\"")
        response = agent.handle_natural_language_request(user_id, query)
        print(f"🤖 Agent: {response[:200]}...")
        print("-" * 30)
    
    print("\n✅ Interview Helper Agent test completed!")