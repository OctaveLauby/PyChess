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


if __name__ == '__main__':
    print("++++ WELCOME TO CHESS ++++")
    print("\nHow to play:")
    print("\t- Specifiy your move such as 'a2 a4'")

    board = Board()
    board.display()

    cont = True
    while cont:
        try:
            print("\n%s is playing:" % board.player)
            message = input("\tMove:")
            if message in ["q", "quit", "s", "stop"]:
                raise GameOver
            pos, npos = read_input(message)
            board.move(pos, npos)
            board.display()
        except InvalidMove as e:
            print("/!\ InvalidMove :", e)
        except GameOver:
            cont = False
            pass
