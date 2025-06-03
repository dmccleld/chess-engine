# ♟️ Python Chess Engine

A simple yet feature-rich Python chess engine supporting human vs. AI or AI vs. AI matches. Designed for educational purposes, strategic experimentation, and fun.

---

## 🚀 Features

- Full implementation of standard chess rules
- Smart AI using:
  - Minimax with alpha-beta pruning
  - Quiescence search for better evaluation
  - Positional scoring based on endgame heuristics
- Player-selectable AI or human control
- Board cloning and FEN export for debugging
- En passant, castling, and promotion support
- Terminal-based interface

---

## 🧠 AI Overview

The AI uses classical search techniques enhanced with:

- **Opening Book**: Hardcoded early-game strategy
- **Board Evaluation**: Based on piece values and position-specific tables
- **Endgame Detection**: Switches to endgame heuristics when material is low

AI move selection:
```python
select_move(board, depth=2)
```
---
## 🛠️ How to Run

1. Clone the Repository

```bash
git clone https://github.com/yourusername/chess-engine.git
cd chess-engine
```

2. Run the Game
```bash
python main.py
```
You'll be prompted to choose whether each player is human or AI.

## 📂 Project Structure
```text
├── AI.py                # AI logic with minimax, pruning, quiescence
├── Cell.py              # Cell container for board squares
├── ChessBoard.py        # Board class with rules and mechanics
├── GameController.py    # Game loop and user interface
├── main.py              # Entry point
├── Pieces.py            # Piece types and movement validation
├── positional_data.py   # Positional scoring tables
├── tests.py             # Board cloning test
├── Utils.py             # Helpers like coordinate conversion
```

## 🧪 Testing
Basic functionality test for cloning:
```bash
python tests.py
```

## 🤝 Contributing
Pull requests and forks are welcome! If you spot a bug or want to add a feature, open an issue or PR.

## 📜 License
MIT License. See LICENSE for details.