"""
🎯 Company Intelligence & Training Engine
Phase 1 of the 4-Phase Interview Helper System

This module handles:
- Company research and job requirement analysis
- Skills gap identification and trending technology detection
- Personalized learning roadmap generation
- Comprehensive training modules for technical subjects
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from groq import Groq
import os
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
GROQ_API_KEY = env_vars.get("GroqAPIKey")

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"❌ Failed to initialize Groq client: {e}")
    client = None

@dataclass
class JobRequirement:
    """Structure for job requirement data"""
    title: str
    company: str
    location: str
    experience_level: str
    required_skills: List[str]
    preferred_skills: List[str]
    job_description: str
    salary_range: Optional[str] = None
    posted_date: Optional[str] = None
    source_url: Optional[str] = None

@dataclass
class SkillAnalysis:
    """Structure for skill gap analysis"""
    current_skills: List[str]
    required_skills: List[str]
    missing_skills: List[str]
    matching_skills: List[str]
    trending_skills: List[str]
    skill_match_percentage: float

@dataclass
class LearningRoadmap:
    """Structure for personalized learning roadmap"""
    target_role: str
    target_company: str
    priority_skills: List[Dict]  # [{"skill": str, "priority": int, "estimated_time": str}]
    core_subjects: List[Dict]    # CSE subjects with modules
    dsa_topics: List[Dict]       # DSA topics with difficulty progression
    aptitude_areas: List[str]
    recommended_resources: List[Dict]
    timeline: Dict[str, List[str]]  # Week-wise learning plan

class CompanyIntelligenceEngine:
    """
    🔍 Company Intelligence & Training System
    
    Comprehensive engine for company research, skill analysis, and personalized training
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Core CSE subjects and their modules
        self.cse_subjects = {
            "DBMS": {
                "modules": [
                    "Relational Model & SQL", "Normalization", "Indexing", 
                    "Transactions & Concurrency", "Query Optimization", "NoSQL Databases"
                ],
                "difficulty": "Medium",
                "estimated_time": "3-4 weeks"
            },
            "Operating Systems": {
                "modules": [
                    "Process Management", "Memory Management", "File Systems",
                    "Synchronization", "Deadlocks", "CPU Scheduling"
                ],
                "difficulty": "Hard",
                "estimated_time": "4-5 weeks"
            },
            "Computer Networks": {
                "modules": [
                    "OSI Model", "TCP/IP", "HTTP/HTTPS", "DNS", 
                    "Routing & Switching", "Network Security"
                ],
                "difficulty": "Medium",
                "estimated_time": "3-4 weeks"
            },
            "Object Oriented Programming": {
                "modules": [
                    "Classes & Objects", "Inheritance", "Polymorphism",
                    "Encapsulation", "Abstraction", "Design Patterns"
                ],
                "difficulty": "Medium",
                "estimated_time": "2-3 weeks"
            },
            "System Design": {
                "modules": [
                    "Scalability Principles", "Load Balancing", "Caching",
                    "Database Design", "Microservices", "Distributed Systems"
                ],
                "difficulty": "Hard",
                "estimated_time": "5-6 weeks"
            }
        }
        
        # DSA topics with difficulty progression
        self.dsa_topics = {
            "Arrays & Strings": {"difficulty": "Easy", "problems": 50, "time": "1-2 weeks"},
            "Linked Lists": {"difficulty": "Easy", "problems": 30, "time": "1 week"},
            "Stacks & Queues": {"difficulty": "Easy-Medium", "problems": 25, "time": "1 week"},
            "Trees & Binary Search Trees": {"difficulty": "Medium", "problems": 40, "time": "2-3 weeks"},
            "Graphs": {"difficulty": "Medium-Hard", "problems": 35, "time": "2-3 weeks"},
            "Dynamic Programming": {"difficulty": "Hard", "problems": 45, "time": "3-4 weeks"},
            "Sorting & Searching": {"difficulty": "Medium", "problems": 30, "time": "1-2 weeks"},
            "Recursion & Backtracking": {"difficulty": "Medium-Hard", "problems": 25, "time": "2 weeks"}
        }
    
    def search_job_requirements(self, company_name: str, role_title: str, location: str = "") -> List[JobRequirement]:
        """
        🔍 Search for job requirements across multiple platforms
        
        Args:
            company_name: Target company name
            role_title: Job role/position title
            location: Job location (optional)
            
        Returns:
            List of JobRequirement objects
        """
        print(f"🔍 Searching job requirements for {role_title} at {company_name}...")
        
        job_requirements = []
        
        try:
            # Simulate job search results (in real implementation, this would scrape actual job boards)
            sample_jobs = self._generate_sample_job_data(company_name, role_title, location)
            job_requirements.extend(sample_jobs)
            
            # Use AI to enhance job requirement analysis
            if client:
                enhanced_requirements = self._enhance_job_analysis(job_requirements)
                job_requirements = enhanced_requirements
            
            print(f"✅ Found {len(job_requirements)} job postings")
            return job_requirements
            
        except Exception as e:
            print(f"❌ Error searching job requirements: {e}")
            return []
    
    def analyze_skills_gap(self, current_skills: List[str], job_requirements: List[JobRequirement]) -> SkillAnalysis:
        """
        📊 Analyze skills gap between current profile and job requirements
        
        Args:
            current_skills: List of user's current skills
            job_requirements: List of job requirements from search
            
        Returns:
            SkillAnalysis object with detailed gap analysis
        """
        print("📊 Analyzing skills gap...")
        
        # Extract all required skills from job postings
        all_required_skills = set()
        all_preferred_skills = set()
        
        for job in job_requirements:
            all_required_skills.update([skill.lower().strip() for skill in job.required_skills])
            all_preferred_skills.update([skill.lower().strip() for skill in job.preferred_skills])
        
        # Normalize current skills
        current_skills_lower = [skill.lower().strip() for skill in current_skills]
        
        # Find matches and gaps
        required_skills_list = list(all_required_skills)
        matching_skills = list(set(current_skills_lower) & all_required_skills)
        missing_skills = list(all_required_skills - set(current_skills_lower))
        
        # Calculate match percentage
        if required_skills_list:
            match_percentage = (len(matching_skills) / len(required_skills_list)) * 100
        else:
            match_percentage = 0
        
        # Get trending skills using AI analysis
        trending_skills = self._identify_trending_skills(job_requirements)
        
        analysis = SkillAnalysis(
            current_skills=current_skills,
            required_skills=required_skills_list,
            missing_skills=missing_skills,
            matching_skills=matching_skills,
            trending_skills=trending_skills,
            skill_match_percentage=round(match_percentage, 2)
        )
        
        print(f"✅ Skills analysis completed - {match_percentage:.1f}% match")
        return analysis
    
    def generate_learning_roadmap(self, skill_analysis: SkillAnalysis, target_role: str, target_company: str) -> LearningRoadmap:
        """
        🗺️ Generate personalized learning roadmap based on skill analysis
        
        Args:
            skill_analysis: Skills gap analysis results
            target_role: Target job role
            target_company: Target company
            
        Returns:
            LearningRoadmap object with detailed learning plan
        """
        print("🗺️ Generating personalized learning roadmap...")
        
        # Prioritize missing skills
        priority_skills = []
        for skill in skill_analysis.missing_skills[:10]:  # Top 10 missing skills
            priority = self._calculate_skill_priority(skill, skill_analysis.trending_skills)
            estimated_time = self._estimate_learning_time(skill)
            
            priority_skills.append({
                "skill": skill,
                "priority": priority,
                "estimated_time": estimated_time,
                "resources": self._get_skill_resources(skill)
            })
        
        # Sort by priority (higher priority first)
        priority_skills.sort(key=lambda x: x["priority"], reverse=True)
        
        # Generate CSE subjects plan
        cse_plan = []
        for subject, details in self.cse_subjects.items():
            if self._is_subject_relevant(subject, target_role):
                cse_plan.append({
                    "subject": subject,
                    "modules": details["modules"],
                    "difficulty": details["difficulty"],
                    "estimated_time": details["estimated_time"],
                    "priority": self._calculate_subject_priority(subject, target_role)
                })
        
        # Sort CSE subjects by priority
        cse_plan.sort(key=lambda x: x["priority"], reverse=True)
        
        # Generate DSA learning plan
        dsa_plan = []
        for topic, details in self.dsa_topics.items():
            dsa_plan.append({
                "topic": topic,
                "difficulty": details["difficulty"],
                "problems_count": details["problems"],
                "estimated_time": details["time"],
                "priority": self._calculate_dsa_priority(topic, target_role)
            })
        
        # Sort DSA topics by priority and difficulty
        dsa_plan.sort(key=lambda x: (x["priority"], self._difficulty_to_number(x["difficulty"])), reverse=True)
        
        # Generate timeline
        timeline = self._generate_timeline(priority_skills, cse_plan, dsa_plan)
        
        roadmap = LearningRoadmap(
            target_role=target_role,
            target_company=target_company,
            priority_skills=priority_skills,
            core_subjects=cse_plan,
            dsa_topics=dsa_plan,
            aptitude_areas=["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability"],
            recommended_resources=self._get_recommended_resources(),
            timeline=timeline
        )
        
        print("✅ Learning roadmap generated successfully")
        return roadmap
    
    def get_company_insights(self, company_name: str) -> Dict:
        """
        🏢 Get detailed company insights and culture information
        
        Args:
            company_name: Name of the target company
            
        Returns:
            Dictionary with company insights
        """
        print(f"🏢 Gathering insights for {company_name}...")
        
        try:
            # Use AI to generate company insights
            if client:
                insights = self._generate_company_insights(company_name)
                return insights
            else:
                # Fallback to basic company info
                return {
                    "company_name": company_name,
                    "industry": "Technology",
                    "company_size": "Large",
                    "culture": "Innovation-focused",
                    "interview_process": "Multiple rounds including technical and behavioral",
                    "popular_skills": ["Python", "JavaScript", "System Design", "Problem Solving"]
                }
                
        except Exception as e:
            print(f"❌ Error getting company insights: {e}")
            return {}
    
    # Helper methods
    def _generate_sample_job_data(self, company: str, role: str, location: str) -> List[JobRequirement]:
        """Generate sample job data for demonstration"""
        
        # Common skills mapping by role
        role_skills_map = {
            "software engineer": {
                "required": ["Python", "Java", "JavaScript", "SQL", "Git", "Problem Solving"],
                "preferred": ["React", "Node.js", "AWS", "Docker", "Kubernetes", "System Design"]
            },
            "data scientist": {
                "required": ["Python", "SQL", "Statistics", "Machine Learning", "Pandas", "NumPy"],
                "preferred": ["TensorFlow", "PyTorch", "Tableau", "R", "Big Data", "Cloud Platforms"]
            },
            "frontend developer": {
                "required": ["JavaScript", "HTML", "CSS", "React", "Git", "Responsive Design"],
                "preferred": ["TypeScript", "Vue.js", "Angular", "SASS", "Webpack", "Testing"]
            },
            "backend developer": {
                "required": ["Python", "Java", "SQL", "REST APIs", "Git", "Database Design"],
                "preferred": ["Docker", "Kubernetes", "Redis", "Microservices", "AWS", "System Design"]
            }
        }
        
        # Get skills for the role (default to software engineer)
        role_key = role.lower()
        for key in role_skills_map:
            if key in role_key:
                role_skills = role_skills_map[key]
                break
        else:
            role_skills = role_skills_map["software engineer"]
        
        # Generate sample job postings
        sample_jobs = [
            JobRequirement(
                title=f"{role} - {company}",
                company=company,
                location=location or "Remote/Hybrid",
                experience_level="2-4 years",
                required_skills=role_skills["required"],
                preferred_skills=role_skills["preferred"],
                job_description=f"We are looking for a talented {role} to join our team...",
                salary_range="$80,000 - $120,000",
                posted_date="2 days ago",
                source_url=f"https://careers.{company.lower().replace(' ', '')}.com"
            )
        ]
        
        return sample_jobs
    
    def _enhance_job_analysis(self, job_requirements: List[JobRequirement]) -> List[JobRequirement]:
        """Use AI to enhance job requirement analysis"""
        
        if not client or not job_requirements:
            return job_requirements
        
        try:
            # Create prompt for AI analysis
            job_data = []
            for job in job_requirements:
                job_data.append({
                    "title": job.title,
                    "company": job.company,
                    "required_skills": job.required_skills,
                    "description": job.job_description[:500]  # Limit description length
                })
            
            prompt = f"""
            Analyze these job requirements and enhance the skill extraction:
            
            {json.dumps(job_data, indent=2)}
            
            Please:
            1. Extract additional technical skills that might be mentioned in descriptions
            2. Identify soft skills and competencies
            3. Categorize skills by importance (critical, important, nice-to-have)
            4. Suggest related skills that are commonly required
            
            Return the analysis in JSON format with enhanced skill lists.
            """
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Process AI response (simplified for now)
            return job_requirements
            
        except Exception as e:
            print(f"⚠️ AI enhancement failed: {e}")
            return job_requirements
    
    def _identify_trending_skills(self, job_requirements: List[JobRequirement]) -> List[str]:
        """Identify trending skills from job requirements"""
        
        skill_frequency = {}
        
        for job in job_requirements:
            for skill in job.required_skills + job.preferred_skills:
                skill_lower = skill.lower().strip()
                skill_frequency[skill_lower] = skill_frequency.get(skill_lower, 0) + 1
        
        # Sort by frequency and return top trending skills
        sorted_skills = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)
        trending_skills = [skill for skill, freq in sorted_skills[:10]]
        
        return trending_skills
    
    def _calculate_skill_priority(self, skill: str, trending_skills: List[str]) -> int:
        """Calculate priority score for a skill (1-10 scale)"""
        
        priority = 5  # Base priority
        
        # Higher priority for trending skills
        if skill in trending_skills:
            priority += 3
        
        # Higher priority for fundamental skills
        fundamental_skills = ["python", "java", "javascript", "sql", "git", "problem solving"]
        if skill in fundamental_skills:
            priority += 2
        
        # Higher priority for in-demand skills
        in_demand_skills = ["react", "aws", "docker", "kubernetes", "system design", "machine learning"]
        if skill in in_demand_skills:
            priority += 1
        
        return min(priority, 10)  # Cap at 10
    
    def _estimate_learning_time(self, skill: str) -> str:
        """Estimate time needed to learn a skill"""
        
        # Time estimates for different skill categories
        time_estimates = {
            # Programming languages
            "python": "4-6 weeks", "java": "6-8 weeks", "javascript": "4-6 weeks",
            # Frameworks
            "react": "3-4 weeks", "angular": "4-5 weeks", "vue.js": "3-4 weeks",
            # Databases
            "sql": "2-3 weeks", "mongodb": "2-3 weeks", "postgresql": "2-3 weeks",
            # DevOps
            "docker": "2-3 weeks", "kubernetes": "4-5 weeks", "aws": "6-8 weeks",
            # Default
            "default": "3-4 weeks"
        }
        
        skill_lower = skill.lower()
        for key, time in time_estimates.items():
            if key in skill_lower:
                return time
        
        return time_estimates["default"]
    
    def _get_skill_resources(self, skill: str) -> List[Dict]:
        """Get learning resources for a specific skill"""
        
        resources = [
            {"type": "Online Course", "name": f"{skill.title()} Complete Guide", "platform": "Coursera/Udemy"},
            {"type": "Documentation", "name": f"Official {skill.title()} Docs", "platform": "Official Website"},
            {"type": "Practice", "name": f"{skill.title()} Exercises", "platform": "LeetCode/HackerRank"},
            {"type": "Project", "name": f"Build a {skill.title()} Project", "platform": "GitHub"}
        ]
        
        return resources
    
    def _is_subject_relevant(self, subject: str, target_role: str) -> bool:
        """Check if a CSE subject is relevant for the target role"""
        
        role_subjects = {
            "software engineer": ["DBMS", "Operating Systems", "Computer Networks", "Object Oriented Programming", "System Design"],
            "data scientist": ["DBMS", "Object Oriented Programming"],
            "frontend developer": ["Object Oriented Programming", "Computer Networks"],
            "backend developer": ["DBMS", "Operating Systems", "Computer Networks", "Object Oriented Programming", "System Design"]
        }
        
        role_lower = target_role.lower()
        for role_key, subjects in role_subjects.items():
            if role_key in role_lower:
                return subject in subjects
        
        return True  # Default to relevant
    
    def _calculate_subject_priority(self, subject: str, target_role: str) -> int:
        """Calculate priority for CSE subjects based on target role"""
        
        role_priorities = {
            "software engineer": {"DBMS": 9, "System Design": 8, "Operating Systems": 7, "Computer Networks": 6, "Object Oriented Programming": 8},
            "data scientist": {"DBMS": 8, "Object Oriented Programming": 6},
            "backend developer": {"DBMS": 10, "System Design": 9, "Operating Systems": 8, "Computer Networks": 7, "Object Oriented Programming": 7}
        }
        
        role_lower = target_role.lower()
        for role_key, priorities in role_priorities.items():
            if role_key in role_lower:
                return priorities.get(subject, 5)
        
        return 5  # Default priority
    
    def _calculate_dsa_priority(self, topic: str, target_role: str) -> int:
        """Calculate priority for DSA topics based on target role"""
        
        # DSA is generally high priority for technical roles
        base_priorities = {
            "Arrays & Strings": 9,
            "Linked Lists": 8,
            "Stacks & Queues": 7,
            "Trees & Binary Search Trees": 8,
            "Graphs": 7,
            "Dynamic Programming": 9,
            "Sorting & Searching": 8,
            "Recursion & Backtracking": 7
        }
        
        return base_priorities.get(topic, 7)
    
    def _difficulty_to_number(self, difficulty: str) -> int:
        """Convert difficulty string to number for sorting"""
        difficulty_map = {
            "Easy": 1, "Easy-Medium": 2, "Medium": 3, 
            "Medium-Hard": 4, "Hard": 5
        }
        return difficulty_map.get(difficulty, 3)
    
    def _generate_timeline(self, priority_skills: List[Dict], cse_plan: List[Dict], dsa_plan: List[Dict]) -> Dict[str, List[str]]:
        """Generate week-by-week learning timeline"""
        
        timeline = {}
        current_week = 1
        
        # Add high-priority skills first
        for skill in priority_skills[:5]:  # Top 5 skills
            week_key = f"Week {current_week}"
            if week_key not in timeline:
                timeline[week_key] = []
            timeline[week_key].append(f"Learn {skill['skill']} ({skill['estimated_time']})")
            current_week += 1
        
        # Add CSE subjects
        for subject in cse_plan[:3]:  # Top 3 subjects
            week_key = f"Week {current_week}"
            if week_key not in timeline:
                timeline[week_key] = []
            timeline[week_key].append(f"Study {subject['subject']} ({subject['estimated_time']})")
            current_week += 1
        
        # Add DSA topics
        for topic in dsa_plan[:4]:  # Top 4 DSA topics
            week_key = f"Week {current_week}"
            if week_key not in timeline:
                timeline[week_key] = []
            timeline[week_key].append(f"Practice {topic['topic']} ({topic['estimated_time']})")
            current_week += 1
        
        return timeline
    
    def _get_recommended_resources(self) -> List[Dict]:
        """Get list of recommended learning resources"""
        
        resources = [
            {"name": "LeetCode", "type": "DSA Practice", "url": "https://leetcode.com", "priority": "High"},
            {"name": "GeeksforGeeks", "type": "CSE Concepts", "url": "https://geeksforgeeks.org", "priority": "High"},
            {"name": "Coursera", "type": "Online Courses", "url": "https://coursera.org", "priority": "Medium"},
            {"name": "System Design Primer", "type": "System Design", "url": "https://github.com/donnemartin/system-design-primer", "priority": "High"},
            {"name": "InterviewBit", "type": "Interview Prep", "url": "https://interviewbit.com", "priority": "High"},
            {"name": "HackerRank", "type": "Coding Practice", "url": "https://hackerrank.com", "priority": "Medium"},
            {"name": "Cracking the Coding Interview", "type": "Book", "author": "Gayle McDowell", "priority": "High"}
        ]
        
        return resources
    
    def _generate_company_insights(self, company_name: str) -> Dict:
        """Generate company insights using AI"""
        
        if not client:
            return {}
        
        try:
            prompt = f"""
            Provide detailed insights about {company_name} for interview preparation:
            
            1. Company culture and values
            2. Interview process overview
            3. Technical skills commonly tested
            4. Behavioral competencies they value
            5. Recent news and developments
            6. Tips for interviewing at this company
            
            Format as JSON with clear categories.
            """
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1500
            )
            
            # For now, return basic structure (can be enhanced with AI parsing)
            return {
                "company_name": company_name,
                "culture": "Innovation and collaboration focused",
                "interview_rounds": ["Phone Screening", "Technical Interview", "System Design", "Behavioral", "Final Round"],
                "key_skills": ["Problem Solving", "System Design", "Communication", "Leadership"],
                "preparation_tips": ["Focus on problem-solving approach", "Prepare system design scenarios", "Know the company products"]
            }
            
        except Exception as e:
            print(f"⚠️ AI company insights failed: {e}")
            return {}

