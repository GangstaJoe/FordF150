import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

last_move=''


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    
    print(json.dumps(data, indent=2))
    
    global last_move
    #ay yo vide check
    # all placemnet for items
    
    head_x = data['you']['body'][0]['x']
    print('Your head is: ', head_x)
    head_y = data['you']['body'][0]['y']
    print('Your head_y is: ', head_y)
    apple_x = data['board']['food'][0]['x']
    print('The apple_x is:',apple_x)
    apple_y = data ['board']['food'][0]['y']
    print ('The apple_y is :',apple_y)
    HP = data['you']['health']
    print('Health is: ',HP)
    size = len(data['you']['body'])
    print('size is: ',size) 
    apple_right = apple_x > head_x
    apple_left = apple_x < head_x
    apple_down = apple_y > head_y
    apple_up = apple_y < head_y
    directions = ['up', 'down', 'left', 'right'] 
  #cant kill itself does not work for now!!!!
 #   if last_move == 'down':
  #      direction != 'up'
  #  if last_move == 'up':
  #      direction != 'down'
    #cant hit walls
    if last_move == '':
        direction = 'up'    
    if head_y == 0:
        direction = 'right'    
    if head_x == 10 :
        direction = 'down'
            
    if head_y == 10 :
        direction = 'left'
    if head_x == 0 and head_y != 0 and last_move != 'down':
        direction = 'up'
    
        
        #apple eater
    if HP <= 75:
        
        if apple_left is True:
            direction = 'left' 
            print('u_left')
        if apple_right is True:
            direction = 'right'
            print('u_right')
        if apple_up is True and last_move != 'down' :
            direction ='up'
            print('u_up')
        if apple_down is True and last_move != 'up':
            direction = 'down'
            print('u_down')

    if size >= 23:
        if head_y == 0 and head_x == 1  :
            direction = 'down'
        if head_y == 9 and head_x == 1:
            direction = 'right'
        if head_y == 9 and head_x == 2:
            direction = 'up'
        if head_y == 0 and head_x == 2 :
                direction = 'right'
        if head_y == 0 and head_x == 3 :
            direction = 'down'
        if head_y == 9 and head_x == 3:
            direction = 'right'    
        if head_y == 9 and head_x == 4 :
            direction = 'up'
        if head_y == 0 and head_x == 4:
            direction = 'right'
        if head_y == 0 and head_x == 5 :
            direction = 'down'
        if head_y == 9 and head_x == 5:
            direction = 'right'    
        if head_y == 9 and head_x == 6 :
            direction = 'up'
        if head_y == 0 and head_x == 6:
            direction = 'right'   
        if  head_y == 0 and head_x == 7 :
            direction = 'down'
        if head_y == 9 and head_x == 7:
            direction = 'right'
        if head_y == 9 and head_x == 8 :
            direction = 'up'
        if head_y == 0 and head_x == 8:
            direction = 'right'
        if head_y == 0 and head_x == 9 :
            direction = 'down'
        if head_y == 9 and head_x == 9:
            direction = 'right'
    
    
           
        
    last_move = direction
    #eating apple 
    #if HP <= 75 :
     #       direction = apple_y
      #      if head_y != apple_y:
       #         direction = apple_y
        #        if head_x != apple_x:
         #           direction = apple_x
                        
    
    #looping for 3 leangth    
   # if size == 3:
   #     if last_move == '':
   #         direction = 'up'
   #     if last_move == 'up':
   #         direction = 'right'
   #     if last_move == 'right':
   #         direction = 'down'
   #     if last_move == 'down':
   #         direction = 'left'
   #     if last_move == 'left':
   #         direction = 'up'
        
    
   
    print('direction is: ', direction)
    
    return move_response(direction)




@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
#vide confermed