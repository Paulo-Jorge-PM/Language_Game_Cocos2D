# Game for learning a language [prototype]

![screenshot](http://www.paulojorgepm.net/static/images/language_game.png)

I made this in my Masters. It is only a prototype, never finished it. It is the concept of a game with the objetive of teaching a new language. It is based on the Snake game, but with words and images, were the user needs to colect letters of words in a foreign language when they catch an objetct, an animal, etc. When they catch something a full image of the target appears with the complete word and a voice pronouncing it. Rocks serverd as obstacls, if the user touched them he would loos points. In theory this concept could be used to learn a new language from scratch. I had plans to creat enemies on screen, power-ups, and a mini-story from level to level, but I never had the time and had to end my dissertation (this game was an attachment
 to it). After that I got bored and never finished this (and most likely never will).

Note: originally the rocks would reduce points and an explosion sound/animation would fire, at the time it worked. More than 6 years have passed since then (at the moment it is 2018), and today I tested this with the most recent libraries of Cocos2D and Pyglet, and for some reason when the user touches a stone the game crashs. I don't care about this neither have time, so will not bug hunt.

Everyone can use this in any way they like, I don't care about licenses or copyright, just have fun.

##How to run:
If you don't have Python installed simply run the file "main.exe" - I compiled it from the Python source with Pyinstaller: "pyinstaller.exe --onefile --windowed main.py"
Note: I have not tested it in the .exe format.

To run the source code like a boss the only requirement is:
To use this the only requirement is:
-An installed version of Python 2.7 (not tested with other versions)
-Pyglet
-Cocos2D

To get pyglet just do in the comand line:```pip install pyglet```

The same with Cocos2D:```pip install cocos2d```

Then just run the file "main.py". 

##How to play:
Arrow keys (up, right, down, left) control the movement; spacebar makes it run faster; enter pauses the game. Don't touch the rocks; gems give points; catch the little cow sprite and after that a screen will appear with the full word - after that you need to catch the letters in the correct order.

##Contacts:
My Homepage: [www.paulojorgepm.net](http://www.paulojorgepm.net)