#!/usr/bin/env python3
"""
Enhanced Full-Stack Code Generator
Generates properly structured frontend/backend projects based on architecture
"""

import os
import json
import sys
from typing import Dict, List, Any

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))
from EnhancedArchitectAnalyzer import FullStackArchitecture, EnhancedRequirementsAnalyzer

class EnhancedCodeGenerator:
    """Enhanced code generator for full-stack applications"""
    
    def __init__(self):
        self.templates = {
            'backend': BackendTemplates(),
            'frontend': FrontendTemplates(),
            'database': DatabaseTemplates()
        }
    
    def generate_full_stack_project(self, requirements: str, output_path: str) -> Dict[str, Any]:
        """Generate complete full-stack project"""
        print(f"🚀 Generating full-stack project...")
        
        # Step 1: Analyze requirements and create architecture
        analyzer = EnhancedRequirementsAnalyzer()
        architecture = analyzer.analyze_requirements(requirements)
        
        # Step 2: Create project structure
        project_path = os.path.join(output_path, architecture.project_name)
        self._create_project_structure(project_path)
        
        # Step 3: Generate database schema files
        print("📊 Generating database schema...")
        db_files = self._generate_database_files(architecture, project_path)
        
        # Step 4: Generate backend (API + Models)
        print("🔧 Generating backend...")
        backend_files = self._generate_backend_files(architecture, project_path)
        
        # Step 5: Generate frontend (Components + Pages + Routes)
        print("🎨 Generating frontend...")
        frontend_files = self._generate_frontend_files(architecture, project_path)
        
        # Step 6: Generate configuration files
        print("⚙️ Generating configuration...")
        config_files = self._generate_config_files(architecture, project_path)
        
        # Step 7: Generate documentation
        print("📚 Generating documentation...")
        doc_files = self._generate_documentation(architecture, project_path)
        
        total_files = len(db_files) + len(backend_files) + len(frontend_files) + len(config_files) + len(doc_files)
        
        return {
            "success": True,
            "project_name": architecture.project_name,
            "project_path": project_path,
            "architecture": architecture,
            "files_generated": total_files,
            "file_breakdown": {
                "database": len(db_files),
                "backend": len(backend_files),
                "frontend": len(frontend_files),
                "config": len(config_files),
                "docs": len(doc_files)
            }
        }
    
    def _create_project_structure(self, project_path: str):
        """Create proper full-stack project folder structure"""
        folders = [
            # Root
            project_path,
            
            # Backend structure
            f"{project_path}/backend",
            f"{project_path}/backend/src",
            f"{project_path}/backend/src/models",
            f"{project_path}/backend/src/routes",
            f"{project_path}/backend/src/controllers",
            f"{project_path}/backend/src/middleware",
            f"{project_path}/backend/src/utils",
            f"{project_path}/backend/src/config",
            f"{project_path}/backend/tests",
            
            # Frontend structure
            f"{project_path}/frontend",
            f"{project_path}/frontend/src",
            f"{project_path}/frontend/src/components",
            f"{project_path}/frontend/src/pages",
            f"{project_path}/frontend/src/hooks",
            f"{project_path}/frontend/src/services",
            f"{project_path}/frontend/src/utils",
            f"{project_path}/frontend/src/styles",
            f"{project_path}/frontend/public",
            
            # Database
            f"{project_path}/database",
            f"{project_path}/database/migrations",
            f"{project_path}/database/seeds",
            
            # Docs
            f"{project_path}/docs",
            
            # Config
            f"{project_path}/config"
        ]
        
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
    
    def _generate_database_files(self, architecture: FullStackArchitecture, project_path: str) -> List[str]:
        """Generate database schema and migration files"""
        files = []
        
        # Generate schema file
        schema_content = self.templates['database'].generate_schema(architecture.database_schema, architecture.tech_stack['database'])
        schema_path = f"{project_path}/database/schema.sql"
        
        with open(schema_path, 'w', encoding='utf-8') as f:
            f.write(schema_content)
        files.append(schema_path)
        
        # Generate migration files
        for entity in architecture.database_schema.entities:
            migration_content = self.templates['database'].generate_migration(entity, architecture.tech_stack['database'])
            migration_path = f"{project_path}/database/migrations/001_create_{entity['name'].lower()}_table.sql"
            
            with open(migration_path, 'w', encoding='utf-8') as f:
                f.write(migration_content)
            files.append(migration_path)
        
        return files
    
    def _generate_backend_files(self, architecture: FullStackArchitecture, project_path: str) -> List[str]:
        """Generate backend API files"""
        files = []
        backend_tech = architecture.tech_stack['backend']
        
        # Generate models
        for entity in architecture.database_schema.entities:
            model_content = self.templates['backend'].generate_model(entity, backend_tech, architecture.tech_stack['database'])
            model_file = f"{project_path}/backend/src/models/{entity['name']}.js" if backend_tech == 'nodejs' else f"{project_path}/backend/src/models/{entity['name'].lower()}.py"
            
            with open(model_file, 'w', encoding='utf-8') as f:
                f.write(model_content)
            files.append(model_file)
        
        # Generate routes/controllers
        for endpoint in architecture.api_endpoints:
            route_name = endpoint.path.split('/')[2]  # Extract route name from path
            if route_name not in ['auth']:  # Handle auth separately
                controller_content = self.templates['backend'].generate_controller(endpoint, backend_tech)
                controller_file = f"{project_path}/backend/src/controllers/{route_name}Controller.js" if backend_tech == 'nodejs' else f"{project_path}/backend/src/controllers/{route_name}_controller.py"
                
                with open(controller_file, 'w', encoding='utf-8') as f:
                    f.write(controller_content)
                files.append(controller_file)
        
        # Generate main server file
        server_content = self.templates['backend'].generate_server(architecture)
        server_file = f"{project_path}/backend/server.js" if backend_tech == 'nodejs' else f"{project_path}/backend/app.py"
        
        with open(server_file, 'w', encoding='utf-8') as f:
            f.write(server_content)
        files.append(server_file)
        
        # Generate package.json or requirements.txt
        if backend_tech == 'nodejs':
            package_content = self.templates['backend'].generate_package_json(architecture)
            package_file = f"{project_path}/backend/package.json"
            
            with open(package_file, 'w', encoding='utf-8') as f:
                f.write(package_content)
            files.append(package_file)
        else:
            requirements_content = self.templates['backend'].generate_requirements(architecture)
            requirements_file = f"{project_path}/backend/requirements.txt"
            
            with open(requirements_file, 'w', encoding='utf-8') as f:
                f.write(requirements_content)
            files.append(requirements_file)
        
        return files
    
    def _generate_frontend_files(self, architecture: FullStackArchitecture, project_path: str) -> List[str]:
        """Generate frontend files"""
        files = []
        frontend_tech = architecture.tech_stack['frontend']
        
        # Generate pages
        for page in architecture.frontend_pages:
            page_content = self.templates['frontend'].generate_page(page, architecture)
            page_file = f"{project_path}/frontend/src/pages/{page}.jsx" if frontend_tech == 'react' else f"{project_path}/frontend/src/pages/{page}.vue"
            
            with open(page_file, 'w', encoding='utf-8') as f:
                f.write(page_content)
            files.append(page_file)
        
        # Generate components
        for component in architecture.frontend_components:
            component_content = self.templates['frontend'].generate_component(component, architecture)
            component_file = f"{project_path}/frontend/src/components/{component}.jsx" if frontend_tech == 'react' else f"{project_path}/frontend/src/components/{component}.vue"
            
            with open(component_file, 'w', encoding='utf-8') as f:
                f.write(component_content)
            files.append(component_file)
        
        # Generate main App file
        app_content = self.templates['frontend'].generate_app(architecture)
        app_file = f"{project_path}/frontend/src/App.jsx" if frontend_tech == 'react' else f"{project_path}/frontend/src/App.vue"
        
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(app_content)
        files.append(app_file)
        
        # Generate API service
        api_service_content = self.templates['frontend'].generate_api_service(architecture)
        api_file = f"{project_path}/frontend/src/services/api.js"
        
        with open(api_file, 'w', encoding='utf-8') as f:
            f.write(api_service_content)
        files.append(api_file)
        
        # Generate package.json
        package_content = self.templates['frontend'].generate_package_json(architecture)
        package_file = f"{project_path}/frontend/package.json"
        
        with open(package_file, 'w', encoding='utf-8') as f:
            f.write(package_content)
        files.append(package_file)
        
        return files
    
    def _generate_config_files(self, architecture: FullStackArchitecture, project_path: str) -> List[str]:
        """Generate configuration files"""
        files = []
        
        # Generate docker-compose.yml for full stack
        docker_content = self._generate_docker_compose(architecture)
        docker_file = f"{project_path}/docker-compose.yml"
        
        with open(docker_file, 'w', encoding='utf-8') as f:
            f.write(docker_content)
        files.append(docker_file)
        
        # Generate .env.example
        env_content = self._generate_env_example(architecture)
        env_file = f"{project_path}/.env.example"
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        files.append(env_file)
        
        # Generate .gitignore
        gitignore_content = self._generate_gitignore()
        gitignore_file = f"{project_path}/.gitignore"
        
        with open(gitignore_file, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        files.append(gitignore_file)
        
        return files
    
    def _generate_documentation(self, architecture: FullStackArchitecture, project_path: str) -> List[str]:
        """Generate documentation files"""
        files = []
        
        # Generate main README
        readme_content = self._generate_readme(architecture)
        readme_file = f"{project_path}/README.md"
        
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        files.append(readme_file)
        
        # Generate API documentation
        api_docs_content = self._generate_api_docs(architecture)
        api_docs_file = f"{project_path}/docs/API.md"
        
        with open(api_docs_file, 'w', encoding='utf-8') as f:
            f.write(api_docs_content)
        files.append(api_docs_file)
        
        # Generate database schema documentation
        schema_docs_content = self._generate_schema_docs(architecture)
        schema_docs_file = f"{project_path}/docs/DATABASE.md"
        
        with open(schema_docs_file, 'w', encoding='utf-8') as f:
            f.write(schema_docs_content)
        files.append(schema_docs_file)
        
        return files
    
    def _generate_docker_compose(self, architecture: FullStackArchitecture) -> str:
        """Generate docker-compose.yml for full stack"""
        database = architecture.tech_stack['database']
        
        db_service = ""
        if database == 'mongodb':
            db_service = '''
  mongodb:
    image: mongo:latest
    container_name: mongodb
    restart: always
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongodb_data:/data/db'''
        elif database == 'postgresql':
            db_service = '''
  postgresql:
    image: postgres:latest
    container_name: postgresql
    restart: always
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    volumes:
      - postgresql_data:/var/lib/postgresql/data'''
        
        return f'''version: '3.8'

services:
  frontend:
    build: ./frontend
    container_name: {architecture.project_name.lower()}-frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://localhost:5000

  backend:
    build: ./backend
    container_name: {architecture.project_name.lower()}-backend
    ports:
      - "5000:5000"
    depends_on:
      - {database}
    environment:
      - NODE_ENV=development
      - DB_CONNECTION_STRING={"mongodb://admin:password@mongodb:27017" if database == "mongodb" else "postgresql://admin:password@postgresql:5432/appdb"}
{db_service}

volumes:
  {database}_data:
'''
    
    def _generate_env_example(self, architecture: FullStackArchitecture) -> str:
        """Generate .env.example file"""
        database = architecture.tech_stack['database']
        
        db_url = "mongodb://localhost:27017/appdb" if database == "mongodb" else "postgresql://localhost:5432/appdb"
        
        return f'''# Environment Configuration
NODE_ENV=development
PORT=5000

# Database
DATABASE_URL={db_url}

# JWT Secret
JWT_SECRET=your-super-secret-jwt-key

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Email Configuration (if needed)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
'''
    
    def _generate_gitignore(self) -> str:
        """Generate .gitignore file"""
        return '''# Dependencies
node_modules/
*/node_modules/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Build outputs
build/
dist/
*/build/
*/dist/

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
*.log

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Database
*.db
*.sqlite

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/
'''
    
    def _generate_readme(self, architecture: FullStackArchitecture) -> str:
        """Generate main README.md"""
        return f'''# {architecture.project_name}

A full-stack {', '.join(architecture.features)} application built with {architecture.tech_stack['frontend'].title()}, {architecture.tech_stack['backend'].title()}, and {architecture.tech_stack['database'].title()}.

## 🚀 Features

{chr(10).join(f"- {feature.title()}" for feature in architecture.features)}

## 🛠️ Tech Stack

- **Frontend**: {architecture.tech_stack['frontend'].title()}
- **Backend**: {architecture.tech_stack['backend'].title()}  
- **Database**: {architecture.tech_stack['database'].title()}

## 📁 Project Structure

```
{architecture.project_name}/
├── frontend/           # React/Vue/Angular frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
├── backend/            # Node.js/Python backend
│   ├── src/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── controllers/
│   │   └── middleware/
│   └── package.json
├── database/           # Database schema & migrations
├── docs/              # Documentation
└── docker-compose.yml # Container orchestration
```

## 🚀 Quick Start

### Prerequisites
- Node.js (v16+)
- {architecture.tech_stack['database'].title()}
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd {architecture.project_name}
   ```

2. **Install backend dependencies**
   ```bash
   cd backend
   npm install
   ```

3. **Install frontend dependencies**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start the database**
   ```bash
   # Using Docker
   docker-compose up {architecture.tech_stack['database']}
   ```

6. **Run database migrations**
   ```bash
   cd backend
   npm run migrate
   ```

7. **Start the development servers**
   ```bash
   # Terminal 1 - Backend
   cd backend
   npm run dev

   # Terminal 2 - Frontend  
   cd frontend
   npm start
   ```

## 📡 API Endpoints

See [API Documentation](./docs/API.md) for detailed endpoint information.

## 📊 Database Schema

See [Database Documentation](./docs/DATABASE.md) for schema details.

## 🐳 Docker Deployment

Run the entire stack with Docker:

```bash
docker-compose up --build
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.
'''
    
    def _generate_api_docs(self, architecture: FullStackArchitecture) -> str:
        """Generate API documentation"""
        docs = f"# {architecture.project_name} API Documentation\\n\\n"
        
        # Group endpoints by category
        auth_endpoints = [ep for ep in architecture.api_endpoints if '/auth/' in ep.path]
        other_endpoints = [ep for ep in architecture.api_endpoints if '/auth/' not in ep.path]
        
        if auth_endpoints:
            docs += "## Authentication Endpoints\\n\\n"
            for endpoint in auth_endpoints:
                docs += f"### {endpoint.method} {endpoint.path}\\n"
                docs += f"{endpoint.description}\\n\\n"
                
                if endpoint.request_body:
                    docs += "**Request Body:**\\n```json\\n"
                    docs += json.dumps(endpoint.request_body, indent=2)
                    docs += "\\n```\\n\\n"
                
                docs += "**Response:**\\n```json\\n"
                docs += json.dumps(endpoint.response_body, indent=2)
                docs += "\\n```\\n\\n"
        
        if other_endpoints:
            docs += "## API Endpoints\\n\\n"
            for endpoint in other_endpoints:
                docs += f"### {endpoint.method} {endpoint.path}\\n"
                docs += f"{endpoint.description}\\n\\n"
                
                if endpoint.auth_required:
                    docs += "🔒 **Authentication Required**\\n\\n"
                
                if endpoint.request_body:
                    docs += "**Request Body:**\\n```json\\n"
                    docs += json.dumps(endpoint.request_body, indent=2)
                    docs += "\\n```\\n\\n"
                
                docs += "**Response:**\\n```json\\n"
                docs += json.dumps(endpoint.response_body, indent=2)
                docs += "\\n```\\n\\n"
        
        return docs
    
    def _generate_schema_docs(self, architecture: FullStackArchitecture) -> str:
        """Generate database schema documentation"""
        docs = f"# {architecture.project_name} Database Schema\\n\\n"
        
        docs += f"Database: **{architecture.tech_stack['database'].title()}**\\n\\n"
        
        docs += "## Entities\\n\\n"
        for entity in architecture.database_schema.entities:
            docs += f"### {entity['name']}\\n\\n"
            docs += "| Field | Type | Constraints |\\n"
            docs += "|-------|------|-------------|\\n"
            
            for field in entity['fields']:
                constraints = []
                if field.get('primary'):
                    constraints.append('PRIMARY KEY')
                if field.get('unique'):
                    constraints.append('UNIQUE')
                if field.get('required'):
                    constraints.append('NOT NULL')
                if field.get('foreign_key'):
                    constraints.append(f"FK → {field['foreign_key']}")
                if field.get('default'):
                    constraints.append(f"DEFAULT {field['default']}")
                
                constraint_str = ', '.join(constraints) if constraints else ''
                docs += f"| {field['name']} | {field['type']} | {constraint_str} |\\n"
            
            docs += "\\n"
        
        if architecture.database_schema.relationships:
            docs += "## Relationships\\n\\n"
            for rel in architecture.database_schema.relationships:
                docs += f"- **{rel['from']}** {rel['type']} **{rel['to']}**\\n"
        
        return docs

# Placeholder template classes (these would be fully implemented)
class BackendTemplates:
    def generate_model(self, entity, backend_tech, database_tech):
        return f"// {entity['name']} model for {backend_tech} with {database_tech}\\n"
    
    def generate_controller(self, endpoint, backend_tech):
        return f"// Controller for {endpoint.path}\\n"
    
    def generate_server(self, architecture):
        return f"// Main server file for {architecture.project_name}\\n"
    
    def generate_package_json(self, architecture):
        return json.dumps({"name": architecture.project_name.lower(), "version": "1.0.0"}, indent=2)
    
    def generate_requirements(self, architecture):
        return "flask\\npymongo\\n"

class FrontendTemplates:
    def generate_page(self, page, architecture):
        return f"// {page} page component\\n"
    
    def generate_component(self, component, architecture):
        return f"// {component} component\\n"
    
    def generate_app(self, architecture):
        return f"// Main App component for {architecture.project_name}\\n"
    
    def generate_api_service(self, architecture):
        return f"// API service for {architecture.project_name}\\n"
    
    def generate_package_json(self, architecture):
        return json.dumps({"name": f"{architecture.project_name.lower()}-frontend", "version": "1.0.0"}, indent=2)

class DatabaseTemplates:
    def generate_schema(self, schema, database_tech):
        return f"-- Database schema for {database_tech}\\n"
    
    def generate_migration(self, entity, database_tech):
        return f"-- Migration for {entity['name']} table\\n"

if __name__ == "__main__":
    generator = EnhancedCodeGenerator()
    
    # Test generation in workspace
    import os
    workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    result = generator.generate_full_stack_project(
        "create react todo app with authentication and drag and drop",
        workspace_root
    )
    
    print("🎉 ENHANCED FULL-STACK PROJECT GENERATED!")
    print("=" * 50)
    print(f"📛 Project: {result['project_name']}")
    print(f"📁 Location: {result['project_path']}")
    print(f"📄 Total Files: {result['files_generated']}")
    print(f"🗂️ File Breakdown:")
    for category, count in result['file_breakdown'].items():
        print(f"   • {category.title()}: {count} files")