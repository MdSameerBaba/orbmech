"""
Code Generator for AI Project Generator
Creates complete, functional project files based on parsed requirements
"""

import os
import json
from typing import Dict, List
from .RequirementsAnalyzer import ProjectRequirements

class CodeGenerator:
    """Generates complete project structure and code files"""
    
    def __init__(self):
        self.templates = {
            'react': ReactTemplates(),
            'nodejs': NodejsTemplates(),
            'vue': VueTemplates(),
            'python': PythonTemplates()
        }

    def generate_project(self, requirements: ProjectRequirements, project_path: str) -> Dict[str, str]:
        """Generate complete project based on requirements"""
        generated_files = {}
        
        # Create base project structure
        self._create_directory_structure(requirements, project_path)
        
        # Generate configuration files
        config_files = self._generate_config_files(requirements, project_path)
        generated_files.update(config_files)
        
        # Generate main application files
        app_files = self._generate_app_files(requirements, project_path)
        generated_files.update(app_files)
        
        # Generate components
        component_files = self._generate_components(requirements, project_path)
        generated_files.update(component_files)
        
        # Generate pages
        page_files = self._generate_pages(requirements, project_path)
        generated_files.update(page_files)
        
        # Generate API files (if backend)
        if requirements.tech_stack.get('backend'):
            api_files = self._generate_api_files(requirements, project_path)
            generated_files.update(api_files)
        
        # Generate database files
        if requirements.tech_stack.get('database'):
            db_files = self._generate_database_files(requirements, project_path)
            generated_files.update(db_files)
        
        # Generate documentation
        doc_files = self._generate_documentation(requirements, project_path)
        generated_files.update(doc_files)
        
        return generated_files

    def _create_directory_structure(self, requirements: ProjectRequirements, project_path: str):
        """Create the basic directory structure"""
        frontend = requirements.tech_stack.get('frontend')
        backend = requirements.tech_stack.get('backend')
        
        directories = [project_path]
        
        if frontend:
            if frontend == 'react':
                directories.extend([
                    f"{project_path}/src",
                    f"{project_path}/src/components",
                    f"{project_path}/src/pages",
                    f"{project_path}/src/hooks",
                    f"{project_path}/src/utils",
                    f"{project_path}/src/services",
                    f"{project_path}/src/styles",
                    f"{project_path}/public"
                ])
        
        if backend:
            directories.extend([
                f"{project_path}/server",
                f"{project_path}/server/routes",
                f"{project_path}/server/models", 
                f"{project_path}/server/middleware",
                f"{project_path}/server/controllers",
                f"{project_path}/server/config"
            ])
        
        # Create all directories
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def _generate_config_files(self, requirements: ProjectRequirements, project_path: str) -> Dict[str, str]:
        """Generate configuration files (package.json, etc.)"""
        files = {}
        frontend = requirements.tech_stack.get('frontend')
        
        if frontend == 'react':
            # Generate package.json
            package_json = self.templates['react'].generate_package_json(requirements)
            package_path = f"{project_path}/package.json"
            with open(package_path, 'w', encoding='utf-8') as f:
                f.write(package_json)
            files[package_path] = package_json
            
            # Generate .gitignore
            gitignore = self.templates['react'].generate_gitignore()
            gitignore_path = f"{project_path}/.gitignore"
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore)
            files[gitignore_path] = gitignore
            
            # Generate README.md
            readme = self.templates['react'].generate_readme(requirements)
            readme_path = f"{project_path}/README.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme)
            files[readme_path] = readme
        
        return files

    def _generate_app_files(self, requirements: ProjectRequirements, project_path: str) -> Dict[str, str]:
        """Generate main application files"""
        files = {}
        frontend = requirements.tech_stack.get('frontend')
        
        if frontend == 'react':
            # Generate src/App.js
            app_js = self.templates['react'].generate_app_component(requirements)
            app_path = f"{project_path}/src/App.js"
            with open(app_path, 'w', encoding='utf-8') as f:
                f.write(app_js)
            files[app_path] = app_js
            
            # Generate src/index.js
            index_js = self.templates['react'].generate_index_js(requirements)
            index_path = f"{project_path}/src/index.js"
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_js)
            files[index_path] = index_js
            
            # Generate public/index.html
            index_html = self.templates['react'].generate_index_html(requirements)
            html_path = f"{project_path}/public/index.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(index_html)
            files[html_path] = index_html
        
        return files

    def _generate_components(self, requirements: ProjectRequirements, project_path: str) -> Dict[str, str]:
        """Generate React components"""
        files = {}
        frontend = requirements.tech_stack.get('frontend')
        
        if frontend == 'react':
            for component in requirements.components:
                if component != 'App':  # Skip App component (already generated)
                    component_code = self.templates['react'].generate_component(component, requirements)
                    component_path = f"{project_path}/src/components/{component}.js"
                    os.makedirs(os.path.dirname(component_path), exist_ok=True)
                    with open(component_path, 'w', encoding='utf-8') as f:
                        f.write(component_code)
                    files[component_path] = component_code
        
        return files

    def _generate_pages(self, requirements: ProjectRequirements, project_path: str) -> Dict[str, str]:
        """Generate page components"""
        files = {}
        frontend = requirements.tech_stack.get('frontend')
        
        if frontend == 'react':
            for page in requirements.pages:
                    page_code = self.templates['react'].generate_page(page, requirements)
                    page_path = f"{project_path}/src/pages/{page}.js"
                    os.makedirs(os.path.dirname(page_path), exist_ok=True)
                    with open(page_path, 'w', encoding='utf-8') as f:
                        f.write(page_code)
                    files[page_path] = page_code
        
        return files

    def _generate_api_files(self, requirements: ProjectRequirements, project_path: str) -> Dict[str, str]:
        """Generate API/backend files"""
        files = {}
        backend = requirements.tech_stack.get('backend')
        
        if backend == 'nodejs':
            # Generate server.js
            server_js = self.templates['nodejs'].generate_server(requirements)
            server_path = f"{project_path}/server/server.js"
            os.makedirs(os.path.dirname(server_path), exist_ok=True)
            with open(server_path, 'w', encoding='utf-8') as f:
                f.write(server_js)
            files[server_path] = server_js
        
        return files

    def _generate_database_files(self, requirements: ProjectRequirements, project_path: str) -> Dict[str, str]:
        """Generate database-related files"""
        files = {}
        database = requirements.tech_stack.get('database')
        
        if database == 'mongodb':
            # Generate database connection
            db_config = self.templates['nodejs'].generate_db_config(requirements)
            db_path = f"{project_path}/server/config/database.js"
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            with open(db_path, 'w', encoding='utf-8') as f:
                f.write(db_config)
            files[db_path] = db_config
        
        return files

    def _generate_documentation(self, requirements: ProjectRequirements, project_path: str) -> Dict[str, str]:
        """Generate project documentation"""
        files = {}
        
        # API documentation
        if requirements.api_endpoints:
            api_docs = self._generate_api_docs(requirements)
            docs_path = f"{project_path}/API.md"
            with open(docs_path, 'w', encoding='utf-8') as f:
                f.write(api_docs)
            files[docs_path] = api_docs
        
        return files

    def _generate_api_docs(self, requirements: ProjectRequirements) -> str:
        """Generate API documentation"""
        docs = f"# {requirements.name} API Documentation\\n\\n"
        
        for endpoint in requirements.api_endpoints:
            docs += f"## {endpoint}\\n"
            docs += f"Description: Auto-generated endpoint\\n\\n"
        
        return docs


