#!/usr/bin/env python
# -*- coding: utf-8 -*-        
            
import cocos
import cocos.collision_model as cm
import cocos.euclid as eu
from cocos.director import director
from cocos.particle_systems import *

from cocos.scenes import *


import pyglet

pyglet.resource.path = ['data', 'data/images', 'data/sound'] # Tell pyglet where to find the resources
pyglet.resource.reindex()


class Game(cocos.layer.Layer):

    is_event_handler = True #: enable pyglet events - tem que ser chamado antes do init

    velocity = 70
    velocity_original = velocity
    points = 0
    
    #keys
    direction = 'up'
    direction_next = 'up'
    space = False
    enter = False
    enter_splash = False
    
    def __init__(self, map, scene, director, main_batch):
        super( Game, self ).__init__()
        
        self.scene = scene
        self.director = director
        
        self.map = map
        self.animals = {}
        self.letters = {}
        self.obstacles = {}
        self.gems_orange = []
        self.gems_blue = []
        
        #load dos sons
        self.gem_sound = pyglet.resource.media('click_n.wav', streaming=False)
        self.cow_sound = pyglet.resource.media('cow_sound.wav', streaming=False)
        self.crush_sound = pyglet.resource.media('crushing.wav', streaming=False)
        #lista com o nome do animal e respectivo som
        self.list_sounds = {'cow':self.cow_sound}
        
        #constantes e variaveis
        self.cell_width = self.map.tw
        self.cell_height = self.map.th
        self.map_x = self.map.x
        self.map_y = self.map.y
        self.tail = []
        self.intersection_coords = []
        
        self.collision_manager = cm.CollisionManagerGrid(-self.map.x, self.map.x+self.map.px_width,
                                               -self.map.y, self.map.y+self.map.px_height,
                                               self.map.tw, self.map.th)
        
        
        self.layer_z4 = cocos.layer.Layer() #estas layres servem para controlar a ordem do draw
        self.layer_z7 = cocos.layer.Layer()
        self.layer_z9 = cocos.layer.Layer()
        
        self.add(self.layer_z4, z=4) #estas layres servem para controlar a ordem do draw
        self.add(self.layer_z7, z=7) #player, pontos etc
        self.add(self.layer_z9, z=9) #splash
        
        self.main_batch = main_batch
        
        #points:
        self.points = cocos.text.Label('0',
            font_name='Verdana',
            font_size=30,
            color=(255,0,0,255),
            anchor_x='center', anchor_y='center')
        self.points.position = 200, 200
        self.layer_z7.add(self.points)
        
        #word:
        self.word = cocos.text.Label('',
            font_name='Verdana',
            font_size=60,
            color=(0,0,0,255),
            anchor_x='center', anchor_y='center')
        self.word.position = 600, 200
        self.layer_z7.add(self.word)
        
        #main_batch = cocos.batch.BatchNode() 
        #self.add(main_batch, z=2)
        #self.main_batch = main_batch

        #chama a função que faz load dos items no mapa relativo ao level
        self.load_items()

        self.player = cocos.sprite.Sprite('char1.png')
        #self.player.anchor = (0,0) #acho que não funciona, está sempre no centro
        
        self.padding_y = self.player.height/4 #espaço extra para ficar mais no centro vertical da celula
        
        start = self.map.find_cells(player_start=True)[0]

        self.player.position = (start.center[0]+self.map_x, start.center[1]+self.map_y)  #posiciona o anchor central da sprite no centro da celula

        self.player.y += self.padding_y #aumenta, para ficar mais dentro da cell
        self.player.cshape = cm.AARectShape( eu.Vector2(self.player.x, self.player.y), self.player.width/2, self.player.height/2)
        
        self.layer_z7.add(self.player)
        #self.main_batch.add( self.player, z=7 )
        
        self.collision_manager.add(self.player)

        self.cell_now = self.map.get_at_pixel(self.player.x-self.map_x, self.player.y-self.map_y)
        self.cell_next = self.map.get_neighbors(self.cell_now)
        self.schedule(self.update)
        
    def splash_image(self, name):
    
        self.pause_scheduler()
        
        splash = cocos.sprite.Sprite(name+'_splash.png')
        splash.position = (self.map_x+self.map.px_width/2, self.map_y+self.map.px_height/2)
        #splash.do( cocos.actions.interval_actions.FadeIn(5) )
        self.layer_z9.add(splash, z=9)
        self.layer_z9.add(cocos.layer.ColorLayer(255, 255, 255, 255), z=8) #para tapar todo o ecra

        #self.main_batch.add(splash, z=9)

        self.list_sounds[name].play()

        word = cocos.text.Label(name,
            font_name='Verdana',
            font_size=200,
            color=(255,0,0,255),
            anchor_x='center', anchor_y='center')
            
        message = cocos.text.Label('carrega na tecla enter para continuar...',
            font_name='Verdana',
            font_size=15,
            color=(149,149,149,255),
            anchor_x='center', anchor_y='center')
            
            
        word.position=splash.x, splash.y-120
        self.layer_z9.add(word, z=10)
        
        message.position=word.x, word.y-200
        self.layer_z9.add(message, z=10)
        
        n=1
        for letter in name:
            font = cocos.text.Label(letter,
                font_name='Verdana',
                font_size=15,
                color=(0,0,0,255),
                anchor_x='center', anchor_y='center')
            
            for cell in self.map.find_cells(empty=str(n)):
                item = cocos.sprite.Sprite(letter+'.png')
                item.position = (cell.center[0]+self.map.x, cell.center[1]+self.map.y)
                item.cshape = cocos.collision_model.AARectShape( cocos.euclid.Vector2(item.x, item.y), item.width/2, item.height/2 )
                self.layer_z4.add(item)
                self.collision_manager.add(item)
                self.letters[item]=letter
            n=n+1
        word_space=''
        for l in range(n-1):
            word_space=word_space+'_ '
        self.word.element.text=word_space[:-1] #o :-1 serve pra tirar o ultimo espaço no final
          
            
        
        
        #self.do( cocos.actions.interval_actions.Delay(20) )
        
        #splash.kill()
        
        self.enter_splash = True
        self.enter = True
        

          
    def load_items(self):
        for cell in self.map.find_cells(gem='blue'):
        
            #self.add(Layer_z('gem_blue.png', cell.center[0]+self.map.x, cell.center[1]+self.map.y, self.main_batch, 'gem_blue'), z=4)
            
            item = cocos.sprite.Sprite('gem_blue.png')
            item.position = (cell.center[0]+self.map.x, cell.center[1]+self.map.y)
            item.cshape = cocos.collision_model.AARectShape( cocos.euclid.Vector2(item.x, item.y), item.width/2, item.height/2 )
            self.layer_z4.add(item)
            #self.main_batch.add(item, z=4)
            self.collision_manager.add(item)
            self.gems_blue.append(item)
    
        for cell in self.map.find_cells(gem='orange'):
            item = cocos.sprite.Sprite('gem_orange.png')
            item.position = (cell.center[0]+self.map.x, cell.center[1]+self.map.y)
            item.cshape = cocos.collision_model.AARectShape( cocos.euclid.Vector2(item.x, item.y), item.width/2, item.height/2 )
            self.layer_z4.add(item)
            #self.main_batch.add(item, z=4)
            self.collision_manager.add(item)
            self.gems_orange.append(item)
            
        for cell in self.map.find_cells(animal='cow'):
            item = cocos.sprite.Sprite('cow.png')
            item.position = (cell.center[0]+self.map.x, cell.center[1]+self.map.y)
            item.cshape = cocos.collision_model.AARectShape( cocos.euclid.Vector2(item.x, item.y), item.width/2, item.height/2 )
            self.layer_z4.add(item)
            #self.main_batch.add(item, z=4)
            self.collision_manager.add(item)
            self.animals[item]='cow'
            
        for cell in self.map.find_cells(obstacle='rock'):
            item = cocos.sprite.Sprite('rock.png')
            item.position = (cell.center[0]+self.map.x, cell.center[1]+self.map.y)
            item.cshape = cocos.collision_model.AARectShape( cocos.euclid.Vector2(item.x, item.y), item.width/2, item.height/2 )
            self.layer_z4.add(item)
            #self.main_batch.add(item, z=4)
            self.collision_manager.add(item)
            self.obstacles[item]='rock'
 
    def on_key_press (self, key, modifiers):
        if key == pyglet.window.key.UP and self.direction != 'down':
            self.direction_next = 'up'
        if key == pyglet.window.key.RIGHT and self.direction != 'left':
            self.direction_next = 'right'
        if key == pyglet.window.key.DOWN and self.direction != 'up':
            self.direction_next = 'down'
        if key == pyglet.window.key.LEFT and self.direction != 'right':
            self.direction_next = 'left'
        if key == pyglet.window.key.SPACE:
            self.space = True
        if key == pyglet.window.key.ENTER:
            if self.enter == False:
                self.enter = True
                self.pause_scheduler()
                self.on_pause()
            else:
                if self.enter_splash == True:
                    for obj in self.layer_z9.get_children():
                        obj.kill()
                    self.enter_splash = False
                self.enter = False
                self.resume_scheduler()
            
    def on_key_release( self, key, mod ):
        if key == pyglet.window.key.SPACE:
            self.space = False
        #if key == pyglet.window.key.ENTER:
            #self.enter = False
            
    def on_pause(self):
        pass
            
    def tail_move(self, key, dt):
        if self.intersection_coords[key][2] == 'up':
            self.tail[key].position = (self.intersection_coords[key][0], min(self.tail[key].y + self.velocity*dt, self.intersection_coords[key][1]) )
        elif self.intersection_coords[key][2] == 'right':
            self.tail[key].position = (min(self.tail[key].x + self.velocity*dt, self.intersection_coords[key][0]) , self.intersection_coords[key][1])
        elif self.intersection_coords[key][2] == 'down':
            self.tail[key].position = (self.intersection_coords[key][0], max(self.tail[key].y - self.velocity*dt, self.intersection_coords[key][1]) )
        elif self.intersection_coords[key][2] == 'left':
            self.tail[key].position = (max(self.tail[key].x - self.velocity*dt, self.intersection_coords[key][0]), self.intersection_coords[key][1])

            
    def update(self, dt):
        #velocidade
        if self.space == True:
            self.velocity = self.velocity_original * 3
        else: 
            self.velocity = self.velocity_original
            
        #movimento Player
        if self.direction=='up':
            self.player.y = min(self.player.y + self.velocity * dt, self.cell_next[self.map.UP].center[1]+self.padding_y+self.map_y)
            if self.player.y == self.cell_next[self.map.UP].center[1]+self.padding_y+self.map_y: #cruazamento do player com o centro da celula
                self.cell_next = self.map.get_neighbors(self.cell_next[self.map.UP]) #actualiza a cell_next1
                self.intersection_coords.insert ( 0, [self.player.x, self.player.y-self.padding_y, self.direction] ) #coords de intersecção
                if self.direction != self.direction_next: #mudança de direcção
                    self.direction = self.direction_next
        elif self.direction=='right':
            self.player.x = min(self.player.x + self.velocity * dt, self.cell_next[self.map.RIGHT].center[0]+self.map_x)
            if self.player.x == self.cell_next[self.map.RIGHT].center[0]+self.map_x: #cruazamento do player com o centro da celula
                self.cell_next = self.map.get_neighbors(self.cell_next[self.map.RIGHT]) #actualiza a cell_next
                self.intersection_coords.insert ( 0, [self.player.x, self.player.y-self.padding_y, self.direction] ) #coords de intersecção
                if self.direction != self.direction_next: #mudança de direcção
                    self.direction = self.direction_next
        elif self.direction=='down':
            self.player.y = max(self.player.y - self.velocity * dt, self.cell_next[self.map.DOWN].center[1]+self.padding_y+self.map_y)
            if self.player.y == self.cell_next[self.map.DOWN].center[1]+self.padding_y+self.map_y: #cruazamento do player com o centro da celula
                self.cell_next = self.map.get_neighbors(self.cell_next[self.map.DOWN]) #actualiza a cell_next
                self.intersection_coords.insert ( 0, [self.player.x, self.player.y-self.padding_y, self.direction] ) #coords de intersecção  
                if self.direction != self.direction_next: #mudança de direcção
                    self.direction = self.direction_next  
        elif self.direction=='left':
            self.player.x = max(self.player.x - self.velocity * dt, self.cell_next[self.map.LEFT].center[0]+self.map_x)
            if self.player.x == self.cell_next[self.map.LEFT].center[0]+self.map_x: #cruazamento do player com o centro da celula
                self.cell_next = self.map.get_neighbors(self.cell_next[self.map.LEFT]) #actualiza a cell_nex't
                self.intersection_coords.insert ( 0, [self.player.x, self.player.y-self.padding_y, self.direction] ) #coords de intersecção
                if self.direction != self.direction_next: #mudança de direcção
                    self.direction = self.direction_next
            
        else:
            pass #no inicio do jogo, pedir para pressionar tecla de movimento
        
        
        #points

        
        
        
        #para poder determinar as property's da cell actual
        self.cell_now = self.map.get_at_pixel(self.player.x-self.map_x, self.player.y-self.map_y)
        
        #check collision e atualiza sprites cshape em movimento
        self.collision_manager.remove_tricky(self.player)
        self.player.cshape = cocos.collision_model.AARectShape( eu.Vector2(self.player.x, self.player.y), self.player.width/2, self.player.height/2)
        self.collision_manager.add(self.player)
        
        collisions = self.collision_manager.objs_colliding(self.player)

        for obj in collisions:
            self.after_collide_do(obj,self.cell_now)
                
        #apaga as coords a mais, de acordo com o numero de tails
        len_tail = len(self.tail)
        del self.intersection_coords[len_tail+2:]
            
        #move a tail e posiciona os elementos
        for k in range(len_tail):
            self.tail_move(k,dt)
                
    def after_collide_do(self, obj, cell):

        #if 'gem' in cell:
        #if obj.image == 'gem_blue.png' or 'gem_orange.png':
        if obj not in self.animals and obj not in self.obstacles:
            self.gem_sound.play()
            self.collision_manager.remove_tricky(obj)
            len_tail = len(self.tail) #serve pa determinar a key da coord intersection correspondente
            obj.position = (self.intersection_coords[len_tail][0], self.intersection_coords[len_tail][1])
            obj.do( cocos.actions.base_actions.Repeat( cocos.actions.interval_actions.RotateBy(360,0.4) ) )
            self.tail.append(obj)
            #obj.kill()
            
        if obj in self.animals:
            #print obj.batch
        
            #splash = cocos.sprite.Sprite('cow_splash.png')
            #splash.position = (self.map_x+self.map.px_width/2, self.map_y+self.map.px_height/2)
            #self.main_batch.add(splash, z=7)
            self.splash_image('cow')
            #self.pause_scheduler()
            #self.resume_scheduler()
            #self.gem_sound.play()
            self.collision_manager.remove_tricky(obj)
            obj.kill()
        
        if obj in self.gems_orange:
            self.points.element.text = str( int(self.points.element.text) + 10)
            
        if obj in self.gems_blue:
            self.points.element.text = str( int(self.points.element.text) + 50)
        
        if obj in self.obstacles:
            self.points.element.text = str( int(self.points.element.text) - 40)
            self.collision_manager.remove_tricky(obj)
            obj.kill()
            explosion = Explosion()
            explosion.life_var=0.2
            explosion.life=0.2
            explosion.auto_remove_on_finish = True
            explosion.position = obj.x, obj.y
            self.crush_sound.play()
            self.layer_z4.add(explosion)
        
        #OTIMIZAR! No time e protótipo apenas com uma palavra
        #Por isso ficou assim, mas devia ser uma função para qualquer palavra
        if obj in self.letters:
            print 'letter:'+self.letters[obj]
            if self.letters[obj] == 'c':
                if self.word.element.text == '_ _ _':
                    self.word.element.text = 'C _ _'
                elif self.word.element.text == '_ O _':
                    self.word.element.text = 'C O _'
                elif self.word.element.text == '_ _ W':
                    self.word.element.text = 'C _ W'
                elif self.word.element.text == '_ O W':
                    self.word.element.text = 'C O W'
            elif self.letters[obj] == 'o':
                if self.word.element.text == '_ _ _':
                    self.word.element.text = '_ O _'
                elif self.word.element.text == 'C _ _':
                    self.word.element.text = 'C O _'
                elif self.word.element.text == '_ _ W':
                    self.word.element.text = '_ O W'
                elif self.word.element.text == 'C _ W':
                    self.word.element.text = 'C O W'     
            elif self.letters[obj] == 'w':
                if self.word.element.text == '_ _ _':
                    self.word.element.text = '_ _ W'
                elif self.word.element.text == '_ O _':
                    self.word.element.text = '_ O W'
                elif self.word.element.text == 'C _ _':
                    self.word.element.text = 'C _ W'
                elif self.word.element.text == 'C O _':
                    self.word.element.text = 'C O W'
            
            
        
            #main_scene.do( cocos.actions.grid3d_actions.Waves3D( duration=2) + cocos.actions.grid3d_actions.Lens3D(duration=2) )
            
    def points(self):
        pass
