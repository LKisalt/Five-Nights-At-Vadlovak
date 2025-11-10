# Five Nights at Freddy's - Custom Edition

A custom FNAF-like game using your house and friends' PNG images.

## Setup

1. Install Python 3.x
2. Install Pygame: `pip install pygame`
3. Replace placeholder PNG files in `assets/` with your actual images:
   - `office.png`: Your house/office image
   - `camera.png`: Camera view image (another house/friends image)
   - `animatronic1.png`: First friend's image
   - `animatronic2.png`: Second friend's image

## How to Play

- Press 'C' to switch to camera view
- Press 'O' to switch back to office
- Survive 5 hours without getting caught by the animatronics
- Manage your power carefully

## Controls

- C: Camera view
- O: Office view
- X: Left door (open/close)
- V: Right door (open/close)
- Q: Left light
- E: Right light

## Game Mechanics

- Animatronics move based on AI levels
- Power drains over time
- Survive until 6 AM

## Development

The game is built with Pygame. Main game logic is in `main.py`.

To run: `python main.py`