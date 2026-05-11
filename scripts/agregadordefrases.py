import pathlib
import re
import unicodedata

PASTA_BASE = pathlib.Path(".")
OUTPUT_LIMPO = PASTA_BASE / "corpus_frases_alfabetico.txt"
OUTPUT_COM_FONTE = PASTA_BASE / "corpus_frases_alfabetico_com_fonte.txt"

EXTENSAO = "*.txt"

EXCLUIR = {
    OUTPUT_LIMPO.name,
    OUTPUT_COM_FONTE.name,
    "prompt_salazar.txt",
}

ABREVIATURAS = [
    "V. Ex.ª", "V. Exa.", "Ex.ª", "Exa.", "Ex.mo", "Ex.mos",
    "Sr.", "Sra.", "Dr.", "Dra.", "Prof.", "D.",
    "etc.", "ibid.", "cit.", "ob. cit.",
    "M.me", "Mme.", "n.º", "N.º", "S.",
]


def proteger_abreviaturas(texto):
    substituicoes = {}

    for i, abrev in enumerate(sorted(ABREVIATURAS, key=len, reverse=True)):
        chave = f"__ABREV_{i}__"
        substituicoes[chave] = abrev
        texto = texto.replace(abrev, chave)

    return texto, substituicoes


def restaurar_abreviaturas(texto, substituicoes):
    for chave, abrev in substituicoes.items():
        texto = texto.replace(chave, abrev)
    return texto


def normalizar_espacos(texto):
    texto = texto.replace("\ufeff", "")
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n+", " ", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def limpar_inicio_frase(frase):
    """
    Remove sinais gráficos iniciais que não pertencem à parte verbal da frase:
    travessões, hífens, aspas e espaços.
    """
    return frase.strip().lstrip("—–- «“”\"'").strip()


def primeira_letra_real(frase):
    frase = limpar_inicio_frase(frase)
    return frase[0] if frase else ""


def parece_frase_valida(frase):
    frase = limpar_inicio_frase(frase)

    if len(frase) < 12:
        return False

    if not re.search(r"[a-záàâãéêíóôõúç]", frase):
        return False

    letra = primeira_letra_real(frase)

    if not letra:
        return False

    return letra.isupper()


def dividir_em_frases(texto):
    texto = normalizar_espacos(texto)
    texto, substituicoes = proteger_abreviaturas(texto)

    # Divide depois de ponto, ponto e vírgula, interrogação ou exclamação
    # quando a seguir vem maiúscula, eventualmente precedida de travessão ou aspas.
    padrao = r"(?<=[\.;?!])\s+(?=(?:[—–-]\s*)?[«“\"']?[A-ZÁÀÂÃÉÊÍÓÔÕÚÜÇ])"

    partes = re.split(padrao, texto)

    frases = []

    for parte in partes:
        parte = restaurar_abreviaturas(parte.strip(), substituicoes)
        parte = limpar_inicio_frase(parte)

        if parece_frase_valida(parte):
            frases.append(parte)

    return frases


def chave_alfabetica(frase):
    frase = limpar_inicio_frase(frase)
    frase = frase.lower()
    frase = unicodedata.normalize("NFD", frase)
    frase = "".join(c for c in frase if unicodedata.category(c) != "Mn")
    return frase


def main():
    registos = []

    txts = sorted(PASTA_BASE.glob(EXTENSAO))

    for path in txts:
        if path.name in EXCLUIR:
            continue

        try:
            texto = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            texto = path.read_text(encoding="utf-8-sig")

        frases = dividir_em_frases(texto)

        for frase in frases:
            registos.append({
                "ficheiro": path.name,
                "frase": frase
            })

    registos.sort(key=lambda r: chave_alfabetica(r["frase"]))

    with open(OUTPUT_LIMPO, "w", encoding="utf-8") as f:
        for r in registos:
            f.write(r["frase"] + "\n")

    with open(OUTPUT_COM_FONTE, "w", encoding="utf-8") as f:
        for r in registos:
            f.write(f"{r['frase']} [{r['ficheiro']}]\n")

    print("Extração concluída.")
    print(f"Frases extraídas: {len(registos)}")
    print(f"Ficheiro limpo: {OUTPUT_LIMPO}")
    print(f"Ficheiro com fonte: {OUTPUT_COM_FONTE}")


if __name__ == "__main__":
    main()
