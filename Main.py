from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk # will need to pip install Pillow unless i remove the section that uses it (i'm too lazy to try and do it without it rn)
from pygame import mixer
import random
import os

# clears the terminal on game start
os.system("cls")

# enemy definitions
class Enemy: # code finally made by me
    def __init__(self, name, max_hp, defense, attack):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.defense = defense
        self.attack = attack
    def take_damage(self, player_attack):
        damage = max(1, player_attack - self.defense)
        self.hp = max(0, self.hp - damage)  # ✅ fixed line
        return damage
    def is_alive(self):
        return self.hp > 0

class Goblin(Enemy):
    def __init__(self):
        super().__init__(name="Goblin", max_hp=10, defense=2, attack=5)
goblin = Goblin()
print(goblin.is_alive())

def up_input(event):
    global selbutton # idk why i need so many globals for one thing but i can't be bothered rn to try to fix it if it works well
    if selbutton > 0:
        selbutton -= 1
    if mapOn == False and player_x > 0 and inBattle == False:
        locationButtonSelected("north")

def down_input(event):
    global selbutton
    if selbutton < 100:
        selbutton += 1
    if mapOn == False and player_x < len(map)-1 and inBattle == False:
        locationButtonSelected("south")

def left_input(event):
    if mapOn == False and player_y > 0 and inBattle == False:
        locationButtonSelected("west")

def right_input(event):
    if mapOn == False and player_y < len(map[0])-1 and inBattle == False:
        locationButtonSelected("east")

def space_input(event): # space input for selecting button ## not designed yet
    pass
    mixer.init()
    mixer.Sound("jewjewjew.mp3").play() # appoligies for bad test mp3 if i didn't remove this

# function to open and close the map
def open_map(event):
    global mapOn, map_frame
    if mapOn:
        mapOn = False
        map_frame.destroy()  # 💡 remove the whole frame ## chat gave this
        areaName = map[player_x][player_y]
        locationScreen(areaName, areaName+".png", areaDesc[areaName])
    else:
        mapOn = True
        for widget in container.winfo_children():
            widget.destroy()
        map_frame = tk.Frame(container, height=int(root.winfo_screenheight()))   # recreate it fresh each time
        map_frame.pack(anchor="center")
        draw_map()

def draw_map(): # chat GPT made this function for me, it was surprisingly good ngl, i don't really understand how it works but it does
    """Draw or redraw the map grid."""
    for widget in map_frame.winfo_children():
        widget.destroy()  # clear old cells

    cell_labels.clear()

    for r, row in enumerate(map):
        row_labels = []
        for c, cell in enumerate(row):
            # Determine color
            if [r, c] == [player_x, player_y]:
                bg_color = "red"  # player
            elif cell.startswith("forest"):
                bg_color = "green"
            elif cell == "village":
                bg_color = "yellow"
            else:
                bg_color = "grey"
            
            width = int(root.winfo_screenwidth()/75) # idk why /5 doesn't work as it should 
            label = tk.Label(
                map_frame,
                text=cell,  # text=cell[:2] for abbreviation of first 2 letters
                bg=bg_color,
                width=width, 
                height=int(width/3),  # make height proportional to width
                relief="raised",
                borderwidth=1
            )
            label.grid(row=r, column=c, padx=1, pady=1)
            row_labels.append(label)
        cell_labels.append(row_labels)

# function to open and close the inventory
def open_inventory():
    """Toggle the inventory screen."""
    global invOn, inventory_frame, equipped_frame
    if invOn:
        invOn = False
        inventory_frame.destroy()
        equipped_frame.destroy()
        areaName = map[player_x][player_y]
        locationScreen(areaName, areaName+".png", areaDesc[areaName])
    else:
        invOn = True
        for widget in container.winfo_children():
            widget.destroy()
        # inventory frame
        inventory_frame = tk.Frame(container)
        inventory_frame.pack(expand=True, fill="both")

        # equipped items frame
        equipped_frame = tk.Frame(container, relief="sunken", borderwidth=2)
        equipped_frame.pack(side="right", fill="y")
        
        draw_inventory()
        draw_equipped()

