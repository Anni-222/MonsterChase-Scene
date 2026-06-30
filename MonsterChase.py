from scene import *
import sound
import random
import time

class GameScene(Scene):
    def setup(self):
        self.background_color = '#eec73b'
        self.timeLeft = 0
        self.tta = 0
        self.ttd = 0
        self.y = 102.5
        self.player = SpriteNode('plf:AlienBlue_front', position=(100, self.size.height / 2))
        self.joystick = SpriteNode('plf:HudPlayer_blue', position=(100, self.y))
        self.bgj = SpriteNode('iob:arrow_expand_256', position=(100, 100), size=(300, 300))
        self.enemies = []
        self.gameOver = False
        self.ln = 3
        self.lives = []
        self.boxes = []
        self.inventory = []
        self.coins = []
        """for i in range(random.randint(100, 3000)):
        	self.coin = SpriteNode('plf:Item_CoinBronze', position=(random.randint(0, 1200), random.randint(0, 1200)), size=(40, 40))
        	self.coin.alpha = 0.4
        	self.add_child(self.coin)
        	self.coins.append(self.coin)"""
        for i in range(self.ln):
          life = SpriteNode('plf:HudHeart_full', position=(1000+(i*50), 800), size=(60, 60))
          self.add_child(life)
          self.lives.append(life)
        for i in range(4):
        	self.enemy = SpriteNode('plf:Enemy_SlimeBlock', position=(random.randint(100, 1200), random.randint(100, 1200)), size=(70, 70))
        	self.enemy.color = '#ff4a4a'
        	self.enemy.frozen = False
        	self.add_child(self.enemy)
        	self.enemies.append(self.enemy)
        for i in range(random.randint(4, 10)):
        	self.box = SpriteNode('plf:Tile_BoxItem', position=(random.randint(100, 1200), random.randint(100, 1200)), size=(20, 20))
        	self.box.color = '#a90aee'
        	self.add_child(self.box)
        	self.boxes.append(self.box)	
        
        self.obs = []
        for i in range(random.randint(2, 10)):
        	self.ob = SpriteNode('plf:Tile_Cactus', position=(random.randint(100, 1200), random.randint(100, 1200)), size=(100, 100))
        	self.add_child(self.ob)
        	self.obs.append(self.ob)
        self.bgj.alpha = 0.4
        self.add_child(self.player)
        self.add_child(self.joystick)
        self.add_child(self.bgj)
        self.touchy = False
    
    def closeGame(self):
    	self.view.close()
    
    def update(self):
      if self.tta > 0:
      	self.tta += 1
      if self.tta >= 120:
      	self.enemy = SpriteNode('plf:Enemy_SlimeBlock', position=(random.randint(100, 1200), random.randint(100, 1200)), size=(70, 70))
      	self.enemy.color = '#ff4a4a'
      	self.enemy.frozen = False
      	self.add_child(self.enemy)
      	self.enemies.append(self.enemy)
      	self.tta = 0
      
      if self.ttd > 0:
      	self.ttd += 1
      if self.ttd >= 600:
      	self.box = SpriteNode('plf:Tile_BoxItem', position=(random.randint(100, 1200), random.randint(100, 1200)), size=(20, 20))
      	self.box.color = '#a90aee'
      	self.add_child(self.box)
      	self.boxes.append(self.box)
      	self.ttd = 0
      	
      playerHitbox = Rect(
      	self.player.position.x - 25, self.player.position.y - 25, 50, 60)
      if len(self.lives) == 0 and not self.gameOver:
        self.gameOver = True
        closeSequence = Action.sequence(Action.wait(1.5), Action.call(self.closeGame))
        self.run_action(closeSequence)
        print("You have no lives left!")
        return
      for enemy in self.enemies:
        if enemy.frozen:
          #enemy.remove_all_actions()
          continue
        if not enemy.frozen:
          if random.randint(1, 2) == 2:
            moveAction = Action.move_to(self.player.position.x, self.player.position.y, round(random.uniform(0.025, 10.00), 2))
          else:
            moveAction = Action.move_to(random.randint(100, 1000), random.randint(100, 1000), round(random.uniform(1.0, 10.0), 2))
          enemy.run_action(moveAction)
        enemyHitbox = Rect(enemy.position.x - 5, enemy.position.y - 5, 35, 45)
        if playerHitbox.intersects(enemyHitbox):
          self.player.color = 'red'
          reset = Action.move_to(100, 100, 0)
          self.player.run_action(reset)
          self.lives[len(self.lives)-1].texture = Texture('plf:HudHeart_empty')
          self.lives.remove(self.lives[len(self.lives)-1])
          break
        for ob in self.obs:
          obsHitbox = Rect(ob.position.x - 5, ob.position.y - 5, 35, 45)
          if enemyHitbox.intersects(obsHitbox):
            enemy.remove_from_parent()
            if self.tta == 0:
            	self.tta = 1
      for ob in self.obs:
        obsHitbox = Rect(ob.position.x - 5, ob.position.y - 5, 35, 45)
        if playerHitbox.intersects(obsHitbox):
          self.lives[len(self.lives)-1].remove_all_actions()
          self.player.color = 'red'
          self.lives[len(self.lives)-1].texture = Texture('plf:HudHeart_empty')
          self.lives.remove(self.lives[len(self.lives)-1])
          self.player.remove_all_actions()
          self.player.position = (100, 100)
          break
      objects = {'bomb': 'plf:Tile_BombWhite', 'heart': 'plf:HudHeart_full', 'freeze': 'plf:Item_GemBlue'}
      items = ['bomb', 'heart', 'freeze']
      iType = random.choice(items)
      textureName = objects[iType]
      for box in self.boxes:
        if playerHitbox.intersects(box.frame):
          if self.ttd == 0:
            self.ttd = 1
          if iType == 'bomb':
	          something = SpriteNode(textureName, position=(box.position.x, box.position.y), size=(60, 60))
	          something.name = iType
	          self.add_child(something)
	          goInventory = Action.move_to((len(self.inventory)*60)+260, 800, 1)
	          self.inventory.append(something)
	          something.run_action(goInventory)
          elif iType == 'heart':
          	life = SpriteNode('plf:HudHeart_full', position=(box.position.x, box.position.y), size=(60, 60))
          	self.add_child(life)
          	goInventory = Action.move_to(1000+(len(self.lives)*50), 800, 1)
          	life.run_action(goInventory)
          	self.lives.append(life)
          else:
          	something = SpriteNode(textureName, position=(box.position.x, box.position.y), size=(60, 60))
          	something.name = iType
          	self.add_child(something)
          	goInventory = Action.move_to((len(self.inventory)*60)+260, 800, 1)
          	self.inventory.append(something)
          	something.run_action(goInventory)
          box.remove_from_parent()
          self.boxes.remove(box)
      for i in range(len(self.inventory)):
      	self.inventory[i].position = ((i*60)+260, 800)
      
    def touch_moved(self, touch):
        if self.gameOver:
        	return
        if self.touchy:
	        cx, cy = touch.location
	        mainx, mainy = 100, 100
	        dirx, diry = cx - mainx, cy - mainy
	        if 0 < (self.player.position[0]+dirx) < 1200 and 0 < (self.player.position[1]+diry) < 900:
	        	if dirx < 0:
		        	self.player.x_scale = -1.0
		        else:
		        	self.player.x_scale = 1.0
		        self.player.texture = Texture('plf:AlienBlue_swim1')
		        self.player.remove_all_actions()
		        moveAction = Action.move_to(self.player.position.x+dirx, self.player.position.y+diry, 0.6)
		        self.player.run_action(moveAction)
        	else:
        		self.player.remove_all_actions()
        	joyX = max(30, min(cx, 170))
	        joyY = max(30, min(cy, 170))
	        self.joystick.remove_all_actions()
	        shownAction = Action.move_to(joyX, joyY, 0)
	        self.joystick.run_action(shownAction)
    
    def touch_began(self, touch):
    	self.player.color = "#ffffff"
    	if touch.location.y > 750:
    		self.touchy = False
    		return
    	self.touchy = True
    			
    def unfreezeEnemy(self, targetEnemy):
    	targetEnemy.frozen = False
    	targetEnemy.color = '#ff0000'
    	
    def touch_ended(self, touch):
    	self.touchy = False
    	self.player.texture = Texture('plf:AlienBlue_front')
    	self.player.remove_all_actions()
    	shownAction = Action.move_to(100, self.y, 0.1)
    	self.joystick.run_action(shownAction)
    	for obj in list(self.inventory):
    		dx = abs(touch.location.x - obj.position.x)
    		dy = abs(touch.location.y - obj.position.y)
    		if dx < 40 and dy < 40:
    			if obj.name == 'bomb':
    				for enemy in list(self.enemies):
    					enemy.remove_from_parent()
    					self.enemies.remove(enemy)
    					if self.tta == 0:
    						self.tta = 1
    				obj.remove_from_parent()
    				if obj in self.inventory:
    					self.inventory.remove(obj)
    			elif obj.name == 'freeze':
    				for enemy in list(self.enemies):
    					enemy.remove_all_actions()
    					enemy.frozen = True
    					enemy.color = '#ffffff'
    					enemy.texture = Texture('spc:Star3')
    					seq = Action.sequence(Action.wait(3), Action.call(lambda e=enemy: [setattr(e, 'frozen', False), setattr(e, 'texture', Texture('plf:Enemy_SlimeBlock')), setattr(e, 'color', '#ff4a4a')]))
    					enemy.run_action(seq)
    				obj.remove_from_parent()
    				if obj in self.inventory:
    					self.inventory.remove(obj)
    			return
# This boots up the game canvas on your iPad screen!
run(GameScene(), orientation=LANDSCAPE)