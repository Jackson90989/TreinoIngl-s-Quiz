import tkinter as tk
from tkinter import messagebox
import requests
import random
import html

class QuizGame:
    def __init__(self, root):
        # Configura a janela principal
        self.root = root
        self.root.title("Mini Quiz")
        self.root.geometry("700x450")
        self.root.configure(bg="#2c3e50")  # Fundo escuro

        # Variáveis para controle do jogo
        self.pontuacao = 0
        self.indice_pergunta = 0
        self.perguntas = []

        # Label para mostrar a pergunta
        self.label_pergunta = tk.Label(
            root,
            text="Carregando perguntas...",
            wraplength=650,
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        self.label_pergunta.pack(pady=40)

        # Botões para as opções de respostas
        self.botoes = []
        for i in range(4):
            btn = tk.Button(
                root,
                text="",
                width=40,
                height=2,
                font=("Segoe UI", 14),
                bg="#34495e",
                fg="white",
                activebackground="#2980b9",
                activeforeground="white",
                relief="raised",
                bd=4,
                command=lambda i=i: self.verificar_resposta(i)
            )
            btn.pack(pady=10)
            self.botoes.append(btn)

        # Carrega as perguntas da API
        self.carregar_perguntas()

    def carregar_perguntas(self):
        """Busca as perguntas da API pública e inicia o quiz."""
        url = "https://opentdb.com/api.php?amount=5&type=multiple"
        try:
            resposta = requests.get(url)
            dados = resposta.json()
            self.perguntas = dados["results"]
            self.mostrar_pergunta()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar perguntas: {e}")

    def mostrar_pergunta(self):
        """Exibe a pergunta e opções na tela."""
        if self.indice_pergunta >= len(self.perguntas):
            messagebox.showinfo(
                "Fim do Quiz",
                f"Você terminou o quiz!\nSua pontuação: {self.pontuacao} / {len(self.perguntas)}"
            )
            self.root.quit()
            return

        p = self.perguntas[self.indice_pergunta]
        texto_pergunta = html.unescape(p["question"])
        self.resposta_correta = html.unescape(p["correct_answer"])
        respostas_erradas = [html.unescape(r) for r in p["incorrect_answers"]]

        opcoes = respostas_erradas + [self.resposta_correta]
        random.shuffle(opcoes)

        self.label_pergunta.config(text=f"P{self.indice_pergunta + 1}: {texto_pergunta}")

        for i, btn in enumerate(self.botoes):
            btn.config(text=opcoes[i], state=tk.NORMAL)

    def verificar_resposta(self, indice):
        """Verifica se a resposta está correta e avança para próxima pergunta."""
        selecionada = self.botoes[indice].cget("text")
        if selecionada == self.resposta_correta:
            self.pontuacao += 1
            messagebox.showinfo("Correto!", "Você acertou!")
        else:
            messagebox.showinfo("Errado!", f"Resposta correta: {self.resposta_correta}")

        self.indice_pergunta += 1
        self.mostrar_pergunta()


if __name__ == "__main__":
    raiz = tk.Tk()
    jogo = QuizGame(raiz)
    raiz.mainloop()
