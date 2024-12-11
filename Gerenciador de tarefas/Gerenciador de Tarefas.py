import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

# Nome do arquivo para salvar as tarefas
ARQUIVO_TAREFAS = "tarefas.json"

# === Funções Auxiliares ===

def carregar_tarefas():
    """Carrega tarefas do arquivo JSON."""
    if os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, "r") as arquivo:
            return json.load(arquivo)
    return []

def salvar_tarefas(tarefas):
    """Salva tarefas no arquivo JSON."""
    with open(ARQUIVO_TAREFAS, "w") as arquivo:
        json.dump(tarefas, arquivo, indent=4)


# === Funções para Tkinter ===

def atualizar_lista():
    """Atualiza a lista de tarefas na interface."""
    listbox_tarefas.delete(0, tk.END)
    for tarefa in tarefas:
        status = "✔️" if tarefa["concluida"] else "❌"
        prazo = tarefa["prazo"] if tarefa["prazo"] else "Sem prazo"
        listbox_tarefas.insert(tk.END, f"{status} {tarefa['descricao']} (Prazo: {prazo})")

def adicionar_tarefa_gui():
    """Adiciona uma nova tarefa via interface gráfica."""
    descricao = simpledialog.askstring("Nova Tarefa", "Digite a descrição da tarefa:")
    if descricao:
        prazo = simpledialog.askstring("Prazo", "Digite o prazo (opcional, formato AAAA-MM-DD):")
        tarefas.append({"descricao": descricao, "prazo": prazo, "concluida": False})
        atualizar_lista()
        salvar_tarefas(tarefas)
        messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")

def concluir_tarefa_gui():
    """Marca a tarefa selecionada como concluída."""
    try:
        indice = listbox_tarefas.curselection()[0]
        tarefas[indice]["concluida"] = True
        atualizar_lista()
        salvar_tarefas(tarefas)
        messagebox.showinfo("Sucesso", "Tarefa concluída!")
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para concluir.")

def remover_tarefa_gui():
    """Remove a tarefa selecionada."""
    try:
        indice = listbox_tarefas.curselection()[0]
        del tarefas[indice]
        atualizar_lista()
        salvar_tarefas(tarefas)
        messagebox.showinfo("Sucesso", "Tarefa removida!")
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para remover.")

def buscar_tarefas_gui():
    """Busca tarefas pela descrição."""
    termo = simpledialog.askstring("Buscar Tarefa", "Digite um termo para buscar:")
    if termo:
        resultados = [tarefa for tarefa in tarefas if termo.lower() in tarefa["descricao"].lower()]
        if resultados:
            resultado_texto = "\n".join(
                [f"{'✔️' if t['concluida'] else '❌'} {t['descricao']} (Prazo: {t['prazo'] or 'Sem prazo'})" for t in resultados]
            )
            messagebox.showinfo("Resultados da Busca", resultado_texto)
        else:
            messagebox.showinfo("Resultados da Busca", "Nenhuma tarefa encontrada com o termo fornecido.")

def ordenar_tarefas_gui():
    """Ordena as tarefas por prazo."""
    def obter_prazo(tarefa):
        if tarefa["prazo"]:
            return datetime.strptime(tarefa["prazo"], "%Y-%m-%d")
        return datetime.max
    tarefas.sort(key=obter_prazo)
    atualizar_lista()
    salvar_tarefas(tarefas)
    messagebox.showinfo("Sucesso", "Tarefas ordenadas por prazo!")

# === Interface Gráfica ===

# Inicializa o Tkinter
root = tk.Tk()
root.title("Gerenciador de Tarefas")

# Carregar as tarefas do arquivo
tarefas = carregar_tarefas()

# Frame principal
frame = tk.Frame(root)
frame.pack(pady=10)

# Listbox para exibir as tarefas
listbox_tarefas = tk.Listbox(frame, width=50, height=15)
listbox_tarefas.pack(side=tk.LEFT, padx=5)

# Scrollbar para o Listbox
scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox_tarefas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox_tarefas.config(yscrollcommand=scrollbar.set)

# Botões
botao_adicionar = tk.Button(root, text="Adicionar Tarefa", command=adicionar_tarefa_gui)
botao_adicionar.pack(fill=tk.X, padx=10, pady=5)

botao_concluir = tk.Button(root, text="Concluir Tarefa", command=concluir_tarefa_gui)
botao_concluir.pack(fill=tk.X, padx=10, pady=5)

