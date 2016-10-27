#Code for a very simple example of discrete localization
#Uses both sensorial information represented by the sense
#function as well as simulates movement of the robot through
#function move.

# n=5
# p=[1./n]*n
# p=[0,1,0,0,0]
# pHit = 0.6
# pMiss = 0.2
# pExact = 0.8
# pOvershoot = 0.1
# pUndershoot = 0.1
#
# world=['green','red','red','green','green']
# measurements = ['red', 'green']
# motions = [1,-1]

def sense(p, Z):
    q=[]
    for i in range(len(p)):
        hit = (world[i]==Z)
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
    s=sum(q)
    for i in range(5):
        q[i]/=s
    return q

def circular_shift(p, U):             #nice way to shift a list left or right in a circular way!
    n = U % len(p)
    q = p[-n:] + p[:-n]
    return q

def move(p, U):
    q = [0]*len(p)
    for i in range(len(p)):
        q[i] += (p[i-U%len(p)] * pExact + p[i-(U-1)%len(p)] * pOvershoot + p[i-(U+1)%len(p)] * pUndershoot)
    return q

# for i in range(len(motions)):
#     p = sense(p,measurements[i])
#     p = move(p, motions[i])
#
# print p

def sense2D(colors,Z,p,sensor_right):
    q = [[0for row in range(len(colors[0]))] for col in range(len(colors))]

    numRows = len(colors[0])
    numCols = len(colors)
    s = 0
    for i in range(numRows):
        for j in range(numCols):
            hit = (colors[i][j] == Z)
            q[i][j] = (p[i][j] * (hit * sensor_right + (1 - hit) * (1-sensor_right)))
        s += sum(q[i])

    for i in range(numRows):
        for j in range(numCols):
            q[i][j] /= s

    return q

def move2D(p,motions,p_move):
    numRows = len(p[0])
    numCols = len(p)
    moveVer = motions[0]
    moveHor = motions[1]

    #if there is no movement simply return the same probability matrix
    if(moveVer == 0 and moveHor == 0):
        return(p)

    q = [[0 for row in range(numRows)] for col in range(numCols)]

    #Try to move vertically first
    if(moveVer != 0):
        for i in range(numRows):
            for j in range(numCols):
                q[i][j] += (p[i-moveVer%numRows][j] * p_move + p[i][j] * (1-p_move))

    #Try to move Horizontally second
    if(moveHor != 0):
        for i in range(numRows):
            for j in range(numCols):
                q[i][j] += (p[i][j-moveHor%numCols] * p_move + p[i][j] * (1-p_move))

    return q

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x), r)) + ']' for r in p]
    print '[' + ',\n '.join(rows) + ']'

def localize(colors, measurements, motions, sensor_right, p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]
    numIter = len(measurements)
    print 'numIter = ', numIter

    for i in range(numIter):
        # Move First
        p = move2D(p,motions[i],p_move)
        print 'After Move'
        show(p)
        print '------------------'
        #Measure Second
        p = sense2D(colors, measurements[i],p,sensor_right)
        print 'After sense'
        show(p)
        print '-------------------'

    return p

colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R', 'R']
motions = [[0,0], [0,1]]
sensor_right = 1.0
p_move = 0.5
p2 = localize(colors, measurements, motions, sensor_right, p_move)
show(p2)  # displays your answer