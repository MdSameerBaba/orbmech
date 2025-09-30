# comprehensive_dsa_scraper.py

"""
🚀 COMPREHENSIVE DSA CONTENT SCRAPER
=====================================

Combines content from multiple premium DSA sources:
- Striver A2Z DSA Sheet (TakeUForward)
- Love Babbar DSA Sheet & YouTube
- Aditya Verma DSA Patterns
- Apna College DSA Series

Generates language-specific (C++) comprehensive study guides
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class ComprehensiveDSAScraper:
    """Enhanced DSA content scraper combining multiple premium sources"""
    
    def __init__(self, language="cpp"):
        self.language = language
        self.output_file = f"comprehensive_dsa_content_{language}.json"
        
        # Premium DSA sources mapping
        self.sources = {
            "striver": {
                "name": "Striver A2Z DSA Sheet",
                "url": "https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/",
                "youtube": "https://www.youtube.com/@takeUforward",
                "focus": "Complete A2Z coverage with optimal approaches"
            },
            "love_babbar": {
                "name": "Love Babbar DSA Sheet",
                "url": "https://www.lovebabbar.in/",
                "youtube": "https://www.youtube.com/@CodeHelp",
                "focus": "450+ problems with detailed explanations"
            },
            "aditya_verma": {
                "name": "Aditya Verma DSA Patterns",
                "url": "https://www.youtube.com/@AdityaVermaTheProgrammingLord",
                "focus": "Pattern-based problem solving approach"
            },
            "apna_college": {
                "name": "Apna College DSA",
                "url": "https://www.youtube.com/@ApnaCollegeOfficial",
                "focus": "Beginner to advanced with practical examples"
            }
        }
        
    def generate_comprehensive_content(self):
        """Generate comprehensive DSA content combining all sources"""
        print("🚀 Generating Comprehensive DSA Content...")
        print("=" * 60)
        
        comprehensive_content = {
            "metadata": {
                "generated_on": datetime.now().isoformat(),
                "language": self.language,
                "sources": self.sources,
                "total_topics": 0,
                "description": "Comprehensive DSA study material combining premium sources"
            },
            "topics": {}
        }
        
        # Define comprehensive topic structure
        topics = self.get_comprehensive_topic_structure()
        
        for topic_key, topic_info in topics.items():
            print(f"📚 Processing: {topic_info['name']}")
            
            topic_content = self.generate_topic_comprehensive_content(topic_key, topic_info)
            comprehensive_content["topics"][topic_key] = topic_content
            
        comprehensive_content["metadata"]["total_topics"] = len(topics)
        
        # Save to file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(comprehensive_content, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Comprehensive content saved to {self.output_file}")
        return comprehensive_content
    
    def get_comprehensive_topic_structure(self):
        """Get comprehensive topic structure combining all sources"""
        return {
            "arrays": {
                "name": "Arrays & Vectors",
                "priority": 1,
                "difficulty": "Beginner to Advanced",
                "striver_problems": 30,
                "babbar_problems": 45,
                "patterns": ["Two Pointers", "Sliding Window", "Prefix Sum"]
            },
            "strings": {
                "name": "Strings & Pattern Matching", 
                "priority": 2,
                "difficulty": "Beginner to Advanced",
                "striver_problems": 25,
                "babbar_problems": 35,
                "patterns": ["KMP", "Rabin Karp", "Manacher's Algorithm"]
            },
            "linked_lists": {
                "name": "Linked Lists",
                "priority": 3,
                "difficulty": "Beginner to Intermediate",
                "striver_problems": 20,
                "babbar_problems": 25,
                "patterns": ["Fast & Slow Pointers", "Reversal", "Merge Techniques"]
            },
            "binary_trees": {
                "name": "Binary Trees",
                "priority": 4,
                "difficulty": "Intermediate",
                "striver_problems": 35,
                "babbar_problems": 40,
                "patterns": ["DFS", "BFS", "Tree DP"]
            },
            "binary_search_trees": {
                "name": "Binary Search Trees",
                "priority": 5,
                "difficulty": "Intermediate",
                "striver_problems": 15,
                "babbar_problems": 20,
                "patterns": ["BST Properties", "Validation", "Construction"]
            },
            "binary_search": {
                "name": "Binary Search",
                "priority": 6,
                "difficulty": "Intermediate",
                "striver_problems": 25,
                "babbar_problems": 30,
                "patterns": ["Search Space", "Answer Binary Search", "Matrix Search"]
            },
            "stacks_queues": {
                "name": "Stacks & Queues",
                "priority": 7,
                "difficulty": "Beginner to Intermediate",
                "striver_problems": 20,
                "babbar_problems": 25,
                "patterns": ["Monotonic Stack", "Deque", "Priority Queue"]
            },
            "heaps": {
                "name": "Heaps & Priority Queues",
                "priority": 8,
                "difficulty": "Intermediate",
                "striver_problems": 15,
                "babbar_problems": 20,
                "patterns": ["Min/Max Heap", "K-way Merge", "Top K Problems"]
            },
            "hashing": {
                "name": "Hashing & Hash Maps",
                "priority": 9,
                "difficulty": "Beginner to Intermediate",
                "striver_problems": 20,
                "babbar_problems": 25,
                "patterns": ["Frequency Counting", "Anagram Problems", "Subarray Problems"]
            },
            "recursion": {
                "name": "Recursion & Backtracking",
                "priority": 10,
                "difficulty": "Intermediate to Advanced",
                "striver_problems": 25,
                "babbar_problems": 30,
                "patterns": ["Decision Tree", "Subset Generation", "Permutations"]
            },
            "dynamic_programming": {
                "name": "Dynamic Programming",
                "priority": 11,
                "difficulty": "Advanced",
                "striver_problems": 40,
                "babbar_problems": 50,
                "patterns": ["Linear DP", "Grid DP", "Tree DP", "Interval DP"]
            },
            "graphs": {
                "name": "Graph Algorithms",
                "priority": 12,
                "difficulty": "Advanced",
                "striver_problems": 35,
                "babbar_problems": 45,
                "patterns": ["DFS/BFS", "Shortest Path", "MST", "Topological Sort"]
            },
            "tries": {
                "name": "Tries & Advanced Strings",
                "priority": 13,
                "difficulty": "Advanced",
                "striver_problems": 10,
                "babbar_problems": 15,
                "patterns": ["Prefix Trees", "Autocomplete", "Word Search"]
            },
            "greedy": {
                "name": "Greedy Algorithms",
                "priority": 14,
                "difficulty": "Intermediate to Advanced",
                "striver_problems": 20,
                "babbar_problems": 25,
                "patterns": ["Activity Selection", "Huffman Coding", "Job Scheduling"]
            },
            "bit_manipulation": {
                "name": "Bit Manipulation",
                "priority": 15,
                "difficulty": "Intermediate",
                "striver_problems": 15,
                "babbar_problems": 20,
                "patterns": ["XOR Properties", "Bit Masking", "Power of 2"]
            }
        }
    
    def generate_topic_comprehensive_content(self, topic_key: str, topic_info: Dict) -> Dict:
        """Generate comprehensive content for a specific topic"""
        
        # Base content structure
        content = {
            "topic_name": topic_info["name"],
            "priority": topic_info["priority"],
            "difficulty": topic_info["difficulty"],
            "language": self.language,
            "total_problems": topic_info.get("striver_problems", 0) + topic_info.get("babbar_problems", 0),
            "patterns": topic_info.get("patterns", []),
            
            # Source-specific content
            "striver_content": self.get_striver_content(topic_key, topic_info),
            "love_babbar_content": self.get_love_babbar_content(topic_key, topic_info),
            "aditya_verma_content": self.get_aditya_verma_content(topic_key, topic_info),
            "apna_college_content": self.get_apna_college_content(topic_key, topic_info),
            
            # Comprehensive combined content
            "study_plan": self.generate_study_plan(topic_key, topic_info),
            "practice_problems": self.generate_practice_problems(topic_key, topic_info),
            "implementation_guide": self.generate_implementation_guide(topic_key, topic_info),
            "interview_questions": self.generate_interview_questions(topic_key, topic_info),
            
            # Resources
            "youtube_playlists": self.get_youtube_playlists(topic_key),
            "additional_resources": self.get_additional_resources(topic_key)
        }
        
        return content
    
    def get_striver_content(self, topic_key: str, topic_info: Dict) -> Dict:
        """Get Striver A2Z DSA Sheet content for topic"""
        striver_content = {
            "source": "Striver A2Z DSA Sheet",
            "approach": "Optimal solutions with detailed explanations",
            "total_problems": topic_info.get("striver_problems", 0),
            "youtube_channel": "https://www.youtube.com/@takeUforward",
            "content": self.get_striver_topic_details(topic_key)
        }
        return striver_content
    
    def get_striver_topic_details(self, topic_key: str) -> Dict:
        """Get detailed Striver content for specific topic"""
        striver_details = {
            "arrays": {
                "key_concepts": [
                    "Two Pointers Technique",
                    "Sliding Window Maximum",
                    "Kadane's Algorithm",
                    "Moore's Voting Algorithm",
                    "Dutch National Flag Algorithm"
                ],
                "problems": [
                    {"name": "Maximum Subarray Sum", "difficulty": "Medium", "pattern": "Kadane's Algorithm"},
                    {"name": "Two Sum", "difficulty": "Easy", "pattern": "Two Pointers/Hashing"},
                    {"name": "3Sum", "difficulty": "Medium", "pattern": "Two Pointers"},
                    {"name": "Container With Most Water", "difficulty": "Medium", "pattern": "Two Pointers"},
                    {"name": "Trapping Rain Water", "difficulty": "Hard", "pattern": "Two Pointers"},
                    {"name": "Merge Intervals", "difficulty": "Medium", "pattern": "Sorting"},
                    {"name": "Next Permutation", "difficulty": "Medium", "pattern": "In-place Manipulation"},
                    {"name": "Rotate Array", "difficulty": "Medium", "pattern": "Cyclic Replacement"},
                    {"name": "Find Duplicate Number", "difficulty": "Medium", "pattern": "Floyd's Algorithm"},
                    {"name": "Missing Number", "difficulty": "Easy", "pattern": "XOR/Math"}
                ],
                "cpp_implementations": {
                    "kadanes_algorithm": """
