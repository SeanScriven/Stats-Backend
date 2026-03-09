import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("RUGBY_BASE_URL")

# API-Sports requires the key in a specific header
headers = {
    "x-apisports-key": API_KEY,
    "x-rapidapi-host": "v1.rugby.api-sports.io"
}

def get_leagues():
    if not API_KEY:
        print("❌ Error: API Key not found. Check your .env file!")
        return
    
    with httpx.Client(headers=headers) as client:
        print("🚀 Fetching Rugby Leagues...")
        
        # Making the request
        response = client.get(f"{BASE_URL}/leagues")
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            leagues = data.get("response", [])
            
            print(f"✅ Found {len(leagues)} leagues!\n")
            print(f"{'ID':<5} | {'Name':<25} | {'Country'}")
            print("-" * 50)
            
            # Print the first 10 for a quick look
            for league in leagues[:10]:
                name = league['name']
                country = league['country']['name']
                league_id = league['id']
                print(f"{league_id:<5} | {name:<25} | {country}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    get_leagues()