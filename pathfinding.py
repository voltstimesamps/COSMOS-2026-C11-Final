def discrete_cosine(direction):
    if direction == 2: # If east, go right
        return 1
    elif direction == 3: # If west, go left
        return -1
    # Otherwise do nothing
    return 0  

def discrete_sine(direction):
    if direction == 0: # If north, go up
        return -1
    elif direction == 1: # If south, go down
        return 1
    # Otherwise do nothing
    return 0  

# Return whether or not the point (x,y) is within bounds of the map 
def is_valid_pos(x,y):
    return 0 <= x < 5 and 0 <= y < 5 

# If a cell at p_0 is touching the cell at p_1, 
# return the direction p_1 is relative to p_0,
# otherwise return -1
def get_contact_direction(p_0, p_1):
    # 0 North
    # 1 South
    # 2 East
    # 3 West
    for direction in range(4):
        if p_0[0] + discrete_cosine(direction) != p_1[0]:
            continue
        if p_0[1] + discrete_sine(direction) == p_1[1]:
            return direction 
    return -1

# Pathfinding function between p_start and p_goal
# Expand outwards from starting position until the goal position 
# has been hit. If the goal position is never hit, there is 
# no valid path between it and the start position.
def get_path(p_start, p_goal, obstacle_grid):
    # Swap start and goal positions to allow backtracking algorithm
    # to return proper directions that the robot must move in
    temp = p_goal
    p_goal = p_start
    p_start = temp

    # Initialize list of already explored nodes
    total_explored = [p_start]

    # Initialize list of nodes explored on each_epocb
    explored = [[p_start]]

    # Initialize list of farthest out nodes
    outer_nodes = [p_start]

    # Check all possible offshoots until a dead-end is hit on every offshoot
    while True: 
        # Store list of the temporary farthest out nodes
        temp_outer_nodes = []
        # Check possible offshoots of every outer node
        for node in outer_nodes:
            # 0 North
            # 1 South
            # 2 East
            # 3 West
            # Check the cell above, below, right of, and left of the current cell
            for direction in range(4): 
                new_x = node[0] + discrete_cosine(direction) 
                new_y = node[1] + discrete_sine(direction)

                # If the new position is within the bounds of the map,
                # and there is no obstacle at that position,
                # and the position has not already been explored,
                # add the current position to the latest list of outer nodes
                if is_valid_pos(new_x, new_y)\
                    and obstacle_grid[new_x][new_y] == 0\
                    and ((new_x,new_y) not in total_explored):
                    temp_outer_nodes.append((new_x,new_y)) 

        # If there are no outer nodes past the current outer nodes,
        # the pathfinder has hit a dead end at every tree ending
        if len(temp_outer_nodes) == 0:
            return None

        # If the goal position is in the latest list
        # of outer nodes, stop pathfinding
        if p_goal in temp_outer_nodes: 
            break 
        else:
            total_explored += temp_outer_nodes
            explored.append(temp_outer_nodes)
            outer_nodes = temp_outer_nodes

    # Backtrack

    # Initalize list of directions that the robot must move in
    directions = []
    # Initialize current point to backtrack from finish to start position 
    current_point = p_goal

    # Traverse backwards through list of explored nodes
    for i in range(len(explored)-1, -1, -1):
        # Load all points that were checked on iteration i
        next_check_points = explored[i]

        # For each point P that was checked on iteration i,
        # search for the parent node by checking 
        # if the current point Q is touching P
        # and the direction P is relative to Q.
        # Then, update the current point to be P
        for point in next_check_points:    
            contact_direction = get_contact_direction(current_point, point)
            # If touching, append the direction the checked 
            # point P is at relative to the current point Q
            if contact_direction > -1:
                current_point = point
                directions.append(contact_direction)
                # Stop checking other points at this iteration
                # after the parent point is found
                break 
    
    return directions