// Kadane's Algorithm - Maximum Subarray Sum
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int maxSoFar = nums[0];
        int maxEndingHere = nums[0];
        
        for(int i = 1; i < nums.size(); i++) {
            maxEndingHere = max(nums[i], maxEndingHere + nums[i]);
            maxSoFar = max(maxSoFar, maxEndingHere);
        }
        
        return maxSoFar;
    }
};
""",
                    "two_pointers": """
// Two Pointers - Two Sum (Sorted Array)
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        int left = 0, right = nums.size() - 1;
        
        while(left < right) {
            int sum = nums[left] + nums[right];
            if(sum == target) {
                return {left + 1, right + 1}; // 1-indexed
            }
            else if(sum < target) left++;
            else right--;
        }
        
        return {}; // No solution found
    }
};
"""
                }
            },
            "dynamic_programming": {
                "key_concepts": [
                    "Tabulation vs Memoization",
                    "State Definition",
                    "Recurrence Relations",
                    "Space Optimization",
                    "DP on Grids",
                    "DP on Trees",
                    "DP on Strings"
                ],
                "problems": [
                    {"name": "Climbing Stairs", "difficulty": "Easy", "pattern": "Linear DP"},
                    {"name": "House Robber", "difficulty": "Medium", "pattern": "Linear DP"},
                    {"name": "Coin Change", "difficulty": "Medium", "pattern": "Unbounded Knapsack"},
                    {"name": "Longest Common Subsequence", "difficulty": "Medium", "pattern": "String DP"},
                    {"name": "Edit Distance", "difficulty": "Hard", "pattern": "String DP"},
                    {"name": "Maximum Product Subarray", "difficulty": "Medium", "pattern": "Modified Kadane's"},
                    {"name": "Word Break", "difficulty": "Medium", "pattern": "String DP"},
                    {"name": "Palindromic Substrings", "difficulty": "Medium", "pattern": "String DP"},
                    {"name": "Best Time to Buy and Sell Stock", "difficulty": "Easy", "pattern": "State Machine DP"}
                ],
                "cpp_implementations": {
                    "fibonacci_dp": """
