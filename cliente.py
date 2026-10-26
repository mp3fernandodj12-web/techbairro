class Cliente:
    def __init__(self, nome, telefone, email, endereco, id=None):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.endereco = endereco

    def resumo(self):
        return f"{self.nome} | {self.telefone} | {self.email} | {self.endereco}"

    def iniciais(self):
        partes = self.nome.split()
        return "".join(parte[0].upper() for parte in partes if parte)
