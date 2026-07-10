import os
import urllib.request
import json

# double-check that this is exactly your username lowercase
USERNAME = "ewjinx" 

def fetch_github_stats():
    # Use the built-in GitHub Action token to avoid API rate limits
    token = os.environ.get("GITHUB_TOKEN")
    
    def make_request(url):
        req = urllib.request.Request(url)
        if token:
            req.add_header("Authorization", f"token {token}")
        req.add_header("User-Agent", "Python-Urllib")
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode())

    # Fetch user general data
    user_data = make_request(f"https://api.github.com/users/{USERNAME}")
    
    # Fetch user repository data to calculate total star count
    repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    repos_data = make_request(repos_url)
    
    total_stars = sum(repo["stargazers_count"] for repo in repos_data)
    
    return {
        "public_repos": str(user_data.get("public_repos", 0)),
        "followers": str(user_data.get("followers", 0)),
        "stars": str(total_stars)
    }

def update_svgs(stats):
    for mode in ["dark", "light"]:
        template_name = f"template_{mode}.svg"
        output_name = f"{mode}_mode.svg"
        
        with open(template_name, "r", encoding="utf-8") as file:
            content = file.read()
        
        updated_content = content.format(**stats)
        
        with open(output_name, "w", encoding="utf-8") as file:
            file.write(updated_content)
        print(f"Successfully generated {output_name}")

if __name__ == "__main__":
    # Removed the blind try/except block so GitHub can report real script errors
    stats = fetch_github_stats()
    update_svgs(stats)
