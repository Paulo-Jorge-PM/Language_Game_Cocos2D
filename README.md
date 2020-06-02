# Game for learning a language [prototype]

![screenshot](http://www.paulojorgepm.net/static/images/language_game.png)

This is only a prototype (made during my Master’s), never finished it. It is the concept of a game with the objective of teaching a new language. It is based on the Snake game, but with words and images, were the user needs to collect letters of words in a foreign language when they catch an object, an animal, etc. When they catch something a full image of the target appears with the complete word and a voice pronouncing it. Rocks served as obstacles, if the user touched them he would lose points. In theory this concept could be used to learn a new language from scratch in a fun way. I had plans to create enemies on screen, power-ups, and a mini-story from level to level, but I never had the time to implement them. One day I would like to finish this project with full features, but for now it serves only as a concept.

Note: originally the rocks would reduce points and an explosion sound/animation would fire, at the time it worked. More than 6 years have passed since then (at the moment it is 2018), and today I tested this with the most recent libraries of Cocos2D and Pyglet, and for some reason when the user touches a stone the game crashes. This is only a concept and I moved on, so will not bug hunt, if I finish it someday I’ll do it, until then don’t crash against the rocks.

License: you can do anything except make commercial versions out of this concept. For nonprofit objectives this is open-source.

##How to run:
If you don't have Python installed simply run the file "main.exe" - I compiled it from the Python source with Pyinstaller: "pyinstaller.exe --onefile --windowed main.py"
Note: I have not tested it in the .exe format.

To run the source code like a boss the only requirements are:
-An installed version of Python 2.7 (not tested with other versions)
-Pyglet
-Cocos2D

To get pyglet just do in the comand line (having Python's pip instaled):
```
pip install pyglet
```

The same with Cocos2D:
```
pip install cocos2d
```

Then just run the file "main.py". 

##How to play:
Arrow keys (up, right, down, left) control the movement; spacebar makes it run faster; enter pauses the game. Don't touch the rocks; gems give points; catch the little cow sprite and after that a screen will appear with the full word - after that you need to catch the letters in the correct order.

##Contacts:
My Homepage: [www.paulojorgepm.net](http://www.paulojorgepm.net)