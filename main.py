import os, terminal, graphics, shutil, GUIobject, PIL, editor
import pgerom as pe
from time import sleep

import pygame.transform

from selector import selector

project_location = ''
while not project_location:
    project_name = input("Project title: ")
    project_location = f'results\\{project_name}\\'
    if os.path.exists(project_location):
        print(f'A project with the name "{project_name}" already exists.')
        if selector(['Erase and reuse', 'Load'], "what to do?") == 0:
            shutil.rmtree(project_location)
        else:
            obj = GUIobject.load(os.path.join(project_location, "obj.gui"))
            break
    try:
        os.mkdir(project_location)
        sizeX = 0
        sizeY = 0
        while not sizeX:
            try:
                sizeX = int(input('Size (X): '))
            except:
                pass
        while not sizeY:
            try:
                sizeY = int(input('Size (Y): '))
            except:
                pass
        obj = GUIobject.gui(sizeX, sizeY)
        obj.savedata(os.path.join(project_location, "obj.gui"))
    except WindowsError:
        print("Unacceptable naming.\n")
        project_location = ''
obj.generate()
obj.save(os.path.join(project_location, 'image.png'))
graphics.clear()
terminal.font((3, 3))
graphics.resize((int(obj.sizeX/3+2), int(obj.sizeY/3+3)))
path = os.path.join(project_location, "temp.png")
obj.image.crop((0, 0, obj.sizeX, obj.sizeY)).resize(( int(obj.sizeX/3), int(obj.sizeY/3) ), PIL.Image.ANTIALIAS).save(os.path.join(project_location, "temp.png"))
graphics.setColor(graphics.red)
graphics.rect(0, 0, int(obj.sizeX/3+2), int(obj.sizeY/3+3))
pe.init()
graphics.black = graphics.Back.BLACK+graphics.Fore.BLACK
container = None
def regen():
    global  container
    obj.generate()
    obj.save_onlygui(os.path.join(project_location, "temp2.png"))
    container = pe.image(os.path.join(project_location, "temp2.png"), (obj.sizeX, obj.sizeY))
    obj.image.crop((0, 0, obj.sizeX, obj.sizeY)).resize(( int(obj.sizeX/2), int(obj.sizeY/2) )).save(os.path.join(project_location, "temp.png"))
def reload(dark=False, skip=True):
    if not skip:
        if dark:
            c = graphics.black
        else:
            c = graphics.blue
        graphics.clear()
        graphics.rect(0, 0, obj.sizeX + 2, obj.sizeY + 3, c)
    graphics.image(os.path.join(project_location, "temp.png"), 2, 2)
    sleep(0.7)
reload(skip=False)
pe.display.make((obj.sizeX*2+500, obj.sizeY*2), "GUI / Container generator")
def export():
    with open(os.path.join(project_location, 'export.txt'), 'w') as f:
        f.write(obj.compile())
button = {
    'reload':(obj.sizeX*2+400, obj.sizeY*2-40, 90, 30, "Reload."),
    'delete':(obj.sizeX*2+400, obj.sizeY*2-80, 90, 30, "Delete."),
    'export':(obj.sizeX*2+200, obj.sizeY*2-40, 90, 30, "Export."),
    'save':(obj.sizeX*2+300, obj.sizeY*2-40, 90, 30, "Save."),
    'back':(obj.sizeX*2+400, obj.sizeY*2-40, 90, 30, "Finish."),
    'newSlotArray':(obj.sizeX*2+370, 10, 120, 30, "New slot array."),
}
buttons = {}
def button_gen():
    global buttons
    for i in list(button):
        try:
            buttons[i]
            continue
        except:
            pass
        if not os.path.exists(f"resources/button_{i}_ic.png"):
            GUIobject.generate_slot(button[i][2], button[i][3], obj.slot_background_color, obj.slot_border_low, obj.slot_border_high).save(f'resources/button_{i}_ic.png')
        if not os.path.exists(f"resources/button_{i}_ac.png"):
            GUIobject.generate_slot(button[i][2], button[i][3], obj.slot_background_color, obj.slot_border_high, obj.slot_border_low).save(f'resources/button_{i}_ac.png')
        buttons[i + '_text'] = pe.text.make(button[i][4], 'resources/mc.ttf', 15, pe.math.center(button[i]), [pe.color.verydarkgray, None])
        buttons[i] = (button[i], pe.image(f"resources/button_{i}_ic.png", (button[i][2], button[i][3]), (button[i][0], button[i][1])), pe.image(f"resources/button_{i}_ac.png", (button[i][2], button[i][3]), (button[i][0], button[i][1])))
button_gen()
container, overlay = None, None
def REdisplay():
    global container, overlay
    obj.generate()
    obj.save_onlygui(os.path.join(project_location, "temp2.png"))
    container = pe.image(os.path.join(project_location, "temp2.png"), (obj.sizeX, obj.sizeY))
    overlay = pe.pygame.Surface(container.object.get_size(), pe.pygame.SRCALPHA)
REdisplay()
editmode = False
editing = None
while True:
    for pe.event.c in pe.event.get():
        pe.event.quitcheckauto()
    pe.fill.full(obj.background_color)
    if editmode:
        REdisplay()
        editing.display()
    pe.display.blit.rect(pygame.transform.scale(container.object,(obj.sizeX*2, obj.sizeY*2)), (0, 0))
    if not editmode:
        pe.button.image(*buttons['reload'], action=reload, data=(True, False))
        pe.button.image(*buttons['save'], action=obj.savedata, data=(os.path.join(project_location, 'obj.gui')))
        pe.button.image(*buttons['export'], action=export)
        pe.button.image(*buttons['newSlotArray'], action=editor.newSlotArray)
        pe.text.display(buttons['reload_text'])
        pe.text.display(buttons['save_text'])
        pe.text.display(buttons['export_text'])
        pe.text.display(buttons['newSlotArray_text'])
    else:
        editing.interact()
        if not editing.using:
            pe.button.image(*buttons['back'], action=editor.unload)
            pe.text.display(buttons['back_text'])
            pe.button.image(*buttons['delete'], action=editor.erase)
            pe.text.display(buttons['delete_text'])
        pe.display.blit.rect(pygame.transform.scale(overlay, (obj.sizeX * 2, obj.sizeY * 2)).convert_alpha(), (0, 0))
    pe.display.update()