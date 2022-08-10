# PYpong
That's basic pong implementation of pong made in python and pygame.

## An API
In order to fully use pong game API you need to download and include [pong.py](/pong.py) in your project

```python3
from pong import PongGame
```

Then init game object
```python3
width, height = 800, 600

game = PongGame(width, height)
```

To generate new frame and process players input just call:

```python3
game.process_frame(
        display,
        deltaTime,
        input_0,
        input_1,
        drawHits,
        drawScores)
```
display - pygame destination surface object - ```pygame.Surface```  
deltaTime - time since last frame in secounds  
input_0 - input of left player   
&emsp;&emsp;an int value belenging to {-1, 0, 1}   
&emsp;&emsp;where -1 means go down, 0 no action and 1 go up   
input_1 - input of right player  
drawHits - ```bool``` describing to draw total number of hits  
drawScores - ```bool``` describing to draw scores of each player
\
\
\
You also have an example of the game implementation [here](/example.py).