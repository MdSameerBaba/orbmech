"""
AI Project Manager - Main orchestrator for AI-powered project generation
Combines requirements analysis, code generation, and project setup
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from .RequirementsAnalyzer import RequirementsAnalyzer, ProjectRequirements
from .CodeGenerator import CodeGenerator

class AIProjectManager:
    """Main orchestrator for AI-powered project generation"""
    
    def __init__(self):
        self.requirements_analyzer = RequirementsAnalyzer()
        self.code_generator = CodeGenerator()
        self.projects_file = "Data/projects.json"
        
    def create_ai_project(self, user_requirements: str, base_path: str = None) -> Dict[str, any]:
        """
        Main method to create a complete AI-generated project
        
        Args:
            user_requirements: Natural language requirements from user
            base_path: Base directory to create project (default: Desktop)
        
        Returns:
            Dict with project info and generation results
        """
        try:
            print(f"🤖 Starting AI project generation...")
            print(f"📝 Requirements: {user_requirements}")
            
            # Step 1: Analyze requirements
            print("🔍 Analyzing requirements...")
            requirements = self.requirements_analyzer.analyze(user_requirements)
            print(f"✅ Detected project: {requirements.name}")
            print(f"🛠️  Tech stack: {requirements.tech_stack}")
            print(f"⚡ Features: {requirements.features}")
            
            # Step 2: Create project directory
            if not base_path:
                base_path = "C:\\\\Users\\\\mdsam\\\\Desktop"
            
            # Create safe directory name
            safe_name = self._create_safe_name(requirements.name)
            project_path = os.path.join(base_path, safe_name)
            
            print(f"📁 Creating project at: {project_path}")
            os.makedirs(project_path, exist_ok=True)
            
            # Step 3: Generate project files
            print("🏗️  Generating project files...")
            generated_files = self.code_generator.generate_project(requirements, project_path)
            
            print(f"✅ Generated {len(generated_files)} files")
            
            # Step 4: Save project to NEXUS database
            project_data = self._create_project_data(requirements, project_path, generated_files)
            self._save_to_nexus_db(project_data)
            
            # Step 5: Generate setup instructions
            setup_instructions = self._generate_setup_instructions(requirements, project_path)
            
            result = {
                "success": True,
                "project_name": requirements.name,
                "project_path": project_path,
                "project_id": project_data["id"],
                "tech_stack": requirements.tech_stack,
                "features": requirements.features,
                "files_generated": len(generated_files),
                "generated_files": list(generated_files.keys()),
                "setup_instructions": setup_instructions,
                "recommendations": self.requirements_analyzer.get_recommendations(requirements)
            }
            
            print("🎉 AI project generation completed successfully!")
            return result
            
        except Exception as e:
            print(f"❌ Error during project generation: {e}")
            return {
                "success": False,
                "error": str(e),
                "project_name": None,
                "project_path": None
            }
    
    def _create_safe_name(self, name: str) -> str:
        """Create filesystem-safe directory name"""
        import re
        # Remove special characters and replace spaces with underscores
        safe_name = re.sub(r'[^a-zA-Z0-9\\s]', '', name)
        safe_name = safe_name.replace(' ', '_')
        return safe_name
    
    def _create_project_data(self, requirements: ProjectRequirements, project_path: str, generated_files: Dict) -> Dict:
        """Create project data for NEXUS database"""
        
        # Load existing projects to get next ID
        projects_data = self._load_projects_db()
        next_id = len(projects_data.get("active_projects", [])) + len(projects_data.get("completed_projects", [])) + 1
        
        # Determine project type based on tech stack
        project_type = self._determine_project_type(requirements.tech_stack)
        
        project_data = {
            "id": next_id,
            "name": requirements.name,
            "description": requirements.description,
            "type": project_type,
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "deadline": "2025-12-31",  # Default deadline
            "status": "active",
            "progress": 20,  # Started with generated code
            "tasks": self._generate_tasks(requirements),
            "time_spent": 0,
            "last_activity": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "local_path": project_path,
            "github_repo": "",
            "git_initialized": False,
            "ai_generated": True,
            "tech_stack": requirements.tech_stack,
            "features": requirements.features,
            "generated_files": list(generated_files.keys()),
            "components": requirements.components,
            "pages": requirements.pages,
            "dependencies": requirements.dependencies
        }
        
        return project_data
    
    def _determine_project_type(self, tech_stack: Dict[str, str]) -> str:
        """Determine NEXUS project type based on tech stack"""
        if tech_stack.get('frontend') and tech_stack.get('backend'):
            return "fullstack_development"
        elif tech_stack.get('frontend'):
            return "frontend_development"  
        elif tech_stack.get('backend'):
            return "backend_development"
        elif tech_stack.get('mobile'):
            return "mobile_development"
        else:
            return "software_development"
    
    def _generate_tasks(self, requirements: ProjectRequirements) -> List[Dict]:
        """Generate task list based on project requirements"""
        tasks = []
        
        # Base development tasks
        base_tasks = [
            {"name": "Setup Development Environment", "phase": "Setup", "estimated_hours": 2, "status": "completed"},
            {"name": "Project Structure Created", "phase": "Setup", "estimated_hours": 1, "status": "completed"},
            {"name": "Basic Components Generated", "phase": "Development", "estimated_hours": 4, "status": "completed"}
        ]
        
        # Feature-specific tasks
        feature_tasks = {
            'authentication': [
                {"name": "Implement User Authentication", "phase": "Development", "estimated_hours": 8, "status": "pending"},
                {"name": "Add Login/Register Forms", "phase": "Frontend", "estimated_hours": 4, "status": "pending"}
            ],
            'payment': [
                {"name": "Integrate Payment System", "phase": "Development", "estimated_hours": 12, "status": "pending"},
                {"name": "Setup Stripe/Payment Provider", "phase": "Backend", "estimated_hours": 6, "status": "pending"}
            ],
            'dashboard': [
                {"name": "Build Admin Dashboard", "phase": "Frontend", "estimated_hours": 10, "status": "pending"},
                {"name": "Add Analytics & Charts", "phase": "Frontend", "estimated_hours": 6, "status": "pending"}
            ],
            'api': [
                {"name": "Create REST API Endpoints", "phase": "Backend", "estimated_hours": 8, "status": "pending"},
                {"name": "Add API Documentation", "phase": "Documentation", "estimated_hours": 3, "status": "pending"}
            ]
        }
        
        # Add base tasks
        for task in base_tasks:
            task["created_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task["actual_hours"] = 0
            tasks.append(task)
        
        # Add feature-specific tasks
        for feature in requirements.features:
            if feature in feature_tasks:
                for task in feature_tasks[feature]:
                    task["created_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                    task["actual_hours"] = 0
                    tasks.append(task)
        
        # Add final tasks
        final_tasks = [
            {"name": "Testing & Bug Fixes", "phase": "Testing", "estimated_hours": 8, "status": "pending"},
            {"name": "Deployment Setup", "phase": "Deployment", "estimated_hours": 4, "status": "pending"},
            {"name": "Documentation & README", "phase": "Documentation", "estimated_hours": 3, "status": "pending"}
        ]
        
        for task in final_tasks:
            task["created_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task["actual_hours"] = 0
            tasks.append(task)
        
        return tasks
    
    def _load_projects_db(self) -> Dict:
        """Load projects database"""
        try:
            if os.path.exists(self.projects_file):
                with open(self.projects_file, 'r') as f:
                    return json.load(f)
            else:
                return {"active_projects": [], "completed_projects": [], "project_templates": {}}
        except Exception:
            return {"active_projects": [], "completed_projects": [], "project_templates": {}}
    
    def _save_to_nexus_db(self, project_data: Dict):
        """Save generated project to NEXUS projects database"""
        projects_db = self._load_projects_db()
        projects_db["active_projects"].append(project_data)
        
        # Save back to file
        os.makedirs(os.path.dirname(self.projects_file), exist_ok=True)
        with open(self.projects_file, 'w') as f:
            json.dump(projects_db, f, indent=2)
        
        print(f"💾 Saved project to NEXUS database (ID: {project_data['id']})")
    
    def _generate_setup_instructions(self, requirements: ProjectRequirements, project_path: str) -> List[str]:
        """Generate setup instructions for the generated project"""
        instructions = []
        
        # Basic instructions
        instructions.extend([
            f"Navigate to project directory: cd {project_path}",
            "Open project in VS Code: code .",
        ])
        
        # Frontend-specific instructions
        if requirements.tech_stack.get('frontend') == 'react':
            instructions.extend([
                "Install dependencies: npm install",
                "Start development server: npm start",
                "Open http://localhost:3000 in your browser"
            ])
        
        # Backend-specific instructions
        if requirements.tech_stack.get('backend') == 'nodejs':
            instructions.extend([
                "Navigate to server directory: cd server",
                "Install server dependencies: npm install",
                "Create .env file with your environment variables",
                "Start server: npm run dev"
            ])
        
        # Database instructions
        if requirements.tech_stack.get('database') == 'mongodb':
            instructions.extend([
                "Install MongoDB or use MongoDB Atlas",
                "Update database connection string in .env file"
            ])
        
        # Git instructions
        instructions.extend([
            "Initialize git repository: git init",
            "Add files: git add .",
            "Create initial commit: git commit -m 'Initial commit - AI generated project'",
            "Create GitHub repository and push: git remote add origin <your-repo-url>"
        ])
        
        return instructions
    
    def get_project_summary(self, project_id: int) -> Optional[Dict]:
        """Get summary of generated project"""
        projects_db = self._load_projects_db()
        
        for project in projects_db.get("active_projects", []):
            if project["id"] == project_id and project.get("ai_generated"):
                return {
                    "name": project["name"],
                    "tech_stack": project.get("tech_stack", {}),
                    "features": project.get("features", []),
                    "progress": project["progress"],
                    "files_generated": len(project.get("generated_files", [])),
                    "components": project.get("components", []),
                    "pages": project.get("pages", []),
                    "local_path": project["local_path"]
                }
        
        return None
    
    def list_ai_projects(self) -> List[Dict]:
        """List all AI-generated projects"""
        projects_db = self._load_projects_db()
        ai_projects = []
        
        for project in projects_db.get("active_projects", []):
            if project.get("ai_generated"):
                ai_projects.append({
                    "id": project["id"],
                    "name": project["name"],
                    "tech_stack": project.get("tech_stack", {}),
                    "features": project.get("features", []),
                    "created_date": project["created_date"],
                    "progress": project["progress"]
                })
        
        return ai_projects
    
    def enhance_project(self, project_id: int, additional_requirements: str) -> Dict:
        """Enhance existing AI project with additional features"""
        # This would analyze additional requirements and add new features/files
        # Implementation would involve re-running analysis and generation
        pass