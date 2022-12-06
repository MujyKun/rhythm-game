# rhythm-game
A rhythm game created for the CSCI-437 final project.

## Installation / Local Setup
1) Clone the repository ``git clone https://github.com/MujyKun/rhythm-game.git``
2) Go to the repo directory ``cd rhythm-game``
3) Running with Python ^3.9 is recommended. 
4) Install requirements with either 
   1) ``pip install -r requirements.txt`` 
      1) If you do not have pip, you can install it with ``python get-pip.py`` or ``python -m ensurepip --upgrade``
   2) If you have poetry you can use ``poetry install``.  
5) Start the program with `python main.py` or `poetry run python main.py` 

## How To Play
After running the game, press `L` to start the song you have generated. 
You can either use the player controls (W,A,S,D) to move the player around and collect the tiles at the beat zone, or you can 
use the arrow keys (represented on the beat zones) on your keyboard to precisely time a falling tile on the beat zone. 
If a falling tile goes past the beat zone (you miss), it will decrease your accuracy and player's health. 
If your player health goes under 0, you lose the game, and you can start over by pressing `L`. Win the game by making it to the end!

## General/Optional Features
   - Frames Per Second (By default capped to 30 FPS)
     - FPS Counter follows camera and is pinned to the top left.
   - Expandable Canvas
     - Can go outside base resolution.
     - Dynamic Resolution 
       - All sprites are customizable to the window resolution (Including the Camera, Background, and Player)
   - Camera Implementation
     - Can Zoom In/Out with the `-` or `+` keys.
     - Scrollable Camera (Will follow a player that leaves the camera boundaries)
   - Player Types
     - Can create a folder in [player](assets/player) to generate a type.
     - Can animate by unpacking a sprite-sheet and placing the animation type in a new directory.  
   - Player Movement
     - Set Vertical Movement (Keys defaulted to `W` & `S`)
     - Set Horizontal Movement (Keys defaulted to `A` & `D`)
     - Set Jump Movement (Key defaulted to `Spacebar`)
       - Optional Implementation to allow several jumps at a time. 
       - Currently set to only allow jumping while on a floor.
     - Camera Restrictions - Can choose whether the player can move outside the camera range.
     - Gravity (This has only been implemented for the player)
       - Implementations for both Moon and Earth gravity.
   - Background
     - Can be animated or an individual image.
     - Animated backgrounds should go [here](assets/background)
   - Music Tiles
     - Images can be found [here](assets/tiles)
     - Audio can be found [here](assets/notes)
   - Songs
     - Songs can be generated and loaded using JSON.
     - A song should be saved [here](assets)
     - A song should follow the following format: 
     - ```json
       {
       "song": {
          "name": "Test Song",
          "tiles": { 
              "10": ["C#3" , "C#3"],
              "20": ["C#3", "C#3"],
              "30": ["C#3", "C#3"],
              "40": ["C#3", "C#3"],
              "50": ["C#3", "d#3"],
              "60": ["C#3", "d#3"],
              "70": ["C#3", "d#3"],
              "80": ["C#3", "d#3"],
              "90": ["C#3", "d#3"],
              "100": ["C3", "G#3"],
              "110": ["C3", "G#3"],
              "120": ["C3", "G#3"],
              "130": ["C3", "G#3"],
              "140": ["C3", "F3"]
          }
        }
       }
       ```
        - The name is the song name.
        - The tile key consists of the beat number.
        - The tile value consists of the notes played at that specific beat.
        - The limit to the number of notes played on a single beat is dependent on:
          - The number of audio channels present.
          - The number of columns available in the game.
   - Holding Keys
     - Keys not released are stored in a list for continuous execution. 
     - Implemented more specifically for camera zooming.
   - Cursor Movement
     - Cursor Position follows the camera and is pinned to the top left (Below the FPS Counter).
   - Layering
     - Layering has been implemented into sprites so that sprites on top are consistent.


## Game Design Document
![Game Design Document](doc/rhythm_game_game_design.png)


## State Transition Diagram
![State Transition Diagram](doc/rhythm_game_fsm.svg)


## Game Engine
### [PursuedPyBear (ppb)](https://github.com/ppb/pursuedpybear) was used for this project.
   - Strengths
       - Built to be educational friendly.
       - Follows very similar design principles as our own game engines: Sprites, Scenes.
       - Easy to extend with adding new systems.
       - Easy to add events to be used with your own classes.
       - Camera splits up the screen into subsections, so allows the expansion of the canvas resolution.
       - The origin is the center of the screen, so it uses a more familiar quadrant system for positioning of Sprites.
       - Very easy to get started and create a simple example.
   - Weaknesses
       - Built to be educational friendly.
       - Does not officially support music.
       - Does not officially support getting a position within a sound that is playing.
       - The origin is the center of the screen, so can have negative x and y values.
       - The position variable of Sprite is not in pixels.
       - Camera splits up the screen and uses a pixel-ratio to render the screen.
       - Dependency issues with current version.
           - Supports PySDL2, but only supports pysdl2-dll version 2.0.20.
           - pysdl2-dll offers a newer SDLMixer that offers Music functionality.
       - Not enough examples to work with.
       - Unfamiliar to work with and allowed easy mess-ups.


