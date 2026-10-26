"""Gera um ZIP de distribuição da TechBairro sem banco ou arquivos temporários."""
from pathlib import Path
import zipfile

RAIZ = Path(__file__).resolve().parent.parent
ARQUIVO_VERSAO = RAIZ / "techbairro.py"
DESTINO_DIR = RAIZ / "dist"


def obter_versao():
    """Lê a constante VERSAO do arquivo principal sem importar a interface Tkinter."""
    for linha in ARQUIVO_VERSAO.read_text(encoding="utf-8").splitlines():
        if linha.strip().startswith("VERSAO") and "=" in linha:
            return linha.split("=", 1)[1].strip().strip("'\"")
    raise RuntimeError("A constante VERSAO não foi encontrada em techbairro.py.")


def gerar_pacote():
    versao = obter_versao()
    DESTINO_DIR.mkdir(exist_ok=True)
    destino = DESTINO_DIR / f"TechBairro-v{versao}.zip"

    ignorar_partes = {".git", "__pycache__", "dist", "build", ".venv", "venv", "env"}
    ignorar_nomes = {"techbairro.db", "resultado_testes.txt"}
    ignorar_sufixos = {".pyc", ".pyo", ".zip"}

    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as pacote:
        for arquivo in sorted(RAIZ.rglob("*")):
            if not arquivo.is_file() or arquivo == destino:
                continue
            relativo = arquivo.relative_to(RAIZ)
            if any(parte in ignorar_partes for parte in relativo.parts):
                continue
            if arquivo.name in ignorar_nomes or arquivo.suffix in ignorar_sufixos:
                continue
            pacote.write(arquivo, Path(f"TechBairro-v{versao}") / relativo)

    print(f"Pacote criado: {destino}")


if __name__ == "__main__":
    gerar_pacote()
