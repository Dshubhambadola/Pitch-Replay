# Football Race Replay ⚽️🏁

A Python-based football match replay visualization system, inspired by F1 Race Replay tools. This application renders tracking data from StatsBomb on a tactical 2D pitch, complete with player movements, event visualizations (passes, shots), and dynamic formation shapes.

![Tactical View](https://raw.githubusercontent.com/statsbomb/open-data/master/img/statsbomb-logo.png) (StatsBomb Data)

## ✨ Features

- **Tactical 2D Replay**: Overhead view of all 22 players + ball.
- **"Tactical Pro" Theme**: High-contrast Dark Mode with Neon Teal/Pink accents.
- **Event Visualization**:
    - **Passes**: Visualization of pass trajectories with direction arrows.
    - **Shots**: Star markers indicating shot locations with **xG** (Expected Goals).
- **Dynamic Team Shapes**: Real-time Convex Hulls showing team formations.
- **Data Source**: Uses [StatsBomb Open Data](https://github.com/statsbomb/open-data) (free).

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/football-race-replay.git
    cd football-race-replay
    ```

2.  **Install dependencies**:
    ```bash
    pip3 install -r requirements.txt
    ```

### Running the Replay

You can run the application directly:

```bash
./run.sh
```

Or manually:

```bash
./main.py
```

*The application defaults to the Argentina vs France World Cup Final (or another available match in the free dataset).*

## 🎮 Controls

- **Spacebar**: Play / Pause animation.
- **Close Window**: Exit application.

## 🛠 Project Structure

- `data/`: Handles data fetching (`loader.py`) and cleaning (`preprocessor.py`).
- `visualization/`:
    - `pitch.py`: Draws the football pitch using `mplsoccer`.
    - `players.py`: Renders players and formation shapes.
    - `events.py`: Renders pass arrows and shot markers.
- `utils/`: Configuration (`config.py`) and Theme (`theme.py`).
- `main.py`: Main entry point and animation loop.

## 📚 Tech Stack

- **[statsbombpy](https://github.com/statsbomb/statsbombpy)**: Data loading.
- **[mplsoccer](https://github.com/andrewRowlinson/mplsoccer)**: Professional pitch plotting.
- **[matplotlib](https://matplotlib.org/)**: Animation engine.
- **[pandas](https://pandas.pydata.org/)**: Data manipulation.
- **[scipy](https://scipy.org/)**: Spatial computations (Convex Hulls).

## 📄 License

This project uses StatsBomb Open Data.
*StatsBomb Open Data is licensed under its own terms. Please verify usage rights for commercial applications.*
