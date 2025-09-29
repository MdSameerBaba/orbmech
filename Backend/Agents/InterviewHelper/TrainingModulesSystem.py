"""
📚 Training Modules System
Comprehensive training system for DSA, CSE subjects, and Aptitude

This module provides:
- Interactive DSA problem sets with progressive difficulty
- Core CSE subject modules (DBMS, OS, Networks, OOP)
- Aptitude training (Quantitative, Logical, Verbal)
- Progress tracking and performance analytics
"""

import json
import random
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
import subprocess
import tempfile
import os

class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class SubjectType(Enum):
    DSA = "Data Structures & Algorithms"
    DBMS = "Database Management Systems"
    OS = "Operating Systems"
    NETWORKS = "Computer Networks"
    OOP = "Object Oriented Programming"
    APTITUDE = "Aptitude"

@dataclass
class Problem:
    """Structure for coding/aptitude problems"""
    id: str
    title: str
    description: str
    difficulty: Difficulty
    topic: str
    subject_type: SubjectType
    test_cases: List[Dict] = None
    solution_template: str = ""
    expected_complexity: Dict[str, str] = None  # {"time": "O(n)", "space": "O(1)"}
    hints: List[str] = None
    companies: List[str] = None  # Companies that asked this question

@dataclass
class ConceptModule:
    """Structure for concept-based learning modules"""
    id: str
    title: str
    subject_type: SubjectType
    concepts: List[str]
    explanation: str
    examples: List[Dict]
    practice_questions: List[Dict]
    difficulty: Difficulty
    estimated_time: str

@dataclass
class UserProgress:
    """Track user progress across different modules"""
    user_id: str
    problems_solved: Dict[str, List[str]]  # subject -> problem_ids
    concepts_completed: Dict[str, List[str]]  # subject -> concept_ids
    accuracy_scores: Dict[str, float]  # subject -> accuracy percentage
    time_spent: Dict[str, int]  # subject -> minutes
    last_activity: datetime
    current_streak: int
    achievements: List[str]

