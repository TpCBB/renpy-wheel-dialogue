define config.name = "Wheel Synthetic Test"
define config.save_directory = "wheel_synthetic_20261117"
define config.screen_width = 800
define config.screen_height = 600
define config.developer = True
define config.autosave_on_quit = False
default preferences.text_cps = 1

define config.main_menu = False

init python:
    def trace(event, **kwargs):
        if event == 'show':
            with open(config.basedir + '/events.txt', 'a') as f:
                f.write('say: ' + str(kwargs.get('what')) + '\n')
    config.character_callback = trace
    import threading, time, pygame
    def send_test():
        for delay, kind, value in [(3,'wheel',5),(1,'wheel',5),(1,'wheel',5),(1,'wheel',5),(1,'wheel',5),(1,'wheel',5),(1,'wheel',5),(1,'key',pygame.K_DOWN),(1,'key',pygame.K_RETURN),(1,'wheel',4),(1,'wheel',5),(1,'key',pygame.K_DOWN),(1,'key',pygame.K_DOWN),(1,'key',pygame.K_RETURN)]:
            time.sleep(delay)
            mark('INPUT %s %s' % (kind, value))
            if kind == 'wheel':
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button':value,'pos':(400,300)}))
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'button':value,'pos':(400,300)}))
            else:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key':value,'mod':0,'unicode':'','repeat':0,'scancode':0}))
                pygame.event.post(pygame.event.Event(pygame.KEYUP, {'key':value,'mod':0,'unicode':'','repeat':0,'scancode':0}))
    test_thread = threading.Thread(target=send_test)
    test_thread.daemon = True
    test_thread.start()
    def mark(value):
        with open(config.basedir + '/events.txt', 'a') as f:
            f.write(value + '\n')

screen say(who, what):
    window:
        xalign 0.5 yalign 0.8
        vbox:
            text what id "what" size 36

screen choice(items):
    vbox:
        xalign 0.5 yalign 0.5 spacing 20
        for item in items:
            textbutton item.caption action item.action

label start:
    $ mark('LINE ONE')
    "LINE ONE"
    $ mark('LINE TWO')
    "LINE TWO"
    $ mark('LINE THREE')
    "LINE THREE"
    $ mark('MENU ENTER')
    menu:
        "Choose A":
            $ mark('BRANCH A')
            "BRANCH A"
        "Choose B":
            $ mark('BRANCH B')
            "BRANCH B"
    "AFTER BRANCH"
    return
