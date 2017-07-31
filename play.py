from board.board import Board, InvalidMove


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
    f.write(move+"\n")
    board.move(pos, npos)


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
