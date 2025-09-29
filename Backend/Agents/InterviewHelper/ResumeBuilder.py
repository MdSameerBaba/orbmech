"""
📄 Resume Building & Optimization Engine  
Phase 2 of the 4-Phase Interview Helper System

This module handles:
- ATS-friendly resume templates (including John Doe template)
- Role-specific resume customization based on job requirements
- Skills alignment with target positions
- Achievement quantification and impact statements
- Existing resume analysis and enhancement
- Cover letter generation
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from groq import Groq
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
GROQ_API_KEY = env_vars.get("GroqAPIKey")

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"❌ Failed to initialize Groq client: {e}")
    client = None

class ResumeTemplate(Enum):
    JOHN_DOE_CLASSIC = "John Doe Classic"
    JOHN_DOE_MODERN = "John Doe Modern" 
    JOHN_DOE_TECH = "John Doe Tech"
    JOHN_DOE_EXECUTIVE = "John Doe Executive"

class ExperienceLevel(Enum):
    ENTRY_LEVEL = "Entry Level (0-2 years)"
    MID_LEVEL = "Mid Level (3-5 years)"
    SENIOR_LEVEL = "Senior Level (6-10 years)"
    EXECUTIVE_LEVEL = "Executive Level (10+ years)"

@dataclass
class PersonalInfo:
    """Personal information for resume"""
    full_name: str
    email: str
    phone: str
    location: str
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    professional_summary: Optional[str] = None

@dataclass
class WorkExperience:
    """Work experience entry"""
    company: str
    position: str
    location: str
    start_date: str
    end_date: str
    is_current: bool
    responsibilities: List[str]
    achievements: List[str]
    technologies_used: List[str] = None

@dataclass
class Education:
    """Education entry"""
    institution: str
    degree: str
    field_of_study: str
    graduation_date: str
    gpa: Optional[str] = None
    relevant_coursework: List[str] = None
    honors: List[str] = None

@dataclass
class Project:
    """Project entry"""
    name: str
    description: str
    technologies: List[str]
    start_date: str
    end_date: Optional[str]
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    key_features: List[str] = None

@dataclass
class ResumeData:
    """Complete resume data structure"""
    personal_info: PersonalInfo
    work_experience: List[WorkExperience]
    education: List[Education]
    skills: List[str]
    projects: List[Project]
    certifications: List[str] = None
    languages: List[str] = None
    volunteer_work: List[str] = None

@dataclass
class ResumeOptimization:
    """Resume optimization analysis"""
    ats_score: float
    keyword_match_score: float
    missing_keywords: List[str]
    suggested_improvements: List[str]
    strengths: List[str]
    weaknesses: List[str]
    role_alignment_score: float

@dataclass
class ResumeAnalysis:
    """Comprehensive resume analysis"""
    extracted_data: ResumeData
    original_format: str
    parsing_confidence: float
    detected_sections: List[str]
    formatting_issues: List[str]
    content_gaps: List[str]
    ats_readiness: float

@dataclass
class ResumeConversion:
    """Resume conversion results"""
    original_resume: str
    converted_resume: str
    template_used: ResumeTemplate
    improvements_made: List[str]
    before_scores: ResumeOptimization
    after_scores: ResumeOptimization
    conversion_success: bool

class ResumeBuilder:
    """
    📄 Intelligent Resume Builder & Optimizer
    
    Creates ATS-friendly resumes with role-specific customization
    """
    
    def __init__(self):
        self.templates = self._initialize_templates()
        self.ats_keywords = self._load_ats_keywords()
        
        print("📄 Resume Builder initialized successfully!")
    
    def _initialize_templates(self) -> Dict[ResumeTemplate, Dict[str, Any]]:
        """Initialize resume templates with John Doe examples"""
        
        templates = {}
        
        # John Doe Classic Template
        templates[ResumeTemplate.JOHN_DOE_CLASSIC] = {
            "name": "John Doe Classic",
            "description": "Clean, professional template suitable for all industries",
            "sections": ["Header", "Professional Summary", "Work Experience", "Education", "Skills", "Projects"],
            "ats_friendly": True,
            "example_data": {
                "personal_info": PersonalInfo(
                    full_name="John Doe",
                    email="john.doe@email.com",
                    phone="+1 (555) 123-4567",
                    location="San Francisco, CA",
                    linkedin_url="linkedin.com/in/johndoe",
                    github_url="github.com/johndoe",
                    professional_summary="Experienced Software Engineer with 5+ years developing scalable web applications. Proven track record of delivering high-quality code and leading cross-functional teams to achieve project goals."
                ),
                "work_experience": [
                    WorkExperience(
                        company="Tech Innovators Inc.",
                        position="Senior Software Engineer",
                        location="San Francisco, CA",
                        start_date="Jan 2022",
                        end_date="Present",
                        is_current=True,
                        responsibilities=[
                            "Lead development of microservices architecture serving 1M+ users",
                            "Mentor junior developers and conduct code reviews",
                            "Collaborate with product managers to define technical requirements"
                        ],
                        achievements=[
                            "Reduced application load time by 40% through optimization",
                            "Led migration to cloud infrastructure, reducing costs by $50K annually",
                            "Implemented CI/CD pipeline improving deployment efficiency by 60%"
                        ],
                        technologies_used=["Python", "JavaScript", "React", "AWS", "Docker"]
                    ),
                    WorkExperience(
                        company="Digital Solutions LLC",
                        position="Software Engineer",
                        location="San Francisco, CA", 
                        start_date="Jun 2020",
                        end_date="Dec 2021",
                        is_current=False,
                        responsibilities=[
                            "Developed RESTful APIs using Python and Django",
                            "Built responsive web applications with React",
                            "Participated in agile development processes"
                        ],
                        achievements=[
                            "Delivered 15+ features ahead of schedule",
                            "Improved code coverage from 60% to 85%",
                            "Reduced bug reports by 30% through rigorous testing"
                        ],
                        technologies_used=["Python", "Django", "React", "PostgreSQL", "Git"]
                    )
                ]
            }
        }
        
        # John Doe Modern Template
        templates[ResumeTemplate.JOHN_DOE_MODERN] = {
            "name": "John Doe Modern",
            "description": "Contemporary design with visual elements, perfect for creative roles",
            "sections": ["Header", "Professional Summary", "Core Competencies", "Experience", "Education", "Projects", "Achievements"],
            "ats_friendly": True,
            "visual_elements": True
        }
        
        # John Doe Tech Template
        templates[ResumeTemplate.JOHN_DOE_TECH] = {
            "name": "John Doe Tech",
            "description": "Technical resume optimized for software engineering roles",
            "sections": ["Header", "Technical Skills", "Professional Experience", "Projects", "Education", "Certifications"],
            "ats_friendly": True,
            "tech_focused": True
        }
        
        # John Doe Executive Template
        templates[ResumeTemplate.JOHN_DOE_EXECUTIVE] = {
            "name": "John Doe Executive",
            "description": "Leadership-focused template for senior and executive positions",
            "sections": ["Header", "Executive Summary", "Leadership Experience", "Key Achievements", "Education", "Board Positions"],
            "ats_friendly": True,
            "executive_focused": True
        }
        
        return templates
    
    def _load_ats_keywords(self) -> Dict[str, List[str]]:
        """Load ATS-friendly keywords by role category"""
        
        return {
            "software_engineer": [
                "Python", "Java", "JavaScript", "React", "Node.js", "SQL", "Git",
                "Agile", "Scrum", "CI/CD", "Docker", "AWS", "API", "REST", "GraphQL",
                "Test-driven Development", "Code Review", "Debugging", "Optimization"
            ],
            "data_scientist": [
                "Python", "R", "SQL", "Machine Learning", "Deep Learning", "TensorFlow",
                "PyTorch", "Pandas", "NumPy", "Scikit-learn", "Statistics", "Data Visualization",
                "Tableau", "Power BI", "Big Data", "Hadoop", "Spark", "A/B Testing"
            ],
            "product_manager": [
                "Product Strategy", "Roadmap", "User Research", "A/B Testing", "Analytics",
                "Agile", "Scrum", "Stakeholder Management", "Go-to-Market", "KPIs",
                "User Experience", "Market Research", "Competitive Analysis", "SQL"
            ],
            "frontend_developer": [
                "JavaScript", "TypeScript", "React", "Vue.js", "Angular", "HTML5", "CSS3",
                "SASS", "Webpack", "Responsive Design", "Cross-browser Compatibility",
                "Performance Optimization", "Accessibility", "UI/UX", "Git"
            ],
            "backend_developer": [
                "Python", "Java", "Node.js", "Express", "Django", "Spring Boot",
                "RESTful APIs", "GraphQL", "Database Design", "SQL", "NoSQL", "Redis",
                "Microservices", "Docker", "Kubernetes", "AWS", "System Design"
            ]
        }
    
    def create_resume_from_template(self, 
                                  template: ResumeTemplate, 
                                  personal_data: Dict[str, Any],
                                  target_role: str = None,
                                  target_company: str = None) -> str:
        """
        Create a resume using the specified John Doe template
        
        Args:
            template: Resume template to use
            personal_data: User's personal and professional data
            target_role: Role to optimize for (optional)
            target_company: Company to target (optional)
            
        Returns:
            Formatted resume as string
        """
        
        print(f"📄 Creating resume using {template.value} template...")
        
        template_config = self.templates[template]
        
        # Generate resume based on template
        if template == ResumeTemplate.JOHN_DOE_CLASSIC:
            return self._generate_classic_resume(personal_data, target_role, target_company)
        elif template == ResumeTemplate.JOHN_DOE_TECH:
            return self._generate_tech_resume(personal_data, target_role, target_company)
        elif template == ResumeTemplate.JOHN_DOE_MODERN:
            return self._generate_modern_resume(personal_data, target_role, target_company)
        elif template == ResumeTemplate.JOHN_DOE_EXECUTIVE:
            return self._generate_executive_resume(personal_data, target_role, target_company)
        else:
            return self._generate_classic_resume(personal_data, target_role, target_company)
    
    def _generate_classic_resume(self, data: Dict[str, Any], target_role: str, target_company: str) -> str:
        """Generate John Doe Classic template resume"""
        
        resume = f"""
{data.get('full_name', 'John Doe').upper()}
{data.get('email', 'john.doe@email.com')} | {data.get('phone', '+1 (555) 123-4567')} | {data.get('location', 'San Francisco, CA')}
LinkedIn: {data.get('linkedin_url', 'linkedin.com/in/johndoe')} | GitHub: {data.get('github_url', 'github.com/johndoe')}

