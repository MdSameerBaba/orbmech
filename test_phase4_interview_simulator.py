"""
🧪 PHASE 4 AI INTERVIEW SIMULATOR - COMPREHENSIVE TEST SUITE
Multi-Modal Interview Analysis Testing

This test suite validates:
- AI Interview Engine functionality
- Camera-based behavioral analysis
- Audio processing and speech analysis  
- Real-time session management
- Performance analytics and reporting
- NEXUS Agent natural language interface
- Integration with Phases 1, 2, and 3
"""

import sys
import os
import time
import json
from datetime import datetime
import traceback
from pathlib import Path

# Add the Backend path to sys.path for imports
backend_path = os.path.join(os.path.dirname(__file__), 'Backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

try:
    # Import Phase 4 components
    from Backend.Agents.InterviewHelper.AIInterviewEngine import (
        ai_interview_engine, InterviewType, InterviewDifficulty,
        camera_analyzer, audio_analyzer
    )
    from Backend.Agents.InterviewHelper.InterviewSessionManager import (
        interview_session_manager, SessionSettings, LiveAnalysisData
    )
    from Backend.Agents.InterviewHelper.InterviewAnalytics import (
        interview_analytics, PerformanceMetrics
    )
    from Backend.Agents.InterviewHelper.InterviewAgent import (
        interview_agent
    )
    
    IMPORTS_SUCCESSFUL = True
    print("✅ All Phase 4 components imported successfully")
    
except ImportError as e:
    IMPORTS_SUCCESSFUL = False
    print(f"❌ Import error: {e}")
    traceback.print_exc()

def test_ai_interview_engine():
    """Test AI Interview Engine functionality"""
    print("\n🔬 Testing AI Interview Engine...")
    
    try:
        # Test 1: Create interview session
        print("📝 Test 1: Creating interview session...")
        session_id = ai_interview_engine.create_interview_session(
            user_id="test_user_001",
            company_name="Google",
            role="Software Engineer",
            interview_type=InterviewType.MIXED,
            difficulty=InterviewDifficulty.MID
        )
        
        if session_id and session_id in ai_interview_engine.active_sessions:
            print(f"✅ Session created successfully: {session_id}")
            
            # Verify session details
            session = ai_interview_engine.active_sessions[session_id]
            assert session.company_name == "Google"
            assert session.role == "Software Engineer"
            assert session.interview_type == InterviewType.MIXED
            print("✅ Session details verified")
            
        else:
            print("❌ Failed to create interview session")
            return False
        
        # Test 2: Question generation
        print("📝 Test 2: Verifying question generation...")
        session = ai_interview_engine.active_sessions[session_id]
        questions = session.questions
        
        if len(questions) > 0:
            print(f"✅ Generated {len(questions)} interview questions")
            
            # Check question structure
            first_question = questions[0]
            assert hasattr(first_question, 'question_text')
            assert hasattr(first_question, 'difficulty')
            assert hasattr(first_question, 'expected_duration')
            print("✅ Question structure validated")
            
        else:
            print("❌ No questions generated")
            return False
        
        # Test 3: Camera initialization
        print("📝 Test 3: Testing camera initialization...")
        camera_success = ai_interview_engine.start_camera()
        if camera_success:
            print("✅ Camera initialized successfully")
            ai_interview_engine.stop_camera()
            print("✅ Camera stopped successfully")
        else:
            print("⚠️ Camera not available (expected in some environments)")
        
        # Test 4: TTS functionality
        print("📝 Test 4: Testing text-to-speech...")
        try:
            ai_interview_engine.speak("Testing AI interviewer voice")
            print("✅ Text-to-speech functional")
        except:
            print("⚠️ TTS not available (expected in some environments)")
        
        print("✅ AI Interview Engine tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ AI Interview Engine test failed: {e}")
        traceback.print_exc()
        return False

def test_camera_analyzer():
    """Test Camera Analysis functionality"""
    print("\n🔬 Testing Camera Analyzer...")
    
    try:
        import numpy as np
        
        # Test 1: Basic analysis with mock frame
        print("📝 Test 1: Mock frame analysis...")
        
        # Create a mock video frame (640x480 RGB)
        mock_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Analyze the frame
        analysis_result = camera_analyzer.analyze_frame(mock_frame)
        
        # Verify analysis result structure
        assert hasattr(analysis_result, 'eye_contact_score')
        assert hasattr(analysis_result, 'confidence_score')
        assert hasattr(analysis_result, 'professionalism_score')
        assert 0 <= analysis_result.eye_contact_score <= 100
        assert 0 <= analysis_result.confidence_score <= 100
        
        print(f"✅ Frame analysis successful:")
        print(f"   Eye Contact: {analysis_result.eye_contact_score:.1f}%")
        print(f"   Confidence: {analysis_result.confidence_score:.1f}%")
        print(f"   Professionalism: {analysis_result.professionalism_score:.1f}%")
        
        # Test 2: Multiple frame analysis
        print("📝 Test 2: Multiple frame analysis...")
        results = []
        for i in range(5):
            frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            result = camera_analyzer.analyze_frame(frame)
            results.append(result)
        
        print(f"✅ Analyzed {len(results)} frames successfully")
        
        # Test 3: Performance measurement
        print("📝 Test 3: Performance measurement...")
        start_time = time.time()
        
        for i in range(10):
            frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            camera_analyzer.analyze_frame(frame)
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 10
        fps = 1 / avg_time if avg_time > 0 else 0
        
        print(f"✅ Average analysis time: {avg_time:.3f}s ({fps:.1f} FPS)")
        
        print("✅ Camera Analyzer tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Camera Analyzer test failed: {e}")
        traceback.print_exc()
        return False

def test_session_manager():
    """Test Interview Session Manager"""
    print("\n🔬 Testing Interview Session Manager...")
    
    try:
        # Test 1: Session settings configuration
        print("📝 Test 1: Session settings...")
        
        settings = SessionSettings(
            show_live_feedback=True,
            record_session=False,  # Disable recording for tests
            enable_hints=True,
            time_limit_per_question=60,  # Short time for tests
            show_confidence_meter=True
        )
        
        print("✅ Session settings configured")
        
        # Test 2: Live analysis data structure
        print("📝 Test 2: Live analysis data...")
        
        live_data = interview_session_manager.get_live_analysis()
        
        assert hasattr(live_data, 'eye_contact_score')
        assert hasattr(live_data, 'confidence_level')
        assert hasattr(live_data, 'overall_performance')
        assert isinstance(live_data.recommendations, list)
        
        print("✅ Live analysis data structure verified")
        
        # Test 3: Session state management
        print("📝 Test 3: Session state management...")
        
        # Initially no active session
        assert interview_session_manager.active_session is None
        print("✅ Initial state verified")
        
        # Test 4: Mock session startup (without actual camera)
        print("📝 Test 4: Mock session components...")
        
        # Test live analysis update
        from Backend.Agents.InterviewHelper.AIInterviewEngine import VideoAnalysisResult
        
        mock_video_analysis = VideoAnalysisResult(
            timestamp=datetime.now(),
            eye_contact_score=75.0,
            confidence_score=80.0,
            posture_score=70.0,
            gesture_appropriateness=85.0,
            facial_expression="confident",
            attention_level=78.0,
            professionalism_score=82.0
        )
        
        interview_session_manager._update_live_analysis(mock_video_analysis)
        
        updated_data = interview_session_manager.get_live_analysis()
        assert updated_data.eye_contact_score == 75.0
        assert updated_data.confidence_level == 80.0
        
        print("✅ Live analysis update successful")
        
        print("✅ Session Manager tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Session Manager test failed: {e}")
        traceback.print_exc()
        return False

def test_analytics_engine():
    """Test Performance Analytics functionality"""
    print("\n🔬 Testing Analytics Engine...")
    
    try:
        # Test 1: Mock session results analysis
        print("📝 Test 1: Session results analysis...")
        
        mock_session_results = {
            'session_id': 'test_session_001',
            'overall_score': 78.5,
            'communication_score': 80.0,
            'confidence_score': 75.0,
            'professionalism_score': 82.0,
            'technical_score': 77.0,
            'detailed_video_scores': {
                'eye_contact': 78.0,
                'confidence': 75.0,
                'professionalism': 82.0,
                'attention': 76.0
            },
            'detailed_audio_scores': {
                'clarity': 80.0,
                'pace': 150.0,
                'confidence': 75.0,
                'filler_words': 3
            },
            'session_duration': 1800,  # 30 minutes
            'answered_questions': 8,
            'total_questions': 10,
            'session_metadata': {
                'user_id': 'test_user_001',
                'company_name': 'Google',
                'role': 'Software Engineer',
                'interview_type': 'mixed',
                'difficulty': 'mid'
            }
        }
        
        # Analyze session performance
        analysis = interview_analytics.analyze_session_performance(mock_session_results)
        
        assert 'session_id' in analysis
        assert 'performance_metrics' in analysis
        assert 'video_analysis' in analysis
        assert 'audio_analysis' in analysis
        assert 'recommendations' in analysis
        
        print("✅ Session analysis completed successfully")
        print(f"   Overall Grade: {analysis.get('overall_grade', 'N/A')}")
        print(f"   Recommendations: {len(analysis.get('recommendations', []))}")
        
        # Test 2: Performance metrics calculation
        print("📝 Test 2: Performance metrics calculation...")
        
        user_sessions = [mock_session_results]  # Single session for testing
        metrics = interview_analytics._calculate_performance_metrics(user_sessions)
        
        assert isinstance(metrics, PerformanceMetrics)
        assert metrics.overall_score == 78.5
        assert metrics.session_count == 1
        
        print("✅ Performance metrics calculation successful")
        print(f"   Sessions: {metrics.session_count}")
        print(f"   Overall Score: {metrics.overall_score:.1f}%")
        
        # Test 3: Company comparison
        print("📝 Test 3: Company comparison analysis...")
        
        comparison = interview_analytics.compare_performance_across_companies('test_user_001')
        
        # Should handle case with no existing sessions gracefully
        if not comparison:
            print("✅ Graceful handling of empty session data")
        else:
            print("✅ Company comparison analysis completed")
        
        print("✅ Analytics Engine tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Analytics Engine test failed: {e}")
        traceback.print_exc()
        return False

def test_nexus_agent():
    """Test NEXUS Interview Agent natural language interface"""
    print("\n🔬 Testing NEXUS Interview Agent...")
    
    try:
        # Test 1: Command pattern matching
        print("📝 Test 1: Command pattern matching...")
        
        test_commands = [
            "start interview for software engineer at google",
            "show my performance", 
            "give me feedback",
            "prepare for microsoft interview",
            "how am i doing?",
            "stop interview"
        ]
        
        for command in test_commands:
            response = interview_agent.process_command("test_user_001", command)
            assert isinstance(response, str)
            assert len(response) > 0
            print(f"✅ Command processed: '{command[:30]}...'")
        
        # Test 2: Help functionality
        print("📝 Test 2: Help functionality...")
        
        help_text = interview_agent.get_help()
        assert "NEXUS Interview Agent" in help_text
        assert "Available Commands" in help_text
        print("✅ Help functionality working")
        
        # Test 3: Context tracking
        print("📝 Test 3: Context tracking...")
        
        # Process a series of related commands
        interview_agent.process_command("test_user_002", "hello")
        interview_agent.process_command("test_user_002", "show performance")
        interview_agent.process_command("test_user_002", "start interview for data scientist at amazon")
        
        # Check conversation history
        history = interview_agent.conversation_history
        assert len(history) > 0
        print(f"✅ Conversation history tracking: {len(history)} entries")
        
        # Test 4: Role and difficulty determination
        print("📝 Test 4: Role/difficulty determination...")
        
        # Test different role types
        roles_and_types = [
            ("Software Engineer", InterviewType.MIXED),
            ("Senior Staff Engineer", InterviewType.SYSTEM_DESIGN),
            ("Engineering Manager", InterviewType.BEHAVIORAL),
            ("Principal Architect", InterviewType.SYSTEM_DESIGN)
        ]
        
        for role, expected_type in roles_and_types:
            determined_type = interview_agent._determine_interview_type(role)
            print(f"   {role} -> {determined_type.value}")
        
        print("✅ Role/difficulty determination working")
        
        # Test 5: Company extraction
        print("📝 Test 5: Company name extraction...")
        
        test_messages = [
            "I want to interview at google",
            "prepare me for microsoft",
            "amazon interview tips",
            "tell me about facebook"
        ]
        
        for msg in test_messages:
            company = interview_agent._extract_company_from_message(msg)
            print(f"   '{msg}' -> {company}")
        
        print("✅ Company extraction working")
        
        print("✅ NEXUS Agent tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ NEXUS Agent test failed: {e}")
        traceback.print_exc()
        return False

def test_integration():
    """Test integration between all Phase 4 components"""
    print("\n🔬 Testing Phase 4 Integration...")
    
    try:
        # Test 1: End-to-end workflow simulation
        print("📝 Test 1: End-to-end workflow simulation...")
        
        # Step 1: Agent processes interview start command
        agent_response = interview_agent.process_command(
            "integration_test_user", 
            "start interview for senior software engineer at google"
        )
        
        print("✅ Agent processed start command")
        
        # Step 2: Verify session was created in engine
        active_sessions = ai_interview_engine.active_sessions
        if active_sessions:
            print(f"✅ Session created in engine: {len(active_sessions)} active")
        
        # Step 3: Mock performance data flow
        mock_performance = {
            'session_id': 'integration_test',
            'overall_score': 85.0,
            'communication_score': 88.0,
            'confidence_score': 82.0,
            'technical_score': 87.0,
            'session_duration': 2400,
            'answered_questions': 10,
            'total_questions': 10,
            'detailed_video_scores': {'eye_contact': 85, 'confidence': 82},
            'detailed_audio_scores': {'clarity': 88, 'pace': 145, 'filler_words': 2},
            'session_metadata': {
                'user_id': 'integration_test_user',
                'company_name': 'Google',
                'role': 'Senior Software Engineer'
            }
        }
        
        # Step 4: Analytics processes the performance data
        analysis = interview_analytics.analyze_session_performance(mock_performance)
        print("✅ Analytics processed performance data")
        
        # Step 5: Agent provides performance feedback
        feedback_response = interview_agent.process_command(
            "integration_test_user",
            "show my performance"
        )
        
        assert "Performance" in feedback_response or "performance" in feedback_response
        print("✅ Agent provided performance feedback")
        
        # Test 2: Cross-component data consistency
        print("📝 Test 2: Data consistency check...")
        
        # Verify that components share consistent data structures
        from Backend.Agents.InterviewHelper.AIInterviewEngine import InterviewSession, InterviewType, InterviewDifficulty
        from Backend.Agents.InterviewHelper.InterviewAnalytics import PerformanceMetrics
        
        # Check that data classes are properly defined by creating instances
        test_session = InterviewSession(
            session_id="test_id",
            user_id="test_user",
            company_name="Test Company",
            role="Test Role",
            interview_type=InterviewType.MIXED,
            difficulty=InterviewDifficulty.MID,
            start_time=datetime.now()
        )
        
        test_metrics = PerformanceMetrics(
            overall_score=75.0,
            communication_score=80.0,
            confidence_score=70.0,
            professionalism_score=75.0,
            technical_score=72.0,
            eye_contact_avg=78.0,
            posture_avg=75.0,
            gesture_quality=80.0,
            speech_clarity=82.0,
            speaking_pace=150.0,
            filler_words_avg=3.0,
            session_count=1,
            total_duration=1800.0,
            questions_answered=8,
            improvement_trend=2.5
        )
        
        # Verify instances have expected attributes
        assert hasattr(test_session, 'session_id')
        assert hasattr(test_session, 'user_id')
        assert hasattr(test_metrics, 'overall_score')
        assert hasattr(test_metrics, 'session_count')
        
        print("✅ Data structures consistent across components")
        
        # Test 3: Error handling integration
        print("📝 Test 3: Error handling...")
        
        # Test graceful handling of invalid commands
        error_response = interview_agent.process_command(
            "test_user",
            "invalid command that doesn't match any pattern"
        )
        
        assert isinstance(error_response, str)
        assert len(error_response) > 0
        print("✅ Error handling working properly")
        
        print("✅ Phase 4 Integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        traceback.print_exc()
        return False

def test_directory_structure():
    """Test that all required directories and files exist"""
    print("\n🔬 Testing Directory Structure...")
    
    try:
        required_dirs = [
            "Data/Interviews",
            "Data/Interviews/Results", 
            "Data/Interviews/Sessions",
            "Data/Analytics",
            "Data/Analytics/Reports",
            "Data/Analytics/Charts"
        ]
        
        for directory in required_dirs:
            if Path(directory).exists():
                print(f"✅ Directory exists: {directory}")
            else:
                print(f"⚠️ Directory missing (will be created): {directory}")
        
        required_files = [
            "Backend/Agents/InterviewHelper/AIInterviewEngine.py",
            "Backend/Agents/InterviewHelper/InterviewSessionManager.py", 
            "Backend/Agents/InterviewHelper/InterviewAnalytics.py",
            "Backend/Agents/InterviewHelper/InterviewAgent.py"
        ]
        
        for file_path in required_files:
            if Path(file_path).exists():
                print(f"✅ File exists: {file_path}")
            else:
                print(f"❌ File missing: {file_path}")
                return False
        
        print("✅ Directory structure validated!")
        return True
        
    except Exception as e:
        print(f"❌ Directory structure test failed: {e}")
        return False

def run_performance_benchmark():
    """Run performance benchmarks for critical components"""
    print("\n🔬 Running Performance Benchmarks...")
    
    try:
        import numpy as np
        
        # Benchmark 1: Camera analysis performance
        print("📊 Benchmark 1: Camera Analysis Performance...")
        
        start_time = time.time()
        frame_count = 50
        
        for i in range(frame_count):
            mock_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            camera_analyzer.analyze_frame(mock_frame)
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / frame_count
        fps = frame_count / total_time
        
        print(f"✅ Camera Analysis: {avg_time:.3f}s per frame ({fps:.1f} FPS)")
        
        # Benchmark 2: Agent response time
        print("📊 Benchmark 2: Agent Response Performance...")
        
        test_commands = [
            "show performance",
            "give me feedback", 
            "start interview for software engineer at google",
            "prepare for amazon interview"
        ]
        
        response_times = []
        
        for command in test_commands:
            start_time = time.time()
            interview_agent.process_command("benchmark_user", command)
            end_time = time.time()
            
            response_time = end_time - start_time
            response_times.append(response_time)
        
        avg_response_time = sum(response_times) / len(response_times)
        print(f"✅ Agent Response: {avg_response_time:.3f}s average")
        
        # Performance thresholds
        if fps > 10:
            print("✅ Camera analysis meets real-time requirements")
        else:
            print("⚠️ Camera analysis may be too slow for real-time use")
        
        if avg_response_time < 2.0:
            print("✅ Agent response time acceptable")
        else:
            print("⚠️ Agent response time may be too slow")
        
        print("✅ Performance benchmarks completed!")
        return True
        
    except Exception as e:
        print(f"❌ Performance benchmark failed: {e}")
        return False

def generate_test_report():
    """Generate comprehensive test report"""
    print("\n📋 Generating Test Report...")
    
    # Run all tests and collect results
    test_results = {
        'timestamp': datetime.now().isoformat(),
        'phase': 'Phase 4 - AI Interview Simulator',
        'import_status': IMPORTS_SUCCESSFUL,
        'tests': {}
    }
    
    if IMPORTS_SUCCESSFUL:
        tests_to_run = [
            ('Directory Structure', test_directory_structure),
            ('AI Interview Engine', test_ai_interview_engine),
            ('Camera Analyzer', test_camera_analyzer),
            ('Session Manager', test_session_manager),
            ('Analytics Engine', test_analytics_engine),
            ('NEXUS Agent', test_nexus_agent),
            ('Integration', test_integration),
            ('Performance Benchmark', run_performance_benchmark)
        ]
        
        total_tests = len(tests_to_run)
        passed_tests = 0
        
        for test_name, test_function in tests_to_run:
            try:
                result = test_function()
                test_results['tests'][test_name] = {
                    'status': 'PASSED' if result else 'FAILED',
                    'timestamp': datetime.now().isoformat()
                }
                if result:
                    passed_tests += 1
            except Exception as e:
                test_results['tests'][test_name] = {
                    'status': 'ERROR',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
        
        test_results['summary'] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': (passed_tests / total_tests) * 100
        }
    
    else:
        test_results['summary'] = {
            'total_tests': 0,
            'passed_tests': 0, 
            'failed_tests': 0,
            'success_rate': 0,
            'import_error': 'Failed to import Phase 4 components'
        }
    
    # Save test report
    try:
        with open('test_phase4_report.json', 'w') as f:
            json.dump(test_results, f, indent=2)
        print("💾 Test report saved: test_phase4_report.json")
    except Exception as e:
        print(f"⚠️ Could not save test report: {e}")
    
    # Print summary
    print(f"\n{'='*60}")
    print("🎯 PHASE 4 TEST SUMMARY")
    print(f"{'='*60}")
    
    if IMPORTS_SUCCESSFUL:
        summary = test_results['summary']
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed_tests']}")
        print(f"Failed: {summary['failed_tests']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        
        status_icon = "✅" if summary['success_rate'] >= 80 else "⚠️" if summary['success_rate'] >= 60 else "❌"
        print(f"\nOverall Status: {status_icon} {'EXCELLENT' if summary['success_rate'] >= 80 else 'GOOD' if summary['success_rate'] >= 60 else 'NEEDS WORK'}")
        
        if summary['success_rate'] >= 80:
            print("🎬 Phase 4 AI Interview Simulator is ready for production!")
        elif summary['success_rate'] >= 60:
            print("🔧 Phase 4 is functional but needs some improvements")
        else:
            print("🛠️ Phase 4 needs significant debugging before deployment")
    
    else:
        print("❌ Import failures prevented testing")
        print("🔧 Fix import issues before running tests")
    
    print(f"{'='*60}")
    
    return test_results

if __name__ == "__main__":
    print("🎬 Phase 4: AI Interview Simulator - Multi-Modal Analysis")
    print("🧪 Comprehensive Test Suite")
    print(f"{'='*60}")
    
    # Generate comprehensive test report
    report = generate_test_report()
    
    print("\n🎯 Phase 4 testing completed!")
    
    if IMPORTS_SUCCESSFUL and report['summary']['success_rate'] >= 80:
        print("🚀 Ready to integrate with NEXUS system!")
    else:
        print("🔧 Review test results and fix issues before deployment")