botao_remover = tk.Button(root, text="Remover Tarefa", command=remover_tarefa_gui)
botao_remover.pack(fill=tk.X, padx=10, pady=5)

botao_buscar = tk.Button(root, text="Buscar Tarefa", command=buscar_tarefas_gui)
botao_buscar.pack(fill=tk.X, padx=10, pady=5)

botao_ordenar = tk.Button(root, text="Ordenar por Prazo", command=ordenar_tarefas_gui)
botao_ordenar.pack(fill=tk.X, padx=10, pady=5)

botao_sair = tk.Button(root, text="Sair", command=root.quit)
botao_sair.pack(fill=tk.X, padx=10, pady=5)

# Atualiza a lista na interface
atualizar_lista()

# Inicia o loop principal do Tkinter
root.mainloop()        

# === Funcionalidades ===

def adicionar_tarefa(tarefas):
    """Adiciona uma nova tarefa à lista."""
    descricao = input("Digite a descrição da tarefa: ")
    prazo = input("Digite o prazo da tarefa (opcional, formato AAAA-MM-DD): ")
    tarefas.append({"descricao": descricao, "prazo": prazo, "concluida": False})
    print("Tarefa adicionada com sucesso!")

def listar_tarefas(tarefas):
    """Lista todas as tarefas."""
    if not tarefas:
        print("Nenhuma tarefa encontrada.")
        return

    for i, tarefa in enumerate(tarefas):
        status = "✔️" if tarefa["concluida"] else "❌"
        prazo = tarefa["prazo"] if tarefa["prazo"] else "Sem prazo"
        print(f"{i + 1}. {status} {tarefa['descricao']} (Prazo: {prazo})")

def concluir_tarefa(tarefas):
    """Marca uma tarefa como concluída."""
    listar_tarefas(tarefas)
    try:
        indice = int(input("Digite o número da tarefa que deseja concluir: ")) - 1
        if 0 <= indice < len(tarefas):
            tarefas[indice]["concluida"] = True
            print("Tarefa marcada como concluída!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")

def remover_tarefa(tarefas):
    """Remove uma tarefa da lista."""
    listar_tarefas(tarefas)
    try:
        indice = int(input("Digite o número da tarefa que deseja remover: ")) - 1
        if 0 <= indice < len(tarefas):
            tarefas.pop(indice)
            print("Tarefa removida com sucesso!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")

def buscar_tarefas(tarefas):
    """Busca tarefas pela descrição."""
    termo = input("Digite um termo para buscar na descrição das tarefas: ").lower()
    resultados = [tarefa for tarefa in tarefas if termo in tarefa["descricao"].lower()]
    
    if resultados:
        print("\nTarefas encontradas:")
        for i, tarefa in enumerate(resultados):
            status = "✔️" if tarefa["concluida"] else "❌"
            prazo = tarefa["prazo"] if tarefa["prazo"] else "Sem prazo"
            print(f"{i + 1}. {status} {tarefa['descricao']} (Prazo: {prazo})")
    else:
        print("Nenhuma tarefa encontrada com o termo fornecido.")

def ordenar_tarefas_por_prazo(tarefas):
    """Ordena tarefas por prazo."""
    def obter_prazo(tarefa):
        if tarefa["prazo"]:
            return datetime.strptime(tarefa["prazo"], "%Y-%m-%d")
        return datetime.max  # Coloca tarefas sem prazo no final
    tarefas.sort(key=obter_prazo)
    print("Tarefas ordenadas por prazo!")

# === Função Principal ===

def main():
    """Executa o programa principal."""
    tarefas = carregar_tarefas()

    while True:
        print("\n=== Gerenciador de Tarefas ===")
        print("1. Adicionar tarefa")
        print("2. Listar tarefas")
        print("3. Concluir tarefa")
        print("4. Remover tarefa")
        print("5. Buscar tarefas")
        print("6. Ordenar tarefas por prazo")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_tarefa(tarefas)
        elif opcao == "2":
            listar_tarefas(tarefas)
        elif opcao == "3":
            concluir_tarefa(tarefas)
        elif opcao == "4":
            remover_tarefa(tarefas)
        elif opcao == "5":
            buscar_tarefas(tarefas)
        elif opcao == "6":
            ordenar_tarefas_por_prazo(tarefas)
        elif opcao == "7":
            salvar_tarefas(tarefas)
            print("Saindo... Tarefas salvas!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# === Executar o Programa ===

if __name__ == "__main__":
    main()

