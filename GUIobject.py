import os.path
import __main__ as main
import PIL.Image
import editor
from pgerom.save import save as f_save
from pgerom.save import load as f_load

def draw_box(image:PIL.Image, startX, startY, w, h, color):
    x, y = startX, startY
    while x < startX+w:
        while y < startY+h:
            image.putpixel((x, y), color)
            y += 1
        y = startY
        x += 1
    return image
def generate_background(sizeX, sizeY, background_color, border_color, border_high, border_low):
    image = PIL.Image.new("RGBA", (sizeX, sizeY), background_color)
    # Top - left
    image = draw_box(image, 0, 0, 4, 4, border_high)
    image.putpixel((0, 0), (0, 0, 0, 0))
    image.putpixel((1, 0), (0, 0, 0, 0))
    image.putpixel((0, 1), (0, 0, 0, 0))
    image.putpixel((1, 1), border_color)
    image.putpixel((0, 2), border_color)
    image.putpixel((2, 0), border_color)
    image.putpixel((0, 3), border_color)
    image.putpixel((3, 0), border_color)

    # Top - right
    image.putpixel((sizeX-1, 0), (0, 0, 0, 0))
    image.putpixel((sizeX-2, 1), (0, 0, 0, 0))
    image.putpixel((sizeX-2, 2), border_color)
    image.putpixel((sizeX-4, 1), border_high)
    image.putpixel((sizeX-4, 2), border_high)
    image.putpixel((sizeX-3, 1), border_color)
    image.putpixel((sizeX-2, 3), border_low)
    image.putpixel((sizeX-3, 3), border_low)
    image.putpixel((sizeX-1, 1), (0, 0, 0, 0))
    image.putpixel((sizeX-1, 2), (0, 0, 0, 0))
    image.putpixel((sizeX-1, 3), border_color)
    image.putpixel((sizeX-2, 0), (0, 0, 0, 0))
    image.putpixel((sizeX-3, 0), (0, 0, 0, 0))
    image.putpixel((sizeX-4, 0), border_color)

    # Bottom - left
    image.putpixel((0, sizeY-1), (0, 0, 0, 0))
    image.putpixel((0, sizeY-3), (0, 0, 0, 0))
    image.putpixel((2, sizeY-1), (0, 0, 0, 0))
    image.putpixel((3, sizeY-1), border_color)
    image.putpixel((2, sizeY-2), border_color)
    image.putpixel((1, sizeY-3), border_color)
    image.putpixel((0, sizeY-4), border_color)
    image.putpixel((1, sizeY-1), (0, 0, 0, 0))
    image.putpixel((0, sizeY-2), (0, 0, 0, 0))
    image.putpixel((1, sizeY-2), (0, 0, 0, 0))
    image.putpixel((3, sizeY-2), border_low)
    image.putpixel((3, sizeY-3), border_low)
    image.putpixel((1, sizeY-4), border_high)
    image.putpixel((2, sizeY-4), border_high)

    # Bottom - right
    image = draw_box(image, sizeX-4, sizeY-4, 4, 4, border_low)
    image.putpixel((sizeX-1, sizeY-1), (0, 0, 0, 0))
    image.putpixel((sizeX-1, sizeY-2), (0, 0, 0, 0))
    image.putpixel((sizeX-2, sizeY-1), (0, 0, 0, 0))
    image.putpixel((sizeX-3, sizeY-1), border_color)
    image.putpixel((sizeX-1, sizeY-3), border_color)
    image.putpixel((sizeX-2, sizeY-2), border_color)

    # Top
    image = draw_box(image, 2, 0, sizeX-6, 1, border_color)
    image = draw_box(image, 2, 1, sizeX-6, 2, border_high)

    # Bottom
    image = draw_box(image, 4, sizeY-1, sizeX-7, 1, border_color)
    image = draw_box(image, 4, sizeY-3, sizeX-7, 2, border_low)

    # Left
    image = draw_box(image, 0, 2, 1, sizeY-6, border_color)
    image = draw_box(image, 1, 2, 2, sizeY-6, border_high)

    # Right
    image = draw_box(image, sizeX-1, 3, 1, sizeY-6, border_color)
    image = draw_box(image, sizeX-3, 3, 2, sizeY-6, border_low)
    return image
def generate_slot(w, h, background_color, border_high, border_low):
    image = PIL.Image.new("RGBA", (w, h), background_color)
    x, y = 0, 0
    while x < w-1:
        image.putpixel((x, y), border_low)
        image.putpixel((x+1, h-1), border_high)
        x += 1
    x = 0
    while y < h-1:
        image.putpixel((x, y), border_low)
        image.putpixel((w-1, y+1), border_high)
        y += 1
    return image
class slotBarObject:
    def __init__(self, x, y, items=1, align='center'):
        self.x = x
        self.y = y
        self.align = align
        self.items = items
