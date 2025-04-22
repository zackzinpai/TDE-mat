import itertools
import re
import tkinter as tk
from tkinter import messagebox, Toplevel, Text


def validar_expressao(expressao):
    padrao = r'^[pqr\s\(\)¬!∧&∨|→=>↔<=>]+$'
    return bool(re.match(padrao, expressao))


def substituir_operadores(expressao):
    expressao = expressao.replace("<=>", " == ")
    expressao = expressao.replace("=>", " <= ")
    expressao = expressao.replace("¬", "not ").replace("!", "not ")
    expressao = expressao.replace("∧", " and ").replace("&", " and ")
    expressao = expressao.replace("∨", " or ").replace("|", " or ")
    expressao = expressao.replace("→", " <= ")
    expressao = expressao.replace("↔", " == ")
    return expressao


def gerar_tabela(expressao):
    variaveis = sorted(set(re.findall(r'[pqr]', expressao)))
    expressao_python = substituir_operadores(expressao)
    resultados = []
    tabela = []
    for valores in sorted(itertools.product([False, True], repeat=len(variaveis)), reverse=True):
        contexto = dict(zip(variaveis, valores))
        resultado = eval(expressao_python, {}, contexto)
        resultados.append(resultado)
        linha = [int(v) for v in valores] + [int(resultado)]
        tabela.append(linha)
    return variaveis, tabela, resultados


def classificar_proposicao(resultados):
    if all(resultados):
        return "A proposição é uma TAUTOLOGIA."
    elif not any(resultados):
        return "A proposição é uma CONTRADIÇÃO."
    else:
        return "A proposição é uma CONTINGÊNCIA."


def mostrar_instrucoes():
    janela_instrucoes = Toplevel(root)
    janela_instrucoes.title("Instruções de Uso")
    janela_instrucoes.geometry("500x400")
    texto_instrucoes = """
    COMO USAR O GERADOR DE TABELAS-VERDADE

    1. DIGITE SUA PROPOSIÇÃO:
    • Use as variáveis: p, q, r
    • Operadores disponíveis:
      ¬ ou !   Negação
      ∧ ou &   Conjunção (E)
      ∨ ou |   Disjunção (OU)
      → ou =>  Condicional
      ↔ ou <=> Bicondicional

    2. EXEMPLOS VÁLIDOS:
    • p ∧ q
    • (p ∨ q) → r
    • ¬p ↔ (q ∧ r)

    3. RESULTADOS:
    • Tabela com todas combinações possíveis
    • Classificação como:
      - Tautologia (sempre verdadeira)
      - Contradição (sempre falsa)
      - Contingência (depende dos valores)
    """
    quadro_texto = Text(janela_instrucoes, wrap="word",
                        font=("Arial", 10), padx=10, pady=10)
    quadro_texto.insert("1.0", texto_instrucoes)
    quadro_texto.config(state="disabled")
    quadro_texto.pack(fill="both", expand=True)
    tk.Button(janela_instrucoes, text="Fechar",
              command=janela_instrucoes.destroy).pack(pady=10)


def exibir_tabela():
    expressao = entrada.get()
    if expressao.count('(') != expressao.count(')'):
        messagebox.showerror(
            "Erro", "Parênteses desbalanceados! Verifique sua expressão.")
        return
    if not validar_expressao(expressao):
        messagebox.showerror("Erro",
                             "Expressão inválida!\n\nOperadores permitidos:\n"
                             "¬ ou ! (Negação)\n"
                             "∧ ou & (E)\n"
                             "∨ ou | (OU)\n"
                             "→ ou => (Condicional)\n"
                             "↔ ou <=> (Bicondicional)\n\n"
                             "Use apenas as variáveis p, q, r")
        return
    variaveis, tabela, resultados = gerar_tabela(expressao)
    classificacao = classificar_proposicao(resultados)
    for widget in frame_tabela.winfo_children():
        widget.destroy()
    header = " | ".join(variaveis) + " | Resultado"
    tk.Label(frame_tabela, text=header, font=("Arial", 10, "bold")).pack()
    tk.Label(frame_tabela, text="-" * len(header)).pack()
    for linha in tabela:
        linha_str = " | ".join([str(val) for val in linha])
        tk.Label(frame_tabela, text=linha_str, font=("Arial", 10)).pack()
    label_resultado.config(text=classificacao)


root = tk.Tk()
root.title("Gerador de Tabelas-Verdade")
root.geometry("400x500")
tk.Label(root, text="Digite a proposição lógica:", font=("Arial", 12)).pack()
entrada = tk.Entry(root, width=50)
entrada.pack()
tk.Button(root, text="Gerar Tabela-Verdade", command=exibir_tabela).pack()
tk.Button(root, text="Instruções", command=mostrar_instrucoes).pack(pady=10)
frame_tabela = tk.Frame(root)
frame_tabela.pack()
label_resultado = tk.Label(root, text="", font=("Arial", 12, "bold"))
label_resultado.pack()
root.mainloop()
