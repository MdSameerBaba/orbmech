"""
🧪 Assessment & Screening Tests Engine
Phase 3 of the 4-Phase Interview Helper System

This module handles:
- Company-specific assessment creation based on Phase 1 intelligence
- DSA challenges with varying difficulty levels
- Technical MCQs customized for roles and technologies
- Aptitude tests including quantitative, logical, and verbal reasoning
- Timed test environments simulating real screening rounds
- Performance analysis and improvement recommendations
"""

import json
import os
import random
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple, Any, Union
from enum import Enum
from groq import Groq
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
GROQ_API_KEY = env_vars.get("GroqAPIKey")

# Import timed test environment and performance analytics
try:
    from .TimedTestEnvironment import test_environment, TimedTestEnvironment
    from .PerformanceAnalytics import performance_analytics, PerformanceAnalytics
except ImportError:
    # Fallback for direct execution
    test_environment = None
    performance_analytics = None

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"❌ Failed to initialize Groq client: {e}")
    client = None

class AssessmentType(Enum):
    DSA_CODING = "DSA Coding Challenge"
    TECHNICAL_MCQ = "Technical Multiple Choice"
    APTITUDE_QUANTITATIVE = "Quantitative Aptitude"
    APTITUDE_LOGICAL = "Logical Reasoning"
    APTITUDE_VERBAL = "Verbal Ability" 
    SYSTEM_DESIGN = "System Design"
    COMPANY_SPECIFIC = "Company-Specific Assessment"

