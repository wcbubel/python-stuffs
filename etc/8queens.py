#
# 8 Queens
#

def n_queens( n, width ):
    if n == 0:
        return [[]]
    else:
        return add_queen( n-1, width, n_queens(n-1, width))

def add_queen( new_row, width, prev_sol ):
    solut = []
    for sol in prev_sol:
        for new_col in range(width):
            if safe_queen(new_row, new_col, sol):
                solut.append(sol + [new_col])
    return solut

def safe_queen( new_row, new_col, sol ):
    for row in range(new_row):
        if (sol[row] == new_col or
            abs(sol[row]-new_col)==abs(row-new_row)):
                return 0
    return 1

for sol in n_queens( 8, 8 ):
    print sol