PROFESSIONAL SUMMARY
{self._generate_professional_summary(data, target_role, target_company)}

TECHNICAL SKILLS
{self._format_skills_section(data.get('skills', []), target_role)}

PROFESSIONAL EXPERIENCE
{self._format_experience_section(data.get('work_experience', []))}

EDUCATION
{self._format_education_section(data.get('education', []))}

PROJECTS
{self._format_projects_section(data.get('projects', []))}
"""
        
        return resume.strip()
    
    def _generate_tech_resume(self, data: Dict[str, Any], target_role: str, target_company: str) -> str:
        """Generate John Doe Tech template resume"""
        
        resume = f"""
{data.get('full_name', 'John Doe').upper()}
Software Engineer
{data.get('email', 'john.doe@email.com')} | {data.get('phone', '+1 (555) 123-4567')} | {data.get('location', 'San Francisco, CA')}
LinkedIn: {data.get('linkedin_url', 'linkedin.com/in/johndoe')} | GitHub: {data.get('github_url', 'github.com/johndoe')}

TECHNICAL EXPERTISE
{self._format_technical_skills_detailed(data.get('skills', []), target_role)}

PROFESSIONAL EXPERIENCE
{self._format_experience_section_technical(data.get('work_experience', []))}

KEY PROJECTS
{self._format_projects_section_detailed(data.get('projects', []))}

EDUCATION & CERTIFICATIONS
{self._format_education_section(data.get('education', []))}
{self._format_certifications_section(data.get('certifications', []))}
"""
        
        return resume.strip()
    
    def _generate_modern_resume(self, data: Dict[str, Any], target_role: str, target_company: str) -> str:
        """Generate John Doe Modern template resume"""
        
        resume = f"""
════════════════════════════════════════════════════════════════
                    {data.get('full_name', 'John Doe').upper()}
                 {target_role or 'Software Engineer'}
════════════════════════════════════════════════════════════════

📧 {data.get('email', 'john.doe@email.com')}  📱 {data.get('phone', '+1 (555) 123-4567')}  📍 {data.get('location', 'San Francisco, CA')}
🔗 {data.get('linkedin_url', 'linkedin.com/in/johndoe')}  💻 {data.get('github_url', 'github.com/johndoe')}

PROFESSIONAL SUMMARY
▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
{self._generate_professional_summary(data, target_role, target_company)}

CORE COMPETENCIES
▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
{self._format_skills_modern(data.get('skills', []), target_role)}

PROFESSIONAL EXPERIENCE
▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
{self._format_experience_section_modern(data.get('work_experience', []))}
"""
        
        return resume.strip()
    
    def _generate_executive_resume(self, data: Dict[str, Any], target_role: str, target_company: str) -> str:
        """Generate John Doe Executive template resume"""
        
        resume = f"""
{data.get('full_name', 'John Doe').upper()}
{target_role or 'Senior Executive'}

