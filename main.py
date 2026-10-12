#!/usr/bin/env python3
"""Simple choose-your-own-adventure CLI game.

A lightweight MVP for a GitHub Copilot challenge.
"""

from __future__ import annotations

from typing import Dict, List


class GameState:
    def __init__(self) -> None:
        self.inventory: List[str] = []
        self.story_path: List[str] = []

    def add_item(self, item: str) -> None:
        if item not in self.inventory:
            self.inventory.append(item)

    def has_item(self, item: str) -> bool:
        return item in self.inventory


SCENES: Dict[str, Dict[str, object]] = {
    "start": {
        "title": "Moonlit Crossing",
        "text": (
            "The wind carries whispers through the old forest. A glowing lantern\n"
            "hangs by a ruined gate, and a narrow path leads deeper into the dark.\n"
            "Behind you, the village lights fade away. Ahead, something waits."
        ),
        "choices": [
            {"label": "Follow the lantern glow into the Whispering Woods", "next": "woods"},
            {"label": "Walk toward the stone ruins on the hill", "next": "ruins"},
        ],
    },
    "woods": {
        "title": "Whispering Woods",
        "text": (
            "The trees lean close as if listening. A small satchel is caught on a\n"
            "thorn bush. Inside is a brass key and a folded map of the ruined shrine."
        ),
        "choices": [
            {
                "label": "Take the brass key and map",
                "next": "cave",
                "gain_item": "brass key",
                "gain_item_2": "map",
            },
            {"label": "Ignore the satchel and keep moving", "next": "cave"},
        ],
    },
    "ruins": {
        "title": "Old Stone Ruins",
        "text": (
            "The ruins are quiet, but you notice a cracked door with strange metal marks.\n"
            "A faint humming sound comes from inside."
        ),
        "choices": [
            {"label": "Open the door and enter", "next": "shrine"},
            {"label": "Climb down to the cave beneath the ruins", "next": "cave"},
        ],
    },
    "cave": {
        "title": "Moonlit Cave",
        "text": (
            "A wide cave opens before you, lit by a glowing crystal suspended from the ceiling.\n"
            "A deep voice echoes, 'Only the worthy may claim the light.'"
        ),
        "choices": [
            {"label": "Touch the crystal", "next": "ending_hero", "required_item": "brass key"},
            {"label": "Try to take the crystal without permission", "next": "ending_trap"},
            {"label": "Leave the cave and head for the shrine", "next": "shrine"},
        ],
    },
    "shrine": {
        "title": "Forgotten Shrine",
        "text": (
            "The shrine door creaks open. Inside, a stone statue watches over a basin of\n"
            "water and a silver charm hanging from the altar."
        ),
        "choices": [
            {"label": "Take the silver charm", "next": "ending_wealth", "gain_item": "silver charm"},
            {"label": "Listen to the statue and speak a promise", "next": "ending_guardian", "required_item": "map"},
            {"label": "Leave the shrine and run home", "next": "ending_lost"},
        ],
    },
    "ending_hero": {
        "title": "Ending: Keeper of the Light",
        "text": (
            "You unlock the crystal with the brass key. The cave fills with warm light,\n"
            "and the whispers become a song. The forest is no longer dark.\n"
            "You become the keeper of the moonlit path."
        ),
        "ending": True,
    },
    "ending_trap": {
        "title": "Ending: The Price of Greed",
        "text": (
            "The crystal shatters in your hands, and the cave collapses in a burst of cold light.\n"
            "The forest swallows your footsteps, and the path is lost forever."
        ),
        "ending": True,
    },
    "ending_wealth": {
        "title": "Ending: The Golden Curse",
        "text": (
            "The silver charm gleams brighter than any treasure you have ever seen.\n"
            "But as the shrine fades, you realize the charm is a trap that steals\n"
            "your name and leaves you chasing wealth forever."
        ),
        "ending": True,
    },
    "ending_guardian": {
        "title": "Ending: Guardian of the Forest",
        "text": (
            "You speak the promise and show the map of the shrine. The statue turns to life,\n"
            "accepting you as its guardian. The forest is protected, and your story becomes a legend."
        ),
        "ending": True,
    },
    "ending_lost": {
        "title": "Ending: Lost in the Mist",
        "text": (
            "You leave the shrine too soon. The path behind you disappears into fog,\n"
            "and the forest keeps your name in silence. You are never seen again."
        ),
        "ending": True,
    },
}


def show_intro() -> None:
    print("=" * 60)
    print("WELCOME TO THE MOONLIT CROSSING")
    print("A choose-your-own-adventure game")
    print("=" * 60)
    print("Your journey begins in a forest where old stories still whisper.")
    print("Make choices, collect items, and discover your ending.")


def show_inventory(state: GameState) -> None:
    if state.inventory:
        print("\nInventory:", ", ".join(state.inventory))
    else:
        print("\nInventory: empty")


def get_choice(scene: Dict[str, object]) -> int:
    choices = scene["choices"]
    while True:
        try:
            raw_choice = input("\nChoose an option (1-{}): ".format(len(choices)))
            choice_index = int(raw_choice)
            if 1 <= choice_index <= len(choices):
                return choice_index
            print("Please enter a valid number.")
        except ValueError:
            print("Please enter a number.")


def handle_choice(state: GameState, scene_name: str, choice_index: int) -> str:
    scene = SCENES[scene_name]
    choice = scene["choices"][choice_index - 1]
    next_scene = str(choice["next"])

    if "gain_item" in choice:
        state.add_item(str(choice["gain_item"]))
    if "gain_item_2" in choice:
        state.add_item(str(choice["gain_item_2"]))

    if "required_item" in choice and not state.has_item(str(choice["required_item"])):
        print(f"You need the '{choice['required_item']}' before you can do that.")
        print("The path closes, and you are forced to reconsider your next step.")
        return scene_name

    state.story_path.append(next_scene)
    return next_scene


def play_game() -> None:
    state = GameState()
    show_intro()

    current_scene = "start"

    while True:
        scene = SCENES[current_scene]
        print("\n" + "=" * 60)
        print(f"Scene: {scene['title']}")
        print(scene["text"])
        show_inventory(state)

        if scene.get("ending"):
            print("\nThanks for playing.")
            break

        for i, choice in enumerate(scene["choices"], start=1):
            print(f"{i}. {choice['label']}")

        choice_index = get_choice(scene)
        next_scene = handle_choice(state, current_scene, choice_index)
        if next_scene == current_scene:
            continue
        current_scene = next_scene


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Farewell.")
