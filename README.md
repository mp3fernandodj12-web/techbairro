# TechBairro v3.3.2

Aplicação desktop em Python/Tkinter para cadastro, consulta, edição e exclusão de clientes, com persistência em SQLite.

## Arquivos principais
- `techbairro.py`: interface Tkinter e fluxo da aplicação.
- `cliente.py`: classe que representa um cliente.
- `banco.py`: operações com o banco SQLite.
- `validacao.py`: regras de validação dos dados.
- `testar_validacao.py`: testes das regras sem abrir a interface.
- `CHANGELOG.md`: histórico de versões.
- `COMO_EXECUTAR.txt`: instruções de execução.
- `.gitignore`: arquivos que não devem entrar no histórico do Git.
- `scripts/gerar_pacote.py`: cria um pacote ZIP sem banco de dados, cache ou arquivos do Git.
- `docs/`: documentação complementar.

## Executar
Abra o terminal nesta pasta e rode:

```bash
python testar_validacao.py
python techbairro.py
```

O banco `techbairro.db` é criado automaticamente ao iniciar o programa. Ele é ignorado pelo Git e não acompanha o pacote de entrega, pois pode conter dados pessoais.

## Git
Configure sua identidade local no repositório, crie commits pequenos e consulte o histórico com:

```bash
git log --oneline
```
