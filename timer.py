#! /bin/python

import argparse
import pyglet

WINDOW = pyglet.window.Window(fullscreen=True)

class Timer():
    def __init__(self, sec, min_sec):
        self.init_sec = sec
        self.min_sec = min_sec
        self.start = 'READY ?'
        self.label = pyglet.text.Label(self.start, font_size=300,
                                       x=WINDOW.width//2, y=WINDOW.height//2,
                                       anchor_x='center', anchor_y='center')
        
        self.ready = False
        self.count_ready = 3
        self.reset()


        self.beep = pyglet.media.load('sounds/beep1.wav', streaming=False)
        self.beep_go = pyglet.media.load('sounds/beep2.wav', streaming=False)
        self.end = pyglet.media.load('sounds/end.wav', streaming=False)

    def prepare(self, dt):
        if self.count_ready > 0:
            self.label.font_size = 400
            self.label.text = '{:d}'.format(self.count_ready)
            self.count_ready -= int(dt)
            self.beep.play()
        else:
            self.ready = True
            str_ = ''            
            if self.min_sec:
                self.label.font_size = 360
                m, s = divmod(self.seconds, 60)
                str_ = '{:02d}:{:02d}'.format(m, s)
            else:
                str_ = '{:d}'.format(int(self.seconds))
            self.label.text = '{}'.format(str_)
            self.beep_go.play()
            #self.seconds += 1

    def reset(self):
        self.ready = False
        self.count_ready = 3
        self.seconds = self.init_sec
        self.running = False
        self.label.text = self.start
        self.label.color = (255, 255, 255, 255)
		self.label.font_size = 300

    def update(self, dt):
        if self.running:
            if self.ready:
                
                self.seconds -= int(dt)
                if self.min_sec:
                    m, s = divmod(self.seconds, 60)
                    self.label.text = '{:02d}:{:02d}'.format(int(m), int(s))
                else:
                    self.label.text = '{:d}'.format(int(self.seconds))

                if self.seconds <= self.init_sec/3:
                    self.label.color = (255, 0, 0, 255)

                if self.seconds == 0:
                    self.running = False
                    #self.label.text = 'STOP'
                    self.end.play()
            else:
                self.prepare(dt)

def main(minutes, seconds, min_sec):

    # Check if minutes has been given
    if minutes is None:
        # If seconds hasn't been given, we set a simple timer of 1 minute
        if seconds is None:
            minutes = 1
            seconds = 0
        else:
            # Trasnform the seconds in int
            minutes = 0
            seconds = int(seconds)
    else:
        # Transform the minutes in int
        minutes = int(minutes)
        if seconds is None:
            seconds = 0
        else:
            seconds = int(seconds)

    # Transform the seconds in minutes
    sec = seconds + minutes*60
    
    timer = Timer(sec, min_sec)

    # Functions on KEY event
    @WINDOW.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            if timer.running:
                timer.reset()
            elif not timer.ready:
                timer.running = True
            else:
                timer.reset()
        elif symbol == pyglet.window.key.ESCAPE:
            WINDOW.close()

    @WINDOW.event
    def on_draw():
        WINDOW.clear()
        timer.label.draw()

    pyglet.clock.schedule_interval(timer.update, 1)
    pyglet.app.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Timer!')
    parser.add_argument('-m', '--minutes', help='Minutes')
    parser.add_argument('-s', '--seconds', help='Seconds')
    parser.add_argument('-ms', '--min_sec', help='Print Minute Seconds instead of just seconds.', action='store_true')

    args = parser.parse_args()

    main(args.minutes, args.seconds, args.min_sec)
