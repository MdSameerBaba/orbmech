#!/usr/bin/env python3
"""
Enhanced AI Project Generator - Full-Stack Architecture
Schema-First Approach with Proper Frontend/Backend Separation
"""

import os
import json
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

@dataclass
class DatabaseSchema:
    """Database schema definition"""
    entities: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]
    indexes: List[str]
    constraints: List[str]

@dataclass 
class APIEndpoint:
    """API endpoint definition"""
    path: str
    method: str
    description: str
    request_body: Dict[str, Any]
    response_body: Dict[str, Any]
    auth_required: bool

@dataclass
class FullStackArchitecture:
    """Complete full-stack project architecture"""
    project_name: str
    database_schema: DatabaseSchema
    api_endpoints: List[APIEndpoint]
    frontend_pages: List[str]
    frontend_components: List[str]
    frontend_routes: List[Dict[str, str]]
    tech_stack: Dict[str, str]
    features: List[str]

class EnhancedRequirementsAnalyzer:
    """Enhanced analyzer for full-stack requirements"""
    
    def analyze_requirements(self, requirements: str) -> FullStackArchitecture:
        """Analyze requirements and create full-stack architecture"""
        print(f"🔍 Analyzing full-stack requirements: {requirements}")
        
        # Step 1: Detect project type and tech stack
        tech_stack = self._detect_tech_stack(requirements)
        project_name = self._extract_project_name(requirements)
        features = self._extract_features(requirements)
        
        # Step 2: Design database schema first
        print("📊 Designing database schema...")
        database_schema = self._design_database_schema(requirements, features)
        
        # Step 3: Define API endpoints based on schema
        print("🔗 Defining API endpoints...")
        api_endpoints = self._design_api_endpoints(database_schema, features)
        
        # Step 4: Plan frontend architecture
        print("🎨 Planning frontend architecture...")
        frontend_pages = self._plan_frontend_pages(features, api_endpoints)
        frontend_components = self._plan_frontend_components(features)
        frontend_routes = self._plan_frontend_routes(frontend_pages)
        
        return FullStackArchitecture(
            project_name=project_name,
            database_schema=database_schema,
            api_endpoints=api_endpoints,
            frontend_pages=frontend_pages,
            frontend_components=frontend_components,
            frontend_routes=frontend_routes,
            tech_stack=tech_stack,
            features=features
        )
    
    def _detect_tech_stack(self, requirements: str) -> Dict[str, str]:
        """Detect technology stack from requirements"""
        req_lower = requirements.lower()
        
        tech_stack = {}
        
        # Frontend detection
        if 'react' in req_lower:
            tech_stack['frontend'] = 'react'
        elif 'vue' in req_lower:
            tech_stack['frontend'] = 'vue'
        elif 'angular' in req_lower:
            tech_stack['frontend'] = 'angular'
        else:
            tech_stack['frontend'] = 'react'  # default
        
        # Backend detection
        if 'node' in req_lower or 'express' in req_lower:
            tech_stack['backend'] = 'nodejs'
        elif 'python' in req_lower or 'flask' in req_lower:
            tech_stack['backend'] = 'python'
        elif 'django' in req_lower:
            tech_stack['backend'] = 'django'
        else:
            tech_stack['backend'] = 'nodejs'  # default
        
        # Database detection
        if 'mongodb' in req_lower or 'mongo' in req_lower:
            tech_stack['database'] = 'mongodb'
        elif 'postgresql' in req_lower or 'postgres' in req_lower:
            tech_stack['database'] = 'postgresql'
        elif 'mysql' in req_lower:
            tech_stack['database'] = 'mysql'
        else:
            tech_stack['database'] = 'mongodb'  # default
        
        return tech_stack
    
    def _extract_project_name(self, requirements: str) -> str:
        """Extract project name from requirements"""
        req_lower = requirements.lower()
        
        if 'todo' in req_lower:
            return "TodoApp"
        elif 'ecommerce' in req_lower or 'shop' in req_lower:
            return "EcommerceApp"
        elif 'blog' in req_lower:
            return "BlogApp"
        elif 'chat' in req_lower:
            return "ChatApp"
        elif 'dashboard' in req_lower:
            return "DashboardApp"
        else:
            return "FullStackApp"
    
    def _extract_features(self, requirements: str) -> List[str]:
        """Extract features from requirements"""
        req_lower = requirements.lower()
        features = []
        
        feature_keywords = {
            'authentication': ['auth', 'login', 'register', 'signup', 'jwt'],
            'crud': ['create', 'read', 'update', 'delete', 'manage'],
            'real-time': ['real-time', 'live', 'socket', 'websocket'],
            'payment': ['payment', 'stripe', 'paypal', 'billing'],
            'search': ['search', 'filter', 'find'],
            'upload': ['upload', 'file', 'image'],
            'email': ['email', 'notification', 'mail'],
            'dashboard': ['dashboard', 'analytics', 'charts'],
            'api': ['api', 'rest', 'endpoint']
        }
        
        for feature, keywords in feature_keywords.items():
            if any(keyword in req_lower for keyword in keywords):
                features.append(feature)
        
        return features or ['crud']  # default
    
    def _design_database_schema(self, requirements: str, features: List[str]) -> DatabaseSchema:
        """Design database schema based on requirements"""
        entities = []
        relationships = []
        
        # Always include User entity if authentication is needed
        if 'authentication' in features:
            entities.append({
                "name": "User",
                "fields": [
                    {"name": "id", "type": "string", "primary": True},
                    {"name": "email", "type": "string", "unique": True},
                    {"name": "password", "type": "string"},
                    {"name": "firstName", "type": "string"},
                    {"name": "lastName", "type": "string"},
                    {"name": "role", "type": "string", "default": "user"},
                    {"name": "createdAt", "type": "datetime"},
                    {"name": "updatedAt", "type": "datetime"}
                ]
            })
        
        # Project-specific entities
        req_lower = requirements.lower()
        
        if 'todo' in req_lower:
            entities.append({
                "name": "Todo",
                "fields": [
                    {"name": "id", "type": "string", "primary": True},
                    {"name": "title", "type": "string", "required": True},
                    {"name": "description", "type": "text"},
                    {"name": "completed", "type": "boolean", "default": False},
                    {"name": "priority", "type": "string", "default": "medium"},
                    {"name": "dueDate", "type": "datetime"},
                    {"name": "userId", "type": "string", "foreign_key": "User.id"},
                    {"name": "createdAt", "type": "datetime"},
                    {"name": "updatedAt", "type": "datetime"}
                ]
            })
            
            if 'authentication' in features:
                relationships.append({
                    "type": "one-to-many",
                    "from": "User",
                    "to": "Todo",
                    "foreign_key": "userId"
                })
        
        elif 'ecommerce' in req_lower:
            entities.extend([
                {
                    "name": "Product",
                    "fields": [
                        {"name": "id", "type": "string", "primary": True},
                        {"name": "name", "type": "string", "required": True},
                        {"name": "description", "type": "text"},
                        {"name": "price", "type": "decimal", "required": True},
                        {"name": "stock", "type": "integer", "default": 0},
                        {"name": "category", "type": "string"},
                        {"name": "imageUrl", "type": "string"},
                        {"name": "createdAt", "type": "datetime"},
                        {"name": "updatedAt", "type": "datetime"}
                    ]
                },
                {
                    "name": "Order",
                    "fields": [
                        {"name": "id", "type": "string", "primary": True},
                        {"name": "userId", "type": "string", "foreign_key": "User.id"},
                        {"name": "status", "type": "string", "default": "pending"},
                        {"name": "total", "type": "decimal", "required": True},
                        {"name": "createdAt", "type": "datetime"},
                        {"name": "updatedAt", "type": "datetime"}
                    ]
                }
            ])
        
        elif 'blog' in req_lower:
            entities.append({
                "name": "Post",
                "fields": [
                    {"name": "id", "type": "string", "primary": True},
                    {"name": "title", "type": "string", "required": True},
                    {"name": "content", "type": "text", "required": True},
                    {"name": "excerpt", "type": "text"},
                    {"name": "published", "type": "boolean", "default": False},
                    {"name": "authorId", "type": "string", "foreign_key": "User.id"},
                    {"name": "createdAt", "type": "datetime"},
                    {"name": "updatedAt", "type": "datetime"}
                ]
            })
        
        return DatabaseSchema(
            entities=entities,
            relationships=relationships,
            indexes=["User.email", "Todo.userId", "Post.authorId"],
            constraints=["User.email UNIQUE", "User.id NOT NULL"]
        )
    
    def _design_api_endpoints(self, schema: DatabaseSchema, features: List[str]) -> List[APIEndpoint]:
        """Design API endpoints based on database schema"""
        endpoints = []
        
        # Authentication endpoints
        if 'authentication' in features:
            endpoints.extend([
                APIEndpoint(
                    path="/api/auth/register",
                    method="POST",
                    description="Register new user",
                    request_body={"email": "string", "password": "string", "firstName": "string", "lastName": "string"},
                    response_body={"user": "User", "token": "string"},
                    auth_required=False
                ),
                APIEndpoint(
                    path="/api/auth/login",
                    method="POST",
                    description="Login user",
                    request_body={"email": "string", "password": "string"},
                    response_body={"user": "User", "token": "string"},
                    auth_required=False
                ),
                APIEndpoint(
                    path="/api/auth/profile",
                    method="GET",
                    description="Get user profile",
                    request_body={},
                    response_body={"user": "User"},
                    auth_required=True
                )
            ])
        
        # CRUD endpoints for each entity
        for entity in schema.entities:
            if entity["name"] != "User":  # User handled by auth
                entity_name = entity["name"].lower()
                endpoints.extend([
                    APIEndpoint(
                        path=f"/api/{entity_name}s",
                        method="GET",
                        description=f"Get all {entity_name}s",
                        request_body={},
                        response_body={f"{entity_name}s": f"Array<{entity['name']}>"},
                        auth_required='authentication' in features
                    ),
                    APIEndpoint(
                        path=f"/api/{entity_name}s",
                        method="POST",
                        description=f"Create new {entity_name}",
                        request_body={field["name"]: field["type"] for field in entity["fields"] if not field.get("primary")},
                        response_body={entity_name: entity["name"]},
                        auth_required='authentication' in features
                    ),
                    APIEndpoint(
                        path=f"/api/{entity_name}s/:id",
                        method="PUT",
                        description=f"Update {entity_name}",
                        request_body={field["name"]: field["type"] for field in entity["fields"] if not field.get("primary")},
                        response_body={entity_name: entity["name"]},
                        auth_required='authentication' in features
                    ),
                    APIEndpoint(
                        path=f"/api/{entity_name}s/:id",
                        method="DELETE",
                        description=f"Delete {entity_name}",
                        request_body={},
                        response_body={"message": "string"},
                        auth_required='authentication' in features
                    )
                ])
        
        return endpoints
    
    def _plan_frontend_pages(self, features: List[str], api_endpoints: List[APIEndpoint]) -> List[str]:
        """Plan frontend pages based on features"""
        pages = ["Home"]
        
        if 'authentication' in features:
            pages.extend(["Login", "Register", "Profile"])
        
        # Add pages based on entities
        unique_entities = set()
        for endpoint in api_endpoints:
            if "/api/" in endpoint.path and endpoint.method == "GET":
                entity = endpoint.path.split("/")[-1].rstrip("s")
                if entity not in ["auth", "profile"]:
                    unique_entities.add(entity.capitalize())
        
        for entity in unique_entities:
            pages.extend([f"{entity}List", f"{entity}Detail", f"Create{entity}"])
        
        return pages
    
    def _plan_frontend_components(self, features: List[str]) -> List[str]:
        """Plan frontend components based on features"""
        components = ["Header", "Footer", "Layout"]
        
        if 'authentication' in features:
            components.extend(["LoginForm", "RegisterForm", "ProtectedRoute", "AuthProvider"])
        
        if 'crud' in features:
            components.extend(["DataTable", "CreateForm", "EditForm", "DeleteModal"])
        
        if 'search' in features:
            components.extend(["SearchBar", "FilterPanel"])
        
        if 'upload' in features:
            components.extend(["FileUpload", "ImageUpload"])
        
        return components
    
    def _plan_frontend_routes(self, pages: List[str]) -> List[Dict[str, str]]:
        """Plan frontend routes based on pages"""
        routes = []
        
        route_mapping = {
            "Home": "/",
            "Login": "/login",
            "Register": "/register", 
            "Profile": "/profile",
            "TodoList": "/todos",
            "TodoDetail": "/todos/:id",
            "CreateTodo": "/todos/create",
            "ProductList": "/products",
            "ProductDetail": "/products/:id",
            "CreateProduct": "/products/create",
            "PostList": "/posts",
            "PostDetail": "/posts/:id",
            "CreatePost": "/posts/create"
        }
        
        for page in pages:
            if page in route_mapping:
                routes.append({
                    "path": route_mapping[page],
                    "component": page,
                    "protected": page not in ["Home", "Login", "Register"]
                })
        
        return routes

