from pathlib import Path

PASTA = Path(".")

ficheiros_txt = list(PASTA.rglob("*.txt"))

total_caracteres_com_espacos = 0
total_caracteres_sem_espacos = 0
total_palavras = 0
total_linhas = 0

for ficheiro in ficheiros_txt:
    texto = ficheiro.read_text(encoding="utf-8", errors="ignore")

    total_caracteres_com_espacos += len(texto)
    total_caracteres_sem_espacos += len(texto.replace(" ", ""))
    total_palavras += len(texto.split())
    total_linhas += texto.count("\n") + 1

print("Ficheiros TXT:", len(ficheiros_txt))
print("Linhas aproximadas:", total_linhas)
print("Caracteres com espaços:", total_caracteres_com_espacos)
print("Caracteres sem espaços:", total_caracteres_sem_espacos)
print("Palavras aproximadas:", total_palavras)
