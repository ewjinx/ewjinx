import os
import urllib.request
import json
import datetime

USERNAME = "ewjinx" 

def calculate_exact_uptime(birthday):
    """Calculates custom year, month, and day durations cleanly without external dependencies."""
    today = datetime.date.today()
    years = today.year - birthday.year
    months = today.month - birthday.month
    days = today.day - birthday.day
    
    if days < 0:
        months -= 1
        prev_month = today.month - 1 if today.month > 1 else 12
        prev_year = today.year if today.month > 1 else today.year - 1
        
        if prev_month in [1, 3, 5, 7, 8, 10, 12]:
            days += 31
        elif prev_month in [4, 6, 9, 11]:
            days += 30
        else: # February Leap Check
            is_leap = (prev_year % 4 == 0 and prev_year % 100 != 0) or (prev_year % 400 == 0)
            days += 29 if is_leap else 28
            
    if months < 0:
        years -= 1
        months += 12
        
    y_label = f"{years} year{'s' if years != 1 else ''}"
    m_label = f"{months} month{'s' if months != 1 else ''}"
    d_label = f"{days} day{'s' if days != 1 else ''}"
    return f"{y_label}, {m_label}, {d_label}"

def fetch_github_stats():
    token = os.environ.get("GITHUB_TOKEN")
    
    def make_request(url):
        req = urllib.request.Request(url)
        if token:
            req.add_header("Authorization", f"token {token}")
        req.add_header("User-Agent", "Python-Urllib")
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode())

    user_data = make_request(f"https://api.github.com/users/{USERNAME}")
    repos_data = make_request(f"https://api.github.com/users/{USERNAME}/repos?per_page=100")
    total_stars = sum(repo["stargazers_count"] for repo in repos_data)
    
    uptime_str = calculate_exact_uptime(datetime.date(2003, 1, 14))
    
    return {
        "age_data": uptime_str,
        "public_repos": f"{user_data.get('public_repos', 0):,}",
        "followers": f"{user_data.get('followers', 0):,}",
        "stars": f"{total_stars:,}"
    }

def get_justified_dots(label_len, value_len, target_total=14):
    dots_needed = max(1, target_total - (label_len + value_len))
    return ' ' + ('.' * dots_needed) + ' '

def update_svgs(stats):
    # Match the tracking dot column padding boundaries perfectly
    age_dots = get_justified_dots(len("Uptime"), len(stats["age_data"]), 32)
    repo_dots = get_justified_dots(len("Repos"), len(stats["public_repos"]), 10)
    star_dots = get_justified_dots(len("Stars"), len(stats["stars"]), 15)
    follower_dots = get_justified_dots(len("Followers"), len(stats["followers"]), 14)

    for mode in ["dark", "light"]:
        template_name = f"template_{mode}.svg"
        output_name = f"{mode}_mode.svg"
        
        if not os.path.exists(template_name):
            continue
            
        with open(template_name, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Insert strings
        for key, val in stats.items():
            content = content.replace(f"{{{key}}}", val)
            
        # Insert calculated tracking columns
        content = content.replace("{age_dots}", age_dots)
        content = content.replace("{repo_dots}", repo_dots)
        content = content.replace("{star_dots}", star_dots)
        content = content.replace("{follower_dots}", follower_dots)
        
        with open(output_name, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Generated {output_name}")

if __name__ == "__main__":
    github_stats = fetch_github_stats()
    update_svgs(github_stats)