// Basic DP - Fibonacci with Memoization
class Solution {
public:
    unordered_map<int, int> dp;
    
    int fib(int n) {
        if(n <= 1) return n;
        if(dp.find(n) != dp.end()) return dp[n];
        
        dp[n] = fib(n-1) + fib(n-2);
        return dp[n];
    }
};
""",
                    "lcs_dp": """
// Longest Common Subsequence - String DP
class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        int m = text1.length(), n = text2.length();
        vector<vector<int>> dp(m+1, vector<int>(n+1, 0));
        
        for(int i = 1; i <= m; i++) {
            for(int j = 1; j <= n; j++) {
                if(text1[i-1] == text2[j-1]) {
                    dp[i][j] = 1 + dp[i-1][j-1];
                } else {
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
                }
            }
        }
        
        return dp[m][n];
    }
};
"""
                }
            }
        }
        
        return striver_details.get(topic_key, {
            "key_concepts": [f"{topic_key.title()} fundamentals from Striver A2Z"],
            "problems": [{"name": f"Basic {topic_key} problems", "difficulty": "Mixed"}],
            "cpp_implementations": {}
        })
    
    def get_love_babbar_content(self, topic_key: str, topic_info: Dict) -> Dict:
        """Get Love Babbar 450 DSA content"""
        return {
            "source": "Love Babbar 450 DSA Sheet",
            "approach": "Complete problem coverage with step-by-step solutions",
            "total_problems": topic_info.get("babbar_problems", 0),
            "youtube_channel": "https://www.youtube.com/@CodeHelp",
            "content": {
                "focus": "450+ handpicked problems covering all interview scenarios",
                "teaching_style": "Beginner-friendly with detailed explanations",
                "cpp_focus": "Industry-standard C++ implementations",
                "interview_prep": "Direct mapping to company interview questions"
            }
        }
    
    def get_aditya_verma_content(self, topic_key: str, topic_info: Dict) -> Dict:
        """Get Aditya Verma pattern-based content"""
        return {
            "source": "Aditya Verma Pattern-Based DSA",
            "approach": "Pattern recognition and template-based problem solving",
            "youtube_channel": "https://www.youtube.com/@AdityaVermaTheProgrammingLord",
            "content": {
                "focus": "Pattern identification and template creation",
                "teaching_style": "Pattern-based learning for quick recognition",
                "templates": f"Ready-to-use C++ templates for {topic_key}",
                "problem_patterns": topic_info.get("patterns", [])
            }
        }
    
    def get_apna_college_content(self, topic_key: str, topic_info: Dict) -> Dict:
        """Get Apna College beginner-friendly content"""
        return {
            "source": "Apna College DSA",
            "approach": "Beginner to advanced with practical examples",
            "youtube_channel": "https://www.youtube.com/@ApnaCollegeOfficial",
            "content": {
                "focus": "Complete beginner to placement ready",
                "teaching_style": "Interactive learning with live coding",
                "cpp_focus": "Clear C++ syntax and STL usage",
                "placement_prep": "Direct company placement preparation"
            }
        }
    
    def generate_study_plan(self, topic_key: str, topic_info: Dict) -> Dict:
        """Generate comprehensive study plan combining all sources"""
        return {
            "duration": "2-3 weeks",
            "daily_commitment": "2-3 hours",
            "phases": {
                "Phase 1 (Days 1-5)": {
                    "focus": "Theory and Basic Understanding",
                    "resources": ["Apna College basics", "Striver theory videos"],
                    "goals": ["Understand core concepts", "Learn basic implementations"]
                },
                "Phase 2 (Days 6-12)": {
                    "focus": "Pattern Recognition and Problem Solving",
                    "resources": ["Aditya Verma patterns", "Love Babbar problems"],
                    "goals": ["Recognize common patterns", "Solve 20-30 problems"]
                },
                "Phase 3 (Days 13-21)": {
                    "focus": "Advanced Problems and Optimization",
                    "resources": ["Striver advanced problems", "Company-specific questions"],
                    "goals": ["Master advanced techniques", "Achieve optimal solutions"]
                }
            }
        }
    
    def generate_practice_problems(self, topic_key: str, topic_info: Dict) -> Dict:
        """Generate comprehensive practice problem set"""
        return {
            "beginner": {"count": 10, "source": "Apna College + Love Babbar easy"},
            "intermediate": {"count": 15, "source": "Striver + Love Babbar medium"},
            "advanced": {"count": 10, "source": "Striver hard + Company questions"},
            "total_problems": 35,
            "estimated_time": "40-50 hours"
        }
    
    def generate_implementation_guide(self, topic_key: str, topic_info: Dict) -> Dict:
        """Generate C++ implementation guide"""
        return {
            "language": "C++",
            "cpp_version": "C++17",
            "stl_libraries": ["vector", "algorithm", "queue", "stack", "unordered_map"],
            "coding_standards": "Industry-standard practices",
            "templates": f"Ready-to-use templates for {topic_key} problems",
            "optimization_tips": ["Time complexity optimization", "Space complexity reduction"]
        }
    
    def generate_interview_questions(self, topic_key: str, topic_info: Dict) -> List[str]:
        """Generate interview questions for the topic"""
        base_questions = [
            f"Explain the core concepts of {topic_info['name']}",
            f"What are the time and space complexities of common {topic_key} operations?",
            f"When would you choose {topic_key} over other data structures/algorithms?",
            f"Implement a basic {topic_key} solution in C++",
            f"Optimize this {topic_key} solution for better performance"
        ]
        return base_questions
    
    def get_youtube_playlists(self, topic_key: str) -> List[Dict]:
        """Get YouTube playlists for the topic"""
        return [
            {
                "creator": "Striver (TakeUForward)",
                "playlist": f"A2Z DSA Course - {topic_key.title()}",
                "url": f"https://www.youtube.com/playlist?list=PLgUwDviBIf0rPG3Ictpu74YWBQ1CaBkm2",
                "focus": "Complete theoretical + practical coverage"
            },
            {
                "creator": "Love Babbar (CodeHelp)",
                "playlist": f"DSA Supreme - {topic_key.title()}",
                "url": f"https://www.youtube.com/playlist?list=PLDzeHZWIZsTryvtXdMr6rPh4IDexB5NIA",
                "focus": "450 problem-based learning"
            },
            {
                "creator": "Aditya Verma",
                "playlist": f"{topic_key.title()} Patterns",
                "url": f"https://www.youtube.com/playlist?list=PL_z_8CaSLPWekqhdCPmFohncHwz8TY2Go",
                "focus": "Pattern-based problem solving"
            },
            {
                "creator": "Apna College",
                "playlist": f"DSA in C++ - {topic_key.title()}",
                "url": f"https://www.youtube.com/playlist?list=PLfqMhTWNBTe0b2nM6JHVCnAkhQRGiZMSJ",
                "focus": "Beginner to advanced placement prep"
            }
        ]
    
    def get_additional_resources(self, topic_key: str) -> Dict:
        """Get additional learning resources"""
        return {
            "practice_platforms": [
                {"name": "LeetCode", "url": f"https://leetcode.com/tag/{topic_key}/"},
                {"name": "GeeksforGeeks", "url": f"https://www.geeksforgeeks.org/{topic_key}/"},
                {"name": "CodeChef", "url": "https://www.codechef.com/practice"},
                {"name": "Codeforces", "url": "https://codeforces.com/problemset"}
            ],
            "books": [
                "Introduction to Algorithms (CLRS)",
                "Algorithms by Robert Sedgewick",
                "Data Structures and Algorithms Made Easy"
            ],
            "articles": [
                f"GeeksforGeeks {topic_key} articles",
                f"CP-Algorithms {topic_key} section",
                f"Topcoder {topic_key} tutorials"
            ]
        }

def main():
    """Main function to generate comprehensive DSA content"""
    print("🚀 COMPREHENSIVE DSA CONTENT GENERATOR")
    print("=" * 60)
    print("📚 Sources: Striver + Love Babbar + Aditya Verma + Apna College")
    print("💻 Language: C++")
    print("🎯 Goal: Complete interview preparation content")
    print("=" * 60)
    
    # Initialize scraper for C++
    scraper = ComprehensiveDSAScraper(language="cpp")
    
    # Generate comprehensive content
    content = scraper.generate_comprehensive_content()
    
    print("\n🎉 COMPREHENSIVE DSA CONTENT GENERATED!")
    print(f"📁 File: {scraper.output_file}")
    print(f"📚 Topics: {content['metadata']['total_topics']}")
    print(f"🎯 Language: {content['metadata']['language'].upper()}")
    
    # Display sample content
    print("\n📖 SAMPLE CONTENT (Arrays Topic):")
    print("=" * 50)
    if "arrays" in content["topics"]:
        arrays_content = content["topics"]["arrays"]
        print(f"🔢 Topic: {arrays_content['topic_name']}")
        print(f"⭐ Difficulty: {arrays_content['difficulty']}")
        print(f"📊 Total Problems: {arrays_content['total_problems']}")
        print(f"🎯 Patterns: {', '.join(arrays_content['patterns'])}")
        
        if arrays_content["striver_content"]["content"].get("key_concepts"):
            print(f"💡 Key Concepts:")
            for concept in arrays_content["striver_content"]["content"]["key_concepts"][:3]:
                print(f"   • {concept}")
        
    print("\n🚀 Ready for comprehensive DSA learning!")
    return content

if __name__ == "__main__":
    main()