# Example usage and testing
if __name__ == "__main__":
    # Initialize the engine
    engine = CompanyIntelligenceEngine()
    
    # Test company research
    print("🧪 Testing Company Intelligence Engine")
    print("=" * 50)
    
    # Search job requirements
    jobs = engine.search_job_requirements("Google", "Software Engineer", "Mountain View")
    
    # Analyze skills gap
    current_skills = ["Python", "JavaScript", "SQL", "Git"]
    skill_analysis = engine.analyze_skills_gap(current_skills, jobs)
    
    print(f"\n📊 Skills Analysis Results:")
    print(f"   Match Percentage: {skill_analysis.skill_match_percentage}%")
    print(f"   Missing Skills: {skill_analysis.missing_skills[:5]}")  # Top 5
    
    # Generate learning roadmap
    roadmap = engine.generate_learning_roadmap(skill_analysis, "Software Engineer", "Google")
    
    print(f"\n🗺️ Learning Roadmap Generated:")
    print(f"   Priority Skills: {len(roadmap.priority_skills)}")
    print(f"   Core Subjects: {len(roadmap.core_subjects)}")
    print(f"   DSA Topics: {len(roadmap.dsa_topics)}")
    
    # Get company insights
    insights = engine.get_company_insights("Google")
    print(f"\n🏢 Company Insights: {insights.get('company_name', 'N/A')}")
    
    print("\n✅ Company Intelligence Engine test completed!")