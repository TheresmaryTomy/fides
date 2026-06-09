import requests
from bs4 import BeautifulSoup
import time

def download_nabre():
    """Download NABRE from USCCB website"""
    
    base_url = "https://bible.usccb.org/bible"
    
    books = [
        "genesis", "exodus", "leviticus", "numbers", "deuteronomy",
        "joshua", "judges", "ruth", "1-samuel", "2-samuel",
        "1-kings", "2-kings", "1-chronicles", "2-chronicles",
        "ezra", "nehemiah", "tobit", "judith", "esther",
        "1-maccabees", "2-maccabees", "job", "psalms", "proverbs",
        "ecclesiastes", "song-of-songs", "wisdom", "sirach", "isaiah",
        "jeremiah", "lamentations", "baruch", "ezekiel", "daniel",
        "hosea", "joel", "amos", "obadiah", "jonah", "micah",
        "nahum", "habakkuk", "zephaniah", "haggai", "zechariah", "malachi",
        "matthew", "mark", "luke", "john", "acts",
        "romans", "1-corinthians", "2-corinthians", "galatians", "ephesians",
        "philippians", "colossians", "1-thessalonians", "2-thessalonians",
        "1-timothy", "2-timothy", "titus", "philemon", "hebrews",
        "james", "1-peter", "2-peter", "1-john", "2-john",
        "3-john", "jude", "revelation"
    ]
    
    all_text = []
    
    print("Downloading NABRE from USCCB...")
    
    for book in books:
        url = f"{base_url}/{book}"
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Get book title
                title = soup.find('h1')
                title_text = title.get_text(strip=True) if title else book.upper()
                
                # Get verse text
                verses = soup.find_all(['p', 'span'], class_=lambda x: x and 'verse' in x.lower())
                
                if not verses:
                    # Try getting all paragraph text
                    content = soup.find('div', class_=lambda x: x and 'content' in str(x).lower())
                    if content:
                        text = content.get_text(separator='\n', strip=True)
                    else:
                        text = soup.get_text(separator='\n', strip=True)
                else:
                    text = '\n'.join([v.get_text(strip=True) for v in verses])
                
                if len(text) > 200:
                    all_text.append(f"\n\n{title_text.upper()}\n{text}")
                    print(f"✓ {book}")
                else:
                    print(f"✗ {book} — too short, skipping")
                    
        except Exception as e:
            print(f"✗ {book} — error: {e}")
        
        time.sleep(1)  # Be respectful to USCCB servers
    
    # Save to file
    full_text = "\n".join(all_text)
    with open("data/bible_nabre.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
    
    print(f"\nDone! Saved {len(all_text)} books to data/bible_nabre.txt")

if __name__ == "__main__":
    download_nabre()
