## Solve Every Sudoku Puzzle

## See http://norvig.com/sudoku.html

## Throughout this program we have:
##   r is a row,    e.g. 'A'
##   c is a column, e.g. '3'
##   s is a square, e.g. 'A3'
##   d is a digit,  e.g. '9'
##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits


squares  = cross(rows, cols)

unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

################ Unit Tests ################

def test():
    "A set of tests that must pass."
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print ('All tests pass.')

################ Parse a Grid ################



#fill each 3x3 square by random number between 1 and 9 but no repetition within the square return grid
def fill_square(grid):
    #grid is dict(zip(squares, chars))
    #get first group of squares

    squares = ['A1', 'A4', 'A7', 'D1', 'D4', 'D7', 'G1', 'G4', 'G7']
    for s in squares:
        #get the unit of the square
        quadrant = units[s][2]
        seen = []
        #first pass to add the already filled squares
        for square in quadrant:
            value = grid[square]
            if value != '0' or value != '.':
                seen.append(value)
        #second pass to fill the empty squares
        for square in quadrant:
            value = grid[square]
            if value == '0' or value == '.':
                value = str(random.randint(1,9))
                while value in seen:
                    value = str(random.randint(1,9))
                seen.append(value)
                grid[square] = value
    return grid


def calculte_conflics(values):
    conflicts = 0
    for unit in unitlist:
        for square in unit:
            for peer in peers[square]:
                if values[square] == values[peer]:
                    conflicts += 1
    return conflicts




def hill_climbing(grid):
    values = grid_values(grid)
    conflicts = calculte_conflics(values)
    while conflicts > 0:
        #get a random square
        square = random.choice(squares)
        #get the unit of the square
        unit = units[square][2]
        #get the value of the square
        value = values[square]
        #get the peers of the square
        peers = peers[square]
        #get the values of the peers
        peers_values = [values[peer] for peer in peers]
        #get the possible values of the square
        possible_values = [str(i) for i in range(1,10) if str(i) not in peers_values]
        #get a random value from the possible values
        new_value = random.choice(possible_values)
        #update the value of the square
        values[square] = new_value
        #calculate the new conflicts
        new_conflicts = calculte_conflics(values)
        #if the new conflicts are greater than the old conflicts
        if new_conflicts > conflicts:
            #revert the changes
            values[square] = value
        conflicts = new_conflicts
    return values


    






def display_grid(grid):
    squares = ['A1', 'A4', 'A7', 'D1', 'D4', 'D7', 'G1', 'G4', 'G7']
    
    for s in squares:
        
        quadrant = units[s][2]
        print("############")
        for square in quadrant:
            print(grid[square])
            





def display(values):
    "Display these values as a 2-D grid."
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print (''.join(values[r+c].center(width)+('|' if c in '36' else ''))
                      for c in cols)
        if r in 'CF': print(line)



def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))













################ Utilities ################

def some(seq):
    
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False

def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    return open(filename).read().strip().split(sep)

def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq

################ System test ################

import time, random

def solve_all(grids, name='', showif=0.0001):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""
    def time_solve(grid):
        start = time.process_time()
        values = solve(grid)
        #print(values)
        t = time.process_time()-start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print ('(%.2f seconds)\n' % t)
        return (t, solved(values))
    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print ("Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times)/N, N/sum(times), max(times)))

def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    #print(values)
    #print(grid_values)
    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)
    return values is not False and all(unitsolved(unit) for unit in unitlist)

def random_puzzle(N=17):
    """Make a random puzzle with N or more assignments. Restart on contradictions.
    Note the resulting puzzle is not guaranteed to be solvable, but empirically
    about 99.8% of them are solvable. Some have multiple solutions."""
    values = dict((s, digits) for s in squares)
    for s in shuffled(squares):
        if not assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) >= N and len(set(ds)) >= 8:
            return ''.join(values[s] if len(values[s])==1 else '.' for s in squares)
    return random_puzzle(N) ## Give up and make a new puzzle

grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
    
if __name__ == '__main__':

    #display the grid 
    grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    grid = fill_square(grid_values(grid))
    display_grid(grid)







    

## References used:
## http://www.scanraid.com/BasicStrategies.htm
## http://www.sudokudragon.com/sudokustrategy.htm
## http://www.krazydad.com/blog/2005/09/29/an-index-of-sudoku-strategies/
## http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/sudoku/
