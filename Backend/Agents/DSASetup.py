import json
import os

def setup_dsa_usernames():
    """Setup DSA platform usernames"""
    data_path = os.path.join("Data", "dsa_progress.json")
    
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    print("DSA Platform Setup")
    print("=" * 30)
    
    platforms = {
        "leetcode": "LeetCode",
        "codechef": "CodeChef", 
        "codeforces": "Codeforces",
        "hackerrank": "HackerRank"
    }
    
    for platform_key, platform_name in platforms.items():
        current = data["platforms"][platform_key]["username"]
        if current:
            print(f"{platform_name} current username: {current}")
            update = input(f"Update {platform_name} username? (y/n): ").lower()
            if update != 'y':
                continue
        
        username = input(f"Enter your {platform_name} username (or press Enter to skip): ").strip()
        if username:
            data["platforms"][platform_key]["username"] = username
            print(f"✓ {platform_name} username set to: {username}")
        else:
            print(f"⚠ {platform_name} username skipped")
    
    with open(data_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("\n✓ DSA setup complete!")
    return data

if __name__ == "__main__":
    setup_dsa_usernames()