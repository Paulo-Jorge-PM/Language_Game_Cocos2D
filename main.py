#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cocos
import cocos.collision_model as cm
import cocos.euclid as eu
from cocos.director import director

import pyglet

pyglet.resource.path = ['data', 'data/images', 'data/sound'] # Tell pyglet where to find the resources
pyglet.resource.reindex()


import data.level1 as level
from data.level1 import *

director.init( resizable=True, do_not_scale=True, fullscreen=True, audio_backend='pyglet' )
director.show_FPS = True


main_scene = cocos.scene.Scene()
main_scene.add(cocos.layer.ColorLayer(255, 255, 255, 255), z=0)

map = cocos.tiles.load('tiles.xml')['level1']
map.set_view(0, 0, map.px_width, map.px_height)
map.position=(director.window.width/2-map.px_width/2, director.window.height - map.px_height - 50)

main_scene.add(map, z=0)

main_batch = cocos.batch.BatchNode()
main_scene.add(main_batch, z=3)
main_scene.add( level.Game(map, main_scene, director, main_batch), z=1 )

cocos.director.director.run(main_scene)