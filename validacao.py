class ValidadorCliente:
    def validar(self, cliente):
        vazios = []

        if cliente.nome == "":
            vazios.append("Nome")
        if cliente.telefone == "":
            vazios.append("Telefone")
        if cliente.email == "":
            vazios.append("E-mail")
        if cliente.endereco == "":
            vazios.append("Endereço")

        if vazios:
            return f"Preencha o(s) campo(s): {', '.join(vazios)}"

        # RF02: telefone somente com números.
        if not cliente.telefone.isdigit():
            return "Telefone inválido: use somente números."

        # RF03: e-mail com usuário, @ e ponto no domínio.
        if not self.email_parece_valido(cliente.email):
            return "E-mail inválido: use o formato nome@dominio.com"

        return None

    def email_parece_valido(self, email):
        if "@" not in email:
            return False

        usuario, _, dominio = email.partition("@")

        if usuario == "" or "." not in dominio:
            return False

        return True
