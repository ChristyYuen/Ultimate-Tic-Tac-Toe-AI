# Monte Carlo Tree Search for Ultimate Tic-Tac-Toe

## Introduction
This project implements a bot that plays Ultimate Tic-Tac-Toe using Monte Carlo Tree Search (MCTS). Ultimate Tic-Tac-Toe is a turn-based two-player game played on a grid of 9 tic-tac-toe boards, where players must complete a giant row, column, or diagonal. Each player's move influences which board their opponent must play on.

## Running the Game
1. To run the game interactively, use the following command (from the `/src` folder):
    ```bash
    python p3_play.py human human

2. Replace `human` with one of the bot names: `mcts_vanilla`, `mcts_modified`, `random_bot`, or `rollout_bot`.

3. For a simulation between bots without graphical rendering, run:
    ```bash
    python p3_sim.py PLAYER1 PLAYER2

## Code Overview
Main files in the project include:

- `p3_sim.py`: Simulator for running repeated matches between bots.
- `p3_play.py`: Interactive game version.
- `p3_t3.py`: Additional implementation for the Ultimate Tic-Tac-Toe game.
- `mcts_vanilla.py`: Implementation of the vanilla MCTS bot.
- `mcts_modified.py`: Improved MCTS bot with heuristic rollout strategy.
- `mcts_node.py`: Contains the MCTSNode class for managing the MCTS tree.
- `random_bot.py`: A bot that makes random moves.
- `rollout_bot.py`: A bot that uses a rollout strategy for decision-making.

## MCTS Functionality
- **traverse_nodes**: Selects a node based on the MCTS algorithm.
- **expand_leaf**: Adds a new leaf node to the tree.
- **rollout**: Simulates the remainder of the game randomly.
- **backpropagate**: Updates nodes in the tree based on simulation outcomes.
- **think**: Executes the MCTS algorithm to determine the best action.

## Experiments
- **Experiment 1 – Tree Size**: Test the vanilla MCTS bot against itself with varying tree sizes for analysis.
- **Experiment 2 – Heuristic Improvement**: Compare the modified MCTS against the vanilla version to evaluate heuristic effectiveness.

## License
This project is licensed under the MIT License.

