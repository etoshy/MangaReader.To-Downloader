import os
import json
import requests
from bs4 import BeautifulSoup

def download_image(img_url, img_path):
    for attempt in range(3):  # Try downloading the image up to 3 times
        try:
            response = requests.get(img_url, stream=True, timeout=10)
            if response.status_code == 200:
                with open(img_path, "wb") as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
                return
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {img_url} (attempt {attempt+1}): {e}")
    print(f"Failed to download {img_url} after 3 attempts.")

def download_manga_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Error accessing the page")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Getting data from the wrapper
    wrapper = soup.find("div", id="wrapper")
    manga_id = wrapper["data-manga-id"]
    reading_id = wrapper["data-reading-id"]
    language = wrapper["data-lang-code"]
    reading_by = wrapper["data-reading-by"]  # Identifies whether it's a chapter or volume
    
    # Getting manga name and link
    manga_link_tag = soup.find("a", class_="hr-manga")
    manga_name = manga_link_tag.find("h2", class_="manga-name").text.strip()
    manga_link = "https://mangareader.to" + manga_link_tag["href"]
    
    # Getting the chapter or volume number from the page title
    title = soup.find("title").text
    
    if reading_by == "chap":
        number = title.split("Chapter ")[1].split(" ")[0]
        folder_name = f"Chapter {number}"
        image_api_url = f"https://mangareader.to/ajax/image/list/chap/{reading_id}?mode=vertical&quality=high&hozPageSize=1"
    elif reading_by == "vol":
        number = title.split("Volume ")[1].split(" ")[0]
        folder_name = f"Volume {number}"
        image_api_url = f"https://mangareader.to/ajax/image/list/vol/{reading_id}?mode=vertical&quality=high&hozPageSize=1"
    else:
        print("Unknown format")
        return
    
    # Creating directory structure
    base_path = os.path.join("mangas", manga_name, folder_name)
    os.makedirs(base_path, exist_ok=True)
    
    # Creating and saving JSON before downloading images
    data = {
        "manga_name": manga_name,
        "manga_id": manga_id,
        "manga_link": manga_link,
        "reading_id": reading_id,
        "reading_type": reading_by,
        "number": number,
        "language": language,
        "url": url,
        "image_links": []
    }
    
    json_path = os.path.join(base_path, "info.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Data saved in {json_path}")
    
    # Downloading image links
    image_response = requests.get(image_api_url)
    
    if image_response.status_code == 200:
        image_soup = BeautifulSoup(image_response.json()["html"], 'html.parser')
        image_tags = image_soup.find_all("div", class_="iv-card")
        
        for idx, img_tag in enumerate(image_tags, start=1):
            img_url = img_tag["data-url"]
            data["image_links"].append({f"image {idx}": img_url})
            
            # Downloading and saving the image
            img_path = os.path.join(base_path, f"{idx}.jpg")
            download_image(img_url, img_path)
    
    # Updating JSON with image links
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Download completed for {manga_name} {folder_name}")

# Asking the user for links
urls = input("Enter the chapter or volume links separated by commas: ").split(",")
urls = [url.strip() for url in urls]

for url in urls:
    download_manga_data(url)