class TrainingModulesSystem:
    """
    📚 Comprehensive Training System
    
    Provides structured learning for DSA, CSE subjects, and Aptitude
    """
    
    def __init__(self):
        self.problems_db = {}
        self.concepts_db = {}
        self.user_progress = {}
        
        # Initialize training content
        self._initialize_dsa_problems()
        self._initialize_cse_concepts()
        self._initialize_aptitude_problems()
        
    def _initialize_dsa_problems(self):
        """Initialize DSA problem sets"""
        
        # Arrays & Strings Problems
        arrays_problems = [
            Problem(
                id="arr_001",
                title="Two Sum",
                description="""Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

Example:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].""",
                difficulty=Difficulty.EASY,
                topic="Arrays",
                subject_type=SubjectType.DSA,
                test_cases=[
                    {"input": {"nums": [2,7,11,15], "target": 9}, "output": [0,1]},
                    {"input": {"nums": [3,2,4], "target": 6}, "output": [1,2]},
                    {"input": {"nums": [3,3], "target": 6}, "output": [0,1]}
                ],
                solution_template="""def twoSum(nums, target):
    # Your solution here
    pass""",
                expected_complexity={"time": "O(n)", "space": "O(n)"},
                hints=[
                    "Think about using a hash map to store values and their indices",
                    "For each number, check if target - number exists in the hash map"
                ],
                companies=["Google", "Amazon", "Microsoft", "Facebook"]
            ),
            Problem(
                id="arr_002",
                title="Best Time to Buy and Sell Stock",
                description="""You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

Example:
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.""",
                difficulty=Difficulty.EASY,
                topic="Arrays",
                subject_type=SubjectType.DSA,
                test_cases=[
                    {"input": {"prices": [7,1,5,3,6,4]}, "output": 5},
                    {"input": {"prices": [7,6,4,3,1]}, "output": 0},
                    {"input": {"prices": [1,2,3,4,5]}, "output": 4}
                ],
                solution_template="""def maxProfit(prices):
    # Your solution here
    pass""",
                expected_complexity={"time": "O(n)", "space": "O(1)"},
                hints=[
                    "Track the minimum price seen so far",
                    "Calculate profit at each day and keep track of maximum profit"
                ],
                companies=["Amazon", "Microsoft", "Apple"]
            )
        ]
        
        # Linked Lists Problems
        linkedlist_problems = [
            Problem(
                id="ll_001",
                title="Reverse Linked List",
                description="""Given the head of a singly linked list, reverse the list, and return the reversed list.

Example:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]""",
                difficulty=Difficulty.EASY,
                topic="Linked Lists",
                subject_type=SubjectType.DSA,
                test_cases=[
                    {"input": {"head": [1,2,3,4,5]}, "output": [5,4,3,2,1]},
                    {"input": {"head": [1,2]}, "output": [2,1]},
                    {"input": {"head": []}, "output": []}
                ],
                solution_template="""# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseList(head):
    # Your solution here
    pass""",
                expected_complexity={"time": "O(n)", "space": "O(1)"},
                hints=[
                    "Use three pointers: prev, current, and next",
                    "Iteratively reverse the links"
                ],
                companies=["Google", "Facebook", "Microsoft", "Amazon"]
            )
        ]
        
        # Dynamic Programming Problems
        dp_problems = [
            Problem(
                id="dp_001",
                title="Climbing Stairs",
                description="""You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Example:
Input: n = 2
Output: 2
Explanation: There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps""",
                difficulty=Difficulty.EASY,
                topic="Dynamic Programming",
                subject_type=SubjectType.DSA,
                test_cases=[
                    {"input": {"n": 2}, "output": 2},
                    {"input": {"n": 3}, "output": 3},
                    {"input": {"n": 5}, "output": 8}
                ],
                solution_template="""def climbStairs(n):
    # Your solution here
    pass""",
                expected_complexity={"time": "O(n)", "space": "O(1)"},
                hints=[
                    "This is similar to Fibonacci sequence",
                    "Use dynamic programming to avoid recomputing values"
                ],
                companies=["Amazon", "Microsoft", "Adobe"]
            )
        ]
        
        # Store problems by topic
        self.problems_db[SubjectType.DSA] = {
            "Arrays": arrays_problems,
            "Linked Lists": linkedlist_problems,
            "Dynamic Programming": dp_problems
        }
    
    def _initialize_cse_concepts(self):
        """Initialize CSE concept modules"""
        
        # DBMS Concepts
        dbms_modules = [
            ConceptModule(
                id="dbms_001",
                title="Relational Model & SQL Basics",
                subject_type=SubjectType.DBMS,
                concepts=[
                    "Tables, Rows, and Columns",
                    "Primary Keys and Foreign Keys",
                    "SQL SELECT Statements",
                    "WHERE, ORDER BY, GROUP BY Clauses",
                    "JOIN Operations"
                ],
                explanation="""The relational model organizes data into tables (relations) with rows (tuples) and columns (attributes). 
                
Key concepts:
- Primary Key: Unique identifier for each row
- Foreign Key: References primary key of another table
- SQL: Structured Query Language for database operations
- Joins: Combine data from multiple tables""",
                examples=[
                    {
                        "title": "Basic SELECT Query",
                        "code": "SELECT name, age FROM students WHERE age > 18 ORDER BY name;",
                        "explanation": "Selects name and age of students older than 18, ordered by name"
                    },
                    {
                        "title": "INNER JOIN Example",
                        "code": "SELECT s.name, c.course_name FROM students s INNER JOIN courses c ON s.course_id = c.id;",
                        "explanation": "Joins students and courses tables to show student names with their course names"
                    }
                ],
                practice_questions=[
                    {
                        "question": "What is the difference between PRIMARY KEY and UNIQUE constraints?",
                        "type": "conceptual",
                        "difficulty": "Easy"
                    },
                    {
                        "question": "Write a SQL query to find the second highest salary from an Employee table.",
                        "type": "practical",
                        "difficulty": "Medium"
                    }
                ],
                difficulty=Difficulty.EASY,
                estimated_time="3-4 hours"
            ),
            ConceptModule(
                id="dbms_002",
                title="Normalization",
                subject_type=SubjectType.DBMS,
                concepts=[
                    "Database Anomalies",
                    "First Normal Form (1NF)",
                    "Second Normal Form (2NF)",
                    "Third Normal Form (3NF)",
                    "Boyce-Codd Normal Form (BCNF)"
                ],
                explanation="""Normalization is the process of organizing data to reduce redundancy and improve data integrity.

Normal Forms:
- 1NF: Eliminate duplicate columns, create separate tables for related data
- 2NF: Meet 1NF + remove partial dependencies
- 3NF: Meet 2NF + remove transitive dependencies
- BCNF: Meet 3NF + every determinant is a candidate key""",
                examples=[
                    {
                        "title": "1NF Violation Example",
                        "code": "Student(ID, Name, Courses) where Courses = 'Math, Physics, Chemistry'",
                        "explanation": "Violates 1NF because Courses column contains multiple values"
                    }
                ],
                practice_questions=[
                    {
                        "question": "Explain why normalization is important in database design.",
                        "type": "conceptual",
                        "difficulty": "Medium"
                    }
                ],
                difficulty=Difficulty.MEDIUM,
                estimated_time="4-5 hours"
            )
        ]
        
        # Operating Systems Concepts
        os_modules = [
            ConceptModule(
                id="os_001",
                title="Process Management",
                subject_type=SubjectType.OS,
                concepts=[
                    "Process vs Program",
                    "Process States",
                    "Process Control Block (PCB)",
                    "Context Switching",
                    "Inter-process Communication"
                ],
                explanation="""Process management is a core function of operating systems.

Key concepts:
- Process: A program in execution
- Process States: New, Ready, Running, Waiting, Terminated
- PCB: Data structure containing process information
- Context Switch: Saving and restoring process state""",
                examples=[
                    {
                        "title": "Process State Diagram",
                        "code": "New -> Ready -> Running -> Terminated",
                        "explanation": "Basic process lifecycle"
                    }
                ],
                practice_questions=[
                    {
                        "question": "What happens during a context switch?",
                        "type": "conceptual",
                        "difficulty": "Medium"
                    }
                ],
                difficulty=Difficulty.MEDIUM,
                estimated_time="4-5 hours"
            )
        ]
        
        # Store concepts by subject
        self.concepts_db[SubjectType.DBMS] = dbms_modules
        self.concepts_db[SubjectType.OS] = os_modules
    
    def _initialize_aptitude_problems(self):
        """Initialize aptitude problem sets"""
        
        aptitude_problems = [
            Problem(
                id="apt_001",
                title="Percentage Calculation",
                description="""If 15% of a number is 45, what is 25% of the same number?

Options:
A) 65
B) 75
C) 85
D) 95""",
                difficulty=Difficulty.EASY,
                topic="Percentage",
                subject_type=SubjectType.APTITUDE,
                test_cases=[{"input": {}, "output": "B) 75"}],
                hints=[
                    "First find the original number",
                    "15% of x = 45, so x = 45/0.15 = 300",
                    "25% of 300 = 75"
                ]
            ),
            Problem(
                id="apt_002",
                title="Time and Work",
                description="""A can complete a work in 12 days and B can complete the same work in 18 days. 
If they work together, in how many days will they complete the work?

Options:
A) 6.5 days
B) 7.2 days
C) 8.0 days
D) 9.5 days""",
                difficulty=Difficulty.MEDIUM,
                topic="Time and Work",
                subject_type=SubjectType.APTITUDE,
                test_cases=[{"input": {}, "output": "B) 7.2 days"}],
                hints=[
                    "A's rate = 1/12 work per day",
                    "B's rate = 1/18 work per day",
                    "Combined rate = 1/12 + 1/18 = 5/36 work per day",
                    "Time = 1 ÷ (5/36) = 36/5 = 7.2 days"
                ]
            )
        ]
        
        # Store aptitude problems
        self.problems_db[SubjectType.APTITUDE] = {
            "Quantitative": aptitude_problems
        }
    
    def get_problems_by_topic(self, subject_type: SubjectType, topic: str, difficulty: Optional[Difficulty] = None, limit: int = 10) -> List[Problem]:
        """
        Get problems filtered by topic and difficulty
        
        Args:
            subject_type: Type of subject (DSA, DBMS, etc.)
            topic: Specific topic within the subject
            difficulty: Filter by difficulty level
            limit: Maximum number of problems to return
            
        Returns:
            List of Problem objects
        """
        
        if subject_type not in self.problems_db:
            return []
        
        if topic not in self.problems_db[subject_type]:
            return []
        
        problems = self.problems_db[subject_type][topic]
        
        # Filter by difficulty if specified
        if difficulty:
            problems = [p for p in problems if p.difficulty == difficulty]
        
        # Return limited results
        return problems[:limit]
    
    def get_concept_modules(self, subject_type: SubjectType) -> List[ConceptModule]:
        """
        Get all concept modules for a subject
        
        Args:
            subject_type: Type of subject
            
        Returns:
            List of ConceptModule objects
        """
        
        return self.concepts_db.get(subject_type, [])
    
    def execute_code_solution(self, problem: Problem, solution_code: str) -> Dict[str, Any]:
        """
        Execute user's solution against test cases
        
        Args:
            problem: Problem object with test cases
            solution_code: User's solution code
            
        Returns:
            Dictionary with execution results
        """
        
        if not problem.test_cases:
            return {"error": "No test cases available"}
        
        results = {
            "passed": 0,
            "total": len(problem.test_cases),
            "test_results": [],
            "execution_time": 0,
            "error": None
        }
        
        try:
            start_time = time.time()
            
            # Create a temporary file with the solution
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                # Add test cases to the solution
                test_code = solution_code + "\n\n"
                
                for i, test_case in enumerate(problem.test_cases):
                    input_data = test_case["input"]
                    expected_output = test_case["output"]
                    
                    # Generate test execution code
                    if problem.subject_type == SubjectType.DSA:
                        if problem.topic == "Arrays":
                            if "twoSum" in solution_code:
                                test_code += f"result_{i} = twoSum({input_data['nums']}, {input_data['target']})\n"
                            elif "maxProfit" in solution_code:
                                test_code += f"result_{i} = maxProfit({input_data['prices']})\n"
                        elif problem.topic == "Dynamic Programming":
                            if "climbStairs" in solution_code:
                                test_code += f"result_{i} = climbStairs({input_data['n']})\n"
                    
                    test_code += f"print(f'Test {i+1}: {{result_{i}}} == {expected_output} -> {{result_{i} == {expected_output}}}')\n"
                
                f.write(test_code)
                f.flush()
                
                # Execute the code
                result = subprocess.run(['python', f.name], capture_output=True, text=True, timeout=10)
                
                end_time = time.time()
                results["execution_time"] = round((end_time - start_time) * 1000, 2)  # ms
                
                if result.returncode == 0:
                    # Parse output to check test results
                    output_lines = result.stdout.strip().split('\n')
                    
                    for line in output_lines:
                        if "True" in line:
                            results["passed"] += 1
                        results["test_results"].append(line)
                else:
                    results["error"] = result.stderr
                
                # Clean up
                os.unlink(f.name)
                
        except subprocess.TimeoutExpired:
            results["error"] = "Code execution timed out"
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def get_personalized_practice_set(self, user_id: str, subject_type: SubjectType, weak_areas: List[str] = None) -> List[Problem]:
        """
        Generate personalized practice set based on user's progress and weak areas
        
        Args:
            user_id: User identifier
            subject_type: Type of subject
            weak_areas: List of topics user struggles with
            
        Returns:
            Curated list of problems
        """
        
        practice_set = []
        
        # Get user's progress
        progress = self.user_progress.get(user_id, UserProgress(
            user_id=user_id,
            problems_solved={},
            concepts_completed={},
            accuracy_scores={},
            time_spent={},
            last_activity=datetime.now(),
            current_streak=0,
            achievements=[]
        ))
        
        # If user has weak areas, focus on those
        if weak_areas and subject_type in self.problems_db:
            for topic in weak_areas:
                if topic in self.problems_db[subject_type]:
                    # Get problems from weak areas
                    topic_problems = self.problems_db[subject_type][topic]
                    
                    # Filter out already solved problems
                    solved_ids = progress.problems_solved.get(subject_type.value, [])
                    unsolved_problems = [p for p in topic_problems if p.id not in solved_ids]
                    
                    # Add up to 3 problems per weak area
                    practice_set.extend(unsolved_problems[:3])
        
        # If no weak areas specified, get a balanced mix
        else:
            if subject_type in self.problems_db:
                for topic, problems in self.problems_db[subject_type].items():
                    solved_ids = progress.problems_solved.get(subject_type.value, [])
                    unsolved_problems = [p for p in problems if p.id not in solved_ids]
                    
                    # Add 2 problems per topic
                    practice_set.extend(unsolved_problems[:2])
        
        # Limit total problems and randomize
        random.shuffle(practice_set)
        return practice_set[:10]
    
    def update_user_progress(self, user_id: str, problem: Problem, solved: bool, time_taken: int, accuracy: float = None):
        """
        Update user's progress after solving a problem
        
        Args:
            user_id: User identifier
            problem: Problem that was attempted
            solved: Whether the problem was solved correctly
            time_taken: Time taken in seconds
            accuracy: Accuracy score (0-100)
        """
        
        if user_id not in self.user_progress:
            self.user_progress[user_id] = UserProgress(
                user_id=user_id,
                problems_solved={},
                concepts_completed={},
                accuracy_scores={},
                time_spent={},
                last_activity=datetime.now(),
                current_streak=0,
                achievements=[]
            )
        
        progress = self.user_progress[user_id]
        subject_key = problem.subject_type.value
        
        # Update problems solved
        if solved:
            if subject_key not in progress.problems_solved:
                progress.problems_solved[subject_key] = []
            
            if problem.id not in progress.problems_solved[subject_key]:
                progress.problems_solved[subject_key].append(problem.id)
                progress.current_streak += 1
        
        # Update time spent
        if subject_key not in progress.time_spent:
            progress.time_spent[subject_key] = 0
        progress.time_spent[subject_key] += time_taken // 60  # Convert to minutes
        
        # Update accuracy
        if accuracy is not None:
            if subject_key not in progress.accuracy_scores:
                progress.accuracy_scores[subject_key] = []
            progress.accuracy_scores[subject_key] = accuracy
        
        # Update last activity
        progress.last_activity = datetime.now()
        
        # Check for achievements
        self._check_achievements(progress)
    
    def _check_achievements(self, progress: UserProgress):
        """Check and award achievements based on progress"""
        
        achievements = []
        
        # Streak achievements
        if progress.current_streak >= 5 and "5_day_streak" not in progress.achievements:
            achievements.append("5_day_streak")
        
        if progress.current_streak >= 10 and "10_day_streak" not in progress.achievements:
            achievements.append("10_day_streak")
        
        # Problem count achievements
        total_problems = sum(len(problems) for problems in progress.problems_solved.values())
        
        if total_problems >= 50 and "50_problems" not in progress.achievements:
            achievements.append("50_problems")
        
        if total_problems >= 100 and "100_problems" not in progress.achievements:
            achievements.append("100_problems")
        
        # Add new achievements
        progress.achievements.extend(achievements)
    
    def get_progress_analytics(self, user_id: str) -> Dict[str, Any]:
        """
        Get detailed progress analytics for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with analytics data
        """
        
        if user_id not in self.user_progress:
            return {"error": "No progress data found"}
        
        progress = self.user_progress[user_id]
        
        analytics = {
            "total_problems_solved": sum(len(problems) for problems in progress.problems_solved.values()),
            "subjects_progress": {},
            "current_streak": progress.current_streak,
            "total_time_spent": sum(progress.time_spent.values()),
            "achievements": progress.achievements,
            "last_activity": progress.last_activity.isoformat() if progress.last_activity else None,
            "weekly_progress": self._get_weekly_progress(progress),
            "subject_breakdown": {}
        }
        
        # Subject-wise breakdown
        for subject, problems in progress.problems_solved.items():
            analytics["subject_breakdown"][subject] = {
                "problems_solved": len(problems),
                "time_spent": progress.time_spent.get(subject, 0),
                "accuracy": progress.accuracy_scores.get(subject, 0)
            }
        
        return analytics
    
    def _get_weekly_progress(self, progress: UserProgress) -> List[Dict]:
        """Get weekly progress data for charts"""
        
        # Simplified weekly progress (in real implementation, would track daily data)
        weekly_data = []
        
        for i in range(7):  # Last 7 days
            date = datetime.now() - timedelta(days=i)
            weekly_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "problems_solved": random.randint(0, 5),  # Mock data
                "time_spent": random.randint(30, 120)    # Mock data
            })
        
        return weekly_data[::-1]  # Reverse to show chronological order

