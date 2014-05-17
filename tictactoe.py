#!/usr/bin/env python
import random

class Player:
    def __init__(self,c):
        self.mychar = c
        self.myname=None
        self.setName()
    def setName(self):
        prompt='Enter name for Player '+str(self.mychar)+': '
        name = raw_input(prompt)

        if name.isalnum():
            self.myname=name
        else:
            prompt = 'Name must be nonempty alphanumeric string.\n'+prompt
        while (not self.myname):
            name = raw_input(prompt)
            if name.isalnum():
                self.myname=name
            # set human player for player not called computer
            # set computer player for player called computer
    def getC(self):
        # give character of player
        return self.mychar
    def getMove(self,board):
        #ask player where to move
        try:
            return int(raw_input(str(self.myname)+' ('+self.mychar+\
                '), move where? (enter number 1-'+str(board.getDim()**2)+', unoccupied): '))
        except ValueError:
            return 0

class Human(Player):
    def getMove(self,board):
        try:
            return int(raw_input(str(self.myname)+' ('+self.mychar+\
                '), move where? (enter number 1-'+str(board.getDim()**2)+', unoccupied): '))
        except ValueError:
            return 0

# computer is the same as human player, but just rewrite the getMove function
# board.board=[[a,b,c],[d,e,f],[g,h,i]] where each letter can be 'O', 'X', or None; columns within rows
# class Computer(Player):
#     def getMove(self,board):


class Board:
    def __init__(self, dim):
        self.dim=dim

        self.board=[]
        newR=[]
        for r in xrange(0,self.dim):
            for c in xrange(0,self.dim):
                newR.append(None)
            self.board.append(newR)
            newR=[]

    def __str__(self):
        # empty,pretty='.', lambda val: val if val else empty # print contents of square or empty
        # new line before board. new line after each horizontal row. grid lines corresponding to num of squares. bars between columns
        rowslist=[]
        for r in xrange(0,self.dim):
            start=r*self.dim+1
            rowslist.append(' | '.join(map(self._charify,self.board[r]))+\
                '\t('+') ('.join(map(str,[c for c in xrange(start,start+self.dim)]))+')')
        return ('\n'+('-+-'.join('-' for col in self.board[0]))+'\n').join(rowslist)

    # helper function
    def _charify(self,val):
        return str(val) if val else '.'

    def simpleboard(self):
        # empty,pretty='.', lambda val: val if val else empty
        return ('\n'+('-+-'.join('-' for col in self.board[0]))+'\n').join(' | '.join(map(self._charify,row)) for row in self.board)

    def setSquare(self,i_plus_one,v):
        #set value in 1..dim^2
        coords=self.getCoords(i_plus_one)
        self.board[coords[0]][coords[1]] = v
        return coords
    def getVal(self,i_plus_one):
        # get value in square 1..dim^2
        coords=self.getCoords(i_plus_one)
        return self.board[coords[0]][coords[1]]
    def getRow(self,r):
        return self.board[r] # get vals in row, 0..dim-1
    def getCol(self,c):
        return [r[c] for r in self.board] # get vals in column 0..dim-1
    def getD(self,d):
        # get vals in diagonal
        return [self.board[self.dim-1-i][i] for i in xrange(0,self.dim)] if d else [self.board[i][i] for i in xrange(0,self.dim)]
    def getDim(self):
        return self.dim # return the dimension
    def getCoords(self,i_plus_one):
        return [(i_plus_one-1)/self.dim,(i_plus_one-1)%self.dim] # get r and c coordinates
    def simpleStr(self):
        # charify=lambda val: str(val) if val else '.'
        return ''.join(self._charify(c) for r in self.board for c in r)


class Game:
    def __init__(self,players,dim):
        # self.board,self.players=Board(dim),map((Player),players) # create board and players
        self.board,self.players=Board(dim),map((Human),players)
        self.moves,self.lastmove=0,None # no moves yet
        print '\nPlayers:',', '.join(map((lambda p: str(p.myname)),self.players))
        
        self.offset = random.randint(0,1)
        print self.players[self.offset].myname,"goes first!\n"

    def announce(self):
        # get player name, print board
        print str(self.players[(self.moves+self.offset)%len(self.players)].myname),'to move'
        print 'Board:\n',str(self.board),'\n'
    def announce_winner(self):
        # check number of moves versus number of players, and announce
        print str(self.players[(self.moves)%len(self.players)].myname)\
        +' ('+self.players[(self.moves)%len(self.players)].mychar+') '+'wins!'
    def is_won(self):
        # tests each turn to see whether the game has finished
        if self.lastmove: # if game has started
            # single=lambda l: 1==len(l)
            single=lambda l: 1==len(list(set(l))) # returns unique values in a list
            # if there is only one value in the row, column, or diagonal that was last played, that player won

            # check row and column
            if single(self.board.getRow(self.lastmove[0])) or single(self.board.getCol(self.lastmove[1])):
                return True

            if self.lastmove[0]==self.lastmove[1]: #check first diagonal as needed
                if single(self.board.getD(0)):
                    return True

            if self.lastmove[0]+self.lastmove[1] == self.board.getDim()-1: #check second diagonal as needed
                return single(self.board.getD(1))

        return False
    def is_over(self):
        return self.moves==self.board.getDim()**2
    def play_turn(self):
        # get player, have player move, set square
        p=self.players[(self.moves+self.offset)%len(self.players)]
        maxval=self.board.getDim()**2

        val=True
        while (val):
            i=0 #check for valid range 1..dim^2
            while (i not in xrange(1,maxval+1)):
                i=p.getMove(self.board)
            val=self.board.getVal(i)

        self.lastmove=self.board.setSquare(i,p.getC())
        self.moves = self.moves+1

def play():
    tictactoe = Game(['X','O'],3)

    while (not tictactoe.is_won() and not tictactoe.is_over()):
        tictactoe.announce()
        tictactoe.play_turn()

    print 'Board:\n',str(tictactoe.board.simpleboard())

    if tictactoe.is_won():
        tictactoe.announce_winner()
    else:
        print "Game is a draw!"

if __name__ =='__main__':
    play()
