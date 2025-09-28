#!/usr/bin/env python3
"""
Code Quality Analyzer for DSA Practice
"""

import ast
import re
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime

class CodeQualityAnalyzer:
    def __init__(self):
        self.analysis_history = []
        
    def analyze_code(self, code: str, language: str = "python") -> Dict:
        """Analyze code quality and provide suggestions"""
        if language.lower() == "python":
            return self.analyze_python_code(code)
        elif language.lower() in ["java", "cpp", "c++"]:
            return self.analyze_general_code(code, language)
        else:
            return {"error": f"Language {language} not supported yet"}
    
    def analyze_python_code(self, code: str) -> Dict:
        """Analyze Python code quality"""
        analysis = {
            "language": "python",
            "timestamp": datetime.now().isoformat(),
            "metrics": {},
            "issues": [],
            "suggestions": [],
            "complexity_score": 0,
            "maintainability_score": 0
        }
        
        try:
            # Parse the code
            tree = ast.parse(code)
            
            # Basic metrics
            lines = code.split('\n')
            analysis["metrics"]["total_lines"] = len(lines)
            analysis["metrics"]["non_empty_lines"] = len([l for l in lines if l.strip()])
            analysis["metrics"]["comment_lines"] = len([l for l in lines if l.strip().startswith('#')])
            
            # AST Analysis
            visitor = PythonCodeVisitor()
            visitor.visit(tree)
            
            analysis["metrics"]["functions"] = len(visitor.functions)
            analysis["metrics"]["classes"] = len(visitor.classes)
            analysis["metrics"]["loops"] = visitor.loop_count
            analysis["metrics"]["conditions"] = visitor.condition_count
            analysis["metrics"]["max_depth"] = visitor.max_depth
            
            # Check for common issues
            analysis["issues"].extend(self.check_python_issues(code, visitor))
            
            # Generate suggestions
            analysis["suggestions"].extend(self.generate_python_suggestions(code, visitor))
            
            # Calculate scores
            analysis["complexity_score"] = self.calculate_complexity_score(visitor)
            analysis["maintainability_score"] = self.calculate_maintainability_score(code, visitor)
            
        except SyntaxError as e:
            analysis["issues"].append(f"Syntax Error: {e}")
        except Exception as e:
            analysis["issues"].append(f"Analysis Error: {e}")
        
        return analysis
    
    def analyze_general_code(self, code: str, language: str) -> Dict:
        """Analyze general code patterns for non-Python languages"""
        analysis = {
            "language": language,
            "timestamp": datetime.now().isoformat(),
            "metrics": {},
            "issues": [],
            "suggestions": [],
            "complexity_score": 0,
            "maintainability_score": 0
        }
        
        lines = code.split('\n')
        analysis["metrics"]["total_lines"] = len(lines)
        analysis["metrics"]["non_empty_lines"] = len([l for l in lines if l.strip()])
        
        # Language-specific comment patterns
        comment_patterns = {
            "java": [r'^\s*//', r'/\*.*?\*/'],
            "cpp": [r'^\s*//', r'/\*.*?\*/'],
            "c++": [r'^\s*//', r'/\*.*?\*/']
        }
        
        if language.lower() in comment_patterns:
            comment_count = 0
            patterns = comment_patterns[language.lower()]
            for line in lines:
                for pattern in patterns:
                    if re.search(pattern, line):
                        comment_count += 1
                        break
            analysis["metrics"]["comment_lines"] = comment_count
        
        # Check for basic patterns
        analysis["metrics"]["loops"] = len(re.findall(r'\b(for|while)\b', code))
        analysis["metrics"]["conditions"] = len(re.findall(r'\b(if|else if|elif)\b', code))
        analysis["metrics"]["functions"] = len(re.findall(r'\b(def|function|public|private|protected)\s+\w+\s*\(', code))
        
        # Basic suggestions
        if analysis["metrics"]["comment_lines"] == 0:
            analysis["suggestions"].append("Add comments to explain your logic")
        
        if analysis["metrics"]["total_lines"] > 50:
            analysis["suggestions"].append("Consider breaking this into smaller functions")
        
        return analysis
    
    def check_python_issues(self, code: str, visitor) -> List[str]:
        """Check for common Python code issues"""
        issues = []
        
        # Long functions
        for func in visitor.functions:
            if func['length'] > 20:
                issues.append(f"Function '{func['name']}' is too long ({func['length']} lines)")
        
        # Deep nesting
        if visitor.max_depth > 4:
            issues.append(f"Code has deep nesting (depth: {visitor.max_depth})")
        
        # No docstrings
        if visitor.functions and not any('docstring' in func for func in visitor.functions):
            issues.append("Functions lack docstrings")
        
        # Variable naming
        if re.search(r'\b[a-z]\b', code):  # Single letter variables
            issues.append("Avoid single-letter variable names (except for loops)")
        
        return issues
    
    def generate_python_suggestions(self, code: str, visitor) -> List[str]:
        """Generate improvement suggestions for Python code"""
        suggestions = []
        
        # Time complexity suggestions
        if visitor.nested_loops > 1:
            suggestions.append("Consider optimizing nested loops - current complexity might be O(n²) or higher")
        
        # Data structure suggestions
        if "list" in code and "in" in code:
            suggestions.append("Consider using set() for membership testing - O(1) vs O(n)")
        
        if visitor.loop_count > 0 and "append" in code:
            suggestions.append("Consider list comprehension for better performance")
        
        # Algorithm suggestions
        if "sort" in code.lower():
            suggestions.append("Consider if the sorting is necessary - it adds O(n log n) complexity")
        
        if visitor.condition_count > 5:
            suggestions.append("Consider using dictionary mapping instead of multiple if-elif statements")
        
        return suggestions
    
    def calculate_complexity_score(self, visitor) -> int:
        """Calculate complexity score (0-100, lower is better)"""
        score = 0
        score += visitor.loop_count * 10
        score += visitor.condition_count * 5
        score += visitor.nested_loops * 15
        score += max(0, visitor.max_depth - 2) * 10
        
        return min(score, 100)
    
    def calculate_maintainability_score(self, code: str, visitor) -> int:
        """Calculate maintainability score (0-100, higher is better)"""
        score = 100
        
        # Deduct for complexity
        score -= self.calculate_complexity_score(visitor) * 0.3
        
        # Deduct for long functions
        for func in visitor.functions:
            if func['length'] > 20:
                score -= 10
        
        # Add for good practices
        if visitor.docstring_count > 0:
            score += 10
        
        comment_ratio = code.count('#') / max(len(code.split('\n')), 1)
        if comment_ratio > 0.1:
            score += 15
        
        return max(0, min(int(score), 100))
    
    def analyze_dsa_solution(self, problem_name: str, code: str, language: str = "python") -> str:
        """Analyze a DSA solution and provide detailed feedback"""
        analysis = self.analyze_code(code, language)
        
        report = f"📊 CODE ANALYSIS REPORT\n"
        report += f"🎯 Problem: {problem_name}\n"
        report += f"💻 Language: {language.title()}\n"
        report += f"⏰ Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        # Metrics
        report += "📈 METRICS:\n"
        for metric, value in analysis["metrics"].items():
            report += f"  • {metric.replace('_', ' ').title()}: {value}\n"
        
        # Complexity Analysis
        complexity_score = analysis["complexity_score"]
        if complexity_score < 30:
            complexity_level = "🟢 Low"
        elif complexity_score < 60:
            complexity_level = "🟡 Medium"
        else:
            complexity_level = "🔴 High"
        
        report += f"\n🧠 COMPLEXITY ANALYSIS:\n"
        report += f"  • Complexity Score: {complexity_score}/100 ({complexity_level})\n"
        report += f"  • Maintainability Score: {analysis['maintainability_score']}/100\n"
        
        # Issues
        if analysis["issues"]:
            report += f"\n⚠️ ISSUES FOUND ({len(analysis['issues'])}):\n"
            for i, issue in enumerate(analysis["issues"], 1):
                report += f"  {i}. {issue}\n"
        
        # Suggestions
        if analysis["suggestions"]:
            report += f"\n💡 SUGGESTIONS ({len(analysis['suggestions'])}):\n"
            for i, suggestion in enumerate(analysis["suggestions"], 1):
                report += f"  {i}. {suggestion}\n"
        
        # Time Complexity Estimation
        report += f"\n⏱️ ESTIMATED TIME COMPLEXITY:\n"
        report += self.estimate_time_complexity(analysis)
        
        # Overall Rating
        overall_score = (100 - complexity_score + analysis["maintainability_score"]) / 2
        if overall_score >= 80:
            rating = "🌟 Excellent"
        elif overall_score >= 60:
            rating = "👍 Good"
        elif overall_score >= 40:
            rating = "⚠️ Needs Improvement"
        else:
            rating = "🔴 Poor"
        
        report += f"\n🎯 OVERALL RATING: {rating} ({overall_score:.1f}/100)\n"
        
        return report
    
    def estimate_time_complexity(self, analysis: Dict) -> str:
        """Estimate time complexity based on code structure"""
        metrics = analysis["metrics"]
        loops = metrics.get("loops", 0)
        conditions = metrics.get("conditions", 0)
        
        if loops == 0:
            return "  • Estimated: O(1) - Constant time"
        elif loops == 1:
            if "sort" in str(analysis).lower():
                return "  • Estimated: O(n log n) - Due to sorting"
            else:
                return "  • Estimated: O(n) - Linear time"
        elif loops >= 2:
            return "  • Estimated: O(n²) or higher - Multiple nested loops detected"
        else:
            return "  • Estimated: O(n) - Linear time (best case)"

class PythonCodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []
        self.loop_count = 0
        self.condition_count = 0
        self.nested_loops = 0
        self.max_depth = 0
        self.current_depth = 0
        self.docstring_count = 0
    
    def visit_FunctionDef(self, node):
        func_info = {
            'name': node.name,
            'length': len(node.body),
            'args': len(node.args.args)
        }
        
        # Check for docstring
        if (node.body and isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Str)):
            func_info['docstring'] = True
            self.docstring_count += 1
        
        self.functions.append(func_info)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        self.classes.append({'name': node.name, 'methods': len(node.body)})
        self.generic_visit(node)
    
    def visit_For(self, node):
        self.loop_count += 1
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        
        # Check for nested loops
        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.While)) and child != node:
                self.nested_loops += 1
                break
        
        self.generic_visit(node)
        self.current_depth -= 1
    
    def visit_While(self, node):
        self.loop_count += 1
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1
    
    def visit_If(self, node):
        self.condition_count += 1
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1

def DSACodeAnalyzer(code: str, problem_name: str = "Unknown", language: str = "python") -> str:
    """Main function to analyze DSA code"""
    analyzer = CodeQualityAnalyzer()
    return analyzer.analyze_dsa_solution(problem_name, code, language)

if __name__ == "__main__":
    # Test the code analyzer
    print("🔍 Testing Code Quality Analyzer...")
    
    # Test Python code
    test_code = '''
def two_sum(nums, target):
    """Find two numbers that add up to target."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return None

def optimized_two_sum(nums, target):
    """Optimized version using hash map."""
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None
'''
    
    result = DSACodeAnalyzer(test_code, "Two Sum", "python")
    print(result)
    
    print("\n✅ Code analyzer test complete!")