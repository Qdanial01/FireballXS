# 🔥 FireballXS
A micro Dungeons-and-Dragons style interactive story game rendered through a lightweight Python GUI

## 🛠️ Technology
- `Python`
- `tkinter`
- `twine`
- `json`
- `html`

## 🚀 Features
- **Dice-based encounters** - just like a D&D game, dice rolls are simulated through a random number generator for checks such as stealth, strength and combat
- **Branching Narrative** - being a fully text game, players would choose what they would do, and each action would branch the story out to a different outcome, with certain options only available after a condition is met.

## 🧠 The Process
I started by creating a short and simple narrative in Twine. The app’s flowchart view gives a clear view of how the branching story would look from start to finish. Once I had the story laid out, I exported the work as an HTML file and began converting it to structured JSON data. The JSON file would then have the same story that was written in Twine, but this time contain data such as options, actions, minimum threshold of each dice roll and requirements. Using Python, I then began to add the dice roll mechanics, win and lose states and conditional choices before tkinter to build the GUI

## 📦 Running the Project
1. Clone or download the repository
2. Make sure Python is installed on your machine
3. Run in terminal/command prompt: python Number_Guess_Game.py

## 🖼️ Preview
<img width="688" height="376" alt="Image" src="https://github.com/user-attachments/assets/ab23af89-53bd-4cef-88b7-5968d7461642" />
