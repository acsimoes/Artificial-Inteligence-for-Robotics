# -------------------
# Background Information
#
# In this problem, you will build a planner that helps a robot
# find the shortest way in a warehouse filled with boxes
# that he has to pick up and deliver to a drop zone.
#
# For example:
#
# warehouse = [[ 1, 2, 3],
#              [ 0, 0, 0],
#              [ 0, 0, 0]]
# dropzone = [2,0]
# todo = [2, 1]
#
# The robot starts at the dropzone.
# The dropzone can be in any free corner of the warehouse map.
# todo is a list of boxes to be picked up and delivered to the dropzone.
#
# Robot can move diagonally, but the cost of a diagonal move is 1.5.
# The cost of moving one step horizontally or vertically is 1.
# So if the dropzone is at [2, 0], the cost to deliver box number 2
# would be 5.

# To pick up a box, the robot has to move into the same cell as the box.
# When the robot picks up a box, that cell becomes passable (marked 0)
# The robot can pick up only one box at a time and once picked up
# it has to return the box to the dropzone by moving onto the dropzone cell.
# Once the robot has stepped on the dropzone, the box is taken away,
# and it is free to continue with its todo list.
# Tasks must be executed in the order that they are given in the todo list.
# You may assume that in all warehouse maps, all boxes are
# reachable from beginning (the robot is not boxed in).

# -------------------
# User Instructions
#
# Design a planner (any kind you like, so long as it works!)
# in a function named plan() that takes as input three parameters:
# warehouse, dropzone, and todo. See parameter info below.
#
# Your function should RETURN the final, accumulated cost to do
# all tasks in the todo list in the given order, which should
# match with our answer. You may include print statements to show
# the optimum path, but that will have no effect on grading.
#
# Your solution must work for a variety of warehouse layouts and
# any length of todo list.
#
# Add your code at line 76.
#
# --------------------
# Parameter Info
#
# warehouse - a grid of values, where 0 means that the cell is passable,
# and a number 1 <= n <= 99 means that box n is located at that cell.
# dropzone - determines the robot's start location and the place to return boxes
# todo - list of tasks, containing box numbers that have to be picked up
#
# --------------------
# Testing
#
# You may use our test function below, solution_check(),
# to test your code for a variety of input parameters.

warehouse = [[1, 2, 3],
             [0, 0, 0],
             [0, 0, 0]]
dropzone = [2, 0]
todo = [2, 1]


delta = [[[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]],  # go right
         [[1, 1],   #down right
          [1, -1],   #down left
          [-1, 1],   #up right
          [-1, -1]]] #up left

cost = [1, 1.5]

# ------------------------------------------
# Inputs:
#   grid - matrix with the world layout. 0 means empty space, 1 means obstacle
#   init - starting position
#   goal - destination
#   cost - first element is for horizontal and vertical movement. 2nd is for diagonal
# --------------------------------------------------
# Output:
#   return cost of the planned motion
# --------------------------------------------------
def search(grid, init, goal):
    grid_rows = len(grid)
    grid_cols = len(grid[0])
    open = [[0, init[0], init[1]]]
    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    aux_grid = [[grid[col][row] for row in range(len(grid[0]))] for col in range(len(grid))]
    # aux_grid = grid[:]              #auxiliary Grid that will have 2 on positions already visited
    aux_grid[init[0]][init[1]] = 2
    # print 'aux_grid:'
    # print_grid(aux_grid)
    path = []
    resign = False
    found = False
    count = 0
    goalCost = 0
    path_map = {}
    while not found and not resign:
        # selected_position position with lowest cost
        min_value = float("inf")
        selected = []               # position selected for expansion

        for i in range(len(open)):
            x = open[i][1]
            y = open[i][2]
            g = open[i][0]
            f = g
            if (min_value > f):
                min_value = f
                ind = i
                selected = open[i]

        del open[ind]
        x2 = selected[1]
        y2 = selected[2]
        g2 = selected[0]
        expand[x2][y2] = count
        count += 1

        # expand this postion
        for i in range(len(delta)):
            for j in range(len(delta[i])):
                x3 = x2 + delta[i][j][0]
                y3 = y2 + delta[i][j][1]
                g3 = g2 + cost[i]

                #check if whether position is possible (not out of bounds or inside obstacles)
                if(min((x3, y3)) >= 0 and x3 < grid_rows and y3 < grid_cols):
                    if(aux_grid[x3][y3] == 0):

                        #check whether it is at goal
                        if([x3, y3] == goal):
                            print 'Reached Goal!'
                            goalCost = g3
                            # print 'goalCost = ', goalCost
                            path = (g3, x3, y3)
                            expand[x3][y3] = count
                            found = True
                            path_map[(x3, y3)] = (x2, y2)
                        else:
                            #add next_position to the open_position
                            aux_grid[x3][y3] = 2
                            open.append((g3, x3, y3))
                            path_map[(x3, y3)] = (x2, y2)

        if(len(open) == 0 and not found):     # no more possible moves and not at goal
            path = 'fail'
            resign = True


    return goalCost

