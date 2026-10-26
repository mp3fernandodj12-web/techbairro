import os
import sqlite3
import tkinter as tk
from tkinter import messagebox

from cliente import Cliente
from banco import GerenciadorClientes
from validacao import ValidadorCliente

VERSAO = "3.3.2"

PASTA_DO_PROJETO = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(PASTA_DO_PROJETO, "techbairro.db")

print(f"Banco em uso: {CAMINHO_BANCO}")

gerenciador = GerenciadorClientes(CAMINHO_BANCO)
validador = ValidadorCliente()
id_em_edicao = None

janela = tk.Tk()
janela.title("TechBairro — Cadastro de Cliente")
janela.geometry("480x460")
janela.resizable(False, False)

# Cabeçalho
cabecalho = tk.Frame(janela, bg="#2c3e50")
cabecalho.pack(side="top", fill="x")
tk.Label(
    cabecalho, text="Cadastro de Cliente", fg="white", bg="#2c3e50",
    font=("Arial", 14, "bold"), pady=12
).pack()

# Formulário
form = tk.Frame(janela)
form.pack(pady=20)

campos = ["Nome", "Telefone", "E-mail", "Endereço"]
entradas = {}

for i, campo in enumerate(campos):
    tk.Label(form, text=f"{campo}:").grid(
        row=i, column=0, sticky="e", padx=5, pady=6
    )
    entrada = tk.Entry(form, width=30)
    entrada.grid(row=i, column=1, padx=5, pady=6)
    entradas[campo] = entrada

status = tk.Label(
    janela, text="Nenhum cliente cadastrado ainda", fg="gray",
    wraplength=440, justify="left"
)
status.pack(pady=(0, 5))

contador = tk.Label(janela, text=f"Clientes cadastrados: {gerenciador.total()}")
contador.pack()


def limpar_campos():
    global id_em_edicao
    for entrada in entradas.values():
        entrada.delete(0, tk.END)
    id_em_edicao = None


def salvar():
    global id_em_edicao

    valores = {
        campo: entradas[campo].get().strip()
        for campo in campos
    }

    cliente = Cliente(
        valores["Nome"],
        valores["Telefone"],
        valores["E-mail"],
        valores["Endereço"]
    )

    # As regras de negócio ficam centralizadas em validacao.py.
    erro = validador.validar(cliente)
    if erro is not None:
        status.config(text=erro, fg="red")
        return

    try:
        if id_em_edicao is None:
            gerenciador.adicionar(cliente)
            status.config(text=f"Cliente '{cliente.nome}' salvo com sucesso!", fg="green")
        else:
            gerenciador.atualizar(id_em_edicao, cliente)
            status.config(text=f"Cliente '{cliente.nome}' atualizado com sucesso!", fg="green")
    except sqlite3.Error as erro_banco:
        status.config(text=f"Erro ao salvar no banco: {erro_banco}", fg="red")
        return

    contador.config(text=f"Clientes cadastrados: {gerenciador.total()}")
    limpar_campos()


def cancelar():
    limpar_campos()
    status.config(text="Formulário limpo", fg="gray")


def abrir_consulta():
    consulta = tk.Toplevel(janela)
    consulta.title("Consulta de Clientes")
    consulta.geometry("500x380")
    consulta.resizable(False, False)

    area_lista = tk.Frame(consulta)
    area_lista.pack(padx=10, pady=10, fill="x")

    lista = tk.Listbox(area_lista, width=65, height=12)
    scrollbar = tk.Scrollbar(area_lista, command=lista.yview)
    lista.config(yscrollcommand=scrollbar.set)
    lista.pack(side="left")
    scrollbar.pack(side="right", fill="y")

    # Mantém os objetos correspondentes às linhas exibidas.
    clientes_exibidos = []

    def atualizar_lista():
        lista.delete(0, tk.END)
        clientes_exibidos.clear()
        try:
            clientes_exibidos.extend(gerenciador.listar())
        except sqlite3.Error as erro_banco:
            lista.insert(tk.END, f"Erro ao ler o banco: {erro_banco}")
            return

        if not clientes_exibidos:
            lista.insert(tk.END, "Nenhum cliente cadastrado")
            return

        for cliente in clientes_exibidos:
            lista.insert(tk.END, cliente.resumo())

    def cliente_selecionado():
        selecionado = lista.curselection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um cliente antes de continuar.")
            return None
        indice = selecionado[0]
        if indice >= len(clientes_exibidos):
            return None
        return clientes_exibidos[indice]

    def editar_cliente():
        global id_em_edicao
        cliente = cliente_selecionado()
        if cliente is None:
            return

        id_em_edicao = cliente.id
        dados = {
            "Nome": cliente.nome,
            "Telefone": cliente.telefone,
            "E-mail": cliente.email,
            "Endereço": cliente.endereco
        }
        for campo, valor in dados.items():
            entradas[campo].delete(0, tk.END)
            entradas[campo].insert(0, valor)

        status.config(text=f"Editando cliente: {cliente.nome}", fg="blue")
        consulta.destroy()

    def excluir_cliente():
        cliente = cliente_selecionado()
        if cliente is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Tem certeza que deseja excluir o cadastro de {cliente.nome}?\n\n"
            "Essa ação não pode ser desfeita."
        )
        if not confirmar:
            return

        try:
            gerenciador.remover(cliente.id)
        except sqlite3.Error as erro_banco:
            messagebox.showerror(
                "Erro no banco", f"Não foi possível excluir o cliente.\n{erro_banco}"
            )
            return

        atualizar_lista()
        contador.config(text=f"Clientes cadastrados: {gerenciador.total()}")
        status.config(text=f"Cliente '{cliente.nome}' excluído com sucesso!", fg="green")

    botoes_consulta = tk.Frame(consulta)
    botoes_consulta.pack(pady=10)

    tk.Button(
        botoes_consulta, text="Editar selecionado", width=18,
        command=editar_cliente
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        botoes_consulta, text="Excluir selecionado", width=18,
        command=excluir_cliente
    ).grid(row=0, column=1, padx=5)

    atualizar_lista()


botoes = tk.Frame(janela)
botoes.pack(pady=10)

tk.Button(botoes, text="Salvar", width=12, command=salvar).grid(row=0, column=0, padx=5)
tk.Button(botoes, text="Cancelar", width=12, command=cancelar).grid(row=0, column=1, padx=5)
tk.Button(botoes, text="Consultar", width=12, command=abrir_consulta).grid(row=0, column=2, padx=5)

# Versão visível na interface; o nome do arquivo permanece techbairro.py.
tk.Label(janela, text=f"v{VERSAO}", fg="gray").place(
    relx=0.97, rely=0.97, anchor="se"
)

janela.mainloop()
