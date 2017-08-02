from gameplay import InvalidMove
from board import Board


class GameOver(Exception):
    pass


def read_position(position):
    if len(position) != 2:
        raise InvalidMove("Cant' read position %s" % position)
    try:
        y = {
            'a': 0,
            'b': 1,
            'c': 2,
            'd': 3,
            'e': 4,
            'f': 5,
            'g': 6,
            'h': 7,
        }[position[0]]
    except KeyError:
        raise InvalidMove("Cant' read column %s" % position[0])
    try:
        x = 8 - int(position[1])
    except ValueError:
        raise InvalidMove("Cant' read column %s" % position[1])
    return x, y


def read_input(message):
    r = message.split(" ")
    if len(r) != 2:
        raise InvalidMove("Cant' read move %s (needs 2 pos)" % message)
    pos = read_position(r[0])
    npos = read_position(r[1])
    return pos, npos


def play_move(move, board, f):
    pos, npos = read_input(move)
    board.move(pos, npos)
    f.write(move+"\n")


if __name__ == '__main__':
    print("++++ WELCOME TO CHESS ++++")
    print("\nHow to play:")
    print("\t- Specifiy your move such as 'a2 a4'")

    f = open("history.txt", "w+")

    board = Board()

    old_start = [
        "a2 a4",
        "b7 b5",
        "a4 b5",
        "c7 c6",
        "b5 c6",
        "b8 c6",
        "b1 c3",
        "d8 a5",
        "g1 f3",
        "a5 c3",
        "g2 g4",
        "c8 a6",
        "f1 h3",
    ]
    for move in old_start:
        play_move(move, board, f)

    cont = True
    while cont:
        board.display()
        try:
            print("\n%s is playing:" % board.player)
            move = input("\tMove:")
            if move in ["q", "quit", "s", "stop"]:
                raise GameOver
            play_move(move, board, f)
        except InvalidMove as e:
            print("/!\ InvalidMove :", e)
        except GameOver:
            cont = False
            pass

    f.close()
