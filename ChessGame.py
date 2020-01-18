class ChessGame:
	def __init__(self):
		self.BOARD_SIZE=8
		self.board=[ [ None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE) ]
		self.symbols = {("king",True):u"\u2654",("queen",True):u"\u2655",("rook",True):u"\u2656",("bishop",True):u"\u2657",("knight",True):u"\u2658",("pawn",True):u"\u2659",
						("king",False):u"\u265A",("queen",False):u"\u265B",("rook",False):u"\u265C",("bishop",False):u"\u265D",("knight",False):u"\u265E",("pawn",False):u"\u265F"
						}
		self.isMyTurn=True

	def initializeBoard(self):
		self.board=[ [ None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE) ]
		for j in range(self.BOARD_SIZE):
			self.board[1][j] = ("pawn",False)
			self.board[6][j] = ("pawn",True)
		self.board[0] = [("rook",False),("knight",False),("bishop",False),("queen",False),("king",False),("bishop",False),("knight",False),("rook",False)]
		self.board[7] = [("rook",True),("knight",True),("bishop",True),("queen",True),("king",True),("bishop",True),("knight",True),("rook",True)]
		self.isMyTurn = True

	def printBoard(self):
		print(''.join(["   "]+[ " "+col+"  " for col in "abcdefgh"]))
		for rowI in range(self.BOARD_SIZE):
			print("  |"+"---|"*8)
			print(''.join([str(8-rowI)+" |"]+[ " "+self.symbols[piece]+" |" if piece else '   |' for piece in self.board[rowI]]))
		print("  |"+"----"*8)
		print(''.join(["   "]+[ " "+col+"  " for col in "abcdefgh"]))

	def positionToIndexPair(self,position):
		return 8-int(position[1]) , ord(position[0])-97

	def indexPairToposition(self,i,j):
		return chr(j+97)+str(8-i)

	def move(self,startPosition,endPosition):
		if(startPosition==endPosition):
			print("-- invalid move: choose a target position different from the current position.")
			return False
		iS,jS=self.positionToIndexPair(startPosition)
		iE,jE=self.positionToIndexPair(endPosition)
		if(self.board[iS][jS]==None):
			print("-- Error: please choose a piece: "+startPosition)
			return False
		if(self.board[iS][jS][1]!=self.isMyTurn):
			print("-- Error: this is not my piece: "+startPosition)
			return False
		if(self.board[iE][jE]!=None and (self.board[iE][jE][1]==self.isMyTurn) ):
			print("-- Error: the target position is occupied: "+endPosition)
			return False
		name = self.board[iS][jS][0]
		if(self.isValidMove(name,iS,jS,iE,jE)):
			if(self.board[iE][jE]==("king",False)):
				print("!!!CHECK MATE! I wone.")
				return False
			if(self.board[iE][jE]==("king",True)):
				print("!!!CHECK MATE! Opponent won.")
				return False
			self.board[iE][jE]=self.board[iS][jS]
			self.board[iS][jS]=None
			self.isMyTurn=not self.isMyTurn
			return True
		# print("-- Error: no move.")
		return False

	def isValidMove(self,type,iS,jS,iE,jE):
		if(type=="pawn"):
			if(self.isMyTurn):
				if(abs(iS-iE)==1 and jS-1==jE and self.board[iE][jE]!=self.isMyTurn):
					return True
				if( jS==jE and iS-1==iE):
					return True
				if( jS==jE and iS==self.BOARD_SIZE-2 and iS-2==iE and self.board[iS-1][jS]==None):
					return True
			else:
				if(abs(iS-iE)==1 and jS+1==jE and self.board[iE][jE]!=self.isMyTurn):
					return True
				if( jS==jE and iS+1==iE):
					return True
				if( jS==jE and iS==1 and iS+2==iE and self.board[iS+1][jS]==None):
					return True
			print("-- invalid move: pawn is not moved.")
			return False
		if(type=="knight"):
				if(abs(iS-iE)==1 and abs(jS-jE)==2 or abs(iS-iE)==2 and abs(jS-jE)==1):
					return True
				else:
					print("-- invalid move: knight should move in L shape.")
					return False
		if(type=="rook"):
			if(iS!=iE and jS!=jE):
				print("-- invalid move: rook should move straight.")
				return False
			if(iS==iE):
				for j in range(min(jS,jE)+1,max(jS,jE)):
					if(self.board[iS][j]!=None):
						print("-- invalid move: the queen is blocked at: "+self.indexPairToposition(iS,j))
						return False
			if(jS==jE):
				for i in range(min(iS,iE)+1,max(iS,iE)):
					if(self.board[i][jS]!=None):
						print("-- invalid move: the rook is blocked at: "+self.indexPairToposition(i,jS))
						return False
			return True
		if(type=="bishop"):
			if(abs(iS-iE)!=abs(jS-jE)):
				print("-- invalid move: bishop should move diagonally.")
				return False
			if(iS<iE):
				for i,j in zip(range(iS+1,iE),range(jS+1,jE)):
					if(self.board[i][j]!=None):
						print("-- invalid move: the bishop is blocked at: "+self.indexPairToposition(i,j))
						return False
				for i,j in zip(range(iS+1,iE),range(jS-1,jE,-1)):
					if(self.board[i][j]!=None):
						print("-- invalid move: the bishop is blocked at: "+self.indexPairToposition(i,j))
						return False
			else:
				for i,j in zip(range(iS-1,iE,-1),range(jS+1,jE)):
					if(self.board[i][j]!=None):
						print("-- invalid move: the bishop is blocked at: "+self.indexPairToposition(i,j))
						return False
				for i,j in zip(range(iS-1,iE,-1),range(jS-1,jE,-1)):
					if(self.board[i][j]!=None):
						print("-- invalid move: the bishop is blocked at: "+self.indexPairToposition(i,j))
						return False
			return True
		if(type=="queen"):
			if(iS!=iE and jS!=jE and abs(iS-iE)!=abs(jS-jE)):
				print("-- invalid move: pawn should move straight or diagonally.")
				return False
			if(iS==iE):
				for j in range(min(jS,jE)+1,max(jS,jE)):
					if(self.board[iS][j]!=None):
						print("-- invalid move: the queen is blocked at: "+self.indexPairToposition(iS,j))
						return False
			if(jS==jE):
				for i in range(min(iS,iE)+1,max(iS,iE)):
					if(self.board[i][jS]!=None):
						print("-- invalid move: the queen is blocked at: "+self.indexPairToposition(i,jS))
						return False
			if(iS<iE):
				for i,j in zip(range(iS+1,iE),range(jS+1,jE)):
					if(self.board[i][j]!=None):
						print("-- invalid move: the queen is blocked at: "+self.indexPairToposition(i,j))
						return False
				for i,j in zip(range(iS+1,iE),range(jS-1,jE,-1)):
					if(self.board[i][j]!=None):
						print("-- invalid move: the queen is blocked at: "+self.indexPairToposition(i,j))
						return False
			else:
				for i,j in zip(range(iS-1,iE,-1),range(jS+1,jE)):
					if(self.board[i][j]!=None):
						print("-- invalid move: the queen is blocked at: "+self.indexPairToposition(i,j))
						return False
				for i,j in zip(range(iS-1,iE,-1),range(jS-1,jE,-1)):
					if(self.board[i][j]!=None):
						print("-- invalid move: the queen is blocked at: "+self.indexPairToposition(i,j))
						return False
			return True
		if(type=="king"):
				if(abs(iS-iE) in [1,0] and abs(jS-jE) in [1,0]):
					return True
				else:
					print("-- invalid move: king should move only one step around.")
					return False
		return False