class DifficultyLevel(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    EXPERT = "Expert"

class QuestionCategory(Enum):
    # DSA Categories
    ARRAYS = "Arrays"
    STRINGS = "Strings"
    LINKED_LISTS = "Linked Lists"
    TREES = "Trees"
    GRAPHS = "Graphs"
    DYNAMIC_PROGRAMMING = "Dynamic Programming"
    SORTING_SEARCHING = "Sorting & Searching"
    STACK_QUEUE = "Stack & Queue"
    HASH_TABLE = "Hash Table"
    RECURSION = "Recursion"
    
    # Technical Categories
    PROGRAMMING_LANGUAGES = "Programming Languages"
    WEB_DEVELOPMENT = "Web Development"
    DATABASE = "Database Management"
    OPERATING_SYSTEMS = "Operating Systems"
    NETWORKING = "Computer Networks"
    SOFTWARE_ENGINEERING = "Software Engineering"
    CLOUD_COMPUTING = "Cloud Computing"
    
    # Aptitude Categories
    MATHEMATICS = "Mathematics"
    STATISTICS = "Statistics"
    LOGICAL_PUZZLES = "Logical Puzzles"
    PATTERN_RECOGNITION = "Pattern Recognition"
    READING_COMPREHENSION = "Reading Comprehension"
    GRAMMAR = "Grammar & Vocabulary"

@dataclass
class TestCase:
    """Individual test case for coding problems"""
    input_data: str
    expected_output: str
    explanation: Optional[str] = None
    is_hidden: bool = False

@dataclass
class DSAQuestion:
    """Data structure & algorithms question"""
    id: str
    title: str
    description: str
    category: QuestionCategory
    difficulty: DifficultyLevel
    test_cases: List[TestCase]
    hints: List[str]
    solution_approach: str
    time_complexity: str
    space_complexity: str
    companies: List[str] = field(default_factory=list)
    leetcode_link: Optional[str] = None
    tags: List[str] = field(default_factory=list)

@dataclass
class MCQOption:
    """Multiple choice question option"""
    id: str
    text: str
    is_correct: bool
    explanation: Optional[str] = None

@dataclass
class MCQQuestion:
    """Multiple choice question"""
    id: str
    question: str
    category: QuestionCategory
    difficulty: DifficultyLevel
    options: List[MCQOption]
    explanation: str
    companies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

@dataclass
class AssessmentConfig:
    """Configuration for an assessment"""
    assessment_id: str
    name: str
    description: str
    assessment_types: List[AssessmentType]
    total_questions: int
    time_limit_minutes: int
    company_name: Optional[str] = None
    target_role: Optional[str] = None
    experience_level: Optional[str] = None
    passing_score: float = 70.0
    
    # Question distribution
    dsa_questions: int = 0
    mcq_questions: int = 0
    aptitude_questions: int = 0
    
    # Difficulty distribution
    easy_percent: float = 30.0
    medium_percent: float = 50.0
    hard_percent: float = 20.0

@dataclass
class TestResponse:
    """User's response to a question"""
    question_id: str
    question_type: AssessmentType
    user_answer: Union[str, List[str]]
    time_taken_seconds: float
    is_correct: bool
    score: float
    timestamp: datetime

@dataclass
class AssessmentResult:
    """Complete assessment result"""
    assessment_id: str
    user_id: str
    start_time: datetime
    end_time: datetime
    total_time_taken: timedelta
    responses: List[TestResponse]
    
    # Overall scores
    total_score: float
    percentage_score: float
    passed: bool
    
    # Category-wise performance
    dsa_score: Optional[float] = None
    mcq_score: Optional[float] = None
    aptitude_score: Optional[float] = None
    
    # Analysis
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

class AssessmentEngine:
    """Main assessment engine for creating and managing tests"""
    
    def __init__(self):
        self.data_dir = "Data/Assessments/"
        self.results_dir = "Data/AssessmentResults/"
        self.ensure_directories()
        
        # Load question databases
        self.dsa_questions = self.load_dsa_questions()
        self.mcq_questions = self.load_mcq_questions()
        self.aptitude_questions = self.load_aptitude_questions()
        
        # Active assessments
        self.active_assessments: Dict[str, Dict] = {}
    
    def ensure_directories(self):
        """Ensure necessary directories exist"""
        for directory in [self.data_dir, self.results_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def load_dsa_questions(self) -> List[DSAQuestion]:
        """Load DSA questions from database"""
        questions_file = os.path.join(self.data_dir, "dsa_questions.json")
        
        if os.path.exists(questions_file):
            try:
                with open(questions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [DSAQuestion(**q) for q in data]
            except Exception as e:
                print(f"❌ Error loading DSA questions: {e}")
        
        # Return default questions if file doesn't exist
        return self.create_default_dsa_questions()
    
    def load_mcq_questions(self) -> List[MCQQuestion]:
        """Load MCQ questions from database"""
        questions_file = os.path.join(self.data_dir, "mcq_questions.json")
        
        if os.path.exists(questions_file):
            try:
                with open(questions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    questions = []
                    for q_data in data:
                        # Convert options
                        options = [MCQOption(**opt) for opt in q_data['options']]
                        q_data['options'] = options
                        questions.append(MCQQuestion(**q_data))
                    return questions
            except Exception as e:
                print(f"❌ Error loading MCQ questions: {e}")
        
        return self.create_default_mcq_questions()
    
    def load_aptitude_questions(self) -> List[MCQQuestion]:
        """Load aptitude questions from database"""
        questions_file = os.path.join(self.data_dir, "aptitude_questions.json")
        
        if os.path.exists(questions_file):
            try:
                with open(questions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    questions = []
                    for q_data in data:
                        options = [MCQOption(**opt) for opt in q_data['options']]
                        q_data['options'] = options
                        questions.append(MCQQuestion(**q_data))
                    return questions
            except Exception as e:
                print(f"❌ Error loading aptitude questions: {e}")
        
        return self.create_default_aptitude_questions()
    
    def create_company_specific_assessment(self, 
                                         company_intelligence: Dict,
                                         resume_data: Dict,
                                         target_role: str) -> AssessmentConfig:
        """Create customized assessment based on company intelligence and resume"""
        
        print(f"🎯 Creating assessment for {target_role} at {company_intelligence.get('company_name', 'Company')}")
        
        # Determine assessment complexity based on experience level
        experience_level = resume_data.get('experience_level', 'Mid Level')
        
        # Configure based on company and role
        config = AssessmentConfig(
            assessment_id=f"assessment_{int(time.time())}",
            name=f"{target_role} Assessment - {company_intelligence.get('company_name', 'Custom')}",
            description=f"Comprehensive assessment for {target_role} position",
            assessment_types=[
                AssessmentType.DSA_CODING,
                AssessmentType.TECHNICAL_MCQ,
                AssessmentType.APTITUDE_QUANTITATIVE
            ],
            total_questions=self._calculate_total_questions(experience_level),
            time_limit_minutes=self._calculate_time_limit(experience_level),
            company_name=company_intelligence.get('company_name'),
            target_role=target_role,
            experience_level=experience_level
        )
        
        # Customize question distribution
        self._customize_question_distribution(config, company_intelligence, resume_data)
        
        return config
    
    def _calculate_total_questions(self, experience_level: str) -> int:
        """Calculate total questions based on experience level"""
        level_mapping = {
            'Entry Level': 15,
            'Mid Level': 20,
            'Senior Level': 25,
            'Executive Level': 20  # Focus more on system design and leadership
        }
        return level_mapping.get(experience_level, 20)
    
    def _calculate_time_limit(self, experience_level: str) -> int:
        """Calculate time limit based on experience level"""
        level_mapping = {
            'Entry Level': 60,
            'Mid Level': 90,
            'Senior Level': 120,
            'Executive Level': 90
        }
        return level_mapping.get(experience_level, 90)
    
    def _customize_question_distribution(self, 
                                       config: AssessmentConfig,
                                       company_intelligence: Dict,
                                       resume_data: Dict):
        """Customize question distribution based on role and company"""
        
        total = config.total_questions
        
        # Get required skills from company intelligence
        required_skills = company_intelligence.get('required_skills', [])
        role_focus = company_intelligence.get('role_focus', {})
        
        # Adjust based on role type
        if any(skill.lower() in ['python', 'java', 'c++', 'javascript'] for skill in required_skills):
            # Programming-heavy role
            config.dsa_questions = int(total * 0.5)
            config.mcq_questions = int(total * 0.3)
            config.aptitude_questions = int(total * 0.2)
        elif any(skill.lower() in ['system design', 'architecture', 'scalability'] for skill in required_skills):
            # System design focus
            config.dsa_questions = int(total * 0.3)
            config.mcq_questions = int(total * 0.5)
            config.aptitude_questions = int(total * 0.2)
        else:
            # Balanced approach
            config.dsa_questions = int(total * 0.4)
            config.mcq_questions = int(total * 0.4)
            config.aptitude_questions = int(total * 0.2)
        
        # Adjust difficulty based on experience
        if config.experience_level == 'Entry Level':
            config.easy_percent = 50.0
            config.medium_percent = 40.0
            config.hard_percent = 10.0
        elif config.experience_level == 'Senior Level':
            config.easy_percent = 20.0
            config.medium_percent = 40.0
            config.hard_percent = 40.0
    
    def generate_assessment_questions(self, config: AssessmentConfig) -> List[Union[DSAQuestion, MCQQuestion]]:
        """Generate questions for an assessment based on config"""
        
        questions = []
        
        # Generate DSA questions
        if config.dsa_questions > 0:
            dsa_questions = self._select_dsa_questions(config)
            questions.extend(dsa_questions)
        
        # Generate MCQ questions
        if config.mcq_questions > 0:
            mcq_questions = self._select_mcq_questions(config)
            questions.extend(mcq_questions)
        
        # Generate aptitude questions
        if config.aptitude_questions > 0:
            aptitude_questions = self._select_aptitude_questions(config)
            questions.extend(aptitude_questions)
        
        # Shuffle questions
        random.shuffle(questions)
        
        return questions
    
    def _select_dsa_questions(self, config: AssessmentConfig) -> List[DSAQuestion]:
        """Select DSA questions based on config"""
        
        # Filter by company if specified
        available_questions = self.dsa_questions
        if config.company_name:
            company_questions = [q for q in available_questions if config.company_name in q.companies]
            if company_questions:
                available_questions = company_questions
        
        # Select by difficulty distribution
        easy_count = int(config.dsa_questions * config.easy_percent / 100)
        medium_count = int(config.dsa_questions * config.medium_percent / 100)
        hard_count = config.dsa_questions - easy_count - medium_count
        
        selected = []
        
        # Easy questions
        easy_questions = [q for q in available_questions if q.difficulty == DifficultyLevel.EASY]
        selected.extend(random.sample(easy_questions, min(easy_count, len(easy_questions))))
        
        # Medium questions
        medium_questions = [q for q in available_questions if q.difficulty == DifficultyLevel.MEDIUM]
        selected.extend(random.sample(medium_questions, min(medium_count, len(medium_questions))))
        
        # Hard questions
        hard_questions = [q for q in available_questions if q.difficulty == DifficultyLevel.HARD]
        selected.extend(random.sample(hard_questions, min(hard_count, len(hard_questions))))
        
        return selected
    
    def _select_mcq_questions(self, config: AssessmentConfig) -> List[MCQQuestion]:
        """Select MCQ questions based on config"""
        
        # Similar logic to DSA question selection
        available_questions = self.mcq_questions
        
        # Filter by company if specified
        if config.company_name:
            company_questions = [q for q in available_questions if config.company_name in q.companies]
            if company_questions:
                available_questions = company_questions
        
        # Select by difficulty
        easy_count = int(config.mcq_questions * config.easy_percent / 100)
        medium_count = int(config.mcq_questions * config.medium_percent / 100) 
        hard_count = config.mcq_questions - easy_count - medium_count
        
        selected = []
        
        # Easy questions
        easy_questions = [q for q in available_questions if q.difficulty == DifficultyLevel.EASY]
        selected.extend(random.sample(easy_questions, min(easy_count, len(easy_questions))))
        
        # Medium questions
        medium_questions = [q for q in available_questions if q.difficulty == DifficultyLevel.MEDIUM]
        selected.extend(random.sample(medium_questions, min(medium_count, len(medium_questions))))
        
        # Hard questions
        hard_questions = [q for q in available_questions if q.difficulty == DifficultyLevel.HARD]
        selected.extend(random.sample(hard_questions, min(hard_count, len(hard_questions))))
        
        return selected
    
    def _select_aptitude_questions(self, config: AssessmentConfig) -> List[MCQQuestion]:
        """Select aptitude questions based on config"""
        
        # Select from aptitude questions
        available_questions = self.aptitude_questions
        
        if len(available_questions) >= config.aptitude_questions:
            return random.sample(available_questions, config.aptitude_questions)
        else:
            return available_questions
    
    def start_assessment(self, config: AssessmentConfig) -> Dict:
        """Start a new assessment session"""
        
        # Generate questions
        questions = self.generate_assessment_questions(config)
        
        # Create session
        session = {
            'config': config,
            'questions': questions,
            'start_time': datetime.now(),
            'current_question': 0,
            'responses': [],
            'status': 'in_progress'
        }
        
        self.active_assessments[config.assessment_id] = session
        
        print(f"🚀 Assessment '{config.name}' started!")
        print(f"📝 Total Questions: {len(questions)}")
        print(f"⏰ Time Limit: {config.time_limit_minutes} minutes")
        
        return {
            'assessment_id': config.assessment_id,
            'total_questions': len(questions),
            'time_limit': config.time_limit_minutes,
            'first_question': self._format_question_for_display(questions[0]) if questions else None
        }
    
    def _format_question_for_display(self, question: Union[DSAQuestion, MCQQuestion]) -> Dict:
        """Format question for display in UI"""
        
        # Helper function to safely get enum value or return string
        def get_value(attr):
            return attr.value if hasattr(attr, 'value') else str(attr)
        
        if isinstance(question, DSAQuestion):
            return {
                'type': 'dsa',
                'id': question.id,
                'title': question.title,
                'description': question.description,
                'difficulty': get_value(question.difficulty),
                'category': get_value(question.category),
                'hints': question.hints,
                'test_cases': [{'input': tc.input_data, 'output': tc.expected_output} 
                              for tc in question.test_cases if not tc.is_hidden]
            }
        
        elif isinstance(question, MCQQuestion):
            return {
                'type': 'mcq',
                'id': question.id,
                'question': question.question,
                'difficulty': get_value(question.difficulty),
                'category': get_value(question.category),
                'options': [{'id': opt.id, 'text': opt.text} for opt in question.options]
            }
    
    def submit_answer(self, assessment_id: str, question_id: str, answer: Union[str, List[str]]) -> Dict:
        """Submit answer for a question"""
        
        if assessment_id not in self.active_assessments:
            return {'error': 'Assessment not found'}
        
        session = self.active_assessments[assessment_id]
        
        # Find the question
        current_question = None
        for q in session['questions']:
            if q.id == question_id:
                current_question = q
                break
        
        if not current_question:
            return {'error': 'Question not found'}
        
        # Evaluate answer
        is_correct, score = self._evaluate_answer(current_question, answer)
        
        # Record response
        response = TestResponse(
            question_id=question_id,
            question_type=AssessmentType.DSA_CODING if isinstance(current_question, DSAQuestion) else AssessmentType.TECHNICAL_MCQ,
            user_answer=answer,
            time_taken_seconds=time.time(),  # This should be calculated properly
            is_correct=is_correct,
            score=score,
            timestamp=datetime.now()
        )
        
        session['responses'].append(response)
        session['current_question'] += 1
        
        # Check if assessment is complete
        if session['current_question'] >= len(session['questions']):
            return self._complete_assessment(assessment_id)
        
        # Return next question
        next_question = session['questions'][session['current_question']]
        return {
            'correct': is_correct,
            'score': score,
            'next_question': self._format_question_for_display(next_question),
            'progress': {
                'current': session['current_question'] + 1,
                'total': len(session['questions'])
            }
        }
    
    def _evaluate_answer(self, question: Union[DSAQuestion, MCQQuestion], answer: Union[str, List[str]]) -> Tuple[bool, float]:
        """Evaluate user's answer"""
        
        if isinstance(question, MCQQuestion):
            # Find correct option
            correct_options = [opt for opt in question.options if opt.is_correct]
            if len(correct_options) == 1:
                # Single correct answer
                correct_id = correct_options[0].id
                is_correct = answer == correct_id
                return is_correct, 1.0 if is_correct else 0.0
            else:
                # Multiple correct answers
                correct_ids = {opt.id for opt in correct_options}
                user_ids = set(answer if isinstance(answer, list) else [answer])
                
                if user_ids == correct_ids:
                    return True, 1.0
                elif user_ids.intersection(correct_ids):
                    # Partial credit
                    return False, len(user_ids.intersection(correct_ids)) / len(correct_ids)
                else:
                    return False, 0.0
        
        elif isinstance(question, DSAQuestion):
            # For DSA questions, this would involve running code against test cases
            # For now, return partial implementation
            # In a real implementation, you'd use a code execution environment
            return True, 1.0  # Placeholder
        
        return False, 0.0
    
    def _complete_assessment(self, assessment_id: str) -> Dict:
        """Complete assessment and generate results"""
        
        session = self.active_assessments[assessment_id]
        
        # Calculate final scores
        total_score = sum(response.score for response in session['responses'])
        max_score = len(session['responses'])
        percentage = (total_score / max_score) * 100 if max_score > 0 else 0
        
        # Create result object
        result = AssessmentResult(
            assessment_id=assessment_id,
            user_id="current_user",  # This should come from session
            start_time=session['start_time'],
            end_time=datetime.now(),
            total_time_taken=datetime.now() - session['start_time'],
            responses=session['responses'],
            total_score=total_score,
            percentage_score=percentage,
            passed=percentage >= session['config'].passing_score
        )
        
        # Analyze performance
        self._analyze_performance(result, session)
        
        # Save results
        self._save_assessment_result(result)
        
        # Clean up session
        session['status'] = 'completed'
        
        return {
            'completed': True,
            'total_score': total_score,
            'percentage': percentage,
            'passed': result.passed,
            'time_taken': str(result.total_time_taken),
            'strengths': result.strengths,
            'weaknesses': result.weaknesses,
            'recommendations': result.recommendations
        }
    
    def _analyze_performance(self, result: AssessmentResult, session: Dict):
        """Analyze user performance and generate insights"""
        
        # Category-wise analysis
        category_scores = {}
        for response in result.responses:
            # Find the original question to get category
            question = None
            for q in session['questions']:
                if q.id == response.question_id:
                    question = q
                    break
            
            if question and hasattr(question, 'category'):
                category = question.category.value
                if category not in category_scores:
                    category_scores[category] = []
                category_scores[category].append(response.score)
        
        # Calculate category averages
        category_averages = {
            category: sum(scores) / len(scores)
            for category, scores in category_scores.items()
        }
        
        # Identify strengths and weaknesses
        result.strengths = [
            category for category, avg in category_averages.items()
            if avg >= 0.8
        ]
        
        result.weaknesses = [
            category for category, avg in category_averages.items()
            if avg < 0.5
        ]
        
        # Generate recommendations
        result.recommendations = self._generate_recommendations(result, category_averages)
    
    def _generate_recommendations(self, result: AssessmentResult, category_averages: Dict) -> List[str]:
        """Generate improvement recommendations"""
        
        recommendations = []
        
        for category, avg in category_averages.items():
            if avg < 0.5:
                if category == "Arrays":
                    recommendations.append("Practice more array manipulation problems on LeetCode")
                elif category == "Trees":
                    recommendations.append("Focus on tree traversal algorithms and binary search trees")
                elif category == "Dynamic Programming":
                    recommendations.append("Study classic DP patterns and practice bottom-up solutions")
                elif category == "System Design":
                    recommendations.append("Review scalability concepts and practice system design interviews")
                else:
                    recommendations.append(f"Improve {category} skills through targeted practice")
        
        if result.percentage_score < 70:
            recommendations.append("Consider retaking assessment after additional preparation")
        
        return recommendations
    
    def _save_assessment_result(self, result: AssessmentResult):
        """Save assessment result to file"""
        
        filename = f"{result.assessment_id}_{result.user_id}_{result.start_time.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.results_dir, filename)
        
        # Convert to dictionary for serialization
        result_dict = asdict(result)
        result_dict['start_time'] = result.start_time.isoformat()
        result_dict['end_time'] = result.end_time.isoformat()
        result_dict['total_time_taken'] = str(result.total_time_taken)
        
        # Convert response timestamps
        for response in result_dict['responses']:
            response['timestamp'] = response['timestamp'].isoformat()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)
    
    def get_assessment_stats(self) -> Dict:
        """Get overall assessment statistics"""
        
        return {
            'total_dsa_questions': len(self.dsa_questions),
            'total_mcq_questions': len(self.mcq_questions),
            'total_aptitude_questions': len(self.aptitude_questions),
            'active_assessments': len(self.active_assessments),
            'supported_companies': list(set(
                company for q in self.dsa_questions + self.mcq_questions 
                for company in q.companies
            ))
        }
    
    def create_default_dsa_questions(self) -> List[DSAQuestion]:
        """Create default DSA questions for initial setup"""
        
        # This will be expanded with a comprehensive question database
        default_questions = [
            DSAQuestion(
                id="dsa_001",
                title="Two Sum",
                description="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                category=QuestionCategory.ARRAYS,
                difficulty=DifficultyLevel.EASY,
                test_cases=[
                    TestCase("[2,7,11,15], target = 9", "[0,1]", "2 + 7 = 9"),
                    TestCase("[3,2,4], target = 6", "[1,2]", "2 + 4 = 6"),
                    TestCase("[3,3], target = 6", "[0,1]", "3 + 3 = 6")
                ],
                hints=[
                    "Try using a hash map to store values and their indices",
                    "For each element, check if target - element exists in the map"
                ],
                solution_approach="Use a hash map to store elements and their indices. For each element, check if (target - element) exists in the map.",
                time_complexity="O(n)",
                space_complexity="O(n)",
                companies=["Google", "Amazon", "Microsoft", "Facebook"],
                leetcode_link="https://leetcode.com/problems/two-sum/",
                tags=["hash-table", "array"]
            ),
            DSAQuestion(
                id="dsa_002", 
                title="Valid Parentheses",
                description="Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
                category=QuestionCategory.STACK_QUEUE,
                difficulty=DifficultyLevel.EASY,
                test_cases=[
                    TestCase("'()'", "true", "Valid parentheses"),
                    TestCase("'()[]{}'", "true", "All types valid"),
                    TestCase("'(]'", "false", "Mismatched brackets")
                ],
                hints=[
                    "Use a stack to keep track of opening brackets",
                    "When you see a closing bracket, check if it matches the most recent opening bracket"
                ],
                solution_approach="Use a stack. Push opening brackets, pop and check matching for closing brackets.",
                time_complexity="O(n)",
                space_complexity="O(n)",
                companies=["Google", "Amazon", "Microsoft"],
                tags=["stack", "string"]
            )
        ]
        
        return default_questions
    
    def create_default_mcq_questions(self) -> List[MCQQuestion]:
        """Create default MCQ questions for initial setup"""
        
        default_questions = [
            MCQQuestion(
                id="mcq_001",
                question="What is the time complexity of searching in a balanced binary search tree?",
                category=QuestionCategory.TREES,
                difficulty=DifficultyLevel.MEDIUM,
                options=[
                    MCQOption("a", "O(1)", False),
                    MCQOption("b", "O(log n)", True, "BST allows binary search with logarithmic complexity"),
                    MCQOption("c", "O(n)", False),
                    MCQOption("d", "O(n log n)", False)
                ],
                explanation="In a balanced BST, the height is O(log n), making search operations O(log n)",
                companies=["Google", "Microsoft", "Amazon"],
                tags=["trees", "complexity"]
            ),
            MCQQuestion(
                id="mcq_002", 
                question="Which data structure is best for implementing a LRU (Least Recently Used) cache?",
                category=QuestionCategory.HASH_TABLE,
                difficulty=DifficultyLevel.HARD,
                options=[
                    MCQOption("a", "Array", False),
                    MCQOption("b", "Linked List", False),
                    MCQOption("c", "Hash Map", False),
                    MCQOption("d", "Hash Map + Doubly Linked List", True, "Provides O(1) access and O(1) insertion/removal")
                ],
                explanation="LRU cache needs O(1) access (hash map) and O(1) insertion/removal at both ends (doubly linked list)",
                companies=["Google", "Facebook", "Amazon"],
                tags=["hash-table", "linked-list", "design"]
            )
        ]
        
        return default_questions
    
    def create_default_aptitude_questions(self) -> List[MCQQuestion]:
        """Create default aptitude questions for initial setup"""
        
        default_questions = [
            MCQQuestion(
                id="apt_001",
                question="If a train travels 120 km in 2 hours, what is its average speed?",
                category=QuestionCategory.MATHEMATICS,
                difficulty=DifficultyLevel.EASY,
                options=[
                    MCQOption("a", "50 km/h", False),
                    MCQOption("b", "60 km/h", True, "Speed = Distance / Time = 120 / 2 = 60 km/h"),
                    MCQOption("c", "70 km/h", False),
                    MCQOption("d", "80 km/h", False)
                ],
                explanation="Average speed is calculated as total distance divided by total time",
                tags=["mathematics", "speed"]
            ),
            MCQQuestion(
                id="apt_002",
                question="Find the next number in the sequence: 2, 6, 12, 20, 30, ?",
                category=QuestionCategory.PATTERN_RECOGNITION,
                difficulty=DifficultyLevel.MEDIUM,
                options=[
                    MCQOption("a", "40", False),
                    MCQOption("b", "42", True, "Pattern: n(n+1) where n = 1,2,3,4,5,6. Next: 6×7 = 42"),
                    MCQOption("c", "44", False),
                    MCQOption("d", "46", False)
                ],
                explanation="The sequence follows the pattern n(n+1): 1×2, 2×3, 3×4, 4×5, 5×6, 6×7",
                tags=["pattern", "sequence"]
            )
        ]
        
        return default_questions
    
    # =====================================
    # PHASE 3 ENHANCED METHODS - TIMED TESTS & ANALYTICS
    # =====================================
    
    def start_timed_assessment(self, user_id: str, config: AssessmentConfig, 
                              callbacks: Optional[Dict[str, Any]] = None) -> str:
        """Start a timed assessment session with real-time monitoring"""
        
        if not test_environment:
            # Fallback to regular assessment if timed environment unavailable
            return self.start_assessment(config)
        
        # Generate questions for the assessment
        questions = self.generate_assessment_questions(config)
        
        # Format questions for timed environment
        formatted_questions = []
        for question in questions:
            formatted_q = self._format_question_for_display(question)
            
            # Helper function to safely get enum value or return string
            def get_value(attr):
                return attr.value if hasattr(attr, 'value') else str(attr)
            
            formatted_q.update({
                'type': 'DSA' if isinstance(question, DSAQuestion) else 'MCQ',
                'category': get_value(question.category),
                'difficulty': get_value(question.difficulty),
                'time_estimate': self._estimate_question_time(question)
            })
            formatted_questions.append(formatted_q)
        
        # Create test configuration for timed environment
        test_config = {
            'company': config.company_name,
            'role': config.target_role,
            'experience_level': config.experience_level,
            'time_limit': config.time_limit_minutes,
            'total_questions': len(formatted_questions),
            'assessment_config': asdict(config)
        }
        
        # Set up session callbacks for real-time updates
        session_callbacks = {
            'time_warning': self._handle_time_warning,
            'auto_submit': self._handle_auto_submit,
            'paused': self._handle_session_paused,
            'resumed': self._handle_session_resumed,
            'completed': self._handle_session_completed
        }
        
        if callbacks:
            session_callbacks.update(callbacks)
        
        # Create timed test session
        session_id = test_environment.create_test_session(
            user_id=user_id,
            test_config=test_config,
            questions=formatted_questions,
            callbacks=session_callbacks
        )
        
        # Store session mapping for assessment tracking
        self.active_assessments[session_id] = {
            'config': config,
            'questions': questions,
            'formatted_questions': formatted_questions,
            'user_id': user_id,
            'start_time': datetime.now(),
            'is_timed': True
        }
        
        return session_id
    
    def get_timed_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get status of active timed session"""
        
        if not test_environment:
            return None
        
        status = test_environment.get_session_status(session_id)
        
        if status and session_id in self.active_assessments:
            # Add assessment-specific information
            session_info = self.active_assessments[session_id]
            status.update({
                'company': session_info['config'].company_name,
                'role': session_info['config'].target_role,
                'experience_level': session_info['config'].experience_level,
                'assessment_type': 'timed'
            })
        
        return status
    
    def get_current_timed_question(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get current question in timed session"""
        
        if not test_environment:
            return None
        
        return test_environment.get_current_question(session_id)
    
    def submit_timed_answer(self, session_id: str, question_id: str, 
                           answer: Any, time_taken: Optional[int] = None) -> Dict[str, Any]:
        """Submit answer in timed assessment"""
        
        if not test_environment:
            return {"error": "Timed environment not available"}
        
        # Submit to test environment
        result = test_environment.submit_answer(session_id, question_id, answer, time_taken)
        
        # If assessment completed, trigger analysis
        if result.get('success') and 'results' in result:
            self._trigger_performance_analysis(session_id, result['results'])
        
        return result
    
    def pause_timed_assessment(self, session_id: str) -> bool:
        """Pause timed assessment session"""
        
        if not test_environment:
            return False
        
        return test_environment.pause_session(session_id)
    
    def resume_timed_assessment(self, session_id: str) -> bool:
        """Resume paused timed assessment"""
        
        if not test_environment:
            return False
        
        return test_environment.resume_session(session_id)
    
    def submit_timed_assessment(self, session_id: str) -> Dict[str, Any]:
        """Manually submit timed assessment"""
        
        if not test_environment:
            return {"error": "Timed environment not available"}
        
        result = test_environment.submit_test(session_id)
        
        if result.get('success'):
            self._trigger_performance_analysis(session_id, result['results'])
        
        return result
    
    def analyze_user_performance(self, user_id: str, time_period_days: int = 30) -> Dict[str, Any]:
        """Get comprehensive performance analysis for user"""
        
        if not performance_analytics:
            return {"error": "Performance analytics not available"}
        
        profile = performance_analytics.analyze_user_performance(user_id, time_period_days)
        return asdict(profile)
    
    def get_performance_report(self, user_id: str, report_type: str = "detailed") -> Dict[str, Any]:
        """Generate performance report for user"""
        
        if not performance_analytics:
            return {"error": "Performance analytics not available"}
        
        return performance_analytics.create_performance_report(user_id, report_type)
    
    def track_improvement_trends(self, user_id: str, time_period_days: int = 90) -> Dict[str, Any]:
        """Track user improvement over time"""
        
        if not performance_analytics:
            return {"error": "Performance analytics not available"}
        
        return performance_analytics.track_improvement_over_time(user_id, time_period_days)
    
    def generate_study_plan(self, user_id: str) -> Dict[str, Any]:
        """Generate personalized study plan based on performance"""
        
        if not performance_analytics:
            return {"error": "Performance analytics not available"}
        
        return performance_analytics.generate_study_plan(user_id)
    
    def get_company_benchmark(self, company_name: str) -> Dict[str, Any]:
        """Get benchmark data for company assessments"""
        
        if not performance_analytics:
            return {"error": "Performance analytics not available"}
        
        benchmark = performance_analytics.generate_company_benchmark(company_name)
        return asdict(benchmark)
    
    # Private helper methods for timed assessment integration
    
    def _estimate_question_time(self, question: Union[DSAQuestion, MCQQuestion]) -> int:
        """Estimate time needed for question in minutes"""
        
        if isinstance(question, DSAQuestion):
            time_map = {
                DifficultyLevel.EASY: 15,
                DifficultyLevel.MEDIUM: 25, 
                DifficultyLevel.HARD: 35
            }
            return time_map.get(question.difficulty, 25)
        else:
            return 2  # MCQ questions typically take 2 minutes
    
    def _handle_time_warning(self, data: Dict[str, Any]):
        """Handle time warning from timed environment"""
        print(f"⚠️ Time Warning: {data.get('message', 'Time running out!')}")
    
    def _handle_auto_submit(self, data: Dict[str, Any]):
        """Handle auto-submission from timed environment"""
        print(f"⏰ Auto-submitted: {data.get('message', 'Time expired')}")
        
        if 'results' in data:
            session_id = data.get('session_id')
            if session_id:
                self._trigger_performance_analysis(session_id, data['results'])
    
    def _handle_session_paused(self, data: Dict[str, Any]):
        """Handle session pause event"""
        print(f"⏸️ Session paused at {data.get('paused_at', 'unknown time')}")
    
    def _handle_session_resumed(self, data: Dict[str, Any]):
        """Handle session resume event"""
        print(f"▶️ Session resumed at {data.get('resumed_at', 'unknown time')}")
    
    def _handle_session_completed(self, data: Dict[str, Any]):
        """Handle session completion event"""
        print(f"✅ Session completed: {data.get('completion_type', 'manual')}")
        
        if 'results' in data:
            session_id = data.get('session_id')
            if session_id:
                self._trigger_performance_analysis(session_id, data['results'])
    
    def _trigger_performance_analysis(self, session_id: str, results: Dict[str, Any]):
        """Trigger comprehensive performance analysis after assessment completion"""
        
        if not performance_analytics:
            return
        
        try:
            # Analyze the specific test result
            test_analysis = performance_analytics.analyze_test_result(session_id)
            
            # Update user performance profile
            user_id = results.get('user_id')
            if user_id:
                profile = performance_analytics.analyze_user_performance(user_id)
                
                # Save analytics report
                report = performance_analytics.create_performance_report(user_id, "detailed")
                performance_analytics.save_analytics_report(user_id, report)
                
        except Exception as e:
            print(f"Error in performance analysis: {e}")
    
    def get_active_timed_sessions(self) -> List[Dict[str, Any]]:
        """Get all active timed sessions"""
        
        if not test_environment:
            return []
        
        return test_environment.get_active_sessions()
    
    def cleanup_expired_sessions(self):
        """Clean up expired assessment sessions"""
        
        if test_environment:
            test_environment.cleanup_expired_sessions()
        
        # Clean up local session tracking
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session_info in self.active_assessments.items():
            # Mark sessions older than 4 hours as expired
            if current_time - session_info['start_time'] > timedelta(hours=4):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.active_assessments[session_id]

# Initialize the assessment engine
assessment_engine = AssessmentEngine()