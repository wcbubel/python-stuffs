import sys

def move( n, src, dst ):
    global moves
    moves = moves + 1
    print "move %i (%i) %i->%i" % (moves, n, src, dst)

def tower( mover, count, begin, aux, ender ):
    if count > 0:
        tower( mover, count-1, begin, ender, aux )
        mover( count, begin, ender )
        tower( mover, count-1, aux, begin, ender )

if __name__ == "__main__":
    global moves
    moves = 0
    print sys.argv[1]
    c = int(sys.argv[1])
    tower( move, c, 1, 2, 3 )
    print "Moves: " + str(moves)