class gui:
    def __init__(self, sizeX, sizeY, player_inventory = True, player_inventory_align = "center", padding = 4):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.padding = padding
        self.extra_padding = padding+3
        self.imageX = max(256, sizeX)
        self.imageY = max(256, sizeY)
        self.resources = []
        self.objects = []
        self.slotBars = {}
        self.slotSize = (18, 18)
        self.player_inventory = player_inventory
        self.player_inventory_align = player_inventory_align
        self.background_color = (198, 198, 198)
        self.border_color = (0, 0, 0)
        self.border_high = (255, 255, 255)
        self.border_low = (85, 85, 85)
        self.slot_background_color = (139, 139, 139)
        self.slot_border_high = (255, 255, 255)
        self.slot_border_low = (55, 55, 55)
        self.image = PIL.Image.new("RGBA", (self.imageX, self.imageY), (0, 0, 0, 0))
    def generate(self):
        self.image.paste(generate_background(self.sizeX, self.sizeY, self.background_color, self.border_color, self.border_high, self.border_low))
        self.slotcount = 0
        for slotBarKey in list(self.slotBars):
            slotBar = self.slotBars[slotBarKey]
            x, y = None, None
            if slotBar.align.startswith("center"):
                if slotBar.align == "center" or slotBar.align.endswith("X"):
                    x = (self.sizeX - (slotBar.items*self.slotSize[0])) / 2
                if slotBar.align == "center" or slotBar.align.endswith("Y"):
                    y = (self.sizeY - (slotBar.items*self.slotSize[1])) / 2
            if not x:
                x = slotBar.x
            if not y:
                y = slotBar.y
            exit = x + slotBar.items*self.slotSize[0]
            slot = generate_slot(*self.slotSize, self.slot_background_color, self.slot_border_high, self.slot_border_low)
            while x < exit:
                self.image.paste(slot, (x, y))
                self.slotcount += 1
                x += self.slotSize[0]
        if self.player_inventory:
            length = self.slotSize[0]*9
            if self.player_inventory_align == 'center':
                x = int( (self.sizeX - length) / 2 )
            elif self.player_inventory_align == 'left':
                x = self.extra_padding
            elif self.player_inventory_align == 'right':
                x = self.sizeX - length - self.extra_padding
            y = self.sizeY - self.slotSize[1] - self.extra_padding
            for i in range(9):
                self.image.paste(generate_slot(*self.slotSize, self.slot_background_color, self.slot_border_high, self.slot_border_low), (x+(self.slotSize[0]*i), y))
            y = self.sizeY - self.slotSize[1]*2 - self.extra_padding*2
            for i2 in range(3):
                for i in range(9):
                    self.image.paste(generate_slot(*self.slotSize, self.slot_background_color, self.slot_border_high, self.slot_border_low), (x+(self.slotSize[0]*i), y-(self.slotSize[1]*i2)))
    def save(self, location):
        self.image.save(location)
    def save_onlygui(self, location):
        self.image.crop((0, 0, self.sizeX, self.sizeY)).save(location)
    def savedata(self, location):
        f_save(location, self)
    def compile(self):
        q = '{}'
        final = f'''GUIobject export ~ By Red
Please use these values when making your screen. It will insure the alignment of the slots.
Project name: "{main.project_name}"
SlotSize: {self.slotSize}
Size of screen: {self.sizeX}, {self.sizeY}
!!! Please keep a record of your current slots ID and X and Y!!!
```
int currentID = 0;
int x;
int y;
```
slot count: {self.slotcount}

'''
        for editorI in self.objects:
            if type(editorI) == editor.SlotArray:
                final += f'''SlotArray ```
for (int row=0; row < {editorI.sizeY}; row++)
{q[0]}
    y = {editorI.y+1} + {self.slotSize[1]} * row;
    for (int column=0; column < {editorI.sizeX}; column++)
    {q[0]}
        x = {editorI.x+1} + {self.slotSize[0]} * column;
        this.addSlot(new Slot((IInventory) tile, currentID, x, y));
        currentID++;
    {q[1]}
{q[1]}
```

'''
        if self.player_inventory:
            length = self.slotSize[0]*9
            if self.player_inventory_align == 'center':
                x = int( (self.sizeX - length) / 2 )
            elif self.player_inventory_align == 'left':
                x = self.extra_padding
            elif self.player_inventory_align == 'right':
                x = self.sizeX - length - self.extra_padding
            y = self.sizeY - self.slotSize[1] - self.extra_padding
            final += f'''PlayerInventory [\n'''
            final += f'''   hotbar = ```
for (int col = 0; col < 9; col++) {q[0]}
	this.addSlot(new Slot(playerInventory, col, {x+1} + col * {self.slotSize[0]}, {y+1}));
{q[1]}
```

'''
            y = self.sizeY - self.slotSize[1] * 4 - self.extra_padding * 2
            final += f'''    main = ```
for (int row=0; row < 3; row++)
{q[0]}
    y = {y+1} + {self.slotSize[1]} * row;
    for (int column=0; column < 9; column++)
    {q[0]}
        x = {x+1} + {self.slotSize[0]} * column;
        int index = row * 9 + column + 9;
        this.addSlot(new Slot(playerInventory, index, x, y));
    {q[1]}
{q[1]}
```
]
'''
            return final
def load(location):
    return f_load(location)[0]
