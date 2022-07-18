import GUIobject
s = 18
board = (176, 222)
GUIobject.generate_slot(s, s, (255, 0, 0), (255, 255, 255), (0, 0, 0)).save('tests/slot.png')
GUIobject.generate_background(*board, (255, 0, 0), (0, 0, 255), (255, 255, 255), (0, 0, 0)).save('tests/board.png')