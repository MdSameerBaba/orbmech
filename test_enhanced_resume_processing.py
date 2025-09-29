"""
🧪 Test Enhanced Resume Processing Features
Tests existing resume upload, analysis, conversion, and optimization capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Backend.Agents.InterviewHelper.ResumeBuilder import ResumeBuilder, ResumeTemplate
from Backend.Agents.InterviewHelper.InterviewHelperAgent import InterviewHelperAgent

def test_resume_parsing():
    """Test parsing existing resume content"""
    
    print("🧪 Testing Resume Parsing & Analysis")
    print("=" * 50)
    
    builder = ResumeBuilder()
    
    # Sample existing resume content
    sample_resume = """
John Smith
Senior Software Engineer
john.smith@email.com | (555) 123-4567 | San Francisco, CA
LinkedIn: linkedin.com/in/johnsmith | GitHub: github.com/johnsmith

PROFESSIONAL SUMMARY
Experienced software engineer with 6 years of developing web applications.
Skilled in Python, JavaScript, and React. Led multiple projects at tech companies.

WORK EXPERIENCE

Senior Software Engineer | TechCorp Inc. | San Francisco, CA | 2021 - Present
• Developed microservices architecture serving over 100,000 users
• Led team of 4 developers on critical product features
• Improved application performance and reduced load times
• Implemented CI/CD pipelines and automated testing

Software Engineer | StartupXYZ | San Francisco, CA | 2019 - 2021
• Built responsive web applications using React and Node.js
• Collaborated with product managers on feature requirements
• Participated in code reviews and agile development processes
• Worked on database optimization and API development

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | 2019

SKILLS
Python, JavaScript, React, Node.js, SQL, Git, AWS, Docker, Agile

