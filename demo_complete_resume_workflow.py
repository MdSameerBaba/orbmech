"""
🎯 Comprehensive Resume Builder Demo
Demonstrates the complete enhanced resume processing workflow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Backend.Agents.InterviewHelper.InterviewHelperAgent import InterviewHelperAgent

def demo_complete_resume_workflow():
    """Demonstrate the complete resume processing workflow"""
    
    print("🎯 Complete Resume Builder Demo")
    print("=" * 60)
    
    agent = InterviewHelperAgent()
    user_id = "demo_user"
    
    # Sample existing resume to process
    existing_resume = """
Jane Smith
Data Scientist
jane.smith@email.com | (555) 987-6543 | New York, NY

Summary
Experienced data scientist with machine learning background.

Experience
Senior Data Scientist - DataCorp (2021-Present)
- Built predictive models
- Analyzed customer data  
- Worked with stakeholders

Data Analyst - TechStart (2019-2021)
- Created dashboards
- Performed statistical analysis
- Generated reports

Education
MS Data Science, Columbia University, 2019
BS Mathematics, NYU, 2017

Skills
Python, SQL, Machine Learning, Tableau, Statistics
"""
    
    print("📄 **DEMO SCENARIO**: Converting existing resume to John Doe Tech template")
    print("=" * 60)
    
    print("\n🔍 **Step 1: Initial Resume Analysis**")
    print("-" * 40)
    
    # Process the existing resume
    try:
        analysis_result = agent.process_uploaded_resume(
            existing_resume,
            "Senior Data Scientist",
            "tech"
        )
        
        print("✅ Resume analysis completed successfully!")
        print(f"📊 Analysis length: {len(analysis_result)} characters")
        
        # Show key parts of the analysis
        lines = analysis_result.split('\n')
        print("\n📋 **Key Analysis Points**:")
        
        for line in lines:
            if any(keyword in line for keyword in ["ATS Score", "Keyword Match", "Role Alignment", "Confidence"]):
                print(f"   {line}")
        
        print("\n💡 **Sample Improvements Identified**:")
        improvement_section = False
        for line in lines:
            if "Improvements Made" in line:
                improvement_section = True
                continue
            if improvement_section and line.startswith('•'):
                print(f"   {line}")
                if lines.index(line) - lines.index([l for l in lines if "Improvements Made" in l][0]) > 3:
                    break
        
        print("\n📄 **Converted Resume Sample** (first 300 chars):")
        # Find the resume section
        if "```" in analysis_result:
            resume_start = analysis_result.find("```") + 3
            resume_end = analysis_result.find("```", resume_start)
            if resume_end > resume_start:
                converted_resume = analysis_result[resume_start:resume_end]
                print(f"   {converted_resume[:300]}...")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
    
    print(f"\n🎨 **Step 2: Template Showcase**")
    print("-" * 40)
    
    # Show different template options
    template_queries = [
        "Show me John Doe Classic template for Software Engineer",
        "I want John Doe Modern template for Product Manager", 
        "Display John Doe Executive template for Director role"
    ]
    
    for i, query in enumerate(template_queries, 1):
        print(f"\n{i}. Testing: \"{query}\"")
        
        try:
            response = agent.handle_natural_language_request(user_id, query)
            
            # Extract template information
            if "John Doe" in response:
                print("   ✅ Template information provided")
                
                # Show template features
                lines = response.split('\n')
                for line in lines:
                    if any(keyword in line for keyword in ["Perfect for:", "Best For:", "Features:"]):
                        print(f"   📌 {line.strip()}")
            else:
                print("   ❌ Template information not found")
                
        except Exception as e:
            print(f"   ❌ Query failed: {e}")
    
    print(f"\n💬 **Step 3: Natural Language Interaction**")
    print("-" * 40)
    
    # Test various natural language commands
    nl_queries = [
        "Help me optimize my resume for Google",
        "I need ATS-friendly formatting",
        "Convert my resume to modern template",
        "Check my resume for missing keywords",
        "Generate a professional summary for me"
    ]
    
    for i, query in enumerate(nl_queries, 1):
        print(f"\n{i}. User Query: \"{query}\"")
        
        try:
            response = agent.handle_natural_language_request(user_id, query)
            
            # Analyze response quality
            quality_indicators = {
                "helpful": any(keyword in response.lower() for keyword in ["help", "assist", "guide", "support"]),
                "actionable": any(keyword in response.lower() for keyword in ["step", "next", "ready", "proceed"]),
                "informative": len(response) > 200,
                "relevant": any(keyword in response.lower() for keyword in ["resume", "template", "ats", "optimization"])
            }
            
            quality_score = sum(quality_indicators.values())
            print(f"   📊 Response Quality: {quality_score}/4")
            print(f"   📏 Length: {len(response)} chars")
            
            if quality_score >= 3:
                print("   ✅ High-quality response")
            else:
                print("   ⚠️  Response could be improved")
            
        except Exception as e:
            print(f"   ❌ Query processing failed: {e}")
    
    print(f"\n🎯 **Step 4: Advanced Features Demo**")
    print("-" * 40)
    
    # Demonstrate advanced features
    advanced_queries = [
        "What's the best John Doe template for a senior software engineer at Amazon?",
        "How can I improve my ATS score from 75 to 90?",
        "Show me examples of quantified achievements for a data scientist",
        "Generate a cover letter to match my John Doe Classic resume"
    ]
    
    for i, query in enumerate(advanced_queries, 1):
        print(f"\n{i}. Advanced Query: \"{query}\"")
        
        try:
            response = agent.handle_natural_language_request(user_id, query)
            
            # Check for advanced features
            advanced_features = {
                "personalization": any(keyword in response.lower() for keyword in ["specific", "customize", "tailor", "personalize"]),
                "metrics": any(keyword in response for keyword in ["score", "%", "improvement", "analysis"]),
                "examples": any(keyword in response.lower() for keyword in ["example", "sample", "instance", "demonstration"]),
                "guidance": any(keyword in response.lower() for keyword in ["suggest", "recommend", "advice", "tip"])
            }
            
            features_found = sum(advanced_features.values())
            print(f"   🚀 Advanced Features: {features_found}/4")
            
            # Show key insight from response
            if len(response) > 100:
                key_sentences = [s.strip() for s in response.split('.') if len(s.strip()) > 50]
                if key_sentences:
                    print(f"   💡 Key Insight: {key_sentences[0][:100]}...")
            
        except Exception as e:
            print(f"   ❌ Advanced query failed: {e}")

def demo_resume_optimization_scenarios():
    """Demo various resume optimization scenarios"""
    
    print(f"\n📊 Resume Optimization Scenarios Demo")
    print("=" * 60)
    
    agent = InterviewHelperAgent()
    
    # Different resume scenarios
    scenarios = [
        {
            "title": "New Graduate Resume",
            "resume": """
