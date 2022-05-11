from tkinter import Label, Canvas, ACTIVE, DISABLED
from random import choice

from app import config
from app import machine_funcs
import __main__

#  Helpers - - -
#  1: new_game()      > inicia uma nova ronda
#  2: quit_game()     > imprime na consola/tela o resultado final e termina o aplicativo
#  3: update_scores() > atualiza as pontuações no frame de topo
#  4: change_lvl()    > altera o valor do nível de dificuldade da máquina
#  5: add()           > adiciona o símbolo do humano ou máquina consoante quem está a jogar + verifica se alguém ganhou
#  6: check()         > retorna a linha, coluna ou diagonal que tem um número _val de vezes o símbolo _ref
# - - - - - - - -


def new_game():
    """
    Inicia uma nova ronda do jogo
    """
    __main__.scores = [' '] * 9      # Re-inicia scores

    for x in __main__.buttons:       # Todos os botões estão agora ativos
        x['text'] = " "
        x.config(state=ACTIVE, bg=config.COLORS[1])

    # Aleatoriamente escolhe novamente o primeiro jogador e verifica se é a máquina
    if choice(config.SYMBOLS) == __main__.machine:
        # Escolher a primeira posição com base no nível da máquina
        # se 0 aleatório; se 1 escolhe sempre 4 (melhor posição)
        pos = choice(range(9)) if __main__.machine_lvl == 0 else 4
        __main__.buttons[pos]['text'] = __main__.machine
        __main__.scores[pos] = __main__.machine


def quit_game():
    """
    Imprime um relatório final na consola/tela e termina o applicativo
    """
    line = '\n' + '-' * 50 + '\n'
    report = ' | '.join([f'{k.title()}: {v} games' for k, v in __main__.victories.items()])

    print(line, report, line)

    quit()


def stop_game(_result: slice or False, player: str):
    """
    Termina a ronda que estava em curso. Desativa os botões e incrementa variável victories
    """
    __main__.monster_btn.config(state=ACTIVE)

    tags = {'human': ('humano', 44), 'machine': ('máquina', 41)}

    for x in __main__.buttons:
        x.config(state=DISABLED, disabledforeground='white')

        if x in __main__.buttons[_result]:
            x.config(bg=config.COLORS[__main__.machine_lvl + 2], disabledforeground='white')

    __main__.victories[player] += 1
    msg = f'''\u001b[{tags[player][1]};1m{player.title()} Won | {tags[player][0].title()} Venceu\u001b[0m'''
    print(msg.center(50, '-'))


def update_scores():
    """
    Atualiza o valor das pontuações
    """
    values = __main__.victories.get('human'), ':', __main__.victories.get('machine')

    for j, value in enumerate(values):
        Label(__main__.frame_top, text=value, font=config.FONT.get('scores'), bg=config.COLORS[0])\
            .grid(row=0, column=j+1)


def change_lvl():
    """
    Altera o nível da máquina ao pressionar o botão
    """
    flag = __main__.monster_btn['image'] != 'pyimage3'
    __main__.monster_btn.config(image=__main__.monster_imgs[flag])

    __main__.machine_lvl = flag     # Atualiza o nível da máquina

    print(f'Machine lvl. updated: {int(flag)}\n')


def add(_pos: int) -> bool:
    """
    Coloca o símbolo do humano ou máquina. Verifica depois se alguém venceu.
    """

    if __main__.buttons[_pos]['text'] == ' ':
        # É a vez do humano jogar
        __main__.buttons[_pos]['text'] = __main__.scores[_pos] = __main__.human

        result = check(__main__.human, 3, __main__.scores)    # Verifica se venceu (3 símbolos iguais)

        if result:
            # Humano venceu
            stop_game(result, 'human')
            update_scores()
            return True

        # É a vez da máquina
        empty_btns = [x for x in __main__.buttons if x['text'] == " "]      # Verifica possibilidades para jogar

        if len(empty_btns) > 0:
            _pos = machine_funcs.next_move(__main__.scores, __main__.machine_lvl, __main__.machine)

            __main__.buttons[_pos]["text"] = __main__.scores[_pos] = __main__.machine

            result = check(__main__.machine, 3, __main__.scores)      # Verifica se venceu

            if result:
                # Máquina venceu
                stop_game(result, 'machine')
                update_scores()
                return True

        empty_btns = [x for x in __main__.buttons if x['text'] == " "]

        # Não existem mais jogadas, vamos verificar o resultado final
        if len(empty_btns) == 0:

            for analysis in __main__.human, __main__.machine:
                #  Capturar a chave que estamos a analisar
                key = ['machine', 'human'][analysis == __main__.human]

                if check(analysis, 3, __main__.scores):

                    __main__.victories[key] += 1

                    update_scores()

                    msg = f'\u001b[44;1m {key} \u001b[0m'
                    print(msg.center(50, '-'))

                    return True

            else:
                __main__.victories['draw'] += 1
                msg = '\u001b[42;1mDraw | Empate\u001b[0m'
                print(msg.center(50, '-'))

                rect = Canvas(__main__.root, bg=config.COLORS[__main__.machine_lvl + 2])
                rect.place(x=95, y=208)

                rect_label = Label(rect, text='Draw', bg=config.COLORS[__main__.machine_lvl + 2], width=10, height=2,
                                   borderwidth=0, border=0)
                rect_label.config(font=config.FONT.get('result'))
                rect_label.pack()

                update_scores()

                __main__.root.after(1500, rect.destroy)     # Esperar 1.5 segundos, antes de desaparecer
                return True


def check(_val: str, _ref: int, _scores: list) -> slice or False:
    """ Retorna a linha, coluna ou diagonal que tem um número _val de vezes o símbolo _ref
       :returns: um objeto slice correspondente ou Falso"""

    for i in range(3):
        # Analisar todas as linhas e colunas
        linha, coluna = slice(3 * i, (i + 1) * 3, 1), slice(i, 7 + i, 3)

        if _scores[linha].count(_val) == _ref:
            return linha

        if _scores[coluna].count(_val) == _ref:
            return coluna

    # Analisar as duas diagonais possíveis
    for diagonal in slice(0, 9, 4), slice(2, 7, 2):
        if _scores[diagonal].count(_val) == _ref:
            return diagonal

    return None
