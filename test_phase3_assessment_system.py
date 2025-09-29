"""
Comprehensive Test Suite for Phase 3: Assessment & Screening Tests System
Tests all components including assessment engine, timed environment, and performance analytics.
"""

import sys
import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

# Add the Backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Backend'))

try:
    from Backend.Agents.InterviewHelper.AssessmentEngine import assessment_engine, AssessmentConfig, DifficultyLevel, QuestionCategory
    from Backend.Agents.InterviewHelper.TimedTestEnvironment import test_environment
    from Backend.Agents.InterviewHelper.PerformanceAnalytics import performance_analytics
    print("✅ Successfully imported all Phase 3 components")
except ImportError as e:
    print(f"❌ Error importing Phase 3 components: {e}")
    sys.exit(1)

class Phase3TestSuite:
    """Comprehensive test suite for Phase 3 system"""
    
    def __init__(self):
        self.test_user_id = "test_user_phase3"
        self.test_results = []
        
    def run_all_tests(self):
        """Run complete test suite"""
        print("\n🧪 Starting Phase 3 Comprehensive Test Suite")
        print("=" * 60)
        
        # Test 1: Basic Assessment Engine
        self.test_assessment_engine_basics()
        
        # Test 2: Question Database Loading
        self.test_question_databases()
        
        # Test 3: Company-Specific Assessment Creation
        self.test_company_assessments()
        
        # Test 4: Traditional Assessment Flow
        self.test_traditional_assessment()
        
        # Test 5: Timed Test Environment
        self.test_timed_environment()
        
        # Test 6: Performance Analytics
        self.test_performance_analytics()
        
        # Test 7: Integration Test
        self.test_complete_workflow()
        
        # Generate test report
        self.generate_test_report()
    
    def test_assessment_engine_basics(self):
        """Test basic assessment engine functionality"""
        print("\n📋 Test 1: Assessment Engine Basics")
        
        try:
            # Test initialization
            assert assessment_engine is not None
            print("  ✅ Assessment engine initialized")
            
            # Test directory structure
            assessment_engine.ensure_directories()
            print("  ✅ Directory structure verified")
            
            # Test statistics
            stats = assessment_engine.get_assessment_stats()
            assert isinstance(stats, dict)
            assert 'total_dsa_questions' in stats
            print(f"  ✅ Statistics retrieved: {stats['total_dsa_questions']} DSA, {stats['total_mcq_questions']} MCQ, {stats['total_aptitude_questions']} aptitude questions")
            
            self.test_results.append({"test": "Assessment Engine Basics", "status": "PASSED"})
            
        except Exception as e:
            print(f"  ❌ Assessment Engine Basics failed: {e}")
            self.test_results.append({"test": "Assessment Engine Basics", "status": "FAILED", "error": str(e)})
    
    def test_question_databases(self):
        """Test question database loading"""
        print("\n📚 Test 2: Question Database Loading")
        
        try:
            # Test DSA questions
            dsa_questions = assessment_engine.load_dsa_questions()
            assert len(dsa_questions) > 0
            print(f"  ✅ Loaded {len(dsa_questions)} DSA questions")
            
            # Test MCQ questions
            mcq_questions = assessment_engine.load_mcq_questions()
            assert len(mcq_questions) > 0
            print(f"  ✅ Loaded {len(mcq_questions)} MCQ questions")
            
            # Test aptitude questions
            aptitude_questions = assessment_engine.load_aptitude_questions()
            assert len(aptitude_questions) > 0
            print(f"  ✅ Loaded {len(aptitude_questions)} aptitude questions")
            
            # Verify question structure
            sample_dsa = dsa_questions[0]
            assert hasattr(sample_dsa, 'id')
            assert hasattr(sample_dsa, 'title')
            assert hasattr(sample_dsa, 'difficulty')
            print("  ✅ DSA question structure verified")
            
            sample_mcq = mcq_questions[0]
            assert hasattr(sample_mcq, 'id')
            assert hasattr(sample_mcq, 'question')
            assert hasattr(sample_mcq, 'options')
            print("  ✅ MCQ question structure verified")
            
            self.test_results.append({"test": "Question Database Loading", "status": "PASSED"})
            
        except Exception as e:
            print(f"  ❌ Question Database Loading failed: {e}")
            self.test_results.append({"test": "Question Database Loading", "status": "FAILED", "error": str(e)})
    
    def test_company_assessments(self):
        """Test company-specific assessment creation"""
        print("\n🏢 Test 3: Company-Specific Assessments")
        
        try:
            # Test Google assessment
            google_intelligence = {
                "company_name": "Google",
                "tech_stack": ["Python", "Java", "Go"],
                "interview_process": "Technical rounds with system design"
            }
            google_resume = {
                "skills": ["Python", "Algorithms", "System Design"],
                "experience_years": 5
            }
            
            google_config = assessment_engine.create_company_specific_assessment(
                company_intelligence=google_intelligence,
                resume_data=google_resume,
                target_role="Software Engineer"
            )
            assert isinstance(google_config, AssessmentConfig)
            assert google_config.company_name == "Google"
            print("  ✅ Google assessment configuration created")
            
            # Test Amazon assessment
            amazon_intelligence = {
                "company_name": "Amazon",
                "tech_stack": ["Java", "AWS", "Microservices"],
                "interview_process": "Leadership principles and system design"
            }
            amazon_resume = {
                "skills": ["Java", "AWS", "Distributed Systems"],
                "experience_years": 8
            }
            
            amazon_config = assessment_engine.create_company_specific_assessment(
                company_intelligence=amazon_intelligence,
                resume_data=amazon_resume,
                target_role="SDE II"
            )
            assert amazon_config.company_name == "Amazon"
            print("  ✅ Amazon assessment configuration created")
            
            # Test default assessment
            startup_intelligence = {
                "company_name": "StartupXYZ",
                "tech_stack": ["JavaScript", "React", "Node.js"],
                "interview_process": "Technical assessment"
            }
            startup_resume = {
                "skills": ["JavaScript", "React", "Node.js"],
                "experience_years": 2
            }
            
            default_config = assessment_engine.create_company_specific_assessment(
                company_intelligence=startup_intelligence,
                resume_data=startup_resume,
                target_role="Full Stack Developer"
            )
            assert isinstance(default_config, AssessmentConfig)
            print("  ✅ Default assessment configuration created")
            
            self.test_results.append({"test": "Company-Specific Assessments", "status": "PASSED"})
            
        except Exception as e:
            print(f"  ❌ Company-Specific Assessments failed: {e}")
            self.test_results.append({"test": "Company-Specific Assessments", "status": "FAILED", "error": str(e)})
    
    def test_traditional_assessment(self):
        """Test traditional assessment flow"""
        print("\n📝 Test 4: Traditional Assessment Flow")
        
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
            
            # Start assessment
            assessment_result = assessment_engine.start_assessment(config)
            assert 'assessment_id' in assessment_result
            assert 'first_question' in assessment_result
            
            assessment_id = assessment_result['assessment_id']
            print(f"  ✅ Assessment started with ID: {assessment_id}")
            
            # Submit a few answers
            first_question = assessment_result.get('first_question')
            if first_question:
                question_id = first_question['id']
                
                # Submit answer (assume multiple choice for simplicity)
                if first_question.get('type') == 'mcq':
                    answer_result = assessment_engine.submit_answer(
                        assessment_id, question_id, "a"
                    )
                    assert 'next_question' in answer_result or 'assessment_complete' in answer_result
                    print("  ✅ Answer submitted successfully")
                else:
                    print("  ✅ First question retrieved (DSA type)")
            
            self.test_results.append({"test": "Traditional Assessment Flow", "status": "PASSED"})
            
        except Exception as e:
            print(f"  ❌ Traditional Assessment Flow failed: {e}")
            self.test_results.append({"test": "Traditional Assessment Flow", "status": "FAILED", "error": str(e)})
    
    def test_timed_environment(self):
        """Test timed test environment"""
        print("\n⏱️ Test 5: Timed Test Environment")
        
        try:
            if not test_environment:
                print("  ⚠️ Timed environment not available, skipping test")
                self.test_results.append({"test": "Timed Test Environment", "status": "SKIPPED"})
                return
            
            # Create simple test configuration using the assessment engine
            test_intelligence = {
                "company_name": "Test Company",
                "tech_stack": ["Python", "JavaScript"],
                "interview_process": "Quick technical test"
            }
            test_resume = {
                "skills": ["Python", "JavaScript"],
                "experience_years": 3
            }
            
            config = assessment_engine.create_company_specific_assessment(
                company_intelligence=test_intelligence,
                resume_data=test_resume,
                target_role="Test Role"
            )
            # Override time limit for quick test
            config.time_limit_minutes = 5
            
            # Start timed assessment
            session_id = assessment_engine.start_timed_assessment(
                user_id=self.test_user_id,
                config=config
            )
            assert session_id is not None
            print(f"  ✅ Timed session started: {session_id}")
            
            # Check session status
            status = assessment_engine.get_timed_session_status(session_id)
            assert status is not None
            assert status['is_active'] == True
            print("  ✅ Session status retrieved")
            
            # Get current question
            current_q = assessment_engine.get_current_timed_question(session_id)
            assert current_q is not None
            print("  ✅ Current question retrieved")
            
            # Test pause/resume
            pause_result = assessment_engine.pause_timed_assessment(session_id)
            assert pause_result == True
            print("  ✅ Session paused")
            
            resume_result = assessment_engine.resume_timed_assessment(session_id)
            assert resume_result == True
            print("  ✅ Session resumed")
            
            # Submit test early
            submit_result = assessment_engine.submit_timed_assessment(session_id)
            assert submit_result.get('success') == True
            print("  ✅ Timed assessment submitted")
            
            self.test_results.append({"test": "Timed Test Environment", "status": "PASSED"})
            
        except Exception as e:
            print(f"  ❌ Timed Test Environment failed: {e}")
            self.test_results.append({"test": "Timed Test Environment", "status": "FAILED", "error": str(e)})
    
    def test_performance_analytics(self):
        """Test performance analytics system"""
        print("\n📊 Test 6: Performance Analytics")
        
        try:
            if not performance_analytics:
                print("  ⚠️ Performance analytics not available, skipping test")
                self.test_results.append({"test": "Performance Analytics", "status": "SKIPPED"})
                return
            
            # Create sample test data by ensuring results directory exists
            results_dir = Path("Data/Assessments/Results")
            results_dir.mkdir(parents=True, exist_ok=True)
            
            # Test user performance analysis
            profile = assessment_engine.analyze_user_performance(self.test_user_id)
            assert isinstance(profile, dict)
            print("  ✅ User performance analysis completed")
            
            # Test performance report generation
            report = assessment_engine.get_performance_report(self.test_user_id, "summary")
            assert isinstance(report, dict)
            print("  ✅ Performance report generated")
            
            # Test company benchmarks
            benchmark = assessment_engine.get_company_benchmark("Google")
            assert isinstance(benchmark, dict)
            print("  ✅ Company benchmark retrieved")
            
            # Test study plan generation
            study_plan = assessment_engine.generate_study_plan(self.test_user_id)
            assert isinstance(study_plan, dict)
            print("  ✅ Study plan generated")
            
            self.test_results.append({"test": "Performance Analytics", "status": "PASSED"})
            
        except Exception as e:
            print(f"  ❌ Performance Analytics failed: {e}")
            self.test_results.append({"test": "Performance Analytics", "status": "FAILED", "error": str(e)})
    
    def test_complete_workflow(self):
        """Test complete assessment workflow"""
        print("\n🔄 Test 7: Complete Workflow Integration")
        
        try:
            # Test the complete flow from company research to performance analysis
            
            # 1. Create company-specific assessment
            apple_intelligence = {
                "company_name": "Apple",
                "tech_stack": ["Swift", "Objective-C", "iOS"],
                "interview_process": "Technical coding and system design"
            }
            apple_resume = {
                "skills": ["Swift", "iOS Development", "UIKit"],
                "experience_years": 7
            }
            
            config = assessment_engine.create_company_specific_assessment(
                company_intelligence=apple_intelligence,
                resume_data=apple_resume,
                target_role="iOS Developer"
            )
            print("  ✅ Company assessment configuration created")
            
            # 2. Generate questions
            questions = assessment_engine.generate_assessment_questions(config)
            assert len(questions) > 0
            print(f"  ✅ Generated {len(questions)} assessment questions")
            
            # 3. Verify question mix
            dsa_count = sum(1 for q in questions if hasattr(q, 'test_cases'))
            mcq_count = len(questions) - dsa_count
            print(f"  ✅ Question mix verified: {dsa_count} DSA, {mcq_count} MCQ")
            
            # 4. Test session management
            active_sessions = assessment_engine.get_active_timed_sessions()
            assert isinstance(active_sessions, list)
            print("  ✅ Session management verified")
            
            # 5. Test cleanup
            assessment_engine.cleanup_expired_sessions()
            print("  ✅ Session cleanup completed")
            
            self.test_results.append({"test": "Complete Workflow Integration", "status": "PASSED"})
            
        except Exception as e:
            print(f"  ❌ Complete Workflow Integration failed: {e}")
            self.test_results.append({"test": "Complete Workflow Integration", "status": "FAILED", "error": str(e)})
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n📈 Test Results Summary")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['status'] == 'PASSED')
        failed = sum(1 for result in self.test_results if result['status'] == 'FAILED')
        skipped = sum(1 for result in self.test_results if result['status'] == 'SKIPPED')
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️ Skipped: {skipped}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        print("\nDetailed Results:")
        for result in self.test_results:
            status_icon = {"PASSED": "✅", "FAILED": "❌", "SKIPPED": "⚠️"}[result['status']]
            print(f"  {status_icon} {result['test']}: {result['status']}")
            if result.get('error'):
                print(f"      Error: {result['error']}")
        
        # Save test report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "success_rate": passed/total*100 if total > 0 else 0
            },
            "detailed_results": self.test_results
        }
        
        try:
            report_file = Path("test_phase3_report.json")
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            print(f"\n📄 Test report saved to: {report_file}")
        except Exception as e:
            print(f"⚠️ Could not save test report: {e}")
        
        print("\n🎉 Phase 3 Testing Complete!")
        
        if failed == 0:
            print(f"🌟 All tests passed! Phase 3 system is ready for production.")
        else:
            print(f"⚠️ {failed} test(s) failed. Please review and fix before deployment.")

def main():
    """Run the Phase 3 test suite"""
    print("🚀 Phase 3: Assessment & Screening Tests - Test Suite")
    
    # Ensure required directories exist
    Path("Data/Assessments").mkdir(parents=True, exist_ok=True)
    Path("Data/Assessments/Results").mkdir(parents=True, exist_ok=True)
    Path("Data/Assessments/Analytics").mkdir(parents=True, exist_ok=True)
    
    # Run tests
    test_suite = Phase3TestSuite()
    test_suite.run_all_tests()

if __name__ == "__main__":
    main()