# Example usage and testing
if __name__ == "__main__":
    # Initialize the training system
    training_system = TrainingModulesSystem()
    
    print("🧪 Testing Training Modules System")
    print("=" * 50)
    
    # Test getting DSA problems
    array_problems = training_system.get_problems_by_topic(SubjectType.DSA, "Arrays", Difficulty.EASY)
    print(f"\n📝 Found {len(array_problems)} Array problems:")
    for problem in array_problems:
        print(f"   - {problem.title} ({problem.difficulty.value})")
    
    # Test getting concept modules
    dbms_modules = training_system.get_concept_modules(SubjectType.DBMS)
    print(f"\n📚 Found {len(dbms_modules)} DBMS modules:")
    for module in dbms_modules:
        print(f"   - {module.title} ({module.estimated_time})")
    
    # Test personalized practice set
    practice_set = training_system.get_personalized_practice_set("user123", SubjectType.DSA, ["Arrays"])
    print(f"\n🎯 Generated practice set with {len(practice_set)} problems")
    
    # Test code execution (if available)
    if array_problems:
        sample_solution = '''def twoSum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []'''
        
        result = training_system.execute_code_solution(array_problems[0], sample_solution)
        print(f"\n⚡ Code execution result: {result.get('passed', 0)}/{result.get('total', 0)} tests passed")
    
    print("\n✅ Training Modules System test completed!")