import tkinter as tk  # Isso serve pra fazer a janela que aparece na tela
from tkinter import messagebox  # Isso serve pra mostrar janelinhas de aviso
import requests  # Serve pra pegar perguntas da internet
import random  # Serve pra embaralhar as respostas
import html  # Serve pra arrumar uns textos que vêm com códigos estranhos

class QuizGame:
    def __init__(self, root):
        self.root = root  # Guarda a janela que a gente vai usar
        self.root.title("Mini Quiz")  # Dá um nome pra janela
        # Aqui a gente deixa a janela do tamanho da tela inteira, pra ocupar tudo
        raiz.attributes("-fullscreen", True)
        self.root.configure(bg="#2c3e50")  # Muda a cor do fundo pra azul escuro

        self.pontuacao = 0  # Começa com zero pontos, que a pessoa vai ganhar se acertar
        self.indice_pergunta = 0  # Começa na primeira pergunta (posição zero)
        self.perguntas = []  # Aqui vai ficar guardado todas as perguntas que a gente pega

        # Essa parte mostra o texto da pergunta na tela, com letras grandes e brancas
        self.label_pergunta = tk.Label(
            root,
            text="Carregando perguntas...",  # Enquanto pega as perguntas, mostra isso
            wraplength=650,  # Se a frase for muito grande, ela quebra a linha aqui
            font=("Segoe UI", 18, "bold"),  # Tipo e tamanho da letra
            fg="white",  # Cor da letra, branco
            bg="#2c3e50"  # Cor do fundo, azul escuro
        )
        self.label_pergunta.pack(pady=40)  # Coloca um espacinho em cima e embaixo da pergunta

        # Agora a gente cria 4 botões, um pra cada opção de resposta
        self.botoes = []
        for i in range(4):
            btn = tk.Button(
                root,
                text="",  # Por enquanto eles estão vazios, depois vamos colocar as respostas
                width=40,  # Tamanho do botão
                height=2,  # Altura do botão
                font=("Segoe UI", 14),  # Tipo e tamanho da letra no botão
                bg="#34495e",  # Cor de fundo do botão (cinza azulado)
                fg="white",  # Cor da letra do botão (branco)
                activebackground="#2980b9",  # Cor do botão quando a pessoa clica nele
                activeforeground="white",  # Cor da letra quando clica
                relief="raised",  # Dá um relevo pro botão parecer apertável
                bd=4,  # Espessura da borda do botão
                command=lambda i=i: self.verificar_resposta(i)  # Quando clicar chama essa função com o número do botão
            )
            btn.pack(pady=10)  # Coloca um espacinho em cima e embaixo de cada botão
            self.botoes.append(btn)  # Guarda o botão numa lista pra usar depois

        # Aqui a gente chama a função que pega as perguntas da internet
        self.carregar_perguntas()

    def carregar_perguntas(self):
        url = "https://opentdb.com/api.php?amount=5&type=multiple"  # Esse é o endereço onde as perguntas estão
        try:
            resposta = requests.get(url)  # Pega as perguntas lá da internet
            dados = resposta.json()  # Transforma as perguntas num jeito que o Python entende
            self.perguntas = dados["results"]  # Pega só as perguntas da resposta
            self.mostrar_pergunta()  # Começa a mostrar a primeira pergunta na tela
        except Exception as e:
            # Se deu algum problema pra pegar as perguntas, mostra um aviso na tela
            tk.messagebox.showerror("Erro", f"Falha ao carregar perguntas: {e}")

    def mostrar_pergunta(self):
        # Se já mostramos todas as perguntas, mostramos a pontuação final e fechamos o jogo
        if self.indice_pergunta >= len(self.perguntas):
            tk.messagebox.showinfo(
                "Fim do Quiz",  # Título da janelinha
                f"Você terminou o quiz!\nSua pontuação: {self.pontuacao} / {len(self.perguntas)}"  # Mensagem mostrando a pontuação
            )
            self.root.quit()  # Fecha o programa
            return  # Para o resto da função

        # Aqui pega a pergunta atual pra mostrar
        p = self.perguntas[self.indice_pergunta]
        # Algumas perguntas vêm com códigos estranhos, aqui a gente arruma pra aparecer certinho
        texto_pergunta = html.unescape(p["question"])
        self.resposta_correta = html.unescape(p["correct_answer"])
        respostas_erradas = [html.unescape(r) for r in p["incorrect_answers"]]

        # Junta as respostas erradas com a certa e embaralha a ordem delas
        opcoes = respostas_erradas + [self.resposta_correta]
        random.shuffle(opcoes)

        # Muda o texto da pergunta na tela
        self.label_pergunta.config(text=f"P{self.indice_pergunta + 1}: {texto_pergunta}")

        # Muda os botões pra mostrar as respostas que a gente embaralhou, deixa eles ativados e com a cor normal
        for i, btn in enumerate(self.botoes):
            btn.config(text=opcoes[i], state=tk.NORMAL, bg="#34495e", fg="white")

    def verificar_resposta(self, indice):
        # Quando a pessoa clicar num botão, pega o texto que está nele
        selecionada = self.botoes[indice].cget("text")

        # Desliga todos os botões pra pessoa não clicar várias vezes enquanto o programa pensa
        for btn in self.botoes:
            btn.config(state=tk.DISABLED)

        # Se a resposta que a pessoa clicou for igual a resposta certa
        if selecionada == self.resposta_correta:
            self.pontuacao += 1  # Soma um ponto pra pessoa
            self.botoes[indice].config(bg="#2ecc71")  # Pinta o botão de verde
        else:
            self.botoes[indice].config(bg="#e74c3c")  # Se errou pinta de vermelho
            # Também pinta o botão com a resposta certa de verde pra mostrar qual era
            for btn in self.botoes:
                if btn.cget("text") == self.resposta_correta:
                    btn.config(bg="#2ecc71")

        # Espera 1,5 segundos pra mostrar as cores e só depois muda pra próxima pergunta
        self.indice_pergunta += 1
        self.root.after(1500, self.mostrar_pergunta)

if __name__ == "__main__":
    raiz = tk.Tk()  # Cria a janela que aparece
    jogo = QuizGame(raiz)  # Cria o quiz usando essa janela
    raiz.mainloop()  # Fica esperando o usuário clicar e interagir com a janela
