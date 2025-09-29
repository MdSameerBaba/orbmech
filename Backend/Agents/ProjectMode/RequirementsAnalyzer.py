"""
Requirements Analyzer for AI Project Generator
Parses natural language requirements and converts to structured project specifications
"""

import re
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ProjectRequirements:
    """Structured representation of project requirements"""
    name: str
    description: str
    tech_stack: Dict[str, str]  # frontend, backend, database, etc.
    features: List[str]
    dependencies: List[str]
    components: List[str]
    pages: List[str]
    api_endpoints: List[str]
    database_schema: Dict[str, List[str]]
    deployment_platform: Optional[str] = None
    authentication: bool = False
    responsive_design: bool = True
    testing_required: bool = True

class RequirementsAnalyzer:
    """Analyzes natural language requirements and extracts structured data"""
    
    def __init__(self):
        self.tech_stack_patterns = {
            # Frontend Frameworks
            'react': ['react', 'react.js', 'reactjs'],
            'vue': ['vue', 'vue.js', 'vuejs'],
            'angular': ['angular', 'angular.js'],
            'svelte': ['svelte', 'sveltekit'],
            'nextjs': ['next.js', 'nextjs', 'next'],
            'nuxt': ['nuxt', 'nuxt.js'],
            
            # Backend Frameworks
            'nodejs': ['node.js', 'nodejs', 'node', 'express'],
            'python': ['python', 'flask', 'django', 'fastapi'],
            'java': ['java', 'spring', 'spring boot'],
            'php': ['php', 'laravel', 'symfony'],
            'ruby': ['ruby', 'rails', 'ruby on rails'],
            
            # Databases
            'mongodb': ['mongodb', 'mongo'],
            'postgresql': ['postgresql', 'postgres'],
            'mysql': ['mysql'],
            'sqlite': ['sqlite'],
            'firebase': ['firebase', 'firestore'],
            
            # Mobile
            'react-native': ['react native', 'react-native'],
            'flutter': ['flutter'],
            'ionic': ['ionic']
        }
        
        self.feature_patterns = {
            'authentication': ['auth', 'login', 'signup', 'register', 'authentication', 'user management'],
            'payment': ['payment', 'stripe', 'paypal', 'checkout', 'billing'],
            'real-time': ['real-time', 'realtime', 'websocket', 'live', 'chat'],
            'file-upload': ['file upload', 'image upload', 'upload', 'file handling'],
            'notifications': ['notifications', 'push notifications', 'alerts'],
            'search': ['search', 'filtering', 'search functionality'],
            'dashboard': ['dashboard', 'admin panel', 'analytics'],
            'crud': ['crud', 'create', 'read', 'update', 'delete'],
            'drag-drop': ['drag and drop', 'drag-and-drop', 'draggable'],
            'responsive': ['responsive', 'mobile-friendly', 'mobile responsive'],
            'dark-mode': ['dark mode', 'theme switching', 'dark theme'],
            'social': ['social', 'share', 'social media', 'sharing'],
            'api': ['api', 'rest api', 'graphql', 'endpoints'],
            'cms': ['cms', 'content management', 'admin'],
            'ecommerce': ['ecommerce', 'e-commerce', 'shopping cart', 'online store'],
            'blog': ['blog', 'blogging', 'articles', 'posts'],
            'portfolio': ['portfolio', 'showcase'],
            'charts': ['charts', 'graphs', 'data visualization', 'analytics'],
            'map': ['map', 'google maps', 'location', 'geolocation']
        }
        
        self.project_types = {
            'web-app': ['web app', 'web application', 'website'],
            'mobile-app': ['mobile app', 'mobile application', 'app'],
            'desktop-app': ['desktop app', 'desktop application'],
            'api': ['api', 'backend', 'server', 'microservice'],
            'fullstack': ['fullstack', 'full-stack', 'full stack'],
            'frontend': ['frontend', 'front-end', 'client-side'],
            'backend': ['backend', 'back-end', 'server-side']
        }

    def analyze(self, requirements_text: str) -> ProjectRequirements:
        """Main method to analyze requirements text"""
        requirements_lower = requirements_text.lower()
        
        # Extract project name
        name = self._extract_project_name(requirements_text)
        
        # Determine project type
        project_type = self._detect_project_type(requirements_lower)
        
        # Extract tech stack
        tech_stack = self._detect_tech_stack(requirements_lower, project_type)
        
        # Extract features
        features = self._extract_features(requirements_lower)
        
        # Generate components based on features
        components = self._generate_components(features, tech_stack)
        
        # Generate pages
        pages = self._generate_pages(features, project_type)
        
        # Generate dependencies
        dependencies = self._generate_dependencies(tech_stack, features)
        
        # Generate API endpoints
        api_endpoints = self._generate_api_endpoints(features)
        
        # Generate database schema
        database_schema = self._generate_database_schema(features)
        
        # Check for authentication
        has_auth = any(keyword in requirements_lower for keywords in self.feature_patterns['authentication'] for keyword in keywords)
        
        return ProjectRequirements(
            name=name,
            description=requirements_text,
            tech_stack=tech_stack,
            features=features,
            components=components,
            pages=pages,
            dependencies=dependencies,
            api_endpoints=api_endpoints,
            database_schema=database_schema,
            authentication=has_auth,
            responsive_design=True,  # Default to responsive
            testing_required=True    # Default to include testing
        )

    def _extract_project_name(self, text: str) -> str:
        """Extract project name from requirements text"""
        # Look for quoted project names
        quoted_match = re.search(r'["\']([^"\']+)["\']', text)
        if quoted_match:
            return quoted_match.group(1)
        
        # Look for "create [name] app" pattern
        create_match = re.search(r'create\s+(\w+(?:\s+\w+)*)\s+(?:app|application|website|project)', text, re.IGNORECASE)
        if create_match:
            return create_match.group(1).title()
        
        # Default fallback
        return "AI Generated Project"

    def _detect_project_type(self, text: str) -> str:
        """Detect the type of project"""
        for project_type, keywords in self.project_types.items():
            if any(keyword in text for keyword in keywords):
                return project_type
        return 'web-app'  # Default

    def _detect_tech_stack(self, text: str, project_type: str) -> Dict[str, str]:
        """Detect technology stack from requirements"""
        tech_stack = {}
        
        # Detect specific technologies
        for tech, keywords in self.tech_stack_patterns.items():
            if any(keyword in text for keyword in keywords):
                if tech in ['react', 'vue', 'angular', 'svelte']:
                    tech_stack['frontend'] = tech
                elif tech in ['nodejs', 'python', 'java', 'php', 'ruby']:
                    tech_stack['backend'] = tech
                elif tech in ['mongodb', 'postgresql', 'mysql', 'sqlite', 'firebase']:
                    tech_stack['database'] = tech
                elif tech in ['react-native', 'flutter', 'ionic']:
                    tech_stack['mobile'] = tech
        
        # Apply defaults based on project type
        if not tech_stack.get('frontend') and project_type in ['web-app', 'fullstack']:
            tech_stack['frontend'] = 'react'  # Default to React
        
        if not tech_stack.get('backend') and project_type in ['fullstack', 'backend', 'api']:
            tech_stack['backend'] = 'nodejs'  # Default to Node.js
        
        if not tech_stack.get('database') and any(feature in text for feature in ['user', 'data', 'store', 'save']):
            tech_stack['database'] = 'mongodb'  # Default to MongoDB
        
        return tech_stack

    def _extract_features(self, text: str) -> List[str]:
        """Extract features from requirements text"""
        detected_features = []
        
        for feature, keywords in self.feature_patterns.items():
            if any(keyword in text for keyword in keywords):
                detected_features.append(feature)
        
        return detected_features

    def _generate_components(self, features: List[str], tech_stack: Dict[str, str]) -> List[str]:
        """Generate component list based on features and tech stack"""
        components = ['App']  # Always include main App component
        
        feature_components = {
            'authentication': ['LoginForm', 'RegisterForm', 'AuthProvider', 'ProtectedRoute'],
            'dashboard': ['Dashboard', 'Sidebar', 'Header', 'StatsCard'],
            'crud': ['DataTable', 'CreateForm', 'EditForm', 'DeleteModal'],
            'search': ['SearchBar', 'SearchResults', 'FilterPanel'],
            'notifications': ['NotificationCenter', 'NotificationItem'],
            'file-upload': ['FileUploader', 'ImagePreview', 'UploadProgress'],
            'charts': ['Chart', 'LineChart', 'BarChart', 'PieChart'],
            'payment': ['PaymentForm', 'CheckoutSummary', 'PaymentSuccess'],
            'chat': ['ChatRoom', 'MessageList', 'MessageInput'],
            'blog': ['BlogPost', 'BlogList', 'BlogEditor'],
            'ecommerce': ['ProductCard', 'ShoppingCart', 'ProductDetail']
        }
        
        for feature in features:
            if feature in feature_components:
                components.extend(feature_components[feature])
        
        return list(set(components))  # Remove duplicates

    def _generate_pages(self, features: List[str], project_type: str) -> List[str]:
        """Generate page list based on features"""
        pages = ['Home']  # Always include home page
        
        feature_pages = {
            'authentication': ['Login', 'Register', 'Profile'],
            'dashboard': ['Dashboard', 'Analytics'],
            'blog': ['BlogHome', 'BlogPost', 'CreatePost'],
            'ecommerce': ['Products', 'ProductDetail', 'Cart', 'Checkout'],
            'portfolio': ['About', 'Projects', 'Contact'],
            'cms': ['AdminPanel', 'ContentManager']
        }
        
        for feature in features:
            if feature in feature_pages:
                pages.extend(feature_pages[feature])
        
        return list(set(pages))

    def _generate_dependencies(self, tech_stack: Dict[str, str], features: List[str]) -> List[str]:
        """Generate dependency list based on tech stack and features"""
        dependencies = []
        
        # Base dependencies by framework
        framework_deps = {
            'react': ['react', 'react-dom', 'react-router-dom'],
            'vue': ['vue', 'vue-router', 'vuex'],
            'angular': ['@angular/core', '@angular/common', '@angular/router'],
            'nodejs': ['express', 'cors', 'dotenv'],
            'python': ['flask', 'requests', 'python-dotenv'],
        }
        
        # Add base dependencies
        for tech_type, tech in tech_stack.items():
            if tech in framework_deps:
                dependencies.extend(framework_deps[tech])
        
        # Feature-specific dependencies
        feature_deps = {
            'authentication': ['jsonwebtoken', 'bcryptjs', 'passport'],
            'payment': ['stripe', '@stripe/stripe-js'],
            'drag-drop': ['react-beautiful-dnd', 'react-dnd'],
            'charts': ['chart.js', 'react-chartjs-2'],
            'styling': ['styled-components', 'emotion', 'tailwindcss'],
            'testing': ['jest', 'testing-library/react', 'testing-library/jest-dom'],
            'api': ['axios', 'fetch'],
            'state': ['redux', '@reduxjs/toolkit', 'zustand']
        }
        
        # Add feature dependencies
        for feature in features:
            if feature in feature_deps:
                dependencies.extend(feature_deps[feature])
        
        # Add some common dependencies
        if tech_stack.get('frontend') == 'react':
            dependencies.extend(['axios', 'styled-components'])
        
        return list(set(dependencies))

    def _generate_api_endpoints(self, features: List[str]) -> List[str]:
        """Generate API endpoint list based on features"""
        endpoints = []
        
        feature_endpoints = {
            'authentication': ['/api/auth/login', '/api/auth/register', '/api/auth/logout', '/api/user/profile'],
            'crud': ['/api/items', '/api/items/:id'],
            'payment': ['/api/payment/create-intent', '/api/payment/confirm'],
            'file-upload': ['/api/upload', '/api/files/:id'],
            'blog': ['/api/posts', '/api/posts/:id', '/api/posts/:id/comments'],
            'ecommerce': ['/api/products', '/api/products/:id', '/api/cart', '/api/orders']
        }
        
        for feature in features:
            if feature in feature_endpoints:
                endpoints.extend(feature_endpoints[feature])
        
        return list(set(endpoints))

    def _generate_database_schema(self, features: List[str]) -> Dict[str, List[str]]:
        """Generate database schema based on features"""
        schema = {}
        
        feature_schemas = {
            'authentication': {
                'users': ['id', 'email', 'password', 'name', 'createdAt', 'updatedAt']
            },
            'blog': {
                'posts': ['id', 'title', 'content', 'authorId', 'createdAt', 'updatedAt'],
                'comments': ['id', 'postId', 'authorId', 'content', 'createdAt']
            },
            'ecommerce': {
                'products': ['id', 'name', 'price', 'description', 'imageUrl', 'stock'],
                'orders': ['id', 'userId', 'total', 'status', 'createdAt'],
                'orderItems': ['id', 'orderId', 'productId', 'quantity', 'price']
            }
        }
        
        for feature in features:
            if feature in feature_schemas:
                schema.update(feature_schemas[feature])
        
        return schema

    def get_recommendations(self, requirements: ProjectRequirements) -> Dict[str, List[str]]:
        """Get recommendations for improving the project"""
        recommendations = {
            'additional_features': [],
            'best_practices': [],
            'performance_tips': [],
            'security_considerations': []
        }
        
        # Additional features based on current features
        if 'authentication' in requirements.features:
            recommendations['additional_features'].extend([
                'Password reset functionality',
                'Email verification',
                'Two-factor authentication'
            ])
        
        if 'ecommerce' in requirements.features:
            recommendations['additional_features'].extend([
                'Order tracking',
                'Inventory management',
                'Customer reviews'
            ])
        
        # Best practices
        recommendations['best_practices'].extend([
            'Implement proper error handling',
            'Add loading states',
            'Use TypeScript for better type safety',
            'Implement proper logging'
        ])
        
        return recommendations