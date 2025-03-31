import os
import zipfile
import pandas as pd
import pdfplumber

pdf_path = "../dados/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
csv_path = "../dados/rol_procedimentos.csv"
zip_path = "../dados/Teste_joao_vitor_lunardi_machado.zip"

tabelas = []

with pdfplumber.open(pdf_path) as pdf:
    for i in range(3, len(pdf.pages) + 1):
        page = pdf.pages[i - 1]
        table = page.extract_table()

        if table:
            tabelas.extend(table)

df = pd.DataFrame(tabelas)

df.columns = [ "Procedimento", "RN (Alteração)", "Vigência", "Seg. Odontológica", "Seg. Ambulatorial", "HCO", "HSO", "REF", "PAC", "DUT", "Subgrupo", "Grupo", "Capítulo" ]

df = df[df["Procedimento"] != "PROCEDIMENTO"]

df = df.applymap(lambda x: x.replace("\n", " ").strip() if isinstance(x, str) else x)

df.replace({"OD": "Seg. Odontológica", "AMB": "Seg. Ambulatorial"}, inplace=True)

df.to_csv(csv_path, index=False, encoding="utf-8-sig", sep=";")

print(f"Tabela salva em {csv_path}")

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_path, os.path.basename(csv_path))

print(f"Arquivo compactado em {zip_path}")
