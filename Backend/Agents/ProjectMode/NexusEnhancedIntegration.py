"""
NEXUS Enhanced Full-Stack Project Generator Integration
Combines the natural language processing with enhanced architecture generation
"""

import sys
import os

# Add backend to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from EnhancedArchitectAnalyzer import EnhancedRequirementsAnalyzer
from EnhancedCodeGenerator import EnhancedCodeGenerator
from typing import Dict, Any, List
import json
import time

class NexusEnhancedProjectGenerator:
    """
    Enhanced NEXUS AI Project Generator with schema-first architecture
    """
    
    def __init__(self):
        self.analyzer = EnhancedRequirementsAnalyzer()
        self.generator = EnhancedCodeGenerator()
        
    def process_natural_language_command(self, user_input: str, output_dir: str = None) -> Dict[str, Any]:
        """
        Process natural language command and generate full-stack project
        
        Args:
            user_input: Natural language description of project
            output_dir: Where to generate project (defaults to workspace)
            
        Returns:
            Complete project generation results
        """
        print("🤖 NEXUS Enhanced AI Project Generator")
        print("=" * 50)
        
        # Set default output directory
        if not output_dir:
            output_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            
        print(f"📝 Processing: {user_input}")
        print(f"📁 Output Location: {output_dir}")
        print()
        
        # Step 1: Enhanced Requirements Analysis
        print("🔍 Phase 1: Enhanced Requirements Analysis")
        print("-" * 40)
        architecture = self.analyzer.analyze_requirements(user_input)
        
        print(f"✅ Project Name: {architecture.project_name}")
        print(f"✅ Tech Stack: {architecture.tech_stack['frontend']} + {architecture.tech_stack['backend']}")
        print(f"✅ Database: {architecture.tech_stack['database']}")
        print(f"✅ Features: {', '.join(architecture.features)}")
        print(f"✅ Database Entities: {len(architecture.database_schema.entities)} entities")
        print(f"✅ API Endpoints: {len(architecture.api_endpoints)} endpoints")
        print(f"✅ Frontend Components: {len(architecture.frontend_components)} components")
        print()
        
        # Step 2: Full-Stack Generation
        print("🚀 Phase 2: Full-Stack Project Generation")
        print("-" * 40)
        
        start_time = time.time()
        result = self.generator.generate_full_stack_project(user_input, output_dir)
        generation_time = time.time() - start_time
        
        # Step 3: Results Summary
        print("🎉 Phase 3: Generation Complete!")
        print("-" * 40)
        print(f"⏱️  Generation Time: {generation_time:.2f} seconds")
        print(f"📛 Project: {result['project_name']}")
        print(f"📁 Location: {result['project_path']}")
        print(f"📄 Total Files: {result['files_generated']}")
        print()
        
        print("🗂️ File Breakdown:")
        for category, count in result['file_breakdown'].items():
            print(f"   • {category.title()}: {count} files")
        print()
        
        # Step 4: Next Steps Guide
        self._display_next_steps(result, architecture)
        
        return {
            'architecture': architecture,
            'generation_result': result,
            'generation_time': generation_time,
            'status': 'success'
        }
    
    def _display_next_steps(self, result: Dict[str, Any], architecture) -> None:
        """Display next steps for the generated project"""
        print("🚀 Next Steps:")
        print("-" * 40)
        print(f"1. Navigate to project: cd {result['project_path']}")
        print()
        print("2. Development Setup:")
        if architecture.tech_stack['frontend'] == "React":
            print("   Frontend (React):")
            print("   cd frontend && npm install && npm start")
        print()
        if architecture.tech_stack['backend'] == "Nodejs":
            print("   Backend (Node.js):")
            print("   cd backend && npm install && npm run dev")
        print()
        print("3. Database Setup:")
        if architecture.tech_stack['database'] == "Mongodb":
            print("   MongoDB:")
            print("   docker-compose up -d mongodb")
        print()
        print("4. Full Stack Launch:")
        print("   docker-compose up -d")
        print("   Access: http://localhost:3000")
        print()
        print("📚 Documentation: docs/README.md")
        print("🔧 Configuration: config/")
        print("🗄️  Database Schema: database/schema.sql")
        print()

    def get_project_capabilities(self) -> Dict[str, List[str]]:
        """Get supported project types and capabilities"""
        return {
            'frontend_frameworks': ['React', 'Vue', 'Angular', 'Svelte'],
            'backend_frameworks': ['Nodejs', 'Python', 'Django', 'FastAPI'],
            'databases': ['Mongodb', 'PostgreSQL', 'MySQL', 'SQLite'],
            'features': [
                'Authentication & Authorization',
                'CRUD Operations',
                'Real-time Features',
                'File Upload/Management',
                'Search & Filtering',
                'Drag & Drop',
                'Charts & Analytics',
                'Email Integration',
                'Payment Processing',
                'Social Login',
                'API Documentation',
                'Testing Suite'
            ],
            'deployment': ['Docker', 'Kubernetes', 'AWS', 'Azure', 'Vercel']
        }
    

def demonstrate_enhanced_capabilities():
    """Demonstrate the enhanced NEXUS capabilities"""
    print("🌟 NEXUS ENHANCED PROJECT GENERATOR DEMO")
    print("=" * 60)
    
    generator = NexusEnhancedProjectGenerator()
    
    # Show capabilities
    print("📋 Supported Capabilities:")
    capabilities = generator.get_project_capabilities()
    for category, items in capabilities.items():
        print(f"\n🔹 {category.replace('_', ' ').title()}:")
        for item in items[:5]:  # Show first 5 items
            print(f"   • {item}")
        if len(items) > 5:
            print(f"   • ... and {len(items) - 5} more")
    
    print("\n" + "=" * 60)
    print("🎯 Demo Commands You Can Try:")
    print("=" * 60)
    
    demo_commands = [
        "create react todo app with authentication and drag and drop",
        "build vue ecommerce store with payment processing",
        "generate python django blog with user management",
        "create angular dashboard with charts and analytics",
        "build nodejs api with mongodb and jwt auth",
        "generate react native mobile app with offline sync"
    ]
    
    for i, command in enumerate(demo_commands, 1):
        print(f"{i}. {command}")
    
    print("\n" + "=" * 60)
    print("🚀 Ready to generate your project!")
    print("Simply call: generator.process_natural_language_command('your command here')")
    print("=" * 60)


if __name__ == "__main__":
    # Run demonstration
    demonstrate_enhanced_capabilities()
    
    print("\n🔥 LIVE DEMO: Generating Enhanced Todo App...")
    print("=" * 60)
    
    # Generate enhanced project
    generator = NexusEnhancedProjectGenerator()
    result = generator.process_natural_language_command(
        "create react todo app with authentication and drag and drop"
    )
    
    print(f"\n✅ Generation Status: {result['status']}")
    print(f"⏱️  Total Time: {result['generation_time']:.2f} seconds")