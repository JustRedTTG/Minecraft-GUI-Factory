import __main__ as main
import GUIobject
import pgerom as pe
objindex = 0
def dub(point, by=2):
    return (point[0]*by, point[1]*by)
def undub(point, by=2):
    return (point[0]/by, point[1]/by)
class SlotArray:
    def __init__(self, startX, startY, id='obj'):
        global objindex
        self.x = startX
        self.y = startY
        self.sizeX = 1
        self.sizeY = 1
        self.align = 'none'
        self.id = id+str(objindex)
        self.using = False
        objindex += 1
    def erase(self):
        for i in list(main.obj.slotBars):
            if i.endswith(self.id):
                del main.obj.slotBars[i]
    def display(self):
        pe.draw.circle(pe.color.red, (self.x, self.y), 2, 0)
        self.erase()
        for i in range(self.sizeY):
            main.obj.slotBars[f'{i}_{self.id}'] = GUIobject.slotBarObject(self.x, self.y+i*main.obj.slotSize[1], self.sizeX, self.align)
        main.REdisplay()
    def interact(self):
        if not self.using:
            pe.draw.circle(pe.color.red, (self.x, self.y), 2, 0, display_work=main.overlay)
            corner_point = (self.x+main.obj.slotSize[0]*self.sizeX, self.y+main.obj.slotSize[1]*self.sizeY)
            pe.draw.circle(pe.color.red, corner_point, 2, 0, display_work=main.overlay)
        else:
            corner_point = (self.x + main.obj.slotSize[0] * self.sizeX, self.y + main.obj.slotSize[1] * self.sizeY)
            pe.draw.rect(pe.color.verydarkgray, (self.x, self.y, corner_point[0]-self.x, corner_point[1]-self.y), 2, display_work=main.overlay)
        if (not self.using) and pe.math.dist(pe.mouse.pos(), dub(corner_point)) <= 10:
            pe.draw.circle(pe.color.green, corner_point, 2, 0, display_work=main.overlay)
            if pe.mouse.clicked()[0]:
                self.using = True
                mp = pe.mouse.pos()
                db = dub(corner_point)
                self.using_offset = (mp[0]-db[0], mp[1]-db[1])
                self.using_type = 'expand'
        elif (not self.using) and pe.math.dist(pe.mouse.pos(), dub((self.x, self.y))) <= 10:
            pe.draw.circle(pe.color.green, (self.x, self.y), 2, 0, display_work=main.overlay)
            if pe.mouse.clicked()[0]:
                self.using = True
                mp = pe.mouse.pos()
                db = dub((self.x, self.y))
                self.using_offset = (mp[0]-db[0], mp[1]-db[1])
                self.using_type = 'move'
        elif not self.using:
            return
        elif self.using and self.using_type == 'expand':
            mp = undub(pe.mouse.pos())
            pixel_size = (mp[0]-self.using_offset[0], mp[1]-self.using_offset[1])
            self.sizeX = int( (pixel_size[0]-self.x)/main.obj.slotSize[0] )+1
            self.sizeY = int( (pixel_size[1]-self.y)/main.obj.slotSize[1] )+1
            self.sizeX = max(self.sizeX, 1)
            self.sizeY = max(self.sizeY, 1)
            if not pe.mouse.clicked()[0]:
                self.using = False
        elif self.using and self.using_type == 'move':
            mp = undub(pe.mouse.pos())
            pixel_size = (mp[0]-self.using_offset[0], mp[1]-self.using_offset[1])
            pixel_size = self.aligner(pixel_size)
            self.x = pixel_size[0]
            self.y = pixel_size[1]
            self.x = int(self.x)
            self.y = int(self.y)
            if not pe.mouse.clicked()[0]:
                self.using = False
    def aligner(self, point):
        x, y = point[0], point[1]
        x = min( max(main.obj.extra_padding, x), (main.obj.sizeX-main.obj.extra_padding - self.sizeX*main.obj.slotSize[0]) )
        y = min( max(main.obj.extra_padding, y), (main.obj.sizeY-main.obj.extra_padding - self.sizeY*main.obj.slotSize[1]) )
        return (x, y)
def newSlotArray():
    main.editing = SlotArray(main.obj.extra_padding+main.obj.slotSize[0]*objindex, main.obj.extra_padding+main.obj.slotSize[1]*objindex)
    main.editmode = True

# Editor control
def unload():
    try:
        main.obj.objects
    except:
        main.obj.objects = []
    i = 0
    while i < len(main.obj.objects):
        if main.obj.objects[i].id == main.editing.id:
            main.obj.objects[i] = main.editing
            main.editing = None
            main.editmode = False
            main.REdisplay()
            return
        i += 1
    main.obj.objects.append(main.editing)
    main.editing = None
    main.editmode = False
    main.REdisplay()
def erase():
    global objindex
    try:
        main.obj.objects
    except:
        main.obj.objects = []
    i = 0
    while i < len(main.obj.objects):
        if main.obj.objects[i].id == main.editing.id:
            main.obj.objects[i].erase()
            del main.obj.objects[i]
            main.editing = None
            main.editmode = False
            main.REdisplay()
            objindex -= 1
            return
        i += 1
    main.editing.erase()
    main.editing = None
    main.editmode = False
    main.REdisplay()
    objindex -= 1
def edit(id):
    main.editing = main.obj.objects[id]
    main.editmode = True