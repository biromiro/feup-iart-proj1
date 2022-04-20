from time import sleep


class BoardAnimator:
    def __init__(self):
        pass

    def frame(self, board, commands, position, commandIdx):
        board.display(position)
        print(commands)
        print('  ', end='')
        for idx in range(len(commands)):
            if idx == commandIdx:
                print('_', end='')
                break
            print('     ', end='')
        print('')
        sleep(1)
