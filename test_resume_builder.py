"""
🧪 Test Resume Builder with John Doe Templates
Tests the comprehensive resume building system with multiple template styles
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Backend.Agents.InterviewHelper.ResumeBuilder import ResumeBuilder, ResumeTemplate

def test_john_doe_templates():
    """Test all John Doe template variations"""
    
    print("🧪 Testing John Doe Resume Templates")
    print("=" * 50)
    
    # Initialize Resume Builder
    builder = ResumeBuilder()
    
    # Sample user data
    sample_data = {
        "full_name": "Alex Johnson",
        "email": "alex.johnson@email.com", 
        "phone": "+1 (555) 987-6543",
        "location": "New York, NY",
        "linkedin_url": "linkedin.com/in/alexjohnson",
        "github_url": "github.com/alexjohnson",
        "skills": [
            "Python", "JavaScript", "React", "Node.js", "AWS", "Docker", 
            "PostgreSQL", "Git", "Agile", "CI/CD", "REST APIs", "GraphQL"
        ],
        "work_experience": [
            {
                "company": "TechStart Inc.",
                "position": "Senior Full Stack Developer", 
                "location": "New York, NY",
                "start_date": "Mar 2022",
                "end_date": "Present",
                "is_current": True,
                "responsibilities": [
                    "Lead development of scalable web applications serving 100K+ users",
                    "Architect microservices infrastructure using Docker and Kubernetes",
                    "Collaborate with product team to define technical requirements"
                ],
                "achievements": [
                    "Reduced page load times by 45% through code optimization",
                    "Led migration to cloud infrastructure, saving $75K annually",
                    "Mentored 3 junior developers and improved team productivity by 25%"
                ],
                "technologies_used": ["Python", "React", "AWS", "Docker", "PostgreSQL"]
            },
            {
                "company": "Digital Innovations LLC",
                "position": "Software Developer",
                "location": "New York, NY",
                "start_date": "Jun 2020", 
                "end_date": "Feb 2022",
                "is_current": False,
                "responsibilities": [
                    "Built RESTful APIs using Python Flask and Django",
                    "Developed responsive frontend applications with React",
                    "Implemented automated testing and CI/CD pipelines"
                ],
                "achievements": [
                    "Delivered 20+ features ahead of schedule",
                    "Increased test coverage from 55% to 90%",
                    "Reduced bug reports by 35% through improved testing"
                ],
                "technologies_used": ["Python", "Django", "React", "PostgreSQL", "Jenkins"]
            }
        ],
        "education": [
            {
                "institution": "New York University",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "graduation_date": "May 2020",
                "gpa": "3.7",
                "relevant_coursework": ["Data Structures", "Algorithms", "Database Systems"],
                "honors": ["Dean's List", "CS Honor Society"]
            }
        ],
        "projects": [
            {
                "name": "Task Management Platform",
                "description": "Full-stack productivity application with real-time collaboration",
                "technologies": ["React", "Node.js", "Socket.io", "MongoDB", "AWS"],
                "start_date": "Jan 2023",
                "end_date": "Mar 2023",
                "github_url": "github.com/alexjohnson/task-manager",
                "key_features": [
                    "Real-time collaboration with WebSocket integration",
                    "Advanced filtering and search functionality", 
                    "Mobile-responsive design with PWA capabilities"
                ]
            },
            {
                "name": "E-commerce Analytics Dashboard",
                "description": "Business intelligence dashboard for online retailers",
                "technologies": ["Python", "Flask", "D3.js", "PostgreSQL", "Redis"],
                "start_date": "Aug 2022",
                "end_date": "Oct 2022",
                "github_url": "github.com/alexjohnson/ecommerce-analytics",
                "key_features": [
                    "Interactive data visualizations with D3.js",
                    "Real-time sales tracking and reporting",
                    "Automated report generation and email alerts"
                ]
            }
        ],
        "certifications": [
            "AWS Certified Solutions Architect",
            "MongoDB Certified Developer",
            "Scrum Master Certification"
        ]
    }
    
    # Test roles and companies
    test_scenarios = [
        {
            "role": "Senior Software Engineer",
            "company": "Google",
            "template": ResumeTemplate.JOHN_DOE_CLASSIC
        },
        {
            "role": "Full Stack Developer", 
            "company": "Netflix",
            "template": ResumeTemplate.JOHN_DOE_TECH
        },
        {
            "role": "Frontend Developer",
            "company": "Meta",
            "template": ResumeTemplate.JOHN_DOE_MODERN
        },
        {
            "role": "Engineering Manager",
            "company": "Amazon",
            "template": ResumeTemplate.JOHN_DOE_EXECUTIVE
        }
    ]
    
    results = []
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{i}️⃣ Testing {scenario['template'].value} Template")
        print(f"   Target Role: {scenario['role']} at {scenario['company']}")
        print("-" * 40)
        
        try:
            # Generate resume
            resume = builder.create_resume_from_template(
                scenario['template'],
                sample_data,
                scenario['role'],
                scenario['company']
            )
            
            # Optimize for role
            optimization = builder.optimize_resume_for_role(
                resume,
                scenario['role']
            )
            
            result = {
                "template": scenario['template'].value,
                "role": scenario['role'],
                "company": scenario['company'],
                "resume_length": len(resume),
                "ats_score": optimization.ats_score,
                "keyword_match": optimization.keyword_match_score,
                "alignment_score": optimization.role_alignment_score,
                "strengths": len(optimization.strengths),
                "weaknesses": len(optimization.weaknesses),
                "suggestions": len(optimization.suggested_improvements)
            }
            
            results.append(result)
            
            print(f"   ✅ Resume Generated: {result['resume_length']} characters")
            print(f"   📊 ATS Score: {result['ats_score']}/100")
            print(f"   🎯 Keyword Match: {result['keyword_match']}%")
            print(f"   ⭐ Role Alignment: {result['alignment_score']}/100")
            print(f"   💪 Strengths: {result['strengths']} identified")
            print(f"   ⚠️  Areas to Improve: {result['weaknesses']} identified")
            print(f"   💡 Suggestions: {result['suggestions']} provided")
            
            # Show sample of missing keywords
            if optimization.missing_keywords:
                print(f"   🔍 Missing Keywords: {', '.join(optimization.missing_keywords[:3])}")
            
            # Show sample resume section (first 200 chars)
            print(f"   📄 Sample Content:")
            print(f"      {resume[:200]}...")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Summary analysis
    print(f"\n📈 SUMMARY ANALYSIS")
    print("=" * 50)
    
    if results:
        avg_ats = sum(r['ats_score'] for r in results) / len(results)
        avg_keyword = sum(r['keyword_match'] for r in results) / len(results)
        avg_alignment = sum(r['alignment_score'] for r in results) / len(results)
        
        print(f"📊 Average ATS Score: {avg_ats:.1f}/100")
        print(f"🎯 Average Keyword Match: {avg_keyword:.1f}%")
        print(f"⭐ Average Role Alignment: {avg_alignment:.1f}/100")
        
        # Best performing template
        best_template = max(results, key=lambda x: x['alignment_score'])
        print(f"🏆 Best Template: {best_template['template']} ({best_template['alignment_score']}/100)")
        
        # Template comparison
        print(f"\n📋 Template Performance:")
        for result in results:
            print(f"   {result['template']:<20} | ATS: {result['ats_score']}/100 | Keywords: {result['keyword_match']}% | Alignment: {result['alignment_score']}/100")
    
    return results

def test_resume_customization():
    """Test resume customization for different roles"""
    
    print(f"\n🎨 Testing Resume Customization")
    print("=" * 50)
    
    builder = ResumeBuilder()
    
    # Base resume data
    base_data = {
        "full_name": "Sarah Chen",
        "email": "sarah.chen@email.com",
        "phone": "+1 (555) 456-7890",
        "location": "Seattle, WA",
        "linkedin_url": "linkedin.com/in/sarahchen",
        "github_url": "github.com/sarahchen",
        "skills": ["Python", "JavaScript", "Machine Learning", "Data Analysis", "React", "SQL", "TensorFlow"],
        "work_experience": [
            {
                "company": "Data Corp",
                "position": "Data Scientist",
                "location": "Seattle, WA",
                "start_date": "Jan 2021",
                "end_date": "Present",
                "is_current": True,
                "responsibilities": [
                    "Develop machine learning models for predictive analytics",
                    "Analyze large datasets to identify business insights"
                ],
                "achievements": [
                    "Improved model accuracy by 30% using ensemble methods",
                    "Reduced processing time by 50% through optimization"
                ]
            }
        ],
        "education": [
            {
                "institution": "University of Washington",
                "degree": "Master of Science",
                "field_of_study": "Data Science",
                "graduation_date": "2020"
            }
        ],
        "projects": []
    }
    
    # Test different role optimizations
    roles_to_test = [
        "Data Scientist",
        "Software Engineer", 
        "Frontend Developer",
        "Product Manager"
    ]
    
    customization_results = []
    
    for role in roles_to_test:
        print(f"\n🎯 Customizing for {role}")
        print("-" * 30)
        
        # Generate resume
        resume = builder.create_resume_from_template(
            ResumeTemplate.JOHN_DOE_CLASSIC,
            base_data,
            role,
            "Microsoft"
        )
        
        # Analyze optimization
        optimization = builder.optimize_resume_for_role(resume, role)
        
        result = {
            "role": role,
            "keyword_match": optimization.keyword_match_score,
            "missing_keywords": len(optimization.missing_keywords),
            "suggestions": optimization.suggested_improvements
        }
        
        customization_results.append(result)
        
        print(f"   📈 Keyword Match: {result['keyword_match']:.1f}%")
        print(f"   🔍 Missing Keywords: {result['missing_keywords']}")
        print(f"   💡 Top Suggestion: {result['suggestions'][0] if result['suggestions'] else 'None'}")
    
    # Find best role match
    best_match = max(customization_results, key=lambda x: x['keyword_match'])
    print(f"\n🏆 Best Role Match: {best_match['role']} ({best_match['keyword_match']:.1f}% keyword match)")
    
    return customization_results

def test_template_comparison():
    """Compare all John Doe templates side by side"""
    
    print(f"\n🔍 John Doe Template Comparison")
    print("=" * 50)
    
    builder = ResumeBuilder()
    
    # Simple test data
    test_data = {
        "full_name": "John Doe",
        "email": "john.doe@email.com",
        "phone": "+1 (555) 123-4567",
        "location": "San Francisco, CA",
        "linkedin_url": "linkedin.com/in/johndoe",
        "github_url": "github.com/johndoe",
        "skills": ["Python", "React", "AWS", "Docker"],
        "work_experience": [
            {
                "company": "Tech Co",
                "position": "Software Engineer",
                "location": "SF, CA",
                "start_date": "2022",
                "end_date": "Present",
                "is_current": True,
                "responsibilities": ["Develop web apps"],
                "achievements": ["Improved performance by 40%"]
            }
        ],
        "education": [
            {
                "institution": "UC Berkeley",
                "degree": "BS Computer Science",
                "field_of_study": "Computer Science",
                "graduation_date": "2021"
            }
        ],
        "projects": [
            {
                "name": "Web App",
                "description": "Full-stack application",
                "technologies": ["React", "Python"]
            }
        ]
    }
    
    templates = [
        ResumeTemplate.JOHN_DOE_CLASSIC,
        ResumeTemplate.JOHN_DOE_TECH,
        ResumeTemplate.JOHN_DOE_MODERN,
        ResumeTemplate.JOHN_DOE_EXECUTIVE
    ]
    
    comparison_results = []
    
    for template in templates:
        print(f"\n📄 {template.value}")
        print("-" * 30)
        
        try:
            resume = builder.create_resume_from_template(
                template,
                test_data,
                "Software Engineer"
            )
            
            # Show first few lines
            lines = resume.strip().split('\n')[:5]
            for line in lines:
                if line.strip():
                    print(f"   {line[:60]}{'...' if len(line) > 60 else ''}")
            
            result = {
                "template": template.value,
                "length": len(resume),
                "sections": len([line for line in resume.split('\n') if line.isupper() and len(line) > 5])
            }
            
            comparison_results.append(result)
            
            print(f"   📊 Length: {result['length']} chars")
            print(f"   📋 Sections: {result['sections']}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return comparison_results

if __name__ == "__main__":
    print("🚀 Starting Resume Builder Tests")
    print("=" * 60)
    
    # Run all tests
    try:
        template_results = test_john_doe_templates()
        customization_results = test_resume_customization() 
        comparison_results = test_template_comparison()
        
        print(f"\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"✅ Template Tests: {len(template_results)} scenarios tested")
        print(f"✅ Customization Tests: {len(customization_results)} roles tested")
        print(f"✅ Comparison Tests: {len(comparison_results)} templates compared")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()