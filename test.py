# this module if used to
# test 2 modes of the tic_tac_toe game


from game import GameFull, GameBinary


while True:
    try:
        n = int(input("Select difficulty (1 - easy, 2 - medium)"))
        assert (isinstance(n, int))
        assert (n >= 1 and n <= 2)
        break
    except:
        print("Wrong data! Try again")
if n == 1:
    g = GameBinary()
if n == 2:
    g = GameFull()

g.start()