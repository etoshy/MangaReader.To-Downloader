import os
import json
import requests
from bs4 import BeautifulSoup

def baixar_imagem(img_url, img_path):
    for attempt in range(3):  # Tentar baixar a imagem até 3 vezes
        try:
            response = requests.get(img_url, stream=True, timeout=10)
            if response.status_code == 200:
                with open(img_path, "wb") as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
                return
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar {img_url} (tentativa {attempt+1}): {e}")
    print(f"Falha ao baixar {img_url} após 3 tentativas.")

def baixar_dados_manga(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Erro ao acessar a página")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Pegando os dados do wrapper
    wrapper = soup.find("div", id="wrapper")
    manga_id = wrapper["data-manga-id"]
    reading_id = wrapper["data-reading-id"]
    language = wrapper["data-lang-code"]
    reading_by = wrapper["data-reading-by"]  # Identifica se é capítulo ou volume
    
    # Pegando o nome e link do mangá
    manga_link_tag = soup.find("a", class_="hr-manga")
    manga_name = manga_link_tag.find("h2", class_="manga-name").text.strip()
    manga_link = "https://mangareader.to" + manga_link_tag["href"]
    
    # Pegando o número do capítulo ou volume pelo título da página
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
        print("Formato desconhecido")
        return
    
    # Criando a estrutura de diretórios
    base_path = os.path.join("mangas", manga_name, folder_name)
    os.makedirs(base_path, exist_ok=True)
    
    # Criando e salvando o JSON antes de baixar as imagens
    dados = {
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
        json.dump(dados, f, indent=4, ensure_ascii=False)
    
    print(f"Dados salvos em {json_path}")
    
    # Baixando links das imagens
    image_response = requests.get(image_api_url)
    
    if image_response.status_code == 200:
        image_soup = BeautifulSoup(image_response.json()["html"], 'html.parser')
        image_tags = image_soup.find_all("div", class_="iv-card")
        
        for idx, img_tag in enumerate(image_tags, start=1):
            img_url = img_tag["data-url"]
            dados["image_links"].append({f"imagem {idx}": img_url})
            
            # Baixando e salvando a imagem
            img_path = os.path.join(base_path, f"{idx}.jpg")
            baixar_imagem(img_url, img_path)
    
    # Atualizando o JSON com os links de imagens
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    
    print(f"Download concluído para {manga_name} {folder_name}")

# Pedindo os links ao usuário
urls = input("Digite os links dos capítulos ou volumes separados por vírgula: ").split(",")
urls = [url.strip() for url in urls]

for url in urls:
    baixar_dados_manga(url)
