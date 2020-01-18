from ChessGame import ChessGame

chessGame = ChessGame()
chessGame.initializeBoard()
# chessGame.printBoard()

# steps = [("e2","e4"),("d7","d5"),("e4","d5")]
steps = [("e2","e4"),("f7","f5"),("d1","h5"),("g8","f6"),("h5","e8")]

for startPosition,endPosition in steps:
	if(chessGame.move(startPosition,endPosition)):
		chessGame.printBoard()
	else:
		print("-- Stopped!!")
		break