def print_grid(grid):
    grid_rows = len(grid)
    grid_cols = len(grid[0])
    for i in range(grid_rows):
        print grid[i]

# ------------------------------------------
# plan - Returns cost to take all boxes in the todo list to dropzone
#
# ----------------------------------------
# modify code below
# ----------------------------------------
def plan(warehouse, dropzone, todo):

    finalCost = 0
    warehouse[dropzone[0]][dropzone[1]] = 0
    # print 'warehouse:'
    # print_grid(warehouse)
    for i in range(len(todo)):
        # print todo[i]
        goal = []
        end = False
        for j in range(len(warehouse)):
            for k in range(len(warehouse[0])):
                # print '(j,k) = ', (j, k), warehouse[j][k]
                if todo[i] == warehouse[j][k]:
                    goal = [j, k]
                    # print 'goal = ', goal
                    end = True
                    break
            if(end):
                break
        warehouse[goal[0]][goal[1]] = 0
        finalCost += search(warehouse, dropzone, goal)
        # print 'Get Box\nFINALCOST = ', finalCost
        # print 'warehouse:'
        # print_grid(warehouse)
        finalCost += search(warehouse, goal, dropzone)
        # print 'Return to dropzone\nFINALCOST = ', finalCost

    return finalCost

################# TESTING ##################

# ------------------------------------------
# solution check - Checks your plan function using
# data from list called test[]. Uncomment the call
# to solution_check to test your code.
#
def solution_check(test, epsilon=0.00001):
    answer_list = []

    import time
    start = time.clock()
    correct_answers = 0
    for i in range(len(test[0])):
        user_cost = plan(test[0][i], test[1][i], test[2][i])
        true_cost = test[3][i]
        if abs(user_cost - true_cost) < epsilon:
            print "\nTest case", i + 1, "passed!"
            answer_list.append(1)
            correct_answers += 1
            # print "#############################################"
        else:
            print "\nTest case ", i + 1, "unsuccessful. Your answer ", user_cost, "was not within ", epsilon, "of ", true_cost
            answer_list.append(0)
    runtime = time.clock() - start
    if runtime > 1:
        print "Your code is too slow, try to optimize it! Running time was: ", runtime
        return False
    if correct_answers == len(answer_list):
        print "\nYou passed all test cases!"
        return True
    else:
        print "\nYou passed", correct_answers, "of", len(answer_list), "test cases. Try to get them all!"
        return False


# Testing environment
# Test Case 1
warehouse1 = [[1, 2, 3],
              [0, 0, 0],
              [0, 0, 0]]
dropzone1 = [2, 0]
todo1 = [2, 1]
true_cost1 = 9
# Test Case 2
warehouse2 = [[1, 2, 3, 4],
              [0, 0, 0, 0],
              [5, 6, 7, 0],
              ['x', 0, 0, 8]]
dropzone2 = [3, 0]
todo2 = [2, 5, 1]
true_cost2 = 21

# Test Case 3
warehouse3 = [[1, 2, 3, 4, 5, 6, 7],
              [0, 0, 0, 0, 0, 0, 0],
              [8, 9, 10, 11, 0, 0, 0],
              ['x', 0, 0, 0, 0, 0, 12]]
dropzone3 = [3, 0]
todo3 = [5, 10]
true_cost3 = 18

# Test Case 4
warehouse4 = [[1, 17, 5, 18, 9, 19, 13],
              [2, 0, 6, 0, 10, 0, 14],
              [3, 0, 7, 0, 11, 0, 15],
              [4, 0, 8, 0, 12, 0, 16],
              [0, 0, 0, 0, 0, 0, 'x']]
dropzone4 = [4, 6]
todo4 = [13, 11, 6, 17]
true_cost4 = 41

testing_suite = [[warehouse1, warehouse2, warehouse3, warehouse4],
                 [dropzone1, dropzone2, dropzone3, dropzone4],
                 [todo1, todo2, todo3, todo4],
                 [true_cost1, true_cost2, true_cost3, true_cost4]]


solution_check(testing_suite) #UNCOMMENT THIS LINE TO TEST YOUR CODE
