import requests
import os
from dotenv import load_dotenv

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_web(query):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": query}
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        results = response.json()
        if "organic" in results and results["organic"]:
            top = results["organic"][0]
            return f"{top['title']}: {top['link']}"
        else:
            return "No relevant result found."
    else:
        return f"Search failed. Status: {response.status_code}"

# Example usage (delete or comment out this block in production)
if __name__ == "__main__":
    print(search_web("Who is the CEO of Google?"))