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

---

## 🚀 Usage

You can either:

- **Double-click the executable file**  
  *(Created using `pyinstaller`)*

**OR**

- **Run `main.py`** from your terminal or code editor :

  ```bash
  python main.py

---

## 👾 Gameplay

### 🎯 Objective

Your goal is to **reach and complete the final level** to win the game. Each level increases in difficulty and brings new challenges.

### 👻 Enemies

Throughout the game, you’ll encounter **various ghosts** that you must defeat.  
Be careful — if you're killed, you'll have to **restart the game from the beginning**.

### ❤️ Health Tip

Running low on health?  
Keep an eye out for **potion jars** placed throughout the levels.  
Collecting them will **restore your health** and improve your chances of survival.

---

## 🕹️ Controls

| Action            | Key(s)               |
|-------------------|----------------------|
| Move Left         | ← Arrow or `A`       |
| Move Right        | → Arrow or `D`       |
| Jump              | ↑ Arrow or `W`       |
| Throw Grenade     | `G`                  |
| Exit Game         | `ESC`                |

---

## 🛠️ Level Editor

You can access the level editor in two ways:

- Click on **Level Editor** from the main menu.
- Run `level_editor.py` or `level_editor.exe`.


### 🧩 Editor Features & Tips

- Starts with **Level 4 by default** to avoid accidental edits of existing levels.
- The **blank tile** in the sprite selector acts as an **eraser**.
- To load an existing level's map:
  - Use the `<-` and `->` buttons at the bottom right.
  - Select the desired level and press **LOAD**.
- Saving will **overwrite** the selected level's map.
- Use **arrow keys** to scroll along the map.
- Once done with designing, press **SAVE**.

### ▶️ Play Your Custom Level

To play the level you just created:

1. Open `main.py` in a code editor.
2. Change the `level` parameter to your new level number.
3. (Optional) Add your level to the queue by updating the `MAX_LEVEL` parameter accordingly.

---

## ⚠️ Important Notes

- Make sure you have the **latest version of Python** installed on your system.
- `pip` is usually included with Python and is required to install modules.
- The game requires the **`pygame` module**, which can be installed using :

  ```bash
  pip install pygame
- Ensure that all files and assets are placed in their correct relative paths.
- To create your own levels, use **`level_editor.exe`**.
- The leaderboard only records completed runs (all 3 levels by default).

---

## 🤝 Contribution

If you'd like to contribute to this project voluntarily,  
please check out the [CONTRIBUTING.md](https://github.com/WhiteJadeWolf/Ghostbusters/blob/main/CONTRIBUTING.md) file for guidelines.

---

## 🙏 Thanks

Thank you for checking out my small project. ❤️
**Hope you enjoy the game!** 🎉

---
