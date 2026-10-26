# Scripts

`gerar_pacote.py` cria um ZIP de distribuição a partir dos arquivos do projeto.
Ele exclui o banco de dados, cache do Python, pastas de ambiente virtual e arquivos ZIP
gerados para evitar incluir dados pessoais ou arquivos temporários.
Execute na pasta do projeto:

```bash
python scripts/gerar_pacote.py
```

O ZIP será criado dentro de `dist/`, pasta ignorada pelo Git.