if __name__ == "__main__":
    analyzer = EnhancedRequirementsAnalyzer()
    
    # Test with todo app
    requirements = "create react todo app with authentication and drag and drop"
    architecture = analyzer.analyze_requirements(requirements)
    
    print("\\n🏗️ FULL-STACK ARCHITECTURE:")
    print("=" * 50)
    print(f"📛 Project: {architecture.project_name}")
    print(f"🛠️ Tech Stack: {architecture.tech_stack}")
    print(f"⚡ Features: {architecture.features}")
    
    print(f"\\n📊 Database Schema ({len(architecture.database_schema.entities)} entities):")
    for entity in architecture.database_schema.entities:
        print(f"   • {entity['name']} ({len(entity['fields'])} fields)")
    
    print(f"\\n🔗 API Endpoints ({len(architecture.api_endpoints)} endpoints):")
    for endpoint in architecture.api_endpoints[:5]:  # Show first 5
        print(f"   • {endpoint.method} {endpoint.path}")
    
    print(f"\\n🎨 Frontend Pages ({len(architecture.frontend_pages)} pages):")
    for page in architecture.frontend_pages:
        print(f"   • {page}")
    
    print(f"\\n🧩 Components ({len(architecture.frontend_components)} components):")
    for component in architecture.frontend_components:
        print(f"   • {component}")
    
    print(f"\\n🛣️ Routes ({len(architecture.frontend_routes)} routes):")
    for route in architecture.frontend_routes:
        protected = "🔒" if route.get("protected") else "🔓"
        print(f"   • {protected} {route['path']} → {route['component']}")