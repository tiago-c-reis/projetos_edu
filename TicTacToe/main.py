import os
import sys
from tkinter import Tk, Frame, PhotoImage, Label, Button, LEFT
from app import config
from app import helpers

import random


# Função necessária para ir buscar as imagens à pasta temporária para PyInstaller
def resource_path(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS,
        # and places our data files in a folder relative to that temp
        # folder named as specified in the datas tuple in the spec file
        base_path = os.path.join(sys._MEIPASS, '.')
    except AttributeError:
        # sys._MEIPASS is not defined, so use the original path
        base_path = ""

    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    # 1. Definir variáveis necessárias iniciais
    machine_lvl = 0
    victories = {'human': 00, 'machine': 00, 'draw': 0}

    human = random.choice(config.SYMBOLS)                   # escolha aleatória dos símbolos para o humano
    machine = config.SYMBOLS[human == config.SYMBOLS[0]]    # depois a máquina fica com o outro símnolo

    start = random.choice(config.SYMBOLS)     # definir aleatoriamente quem começa o jogo

    # 2. Criar janela de base:
    root = Tk()

    # 2.1. Definir cor de fundo, dimensões e evitar que as suas dimensões sejam modficadas
    root.config(bg=config.COLORS[0])
    root.geometry(str(config.WIDTH) + 'x' + str(config.HEIGHT))
    root.resizable(False, False)

    # 2.2. Adicionar icone e título do aplicativo
    root.iconbitmap(resource_path(r"app\images\root.ico"))
    root.title(config.TXT.get('title'))

    # 2.3. Criar frame de topo
    frame_top = Frame(root, bg=config.COLORS[0])
    frame_top.pack()

    # 2.3.1. Colocar foto do humano
    human_photo = PhotoImage(file=resource_path(r"app\images\human_photo.png"), width=70, height=70)
    Label(frame_top, image=human_photo, bg=config.COLORS[0]).grid(row=0, column=0)

    # 2.3.2. Atualizar a pontuações no frama de topo
    helpers.update_scores()

    # 2.3.3. Colocar foto da máquina
    monster0, monster1 = resource_path(r"app\images\monster_photo_0.png"), resource_path(r"app\images\monster_photo_1.png")

    monster_imgs = ()
    for img in monster0, monster1:
        monster_imgs += PhotoImage(file=img, width=70, height=70),

    monster_btn = Button(frame_top, image=monster_imgs[0], bg=config.COLORS[0], border=0,
                         activebackground=config.COLORS[0], command=helpers.change_lvl)
    monster_btn.grid(row=0, column=5)

    # 2.4. Criar frame do meio
    frame_middle = Frame(root, bg=config.COLORS[0], padx=10, pady=10)
    frame_middle.pack()

    # 2.4.1 Criar 9 butões para o applicativo
    buttons, scores = [], [' '] * 9
    for i in range(9):
        # Para os 9 butões, vamos determinar para cada botão a sua linha e coluna correspondentes
        row, col = i // 3, i % 3

        # Obter os butões e colocar pelo método grid no frame do meio
        btn = Button(frame_middle, text=' ', font=config.FONT.get('btns'), height=1, width=3,
                     bg=config.COLORS[1], activebackground=config.COLORS[1], fg='white', activeforeground='white',
                     border=0, command=lambda x=i: helpers.add(x))
        btn.grid(row=row, column=col, padx=3, pady=5)

        # Anexar os objetos (butões) criados à variável buttons
        buttons.append(btn)

    # 2.5. Criar frame do fim
    frame_bottom = Frame(root, bg=config.COLORS[0])
    frame_bottom.pack(ipady=10)

    # 2.5.1 Criar 2 butões: Quit Game, New Game
    function_names = 'Quit Game', 'New Game'
    for i, func in enumerate((helpers.quit_game, helpers.new_game)):
        _btn = Button(frame_bottom, text=function_names[i], padx=5, pady=5,
                      bg=config.COLORS[0], activebackground=config.COLORS[0],
                      font=('Comic Sans MS', 14, 'bold italic'),
                      activeforeground='white',
                      border=0, command=func)
        _btn.grid(row=0, column=i)

    # (Opcional) 2.6. Criar frame promocional do canal
    frame_channel = Frame(root, bg='white')
    frame_channel.pack()

    yt_photo = PhotoImage(file=resource_path(r"app\images\youtube_logo.png"))

    yt_label_0 = Label(frame_channel, bg=config.COLORS[0])
    yt_label_0.config(text=config.TXT.get('channel'), font=config.FONT.get('promo')[0],
                      padx=10, bg='white', image=yt_photo, compound=LEFT)
    yt_label_0.pack()

    yt_label_1 = Label(frame_channel, bg=config.COLORS[0])
    yt_label_1.config(text=config.TXT.get('url'), font=config.FONT.get('promo')[1],
                      fg=config.COLORS[1], bg='white')
    yt_label_1.pack()

    # 2.7. No caso em que a máquina é a primeira a começar
    if start == machine:
        # Escolher a primeira posição com base no nível da máquina
        # se 0 aleatório; se 1 escolhe sempre 4 (melhor posição)
        pos = random.choice(range(9)) if machine_lvl == 0 else 4
        buttons[pos]['text'] = scores[pos] = machine

    # 2.8. Mainloop da nossa janela de base
    root.mainloop()
