# python-game-of-life
Conway's Game of Life, made with Python

This is my version of the Game of Life I managed to create as one of my challenges.
There's not too much else I can think of to add to it except try to clean up the code
	as best as I can and make it run as efficient as it can.
	
One of my next goals is to write this for Linux, using Bash, which should be tricky enough.

2022-09-19:
	- Cleaned up mouse/cursor grid-snapping functionality

	- Cleaned up dead_board function
	
	+ clear screen with "c" key

	+ Ability to press and hold mouse button when drawing instead of having to click
		each spot, individually.

	+ +/- keys speed/slow the simulation speed (FPS cap remains at 60)

	+ Ability to save (s) and restore (r) the board state. On start, the initial random
		board state is saved automatically.

	+ Save board state (ctrl+s) in binary format (Ctrl+s)
		-Still need to create file load function
