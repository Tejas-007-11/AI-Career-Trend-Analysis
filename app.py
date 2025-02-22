import requests

def get_trending_skills():
    response = requests.get("http://127.0.0.1:5000/trending-skills")
    if response.status_code == 200:
        skills = response.json().get("trending_skills", [])
        print("\nTrending Skills:")
        for skill in skills:
            print(f"- {skill}")
    else:
        print("Error fetching trending skills")

def get_career_recommendations():
    user_skills = input("Enter your skills (comma-separated): ").split(',')
    user_skills = [skill.strip() for skill in user_skills]
    
    response = requests.post("http://127.0.0.1:5000/recommend-career", json={"skills": user_skills})
    if response.status_code == 200:
        recommendations = response.json().get("career_recommendations", [])
        print("\nRecommended Careers:")
        for role, score in recommendations:
            print(f"- {role} (Match Score: {score:.2f})")
    else:
        print("Error fetching career recommendations")

def main():
    while True:
        print("\n1. View Trending Skills")
        print("2. Get Career Recommendations")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            get_trending_skills()
        elif choice == "2":
            get_career_recommendations()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
