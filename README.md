# 👻 GhostBusters

**GhostBusters** is a small platformer game made with **Pygame**.  
The game features **tile-based physics**, **smooth scrolling**, and **parallax animations** for a retro-style gaming experience.

---

## 🎮 How to Play?

Just **double-click** the executable file to launch the game!  
> *(The `.exe` was created using `pyinstaller` — special thanks to **CODE WITH RUSS** for his helpful video on the topic.)*

---

## 📦 Requirements

- Install the latest version of [Python](https://www.python.org/downloads/) in your system along with pip3
- Install the `pygame` module by running :

  ```bash
  pip install pygame

## 🚀 Usage

You can either:

- **Double-click the executable file**  
  *(Created using `pyinstaller`)*

**OR**

- **Run `main.py`** from your terminal or code editor :

  ```bash
  python main.py
The objective of the game is to reach and clear the final level in order to win the game. 
In the way you'll encounter several ghosts who you have to kill and remember don't get killed otherwise you have to start the game from the beginning. 
If less on health find potion jars to get some health.

## Controls

* Left arrow key or A to go left
* Right arrow key or D to go right
* Up arrow key or W to jump
* G to throw grenade
* press ESC to escape the game

## Level Editor

* To open the level editor, you can click on the Level Editor option in main menu. Alternatively, you can run level_editor.py in the main folder or run 'level_editor.exe' file.
* By default, level editor starts with level 4 so that accidental edits of existing levels are avoided.
* The blank space in sprite selector is the eraser -- so use it accordingly.
* If you want to load an existing level's map, use <- -> buttons on the bottom right to select the level and then press 'LOAD'.
* Saving existing levels with new level designs will replace the old one.
* To scroll along the map, use arrow keys.
* Once you are done with the level design, you can save it. To play the level, open main.py with any code editor and change 'level' parameter to the corresponding level where you saved it. Also, you can add it to the queue of existing levels by following the order of levels and changing 'MAX_LEVEL' parameter accordingly.


## NOTE :--

* Please install the latest python version in your system before running the game. (pip is automatically installled)
* pygame module is required to run the game. pip is required to install the module.
* Make sure all files and assets are properly installed in required relative paths.
* If you want to create your own levels, run 'level_editor.exe'
* Leaderboard in the game will only be updated with the records of the games (all 3 levels, by default) you have won.

## CHECK CONTRIBUTION.md FILE FOR ANY VOLUNTARY CONTRIBUTION OFFER.
## THANK YOU FOR TRYING OUT MY SMALL PROJECT. HOPE YOU LIKE IT :
