
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log, inf

num_nodes = 800
explore_faction = 2.

def math_of_UTC(node):
    #if node.visits == 0:
    #    return inf
    return (node.wins / node.visits) + (explore_faction * sqrt(log(node.parent.visits)/node.visits) )
def one_math_of_UTC(node):
    #if node.visits == 0:
    #    return -inf
    return (1 - (node.wins / node.visits)) + (explore_faction * sqrt(log(node.parent.visits)/node.visits) ) # THERE'S GOTTA BE A SMARTER WAY TO DO THIS

def traverse_nodes(root_node, board, root_state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    node = root_node
    state = root_state

    while node.child_nodes:
        if len(node.untried_actions) != 0:
            return node, state

        selection = {} # a.k.a. ‘selection’; navigates the tree node. Dictionary for tuples
        child_moves = node.child_nodes.keys() 

        for move in child_moves:
            #do math
            curr_child_state = board.next_state(state, move)

            curr_child_node = node.child_nodes[move]

            if board.current_player(state) == identity:
                temp = math_of_UTC(curr_child_node) # UTC math
            else:
                temp = one_math_of_UTC(curr_child_node)
            selection[temp] = (curr_child_node, move, curr_child_state)

        max_node = max(selection.keys()) #Brain fart, smth here)

        node = selection[max_node][0] #SHOULD UPDATE TO THE LAST NODE EACH TIME
        state = selection[max_node][2]
    return node, state

    #pass
    # Hint: return leaf_node


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node. & associated state

    """
    pop_node = node.untried_actions.pop(0)

    new_state = board.next_state(state, pop_node)

    action_list = board.legal_actions(new_state)     

    new_node = MCTSNode(node, pop_node, action_list)

    node.child_nodes[pop_node] = new_node
    
    return new_node, new_state
    #pass
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.
    Returns:
        win: the Win dictionary for the finished rollout
    """
    moves_done = []


    rollout_state = state
    while board.is_ended(rollout_state) != True:
        possibleActions = board.legal_actions(rollout_state)
        actionWeights = {}
        count = 0
        while count <= 3:
            action = choice(possibleActions)
            actionWeight = 0
            actionMacro = (action[0], action[1])
            actionMicro = (action[2], action[3])
            hypotheticalState = board.next_state(rollout_state, action)
            if board.owned_boxes(rollout_state)[actionMacro] != board.owned_boxes(hypotheticalState)[actionMacro]:
                actionWeight += 6
            else:
                if actionMicro == (1,1):
                    actionWeight += 2
                if actionMicro == (0,0) or actionMicro == (0,2) or actionMicro == (2,0) or actionMicro == (2,2):
                    actionWeight += 1
            if actionMacro == (1,1):
                actionWeight += 4
            if actionMacro == (0,0) or actionMacro == (0,2) or actionMacro == (2,0) or actionMacro == (2,2):
                actionWeight += 3
            count += 1
        actionWeights[actionWeight] = action  

        best_action = max(actionWeights.keys())
    
        rollout_move = actionWeights[best_action] 
        rollout_state = board.next_state(rollout_state, rollout_move)
        moves_done.append(rollout_move)

    win = board.points_values(rollout_state)
    return win


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """

    #if node is root return
    if node.parent == None:
        node.visits += 1
        return
    #do update stats in node
    node.visits += 1
    node.wins += won

    backpropagate(node.parent, won)
    return


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        childToExplore, stateToExplore = traverse_nodes(node, board, sampled_game, identity_of_bot)

        if board.is_ended(stateToExplore) == True:
            win = board.points_values(stateToExplore)[identity_of_bot]
            backpropagate(childToExplore, win)
        else:  
            newActionNode, newActionState = expand_leaf(childToExplore, board, stateToExplore)

            winDict = rollout(board, newActionState)

            winCount = winDict[identity_of_bot]

            backpropagate(newActionNode, winCount)

        #if step % 100 == 0:
        #    print("Finished step ", step)

        # Do MCTS - This is all you!

    selection = {} # a.k.a. ‘selection’; navigates the tree node. Dictionary for tuples
    childrenMoves = root_node.child_nodes.keys()

    for childMove in childrenMoves:
        #do math
        curr_child_state = board.next_state(state, childMove)
        if board.is_ended(curr_child_state):
            winValue = board.win_values(curr_child_state)
            if winValue[identity_of_bot] == 1:
                return childMove
        child = root_node.child_nodes[childMove]

        temp = child.wins / child.visits

        selection[temp] = (child, child.parent_action)

    max_node = max(selection.keys()) #Brain fart, smth here)
    
    selected_action = selection[max_node][1] 
    #del selection[max_node]

    #max_node = max(selection.keys())
    #second_choice = selection[max_node][1]
    #del selection[max_node]

    #max_node = max(selection.keys())
    #third_choice = selection[max_node][1]
    #del selection[max_node]

    #print("Top 3 choices")
    #print(selected_action)
    #print(second_choice)
    #print(third_choice)

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return selected_action
