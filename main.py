import json
import os
import random
import tkinter as tk
from tkinter import messagebox


def load_story(json_path: str) -> dict:
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


class AdventureGame:
    """A class encapsulating the adventure game logic and GUI."""

    def __init__(self, story_path: str) -> None:
        self.story = load_story(story_path)
        self.current_node_id = self.story.get('start', '')
        self.flags: dict[str, bool] = {'sneaked': False}

        #Tkinter window.
        self.root = tk.Tk()
        self.root.title("The Goblin King's Ransom")
        self.text_var = tk.StringVar() # text to display
        self.text_label = tk.Label(
            self.root,
            textvariable=self.text_var,
            wraplength=480,
            justify='left',
            padx=10,
            pady=10,
            anchor='w'
        )
        self.text_label.pack(padx=10, pady=10, fill='x')
        # option buttons.
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(padx=10, pady=10, fill='x')

        # Initialize display
        self.update_display()

    #Roll d6
    def roll_dice(self) -> int:
        return random.randint(1, 6)

    def handle_option(self, option: dict) -> None:
        action = option.get('action')
        threshold = option.get('threshold', 0)
        fail_target = option.get('fail_target')
        target = option.get('target')

        # Assume no dice roll is needed by default.
        next_node_id = target

        if action in {'stealth', 'strength', 'combat', 'challenge'}:
            roll = self.roll_dice()
            if action == 'stealth':
                # Stealth check
                success = roll >= threshold
                if success:
                    self.flags['sneaked'] = True
                    next_node_id = target
                else:
                    # Fail stealth
                    next_node_id = fail_target or target
                messagebox.showinfo(
                    'Stealth Check',
                    f'You rolled a {roll}.\n' +
                    ('Your stealth was successful!' if success else 'You stumbled and made noise!')
                )
            elif action == 'strength':
                # Strength check
                success = roll >= threshold
                next_node_id = target if success else (fail_target or target)
                messagebox.showinfo(
                    'Strength Check',
                    f'You rolled a {roll}.\n' +
                    ('You muscled your way through!' if success else 'The rubble proved too tough!')
                )
            elif action == 'combat':
                success = roll >= threshold
                next_node_id = target if success else (fail_target or target)
                messagebox.showinfo(
                    'Combat Roll',
                    f'You rolled a {roll}.\n' +
                    ('You vanquished the Bone Goblin Champion!' if success else 'You were defeated by the Champion!')
                )
            elif action == 'challenge':
                # Challenge roll against Goblin King.
                success = roll >= threshold
                messagebox.showinfo(
                    'Challenge Roll',
                    f'You rolled a {roll}.\n'
                    f'Target to win is {threshold}.\n'
                    + ('A lucky strike! You win the duel.' if success else 'Your swing misses. You lose the duel.')
                )
                # On success, go to node 9. On failure go to fail_target or node 13.
                next_node_id = '9' if success else (fail_target or '13')
        self.current_node_id = str(next_node_id)
        self.update_display()

    def update_display(self) -> None:
        node = self.story['nodes'][self.current_node_id]
        self.text_var.set(node.get('text', ''))
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        options = node.get('options', [])
        available_options: list[dict] = []
        for opt in options:
            requires = opt.get('requires', {})
            meets_reqs = True
            for key, val in requires.items():
                if self.flags.get(key) != val:
                    meets_reqs = False
                    break
            if meets_reqs:
                available_options.append(opt)
        if not available_options:
            restart_btn = tk.Button(
                self.buttons_frame,
                text='Restart',
                command=self.restart_game
            )
            restart_btn.pack(pady=10)
        else:
            # Create button
            for opt in available_options:
                btn = tk.Button(
                    self.buttons_frame,
                    text=opt.get('text', ''),
                    wraplength=480,
                    justify='left',
                    command=lambda o=opt: self.handle_option(o)
                )
                btn.pack(fill='x', pady=5)

    def restart_game(self) -> None:
        self.current_node_id = self.story.get('start', '')
        # Reset all flags
        self.flags = {'sneaked': False}
        self.update_display()

    def run(self) -> None:
        """Start the Tkinter main event loop."""
        self.root.mainloop()


def main() -> None:
    # Determine the path to story.json relative to this script.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    story_file = os.path.join(script_dir, 'story.json')
    # Error check
    if not os.path.exists(story_file):
        raise FileNotFoundError(f"Could not find story.json at {story_file}")
    # Run game
    game = AdventureGame(story_file)
    game.run()


if __name__ == '__main__':
    main()