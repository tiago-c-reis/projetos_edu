from random import choice

from app import helpers
from app import config

#  Machine_functions - - -
#  1: next_move()  > indica a posição onde a máquina irá jogar
# - - - - - - - -


def next_move(_scores: list, _lvl: int, _val: str) -> int:
    """
    Indica a posição onde a máquina irá jogar de acordo com Crowle & Singer (1993)
    :return: int > posição da próxima jogada
    """
    match _lvl:
        case 0:
            # Neste nível, a máquina escolhe aleatoriamente as posições que estejam disponíveis
            empty_pos = [i for i, x in enumerate(_scores) if x == ' ']
            play_pos = choice(empty_pos)

            print('\nRANDOM'.ljust(30, '-'))
            print(f'Computer move to {play_pos}\n')
            return play_pos

        case _:
            # Neste nível, a máquina escolhe com base nos critérios de Kevin & Siegler (1993)

            # 1: Vencer ou Bloquear > Vencer, se a máquina tem dois iguais em posição para ganhar
            #                         Bloquear, se o humano tem dois iguais em posição para ganhar
            win_slices = helpers.check(_val, 2, _scores)
            block_slices = helpers.check(config.SYMBOLS[_val == config.SYMBOLS[0]], 2, _scores)

            for j, slice_value in enumerate((win_slices, block_slices)):
                if slice_value:
                    for i, x in enumerate(_scores[slice_value]):
                        if x == " ":
                            print('\n', ['WIN', 'BLOCK'][j].ljust(30, '-'), sep='')
                            print(f'Computer move to {slice_value.start + slice_value.step * i}\n')
                            return slice_value.start + slice_value.step * i

            # 2: Centro > Escolher sempre o centro (pos = 4)
            if _scores[4] == " ":
                print('\nCENTER'.ljust(30, '-'))
                print(f'Computer move to {4}\n')
                return 4

            # 3: Canto Oposto > Escolher um canto oposto
            corners = 0, 2, 6, 8,
            for i, x in enumerate(corners):
                if _scores[x] == config.SYMBOLS[_val == config.SYMBOLS[0]] and _scores[::-1][x] == " ":
                    print('\nOPOSITE CORNER'.ljust(30, '-'))
                    print(f'Computer move to {corners[::-1][i]}\n')
                    return corners[::-1][i]

            # 4: Espaço lateral > Escolher posição a meio de uma lateral
            sides = 1, 3, 7, 5,
            for x in corners + sides:
                if _scores[x] == " ":
                    print('\nEMPTY CORNER OR SIDE'.ljust(30, '-'))
                    print(f'Computer move to {x}\n')
                    return x
