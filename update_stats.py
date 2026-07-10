import os
import urllib.request
import json

# Replace with your actual GitHub username
USERNAME = "ewjinx"

def fetch_github_stats():
    # Fetch user general data
    user_url = f"https://api.github.com/users/{USERNAME}"
    user_response = urllib.request.urlopen(user_url)
    user_data = json.loads(user_response.read().decode())
    
    # Fetch user repository data to calculate total star count
    repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    repos_response = urllib.request.urlopen(repos_url)
    repos_data = json.loads(repos_response.read().decode())
    
    total_stars = sum(repo["stargazers_count"] for repo in repos_data)
    
    return {
        "public_repos": str(user_data.get("public_repos", 0)),
        "followers": str(user_data.get("followers", 0)),
        "stars": str(total_stars)
    }

def update_svgs(stats):
    # Process both dark and light variations
    for mode in ["dark", "light"]:
        template_name = f"template_{mode}.svg"
        output_name = f"{mode}_mode.svg"
        
        if os.path.exists(template_name):
            with open(template_name, "r", encoding="utf-8") as file:
                content = file.read()
            
            # Safely format strings using our placeholders
            updated_content = content.format(**stats)
            
            with open(output_name, "w", encoding="utf-8") as file:
                file.write(updated_content)
            print(f"Successfully generated {output_name}")

if __name__ == "__main__":
    try:
        stats = fetch_github_stats()
        update_svgs(stats)
    except Exception as e:
        print(f"Error executing script: {e}")
