import requests
from bs4 import BeautifulSoup
import os
import zipfile

URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

response = requests.get(URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

pdf_links = []
for link in soup.find_all("a", href=True):
    if link["href"].endswith(".pdf") and "Anexo_" in link["href"]:
        pdf_links.append(link["href"])

pdf_links = [l if l.startswith("http") else f"https://www.gov.br{l}" for l in pdf_links]

pdf_folder = "pdfs"
os.makedirs(pdf_folder, exist_ok=True)

pdf_files = []
for pdf_url in pdf_links:
    pdf_name = pdf_url.split("/")[-1]
    pdf_path = os.path.join(pdf_folder, pdf_name)

    print(f"Baixando {pdf_name}...")
    pdf_response = requests.get(pdf_url, timeout=10)
    pdf_response.raise_for_status()

    with open(pdf_path, "wb") as f:
        f.write(pdf_response.content)

    pdf_files.append(pdf_path)

print("Download completo.")

zip_path = "anexos.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for pdf in pdf_files:
        zipf.write(pdf, os.path.basename(pdf))

print(f"Arquivos compactados em {zip_path}")