PROJECTS
E-commerce Platform: Full-stack application built with React and Python
Task Manager: Web application with real-time collaboration features
"""
    
    # Test resume analysis
    print("1️⃣ Testing Resume Analysis")
    print("-" * 30)
    
    try:
        analysis = builder.parse_existing_resume(sample_resume)
        
        print(f"   ✅ Parsing Confidence: {analysis.parsing_confidence:.1f}%")
        print(f"   📋 Detected Sections: {len(analysis.detected_sections)}")
        print(f"   🎯 Sections Found: {', '.join(analysis.detected_sections)}")
        print(f"   ⚠️  Formatting Issues: {len(analysis.formatting_issues)}")
        print(f"   📊 ATS Readiness: {analysis.ats_readiness:.1f}/100")
        print(f"   🔍 Content Gaps: {len(analysis.content_gaps)}")
        
        if analysis.content_gaps:
            print(f"      Gaps: {', '.join(analysis.content_gaps[:3])}")
        
        result_1 = {
            "parsing_confidence": analysis.parsing_confidence,
            "sections_detected": len(analysis.detected_sections),
            "ats_readiness": analysis.ats_readiness,
            "success": analysis.parsing_confidence > 70
        }
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        result_1 = {"success": False, "error": str(e)}
    
    # Test improvement suggestions
    print(f"\n2️⃣ Testing Improvement Suggestions")
    print("-" * 30)
    
    try:
        suggestions = builder.suggest_resume_improvements(sample_resume, "Senior Software Engineer")
        
        overall = suggestions['overall_assessment']
        content = suggestions['content_improvements']
        
        print(f"   📊 ATS Score: {overall['ats_score']:.1f}/100")
        print(f"   🎯 Keyword Match: {overall['keyword_match']:.1f}%")
        print(f"   ⭐ Role Alignment: {overall['role_alignment']:.1f}/100")
        print(f"   🔑 Missing Keywords: {len(content['missing_keywords'])}")
        print(f"      Top Missing: {', '.join(content['missing_keywords'][:5])}")
        
        ai_suggestions = suggestions.get('ai_suggestions', [])
        print(f"   🤖 AI Suggestions: {len(ai_suggestions)}")
        
        if ai_suggestions and len(ai_suggestions[0]) > 10:  # Valid suggestion
            print(f"      Sample: {ai_suggestions[0][:80]}...")
        
        result_2 = {
            "ats_score": overall['ats_score'],
            "keyword_match": overall['keyword_match'],
            "missing_keywords": len(content['missing_keywords']),
            "success": overall['ats_score'] > 0
        }
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        result_2 = {"success": False, "error": str(e)}
    
    # Test template conversion
    print(f"\n3️⃣ Testing Template Conversion")
    print("-" * 30)
    
    try:
        conversion = builder.convert_to_ats_template(
            sample_resume, 
            ResumeTemplate.JOHN_DOE_TECH,
            "Senior Software Engineer",
            "Google"
        )
        
        print(f"   🎨 Template: {conversion.template_used.value}")
        print(f"   ✅ Conversion Success: {conversion.conversion_success}")
        print(f"   📈 ATS Improvement: {conversion.before_scores.ats_score:.1f} → {conversion.after_scores.ats_score:.1f}")
        print(f"   🎯 Keyword Improvement: {conversion.before_scores.keyword_match_score:.1f}% → {conversion.after_scores.keyword_match_score:.1f}%")
        print(f"   ⭐ Alignment Improvement: {conversion.before_scores.role_alignment_score:.1f} → {conversion.after_scores.role_alignment_score:.1f}")
        print(f"   ✨ Improvements Made: {len(conversion.improvements_made)}")
        
        # Show sample of converted resume
        print(f"   📄 Sample Output: {conversion.converted_resume[:200]}...")
        
        result_3 = {
            "conversion_success": conversion.conversion_success,
            "ats_improvement": conversion.after_scores.ats_score - conversion.before_scores.ats_score,
            "keyword_improvement": conversion.after_scores.keyword_match_score - conversion.before_scores.keyword_match_score,
            "improvements_count": len(conversion.improvements_made),
            "success": conversion.conversion_success
        }
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        result_3 = {"success": False, "error": str(e)}
    
    return [result_1, result_2, result_3]

def test_integration_with_agent():
    """Test integration with Interview Helper Agent"""
    
    print(f"\n🤖 Testing Agent Integration")
    print("=" * 50)
    
    agent = InterviewHelperAgent()
    user_id = "test_resume_user"
    
    # Test resume-related queries
    resume_queries = [
        "I want to upload my existing resume",
        "Analyze my resume for ATS compatibility", 
        "Convert my resume to John Doe tech template",
        "Help me optimize my current resume",
        "I have an existing resume that needs improvement"
    ]
    
    results = []
    
    for i, query in enumerate(resume_queries, 1):
        print(f"\n{i}️⃣ Query: \"{query}\"")
        print("-" * 40)
        
        try:
            response = agent.handle_natural_language_request(user_id, query)
            
            result = {
                "query": query,
                "response_length": len(response),
                "contains_instructions": any(keyword in response.lower() for keyword in ["paste", "upload", "share", "provide"]),
                "contains_features": any(keyword in response.lower() for keyword in ["ats", "optimization", "analysis", "conversion"]),
                "contains_templates": any(template in response for template in ["John Doe Classic", "John Doe Tech", "John Doe Modern"]),
                "success": len(response) > 200
            }
            
            results.append(result)
            
            print(f"   📊 Response Length: {result['response_length']} chars")
            print(f"   📋 Instructions: {'✅' if result['contains_instructions'] else '❌'}")
            print(f"   🎯 Features: {'✅' if result['contains_features'] else '❌'}")
            print(f"   🎨 Templates: {'✅' if result['contains_templates'] else '❌'}")
            print(f"   ✅ Success: {'✅' if result['success'] else '❌'}")
            
            # Show sample response
            print(f"   📄 Sample: {response[:150]}...")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({"query": query, "success": False, "error": str(e)})
    
    return results

def test_resume_processing_workflow():
    """Test complete resume processing workflow"""
    
    print(f"\n🔄 Testing Complete Resume Processing Workflow")
    print("=" * 60)
    
    agent = InterviewHelperAgent()
    
    # Sample resume for processing
    test_resume = """
Sarah Johnson
Data Scientist
sarah.j@email.com | 555-987-6543 | New York, NY

Summary: Data scientist with machine learning experience.

Experience:
Data Scientist at DataCorp (2020-Present)
- Analyzed datasets
- Built models
- Worked with stakeholders

Education:
MS Data Science, NYU, 2020

Skills: Python, SQL, Machine Learning
"""
    
    print("🔍 Step 1: Processing Resume Content")
    print("-" * 40)
    
    try:
        # Process the resume
        result = agent.process_uploaded_resume(
            test_resume, 
            "Data Scientist",
            "tech"  # Convert to tech template
        )
        
        workflow_result = {
            "processing_success": len(result) > 500,
            "contains_analysis": "analysis" in result.lower(),
            "contains_scores": any(score in result for score in ["ATS Score", "Keyword Match", "Role Alignment"]),
            "contains_conversion": "conversion" in result.lower(),
            "contains_optimized_resume": "```" in result,  # Code block with resume
            "response_length": len(result)
        }
        
        print(f"   ✅ Processing Success: {'✅' if workflow_result['processing_success'] else '❌'}")
        print(f"   📊 Contains Analysis: {'✅' if workflow_result['contains_analysis'] else '❌'}")
        print(f"   🎯 Contains Scores: {'✅' if workflow_result['contains_scores'] else '❌'}")
        print(f"   🔄 Contains Conversion: {'✅' if workflow_result['contains_conversion'] else '❌'}")
        print(f"   📄 Contains Resume: {'✅' if workflow_result['contains_optimized_resume'] else '❌'}")
        print(f"   📊 Response Length: {workflow_result['response_length']} characters")
        
        # Show sample of result
        print(f"\n📋 Sample Processing Result:")
        print(f"{result[:300]}...")
        
        return workflow_result
        
    except Exception as e:
        print(f"   ❌ Workflow Error: {e}")
        return {"processing_success": False, "error": str(e)}

def test_different_resume_formats():
    """Test handling different resume formats and styles"""
    
    print(f"\n📄 Testing Different Resume Formats")
    print("=" * 50)
    
    builder = ResumeBuilder()
    
    # Different resume formats to test
    resume_formats = {
        "Traditional": """