class ReactTemplates:
    """React-specific code templates"""
    
    def generate_package_json(self, requirements: ProjectRequirements) -> str:
        """Generate package.json for React project"""
        dependencies = {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.8.0",
            "axios": "^1.3.0"
        }
        
        # Add feature-specific dependencies
        if 'drag-drop' in requirements.features:
            dependencies["react-beautiful-dnd"] = "^13.1.1"
        
        if 'charts' in requirements.features:
            dependencies["chart.js"] = "^4.2.0"
            dependencies["react-chartjs-2"] = "^5.2.0"
        
        if 'authentication' in requirements.features:
            dependencies["jsonwebtoken"] = "^9.0.0"
        
        package = {
            "name": requirements.name.lower().replace(' ', '-'),
            "version": "1.0.0",
            "description": requirements.description,
            "private": True,
            "dependencies": dependencies,
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            },
            "browserslist": {
                "production": [
                    ">0.2%",
                    "not dead",
                    "not op_mini all"
                ],
                "development": [
                    "last 1 chrome version",
                    "last 1 firefox version",
                    "last 1 safari version"
                ]
            }
        }
        
        return json.dumps(package, indent=2)

    def generate_gitignore(self) -> str:
        """Generate .gitignore file"""
        return """# Dependencies
node_modules/
/.pnp
.pnp.js

# Testing
/coverage

# Production
/build

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
"""

    def generate_readme(self, requirements: ProjectRequirements) -> str:
        """Generate README.md"""
        return f"""# {requirements.name}

{requirements.description}

## Features

{chr(10).join([f"- {feature.replace('-', ' ').title()}" for feature in requirements.features])}

## Tech Stack

- Frontend: {requirements.tech_stack.get('frontend', 'N/A').title()}
- Backend: {requirements.tech_stack.get('backend', 'N/A').title()}
- Database: {requirements.tech_stack.get('database', 'N/A').title()}

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production

## Project Structure

```
src/
├── components/     # Reusable components
├── pages/         # Page components
├── hooks/         # Custom hooks
├── services/      # API services
├── utils/         # Utility functions
└── styles/        # CSS/styled-components
```

## Contributing

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License.
"""

    def generate_app_component(self, requirements: ProjectRequirements) -> str:
        """Generate main App component"""
        imports = [
            "import React from 'react';",
            "import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';"
        ]
        
        # Add page imports
        for page in requirements.pages:
            imports.append(f"import {page} from './pages/{page}';")
        
        # Add authentication provider if needed
        if 'authentication' in requirements.features:
            imports.append("import AuthProvider from './components/AuthProvider';")
        
        routes = []
        for page in requirements.pages:
            path = "/" if page == "Home" else f"/{page.lower()}"
            routes.append(f'        <Route path="{path}" element={{{page}()}} />')
        
        app_component = f"""
{chr(10).join(imports)}
import './App.css';

function App() {{
  return (
    <Router>
      {'<AuthProvider>' if 'authentication' in requirements.features else ''}
        <div className="App">
          <Routes>
{chr(10).join(routes)}
          </Routes>
        </div>
      {'</AuthProvider>' if 'authentication' in requirements.features else ''}
    </Router>
  );
}}

export default App;
"""
        return app_component

    def generate_index_js(self, requirements: ProjectRequirements) -> str:
        """Generate src/index.js"""
        return """import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""

    def generate_index_html(self, requirements: ProjectRequirements) -> str:
        """Generate public/index.html"""
        return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="{requirements.description}" />
    <title>{requirements.name}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
"""

    def generate_component(self, component_name: str, requirements: ProjectRequirements) -> str:
        """Generate a React component"""
        # Component-specific templates
        if component_name == 'LoginForm':
            return self._generate_login_form()
        elif component_name == 'Dashboard':
            return self._generate_dashboard()
        else:
            # Generic component template
            return f"""import React from 'react';

const {component_name} = () => {{
  return (
    <div className="{component_name.lower()}">
      <h2>{component_name}</h2>
      <p>This is the {component_name} component.</p>
    </div>
  );
}};

export default {component_name};
"""

    def generate_page(self, page_name: str, requirements: ProjectRequirements) -> str:
        """Generate a React page component"""
        if page_name == 'Home':
            return self._generate_home_page(requirements)
        elif page_name == 'Login':
            return self._generate_login_page()
        else:
            return f"""import React from 'react';

const {page_name} = () => {{
  return (
    <div className="{page_name.lower()}-page">
      <h1>{page_name}</h1>
      <p>Welcome to the {page_name} page.</p>
    </div>
  );
}};

export default {page_name};
"""

    def _generate_home_page(self, requirements: ProjectRequirements) -> str:
        """Generate Home page with project-specific content"""
        return f"""import React from 'react';

const Home = () => {{
  return (
    <div className="home-page">
      <header className="hero">
        <h1>Welcome to {requirements.name}</h1>
        <p>{requirements.description}</p>
      </header>
      
      <section className="features">
        <h2>Features</h2>
        <div className="feature-grid">
          {chr(10).join([f'          <div className="feature-card"><h3>{feature.replace("-", " ").title()}</h3></div>' for feature in requirements.features[:4]])}
        </div>
      </section>
    </div>
  );
}};

export default Home;
"""

    def _generate_login_form(self) -> str:
        """Generate LoginForm component"""
        return """import React, { useState } from 'react';

const LoginForm = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Add your login logic here
      await onLogin({ email, password });
    } catch (error) {
      console.error('Login failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="login-form" onSubmit={handleSubmit}>
      <h2>Login</h2>
      
      <div className="form-group">
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      
      <button type="submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
};

export default LoginForm;
"""

    def _generate_login_page(self) -> str:
        """Generate Login page"""
        return """import React from 'react';
import LoginForm from '../components/LoginForm';

const Login = () => {
  const handleLogin = async (credentials) => {
    // Implement login logic
    console.log('Login attempt:', credentials);
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <LoginForm onLogin={handleLogin} />
      </div>
    </div>
  );
};

export default Login;
"""

    def _generate_dashboard(self) -> str:
        """Generate Dashboard component"""
        return """import React from 'react';

const Dashboard = () => {
  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Dashboard</h1>
      </header>
      
      <div className="dashboard-content">
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Users</h3>
            <p className="stat-number">1,234</p>
          </div>
          
          <div className="stat-card">
            <h3>Active Sessions</h3>
            <p className="stat-number">567</p>
          </div>
          
          <div className="stat-card">
            <h3>Revenue</h3>
            <p className="stat-number">$12,345</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
"""


class NodejsTemplates:
    """Node.js-specific code templates"""
    
    def generate_server(self, requirements: ProjectRequirements) -> str:
        """Generate main server file"""
        return """const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.get('/', (req, res) => {
  res.json({ message: 'Server is running!' });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
"""

    def generate_db_config(self, requirements: ProjectRequirements) -> str:
        """Generate database configuration"""
        return """const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log('MongoDB connected successfully');
  } catch (error) {
    console.error('MongoDB connection error:', error);
    process.exit(1);
  }
};

module.exports = connectDB;
"""


class VueTemplates:
    """Vue.js-specific code templates"""
    pass


class PythonTemplates:
    """Python-specific code templates"""
    pass