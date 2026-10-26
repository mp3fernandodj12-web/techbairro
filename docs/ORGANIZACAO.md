# Organização do projeto TechBairro

- `techbairro.py`: interface e interação com o usuário.
- `cliente.py`: representação dos dados de cada cliente.
- `validacao.py`: regras de validação, sem dependência da interface ou do banco.
- `banco.py`: acesso e operações no SQLite.
- `testar_validacao.py`: testes automatizados da validação.
- `scripts/`: ferramentas auxiliares, como a geração de um ZIP de distribuição.

O banco `techbairro.db`, caches e pacotes gerados ficam fora do histórico do Git.
Não coloque dados reais de clientes em commits, capturas de tela ou arquivos de entrega.