## Example GIFs

### Different Player Types
![Different Players](doc/example_gifs/different_players.gif)

### Game Over
![Game Over](doc/example_gifs/game_over.gif)

### Game Win
![Game Win](doc/example_gifs/game_win.gif)

### "Earth" Gravity
![Earth Gravity](doc/example_gifs/earth_gravity.gif)

### "Moon" Gravity
![Moon Gravity](doc/example_gifs/moon_gravity.gif)

### Player Locked to Camera
![Player Camera Locked](doc/example_gifs/locked_to_camera.gif)

### Camera Following Player
![Camera Following Player](doc/example_gifs/scrollable_camera.gif)

### Camera Not Following Player
![Camera Not Following Player](doc/example_gifs/nonscrollable_camera.gif)

### Several Jumps
![Several Jumps](doc/example_gifs/several_jumps.gif)

## Contributions | Software Engineering Plan
### [@MujyKun](https://github.com/MujyKun)
- Development
  - FPS Counter & Mouse Movement/Position [FPSScene].
  - Text Labels to go on Screen [Label]
  - Note Tile to be played in game [Note]
  - Added Autoplay features so that the game can play itself.
  - Implemented Gravity
  - Implemented Player Movement (Several jumps, walking, horizontal/vertical movement, only floor jumping)
  - Implemented advanced camera (can follow player, scroll, navigate outside of the canvas, zoom)
  - Implemented majority Labels stay within the camera region if they were to zoom out or in.
  - Added Dynamic Canvas Resolution to support a multitude of resolutions despite the object sizes. 
  - Implemented animations to majority objects (Players, BeatZones, Background, ...)
  - Added collision detection to Players, Notes, and Floors. 
  - Implemented loading logic for songs. 
  - Distributed tiles to be arranged in BeatZone columns.
  - Built the framework for the game.
  - Built demo.
  - Implemented moons for backgrounds.
- Managed Dependencies
  - Created a fork of the game engine library ([PPB](https://github.com/ppb/pursuedpybear)) to fix dependencies issues with the sound controllers.
  - Project is now easily installable with pip or poetry. 
- Assets
  - Created animated player models for walking left, right, and standing still using the [Universal LPC Spritesheet Generator](https://sanderfrenken.github.io/Universal-LPC-Spritesheet-Character-Generator/#?body=Body_color_light&head=Human_male_light) 
  - Created animated backgrounds 
  - Utilized a piano note sound pack from [here](https://www.reddit.com/r/piano/comments/3u6ke7/heres_some_midi_and_mp3_files_for_individual/) 
  - Generated Piano Tiles that reference the key being pressed in Photoshop
  - Created BeatZone arrows and also added a glow effect when they are pressed.
  - Designed structure for song JSON files.
  - Implemented fonts into [resources](resources)
- Documentation
  - All code was documented with Sphinx/PIP8 standards. 
  - General Features documented in README.
  - Included Installation/Local Setup
  - Included Example Gifs
  
### [@DrewBieger](https://github.com/DrewBieger)
- Development
  - Researched and implemented pause/play features for background songs to be played with pysdl2, as well as modified ppb to fit our needs.
  - Implemented the Background to display a image behind every other object.
  - Implemented the beat management system of the project (Conductor)
  - Implemented the integration of both the music and sound system (Music, MusicController
  - Implemented events for the user to play, stop, pause, and unpause music (ext_events)
  - Implemented a feature to display the bpm of the song that is currently playing (BeatVisualizer, BeatTrigger)
  - Implemented an event for the user to start a BeatVisualizer to be in sync with the music
  - Created piano notes for the player to hit within beat (Note)
  - Implemented Note’s calculation on where to set its own height based upon given speed, bpm, and the target’s y position.
  - Added a health system for the Player to support multiple ways for the game to be scored (Player health, number of hits, number of misses, Player accuracy)
  - Implemented an accuracy system for the tiles that uses Conductor’s time difference between the last note that was played and the next note that is played.
  - Added collision detection system for BeatZone with Notes.
  - Implemented a game over scene that would be played after the player "loses".
  - Added a game over transition event with Player health hitting 0.
- Assets
  - Created a beat sound effect to be played on every beat with [jfxr](https://github.com/ttencate/jfxr). 
- Documentation
  - All code was documented with Sphinx/PIP8 standards.
  - General Features documented in README.
  - Created game design document.
  - Created state transition document.

## [Playable Demo](https://youtu.be/2ClTZRxASbg)

## [Copyrights](copyrights.md)
Copyrighted content or content that requires a mention of the creators for usage can be found [here](copyrights.md).