def draw_inventory(): # chat made this section too, sadly i don't understand it as well as the map one
    """Draw inventory in a grid."""
    # Make frame resizable
    rows = len(inventory) // 3 + (len(inventory) % 3 > 0)  # Calculate needed rows
    cols = len(inventory) if len(inventory) < 3 else 3  # Max 3 columns
    for r in range(rows):
        inventory_frame.rowconfigure(r, weight=1)
    for c in range(cols):
        inventory_frame.columnconfigure(c, weight=1)
    
    # Fill with items
    i = 0
    for item, qty in inventory.items():
        r = i // cols
        c = i % cols

        # Item name and qty
        frame = tk.Frame(inventory_frame, relief="ridge", borderwidth=2)
        frame.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)

        lbl = tk.Label(frame, text=f"{item}\nQty: {qty}", font=("Arial", 12))
        lbl.pack(pady=5)

        # Buttons for interactions
        btn_use = tk.Button(frame, text="Use", command=lambda i=item: use_item(i))
        btn_drop = tk.Button(frame, text="Drop", command=lambda i=item: drop_item(i))
        btn_equip = tk.Button(frame, text="Equip", command=lambda i=item: equip_item(i))

        btn_use.pack(side="left", expand=True, fill="x", padx=2, pady=2)
        btn_drop.pack(side="left", expand=True, fill="x", padx=2, pady=2)
        btn_equip.pack(side="left", expand=True, fill="x", padx=2, pady=2)

        # my sloppy code to add a back button to each item frame, not ideal but it works
        btn_back = tk.Button(frame, text="Back", command=open_inventory)
        btn_back.pack(side="bottom", expand=True, fill="x", padx=2, pady=2)

         # Increment index
        i += 1

def draw_equipped():
    if equip_item is None:  # If no items are equipped, skip drawing
        return
    for widget in equipped_frame.winfo_children():
        widget.destroy()

    tk.Label(equipped_frame, text="Equipped Items", font=("Arial", 14, "bold")).pack(pady=5)

    for slot, item in equipped.items():
        text = f"{slot}: {item if item else 'None'}"
        tk.Label(equipped_frame, text=text, font=("Arial", 12)).pack(anchor="w", padx=10, pady=2)

# === Interaction functions ===
def use_item(item):
    if inventory[item] > 0:
        inventory[item] -= 1
        messagebox.showinfo("Used Item", f"You used a {item}!")
        refresh_inventory()
    else:
        messagebox.showwarning("Out of Stock", f"No {item} left!")

def drop_item(item):
    if inventory[item] > 0:
        inventory[item] -= 1
        messagebox.showinfo("Dropped Item", f"You dropped a {item}.")
        refresh_inventory()
    else:
        messagebox.showwarning("Empty", f"No {item} to drop!")

def equip_item(item):
    """Equip an item into a suitable slot."""
    if "Sword" in item or "Bow" in item:
        equipped["Weapon"] = item
    elif "Shield" in item:
        equipped["Shield"] = item
    else:
        equipped["Accessory"] = item

    messagebox.showinfo("Equipped", f"You equipped {item}!")
    draw_equipped()

def refresh_inventory():
    """Redraw the inventory after changes."""
    for widget in inventory_frame.winfo_children():
        widget.destroy()
    draw_inventory()

def locationButtonSelected(option):
    print(f"{option} selected")
    global player_x, player_y
    if option == "north":
        player_x -= 1
    elif option == "south":
        player_x += 1
    elif option == "west":
        player_y -= 1
    elif option == "east":
        player_y += 1
    elif option == "inventory":
        open_inventory()
        return
    elif option == "stats": # not implemented yet
        pass
    elif option == "map":
        open_map(None) # None because it needs an event argument but we don't have one here
        return # return to prevent reloading location screen
    
    areaName = map[player_x][player_y]
    locationScreen(areaName, areaName+".png", areaDesc[areaName])
    
def locationScreen(areaName, areaImage, areaDesc):
    enemy = check_encounter(areaName.lower())
    if enemy:
        enemy_encounter(enemy)
        return
    
    for widget in container.winfo_children():
        widget.destroy()
    # area name
    areaFont = Font(family="Times New Roman", size=int(root.winfo_screenheight()*0.024), weight="bold", underline=1) # creates a custom font that maybe used where ever
    labelAreaName = tk.Label(master=container, text=areaName, fg="black", anchor="center", font=areaFont)
    labelAreaName.columnconfigure(0)
    
    # area image
    img = Image.open(areaImage) # opens the image as original size
    img = img.resize((int(root.winfo_screenwidth()*0.75), int(root.winfo_screenheight()*0.5)), Image.LANCZOS) # resizes image to acomidate window size   ## also didn't need the use of PILLOW as i ended up using percentages which tkinter already handles...   ### also don't understand LANCZOS or what it is
    img = ImageTk.PhotoImage(img)
    imageLabel = tk.Label(container, image=img)
    imageLabel.image = img # keeps the reference alive otherwise tkinter will garbage-collect it, otherwise image will not appear when ran

    # area description
    descFont = Font(family="Arial", size=12)
    labelAreaDesc = tk.Label(master=container, text=areaDesc, font=descFont, wraplength=int(root.winfo_screenwidth()*0.65))

    # area options
    list = ['North', 'East', 'West', 'South', 'Inventory', 'Stats', 'Map'] # list of options for the area, will be changed later to be dynamic
    listnum = len(list)
    frame = tk.Frame(container)
    x = -1 # i couldn't figure out how to make it more effient so ima just use x as a counter...
    for i in range(round(listnum/2+0.1)): # +0.1 is to prevent round to even
        for j in range(2):
            x += 1
            if x != listnum:
                BG="Blue"
                if i == selbutton:
                    BG="Red"
                label = tk.Button(master=frame, bg=BG, text=f"{list[x]}", command=lambda option=list[x]: locationButtonSelected(option.lower()), width=20, height=2)
                label.grid(row=i, column=j, padx=5, pady=5)
            else:
                label.grid_configure(row=i, column=j-1, columnspan=2)

    # packing the screen elements onto the tab
    labelAreaName.pack()
    imageLabel.pack()
    labelAreaDesc.pack()
    frame.pack()

