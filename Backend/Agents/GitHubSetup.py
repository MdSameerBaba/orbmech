import os
import json
from dotenv import dotenv_values

def setup_github_credentials():
    """Setup GitHub credentials for Git integration"""
    print("🔧 GITHUB SETUP")
    print("=" * 40)
    
    env_vars = dotenv_values(".env")
    current_username = env_vars.get("GITHUB_USERNAME", "")
    current_token = env_vars.get("GITHUB_TOKEN", "")
    
    if current_username and current_token:
        print(f"Current GitHub username: {current_username}")
        update = input("Update GitHub credentials? (y/n): ").lower()
        if update != 'y':
            return True
    
    print("\n📋 To use GitHub integration, you need:")
    print("1. Your GitHub username")
    print("2. A Personal Access Token (PAT)")
    print("\n🔗 Create PAT at: https://github.com/settings/tokens")
    print("Required permissions: repo, workflow, write:packages")
    
    username = input("\nEnter your GitHub username: ").strip()
    if not username:
        print("❌ GitHub username is required")
        return False
    
    token = input("Enter your GitHub Personal Access Token: ").strip()
    if not token:
        print("❌ GitHub token is required")
        return False
    
    # Update .env file
    try:
        env_path = ".env"
        env_lines = []
        
        # Read existing .env
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                env_lines = f.readlines()
        
        # Update or add GitHub credentials
        github_username_found = False
        github_token_found = False
        
        for i, line in enumerate(env_lines):
            if line.startswith("GITHUB_USERNAME="):
                env_lines[i] = f"GITHUB_USERNAME={username}\n"
                github_username_found = True
            elif line.startswith("GITHUB_TOKEN="):
                env_lines[i] = f"GITHUB_TOKEN={token}\n"
                github_token_found = True
        
        # Add if not found
        if not github_username_found:
            env_lines.append(f"GITHUB_USERNAME={username}\n")
        if not github_token_found:
            env_lines.append(f"GITHUB_TOKEN={token}\n")
        
        # Write back to .env
        with open(env_path, 'w') as f:
            f.writelines(env_lines)
        
        print(f"✅ GitHub credentials saved!")
        print(f"Username: {username}")
        print(f"Token: {'*' * (len(token) - 4) + token[-4:]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving credentials: {e}")
        return False

def verify_github_setup():
    """Verify GitHub CLI and credentials are properly configured"""
    import subprocess
    
    try:
        # Check if GitHub CLI is installed
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            return False, "GitHub CLI not installed. Install from: https://cli.github.com/"
        
        # Check if authenticated
        result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            return False, "GitHub CLI not authenticated. Run: gh auth login"
        
        return True, "GitHub CLI is properly configured"
        
    except FileNotFoundError:
        return False, "GitHub CLI not found. Install from: https://cli.github.com/"
    except Exception as e:
        return False, f"Error checking GitHub setup: {e}"

def get_github_credentials():
    """Get GitHub credentials from environment"""
    env_vars = dotenv_values(".env")
    return {
        "username": env_vars.get("GITHUB_USERNAME", ""),
        "token": env_vars.get("GITHUB_TOKEN", "")
    }

if __name__ == "__main__":
    setup_github_credentials()