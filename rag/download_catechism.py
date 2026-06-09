import requests
from bs4 import BeautifulSoup
import time

def download_catechism():
    base_url = "https://www.vatican.va/archive/ENG0015/__P{}.HTM"
    all_text = []
    
    print("Downloading Catechism from Vatican website...")
    
    # The CCC has sections from index 1 to around 200
    for i in range(1, 200):
        # Convert number to base-36 (Vatican's URL format)
        section = format(i, 'X').lower()
        url = base_url.format(section)
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                text = soup.get_text(separator='\n', strip=True)
                if len(text) > 100:  # Skip empty pages
                    all_text.append(text)
                    print(f"Downloaded section {i}")
            else:
                break
                
        except Exception as e:
            print(f"Stopped at section {i}: {e}")
            break
            
        time.sleep(0.5)  # Be respectful to Vatican servers
    
    # Save to file
    full_text = "\n\n".join(all_text)
    with open("data/catechism_full.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
    
    print(f"Done! Saved {len(all_text)} sections to data/catechism_full.txt")

if __name__ == "__main__":
    download_catechism()
