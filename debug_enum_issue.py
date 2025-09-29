"""
Debug script to isolate the enum issue
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Backend'))

from Backend.Agents.InterviewHelper.AssessmentEngine import assessment_engine

# Create simple test
try:
    # Create assessment configuration
    microsoft_intelligence = {
        "company_name": "Microsoft",
        "tech_stack": ["C#", ".NET", "Azure"],
        "interview_process": "Technical assessment with system design"
    }
    microsoft_resume = {
        "skills": ["C#", ".NET", "Cloud Computing"],
        "experience_years": 4
    }
    
    config = assessment_engine.create_company_specific_assessment(
        company_intelligence=microsoft_intelligence,
        resume_data=microsoft_resume,
        target_role="Software Engineer"
    )
    
    print("✅ Config created successfully")
    
    # Generate questions
    questions = assessment_engine.generate_assessment_questions(config)
    print(f"✅ Generated {len(questions)} questions")
    
    # Check first question
    if questions:
        first_q = questions[0]
        print(f"First question type: {type(first_q)}")
        print(f"First question difficulty type: {type(first_q.difficulty)}")
        print(f"First question category type: {type(first_q.category)}")
        
        # Try formatting
        formatted = assessment_engine._format_question_for_display(first_q)
        print("✅ Question formatted successfully")
        print(f"Formatted type: {formatted.get('type')}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()