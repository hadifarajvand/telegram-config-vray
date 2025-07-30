#!/usr/bin/env python3
"""
Setup script for Telegram Configuration Collector
This script helps you configure the repository for your own use.
"""

import os
import re
import json

def update_readme(username, repo_name):
    """Update README.md with your GitHub username and repository name"""
    readme_path = "readme.md"
    
    if not os.path.exists(readme_path):
        print("❌ README.md not found!")
        return False
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace placeholders with actual values
    content = content.replace('YOUR_USERNAME', username)
    content = content.replace('YOUR_REPO_NAME', repo_name)
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated README.md with {username}/{repo_name}")
    return True

def update_workflows(email, name):
    """Update GitHub workflow files with your email and name"""
    workflow_files = [
        ".github/workflows/schedule.yml",
        ".github/workflows/push.yml"
    ]
    
    for workflow_file in workflow_files:
        if not os.path.exists(workflow_file):
            print(f"❌ {workflow_file} not found!")
            continue
        
        with open(workflow_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace placeholder email and name
        content = content.replace('your-email@example.com', email)
        content = content.replace('Your Name', name)
        
        with open(workflow_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {workflow_file}")

def create_initial_files():
    """Create initial files if they don't exist"""
    
    # Create last update file
    if not os.path.exists("last update"):
        with open("last update", "w") as f:
            from datetime import datetime, timezone, timedelta
            current_datetime = datetime.now(tz=timezone(timedelta(hours=3, minutes=30)))
            f.write(str(current_datetime))
        print("✅ Created 'last update' file")
    
    # Create invalid telegram channels file
    if not os.path.exists("invalid telegram channels.json"):
        with open("invalid telegram channels.json", "w") as f:
            json.dump([], f, indent=4)
        print("✅ Created 'invalid telegram channels.json' file")
    
    # Create splitted directory and no-match file
    os.makedirs("splitted", exist_ok=True)
    if not os.path.exists("splitted/no-match"):
        with open("splitted/no-match", "w") as f:
            f.write("#Non-Adaptive Configurations\n")
        print("✅ Created 'splitted/no-match' file")

def main():
    print("🚀 Telegram Configuration Collector Setup")
    print("=" * 50)
    
    # Get user information
    username = input("Enter your GitHub username (default: hadifarajvand): ").strip() or "hadifarajvand"
    repo_name = input("Enter your repository name (default: telegram-config-vray): ").strip() or "telegram-config-vray"
    email = input("Enter your email address (default: hadifarajvand@gmail.com): ").strip() or "hadifarajvand@gmail.com"
    name = input("Enter your name (default: Hadi Farajvand): ").strip() or "Hadi Farajvand"
    
    if not all([username, repo_name, email, name]):
        print("❌ All fields are required!")
        return
    
    print("\n📝 Updating files...")
    
    # Update README
    if update_readme(username, repo_name):
        print("✅ README.md updated successfully")
    
    # Update workflows
    update_workflows(email, name)
    
    # Create initial files
    create_initial_files()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Review and customize 'telegram channels.json' with your preferred channels")
    print("2. Review and customize 'subscription links.json' with your preferred sources")
    print("3. Commit and push your changes to GitHub")
    print("4. Enable GitHub Actions in your repository settings")
    print("5. The script will run automatically every hour and on push events")

if __name__ == "__main__":
    main() 