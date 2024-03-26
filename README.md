# Connect4 Game AI

Connect4 game implemented in Python, where players can compete against an optimized AI agent. The game utilizes the Minimax algorithm to provide a challenging opponent.

## Game Rules

### Board Size
The board size can be any size with a width of 7 or greater and a height of 6.

### Evaluation
Players earn points based on the number of connected pieces in the same row, column, or diagonals. The player with the higher score wins the game.

### Example:
A sequence like `1,1,1,1,1,1,1` is considered as 3 points for player 1.

### Valid Move
Players can choose any column on the board, but it's only legal if the column isn't already full.

### Termination
The game terminates when there are no more available spaces on the board.

## GUI

A sample user interface using pygame allows players to interact with the game. Players can hover over columns to select their move and click to drop their piece. The AI responds shortly after, and the game continues until the board is full. The GUI also displays the scores for the AI agent and the human player, along with corresponding Minimax trees for each move.

## AI Agent

The AI agent is optimized to maximize its score and win the game. It utilizes the Minimax algorithm with different variations:

- Normal Minimax
- Pruning Minimax
- Expectation Minimax

### Scoring
To determine the best move, the AI agent considers:

- Number of connected pieces: 4 connected pieces yield the highest score.
- Weighted center: Pieces placed at the center of the board are given higher scores.

## Conclusion

Through experimentation, we compared the performance of different Minimax approaches at various depths (K values). Here's a summary:

- Normal Minimax: The least efficient as it checks losing moves unnecessarily.
- Pruning Minimax: An improvement over normal Minimax due to its pruning process.
- Expectation Minimax: Slightly better than Pruning Minimax.

## Video


The video's speed got *6 so the video can be uploaded

























https://github.com/Mohamedragih1/Connect-Four-AI/assets/93843532/62d8a915-fabd-4455-b260-08d572305033






