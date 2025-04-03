import pdfplumber
import pandas as pd
import zipfile
import os

downloads_dir = "downloads"
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

pdf_path = "D:\\Teste-de-nivelamento\\teste-transformacao-de-dados\\arquivo-pdf\\Anexo_I.pdf"
csv_path = "downloads/Rol_Procedimentos.csv"
zip_path = "downloads/Teste_leonardo_jarussi.zip"

substituicoes = {
    "OD": "Procedimentos Odontológicos",
    "AMB": "Procedimentos Ambulatoriais"
}
dados = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_table()
        if tables:
            for row in tables:
                dados.append(row)

df = pd.DataFrame(dados)
df = df.dropna().reset_index(drop=True)
df.replace(substituicoes, inplace=True)
df.to_csv(csv_path, index=False, sep=';')

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_path, os.path.basename(csv_path))

print(f"Transformação concluída! Arquivo salvo em: {zip_path}")