{data.get('email', 'john.doe@email.com')} | {data.get('phone', '+1 (555) 123-4567')} | {data.get('location', 'San Francisco, CA')}
LinkedIn: {data.get('linkedin_url', 'linkedin.com/in/johndoe')}

EXECUTIVE SUMMARY
{self._generate_executive_summary(data, target_role, target_company)}

LEADERSHIP EXPERIENCE
{self._format_experience_section_executive(data.get('work_experience', []))}

KEY ACHIEVEMENTS
{self._format_key_achievements(data.get('work_experience', []))}

EDUCATION
{self._format_education_section(data.get('education', []))}
"""
        
        return resume.strip()
    
    def _generate_professional_summary(self, data: Dict[str, Any], target_role: str, target_company: str) -> str:
        """Generate AI-enhanced professional summary"""
        
        if not client:
            # Fallback professional summary
            experience_years = self._calculate_experience_years(data.get('work_experience', []))
            return f"Experienced {target_role or 'Software Engineer'} with {experience_years}+ years of experience in developing scalable applications and leading technical initiatives. Proven track record of delivering high-quality solutions and driving business growth."
        
        try:
            # Create AI prompt for professional summary
            prompt = f"""
            Create a compelling 2-3 sentence professional summary for a resume targeting {target_role or 'Software Engineer'} at {target_company or 'a leading technology company'}.
            
            Use this background information:
            - Work Experience: {len(data.get('work_experience', []))} positions
            - Skills: {', '.join(data.get('skills', [])[:8])}
            - Experience Level: {self._calculate_experience_years(data.get('work_experience', []))} years
            
            Make it:
            - ATS-friendly with relevant keywords
            - Quantifiable achievements focused
            - Role-specific and impactful
            - Professional and concise
            
            Return only the summary text, no formatting.
            """
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"⚠️ AI summary generation failed: {e}")
            experience_years = self._calculate_experience_years(data.get('work_experience', []))
            return f"Experienced {target_role or 'Software Engineer'} with {experience_years}+ years of experience in developing scalable applications and leading technical initiatives."
    
    def _generate_executive_summary(self, data: Dict[str, Any], target_role: str, target_company: str) -> str:
        """Generate executive-level summary"""
        
        experience_years = self._calculate_experience_years(data.get('work_experience', []))
        return f"Senior executive with {experience_years}+ years of leadership experience driving organizational growth and digital transformation. Proven track record of building high-performing teams, delivering strategic initiatives, and achieving measurable business results in competitive markets."
    
    def _calculate_experience_years(self, work_experience: List[Dict]) -> int:
        """Calculate total years of experience"""
        
        if not work_experience:
            return 0
        
        # Simple calculation - in real implementation, would parse dates properly
        return len(work_experience) * 2  # Assume average 2 years per position
    
    def _format_skills_section(self, skills: List[str], target_role: str) -> str:
        """Format skills section with role-specific optimization"""
        
        if not skills:
            # Use default skills based on role
            role_key = target_role.lower().replace(' ', '_') if target_role else 'software_engineer'
            skills = self.ats_keywords.get(role_key, self.ats_keywords['software_engineer'])[:10]
        
        # Group skills by category
        technical_skills = []
        tools_frameworks = []
        soft_skills = []
        
        for skill in skills:
            skill_lower = skill.lower()
            if any(tech in skill_lower for tech in ['python', 'java', 'javascript', 'sql', 'html', 'css']):
                technical_skills.append(skill)
            elif any(tool in skill_lower for tool in ['react', 'angular', 'docker', 'aws', 'git', 'jenkins']):
                tools_frameworks.append(skill)
            else:
                soft_skills.append(skill)
        
        formatted_skills = ""
        
        if technical_skills:
            formatted_skills += f"Languages: {', '.join(technical_skills)}\n"
        
        if tools_frameworks:
            formatted_skills += f"Tools & Frameworks: {', '.join(tools_frameworks)}\n"
        
        if soft_skills:
            formatted_skills += f"Additional Skills: {', '.join(soft_skills)}"
        
        return formatted_skills.strip()
    
    def _format_technical_skills_detailed(self, skills: List[str], target_role: str) -> str:
        """Format detailed technical skills for tech resume"""
        
        if not skills:
            role_key = target_role.lower().replace(' ', '_') if target_role else 'software_engineer'
            skills = self.ats_keywords.get(role_key, self.ats_keywords['software_engineer'])
        
        # Categorize skills for tech resume
        languages = [s for s in skills if s in ['Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust']]
        frameworks = [s for s in skills if s in ['React', 'Angular', 'Vue.js', 'Django', 'Flask', 'Spring Boot', 'Express']]
        databases = [s for s in skills if s in ['SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'DynamoDB']]
        cloud_tools = [s for s in skills if s in ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins']]
        
        result = ""
        if languages:
            result += f"Programming Languages: {', '.join(languages)}\n"
        if frameworks:
            result += f"Frameworks & Libraries: {', '.join(frameworks)}\n"
        if databases:
            result += f"Databases: {', '.join(databases)}\n"
        if cloud_tools:
            result += f"Cloud & DevOps: {', '.join(cloud_tools)}\n"
        
        return result.strip()
    
    def _format_skills_modern(self, skills: List[str], target_role: str) -> str:
        """Format skills in modern visual style"""
        
        if not skills:
            role_key = target_role.lower().replace(' ', '_') if target_role else 'software_engineer'
            skills = self.ats_keywords.get(role_key, self.ats_keywords['software_engineer'])[:12]
        
        # Create visual skill representation
        formatted = ""
        for i, skill in enumerate(skills[:12]):  # Limit to 12 skills
            if i % 4 == 0:
                formatted += "\n"
            formatted += f"▪ {skill}    "
        
        return formatted.strip()
    
    def _format_experience_section(self, work_experience: List[Dict]) -> str:
        """Format work experience section"""
        
        if not work_experience:
            return "No work experience provided"
        
        formatted = ""
        
        for exp in work_experience:
            formatted += f"\n{exp.get('position', 'Position')} | {exp.get('company', 'Company')} | {exp.get('location', 'Location')}\n"
            formatted += f"{exp.get('start_date', 'Start')} - {exp.get('end_date', 'End')}\n"
            
            # Add responsibilities
            responsibilities = exp.get('responsibilities', [])
            for resp in responsibilities:
                formatted += f"• {resp}\n"
            
            # Add achievements
            achievements = exp.get('achievements', [])
            for achievement in achievements:
                formatted += f"• {achievement}\n"
            
            formatted += "\n"
        
        return formatted.strip()
    
    def _format_experience_section_technical(self, work_experience: List[Dict]) -> str:
        """Format experience section with technical focus"""
        
        formatted = ""
        
        for exp in work_experience:
            formatted += f"\n{exp.get('position', 'Position')} | {exp.get('company', 'Company')} | {exp.get('start_date', 'Start')} - {exp.get('end_date', 'End')}\n"
            
            # Emphasize technical achievements
            achievements = exp.get('achievements', [])
            technologies = exp.get('technologies_used', [])
            
            for achievement in achievements:
                formatted += f"• {achievement}\n"
            
            if technologies:
                formatted += f"Technologies: {', '.join(technologies)}\n"
            
            formatted += "\n"
        
        return formatted.strip()
    
    def _format_experience_section_modern(self, work_experience: List[Dict]) -> str:
        """Format experience with modern visual elements"""
        
        formatted = ""
        
        for i, exp in enumerate(work_experience):
            formatted += f"\n🏢 {exp.get('company', 'Company')} | {exp.get('position', 'Position')}\n"
            formatted += f"📅 {exp.get('start_date', 'Start')} - {exp.get('end_date', 'End')} | 📍 {exp.get('location', 'Location')}\n"
            
            achievements = exp.get('achievements', [])
            for achievement in achievements:
                formatted += f"⭐ {achievement}\n"
            
            if i < len(work_experience) - 1:
                formatted += "─" * 60 + "\n"
        
        return formatted.strip()
    
    def _format_experience_section_executive(self, work_experience: List[Dict]) -> str:
        """Format experience section for executive positions"""
        
        formatted = ""
        
        for exp in work_experience:
            formatted += f"\n{exp.get('position', 'Position')} | {exp.get('company', 'Company')}\n"
            formatted += f"{exp.get('start_date', 'Start')} - {exp.get('end_date', 'End')}\n"
            
            responsibilities = exp.get('responsibilities', [])
            achievements = exp.get('achievements', [])
            
            # Focus on leadership and business impact
            for resp in responsibilities:
                if any(keyword in resp.lower() for keyword in ['lead', 'manage', 'direct', 'oversee', 'strategy']):
                    formatted += f"• {resp}\n"
            
            for achievement in achievements:
                formatted += f"• {achievement}\n"
            
            formatted += "\n"
        
        return formatted.strip()
    
    def _format_education_section(self, education: List[Dict]) -> str:
        """Format education section"""
        
        if not education:
            return "Education details not provided"
        
        formatted = ""
        
        for edu in education:
            formatted += f"{edu.get('degree', 'Degree')} in {edu.get('field_of_study', 'Field')}\n"
            formatted += f"{edu.get('institution', 'Institution')} | {edu.get('graduation_date', 'Graduation Date')}\n"
            
            if edu.get('gpa'):
                formatted += f"GPA: {edu['gpa']}\n"
            
            formatted += "\n"
        
        return formatted.strip()
    
    def _format_projects_section(self, projects: List[Dict]) -> str:
        """Format projects section"""
        
        if not projects:
            return "No projects provided"
        
        formatted = ""
        
        for project in projects:
            formatted += f"\n{project.get('name', 'Project Name')}\n"
            formatted += f"{project.get('description', 'Project description not provided')}\n"
            
            technologies = project.get('technologies', [])
            if technologies:
                formatted += f"Technologies: {', '.join(technologies)}\n"
            
            if project.get('github_url'):
                formatted += f"GitHub: {project['github_url']}\n"
            
            formatted += "\n"
        
        return formatted.strip()
    
    def _format_projects_section_detailed(self, projects: List[Dict]) -> str:
        """Format projects section with detailed technical information"""
        
        formatted = ""
        
        for project in projects:
            formatted += f"\n{project.get('name', 'Project Name')}\n"
            formatted += f"{project.get('description', 'Description not provided')}\n"
            
            key_features = project.get('key_features', [])
            for feature in key_features:
                formatted += f"• {feature}\n"
            
            technologies = project.get('technologies', [])
            if technologies:
                formatted += f"Tech Stack: {', '.join(technologies)}\n"
            
            if project.get('github_url'):
                formatted += f"Repository: {project['github_url']}\n"
            
            formatted += "\n"
        
        return formatted.strip()
    
    def _format_certifications_section(self, certifications: List[str]) -> str:
        """Format certifications section"""
        
        if not certifications:
            return ""
        
        formatted = "\nCERTIFICATIONS\n"
        for cert in certifications:
            formatted += f"• {cert}\n"
        
        return formatted.strip()
    
    def _format_key_achievements(self, work_experience: List[Dict]) -> str:
        """Extract and format key achievements for executive resume"""
        
        all_achievements = []
        
        for exp in work_experience:
            achievements = exp.get('achievements', [])
            all_achievements.extend(achievements)
        
        # Select top achievements (those with numbers/metrics)
        key_achievements = []
        for achievement in all_achievements:
            if any(char.isdigit() for char in achievement) or any(keyword in achievement.lower() for keyword in ['%', 'million', 'thousand', 'reduced', 'increased', 'improved']):
                key_achievements.append(achievement)
        
        formatted = ""
        for achievement in key_achievements[:5]:  # Top 5 achievements
            formatted += f"• {achievement}\n"
        
        return formatted.strip()
    
    def optimize_resume_for_role(self, resume_content: str, target_role: str, job_description: str = None) -> ResumeOptimization:
        """
        Analyze and optimize resume for specific role
        
        Args:
            resume_content: Current resume content
            target_role: Target job role
            job_description: Job description to match against (optional)
            
        Returns:
            ResumeOptimization object with analysis and suggestions
        """
        
        print(f"🔍 Analyzing resume optimization for {target_role}...")
        
        # Get relevant keywords for the role
        role_key = target_role.lower().replace(' ', '_')
        relevant_keywords = self.ats_keywords.get(role_key, self.ats_keywords['software_engineer'])
        
        # Analyze keyword matching
        resume_lower = resume_content.lower()
        matched_keywords = [kw for kw in relevant_keywords if kw.lower() in resume_lower]
        missing_keywords = [kw for kw in relevant_keywords if kw.lower() not in resume_lower]
        
        # Calculate scores
        keyword_match_score = (len(matched_keywords) / len(relevant_keywords)) * 100
        ats_score = self._calculate_ats_score(resume_content)
        role_alignment_score = keyword_match_score * 0.7 + ats_score * 0.3
        
        # Generate suggestions
        suggestions = self._generate_optimization_suggestions(missing_keywords, resume_content, target_role)
        
        optimization = ResumeOptimization(
            ats_score=round(ats_score, 2),
            keyword_match_score=round(keyword_match_score, 2),
            missing_keywords=missing_keywords[:10],  # Top 10 missing keywords
            suggested_improvements=suggestions,
            strengths=self._identify_strengths(resume_content, matched_keywords),
            weaknesses=self._identify_weaknesses(resume_content, missing_keywords),
            role_alignment_score=round(role_alignment_score, 2)
        )
        
        return optimization
    
    def _calculate_ats_score(self, resume_content: str) -> float:
        """Calculate ATS-friendliness score"""
        
        score = 100.0
        
        # Check for common ATS issues
        if len(resume_content.split()) < 200:
            score -= 20  # Too short
        
        if len(resume_content.split()) > 800:
            score -= 10  # Too long
        
        # Check for good practices
        if "PROFESSIONAL SUMMARY" in resume_content.upper():
            score += 5
        
        if "TECHNICAL SKILLS" in resume_content.upper() or "SKILLS" in resume_content.upper():
            score += 5
        
        # Check for quantified achievements
        if any(char.isdigit() for char in resume_content):
            score += 10
        
        return max(0, min(100, score))
    
    def _generate_optimization_suggestions(self, missing_keywords: List[str], resume_content: str, target_role: str) -> List[str]:
        """Generate resume improvement suggestions"""
        
        suggestions = []
        
        if missing_keywords:
            suggestions.append(f"Add these relevant keywords: {', '.join(missing_keywords[:5])}")
        
        if not any(char.isdigit() for char in resume_content):
            suggestions.append("Include quantified achievements (e.g., 'Improved performance by 40%')")
        
        if "PROFESSIONAL SUMMARY" not in resume_content.upper():
            suggestions.append("Add a professional summary section at the top")
        
        if len(resume_content.split()) < 300:
            suggestions.append("Expand your resume with more detailed descriptions of your experience")
        
        if target_role.lower() == "software engineer" and "github" not in resume_content.lower():
            suggestions.append("Include your GitHub profile to showcase your code")
        
        return suggestions
    
    def _identify_strengths(self, resume_content: str, matched_keywords: List[str]) -> List[str]:
        """Identify resume strengths"""
        
        strengths = []
        
        if len(matched_keywords) > 10:
            strengths.append("Strong keyword optimization for target role")
        
        if any(char.isdigit() for char in resume_content):
            strengths.append("Includes quantified achievements")
        
        if "github" in resume_content.lower():
            strengths.append("Includes professional GitHub profile")
        
        if len(resume_content.split()) > 400:
            strengths.append("Comprehensive professional experience")
        
        return strengths
    
    def _identify_weaknesses(self, resume_content: str, missing_keywords: List[str]) -> List[str]:
        """Identify resume weaknesses"""
        
        weaknesses = []
        
        if len(missing_keywords) > 5:
            weaknesses.append("Missing several relevant keywords for target role")
        
        if not any(char.isdigit() for char in resume_content):
            weaknesses.append("Lacks quantified achievements and metrics")
        
        if len(resume_content.split()) < 300:
            weaknesses.append("Resume content is too brief")
        
        return weaknesses
    
    def parse_existing_resume(self, resume_content: str, file_format: str = "text") -> ResumeAnalysis:
        """
        Parse an existing resume and extract structured data
        
        Args:
            resume_content: Raw resume content (text, HTML, etc.)
            file_format: Format of the input ("text", "html", "pdf", "docx")
            
        Returns:
            ResumeAnalysis object with extracted data and analysis
        """
        
        print(f"📄 Analyzing existing resume ({file_format} format)...")
        
        # Extract structured data from resume
        extracted_data = self._extract_resume_data(resume_content)
        
        # Analyze resume structure and content
        detected_sections = self._detect_resume_sections(resume_content)
        formatting_issues = self._identify_formatting_issues(resume_content)
        content_gaps = self._identify_content_gaps(extracted_data)
        
        # Calculate parsing confidence
        parsing_confidence = self._calculate_parsing_confidence(
            extracted_data, detected_sections, len(formatting_issues)
        )
        
        # Calculate ATS readiness
        ats_readiness = self._calculate_ats_score(resume_content)
        
        analysis = ResumeAnalysis(
            extracted_data=extracted_data,
            original_format=file_format,
            parsing_confidence=parsing_confidence,
            detected_sections=detected_sections,
            formatting_issues=formatting_issues,
            content_gaps=content_gaps,
            ats_readiness=ats_readiness
        )
        
        return analysis
    
    def convert_to_ats_template(self, 
                               resume_content: str, 
                               target_template: ResumeTemplate = ResumeTemplate.JOHN_DOE_CLASSIC,
                               target_role: str = None,
                               target_company: str = None) -> ResumeConversion:
        """
        Convert existing resume to ATS-friendly John Doe template
        
        Args:
            resume_content: Original resume content
            target_template: John Doe template to convert to
            target_role: Target role for optimization
            target_company: Target company for customization
            
        Returns:
            ResumeConversion object with before/after analysis
        """
        
        print(f"🔄 Converting resume to {target_template.value} template...")
        
        # Analyze original resume
        original_analysis = self.parse_existing_resume(resume_content)
        before_scores = self.optimize_resume_for_role(resume_content, target_role or "Software Engineer")
        
        # Extract and enhance data
        enhanced_data = self._enhance_extracted_data(original_analysis.extracted_data, target_role, target_company)
        
        # Generate new resume with template
        converted_resume = self.create_resume_from_template(
            target_template,
            enhanced_data,
            target_role,
            target_company
        )
        
        # Analyze converted resume
        after_scores = self.optimize_resume_for_role(converted_resume, target_role or "Software Engineer")
        
        # Identify improvements made
        improvements_made = self._identify_conversion_improvements(before_scores, after_scores)
        
        conversion = ResumeConversion(
            original_resume=resume_content,
            converted_resume=converted_resume,
            template_used=target_template,
            improvements_made=improvements_made,
            before_scores=before_scores,
            after_scores=after_scores,
            conversion_success=after_scores.ats_score > before_scores.ats_score
        )
        
        return conversion
    
    def suggest_resume_improvements(self, resume_content: str, target_role: str = None) -> Dict[str, Any]:
        """
        Analyze resume and provide detailed improvement suggestions
        
        Args:
            resume_content: Resume content to analyze
            target_role: Target role for optimization
            
        Returns:
            Dictionary with comprehensive improvement suggestions
        """
        
        print(f"🔍 Analyzing resume for improvement opportunities...")
        
        # Parse and analyze resume
        analysis = self.parse_existing_resume(resume_content)
        optimization = self.optimize_resume_for_role(resume_content, target_role or "Software Engineer")
        
        # Generate AI-powered suggestions if available
        ai_suggestions = self._generate_ai_improvements(resume_content, target_role) if client else []
        
        suggestions = {
            "overall_assessment": {
                "ats_score": optimization.ats_score,
                "parsing_confidence": analysis.parsing_confidence,
                "keyword_match": optimization.keyword_match_score,
                "role_alignment": optimization.role_alignment_score
            },
            "structural_improvements": {
                "formatting_issues": analysis.formatting_issues,
                "missing_sections": [section for section in ["PROFESSIONAL SUMMARY", "SKILLS", "EXPERIENCE", "EDUCATION"] 
                                   if section not in analysis.detected_sections],
                "section_order": self._suggest_section_order(analysis.detected_sections, target_role)
            },
            "content_improvements": {
                "missing_keywords": optimization.missing_keywords[:10],
                "content_gaps": analysis.content_gaps,
                "achievement_enhancement": self._suggest_achievement_improvements(resume_content),
                "quantification_opportunities": self._find_quantification_opportunities(resume_content)
            },
            "template_recommendations": {
                "best_template": self._recommend_template(analysis.extracted_data, target_role),
                "template_benefits": self._explain_template_benefits(target_role),
                "conversion_preview": "Available - see convert_to_ats_template()"
            },
            "ai_suggestions": ai_suggestions,
            "next_steps": self._generate_next_steps(optimization, analysis)
        }
        
        return suggestions
    
    def _extract_resume_data(self, resume_content: str) -> ResumeData:
        """Extract structured data from resume content"""
        
        # Basic extraction using regex patterns
        lines = resume_content.split('\n')
        
        # Extract personal info
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_content)
        phone_match = re.search(r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})', resume_content)
        
        # Extract name (usually first line or largest text)
        potential_names = [line.strip() for line in lines[:5] if line.strip() and len(line.strip().split()) <= 4]
        name = potential_names[0] if potential_names else "Name Not Found"
        
        personal_info = PersonalInfo(
            full_name=name,
            email=email_match.group() if email_match else "email@example.com",
            phone=phone_match.group() if phone_match else "+1 (555) 123-4567",
            location="Location Not Specified",
            linkedin_url=self._extract_linkedin(resume_content),
            github_url=self._extract_github(resume_content)
        )
        
        # Extract work experience
        work_experience = self._extract_work_experience(resume_content)
        
        # Extract education
        education = self._extract_education(resume_content)
        
        # Extract skills
        skills = self._extract_skills(resume_content)
        
        # Extract projects
        projects = self._extract_projects(resume_content)
        
        return ResumeData(
            personal_info=personal_info,
            work_experience=work_experience,
            education=education,
            skills=skills,
            projects=projects
        )
    
    def _extract_linkedin(self, content: str) -> Optional[str]:
        """Extract LinkedIn URL from resume"""
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', content.lower())
        return linkedin_match.group() if linkedin_match else None
    
    def _extract_github(self, content: str) -> Optional[str]:
        """Extract GitHub URL from resume"""
        github_match = re.search(r'github\.com/[\w-]+', content.lower())
        return github_match.group() if github_match else None
    
    def _extract_work_experience(self, content: str) -> List[WorkExperience]:
        """Extract work experience from resume"""
        
        # This is a simplified extraction - in a full implementation,
        # you'd use more sophisticated NLP techniques
        
        experiences = []
        lines = content.split('\n')
        
        # Look for common experience patterns
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Look for job titles or company names
            if any(keyword in line.lower() for keyword in ['engineer', 'developer', 'manager', 'analyst', 'specialist']):
                # Try to extract experience details
                experience = WorkExperience(
                    company="Company Name",
                    position=line,
                    location="Location",
                    start_date="Start Date",
                    end_date="End Date",
                    is_current=False,
                    responsibilities=["Responsibility extracted from resume"],
                    achievements=["Achievement extracted from resume"]
                )
                experiences.append(experience)
        
        # Return at least one placeholder if none found
        if not experiences:
            experiences.append(WorkExperience(
                company="Previous Company",
                position="Previous Position",
                location="Location",
                start_date="2020",
                end_date="2023",
                is_current=False,
                responsibilities=["Experience details not clearly parsed"],
                achievements=["Please update with specific achievements"]
            ))
        
        return experiences[:3]  # Limit to 3 most recent
    
    def _extract_education(self, content: str) -> List[Education]:
        """Extract education from resume"""
        
        education_list = []
        
        # Look for education keywords
        education_keywords = ['university', 'college', 'bachelor', 'master', 'degree', 'phd', 'diploma']
        
        lines = content.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in education_keywords):
                education = Education(
                    institution="Educational Institution",
                    degree="Degree Type",
                    field_of_study="Field of Study",
                    graduation_date="Graduation Year"
                )
                education_list.append(education)
                break  # Take first match
        
        # Default education if none found
        if not education_list:
            education_list.append(Education(
                institution="University Name",
                degree="Bachelor's Degree",
                field_of_study="Field of Study",
                graduation_date="Graduation Year"
            ))
        
        return education_list
    
    def _extract_skills(self, content: str) -> List[str]:
        """Extract skills from resume"""
        
        # Common technical skills to look for
        common_skills = [
            'Python', 'Java', 'JavaScript', 'React', 'Angular', 'Vue.js', 'Node.js',
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes',
            'Git', 'Jenkins', 'CI/CD', 'Agile', 'Scrum',
            'Machine Learning', 'Data Science', 'TensorFlow', 'PyTorch',
            'HTML', 'CSS', 'Bootstrap', 'Tailwind'
        ]
        
        found_skills = []
        content_lower = content.lower()
        
        for skill in common_skills:
            if skill.lower() in content_lower:
                found_skills.append(skill)
        
        # Add some default skills if none found
        if not found_skills:
            found_skills = ['Communication', 'Problem Solving', 'Teamwork', 'Leadership']
        
        return found_skills[:12]  # Limit to 12 skills
    
    def _extract_projects(self, content: str) -> List[Project]:
        """Extract projects from resume"""
        
        projects = []
        
        # Look for project keywords
        if 'project' in content.lower():
            project = Project(
                name="Project Name",
                description="Project description extracted from resume",
                technologies=["Technology 1", "Technology 2"],
                start_date="Start Date",
                end_date="End Date"
            )
            projects.append(project)
        
        return projects
    
    def _detect_resume_sections(self, content: str) -> List[str]:
        """Detect sections present in resume"""
        
        sections = []
        content_upper = content.upper()
        
        section_keywords = {
            'PROFESSIONAL SUMMARY': ['SUMMARY', 'PROFILE', 'OBJECTIVE'],
            'WORK EXPERIENCE': ['EXPERIENCE', 'EMPLOYMENT', 'WORK HISTORY'],
            'EDUCATION': ['EDUCATION', 'ACADEMIC'],
            'SKILLS': ['SKILLS', 'TECHNICAL SKILLS', 'COMPETENCIES'],
            'PROJECTS': ['PROJECTS', 'PORTFOLIO'],
            'CERTIFICATIONS': ['CERTIFICATIONS', 'CERTIFICATES'],
            'ACHIEVEMENTS': ['ACHIEVEMENTS', 'ACCOMPLISHMENTS', 'AWARDS']
        }
        
        for section, keywords in section_keywords.items():
            if any(keyword in content_upper for keyword in keywords):
                sections.append(section)
        
        return sections
    
    def _identify_formatting_issues(self, content: str) -> List[str]:
        """Identify formatting issues in resume"""
        
        issues = []
        
        # Check for common formatting problems
        if len(content.split('\n')) < 10:
            issues.append("Resume appears too short or poorly formatted")
        
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content):
            issues.append("Email address not found or poorly formatted")
        
        if not re.search(r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})', content):
            issues.append("Phone number not found or poorly formatted")
        
        # Check for inconsistent bullet points
        bullet_patterns = [r'•', r'\*', r'-', r'◦']
        bullet_counts = [len(re.findall(pattern, content)) for pattern in bullet_patterns]
        if sum(1 for count in bullet_counts if count > 0) > 2:
            issues.append("Inconsistent bullet point formatting")
        
        return issues
    
    def _identify_content_gaps(self, data: ResumeData) -> List[str]:
        """Identify content gaps in resume"""
        
        gaps = []
        
        if not data.personal_info.professional_summary:
            gaps.append("Missing professional summary")
        
        if len(data.skills) < 5:
            gaps.append("Limited skills listed")
        
        if len(data.work_experience) == 0:
            gaps.append("No work experience found")
        
        if not any('achievement' in str(exp).lower() for exp in data.work_experience):
            gaps.append("Lacks quantified achievements")
        
        if len(data.projects) == 0:
            gaps.append("No projects listed")
        
        return gaps
    
    def _calculate_parsing_confidence(self, data: ResumeData, sections: List[str], issues_count: int) -> float:
        """Calculate confidence in parsing accuracy"""
        
        confidence = 100.0
        
        # Reduce confidence based on missing information
        if data.personal_info.full_name == "Name Not Found":
            confidence -= 20
        
        if "email@example.com" in data.personal_info.email:
            confidence -= 15
        
        if len(sections) < 3:
            confidence -= 10
        
        # Reduce based on formatting issues
        confidence -= (issues_count * 5)
        
        return max(0, min(100, confidence))
    
    def _enhance_extracted_data(self, data: ResumeData, target_role: str, target_company: str) -> Dict[str, Any]:
        """Enhance extracted data for template conversion"""
        
        # Convert ResumeData to dictionary format expected by templates
        enhanced_data = {
            "full_name": data.personal_info.full_name,
            "email": data.personal_info.email,
            "phone": data.personal_info.phone,
            "location": data.personal_info.location,
            "linkedin_url": data.personal_info.linkedin_url,
            "github_url": data.personal_info.github_url,
            "professional_summary": data.personal_info.professional_summary or f"Experienced professional with expertise in {target_role} seeking opportunities at {target_company}.",
            "skills": data.skills,
            "work_experience": [asdict(exp) for exp in data.work_experience] if data.work_experience else [],
            "education": [asdict(edu) for edu in data.education] if data.education else [],
            "projects": [asdict(proj) for proj in data.projects] if data.projects else []
        }
        
        return enhanced_data
    
    def _identify_conversion_improvements(self, before: ResumeOptimization, after: ResumeOptimization) -> List[str]:
        """Identify improvements made during conversion"""
        
        improvements = []
        
        if after.ats_score > before.ats_score:
            improvements.append(f"Improved ATS compatibility from {before.ats_score:.1f} to {after.ats_score:.1f}")
        
        if after.keyword_match_score > before.keyword_match_score:
            improvements.append(f"Enhanced keyword matching from {before.keyword_match_score:.1f}% to {after.keyword_match_score:.1f}%")
        
        if after.role_alignment_score > before.role_alignment_score:
            improvements.append(f"Better role alignment from {before.role_alignment_score:.1f} to {after.role_alignment_score:.1f}")
        
        if len(after.missing_keywords) < len(before.missing_keywords):
            improvements.append(f"Added {len(before.missing_keywords) - len(after.missing_keywords)} relevant keywords")
        
        improvements.append("Applied professional John Doe template formatting")
        improvements.append("Optimized section order for ATS parsing")
        improvements.append("Enhanced readability and visual presentation")
        
        return improvements
    
    def _generate_ai_improvements(self, resume_content: str, target_role: str) -> List[str]:
        """Generate AI-powered improvement suggestions"""
        
        if not client:
            return ["AI suggestions unavailable - API not configured"]
        
        try:
            prompt = f"""
            Analyze this resume for a {target_role or 'Software Engineer'} position and provide 5 specific, actionable improvement suggestions:
            
            Resume Content:
            {resume_content[:1000]}...
            
            Focus on:
            1. ATS optimization
            2. Keyword enhancement
            3. Achievement quantification
            4. Content gaps
            5. Industry best practices
            
            Provide specific, actionable suggestions.
            """
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            suggestions = response.choices[0].message.content.strip().split('\n')
            return [s.strip() for s in suggestions if s.strip()][:5]
            
        except Exception as e:
            print(f"⚠️ AI suggestions failed: {e}")
            return ["AI analysis temporarily unavailable"]
    
    def _suggest_achievement_improvements(self, content: str) -> List[str]:
        """Suggest ways to improve achievement descriptions"""
        
        suggestions = []
        
        # Look for unquantified statements
        if not re.search(r'\d+%', content):
            suggestions.append("Add percentage improvements (e.g., 'Improved performance by 40%')")
        
        if not re.search(r'\$\d+', content):
            suggestions.append("Include financial impact where possible (e.g., 'Saved $50K annually')")
        
        if not re.search(r'\d+\s+(users|customers|clients)', content):
            suggestions.append("Quantify user/customer impact (e.g., 'Served 10,000+ users')")
        
        action_verbs = ['led', 'managed', 'developed', 'implemented', 'optimized', 'automated']
        if not any(verb in content.lower() for verb in action_verbs):
            suggestions.append("Use strong action verbs (led, managed, developed, implemented)")
        
        return suggestions[:3]
    
    def _find_quantification_opportunities(self, content: str) -> List[str]:
        """Find opportunities to add quantification"""
        
        opportunities = []
        
        # Look for vague terms that could be quantified
        vague_terms = ['many', 'several', 'various', 'multiple', 'numerous', 'some']
        for term in vague_terms:
            if term in content.lower():
                opportunities.append(f"Replace '{term}' with specific numbers")
        
        # Look for achievements without metrics
        if 'improved' in content.lower() and not re.search(r'\d+%', content):
            opportunities.append("Quantify improvements with percentages")
        
        if 'managed' in content.lower() and not re.search(r'\d+\s+(people|team|members)', content):
            opportunities.append("Specify team size or number of people managed")
        
        return opportunities[:3]
    
    def _recommend_template(self, data: ResumeData, target_role: str) -> str:
        """Recommend best John Doe template based on role and experience"""
        
        if not target_role:
            return "John Doe Classic"
        
        role_lower = target_role.lower()
        
        if any(keyword in role_lower for keyword in ['software', 'developer', 'engineer', 'programmer']):
            return "John Doe Tech"
        elif any(keyword in role_lower for keyword in ['manager', 'director', 'vp', 'executive', 'lead']):
            return "John Doe Executive"
        elif any(keyword in role_lower for keyword in ['designer', 'creative', 'marketing', 'product']):
            return "John Doe Modern"
        else:
            return "John Doe Classic"
    
    def _explain_template_benefits(self, target_role: str) -> List[str]:
        """Explain benefits of recommended template"""
        
        template = self._recommend_template(None, target_role)
        
        benefits = {
            "John Doe Classic": [
                "Clean, professional format preferred by traditional industries",
                "Excellent ATS compatibility and parsing accuracy",
                "Balanced emphasis on all resume sections"
            ],
            "John Doe Tech": [
                "Technical skills prominently featured",
                "Project-focused layout ideal for developers",
                "Optimized for tech industry keywords"
            ],
            "John Doe Modern": [
                "Contemporary design stands out from crowd",
                "Visual elements enhance readability",
                "Perfect for creative and modern companies"
            ],
            "John Doe Executive": [
                "Leadership achievements prominently displayed",
                "Business impact and metrics emphasized",
                "Ideal for senior and management positions"
            ]
        }
        
        return benefits.get(template, benefits["John Doe Classic"])
    
    def _suggest_section_order(self, current_sections: List[str], target_role: str) -> List[str]:
        """Suggest optimal section order for ATS and readability"""
        
        if any(keyword in (target_role or '').lower() for keyword in ['senior', 'manager', 'director', 'vp']):
            # Executive order
            return [
                "Professional Summary", 
                "Core Competencies", 
                "Professional Experience", 
                "Key Achievements",
                "Education", 
                "Certifications"
            ]
        elif any(keyword in (target_role or '').lower() for keyword in ['software', 'developer', 'engineer']):
            # Technical order
            return [
                "Professional Summary",
                "Technical Skills",
                "Professional Experience", 
                "Projects",
                "Education",
                "Certifications"
            ]
        else:
            # Standard order
            return [
                "Professional Summary",
                "Skills",
                "Professional Experience",
                "Education", 
                "Projects",
                "Certifications"
            ]
    
    def _generate_next_steps(self, optimization: ResumeOptimization, analysis: ResumeAnalysis) -> List[str]:
        """Generate actionable next steps"""
        
        steps = []
        
        if optimization.ats_score < 80:
            steps.append("Convert to ATS-friendly John Doe template")
        
        if optimization.keyword_match_score < 60:
            steps.append(f"Add missing keywords: {', '.join(optimization.missing_keywords[:3])}")
        
        if analysis.parsing_confidence < 80:
            steps.append("Improve formatting and structure for better ATS parsing")
        
        if len(analysis.content_gaps) > 0:
            steps.append(f"Address content gaps: {', '.join(analysis.content_gaps[:2])}")
        
        steps.append("Review and quantify achievements with specific metrics")
        steps.append("Customize for each job application")
        
        return steps[:5]

# Example usage and testing
if __name__ == "__main__":
    # Initialize the Resume Builder
    builder = ResumeBuilder()
    
    print("🧪 Testing Resume Builder")
    print("=" * 40)
    
    # Test data
    sample_data = {
        "full_name": "John Doe",
        "email": "john.doe@email.com",
        "phone": "+1 (555) 123-4567",
        "location": "San Francisco, CA",
        "linkedin_url": "linkedin.com/in/johndoe",
        "github_url": "github.com/johndoe",
        "skills": ["Python", "JavaScript", "React", "AWS", "Docker", "SQL", "Git", "Agile"],
        "work_experience": [
            {
                "company": "Tech Corp",
                "position": "Senior Software Engineer",
                "location": "San Francisco, CA",
                "start_date": "Jan 2022",
                "end_date": "Present",
                "is_current": True,
                "responsibilities": [
                    "Lead development of microservices architecture",
                    "Mentor junior developers"
                ],
                "achievements": [
                    "Improved application performance by 40%",
                    "Reduced deployment time by 60%"
                ],
                "technologies_used": ["Python", "React", "AWS"]
            }
        ],
        "education": [
            {
                "institution": "University of California",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "graduation_date": "2020",
                "gpa": "3.8"
            }
        ],
        "projects": [
            {
                "name": "E-commerce Platform",
                "description": "Full-stack web application for online shopping",
                "technologies": ["React", "Node.js", "MongoDB"],
                "github_url": "github.com/johndoe/ecommerce"
            }
        ]
    }
    
    # Test resume generation
    print("\n1️⃣ Testing John Doe Classic Template")
    classic_resume = builder.create_resume_from_template(
        ResumeTemplate.JOHN_DOE_CLASSIC,
        sample_data,
        "Software Engineer",
        "Google"
    )
    print(f"   Generated resume: {len(classic_resume)} characters")
    
    # Test resume optimization
    print("\n2️⃣ Testing Resume Optimization")
    optimization = builder.optimize_resume_for_role(
        classic_resume,
        "Software Engineer"
    )
    
    print(f"   ATS Score: {optimization.ats_score}/100")
    print(f"   Keyword Match: {optimization.keyword_match_score}%")
    print(f"   Role Alignment: {optimization.role_alignment_score}/100")
    print(f"   Missing Keywords: {optimization.missing_keywords[:3]}")
    
    # Test different templates
    print("\n3️⃣ Testing Different Templates")
    
    templates_to_test = [ResumeTemplate.JOHN_DOE_TECH, ResumeTemplate.JOHN_DOE_MODERN]
    
    for template in templates_to_test:
        resume = builder.create_resume_from_template(template, sample_data, "Software Engineer")
        print(f"   {template.value}: {len(resume)} characters")
    
    print("\n✅ Resume Builder test completed!")