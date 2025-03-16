# MangaReader.to Downloader ![Views Counter](https://views-counter.vercel.app/badge?pageId=https%3A%2F%2Fgithub%2Ecom%2Fetoshy%2FMangaReader%2ETo-Downloader&leftColor=ffffff&rightColor=000000&type=total&label=Viewers&style=none)

This is a Python script to download manga images from the site [MangaReader.to](https://mangareader.to). The script extracts manga information such as name, ID, reading type (chapter or volume), language, and downloads the chapter/volume images, saving everything in an organized directory structure.

---

## Requirements

Before running the script, make sure you have Python installed along with the following packages:

- `requests`
- `beautifulsoup4`

If you haven’t installed them yet, run the following command:

```bash
pip install requests beautifulsoup4
```

---

## How to Run

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/etoshy/mangareader.to-downloader.git
   cd mangareader.to-downloader
   ```

2. **Run the script**
   ```bash
   python manga_downloader.py
   ```

3. **Enter the links**
   When prompted, enter the chapter or volume links separated by commas.

   Example input:
   ```
   https://mangareader.to/read/one-piece-100, https://mangareader.to/read/naruto-45
   ```

4. **The script will download the data and images**
   - The manga information will be saved in a `info.json` file
   - Images will be downloaded and organized inside `mangas/MangaName/Chapter_X` or `Volume_X` folders

---

## Directory Structure

After running the script, the file structure will look like this:

```
/mangas/
   ├── One Piece/
   │   ├── Chapter 100/
   │   │   ├── info.json
   │   │   ├── 1.jpg
   │   │   ├── 2.jpg
   │   │   ├── ...
   │
   ├── Naruto/
       ├── Volume 45/
       │   ├── info.json
       │   ├── 1.jpg
       │   ├── 2.jpg
       │   ├── ...
```

---

## Possible Errors and Solutions

1. **Error accessing the page**
   - Check if the link is correct
   - The website may be down or have changed its HTML structure

2. **Error downloading images**
   - Make sure the image URLs are correct
   - Check your internet connection
   - It may be necessary to adjust the part of the code that retrieves the image links

---

### Author
Created by [etoshy](https://github.com/etoshy/)

