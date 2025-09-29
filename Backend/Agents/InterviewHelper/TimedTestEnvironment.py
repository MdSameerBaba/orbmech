"""
Timed Test Environment for Interactive Assessment Management
Handles real-time test execution, timing, and user interaction during assessments.
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
import threading
from queue import Queue, Empty

@dataclass
class TestSession:
    """Active test session with timing and state management"""
    session_id: str
    user_id: str
    test_config: Dict[str, Any]
    questions: List[Dict[str, Any]]
    start_time: datetime
    time_limit: int  # minutes
    current_question: int
    responses: Dict[str, Any]
    is_active: bool
    paused_time: int = 0
    warnings_sent: List[str] = None
    
    def __post_init__(self):
        if self.warnings_sent is None:
            self.warnings_sent = []
    
    @property
    def elapsed_time(self) -> int:
        """Get elapsed time in seconds"""
        if not self.is_active:
            return self.paused_time
        return int((datetime.now() - self.start_time).total_seconds()) + self.paused_time
    
    @property
    def remaining_time(self) -> int:
        """Get remaining time in seconds"""
        total_seconds = self.time_limit * 60
        return max(0, total_seconds - self.elapsed_time)
    
    @property
    def progress_percentage(self) -> float:
        """Get test completion percentage"""
        if not self.questions:
            return 0.0
        return (len(self.responses) / len(self.questions)) * 100

class TimedTestEnvironment:
    """
    Manages timed test sessions with real-time monitoring and interaction.
    Provides timer management, auto-submission, and progress tracking.
    """
    
    def __init__(self):
        self.active_sessions: Dict[str, TestSession] = {}
        self.session_callbacks: Dict[str, Dict[str, Callable]] = {}
        self._running = True
        self._monitor_thread = None
        self._start_monitor()
    
    def _start_monitor(self):
        """Start background monitoring thread"""
        def monitor_loop():
            while self._running:
                try:
                    self._check_all_sessions()
                    time.sleep(1)  # Check every second
                except Exception as e:
                    print(f"Monitor error: {e}")
        
        self._monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self._monitor_thread.start()
    
    def _check_all_sessions(self):
        """Check all active sessions for time warnings and auto-submission"""
        current_sessions = list(self.active_sessions.items())
        
        for session_id, session in current_sessions:
            if not session.is_active:
                continue
            
            remaining = session.remaining_time
            
            # Send time warnings
            self._send_time_warnings(session_id, session, remaining)
            
            # Auto-submit if time expired
            if remaining <= 0:
                self._auto_submit_test(session_id, session)
    
    def _send_time_warnings(self, session_id: str, session: TestSession, remaining: int):
        """Send time warning notifications"""
        warnings = [
            (300, "5_minutes"),  # 5 minutes
            (120, "2_minutes"),  # 2 minutes
            (60, "1_minute"),    # 1 minute
            (30, "30_seconds")   # 30 seconds
        ]
        
        for threshold, warning_key in warnings:
            if remaining <= threshold and warning_key not in session.warnings_sent:
                session.warnings_sent.append(warning_key)
                self._trigger_callback(session_id, "time_warning", {
                    "remaining_time": remaining,
                    "warning_type": warning_key,
                    "message": f"⚠️ {threshold // 60 if threshold >= 60 else threshold} {'minute(s)' if threshold >= 60 else 'seconds'} remaining!"
                })
    
    def _auto_submit_test(self, session_id: str, session: TestSession):
        """Auto-submit test when time expires"""
        session.is_active = False
        
        # Calculate final results
        results = self._calculate_results(session)
        
        self._trigger_callback(session_id, "auto_submit", {
            "reason": "time_expired",
            "results": results,
            "message": "⏰ Time expired! Test has been automatically submitted."
        })
        
        # Archive session
        self._archive_session(session_id, session, results)
    
    def _trigger_callback(self, session_id: str, event: str, data: Dict[str, Any]):
        """Trigger registered callbacks for session events"""
        if session_id in self.session_callbacks:
            callback_func = self.session_callbacks[session_id].get(event)
            if callback_func:
                try:
                    callback_func(data)
                except Exception as e:
                    print(f"Callback error for {event}: {e}")
    
    def create_test_session(self, 
                          user_id: str, 
                          test_config: Dict[str, Any],
                          questions: List[Dict[str, Any]],
                          callbacks: Optional[Dict[str, Callable]] = None) -> str:
        """Create new timed test session"""
        session_id = f"test_{user_id}_{int(time.time())}"
        
        session = TestSession(
            session_id=session_id,
            user_id=user_id,
            test_config=test_config,
            questions=questions,
            start_time=datetime.now(),
            time_limit=test_config.get('time_limit', 60),
            current_question=0,
            responses={},
            is_active=True
        )
        
        self.active_sessions[session_id] = session
        
        if callbacks:
            self.session_callbacks[session_id] = callbacks
        
        return session_id
    
    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get current session status and timing information"""
        session = self.active_sessions.get(session_id)
        if not session:
            return None
        
        return {
            "session_id": session_id,
            "is_active": session.is_active,
            "current_question": session.current_question,
            "total_questions": len(session.questions),
            "elapsed_time": session.elapsed_time,
            "remaining_time": session.remaining_time,
            "progress_percentage": session.progress_percentage,
            "responses_count": len(session.responses),
            "time_limit": session.time_limit
        }
    
    def submit_answer(self, session_id: str, question_id: str, answer: Any, 
                     time_taken: Optional[int] = None) -> Dict[str, Any]:
        """Submit answer for current question"""
        session = self.active_sessions.get(session_id)
        if not session or not session.is_active:
            return {"error": "Session not active"}
        
        if session.remaining_time <= 0:
            return {"error": "Time expired"}
        
        # Record response
        session.responses[question_id] = {
            "answer": answer,
            "timestamp": datetime.now().isoformat(),
            "time_taken": time_taken or 0,
            "question_number": session.current_question + 1
        }
        
        # Move to next question
        session.current_question += 1
        
        # Check if test completed
        if session.current_question >= len(session.questions):
            return self._complete_test(session_id)
        
        return {
            "success": True,
            "current_question": session.current_question,
            "progress": session.progress_percentage,
            "remaining_time": session.remaining_time
        }
    
    def get_current_question(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get current question for active session"""
        session = self.active_sessions.get(session_id)
        if not session or not session.is_active:
            return None
        
        if session.current_question >= len(session.questions):
            return None
        
        question = session.questions[session.current_question].copy()
        
        # Add session context
        question.update({
            "question_number": session.current_question + 1,
            "total_questions": len(session.questions),
            "remaining_time": session.remaining_time,
            "progress": session.progress_percentage
        })
        
        return question
    
    def pause_session(self, session_id: str) -> bool:
        """Pause active session (if allowed)"""
        session = self.active_sessions.get(session_id)
        if not session or not session.is_active:
            return False
        
        session.paused_time = session.elapsed_time
        session.is_active = False
        
        self._trigger_callback(session_id, "paused", {
            "paused_at": datetime.now().isoformat(),
            "elapsed_time": session.paused_time
        })
        
        return True
    
    def resume_session(self, session_id: str) -> bool:
        """Resume paused session"""
        session = self.active_sessions.get(session_id)
        if not session or session.is_active:
            return False
        
        session.start_time = datetime.now()
        session.is_active = True
        
        self._trigger_callback(session_id, "resumed", {
            "resumed_at": datetime.now().isoformat(),
            "remaining_time": session.remaining_time
        })
        
        return True
    
    def submit_test(self, session_id: str) -> Dict[str, Any]:
        """Manually submit test before time expires"""
        session = self.active_sessions.get(session_id)
        if not session or not session.is_active:
            return {"error": "Session not active"}
        
        return self._complete_test(session_id)
    
    def _complete_test(self, session_id: str) -> Dict[str, Any]:
        """Complete test and calculate results"""
        session = self.active_sessions[session_id]
        session.is_active = False
        
        results = self._calculate_results(session)
        
        self._trigger_callback(session_id, "completed", {
            "completion_type": "manual",
            "results": results
        })
        
        # Archive session
        self._archive_session(session_id, session, results)
        
        return {
            "success": True,
            "results": results,
            "completion_time": datetime.now().isoformat()
        }
    
    def _calculate_results(self, session: TestSession) -> Dict[str, Any]:
        """Calculate comprehensive test results"""
        total_questions = len(session.questions)
        answered_questions = len(session.responses)
        
        # Calculate scores by category
        category_scores = {}
        correct_answers = 0
        total_score = 0
        
        for question in session.questions:
            question_id = question.get('id', '')
            category = question.get('category', 'GENERAL')
            
            if category not in category_scores:
                category_scores[category] = {
                    'correct': 0,
                    'total': 0,
                    'questions': []
                }
            
            category_scores[category]['total'] += 1
            category_scores[category]['questions'].append(question_id)
            
            if question_id in session.responses:
                user_answer = session.responses[question_id]['answer']
                
                # Check if answer is correct based on question type
                is_correct = self._check_answer_correctness(question, user_answer)
                
                if is_correct:
                    correct_answers += 1
                    category_scores[category]['correct'] += 1
                    total_score += 1
        
        # Calculate percentages
        overall_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        category_percentages = {}
        for category, scores in category_scores.items():
            percentage = (scores['correct'] / scores['total'] * 100) if scores['total'] > 0 else 0
            category_percentages[category] = {
                'percentage': round(percentage, 2),
                'correct': scores['correct'],
                'total': scores['total']
            }
        
        return {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "total_questions": total_questions,
            "answered_questions": answered_questions,
            "correct_answers": correct_answers,
            "overall_percentage": round(overall_percentage, 2),
            "category_breakdown": category_percentages,
            "time_taken": session.elapsed_time,
            "time_limit": session.time_limit * 60,
            "completion_rate": round((answered_questions / total_questions * 100), 2),
            "test_config": session.test_config,
            "started_at": session.start_time.isoformat(),
            "completed_at": datetime.now().isoformat()
        }
    
    def _check_answer_correctness(self, question: Dict[str, Any], user_answer: Any) -> bool:
        """Check if user answer is correct based on question type"""
        question_type = question.get('type', 'MCQ')
        
        if question_type == 'MCQ':
            # Multiple choice - check against correct option
            correct_option = None
            for option in question.get('options', []):
                if option.get('is_correct', False):
                    correct_option = option.get('id')
                    break
            return user_answer == correct_option
        
        elif question_type == 'DSA':
            # For coding problems, this would need code execution
            # For now, assume manual evaluation or simplified checking
            return user_answer.get('passed_tests', 0) > 0
        
        else:
            # Default case
            return str(user_answer).lower() == str(question.get('correct_answer', '')).lower()
    
    def _archive_session(self, session_id: str, session: TestSession, results: Dict[str, Any]):
        """Archive completed session data"""
        try:
            archive_dir = Path("Data/Assessments/Results")
            archive_dir.mkdir(exist_ok=True)
            
            archive_data = {
                "session": asdict(session),
                "results": results,
                "archived_at": datetime.now().isoformat()
            }
            
            archive_file = archive_dir / f"{session_id}_results.json"
            with open(archive_file, 'w') as f:
                json.dump(archive_data, f, indent=2, default=str)
            
            # Remove from active sessions
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
            if session_id in self.session_callbacks:
                del self.session_callbacks[session_id]
                
        except Exception as e:
            print(f"Error archiving session {session_id}: {e}")
    
    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Get list of all active sessions"""
        return [
            {
                "session_id": session_id,
                "user_id": session.user_id,
                "start_time": session.start_time.isoformat(),
                "elapsed_time": session.elapsed_time,
                "remaining_time": session.remaining_time,
                "progress": session.progress_percentage,
                "is_active": session.is_active
            }
            for session_id, session in self.active_sessions.items()
        ]
    
    def cleanup_expired_sessions(self):
        """Clean up expired or abandoned sessions"""
        expired_sessions = []
        
        for session_id, session in self.active_sessions.items():
            # Mark as expired if inactive for too long
            if not session.is_active or session.remaining_time <= 0:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            session = self.active_sessions[session_id]
            results = self._calculate_results(session)
            self._archive_session(session_id, session, results)
    
    def shutdown(self):
        """Shutdown the test environment and clean up resources"""
        self._running = False
        
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=5)
        
        # Archive all active sessions
        for session_id in list(self.active_sessions.keys()):
            session = self.active_sessions[session_id]
            results = self._calculate_results(session)
            self._archive_session(session_id, session, results)

# Global instance for use across the application
test_environment = TimedTestEnvironment()