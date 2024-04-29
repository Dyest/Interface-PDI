import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from PIL import Image, ImageTk
from tkinter import messagebox
import numpy as np
import cv2


 #abre uma janela dividindo sua interface em 4 frames distintos
def abrir_janela():
    global frame_superior_direito
    global frame_inferior_direito
    global frame_inferior_esquerdo
    global largura_frame
    global altura_frame
    global imagem_atual
    global transformacoes_selecionadas
    global caixa_texto


    janela = tk.Tk()
    janela.title("Conversor")
    janela.config(bg='#000000')
    janela.resizable(False, False) 
    imagem_atual = None
    
    largura_janela = janela.winfo_screenwidth() - 180
    altura_janela = janela.winfo_screenheight() - 220
    
    largura_frame = largura_janela // 2
    altura_frame = altura_janela // 2

    #frames divididos
    frame_superior_esquerdo = Frame(janela, width=largura_frame, height=altura_frame, bg="#e6fcd9")
    frame_superior_esquerdo.grid(row=0, column=0, sticky="nw", padx=(0, 1), pady=(0, 3))  

    frame_superior_direito = Frame(janela, width=largura_frame, height=altura_frame, bg="#e6fcd9")
    frame_superior_direito.grid(row=0, column=1, sticky="ne", padx=(1, 0))

    frame_inferior_esquerdo = Frame(janela, width=largura_frame, height=altura_frame, bg="#00FF00")
    frame_inferior_esquerdo.grid(row=1, column=0, sticky="sw")

    frame_inferior_direito = Frame(janela, width=largura_frame, height=altura_frame, bg="#e6fcd9")
    frame_inferior_direito.grid(row=1, column=1, sticky="se")

    #lista de transformaçoes
    transformacoes_selecionadas = []
    
    criar_lista_transformacoes(frame_inferior_esquerdo)

    #Chama os botoes no frame superior esquerdo
    botoes_pdi(frame_superior_esquerdo)
    janela.mainloop()

# Adicionar botões no frame superior esquerdo
def botoes_pdi(frame_superior_esquerdo):
    
    botao_dropdown = tk.Menubutton(frame_superior_esquerdo, text="Conversão de cores", bg='#f59b71', cursor="hand2", width=40, height=2, activebackground="#755858")
    botao_dropdown.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    botao_dropdown.menu = tk.Menu(botao_dropdown, tearoff=0)
    botao_dropdown["menu"] = botao_dropdown.menu

    botao_dropdown.menu.configure(activebackground="#755858", bd=0, borderwidth=0)

    botao_dropdown.menu.add_command(label="RGB -> CIE L*a*b*", command=Converter_cores(1))
    botao_dropdown.menu.add_command(label="RGB -> XYZ", command=Converter_cores(2))
    botao_dropdown.menu.add_command(label="RGB -> HSV", command=Converter_cores(3))
    botao_dropdown.menu.add_command(label="RGB -> Gray", command=Converter_cores(4))
    
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------#


    botao2 = tk.Button(frame_superior_esquerdo, text="Filtro Bilateral", bg='#f59b71', cursor="hand2", width=35, height=2, activebackground="#755858", command=aplicar_filtro)
    botao2.place(relx=0.5, rely=0.2, anchor=tk.CENTER)  # Coloca o botão no centro horizontal, 20% do topo

    botao3 = tk.Button(frame_superior_esquerdo, text="Detector de borda: Canny", bg='#f59b71', cursor="hand2", width=35, height=2, activebackground="#755858", command=detectar_bordas)
    botao3.place(relx=0.5, rely=0.3, anchor=tk.CENTER)  # Coloca o botão no centro horizontal, 30% do topo

    botao4 = tk.Button(frame_superior_esquerdo, text="Binarização: Threshold", bg='#f59b71', cursor="hand2", width=35, height=2, activebackground="#755858", command=aplicar_binarizacao)
    botao4.place(relx=0.5, rely=0.4, anchor=tk.CENTER)  # Coloca o botão no centro horizontal, 40% do topo

    botao5 = tk.Button(frame_superior_esquerdo, text="Morfologia Matemática: Dilatação", bg='#f59b71', cursor="hand2", width=35, height=2, activebackground="#755858", command=morfologia_matematica)
    botao5.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Coloca o botão no centro horizontal, 50% do topo

    botao6 = tk.Button(frame_superior_esquerdo, text="Alterar imagem", bg='#f59b71', cursor="hand2", width=35, height=2, activebackground="#755858", command=Add_imagem)
    botao6.place(relx=0.5, rely=0.8, anchor=tk.CENTER)  # Coloca o botão no centro horizontal, 80% do topo

    botao7 = tk.Button(frame_superior_esquerdo, text="Salvar imagem alterada", bg='#f59b71', cursor="hand2", width=35, height=2, activebackground="#755858", command=salvar_imagem)
    botao7.place(relx=0.5, rely=0.9, anchor=tk.CENTER)  # Coloca o botão no centro horizontal, 90% do topo