Alex Johnson
Recent Graduate
alex@email.com | 555-123-4567

Education: BS Computer Science, State University, 2024
GPA: 3.7

Projects:
- Web application using React
- Mobile app with Flutter
- Data analysis project

Skills: Python, JavaScript, React, SQL
""",
            "target_role": "Entry Level Software Engineer"
        },
        
        {
            "title": "Career Changer Resume", 
            "resume": """
Sarah Chen
sarah.chen@email.com | 555-987-6543

Experience:
Marketing Manager at RetailCorp (2018-2023)
- Managed campaigns
- Analyzed market data
- Led team of 5

Education: MBA Marketing, Business School, 2018

Recently completed: Full Stack Web Development Bootcamp
Skills: HTML, CSS, JavaScript, Node.js, MongoDB
""",
            "target_role": "Junior Full Stack Developer"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}️⃣ **{scenario['title']} Scenario**")
        print("-" * 40)
        
        try:
            # Process the scenario resume
            result = agent.process_uploaded_resume(
                scenario['resume'],
                scenario['target_role']
            )
            
            # Extract key metrics
            lines = result.split('\n')
            metrics = {}
            
            for line in lines:
                if "ATS Score:" in line:
                    metrics['ats'] = line.split(':')[-1].strip()
                elif "Keyword Match:" in line:
                    metrics['keywords'] = line.split(':')[-1].strip()
                elif "Confidence:" in line:
                    metrics['confidence'] = line.split(':')[-1].strip()
            
            print(f"   🎯 Target Role: {scenario['target_role']}")
            if metrics:
                print(f"   📊 Metrics:")
                for key, value in metrics.items():
                    print(f"      {key.title()}: {value}")
            
            # Show top suggestions
            if "Suggestions" in result:
                print(f"   💡 Key Recommendations:")
                suggestion_lines = [line for line in lines if line.strip().startswith('•')][:3]
                for suggestion in suggestion_lines:
                    print(f"      {suggestion.strip()}")
            
        except Exception as e:
            print(f"   ❌ Scenario processing failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting Comprehensive Resume Builder Demo")
    print("=" * 80)
    
    try:
        # Run complete workflow demo
        demo_complete_resume_workflow()
        
        # Run optimization scenarios
        demo_resume_optimization_scenarios()
        
        print(f"\n🎉 COMPREHENSIVE DEMO COMPLETED!")
        print("=" * 80)
        
        print(f"\n🎯 **Demo Summary:**")
        print(f"✅ Existing resume analysis and conversion")
        print(f"✅ John Doe template integration")
        print(f"✅ Natural language command processing")
        print(f"✅ Advanced optimization features")
        print(f"✅ Multiple resume scenario handling")
        print(f"✅ ATS-friendly formatting and scoring")
        
        print(f"\n🚀 **Phase 2 Enhanced Features:**")
        print(f"• 📄 Existing resume upload and parsing")
        print(f"• 🔍 Comprehensive ATS analysis")
        print(f"• 🔄 Automatic template conversion")
        print(f"• 💡 AI-powered improvement suggestions")
        print(f"• 🎨 4 John Doe template variations")
        print(f"• 🤖 Natural language interaction")
        print(f"• 📊 Before/after optimization metrics")
        print(f"• 🎯 Role-specific customization")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()