def check_encounter(area_name):
    possible_enemies = enemies_by_area.get(area_name, [])
    if not possible_enemies:
        return None
    if random.random() < 0.1:  # 10% chance
        # clone enemy so each fight starts fresh
        base_enemy = random.choice(possible_enemies)
        return Enemy(base_enemy.name, base_enemy.max_hp, base_enemy.defense, base_enemy.attack)
    return None

def enemy_encounter(enemy: Enemy):
    global inBattle
    inBattle = True

    for widget in container.winfo_children():
        widget.destroy()

    tk.Label(container, text=f"A wild {enemy.name} appears!", font=("Arial", 16)).pack(pady=10)

    hp_label = tk.Label(container, text=f"HP: {enemy.hp}/{enemy.max_hp}", font=("Arial", 12))
    hp_label.pack(pady=5)

    def attack():
        damage = enemy.take_damage(5)  # player attack = 5 for now
        hp_label.config(text=f"HP: {enemy.hp}/{enemy.max_hp}")
        tk.Label(container, text=f"You dealt {damage} damage!").pack()

        if not enemy.is_alive():
            tk.Label(container, text=f"You defeated {enemy.name}!", fg="green").pack()
            global inBattle
            inBattle = False
            areaName = map[player_x][player_y]
            container.after(2000, lambda: locationScreen(areaName, areaName+".png", areaDesc[areaName]))

    def run():
        global inBattle, areaName
        inBattle = False
        areaName = map[player_x][player_y]
        container.after(500, lambda: locationScreen(areaName, areaName+".png", areaDesc[areaName]))

    tk.Button(container, text="Attack", command=attack).pack(pady=5)
    tk.Button(container, text="Run", command=run).pack(pady=5)


root = tk.Tk()
root.title("Adventure game")
root.state("zoomed") # maximises the window to "fullscreen"

# button binds
root.bind("<w>", up_input)
root.bind("<s>", down_input)
root.bind("<a>", left_input)
root.bind("<d>", right_input)
root.bind("<space>", space_input)
root.bind("<m>", open_map)

## resize screen bind? for if the player wants the screen bigger or smaller -- not important rn

# values created for testing/ on game open
# selected button
selbutton = 0