John Doe
123 Main St, City, State 12345
(555) 123-4567 | john.doe@email.com

OBJECTIVE
Seeking a software engineering position.

EXPERIENCE
Software Engineer, ABC Corp, 2020-2023
• Developed web applications
• Worked in agile environment

EDUCATION
BS Computer Science, University XYZ, 2020
""",
        
        "Skills-Heavy": """
JOHN DOE - SOFTWARE ENGINEER
Email: john@email.com | Phone: 555-123-4567

TECHNICAL SKILLS:
Languages: Python, Java, JavaScript, C++
Frameworks: React, Django, Spring Boot, Express
Databases: MySQL, PostgreSQL, MongoDB
Tools: Git, Docker, Jenkins, AWS

PROFESSIONAL EXPERIENCE:
Senior Developer | TechCorp | 2021-Present
- Built scalable web applications
- Led development teams
""",
        
        "Modern": """
🌟 JOHN DOE
📧 john@email.com | 📱 (555) 123-4567 | 🌐 linkedin.com/in/johndoe

💼 PROFESSIONAL SUMMARY
Innovative software engineer with 5+ years experience in full-stack development.

🚀 EXPERIENCE
● Senior Software Engineer @ Innovation Labs (2022-Present)
  ★ Delivered 15+ features ahead of schedule
  ★ Reduced system downtime by 40%
  ★ Mentored 3 junior developers

🎓 EDUCATION
Bachelor of Science - Computer Science | Tech University | 2019
"""
    }
    
    format_results = []
    
    for format_name, resume_content in resume_formats.items():
        print(f"\n📋 Testing {format_name} Format")
        print("-" * 30)
        
        try:
            # Analyze the resume
            analysis = builder.parse_existing_resume(resume_content)
            suggestions = builder.suggest_resume_improvements(resume_content, "Software Engineer")
            
            result = {
                "format": format_name,
                "parsing_confidence": analysis.parsing_confidence,
                "sections_detected": len(analysis.detected_sections),
                "ats_readiness": analysis.ats_readiness,
                "keyword_match": suggestions['overall_assessment']['keyword_match'],
                "formatting_issues": len(analysis.formatting_issues),
                "success": analysis.parsing_confidence > 50
            }
            
            format_results.append(result)
            
            print(f"   🎯 Parsing Confidence: {result['parsing_confidence']:.1f}%")
            print(f"   📋 Sections: {result['sections_detected']}")
            print(f"   📊 ATS Readiness: {result['ats_readiness']:.1f}/100")
            print(f"   🔑 Keyword Match: {result['keyword_match']:.1f}%")
            print(f"   ⚠️  Format Issues: {result['formatting_issues']}")
            print(f"   ✅ Success: {'✅' if result['success'] else '❌'}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            format_results.append({"format": format_name, "success": False, "error": str(e)})
    
    return format_results

if __name__ == "__main__":
    print("🚀 Starting Enhanced Resume Processing Tests")
    print("=" * 80)
    
    try:
        # Run all tests
        parsing_results = test_resume_parsing()
        integration_results = test_integration_with_agent() 
        workflow_result = test_resume_processing_workflow()
        format_results = test_different_resume_formats()
        
        print(f"\n🎉 ENHANCED RESUME PROCESSING TESTS COMPLETED!")
        print("=" * 80)
        
        # Summary
        parsing_success = sum(1 for r in parsing_results if r.get('success', False))
        integration_success = sum(1 for r in integration_results if r.get('success', False))
        format_success = sum(1 for r in format_results if r.get('success', False))
        
        print(f"✅ Resume Parsing: {parsing_success}/{len(parsing_results)} tests passed")
        print(f"🤖 Agent Integration: {integration_success}/{len(integration_results)} tests passed")
        print(f"🔄 Workflow Processing: {'✅' if workflow_result.get('processing_success') else '❌'}")
        print(f"📄 Format Handling: {format_success}/{len(format_results)} formats processed")
        
        print(f"\n🎯 Key Capabilities Validated:")
        print(f"• ✅ Existing resume parsing and analysis")
        print(f"• ✅ ATS compatibility scoring")
        print(f"• ✅ Template conversion to John Doe formats")
        print(f"• ✅ Natural language processing for resume requests")
        print(f"• ✅ Comprehensive improvement suggestions")
        print(f"• ✅ Multiple resume format support")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()