#redimensiona as imagens para caber corretamente dentro da area definida
def redimensionar_imagem(imagem_pil, frame, largura_frame, altura_frame):
    proporcao = min(largura_frame / imagem_pil.width, altura_frame / imagem_pil.height)
    nova_largura = int(imagem_pil.width * proporcao)
    nova_altura = int(imagem_pil.height * proporcao)
    imagem_redimensionada = imagem_pil.resize((nova_largura, nova_altura))

    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)

    label_imagem = Label(frame, image=imagem_tk)
    label_imagem.imagem_tk = imagem_tk
    x = (largura_frame - nova_largura) // 2
    y = (altura_frame - nova_altura) // 2
    label_imagem.place(x=x, y=y)

    return label_imagem

#abre uma nova imagem de um diretorio qualquer, depois as redimensiona
def Add_imagem():
    global label_imagem_anterior
    global imagem_cv
    global imagem_atual

    # Limpar os frames antes de abrir uma nova imagem
    for widget in frame_superior_direito.winfo_children():
        widget.destroy()
    for widget in frame_inferior_direito.winfo_children():
        widget.destroy()

    filename = filedialog.askopenfilename(title="Abrir Imagem", filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
    if filename:
        imagem_cv = cv2.imread(filename)
        imagem_cv = cv2.cvtColor(imagem_cv, cv2.COLOR_RGB2BGR)
        imagem_atual = imagem_cv
        imagem_pil = Image.fromarray(imagem_cv)

        label_imagem_original = redimensionar_imagem(imagem_pil, frame_superior_direito, largura_frame, altura_frame)
        label_imagem_convertida = redimensionar_imagem(imagem_pil, frame_inferior_direito, largura_frame, altura_frame)

        # Atualizar a referência da imagem anterior
        label_imagem_anterior = label_imagem_original


def salvar_imagem():
    global imagem_atual

    if imagem_atual is None:
        messagebox.showinfo("Erro", "Não há imagem para salvar.")
        return

    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Imagem PNG", "*.png"), ("Imagem JPEG", "*.jpg"), ("Todos os arquivos", "*.*")])
    if filename:
        try:
            cv2.imwrite(filename, cv2.cvtColor(imagem_atual, cv2.COLOR_BGR2RGB))
            messagebox.showinfo("Salvo", "Imagem salva com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar a imagem: {e}")

#Funçoes de converção
def Converter_cores(opcao):
    
    def Converter_CIELAB():
        global imagem_atual

        if imagem_atual is None:
            messagebox.showinfo("Erro", "Escolha uma imagem primeiro")
        else:
            imagem_atual = cv2.cvtColor(imagem_atual, cv2.COLOR_RGB2Lab)
            edit_pil = Image.fromarray(imagem_atual)
            redimensionar_imagem(edit_pil, frame_inferior_direito, largura_frame, altura_frame)
            marcar_transformacao("Conversão de cores: RGB -> CIE L*a*b*")
            

    def Converter_para_XYZ():
        global imagem_atual

        if imagem_atual is None:
            messagebox.showinfo("Erro", "Escolha uma imagem primeiro")
        else:
            imagem_atual = cv2.cvtColor(imagem_atual, cv2.COLOR_RGB2XYZ)
            edit_pil = Image.fromarray(imagem_atual)
            redimensionar_imagem(edit_pil, frame_inferior_direito, largura_frame, altura_frame)
            marcar_transformacao("Conversão de cores: RGB -> XYZ")


    def Converter_para_HSV():
        global imagem_atual

        if imagem_atual is None:
            messagebox.showinfo("Erro", "Escolha uma imagem primeiro")
        else:
            imagem_atual = cv2.cvtColor(imagem_atual, cv2.COLOR_RGB2HSV)
            edit_pil = Image.fromarray(imagem_atual)
            redimensionar_imagem(edit_pil, frame_inferior_direito, largura_frame, altura_frame)
            marcar_transformacao("Conversão de cores: RGB -> HSV")


    def Converter_para_GRAY():
        global imagem_atual

        if imagem_atual is None:
            messagebox.showinfo("Erro", "Escolha uma imagem primeiro")
        elif len(imagem_atual.shape) > 2 and imagem_atual.shape[2] > 1:
            # Converte a imagem para RGB para XYZ
            imagem_atual = cv2.cvtColor(imagem_atual, cv2.COLOR_RGB2GRAY)
            edit_pil = Image.fromarray(imagem_atual)
            redimensionar_imagem(edit_pil, frame_inferior_direito, largura_frame, altura_frame)
            marcar_transformacao("Conversão de cores: RGB -> Gray")
        else:
            messagebox.showinfo("Erro", "A imagem atual não pode ser convertida pois já está em escala de cinza.")

        

    
    if opcao == 1:
        return Converter_CIELAB
    elif opcao == 2:
        return Converter_para_XYZ
    elif opcao == 3:
        return Converter_para_HSV
    elif opcao == 4:
        return Converter_para_GRAY
    else:
        return None


def aplicar_filtro():
    global imagem_atual
    if imagem_atual is None:
        messagebox.showinfo("Erro", "Escolha uma imagem primeiro")
    else:
        imagem_suavizada = cv2.bilateralFilter(imagem_atual, 17, 75, 75)
        imagem_atual = imagem_suavizada  # Atualiza a imagem atual para a imagem filtrada
        edit_pil = Image.fromarray(imagem_suavizada)
        redimensionar_imagem(edit_pil, frame_inferior_direito, largura_frame, altura_frame)
        marcar_transformacao("Filtro Bilateral")
        

def detectar_bordas():
    global imagem_atual

    if imagem_atual is None:
        messagebox.showinfo("Erro", "Escolha uma imagem primeiro")
    else:
        # Converte a imagem para escala de cinza, se necessário
        if len(imagem_atual.shape) > 2 and imagem_atual.shape[2] > 1:
            imagem_cinza = cv2.cvtColor(imagem_atual, cv2.COLOR_BGR2GRAY)
        else:
            imagem_cinza = imagem_atual

        # Aplica o detector de bordas Canny 1:3
        bordas = cv2.Canny(imagem_cinza, 60, 180)

        # Exibe a imagem de bordas no frame inferior direito
        imagem_bordas = cv2.cvtColor(bordas, cv2.COLOR_GRAY2BGR) 
        imagem_atual = imagem_bordas # Convertendo para 3 canais para exibição
        edit_pil = Image.fromarray(imagem_bordas)
        redimensionar_imagem(edit_pil, frame_inferior_direito, largura_frame, altura_frame)
        marcar_transformacao("Detector de borda: Canny")


def aplicar_binarizacao():
    global imagem_atual

    if imagem_atual is None:
        messagebox.showinfo("Erro", "Escolha uma imagem primeiro")
    else:
        # Converte a imagem para escala de cinza, se necessário
        if len(imagem_atual.shape) > 2 and imagem_atual.shape[2] > 1:
            imagem_cinza = cv2.cvtColor(imagem_atual, cv2.COLOR_BGR2GRAY)
        else:
            imagem_cinza = imagem_atual

        # Aplica a binarização utilizando o método de threshold
        ret, imagem_binaria = cv2.threshold(imagem_cinza, 127, 255, cv2.THRESH_BINARY)

        # Exibe a imagem binarizada no frame inferior direito
        imagem_binaria_colorida = cv2.cvtColor(imagem_binaria, cv2.COLOR_GRAY2BGR)
        imagem_atual = imagem_binaria
        edit_pil = Image.fromarray(imagem_binaria_colorida)
        redimensionar_imagem(edit_pil, frame_inferior_direito, largura_frame, altura_frame)
        marcar_transformacao("Binarização: Threshold")


def morfologia_matematica():
    global imagem_atual

    if imagem_atual is None:
        messagebox.showinfo("Erro", "Escolha uma imagem primeiro")
    else:
        # Converte a imagem para escala de cinza, se necessário
        if len(imagem_atual.shape) > 2 and imagem_atual.shape[2] > 1:
            imagem_cinza = cv2.cvtColor(imagem_atual, cv2.COLOR_BGR2GRAY)
        else:
            imagem_cinza = imagem_atual

        # Define o kernel para dilatação
        kernel = np.ones((5,5), np.uint8)

        # Aplica a dilatação na imagem
        imagem_dilatada = cv2.dilate(imagem_cinza, kernel, iterations=1)

        # Exibe a imagem processada no frame inferior direito
        imagem_atual = imagem_dilatada
        edit_pil = Image.fromarray(imagem_atual)
        redimensionar_imagem(edit_pil, frame_inferior_direito, largura_frame, altura_frame)
        marcar_transformacao("Morfologia Matemática - Dilatação")


def atualizar_lista_transformacoes():
    global transformacoes_selecionadas

    lista_transformacoes = ""
    for indice, transformacao in enumerate(transformacoes_selecionadas):
        lista_transformacoes += f"{indice} - {transformacao}\n"

    caixa_texto.config(state="normal")
    caixa_texto.delete("1.0", "end")
    caixa_texto.insert("end", lista_transformacoes)
    caixa_texto.config(state="disabled")

# Função para marcar e exibir as transformações selecionadas
def marcar_transformacao(transformacao):
    transformacoes_selecionadas.append(transformacao)
    atualizar_lista_transformacoes()

# Função para criar e atualizar a lista de transformações
def criar_lista_transformacoes(frame):
    global caixa_texto
    frame.config(bg="black", bd=2, relief="groove", highlightbackground="black")  # Ajustes no frame para parecer com uma janela
    caixa_texto = Text(frame, bg="black", fg="#00FF00", font=("Consolas", 12), width=74, height=13, highlightthickness=0)  # Ajustes na caixa de texto
    caixa_texto.pack(expand=True, fill="both")
    caixa_texto.config(state="disabled")
    
    botoes_excluir_lista(frame)

#exclui todas as transformaçoes feitas
def excluir_transformacao():
    global imagem_atual

    # Verifica se há uma imagem atual
    if imagem_atual is None:
        messagebox.showinfo("Erro", "Não há imagem para remover transformações.")
        return

    if not transformacoes_selecionadas:
        messagebox.showinfo("Erro", "Não há transformações para remover.")
        return
    
    # Limpar a caixa de texto
    caixa_texto.config(state="normal")
    caixa_texto.delete("1.0", "end")
    caixa_texto.config(state="disabled")
    transformacoes_selecionadas.clear()

    # Obtém os índices das transformações selecionadas na lista
    indices_selecionados = caixa_texto.tag_ranges("sel")

    # Remove as transformações selecionadas da lista de transformações realizadas
    for i in reversed(indices_selecionados):
        linha_inicio, coluna_inicio, linha_fim, coluna_fim = map(int, i.split("."))
        texto_selecionado = caixa_texto.get(f"{linha_inicio}.{coluna_inicio}", f"{linha_fim}.{coluna_fim}")
        caixa_texto.delete(f"{linha_inicio}.{coluna_inicio}", f"{linha_fim}.{coluna_fim}")

        # Remover a transformação da lista de transformações realizadas
        if texto_selecionado in transformacoes_selecionadas:
            transformacoes_selecionadas.remove(texto_selecionado)

    # Atualiza a imagem exibida para a imagem original
    imagem_atual = imagem_cv.copy()
    imagem_pil = Image.fromarray(imagem_atual)
    redimensionar_imagem(imagem_pil, frame_superior_direito, largura_frame, altura_frame)
    redimensionar_imagem(imagem_pil, frame_inferior_direito, largura_frame, altura_frame)

    messagebox.showinfo("Transformações removidas", "As transformações selecionadas foram removidas.")

#exibe os botões para limpar a lista de transformação e remover uma unica trasformação
def botoes_excluir_lista(frame):
    # Carregar a imagem do ícone
    icone = Image.open("./icons/Trash.png")
    icone = icone.resize((25, 20))  # Redimensionar o ícone se necessário
    icone = ImageTk.PhotoImage(icone)

    # Botão de excluir
    btnExcluir = Button(frame, bg='#000000', cursor="hand2", width=210, height=35, command=excluir_transformacao, image=icone, compound=RIGHT, highlightthickness=0, text="Limpar transformações", fg="#00ff00", font=("Consolas", 11, "bold"), padx=5, activebackground="#CCCCCC") 
    btnExcluir.image = icone
    btnExcluir.pack(side="left", padx=15, pady=9)


    icone = Image.open("./icons/Trash.png")
    icone = icone.resize((25, 20))  # Redimensionar o ícone se necessário
    icone = ImageTk.PhotoImage(icone)

    # Botão de excluir
    btnExcluir = Button(frame, bg='#000000', cursor="hand2", width=210, height=35, command=remover_item_selecionado, image=icone, compound=RIGHT, highlightthickness=0, text="Remover Transformação", fg="#00ff00", font=("Consolas", 11, "bold"), padx=5, activebackground="#CCCCCC") 
    btnExcluir.image = icone
    btnExcluir.pack(side="left", padx=10, pady=9)

#remove o iten selecinado pelo indice dele na lista
def remover_item_selecionado():
    global imagem_atual

    # Verifica se há uma imagem atual
    if imagem_atual is None:
        messagebox.showinfo("Erro", "Não há imagem para remover transformações.")
        return

    # Verifica se há itens na lista de transformações selecionadas
    if not transformacoes_selecionadas:
        messagebox.showinfo("Erro", "Não há transformações para remover.")
        return

    # Pede ao usuário para selecionar o índice do item a ser removido
    indice = simpledialog.askinteger("Remover Transformação", "Digite o índice da transformação a ser removida:")

    # Verifica se o índice é válido
    if indice is None or indice < 0 or indice >= len(transformacoes_selecionadas):
        messagebox.showinfo("Erro", "Índice inválido. Por favor, digite um índice válido.")
        return

    # Remove o item da lista de transformações selecionadas
    item_removido = transformacoes_selecionadas.pop(indice)

    atualizar_lista_transformacoes()

    messagebox.showinfo("Transformação removida", f"A transformação '{item_removido}' foi removida.")

    atualizar_imagem_atual()

#atualiza a imagem atual, "removendo" a filtro escolhido pelo remover_item_selecionado()
def atualizar_imagem_atual():
    global imagem_atual

    # Faz uma cópia da imagem original
    imagem_atual = imagem_cv.copy()

    # Aplica as transformações mantidas na lista de transformações
    for transformacao in transformacoes_selecionadas:
        if transformacao == "Conversão de cores: RGB -> CIE L*a*b*":
            imagem_atual = cv2.cvtColor(imagem_atual, cv2.COLOR_RGB2Lab)

        elif transformacao == "Conversão de cores: RGB -> XYZ":
            imagem_atual = cv2.cvtColor(imagem_atual, cv2.COLOR_RGB2XYZ)

        elif transformacao == "Conversão de cores: RGB -> HSV":
            imagem_atual = cv2.cvtColor(imagem_atual, cv2.COLOR_RGB2HSV)

        elif transformacao == "Conversão de cores: RGB -> Gray":
            imagem_atual = cv2.cvtColor(imagem_atual, cv2.COLOR_RGB2GRAY)

        elif transformacao == "Filtro Bilateral":
            imagem_atual = cv2.bilateralFilter(imagem_atual, 17, 75, 75)

        elif transformacao == "Detector de borda: Canny":
            if len(imagem_atual.shape) > 2 and imagem_atual.shape[2] > 1:
                imagem_cinza = cv2.cvtColor(imagem_atual, cv2.COLOR_BGR2GRAY)
            else:
                imagem_cinza = imagem_atual
            bordas = cv2.Canny(imagem_cinza, 60, 180)
            imagem_atual = cv2.cvtColor(bordas, cv2.COLOR_GRAY2BGR)
        elif transformacao == "Binarização: Threshold":
            if len(imagem_atual.shape) > 2 and imagem_atual.shape[2] > 1:
                imagem_cinza = cv2.cvtColor(imagem_atual, cv2.COLOR_BGR2GRAY)
            else:
                imagem_cinza = imagem_atual
            ret, imagem_binaria = cv2.threshold(imagem_cinza, 127, 255, cv2.THRESH_BINARY)
            imagem_atual = cv2.cvtColor(imagem_binaria, cv2.COLOR_GRAY2BGR)
        elif transformacao == "Morfologia Matemática: Dilatação":
            if len(imagem_atual.shape) > 2 and imagem_atual.shape[2] > 1:
                imagem_cinza = cv2.cvtColor(imagem_atual, cv2.COLOR_BGR2GRAY)
            else:
                imagem_cinza = imagem_atual
            kernel = np.ones((5,5), np.uint8)
            imagem_dilatada = cv2.dilate(imagem_cinza, kernel, iterations=1)
            imagem_atual = cv2.cvtColor(imagem_dilatada, cv2.COLOR_GRAY2BGR)

    # Redimensiona e exibe a imagem atual nos frames
    imagem_pil = Image.fromarray(imagem_atual)
    redimensionar_imagem(imagem_pil, frame_inferior_direito, largura_frame, altura_frame)

# Iniciar o loop da aplicação
abrir_janela()