# map of game
map = [ # this map is rotated 90 degrees clockwise compared to normal cartesian coords, so map[x][y] instead of map[y][x]
    ["volcanic_outlands", "volcano_2", "tundra_1", "tundra_2", "tundra_mountain_tops"],
    ["volcano_2", "volcano_1", "forest_1", "tundra_1", "tundra_2"],
    ["volcano_1", "forest_1", "village",   "forest_1", "ocean_1"],
    ["forest_2", "forest_2", "forest_1", "ocean_1", "ocean_2"],
    ["forest_2", "forest_2", "forest_2", "ocean_2", "ocean_depths"],
]
areaDesc = {
    "volcanic_outlands": "The ground is scorched and cracked, with rivers of molten lava cutting through the landscape. The air is thick with smoke and ash, making it difficult to breathe. Jagged rocks and sparse, charred vegetation dot the area, hinting at the harsh conditions that dominate this fiery terrain.",
    "volcano_2": "You stand on the slopes of an active volcano, where the ground trembles beneath your feet. The air is hot and filled with the scent of sulfur, while occasional bursts of smoke and ash rise from the crater above. The landscape is rugged, with hardened lava flows and sparse vegetation struggling to survive in this volatile environment.",
    "volcano_1": "The volcano looms above, its peak shrouded in smoke. The ground is uneven and rocky, with patches of hardened lava and sparse, resilient plants. The air is warm and carries the faint scent of sulfur, reminding you of the volcano's dormant power.",
    "tundra_1": "The tundra stretches out before you, a vast expanse of flat, treeless land covered in a mix of grasses, mosses, and lichens. The ground is often frozen, with patches of snow and ice lingering even in warmer months. The air is crisp and cold, carrying the faint scent of earth and distant water.",
    "tundra_2": "The tundra is a stark, open landscape where low-lying vegetation like mosses, lichens, and hardy grasses dominate. The ground is often frozen, with patches of snow and ice persisting year-round. The air is cold and dry, with a clear, expansive sky overhead.",
    "tundra_mountain_tops": "The mountain tops rise sharply, their peaks capped with snow and ice. The air is thin and cold, making each breath a challenge. Jagged rocks and sparse alpine vegetation cling to the slopes, while the view stretches out to reveal the vast tundra below.",
    "forest_1": "Tall trees rise around you, their dense canopy blotting out much of the sky. Shafts of light pierce through the leaves, illuminating patches of moss and tangled roots. The air is cool and damp, carrying the earthy scent of soil and distant foliage. Every sound—whether a birdcall or the snap of a twig—seems to echo deeper than it should.",
    "forest_2": "You find yourself in a dense forest where towering trees with thick trunks and lush canopies create a shaded, almost mystical atmosphere. The ground is carpeted with fallen leaves, moss, and ferns, while the air is filled with the earthy scent of damp wood and foliage. Sunlight filters through the leaves, casting dappled patterns on the forest floor.",
    "village": "You enter a quaint village nestled among rolling hills and surrounded by lush forests. Cobblestone streets wind between charming cottages with thatched roofs and colorful gardens. The air is filled with the sounds of daily life—children playing, merchants calling out their wares, and the distant clatter of horse-drawn carts. The scent of fresh bread and blooming flowers adds to the village's welcoming atmosphere.",
    "ocean_1": "You stand on a sandy beach where the waves gently lap at the shore. The ocean stretches out endlessly before you, its surface shimmering under the sunlight. Seagulls call overhead, and the salty breeze carries the invigorating scent of the sea. The beach is dotted with seashells and smooth stones, while distant ships sail on the horizon.",
    "ocean_2": "The ocean is a vast expanse of deep blue, with waves that rise and fall rhythmically. The salty air is filled with the cries of seabirds, and the scent of seaweed and brine is strong. The horizon seems to stretch infinitely, where the sky meets the water in a seamless blend of colors. Occasional glimpses of marine life, like dolphins or seabirds diving, add to the ocean's dynamic beauty.",
    "ocean_depths": "Beneath the surface, the ocean depths are a mysterious and otherworldly realm. Sunlight barely penetrates the dark waters, creating an eerie twilight where strange and colorful creatures glide silently. Coral reefs teem with life, while larger predators move in the shadows. The water is cool and filled with the scent of salt and the faint hum of underwater currents."
} # ai generated area descriptions, may need to be changed later

mapOn = False # whether the map is on screen or not

invOn = False # whether the inventory is on screen or not
inventory_frame = None
equipped_frame = None
inventory = {
    "Potion": 3,
    "Sword": 1,
    "Shield": 1,
    "Herb": 5,
    "Bow": 1,
    "Arrow": 20
}

# Equipped items tracker
equipped = {
    "Weapon": None,
    "Shield": None,
    "Accessory": None
}

# starting coords of player
player_x, player_y = 2,2

# enemies by area
enemies_by_area = {
    "forest_1": [Goblin(), Enemy("Wolf", 15, 3, 5)],   
    "forest_2": [Enemy("Wolf", 15, 3, 5)],
    "village": [Enemy("Bandit", 20, 4, 6)]
} # can add more enemies and areas later


# to hold references to cell labels    ## started using copilot to help explain code, it suggested this comment which is actually pretty good so imma keep it
cell_labels = []

# in battle or not
inBattle = False

map_frame = tk.Frame(root)
map_frame.pack(padx=10, pady=10)



areaName = map[2][2] # starting area name
container = tk.Frame(root)
container.pack(fill="both", expand=True)
testDesc = "Tall trees rise around you, their dense canopy blotting out much of the sky. Shafts of light pierce through the leaves, illuminating patches of moss and tangled roots. The air is cool and damp, carrying the earthy scent of soil and distant foliage. Every sound—whether a birdcall or the snap of a twig—seems to echo deeper than it should."
locationScreen(areaName, areaName+".png", areaDesc[areaName]) # images must be png otherwise need Pillow import to change that but idk how to, and don't feel like trying so ima manually change to png


##### random ass bug i just found after not touching the code for hours that i don't have time to try to fix,
##### where the next screen when moving with wasd (idk if buttons work) it won't open the screen unless you encounter an enemy
##### also you can encounter an enemy when opening and closing the map... but it could be considered a feature so idc

root.mainloop()