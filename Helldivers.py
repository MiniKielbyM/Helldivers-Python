# global functions
import sys
import os
import keyboard
import time
import re
import random
import math
try:
    import ctypes
except ImportError:
    ctypes = None
try:
    import msvcrt
except ImportError:
    msvcrt = None
try:
    import termios
except ImportError:
    termios =  None
import heapq
from fractions import Fraction
import copy
import asyncio
import websockets
import socket

# Regex to strip ANSI escape sequences
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

x = os.get_terminal_size().columns
y = os.get_terminal_size().lines
def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  #assigns a free port
        return s.getsockname()[1]
async def ping_port(host, port):
    uri = f"ws://{host}:{port}"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send("ping")
            response = await websocket.recv()
            if response == "pong":
                print(f"✔ WebSocket server responded to ping on {port}")
                return True
    except Exception as e:
        pass
    return False
async def scan_ports(host="localhost", start=8000, end=8010):
    results = []
    for port in range(start, end + 1):
        if await ping_port(host, port):
            results.append(port)
    return results
def print_slow(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()
# Function to hide the cursor in the terminal
def hide_cursor():
    if os.name is 'nt':

        class CONSOLE_CURSOR_INFO(ctypes.Structure):
            _fields_ = [("dwSize", ctypes.c_int),
                        ("bVisible", ctypes.c_bool)]

        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        cursor_info = CONSOLE_CURSOR_INFO()
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(cursor_info))
        cursor_info.bVisible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(cursor_info))
    else:
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()
def show_cursor():
    if os.name is 'nt':
        class CONSOLE_CURSOR_INFO(ctypes.Structure):
            _fields_ = [("dwSize", ctypes.c_int),
                        ("bVisible", ctypes.c_bool)]

        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        cursor_info = CONSOLE_CURSOR_INFO()
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(cursor_info))
        cursor_info.bVisible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(cursor_info))
    else:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
if os.name is 'nt':
    def flush_input():
        while msvcrt.kbhit():
            msvcrt.getch()
else:
    def flush_input():
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
def clear():
    # Clear the terminal screen
    if os.name is 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and Mac
        os.system('clear')
    flush_input()
clear()
if x < 90 or y < 6:
    print("Please resize your terminal to at least 91 rows and 6 columns.")
    exit()
def visible_length(s):
    return len(ansi_escape.sub('', s))
def center_text_x(text, width):
    lines = text.split('\n')
    centered_lines = []
    for line in lines:
        pad = (width - visible_length(line)) // 2
        centered_line = ' ' * max(pad, 0) + line
        centered_lines.append(centered_line)
    return '\n'.join(centered_lines)
def print_centered(text):
    print(center_text_x(text, x))
def parse_level(level,enemies=[], actionItem="", debug=False):
    final = "\033[33m\n" + level[0][5] + "\n\n\033[0m"
    yAt = 0
    xAt = 0
    for yL in level[1]:
        for xL in yL:
            if xL is 0:
                final += "\033[38;2;160;99;4m██\033[0m"
            elif xL is 1:
                final += "\033[38;2;200;200;200m▒▒\033[0m"
            elif xL is 2:
                final += "\033[38;2;200;200;200m██\033[0m"
            elif xL is 3:
                if debug:
                    print("enemy at:")
                    print(xAt, end=" ")
                    print(yAt)
                if enemies != []:
                    for enemy in enemies:
                        if enemy[1] is xAt and enemy[2] is yAt:
                            final += f"\033[48;5;196;38;2;0m{enemy[0][1]}\033[0m"
                            break
                        if enemy is enemies[len(enemies)-1]:
                            final += "\033[38;2;0;m??\033[0m"
                            break
                else:
                    final += "\033[38;2;255;0;0m??\033[0m"
            elif xL is 4:
                final += "\033[38;2;255;0;0m▚▚\033[0m"
            elif xL is 5:                    
                if debug:
                    print("player at:")
                    print(xAt, end=" ")
                    print(yAt)
                final += "\033[38;2;0;255;0mOO\033[0m"
            elif xL is 6:
                if debug:
                    print("interactable at:")
                    print(xAt, end=" ")
                    print(yAt)
                final += "\033[38;2;0;0;255;48;5;226m⏺ \033[0m"
            elif xL is 7:
                final += "\033[38;2;255;255;0m▓▓\033[0m"
            elif xL is 8:
                final += "\033[38;2;255;0;255m▚▚\033[0m"
            elif xL is 9:
                if debug:
                    print("hellbomb at:")
                    print(xAt, end=" ")
                    print(yAt)
                final += "\033[38;2;255;255;0;48;2;0;0;0mꗈ \033[0m"
            elif xL is 10:
                if debug:
                    print("enemy at:")
                    print(xAt, end=" ")
                    print(yAt)
                if enemies != []:
                    for enemy in enemies:
                        if enemy[1] is xAt and enemy[2] is yAt:
                            final += f"\033[48;2;255;255;0;38;2;0m{enemy[0][1]}\033[0m"
                            break
                        if enemy is enemies[len(enemies)-1]:
                            final += "\033[38;2;0;m??\033[0m"
                            break
            elif xL is 11:
                if debug:
                    print("enemy at:")
                    print(xAt, end=" ")
                    print(yAt)
                if enemies != []:
                    for enemy in enemies:
                        if enemy[1] is xAt and enemy[2] is yAt:
                            final += f"\033[48;2;0;255;0;38;2;0m{enemy[0][1]}\033[0m"
                            break
                        if enemy is enemies[len(enemies)-1]:
                            final += "\033[38;2;0;m??\033[0m"
                            break
                else:
                    final += "\033[38;2;255;0;255m▚▚\033[0m"
            elif xL is 12:
                try:
                    if playerIndexTurn == 0:
                        final += "\033[38;2;255;153;0;48;2;0;0;0m><\033[0m"
                    elif playerIndexTurn == 1:
                        final += "\033[38;2;0;63;255;48;2;0;0;0m><\033[0m"
                    elif playerIndexTurn == 2:
                        final += "\033[38;2;0;150;0;48;2;0;0;0m><\033[0m"
                    elif playerIndexTurn == 3:
                        final += "\033[38;2;192;0;151;48;2;0;0;0m><\033[0m"
                except:
                    final += "\033[38;2;255;0;255m▚▚\033[0m"
            else: 
                final += "\033[38;2;255;0;255m▚▚\033[0m"
            xAt += 1
        final += "\n"
        yAt += 1
        xAt = 0
    final += actionItem + "\n"
    for i in range(len(level[0][6])):
        j = ""
        if i == 0:
            j = f"\033[48;2;255;153;0;38;2;255;255;255m {str(level[0][6][i][13])[0]}{str(i+1)} \033[0m\033[38;2;255;153;0m\tHP {level[0][6][i][5]}/{level[0][6][i][6]} \033[0m"
            for t in range(x-visible_length(j)-3):
                j += " "
            final += j + "\n\n"
        elif i == 1:
            j = f"\033[48;2;0;63;255;38;2;255;255;255m {str(level[0][6][i][13])[0]}{str(i+1)} \033[0m"
            for t in range(x-visible_length(j)-3):
                j += " "
            final += j + "\n\n"
        elif i == 2:
            j = f"\033[48;2;0;150;0;38;2;255;255;255m {str(level[0][6][i][13])[0]}{str(i+1)} \033[0m"
            for t in range(x-visible_length(j)-3):
                j += " "
            final += j + "\n\n"
        elif i == 3:
            j = f"\033[48;2;192;0;151;38;2;255;255;255m {str(level[0][6][i][13])[0]}{str(i+1)} \033[0m"
            for t in range(x-visible_length(j)-3):
                j += " "
            final += j + "\n\n"
    return final
def hypotenuse_los(grid, start, end, view_distance, debug = False, grenade = False):
    if debug:
        print("Calculating line of sight...")  # Debug output
    x0, y0 = start
    x1, y1 = end
    dx = x1 - x0
    dy = y1 - y0
    dist = math.hypot(dx, dy)
    if round(dist) > view_distance:
        if debug:
            print(f"Distance {dist} exceeds view distance {view_distance}.")  # Debug output
        return False
    steps = round(dist * 2)  # higher multiplier = smoother line
    if steps is 0:
        steps = 1
    if debug:
        print(f"Calculating line of sight from ({x0}, {y0}) to ({x1}, {y1}) with {steps} steps")  # Debug output
    for step in range(1, steps + 1):  # skip step 0
        t = step / steps
        x = x0 + t * dx
        y = y0 + t * dy
        ix = int(round(x))
        iy = int(round(y))
        if not (0 <= iy < len(grid) and 0 <= ix < len(grid[0])):
            return False  # out of bounds
        val = grid[iy][ix]
        if debug:
            print(f"Checking tile ({ix}, {iy}) with value {val} at step {step}/{steps}")  # Debug output
        if val not in (0, 1, 12):
            if val not in (3, 5) and not grenade:
                if val is grid[y0][x0]:
                    continue  # skip the source tile
                if iy is y1 and ix is x1:
                    if debug:
                        print(f"Reached target tile ({ix}, {iy}) with value {val}.")
                        print("Line of sight is clear.")  # Debug output
                    return True
                if debug:
                    print(f"Blocked by tile ({ix}, {iy}) with value {val}.")
                return False
    if debug:
        print("Line of sight is clear.")  # Debug output
    return True
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance
def get_neighbors(pos, grid):
    x, y = pos
    neighbors = []
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:  # No diagonals
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            if grid[ny][nx] is 0:  # Walkable
                neighbors.append((nx, ny))
    return neighbors
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]  # reverse the path
def find_path(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, tuple(start)))
    
    came_from = {}
    g_score = {tuple(start): 0}
    f_score = {tuple(start): heuristic(tuple(start), goal)}

    closest = tuple(start)
    closest_dist = heuristic(tuple(start), goal)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current is goal:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(current, grid):
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                f_score[neighbor] = f
                heapq.heappush(open_set, (f, neighbor))

                # Keep track of closest reachable node
                h = heuristic(neighbor, goal)
                if h < closest_dist:
                    closest = neighbor
                    closest_dist = h

    # If no path to goal, return path to closest reachable tile
    return reconstruct_path(came_from, closest)
def parseActions(levelMeta, gridMap, action, conditions):
    if action[0] == "clear":
        for clearpos in action[1]:
            gridMap[clearpos[0]][clearpos[1]] = 0
            clear()
            print_centered(f"{parse_level([level[0],gridMap],level[0][0])}")
            time.sleep(0.3)
        action[0] = "set"
        return[gridMap, action, conditions, levelMeta]
    elif action[0] == "set":
        for setpos in reversed(action[1]):
            gridMap[setpos[0]][setpos[1]] = action[2]
            clear()
            print_centered(f"{parse_level([level[0],gridMap],level[0][0])}")
            time.sleep(0.3)
        action[0] = "clear"
        return[gridMap, action, conditions, levelMeta]
    elif action[0] == "damage":
        levelMeta[0][6][playerIndexTurn][5] = 50
        return[gridMap, action, conditions, levelMeta] 
    elif action[0] == "condition":
        if action[1][1] == "set":
            for condition in conditions:
                if condition[0] == action[1][0]:
                    conditions[conditions.index(condition)][1] = action[1][2]
            return[gridMap, action, conditions, levelMeta]
        elif action[1][1] == "add": 
            for condition in conditions:
                if condition[0] == action[1][0]:
                    conditions[conditions.index(condition)][1] += action[1][2]
            return[gridMap, action, conditions, levelMeta]
        elif action[1][1] == "sub":
            for condition in conditions:
                if condition[0] == action[1][0]:
                    conditions[conditions.index(condition)][1] -= action[1][2]
            return[gridMap, action, conditions, levelMeta]
        elif action[1][1] == "mult":
            for condition in conditions:
                if condition[0] == action[1][0]:
                    conditions[conditions.index(condition)][1] *= action[1][2]
            return[gridMap, action, conditions, levelMeta]
        elif action[1][1] == "div":
            for condition in conditions:
                if condition[0] == action[1][0]:
                    if action[1][2] != 0:
                        conditions[conditions.index(condition)][1] /= action[1][2]
            return[gridMap, action, conditions, levelMeta]
        elif action[1][1] == "check":
            for condition in conditions:
                if condition[0] == action[1][0]:
                    if conditions[conditions.index(condition)][1] == action[1][2]:
                        action = parseActions(levelMeta, gridMap, action[1][3], conditions)[1]
            return[gridMap, action, conditions, levelMeta]
def exponential_weighted_choice(arr, decay=0.7):
    weights = [decay ** i for i in range(len(arr))]
    total = sum(weights)
    normalized_weights = [w / total for w in weights]
    return random.choices(arr, weights=normalized_weights, k=1)[0]
os.system('color 06') # sets the background to black

# global variables
Trained = False
Name = "Helldiver"
Ship_Name = "Super Destroyer"
Requisition = 250000
SC = 500
Medals = 0
# Common, Rare, Super
Samples = [100,50,10]
# Patriotic Administration Center, Orbital Cannons, Hangar, Bridge, Engineering Bay, Robotics Workshop
Ship_Mods = [0,0,0,0,0,0,0] 
xHalfStr = ""
for _ in range(int(x/2)-1):
    xHalfStr += " "
if True: #hides all the stats, remove before release
    ## enemies
    # Enemy = ["Enemy Name", "Abbr.", Melee, Melee Damage, Melee AP, Ranged, Ranged Damage, Ranged AP, Range, Distance Moveable, LOS distance, health, armor, max hp]
    Scavenger = ["Scavenger", "SV", True, 5, 0, False, 0, 0, 0, 5, 5, 10, 0, 10]
    Pouncer = ["Pouncer", "PC", True, 5, 0, False, 0, 0, 0, 5, 10, 15, 0, 15]
    Hunter = ["Hunter", "HT", True, 10, 1, False, 0, 0, 0, 5, 5, 10, 5, 10]
    Hive_Guard = ["Hive Guard", "HG", True, 5, 0, False, 0, 0, 0, 2, 5, 15, 30, 15]
    Charger = ["Charger", "CR", True, 30, 20, False, 0, 0, 0, 10, 5, 50, 50, 50]
    Shreiker = ["Shreiker", "SR", True, 10, 5, False, 0, 0, 0, 10, 10, 10, 0, 10]
    Bile_Spewer = ["Bile Spewer", "BS", True, 5, 51, True, 15, 2, 10, 2, 10, 15, 0, 15]
    Stalkers = ["Stalkers", "SK", True, 15, 10, False, 0, 0, 0, 3, 5, 20, 10, 20]
    Bile_Titan = ["Bile Titan", "BT", True, 100, 100, True, 75, 100, 2, 5, 5, 50, 75, 50]
    bugs = [Scavenger, Pouncer, Hunter, Hive_Guard, Charger, Shreiker, Bile_Spewer, Stalkers, Bile_Titan]
    
    Trooper = ["Trooper", "TR", False, 0, 0, True, 5, 0, 2, 5, 10, 10, 0, 10]
    Comissar = ["Comissar", "CM", True, 10, 5, True, 5, 0, 3, 2, 5, 10, 0, 10]
    Scout_Strider = ["Scout_Strider", "ST", True, 25, 10, True, 30, 20, 10, 15, 10, 10, 30, 10]
    Beserker = ["Beserker", "BK", True, 35, 25, False, 0, 0, 0, 2, 5, 25, 10, 25]
    Devistator = ["Devistator", "DV", True, 20, 5, True, 30, 5, 5, 1 , 5, 50, 25, 50]
    Hulk = ["Hulk", "HK", True, 75, 10, True, 50, 100, 2, 2, 5, 30, 75, 30]
    Tank = ["Tank", "TK", True, 20, 100, True, 80, 100, 10, 5, 15, 30, 100, 30]
    Factory_Strider = ["Factory Strider", "FS", True, 100, 100, True, 75, 50, 5, 1, 10, 50, 150, 50]
    bots = [Trooper, Comissar, Scout_Strider, Beserker, Devistator, Hulk, Tank, Factory_Strider]

    Voteless = ["Voteless", "VT", True, 5, 0, False, 0, 0, 0, 5, 5, 5, 0, 5]
    Watcher = ["Watcher", "WC", False, 0, 0, True, 20, 5, 2, 5, 10, 5, 5, 5]
    Overseer = ["Overseer", "OS", True, 50, 0, False, 0, 0, 0, 5, 7, 20, 30, 20]
    Elevated_Overseer = ["Elevated Overseer", "EO", False, 0, 0, True, 20, 5, 5, 1, 5, 20, 15, 20]
    Cresent_Overseer = ["Cresent Overseer", "CO", False, 0, 0, True, 50, 25, 10, 10, 3, 20, 15, 20]
    Flesh_Mob = ["Flesh Mob", "FM", True, 25, 0, False, 0, 0, 0, 4, 5, 200, 0, 200]
    Harvester = ["Harvester", "HV", True, 50, 25, True, 100, 50, 5, 2, 10, 25, 85, 25]
    squids = [Voteless, Watcher, Overseer, Elevated_Overseer, Cresent_Overseer, Flesh_Mob, Harvester]

    ## Weapons
    # Weapon = [Weapon Name, Damage, AP, Range, Ammo, Mag Count, Reload Time, Burst Size, Damage Falloff, Explosive, current ammo, current mags]

    # Primary Weapons
    Liberator_Penetrator = ["Liberator Penetrator", 5, 5, 3, 30, 4, 1, 0, 0, False, 30, 4]
    LAS_5_Scythe = ["LAS-5 Scythe", 1, math.inf, 2, 100, 3, 1, 0, 0, False, 100, 3]
    PLAS_1_Scorcher = ["PLAS-1 Scorcher", 5, 10, 5, 15, 5, 1, 0, 0, False, 15, 5]
    FLAM_66_Torcher = ["FLAM-66 Torcher", 10, 0, 2, 50, 4, 1, 1, 0, False, 50, 4]
    Explosive_Crossbow = ["Explosive Crossbow", 20, 10, 4, 5, 3, 1, 1, 1, True, 5, 3]

    # Secondary Weapons
    LAS_7_Dagger = ["LAS-7 Dagger", 2, math.inf, 1, 500, 1, 3, 0, 0, False, 500, 1]
    P_2_Peacemaker = ["P-2 Peacemaker", 4, 2, 5, 15, 5, 1, 0, 0, False, 15, 5]
    P_19_Redeemer = ["P-19 Redeemer", 5, 0, 3, 100, 5, 1, 0, 0, False, 100, 5]
    GP_31_Ultimatum = ["GP-31 Ultimatum", 10, 10, 3, 1, 2, 2, 5, 1, True, 1, 2]
    P_4_Senator = ["P-4 Senator", 15, 15, 3, 6, 4, 1, 0, 0, False, 6, 4]

    ##Grenades
    #Grenade = [Name, Damage, AP, Aoe, DPS, DPS time]
    G_6_Frag = ["G-6 Frag", 20, 10, 2, 0, 0]
    G_12_High_Explosive = ["G-12 High Explosive", 50, 0, 2, 0, 0]
    G_16_Impact = ["G-16 Impact", 25, 15, 1, 0, 0]
    G_4_Gas = ["G-4 Gas", 10, math.inf , 3, 10, 3]
    G_10_Incindiary = ["G-10 Incendiary", 5, math.inf , 3, 5, 6]
    G_123_Thermite = ["G-123 Thermite", 30, 100, 1, 0, 0]

    ## Armor
    # Armor = [Armor Name, Movement Mod, Armor Stat, Armor Passive]
    B_01_Tactical = ["B-01 Tactical", 0, 35, "Extra Padding"]#+10 armor ✓
    SC_34_Infiltrator = ["SC-34 Infiltrator", 1, 5, "Scout"]#70% enemy sight range against wearer ✓ 
    SA_04_Combat_Technician = ["SA-04 Combat Technician", 0, 25, "Scout"]
    CE_35_Trench_Engineer = ["CE-35 Trench Engineer", 0, 25, "Engineering Kit"]#+2 grenades ✓
    CE_07_Demolition_Specialist = ["CE-07 Demolition Specialist", 1, 5, "Engineering Kit"]
    DP_40_Hero_of_the_Federation = ["DP-40 Hero of the Federation", 0, 25, "Democracy Protects"]#50% chance to live on 1 hp if lethal damage would have been dealt ✓
    FS_23_Battle_Master = ["FS-23 Battle Master", -1, 45, "Fortified"]#50% damage reduction to explosives
    CM_14_Physician = ["CM-14 Physician", 0, 25, "Med-Kit"]#+2 stims ✓, Stims heal 2 turns in a row ✓
    SA_12_Servo_Assisted = ["SA-12 Servo Assisted", 0, 25, "Servo-Assisted"]#+10 hp ✓, 130% throw range ✓
    SA_32_Dynamo = ["SA-32 Dynamo", -1, 45, "Servo-Assisted"]
    PH_9_Predator = ["PH-9 Predator", 1, 5, "Peak Physique"]#200% Melee damage ✓, +5 melee AP ✓
    P_202_Twigsnapper = ["PH-202 Twigsnapper", -1, 45, "Peak Physique"]
    I_09_Heatseeker = ["I-09 Heatseeker", 1, 5, "Inflammable"]#10% fire damage
    I_102_Draconaught = ["I-102 Draconaught", 0, 25, "Inflammable"]
    AF_50_Noxious_Ranger = ["AF-50 Noxious Ranger", 1, 5, "Advanced Filtration"]#20% gas damage
    AF_02_Haz_Master = ["AF-02 Haz-Master", 0, 25, "Advanced Filtration"]
    SR_24_Street_Scout = ["SR-24 Street Scout", 1, 5, "Siege-Ready"]#120% ammo ✓
    SR_18_Roadblock = ["SR-18 Roadblock", -1, 45, "Siege-Ready"]
    IE_12_Righteous = ["IE-12 Righteous", 0, 25, "Integrated Explosives"]#Explode 1 turn after death with 20 damage and 10 ap and 1 Aoe 
    RE_1861_Parade_Commander = ["RE-1861 Parade Commander", 1, 5, "Reinforced Epaulettes"]#150% melee damage ✓, 50% chance of +20 health for the turn ✓
    RE_2310_Honorary_Guard = ["RE-2310 Honorary Guard", 0, 25, "Reinforced Epaulettes"]
    Armors = [B_01_Tactical, SC_34_Infiltrator, SA_04_Combat_Technician, CE_35_Trench_Engineer, CE_07_Demolition_Specialist, DP_40_Hero_of_the_Federation, FS_23_Battle_Master, CM_14_Physician, SA_12_Servo_Assisted, SA_32_Dynamo, PH_9_Predator, P_202_Twigsnapper, I_09_Heatseeker, I_102_Draconaught, AF_50_Noxious_Ranger, AF_02_Haz_Master, SR_24_Street_Scout, SR_18_Roadblock, IE_12_Righteous, RE_1861_Parade_Commander, RE_2310_Honorary_Guard]

    Quasar = [1, "Quasar", 100, 10, True, math.inf, 1, 1, 5, 1, False]
    Expendible_Anti_Tank = [1, "Expendible Anti Tank", 50, 100, True, 2, 0, 0, 5, 1, False]
    Recoilless_Rifle = [3, "Recoilless Rifle", 100, 30, True, 7, 2, 0, 5, 1, False]
    Spear = [3, "Spear", 50, 100, True, 3, 2, 0, 5, 1, False]
    Machine_Gun = [1, "Machine gun", 50, 5, False, 4, 0, 0, 3, 30, False]
    Grenade_Launcher = [1, "Grenade Launcher", 50, 10, True, 4, 0, 1, 3, 10, False]
    Flamethrower = [1, "Flamethrower", 10, 0, True, 4, 0, 1, 2, 10, False]
    Arcthrower = [1, "Arcthrower", 15, math.inf, False, math.inf, 1, 0, 4, 1, True]
    Bomb_500kg = [4, "500kg", 150, 50, True, 1, 2, 2, 0, 0, 0]
    Barrage_380mm = [4, "380mm Barrage", 100, 50, True, math.inf, 5, 3, 100, 50, 3]
    Orbital_Precision_Strike = [4, "Orbital Precision Strike", 25, 50, True, math.inf, 2, 1, 0, 0, 0]
    Cluster_Bomb = [4, "Cluster bomb", 30, 10, True, 3, 1, 2, 0, 0, 0]
    Strafing_Run = [4, "Strafing run", 30, 20, False, 3, 1, 1, 0, 0, 0]
    Eagle_Airstrike = [4, "Eagle airstrike", 50, 10, True, 2, 1, 1, 0, 0, 0]
    Rocket_Pods = [4, "Rocket pods", 35, 30, True, 4, 1, 1, 0, 0, 0]
    Orbital_Gatling = [4, "Orbital Gatling", 50, 10, False, math.inf, 3, 1, 0, 0, 0]
    Orbital_Gas = [4, "Orbital Gas", 25, 100, False, math.inf, 3, 2, 10, math.inf, 2]
    Gatling_Sentry = [5, "Gatling Sentry", 10, 0, False, math.inf, 1, False, 3, 50, 25, False, 0]
    Machine_Gun_Sentry = [5, "Machine Gun Sentry", 5, 2, False, math.inf, 2, False, 3, 50, 25, False, 0]
    Rocket_Sentry = [5, "Rocket Sentry", 25, 10, False, math.inf, 3, False, 3, 50, 25, False, 0]
    Autocannon_Sentry = [5, "Autocannon Sentry", 20, 15, False, math.inf, 2, False, 3, 50, 25, False, 0]
    Anti_Tank_Emplacement = [5, "Anti Tank Emplacement", 100, math.inf, False, math.inf, 3, True, 3, 50, 25, False, 0]
    Gas_Mines = [5, "Gas Mines", 15, math.inf, False, math.inf, 6, False, 0, 0, 0, True, 1]
    Incendiary_Mines = [5, "Incendiary Mines", 20, math.inf, False, math.inf, 4, False, 0, 0, 0, True, 2]
    Regular_Mines = [5, "Regular Mines", 25, math.inf, False, math.inf, 3, False, 0, 0, 0, True, 3]
    Anti_Tank_Mines = [5, "Anti Tank Mines", 50, math.inf, False, math.inf, 4, False, 0, 0, 0, True, 4]
    Supply_Pack = [2, "Supply Pack", math.inf, 6, False, 0, 0, 0, 0]
    Shield_Generator_Pack = [2, "Shield Generator Pack", math.inf, 6, False, 0, 0, 0, 0]
    Hellbomb_Backpack = [2, "Hellbomb Backpack", math.inf, 6, False, 0, 0, 0, 0]
    Balistic_Shield = [2, "Balistic Shield", math.inf, 6, False, 0, 0, 0, 0]
    Guard_Dog = [2, "Guard Dog", math.inf, 6, True, 5, 10, 30, 3]
    Guard_Dog_Rover = [2, "Guard Dog Rover", math.inf, 6, True, 1, math.inf, 100, 3]
    Guard_Dog_Breath = [2, "Guard Dog Dog Breath", math.inf, 6, True, 5, math.inf, 45, 3]

# main code
if (y-8)%2 is 0:
    for _ in range(int((y-8)/2)):
        print_centered(" ")
else:
    for _ in range(int((y-8)/2)+1):
        print_centered(" ")
if True:
    print_centered(" _    _   ______   _        _        _____    _____  __      __  ______   _____     _____ ")
    print_centered("|█|  |█| |██████| |█|      |█|      |█████\\  |█████| \\▚\\    /▞/ |██████| |█████\\   /█████|")
    print_centered("|█|__|█| |█|__    |█|      |█|      |█|  |█|   |█|    \\▚\\  /▞/  |█|__    |█|__)█| |█(___  ")
    print_centered("|██████| |████|   |█|      |█|      |█|  |█|   |█|     \\▚\\/▞/   |████|   |█████/   \\████\\ ")
    print_centered("|█|  |█| |█|____  |█|____  |█|____  |█|__|█|  _|█|_     \\▚▞/    |█|____  |█| \\█\\   ____)█|")
    print_centered("|█|  |█| |██████| |██████| |██████| |█████/  |█████|     \\/     |██████| |█|  \\█\\ |█████/ ")
    print_centered(" ")
    print_centered("PRESS ANY KEY TO START")
if (y-8)%2 is 0:
    for _ in range(int((y-8)/2)):
        print_centered(" ")
else:
    for _ in range(int((y-8)/2)+1):
        print_centered(" ")
hide_cursor()
while True:
    if keyboard.read_event().event_type is keyboard.KEY_DOWN:
        break
clear()
if True: #hides maps
    ## world numbers
    # 0 = ground
    # 1 = barrier
    # 2 = wall
    # 3 = enemy
    # 4 = enemy spawner
    # 5 = player
    # 6 = interactable object
    # 7 = gate
    # 8 = special
    # 9 = hellbomb
    # 10 = targetable enemy - not used directly
    # 11 = targeted enemy - not used directly
    # 12 = grenade target - not used directly
    training_1_2_3  = [
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,0,0,0,0,0,1,0,0,0,4,0,0,0,0,2],
        [2,0,0,0,0,0,1,0,0,3,0,3,0,0,0,2],
        [2,0,0,0,0,0,1,1,1,1,1,1,1,1,1,2],
        [2,6,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,2,7,7,2,2,7,7,7,7,2,2,2,2,2,2],
        [2,6,0,0,2,0,0,0,0,0,6,1,0,0,2,2],
        [7,0,0,0,2,0,0,0,0,0,0,1,0,0,2,2],
        [7,0,0,0,2,0,0,0,0,0,0,1,0,3,2,2],
        [2,0,6,0,2,0,0,0,0,0,0,1,0,0,2,2],
        [2,0,0,0,2,0,0,0,0,0,0,1,0,0,2,2],
        [2,2,2,2,2,2,7,7,7,7,2,2,2,2,2,2],
        [2,0,0,0,0,0,0,0,0,0,6,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,5,0,0,0,0,0,0,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    ]
    training_4  = [
        [2,2,2,2,2,2,2,2,2,2,2],
        [2,0,0,0,1,0,0,0,0,0,2],
        [2,3,0,0,1,0,0,0,0,5,7],
        [2,0,0,3,1,0,0,0,0,0,7],
        [2,0,0,0,1,0,0,0,0,0,2],
        [2,0,3,0,1,0,0,0,0,6,2],
        [2,2,2,2,2,2,7,7,7,2,2],
        [2,0,0,0,0,0,0,0,0,0,2],
        [2,6,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,2],
        [2,2,2,2,2,2,2,2,2,2,2]
    ]
    Training = [
        training_1_2_3,
        training_4
    ]
    Exterminate_1  = [
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,2,2,0,0,0,0,0,0,0,2,2,2,2,2,2],
        [2,2,0,3,0,0,0,0,4,0,0,9,0,3,2,2],
        [2,0,0,0,0,4,0,0,0,3,0,0,0,0,2,2],
        [2,0,0,0,0,0,3,0,0,0,0,0,4,0,0,2],
        [2,0,4,0,0,1,1,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,3,1,0,6,0,2,0,0,0,0,0,2],
        [2,2,0,0,0,0,5,0,0,2,0,0,0,0,0,2],
        [2,2,4,0,0,0,0,0,0,0,0,4,0,0,0,2],
        [2,0,0,3,0,0,1,1,1,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
        [2,0,3,0,0,4,0,0,0,0,3,0,0,4,2,2],
        [2,2,0,0,0,0,0,0,0,0,0,0,3,0,0,2],
        [2,2,2,0,0,3,0,0,0,4,0,0,0,0,2,2],
        [2,2,0,0,2,0,0,0,0,0,0,0,2,2,2,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    ]
    Exterminate_2  = [
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,2,2,2,0,3,0,0,0,0,0,0,0,0,2,2],
        [2,0,2,0,0,0,0,0,3,0,0,0,4,0,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,0,0,3,0,1,0,0,4,0,0,1,0,0,0,2],
        [2,0,0,0,0,1,3,3,3,3,3,1,0,0,0,2],
        [2,0,0,0,3,1,0,0,6,0,0,1,0,0,0,2],
        [2,0,4,0,0,1,0,0,0,0,0,1,0,3,0,2],
        [2,0,3,0,0,1,0,0,5,0,0,1,0,0,0,2],
        [2,0,0,0,0,1,0,0,0,0,0,1,0,4,0,2],
        [2,0,0,3,0,1,0,0,0,0,0,1,0,0,0,2],
        [2,0,0,0,0,1,0,0,0,0,0,1,0,0,0,2],
        [2,0,3,0,0,0,0,3,0,0,0,0,0,0,0,2],
        [2,2,3,4,3,0,0,0,0,0,0,0,0,0,2,2],
        [2,2,0,0,0,0,0,0,0,0,3,0,0,2,2,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    ]
    Exterminate = [
        Exterminate_1,
        Exterminate_2
    ]
    Evac_Civs_1  = [
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,1,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,3,0,3,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,1,1,0,0,0,0,0,0,0,4,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,1,1,0,4,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,1,2,2,2,2,2,2,1,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,1,2,2,1,0,0,0,0,0,0,1,2,2,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,3,0,0,0,0,1,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,9,2,2,1,0,2],
        [2,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,2],
        [2,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,1,1,4,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,1,1,0,3,3,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,2,2,2,2],
        [2,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,6,8,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,3,0,0,6,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,3,8,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,3,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,8,0,0,0,0,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    ]
    Evac_Civs_2  = [
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2],
        [2,1,1,0,0,0,0,3,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,6,0,0,0,4,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,2],
        [2,1,0,0,0,0,0,3,3,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,3,0,0,2],
        [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,1,1,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,0,0,0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,6,8,0,1,3,0,0,0,0,0,0,0,0,0,2],
        [2,2,1,0,0,0,0,0,0,0,0,0,0,0,6,0,9,0,0,0,1,3,4,0,0,0,0,0,0,0,0,2],
        [2,2,0,0,0,3,0,0,0,0,0,0,0,0,8,0,0,0,0,0,1,0,3,0,0,0,0,0,0,0,0,2],
        [2,1,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,3,0,0,0,4,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,1,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,3,0,1,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,3,1,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,2],
        [2,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,3,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,4,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,1,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2],
        [2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    ]
    Evac_Civs = [
        Evac_Civs_1,
        Evac_Civs_2
    ]
    ICBM_1  = [
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,0,0,0,0,0,0,0,1,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,2],
        [2,0,0,6,0,0,0,2,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,2],
        [2,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,2],
        [2,1,2,2,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,3,0,3,0,0,0,0,0,0,0,0,0,2],
        [2,2,1,1,0,0,0,0,0,0,0,0,0,0,0,1,3,0,3,0,4,0,0,0,0,0,0,0,0,0,0,2],
        [2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,4,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,3,0,0,0,1,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,4,0,0,0,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,2],
        [2,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,2],
        [2,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,3,0,3,0,0,0,0,0,0,0,1,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,3,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,3,0,2],
        [2,0,3,0,3,0,0,0,0,1,0,0,0,0,1,9,2,2,1,0,0,0,0,0,0,3,0,6,0,0,0,2],
        [2,0,0,4,0,3,0,0,1,1,0,0,0,0,1,2,2,2,1,1,3,1,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,2,2,1,0,0,1,3,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,1,3,6,1,0,0,6,0,0,0,0,0,6,2],
        [2,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,3,1,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    ]
    ICBM_2  = [
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,3,0,4,0,3,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,3,0,1,3,0,6,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,3,0,0,0,0,3,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,1,1,0,0,0,1,0,3,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,1,2,2,1,0,0,1,0,0,0,0,0,3,0,3,1,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,4,0,1,2,2,1,0,0,0,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,2],
        [2,0,3,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,3,0,0,1,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,1,9,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,2],
        [2,0,0,0,0,0,1,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,1,2,2,2,1,0,0,0,0,0,0,0,0,0,0,6,0,0,6,0,0,0,6,0,0,2],
        [2,0,0,0,0,0,0,1,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,2],
        [2,1,1,1,1,1,1,0,0,0,0,3,4,0,3,4,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,2],
        [2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,2],
        [2,1,1,1,1,1,1,0,0,0,0,0,3,4,0,0,0,0,0,0,0,0,3,0,0,0,1,0,0,0,0,2],
        [2,0,3,0,3,0,0,0,0,0,0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,2,0,0,0,0,2],
        [2,0,0,4,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,1,2,0,0,3,0,0,2],
        [2,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,3,4,0,0,0,0,2],
        [2,0,0,0,4,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,3,0,0,0,0,2],
        [2,0,3,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,4,0,4,0,0,2,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    ]
    ICBM = [
        ICBM_1,
        ICBM_2
    ]
    Raise_Flag_1  = [
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,2,2,1,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2],
        [2,2,4,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,3,4,2,2],
        [2,2,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,2],
        [2,0,3,0,8,8,8,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,2],
        [2,0,0,8,0,3,0,8,0,1,0,0,0,0,0,0,0,0,5,0,0,0,0,1,2,2,2,2,1,0,2],
        [2,0,8,0,0,0,0,0,8,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,2],
        [2,0,8,0,0,0,0,0,8,1,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,8,0,0,0,3,0,8,1,0,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,2,0,8,0,0,0,8,0,1,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,2,2,0,8,8,8,0,0,1,0,4,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,2,2,2,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
        [2,2,2,1,1,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
        [2,2,2,1,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,3,0,0,0,0,0,0,0,2,2],
        [2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,9,2,0,0,3,4,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,1,4,3,8,8,8,0,0,0,2],
        [2,0,0,0,1,1,1,0,0,0,1,1,1,4,0,0,0,0,0,0,0,1,3,8,0,0,0,8,0,0,2],
        [2,0,0,0,1,0,0,8,8,8,0,0,1,3,0,0,0,0,0,0,0,1,8,0,3,0,0,0,8,0,2],
        [2,0,0,3,1,0,8,0,0,0,8,0,1,0,0,0,1,0,0,0,0,1,8,0,0,0,0,0,8,0,2],
        [2,0,0,0,1,8,0,3,0,0,0,8,1,0,0,1,1,1,0,0,0,1,8,0,0,0,3,0,8,0,2],
        [2,0,0,4,1,8,0,0,0,0,0,8,1,0,0,0,2,2,1,0,0,1,0,8,0,0,0,8,0,0,2],
        [2,0,3,0,1,8,0,0,0,3,0,8,1,0,0,0,1,2,1,0,0,1,0,0,8,8,8,0,0,0,2],
        [2,1,0,0,1,0,8,0,0,0,8,0,1,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,2],
        [2,2,1,0,1,0,0,8,8,8,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,2,4,2],
        [2,1,2,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,3,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,3,3,3,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    ]
    Raise_Flag_2 = [
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,2,2,2],
        [2,2,4,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,0,0,0,0,0,0,0,3,4,2,2],
        [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,8,8,8,0,0,0,0,3,0,2],
        [2,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,8,0,0,0,8,0,1,1,0,0,2],
        [2,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,1,8,0,3,0,1,2,8,2,2,1,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,8,0,0,0,0,1,8,0,0,0,0,2],
        [2,0,0,3,0,0,4,0,2,0,0,0,0,0,0,1,2,1,1,8,0,0,0,0,0,8,0,0,0,0,2],
        [2,0,0,4,0,0,3,0,2,0,0,0,0,0,0,2,1,0,1,0,8,0,0,0,8,0,0,0,0,0,2],
        [2,2,0,3,0,4,0,0,2,0,3,8,8,8,0,0,0,0,1,1,1,8,8,8,0,0,0,0,0,0,2],
        [2,2,2,0,0,0,0,2,0,0,8,4,3,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,2,2,2,1,2,2,0,0,8,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,3,0,0,0,2,2],
        [2,2,2,1,1,0,0,0,0,8,0,0,0,0,2,8,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
        [2,2,2,1,0,0,0,0,5,8,0,0,0,0,0,8,1,0,0,0,0,3,0,0,0,0,0,0,0,2,2],
        [2,1,1,0,0,0,0,0,0,0,8,0,0,0,8,9,2,0,0,3,4,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,8,8,8,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,4,3,0,0,0,0,0,0,2],
        [2,0,0,0,1,1,1,0,0,0,1,1,1,4,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,2],
        [2,0,0,0,1,0,0,8,8,8,0,0,1,3,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,2],
        [2,0,0,3,1,0,8,0,0,0,8,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,1,8,0,3,0,0,0,8,1,0,0,1,1,1,0,0,0,0,2,0,0,0,3,0,0,0,2],
        [2,0,0,4,1,8,0,0,0,0,0,8,1,0,0,0,2,2,1,0,0,2,0,0,0,0,0,0,0,0,2],
        [2,0,3,0,1,8,0,0,0,3,0,8,1,0,0,0,1,2,1,0,0,2,0,0,0,0,0,0,0,0,2],
        [2,1,0,0,1,0,8,0,0,0,8,0,1,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,2],
        [2,2,1,0,1,0,0,8,8,8,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,2,4,2],
        [2,1,2,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,3,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,3,3,3,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    ]
    Raise_Flag = [
        Raise_Flag_1,
        Raise_Flag_2
    ]
    Destroy_Outposts_1  = [
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,0,4,0,0,4,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,4,0,3,0,0,0,3,1,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,3,0,2,0,2,0,0,1,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,1,1,2,0,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1,3,0,4,0,0,0,0,2],
        [2,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,3,0,0,0,0,0,2],
        [2,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,3,4,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,2,2,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,1,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,1,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,1,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,3,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,3,0,0,3,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,4,0,0,0,2],
        [2,0,0,0,0,4,3,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,1,1,2,0,2,1,1,1,2],
        [2,0,0,0,0,0,0,4,0,3,0,0,0,0,0,0,0,3,0,4,2,0,3,0,2,0,2,0,3,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,3,4,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,2,2,0,0,3,0,4,0,8,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,0,0,3,3,0,0,0,4,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    ]
    Destroy_Outposts_2  = [
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,3,4,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,3,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,5,0,0,0,0,0,0,0,1,1,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,2],
        [2,0,0,0,3,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,8,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,4,3,1,2,1,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,2],
        [2,0,0,3,4,3,1,2,2,1,0,0,0,3,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,1,2,1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,0,0,0,0,0,0,1,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,4,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,2,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,1,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,1,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,3,0,9,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,3,0,0,1,1,1,0,0,0,0,0,0,2],
        [2,0,0,0,0,4,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,4,0,3,0,0,0,0,6,0,0,3,0,0,0,1,3,0,3,0,0,0,3,0,2],
        [2,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,4,0,0,4,3,4,2],
        [2,0,0,1,2,2,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,3,0,0,0,2],
        [2,0,0,0,1,1,2,2,2,1,0,0,0,0,0,0,3,0,0,0,0,1,0,0,3,0,0,0,0,0,2],
        [2,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,3,3,0,4,0,4,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    ]
    Destroy_Outposts = [
        Destroy_Outposts_1,
        Destroy_Outposts_2
    ]
    Meme_1  = [
        [3,3,3,3,3,3,3,3,3,3,3],
        [3,9,9,9,9,9,9,9,9,9,3],
        [3,9,9,9,9,9,9,9,9,9,3],
        [3,9,9,9,9,6,9,9,9,9,3],
        [3,9,9,9,9,0,9,9,9,9,3],
        [3,9,9,9,0,5,0,9,9,9,3],
        [3,9,9,9,9,0,9,9,9,9,3],
        [3,9,9,9,9,9,9,9,9,9,3],
        [3,9,9,9,9,9,9,9,9,9,3],
        [3,9,9,9,9,9,9,9,9,9,3],
        [3,3,3,3,3,3,3,3,3,3,3]
    ]
    Meme_2  = [
        [2,0,2,2,2,2,2,2,2,2,2],
        [0,5,0,0,0,0,0,1,2,3,2],
        [2,0,1,0,1,2,0,2,1,0,2],
        [2,0,2,0,2,1,0,0,2,0,2],
        [2,0,1,0,0,2,1,0,0,0,2],
        [2,0,2,1,2,1,2,0,2,0,2],
        [2,3,1,0,0,0,0,0,1,0,2],
        [2,1,2,0,2,3,2,1,2,4,2],
        [2,2,1,0,1,2,1,0,0,3,2],
        [2,3,0,0,0,0,0,1,2,6,2],
        [2,2,2,2,2,2,2,2,2,2,2]
    ]
    Meme_Maps = [
        Meme_1,
        Meme_2
    ]

level = [
    [
        ##[list(EnemyType.copy()), x, y, ["killAction", [KillActionMetadata]]]
        ## []
        [[list(Scavenger.copy()), 13, 8, ["condition", ["killedBug1", "set", True]]],[list(Scavenger.copy()), 9, 2],[list(Scavenger.copy()), 11, 2]], ##enemies
        [["killedBug1", False], ["closedHole1", False]], ## conditions
        [[["clear", [[11,6],[11,7],[11,8],[11,9]],7], [12,10]], [["condition", ["killedBug1", "check", True, ["clear", [[5,6],[5,7],[5,8],[5,9]],7]]], [6, 10]], [["spawner",["condition", ["closedHole1", "set", True]]], [1,10]], [["condition", ["closedHole1", "check", True, ["clear", [[5, 2],[5, 3]], 7]]], [4, 1]]], ## points of interest
        "player 0", ##turn
        math.inf, ##base moves
        "| Helldivers Training |\n| Use WASD or arrow keys to move |\n| Space to attack |\n| E to interact |\n| G to throw grenade |\n| 1/2 to change weapon |", ## header
        [ ##players
            [[8,14], list(Explosive_Crossbow.copy()), list(GP_31_Ultimatum.copy()), list(B_01_Tactical.copy()), 1, 100, 100, 4, 4, 4, 4, 0, 0, Name, list(G_6_Frag.copy())]
        ],
        bugs
    ],
    list(copy.deepcopy(training_1_2_3))
]
level_evac_1 = [
    [
        ##[list(EnemyType.copy()), x, y, ["killAction", [KillActionMetadata]]]
        ##[]
        [[list(Scavenger.copy()), 4, 14,],[list(Hunter.copy()), 12, 6],[list(Scavenger.copy()), 10, 6],[list(Scavenger.copy()), 11, 5],[list(Pouncer.copy()), 11, 7],[list(Stalkers.copy()), 9, 20],[list(Charger.copy()), 10, 20],[list(Scavenger.copy()), 11, 19],[list(Bile_Titan.copy()), 8, 26],[list(Scavenger.copy()), 9, 26],[list(Shreiker.copy()), 16, 20],[list(Shreiker.copy()), 17, 20],[list(Shreiker.copy()), 17, 21],[list(Scavenger.copy()), 27, 27],[list(Scavenger.copy()), 27, 29],[list(Scavenger.copy()), 27, 29],[list(Hunter.copy()), 29, 28]], ##enemies

        [["evacedCivs", False]], ## conditions
        [[["condition", ["evacedCivs", "check", True, ["extraction"],]], [2, 2]],[["spawner"], [10,15]],[["spawner"], [8,28]],[["spawner"], [19,9]],[["spawner"], [24,21]],[["civ enter"], [24,28]],[["civ enter button"], [27,30]],[["civ enter button"], [24,27]],[["civ enter"], [28,30]],[["civ exit"], [30,26]],[["hellbomb"], [15,26]]], ## points of interest
        "player 0", ##turn
        math.inf, ##base moves
        "", ## header
        [ ##players
            [[8,8], list(Liberator_Penetrator.copy()), list(P_19_Redeemer.copy()), list(SR_24_Street_Scout.copy()), 1, 100, 100, 4, 4, 4, 4, 0, 0, Name, list(G_6_Frag.copy())]
        ],
        bugs
    ],
    list(copy.deepcopy(Evac_Civs_1))
]
level_ex_1 = [
    [
        ##[list(EnemyType.copy()), x, y, ["killAction", [KillActionMetadata]]]
        [[list(Hive_Guard.copy()), 3, 2, ["condition", ["killedEnemies", "add", 1]]],[list(Hunter.copy()), 4, 6, ["condition", ["killedEnemies", "add", 1]]],[list(Charger.copy()), 3, 9, ["condition", ["killedEnemies", "add", 1]]],[list(Bile_Titan.copy()), 2, 11, ["condition", ["killedEnemies", "add", 1]]],[list(Pouncer.copy()), 5, 13, ["condition", ["killedEnemies", "add", 1]]],[list(Hive_Guard.copy()), 10, 11, ["condition", ["killedEnemies", "add", 1]]],[list(Bile_Titan.copy()), 12, 12, ["condition", ["killedEnemies", "add", 1]]],[list(Scavenger.copy()), 6, 4, ["condition", ["killedEnemies", "add", 1]]],[list(Charger.copy()), 9, 3, ["condition", ["killedEnemies", "add", 1]]],[list(Bile_Titan.copy()), 13, 2, ["condition", ["killedEnemies", "add", 1]]]], ##enemies
        ##[[list(Devistator.copy()), 3, 2, ["condition", ["killedEnemies", "add", 1]]],[list(Beserker.copy()), 4, 6, ["condition", ["killedEnemies", "add", 1]]],[list(Hulk.copy()), 3, 9, ["condition", ["killedEnemies", "add", 1]]],[list(Factory_Strider.copy()), 2, 11, ["condition", ["killedEnemies", "add", 1]]],[list(Scout_Strider.copy()), 5, 13, ["condition", ["killedEnemies", "add", 1]]],[list(Devistator.copy()), 10, 11, ["condition", ["killedEnemies", "add", 1]]],[list(Factory_Strider.copy()), 12, 12, ["condition", ["killedEnemies", "add", 1]]],[list(Trooper.copy()), 6, 4, ["condition", ["killedEnemies", "add", 1]]],[list(Hulk.copy()), 9, 3, ["condition", ["killedEnemies", "add", 1]]],[list(Factory_Strider.copy()), 13, 2, ["condition", ["killedEnemies", "add", 1]]]], ##enemies
        ##[[list(Cresent_Overseer.copy()), 3, 2, ["condition", ["killedEnemies", "add", 1]]],[list(Overseer.copy()), 4, 6, ["condition", ["killedEnemies", "add", 1]]],[list(Flesh_Mob.copy()), 3, 9, ["condition", ["killedEnemies", "add", 1]]],[list(Harvester.copy()), 2, 11, ["condition", ["killedEnemies", "add", 1]]],[list(Elevated_Overseer.copy()), 5, 13, ["condition", ["killedEnemies", "add", 1]]],[list(Watcher.copy()), 10, 11, ["condition", ["killedEnemies", "add", 1]]],[list(Harvester.copy()), 12, 12, ["condition", ["killedEnemies", "add", 1]]],[list(Voteless.copy()), 6, 4, ["condition", ["killedEnemies", "add", 1]]],[list(Flesh_Mob.copy()), 9, 3, ["condition", ["killedEnemies", "add", 1]]],[list(Harvester.copy()), 13, 2, ["condition", ["killedEnemies", "add", 1]]]], ##enemies
        [["killedEnemies", 0]], ## conditions
        [[["hellbomb"], [2,11]], [["condition", ["killedEnemies", "check", 10, ["extraction"],]], [6, 7]],[["spawner"], [2,8]],[["spawner"], [3,5]],[["spawner"], [4,12]],[["spawner"], [5,2]],[["spawner"], [8,2]],[["spawner"], [8,11]],[["spawner"], [11,5]],[["spawner"], [11,13]],[["spawner"], [13,9]]], ## points of interest
        "player 0", ##turn
        5, ##base moves
        "", ## header
        [ ##players
            [[6,7], list(Liberator_Penetrator.copy()), list(P_19_Redeemer.copy()), list(SR_24_Street_Scout.copy()), 1, 100, 100, 4, 4, 4, 4, 0, 0, Name, list(G_6_Frag.copy())]
        ],
        bugs
    ],
    list(copy.deepcopy(Exterminate_1))
]
level_ex_2 = [
    [
        ##[list(EnemyType.copy()), x, y, ["killAction", [KillActionMetadata]]]
        ##[]
        [[list(Scavenger.copy()), 6, 5, ["condition", ["killedEnemies", "add", 1]]],[list(Scavenger.copy()), 7, 5, ["condition", ["killedEnemies", "add", 1]]],[list(Scavenger.copy()), 8, 5, ["condition", ["killedEnemies", "add", 1]]],[list(Scavenger.copy()), 9, 5, ["condition", ["killedEnemies", "add", 1]]],[list(Scavenger.copy()), 10, 5, ["condition", ["killedEnemies", "add", 1]]],[list(Charger.copy()), 7, 12, ["condition", ["killedEnemies", "add", 1]]],[list(Hunter.copy()), 10, 14, ["condition", ["killedEnemies", "add", 1]]],[list(Bile_Titan.copy()), 13, 7, ["condition", ["killedEnemies", "add", 1]]],[list(Scavenger.copy()), 4, 13, ["condition", ["killedEnemies", "add", 1]]],[list(Scavenger.copy()), 2, 12, ["condition", ["killedEnemies", "add", 1]]],[list(Scavenger.copy()), 2, 13, ["condition", ["killedEnemies", "add", 1]]],[list(Bile_Spewer.copy()), 3, 10, ["condition", ["killedEnemies", "add", 1]]],[list(Bile_Spewer.copy()), 2, 8, ["condition", ["killedEnemies", "add", 1]]],[list(Scavenger.copy()), 4, 6, ["condition", ["killedEnemies", "add", 1]]],[list(Bile_Spewer.copy()), 3, 4, ["condition", ["killedEnemies", "add", 1]]],[list(Charger.copy()), 8, 2, ["condition", ["killedEnemies", "add", 1]]],[list(Hunter.copy()), 5, 1, ["condition", ["killedEnemies", "add", 1]]]], ##enemies

        [["killedEnemies", 0]], ## conditions
        [[["condition", ["killedEnemies", "check", 17, ["extraction"],]], [6, 8]],[["spawner"], [13,3]],[["spawner"], [7,2]],[["spawner"], [4,8]],[["spawner"], [2,12]],[["spawner"], [9,13]]], ## points of interest
        "player 0", ##turn
        5, ##base moves
        "", ## header
        [ ##players
            [[8,8], list(Liberator_Penetrator.copy()), list(LAS_7_Dagger.copy()), list(SR_24_Street_Scout.copy()), 1, 100, 100, 4, 4, 4, 4, 0, 0, Name, list(G_6_Frag.copy())]
        ],
        bugs
    ],
    list(copy.deepcopy(Exterminate_2))
]
for playerIndexTurn in range(len(level[0][6])):
    if level[0][6][playerIndexTurn][3][3].lower() == "servo-assisted":
        level[0][6][playerIndexTurn][5] += 10
        level[0][6][playerIndexTurn][6] += 10
    if level[0][6][playerIndexTurn][3][3].lower() == "engineering kit":
        level[0][6][playerIndexTurn][7] += 2
        level[0][6][playerIndexTurn][8] += 2
    if level[0][6][playerIndexTurn][3][3].lower() == "med-kit":
        level[0][6][playerIndexTurn][9] += 2
        level[0][6][playerIndexTurn][10] += 2
    if level[0][6][playerIndexTurn][3][3].lower() == "siege-ready":
        level[0][6][playerIndexTurn][1][4] = int(round(level[0][6][playerIndexTurn][1][4] * Fraction(6, 5)))
        level[0][6][playerIndexTurn][2][4] = int(round(level[0][6][playerIndexTurn][2][4] * Fraction(6, 5)))
        level[0][6][playerIndexTurn][1][10] = int(round(level[0][6][playerIndexTurn][1][10] * Fraction(6, 5)))
        level[0][6][playerIndexTurn][2][10] = int(round(level[0][6][playerIndexTurn][2][10] * Fraction(6, 5)))
# Enemy = [list(EnemyType.copy()), x, y, ["killAction", [KillActionMetadata]]]
# Condition = ["name", value]

hide_cursor()

while True:
    actionItem = ""
    if level[0][3].startswith("player "):
        playerIndexTurn = int(level[0][3][-1])
        if level[0][6][playerIndexTurn][3][3].lower() == "reinforced epaulets" and random.randint(0, 100) < 50:
            level[0][6][playerIndexTurn][5] += 20
            level[0][6][playerIndexTurn][6] = 120
        else:
            level[0][6][playerIndexTurn][6] = 100
            if level[0][6][playerIndexTurn][5] > level[0][6][playerIndexTurn][6]:
                level[0][6][playerIndexTurn][5] = level[0][6][playerIndexTurn][6]
        if level[0][6][playerIndexTurn][12] > 0:
            level[0][6][playerIndexTurn][12] -= 1
            level[0][6][playerIndexTurn][5] += 60
            if level[0][6][playerIndexTurn][5] > level[0][6][playerIndexTurn][6]:
                level[0][6][playerIndexTurn][5] = level[0][6][playerIndexTurn][6]
        shootPhases = 0
        targets = []
        clear()
        if level[0][6][playerIndexTurn][11] > 0:
            level[0][6][playerIndexTurn][11] -= 1
        if level[0][6][playerIndexTurn][11] != 0:
            actionItem = f"\033[33mReloading {level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][0]} for {level[0][6][playerIndexTurn][11]} turns...\n"
            actionItem += f"\033[31mPress X to end turn\033[0m"
            print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
            while True:
                if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                    keyPressed = keyboard.read_event().name
                    if keyPressed == "x":
                        clear()
                        actionItem = "\033[31mPress X again to confirm."
                        print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                        while True:
                            if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                                keyPressed = keyboard.read_event().name
                                if keyPressed == "x":
                                    clear()
                                    actionItem = "\033[31mEnding turn..."
                                    print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                                    time.sleep(1)
                                    level[0][3] = "enemy"
                                    level[0][4] = 5 + level[0][6][playerIndexTurn][3][1]
                                    break
                                else:
                                    continue
                        break
                    else:
                        continue
        actionItem = f"\033[33mMoves left: {level[0][4]}"
        if level[0][4] is 0:
            actionItem += "\n\033[31mPress X to end turn\033[0m"
        for poi in level[0][2]:
            if level[1][poi[1][0]][poi[1][1]] == 6:
                if poi[1][0] is level[0][6][playerIndexTurn][0][1]+1 and poi[1][1] is level[0][6][playerIndexTurn][0][0] or poi[1][0] is level[0][6][playerIndexTurn][0][1]-1 and poi[1][1] is level[0][6][playerIndexTurn][0][0] or poi[1][0] is level[0][6][playerIndexTurn][0][1] and poi[1][1] is level[0][6][playerIndexTurn][0][0]+1 or poi[1][0] is level[0][6][playerIndexTurn][0][1] and poi[1][1] is level[0][6][playerIndexTurn][0][0]-1:
                    if poi[0][0] == "hellbomb" or poi[0][0] == "spawner":
                        break
                    if len(poi) >= 3:
                        actionItem += f"\n\033[33m{poi[2]}\033[0m"
                    else:
                        actionItem += f"\n\033[33mPress E to interact\033[0m"
        print(level[0][6][0][0][1], level[0][6][0][0][0])
        print()
        print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
        while True:
            if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                keyPressed = keyboard.read_event().name
                if keyPressed == "up" or keyPressed == "w":
                    if level[1][level[0][6][playerIndexTurn][0][1]-1][level[0][6][playerIndexTurn][0][0]] == 0 and level[0][4] > 0:
                        level[1][level[0][6][playerIndexTurn][0][1]][level[0][6][playerIndexTurn][0][0]] = 0
                        level[0][6][playerIndexTurn][0][1] -= 1
                        level[1][level[0][6][playerIndexTurn][0][1]][level[0][6][playerIndexTurn][0][0]] = 5
                        level[0][4] -= 1
                elif keyPressed == "down" or keyPressed == "s":
                    if level[1][level[0][6][playerIndexTurn][0][1]+1][level[0][6][playerIndexTurn][0][0]] == 0 and level[0][4] > 0:
                        level[1][level[0][6][playerIndexTurn][0][1]][level[0][6][playerIndexTurn][0][0]] = 0
                        level[0][6][playerIndexTurn][0][1] += 1
                        level[1][level[0][6][playerIndexTurn][0][1]][level[0][6][playerIndexTurn][0][0]] = 5
                        level[0][4] -= 1
                elif keyPressed == "left" or keyPressed == "a":
                    if level[1][level[0][6][playerIndexTurn][0][1]][level[0][6][playerIndexTurn][0][0]-1] == 0 and level[0][4] > 0:
                        level[1][level[0][6][playerIndexTurn][0][1]][level[0][6][playerIndexTurn][0][0]] = 0
                        level[0][6][playerIndexTurn][0][0] -= 1
                        level[1][level[0][6][playerIndexTurn][0][1]][level[0][6][playerIndexTurn][0][0]] = 5
                        level[0][4] -= 1
                elif keyPressed == "right" or keyPressed == "d":
                    if level[1][level[0][6][playerIndexTurn][0][1]][level[0][6][playerIndexTurn][0][0]+1] == 0 and level[0][4] > 0:
                        level[1][level[0][6][playerIndexTurn][0][1]][level[0][6][playerIndexTurn][0][0]] = 0
                        level[0][6][playerIndexTurn][0][0] += 1
                        level[1][level[0][6][playerIndexTurn][0][1]][level[0][6][playerIndexTurn][0][0]] = 5
                        level[0][4] -= 1
                elif keyPressed == "1":
                    level[0][6][playerIndexTurn][4] = 1
                elif keyPressed == "2":
                    level[0][6][playerIndexTurn][4] = 2
                elif keyPressed == "space":
                    actionItem = ""
                    shootPhases += 1
                    if shootPhases != 3:
                        targets = []
                        targetIndex = 0
                        for enemy in level[0][0]:
                            if hypotenuse_los(level[1], level[0][6][playerIndexTurn][0], [enemy[1], enemy[2]], 5):
                                targets.append(enemy)
                                level[1][enemy[2]][enemy[1]] = 10
                                clear()
                                for target in targets:
                                    actionItem += f"\033[33m{target[0][0]}:\nHP: {target[0][11]}/{target[0][13]}\nArmor: {target[0][12]}/{target[0][12]}\033[0m\n"
                                print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                        if len(targets) is not 0:
                            clear()
                            actionItem = ""
                            level[1][targets[targetIndex][2]][targets[targetIndex][1]] = 11
                            for target in targets:
                                if target is targets[targetIndex]:
                                    actionItem += f"\033[33m✓ {target[0][0]} ✓\nHP: {target[0][11]}/{target[0][13]}\nArmor: {target[0][12]}/{target[0][12]}\033[0m\n"
                                else:
                                    actionItem += f"\033[33m{target[0][0]}:\nHP: {target[0][11]}/{target[0][13]}\nArmor: {target[0][12]}/{target[0][12]}\033[0m\n"
                            print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                            while True:
                                if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                                    actionItem = ""
                                    keyPressed = keyboard.read_event().name
                                    if keyPressed == "up" or keyPressed == "right":
                                        level[1][targets[targetIndex][2]][targets[targetIndex][1]] = 10
                                        if targetIndex is len(targets) - 1:
                                            targetIndex = 0
                                        else:
                                            targetIndex += 1
                                        level[1][targets[targetIndex][2]][targets[targetIndex][1]] = 11
                                        for target in targets:
                                            if target is targets[targetIndex]:
                                                actionItem += f"\033[33m✓ {target[0][0]} ✓\nHP: {target[0][11]}/{target[0][13]}\nArmor: {target[0][12]}/{target[0][12]}\033[0m\n"
                                            else:
                                                actionItem += f"\033[33m{target[0][0]}:\nHP: {target[0][11]}/{target[0][13]}\nArmor: {target[0][12]}/{target[0][12]}\033[0m\n"
                                        clear()
                                        print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                                    elif keyPressed == "down" or keyPressed == "left":
                                        level[1][targets[targetIndex][2]][targets[targetIndex][1]] = 10
                                        if targetIndex is 0:
                                            targetIndex = len(targets) - 1
                                        else:
                                            targetIndex -= 1
                                        level[1][targets[targetIndex][2]][targets[targetIndex][1]] = 11
                                        for target in targets:
                                            if target is targets[targetIndex]:
                                                actionItem += f"\033[33m✓ {target[0][0]} ✓\nHP: {target[0][11]}/{target[0][13]}\nArmor: {target[0][12]}/{target[0][12]}\033[0m\n"
                                            else:
                                                actionItem += f"\033[33m{target[0][0]}:\nHP: {target[0][11]}/{target[0][13]}\nArmor: {target[0][12]}/{target[0][12]}\033[0m\n"
                                        clear()
                                        print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                                    elif keyPressed == "enter" or keyPressed == "space":
                                        clear()
                                        actionItem = ""
                                        actionItem += f"\033[33m{targets[targetIndex][0][0]}:\nHP: {targets[targetIndex][0][11]}/{targets[targetIndex][0][13]}\nArmor: {targets[targetIndex][0][12]}/{targets[targetIndex][0][12]}\033[0m\n"
                                        attacks = [f"Fire {level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][0]}", "Melee", "Cancel"]
                                        if not hypotenuse_los(level[1], [level[0][6][playerIndexTurn][0][0], level[0][6][playerIndexTurn][0][1]], [targets[targetIndex][1], targets[targetIndex][2]], 1):
                                            attacks.pop(attacks.index("Melee"))
                                        selectionIndex = 1
                                        actionItem += f"\033[33m✓ 1: {attacks[0]} ✓\n"
                                        actionItem += f"\033[33m2: {attacks[1]}\n"
                                        if len(attacks) is 3:
                                            actionItem += f"\033[33m3: {attacks[2]}\n"
                                        print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                                        while True:
                                            if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                                                keyPressed = keyboard.read_event().name
                                                if keyPressed == "1":
                                                    selectionIndex = 1
                                                elif keyPressed == "2":
                                                    selectionIndex = 2
                                                elif keyPressed == "3" and len(attacks) is 3:
                                                    selectionIndex = 3
                                                elif keyPressed == "up":
                                                    if selectionIndex is 1:
                                                        selectionIndex = len(attacks)
                                                    else:
                                                        selectionIndex -= 1
                                                elif keyPressed == "down":
                                                    if selectionIndex is len(attacks):
                                                        selectionIndex = 1
                                                    else:
                                                        selectionIndex += 1
                                                elif keyPressed != "enter" and keyPressed != "space":
                                                    break
                                                clear()
                                                actionItem = f"\033[33m{targets[targetIndex][0][0]}:\nHP: {targets[targetIndex][0][11]}/{targets[targetIndex][0][13]}\nArmor: {targets[targetIndex][0][12]}/{targets[targetIndex][0][12]}\033[0m\n"
                                                if selectionIndex is 1:
                                                    actionItem += f"\033[33m✓ 1: {attacks[0]} ✓\n"
                                                    actionItem += f"\033[33m2: {attacks[1]}\n"
                                                    if len(attacks) is 3:
                                                        actionItem += f"\033[33m3: {attacks[2]}\n"
                                                elif selectionIndex is 2:
                                                    actionItem += f"\033[33m1: {attacks[0]}\n"
                                                    actionItem += f"\033[33m✓ 2: {attacks[1]} ✓\n"
                                                    if len(attacks) is 3:
                                                        actionItem += f"\033[33m3: {attacks[2]}\n"
                                                elif selectionIndex is 3:
                                                    actionItem += f"\033[33m1: {attacks[0]}\n"
                                                    actionItem += f"\033[33m2: {attacks[1]}\n"
                                                    actionItem += f"\033[33m✓ 3: {attacks[2]} ✓\n"
                                                print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                                                if keyPressed != "enter" and keyPressed != "space":
                                                    continue
                                                elif keyPressed == "enter" or keyPressed == "space":
                                                    if attacks[selectionIndex-1] == "Cancel":
                                                        break
                                                    elif attacks[selectionIndex-1].startswith("Fire"):
                                                        for target in targets:
                                                            if level[1][target[2]][target[1]] is 10:
                                                                level[1][target[2]][target[1]] = 3
                                                        bullets = 0
                                                        tempArmor = targets[targetIndex][0][12]
                                                        clear()
                                                        actionItem = ""
                                                        actionItem += f"\033[33m{targets[targetIndex][0][0]}:\nHP: {targets[targetIndex][0][11]}/{targets[targetIndex][0][13]}\nArmor: {targets[targetIndex][0][12]}/{targets[targetIndex][0][12]}\n"
                                                        actionItem += f"Firing {bullets}/{level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][10]}\nUse Up/Down arrows to change the amount\033[0m"
                                                        print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                                                        trueDmg = 0
                                                        dmg = level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][1] * bullets
                                                        maxArmor = targets[targetIndex][0][12] - (level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][2] * bullets)
                                                        tempArmor = maxArmor - dmg
                                                        while True:
                                                            if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                                                                keyPressed = keyboard.read_event().name
                                                                if keyPressed == "up":
                                                                    if bullets < level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][10]:
                                                                        bullets += 1
                                                                elif keyPressed == "down":
                                                                    if bullets != 0:
                                                                        bullets += -1
                                                                elif keyPressed == "enter" or keyPressed == "space":
                                                                    clear()
                                                                    actionItem = ""
                                                                    actionItem += f"\033[33m{targets[targetIndex][0][0]}:\nHP: {targets[targetIndex][0][11]-trueDmg}/{targets[targetIndex][0][13]}\nArmor: {tempArmor}/{maxArmor}\n"
                                                                    actionItem += f"\033[33mYou are going to fire {bullets}/{level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][10]} at {targets[targetIndex][0][0]}, leaving {level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][10]-bullets} remaining\n"
                                                                    actionItem += "Press Enter to confirm"
                                                                    print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                                                                    breakOut = False
                                                                    while True:
                                                                        if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                                                                            keyPressed = keyboard.read_event().name
                                                                            if keyPressed == "enter" or keyPressed == "space":
                                                                                targets[targetIndex][0][11] -= trueDmg
                                                                                targets[targetIndex][0][12] = maxArmor
                                                                                if targets[targetIndex][0][11] <= 0:
                                                                                    
                                                                                    level[1][targets[targetIndex][2]][targets[targetIndex][1]] = 0
                                                                                    if len(targets[targetIndex]) > 3:
                                                                                        i = parseActions(level[0], level[1], targets[targetIndex][3], level[0][1])
                                                                                        level[1] = i[0]
                                                                                        targets[targetIndex][3] = i[1]
                                                                                        level[0][1] = i[2]
                                                                                    level[0][0].remove(targets[targetIndex])
                                                                                    targets.pop(targetIndex)
                                                                                level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][10] += -bullets
                                                                                breakOut = True
                                                                                break
                                                                            else:
                                                                                break
                                                                    if breakOut == True:
                                                                        break
                                                                clear()
                                                                trueDmg = 0
                                                                dmg = level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][1] * bullets
                                                                maxArmor = targets[targetIndex][0][12] - (level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][2] * bullets)
                                                                tempArmor = maxArmor - dmg
                                                                if maxArmor < 0:
                                                                    maxArmor = 0
                                                                if tempArmor < 0:
                                                                    trueDmg = dmg - maxArmor
                                                                    tempArmor = 0
                                                                if trueDmg >= targets[targetIndex][0][11]:
                                                                    trueDmg = targets[targetIndex][0][11]
                                                                actionItem = ""
                                                                actionItem += f"\033[33m{targets[targetIndex][0][0]}:\nHP: {targets[targetIndex][0][11] - trueDmg}/{targets[targetIndex][0][13]}\nArmor: {tempArmor}/{maxArmor}\n"
                                                                actionItem += f"Firing {bullets}/{level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][10]}\nUse Up/Down arrows to change the amount\n"
                                                                actionItem += "Press Enter to confirm \033[0m"
                                                                print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                                                        break
                                                    elif attacks[selectionIndex-1] == "Melee":
                                                        trueDmg = 0
                                                        dmg = random.randint(1, 5)
                                                        maxArmor = targets[targetIndex][0][12] - 1
                                                        if level[0][6][playerIndexTurn][3][3].lower() == "peak physique":
                                                            dmg = dmg * 2 
                                                            maxArmor -= 5
                                                        if level[0][6][playerIndexTurn][3][3].lower() == "reinforced epaulets":
                                                            dmg = int(round(Fraction(3,2) * dmg))
                                                        tempArmor = maxArmor - dmg
                                                        if maxArmor < 0:
                                                            maxArmor = 0
                                                        if tempArmor < 0:
                                                            trueDmg = dmg - maxArmor
                                                            tempArmor = 0
                                                        if trueDmg >= targets[targetIndex][0][11]:
                                                            trueDmg = targets[targetIndex][0][11]
                                                        actionItem = f"\033[33m{targets[targetIndex][0][0]}:\nHP: {targets[targetIndex][0][11]-trueDmg}/{targets[targetIndex][0][13]}\nArmor: {tempArmor}/{maxArmor}\n"
                                                        actionItem += "Press Enter to confirm"
                                                        clear()
                                                        print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                                                        while True:
                                                            if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                                                                keyPressed = keyboard.read_event().name
                                                                if keyPressed == "enter" or keyPressed == "space":
                                                                    targets[targetIndex][0][11] -= trueDmg
                                                                    targets[targetIndex][0][12] = maxArmor
                                                                    if targets[targetIndex][0][11] <= 0:
                                                                        level[1][targets[targetIndex][2]][targets[targetIndex][1]] = 0
                                                                        if len(targets[targetIndex]) > 3:
                                                                            i = parseActions(level[0], level[1], targets[targetIndex][3], level[0][1])
                                                                            level[1] = i[0]
                                                                            targets[targetIndex][3] = i[1]
                                                                            level[0][1] = i[2]
                                                                        level[0][0].remove(targets[targetIndex])
                                                                        targets.pop(targetIndex)
                                                                    break
                                                            else:
                                                                break
                                                        break
                                                    break
                                                else:
                                                    break
                                        break
                                    else:
                                        break
                            for target in targets:
                                level[1][target[2]][target[1]] = 3
                            clear()
                            break
                elif keyPressed == "e":
                    for poi in level[0][2]:
                        if level[1][poi[1][0]][poi[1][1]] == 6:
                            if (poi[1][1] is level[0][6][playerIndexTurn][0][0]+1 and poi[1][0] is level[0][6][playerIndexTurn][0][1]) or (poi[1][1] is level[0][6][playerIndexTurn][0][0]-1 and poi[1][0] is level[0][6][playerIndexTurn][0][1]) or (poi[1][0] is level[0][6][playerIndexTurn][0][1]+1 and poi[1][1] is level[0][6][playerIndexTurn][0][0]) or (poi[1][0] is level[0][6][playerIndexTurn][0][1]-1 and poi[1][1] is level[0][6][playerIndexTurn][0][0]):
                                if poi[0][0] == "hellbomb" or poi[0][0] == "spawner":
                                    break
                                i = parseActions(level[0], level[1], poi[0], level[0][1])
                                level[1] = i[0]
                                poi[0] = i[1]
                                level[0][1] = i[2]
                elif keyPressed == "x":
                    actionItem = "\033[31mPress X again to confirm."
                    clear()
                    print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                    while True:
                        if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                            keyPressed = keyboard.read_event().name
                            if keyPressed == "x":
                                actionItem = "\033[31mEnding turn..."
                                clear()
                                print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                                time.sleep(1)
                                if len(level[0][6]) == playerIndexTurn + 1:
                                    level[0][3] = "enemy"
                                else:
                                    level[0][3] = f"player {playerIndexTurn + 1}"
                                level[0][4] = 5 + level[0][6][playerIndexTurn][3][1]
                                break
                            else:
                                break
                elif keyPressed == "g":
                    if level[0][6][playerIndexTurn][7] is not 0:
                        level[0][6][playerIndexTurn][7] -= 1
                        grenadeX = level[0][6][playerIndexTurn][0][0]
                        grenadeY = level[0][6][playerIndexTurn][0][1]-1
                        if level[1][grenadeY][grenadeX] not in [0, 1, 3, 4, 5, 8, 9]:
                            print("You cannot move the grenade there!")
                            time.sleep(100)
                        actual = level[1][grenadeY][grenadeX]
                        level[1][grenadeY][grenadeX] = 12
                        actionItem = "\033[33mpress Enter to confirm\033[0m"
                        r = 3.99
                        if level[0][6][playerIndexTurn][3][3].lower() == "servo-assisted":
                            r = 4.99
                        clear()
                        print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                        while True:
                            if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                                keyPressed = keyboard.read_event().name
                                if keyPressed == "up" or keyPressed == "w":
                                    if grenadeY <= 0 or level[1][grenadeY-1][grenadeX] in [0, 1, 3, 4, 5, 8, 9]:
                                        if hypotenuse_los(level[1], [grenadeX, grenadeY-1], level[0][6][playerIndexTurn][0], r):
                                            level[1][grenadeY][grenadeX] = actual
                                            grenadeY -= 1
                                            actual = level[1][grenadeY][grenadeX]
                                            level[1][grenadeY][grenadeX] = 12
                                elif keyPressed == "down" or keyPressed == "s":
                                    if grenadeY >= len(level[1])-1 or level[1][grenadeY+1][grenadeX] in [0, 1, 3, 4, 5, 8, 9]:
                                        if hypotenuse_los(level[1], [grenadeX, grenadeY+1], level[0][6][playerIndexTurn][0], r):
                                            level[1][grenadeY][grenadeX] = actual
                                            grenadeY += 1
                                            actual = level[1][grenadeY][grenadeX]
                                            level[1][grenadeY][grenadeX] = 12
                                elif keyPressed == "left" or keyPressed == "a":
                                    if grenadeX <= 0 or level[1][grenadeY][grenadeX-1] in [0, 1, 3, 4, 5, 8, 9]:
                                        if hypotenuse_los(level[1], [grenadeX-1, grenadeY], level[0][6][playerIndexTurn][0], r):
                                            level[1][grenadeY][grenadeX] = actual
                                            grenadeX -= 1
                                            actual = level[1][grenadeY][grenadeX]
                                            level[1][grenadeY][grenadeX] = 12
                                elif keyPressed == "right" or keyPressed == "d":
                                    if grenadeX >= len(level[1][0])-1 or level[1][grenadeY][grenadeX+1] in [0, 1, 3, 4, 5, 8, 9]:
                                        if hypotenuse_los(level[1], [grenadeX+1, grenadeY], level[0][6][playerIndexTurn][0], r):
                                            level[1][grenadeY][grenadeX] = actual
                                            grenadeX += 1
                                            actual = level[1][grenadeY][grenadeX]
                                            level[1][grenadeY][grenadeX] = 12
                                elif keyPressed == "enter" or keyPressed == "space":
                                    level[1][grenadeY][grenadeX] = actual
                                    if actual == 4:
                                        for poi in level[0][2]:
                                            if poi[1][1] == grenadeX and poi[1][0] == grenadeY:
                                                try:
                                                    i = parseActions(level[0], level[1], poi[0][1], level[0][1])
                                                    level[1] = i[0]
                                                    poi[0][1] = i[1]
                                                    level[0][1] = i[2]
                                                except Exception as e:
                                                    None
                                                level[0][2].remove(poi)
                                                level[1][grenadeY][grenadeX] = 0
                                    for enemy in list(level[0][0].copy()):
                                        if hypotenuse_los(level[1], [enemy[1], enemy[2]], [grenadeX, grenadeY], level[0][6][playerIndexTurn][14][3], grenade=True):
                                            enemy[0][11] -= level[0][6][playerIndexTurn][14][2]
                                            if enemy[0][12] <= 0:
                                                enemy[0][12] = 0
                                            if enemy[0][12] - level[0][6][playerIndexTurn][14][1] < 0:
                                                enemy[0][11] -= level[0][6][playerIndexTurn][14][1] - enemy[0][12]
                                            if enemy[0][11] <= 0:
                                                level[1][enemy[2]][enemy[1]] = 0
                                                if len(enemy) > 3:
                                                    i = parseActions(level[0], level[1], enemy[3], level[0][1])
                                                    level[1] = i[0]
                                                    enemy[3] = i[1]
                                                    level[0][1] = i[2]
                                                level[1][enemy[2]][enemy[1]] = 0
                                                level[0][0].remove(enemy)
                                    for player in level[0][6]:
                                        if hypotenuse_los(level[1], [player[0][0], player[0][1]], [grenadeX, grenadeY], level[0][6][playerIndexTurn][14][3], grenade=True):
                                            player[3][2] -= level[0][6][playerIndexTurn][14][2]
                                            if player[3][2] >= 0:
                                                player[3][2] = 0
                                            if player[3][2] - level[0][6][playerIndexTurn][14][1] < 0:
                                                player[5] +=  player[3][2] - level[0][6][playerIndexTurn][14][1]
                                            if player[5] <= 0:
                                                if player[3][3].lower() == "democracy protects" and random.randint(1, 100) <= 50:
                                                    player[5] = 1
                                                else:
                                                    player[5] = 0
                                                    if player[3][3].lower() == "integrated explosives":
                                                        for enemy in list(level[0][0].copy()):
                                                            if hypotenuse_los(level[1], [enemy[1], enemy[2]], [grenadeX, grenadeY], 1, grenade=True):
                                                                enemy[0][12] -= 10
                                                                if enemy[0][12] <= 0:
                                                                    enemy[0][12] = 0
                                                                    enemy[0][11] -= 20
                                                                if enemy[0][11] <= 0:
                                                                    level[1][enemy[2]][enemy[1]] = 0
                                                                    if len(enemy) > 3:
                                                                        i = parseActions(level[0], level[1], enemy[3], level[0][1])
                                                                        level[1] = i[0]
                                                                        enemy[3] = i[1]
                                                                        level[0][1] = i[2]
                                                                    level[1][enemy[2]][enemy[1]] = 0
                                                                    level[0][0].remove(enemy)
                                                    sys.exit(0)
                                    break
                                else:
                                    level[1][grenadeY][grenadeX] = actual
                                    break
                                clear()
                                print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                elif keyPressed == "r":
                    level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][10] = level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][4]
                    level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][11] += -1
                    level[0][6][playerIndexTurn][11] = level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][6]
                    actionItem = f"\033[33mReloading {level[0][6][playerIndexTurn][level[0][6][playerIndexTurn][4]][0]} for {level[0][6][playerIndexTurn][11]} turns...\n"
                    actionItem += f"\033[31mPress X to end turn\033[0m"
                    clear()
                    print(level[0][6][playerIndexTurn][11])
                    print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                    while True:
                        if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                            keyPressed = keyboard.read_event().name
                            if keyPressed == "x":                                
                                actionItem = "\033[31mEnding turn..."
                                clear()
                                print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                                time.sleep(1)
                                if len(level[0][6]) == playerIndexTurn + 1:
                                    level[0][3] = "enemy"
                                else:
                                    level[0][3] = f"player {playerIndexTurn + 1}"
                                level[0][4] = 5 + level[0][6][playerIndexTurn][3][1]
                                break
                            else:
                                continue
                        break
                elif keyPressed == "v":
                    if level[0][6][playerIndexTurn][9] > 0:
                        level[0][6][playerIndexTurn][9] -= 1
                        level[0][6][playerIndexTurn][5] += 60
                        if level[0][6][playerIndexTurn][5] > level[0][6][playerIndexTurn][6]:
                            level[0][6][playerIndexTurn][5] = level[0][6][playerIndexTurn][6]
                        actionItem = f"\033[33mYou have used a stim, your health is now {level[0][6][playerIndexTurn][5]}/{level[0][6][playerIndexTurn][6]}\033[0m"
                        if level[0][6][playerIndexTurn][3][3].lower() == "med-kit":
                            level[0][6][playerIndexTurn][11] = 1
                        time.sleep(2)
                clear()
                break
    elif level[0][3] == "enemy":
        for enemy in level[0][0]:
            visMod = 0
            if Ship_Mods[3] is 1 or 2 or 3 or 4:
                visMod = 1
            if level[0][6][playerIndexTurn][3][3].lower() == "scout":
                visMod += Fraction(30, 100) * enemy[0][9]
            if hypotenuse_los(level[1], [enemy[1], enemy[2]], level[0][6][playerIndexTurn][0], enemy[0][9]-visMod):
                path = find_path(level[1], [enemy[1], enemy[2]], level[0][6][playerIndexTurn][0])
                if len(path) > enemy[0][10]:
                    while len(path) > enemy[0][10]:
                        path.pop()
                for coord in path:
                    currentPos = [enemy[1], enemy[2]]
                    level[1][currentPos[1]][currentPos[0]] = 0
                    level[1][coord[1]][coord[0]] = 3
                    enemy[1] = coord[0]
                    enemy[2] = coord[1]
                    clear()
                    print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                    time.sleep(0.5)
            if enemy[0][2] == True and hypotenuse_los(level[1], [enemy[1], enemy[2]], level[0][6][playerIndexTurn][0], 1.59):
                trueDmg = 0
                dmg = enemy[0][3]
                maxArmor = level[0][6][playerIndexTurn][3][2] - enemy[0][7]
                tempArmor = maxArmor - dmg
                if maxArmor < 0:
                    maxArmor = 0
                if tempArmor < 0:
                    trueDmg = dmg - maxArmor
                    tempArmor = 0
                if trueDmg >= level[0][6][playerIndexTurn][5]:
                    trueDmg = level[0][6][playerIndexTurn][5]
                level[0][6][playerIndexTurn][3][2] = tempArmor
                level[0][6][playerIndexTurn][5] -= trueDmg
                if level[0][6][playerIndexTurn][5] <= 0:
                    if level[0][6][playerIndexTurn] [3][3].lower() == "democracy protects" and random.randint(0, 100) < 50:
                        level[0][6][playerIndexTurn][5] = 1
                    else:
                        actionItem = f"\033[31mYou have been hit for {trueDmg} damage by a {enemy[0][0]}\033[0m\n"
                        actionItem += f"\033[33mYour health is now {level[0][6][playerIndexTurn][5]}/{level[0][6][playerIndexTurn][6]}\033[0m\n"
                        actionItem += f"\033[33mYour armor is now {level[0][6][playerIndexTurn][3][2]}\033[0m\n"
                        actionItem += "\033[31mYou have been killed by an enemy\033[0m"
                        clear()
                        print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                        sys.exit()
                actionItem = f"\033[31mYou have been hit for {trueDmg} damage!\033[0m\n"
                actionItem += f"\033[33mYour health is now {level[0][6][playerIndexTurn][5]}/{level[0][6][playerIndexTurn][6]}\033[0m\n"
                actionItem += f"\033[33mYour armor is now {level[0][6][playerIndexTurn][3][2]}\033[0m\n"
                clear()
                print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                time.sleep(2)                
            elif enemy[0][5] == True:
                if hypotenuse_los(level[1], [enemy[1], enemy[2]], level[0][6][playerIndexTurn][0], enemy[0][8]):
                    trueDmg = 0
                    dmg = enemy[0][3]
                    maxArmor = level[0][6][playerIndexTurn][3][2] - enemy[0][4]
                    tempArmor = maxArmor - dmg
                    if maxArmor < 0:
                        maxArmor = 0
                    if tempArmor < 0:
                        trueDmg = dmg - maxArmor
                        tempArmor = 0
                    if trueDmg >= level[0][6][playerIndexTurn][5]:
                        trueDmg = level[0][6][playerIndexTurn][5]
                    level[0][6][playerIndexTurn][3][2] = tempArmor
                    level[0][6][playerIndexTurn][5] -= trueDmg
                    if level[0][6][playerIndexTurn][5] <= 0:
                        if level[0][6][playerIndexTurn] [3][3].lower() == "democracy protects" and random.randint(0, 100) < 50:
                            level[0][6][playerIndexTurn][5] = 1
                        else:
                            actionItem = f"\033[31mYou have been hit for {trueDmg} damage by a {enemy[0][0]}\033[0m\n"
                            actionItem += f"\033[33mYour health is now {level[0][6][playerIndexTurn][5]}/{level[0][6][playerIndexTurn][6]}\033[0m\n"
                            actionItem += f"\033[33mYour armor is now {level[0][6][playerIndexTurn][3][2]}\033[0m\n"
                            actionItem += "\033[31mYou have been killed by an enemy\033[0m"
                            clear()
                            print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                            sys.exit()
                    actionItem = f"\033[31mYou have been hit for {trueDmg} damage by a {enemy[0][0]}\033[0m\n"
                    actionItem += f"\033[33mYour health is now {level[0][6][playerIndexTurn][5]}/{level[0][6][playerIndexTurn][6]}\033[0m\n"
                    actionItem += f"\033[33mYour armor is now {level[0][6][playerIndexTurn][3][2]}\033[0m\n"
                    clear()
                    print_centered(f"{parse_level(level,enemies=level[0][0], actionItem = actionItem)}")
                    time.sleep(2)
        clear()
        level[0][3] = "spawners"
    elif level[0][3] == "spawners":
        for poi in level[0][2]:
            if poi[0][0] == "spawner":
                if level[1][poi[1][0]][poi[1][1]] == 4:
                    for _ in range(random.randint(1, 3)):
                        enemy = list(exponential_weighted_choice(level[0][7]))
                        for yS in range(poi[1][0]+2, poi[1][0]-2, -1):
                            for xS in range(poi[1][1]+2, poi[1][1]-2, -1):
                                if level[1][yS][xS] == 0:
                                    level[1][yS][xS] = 3
                                    level[0][0].append(list((enemy, xS, yS)))
                                    clear()
                                    print_centered(f"{parse_level(level=level,enemies=level[0][0], actionItem = actionItem)}")
                                    time.sleep(1)
                                    break
                                else:
                                    continue
                            break
        level[0][3] = "player 0"
print_slow("ALERT: ENCRYPTED TRANSMISSION RECEIVED\n\nDECRYPTING...\n.\n.\n.\nCLASSIFICATION: TOP SECRET\n\nMINISTRY OF DEFENSE\nDIRECTORY OF HELLDIVER READINESS\nORIGINATING STATION: MARS\n\nMEMORANDUM FOR: Helldiver Readiness Command\nSUBJECT: Daily Incoming Recruit Report\n\nTotal Incoming Trainees: 48,736\nAvg. Age(Years): 18.7\nAvg. Combat Readiness Rating: 27.1%\nAvg. Patriotism Rating: 97.4%\n\nExpected Survival Rate: 21.3%\nProjected Helldiver Production: WITHIN QUOTA\n\nEND TRANSMISSION ")
print("You step out of your cryopod, shivering from the cold. The super destroyer awaits your command.")
print("What is your name, helldiver?")
Name = input("Enter your name: ")
print(f"Welcome to the Helldivers {Name}")
while True:
    clear()
    print("What do you wish to do?\n\t1:Enter the Galactic War\n\t2:Customize your Super Destroyer\n\t3:Alter your Equipment\n\t4:Exit game")
    Current_Decision = int(input("Enter your choice: "))
    if Current_Decision is 1:
        clear()
        print("You have entered the Galactic War")
        break
    elif Current_Decision is 2:
        while True:
            clear()
            print("You have entered the Super Destroyer customization menu")
            print("What would you like to customize?\n\t1:Ship Name\n\t2:Ship Modules")
            Current_Decision = int(input("Enter your choice: "))        
            if Current_Decision is 1:
                clear()
                print("You have chosen to customize the ship name")
                Ship_Name = input("Enter new ship name: ")
                print(f"Ship name changed to SES {Ship_Name}")
                break
            elif Current_Decision is 2:
                while True:
                    clear()
                    print("What module would you like to customize?\n\t1:Patriotic Administration Center\n\t2:Orbital Cannons\n\t3:Hangar\n\t4:Bridge\n\t5:Engineering Bay\n\t6:Robotics Workshop\n\t7:exit")
                    Current_Decision = int(input("Enter your choice: "))
                    if Current_Decision is 1:
                        while True:
                            clear()
                            next_mod = ""
                            print_centered(f"Requisition: {str(Requisition)}R")
                            print("\n\n\n")
                            print_centered("| Patriotic Administration Center |\n")
                            os.system('color 06')
                            if(Ship_Mods[0] is 0):
                                next_mod = "Donation Access License"
                                print_centered("\nDonation Access License: Support Weapons deploy with an extra magazine.")
                                print_centered("\nStreamlined Request Process: Reduces Support Weapon Stratagem cooldown")
                                print_centered("\nHand Carts: Reduces Backpack Stratagem cooldown")
                                print_centered("\nSuperior Packing Methodology: Resupply Boxes fill support weapons to maximum ammo")
                                print_centered("\nPayroll Management System: Reduces reload time for Support Weapons")
                                
                            elif(Ship_Mods[0] is 1):
                                next_mod = "Streamlined Request Process"
                                print_centered("\n✓ Donation Access License: Support Weapons deploy with an extra magazine. ✓")
                                print_centered("\nStreamlined Request Process: Reduces Support Weapon Stratagem cooldown")
                                print_centered("\nHand Carts: Reduces Backpack Stratagem cooldown")
                                print_centered("\nSuperior Packing Methodology: Resupply Boxes fill support weapons to maximum ammo")
                                print_centered("\nPayroll Management System: Reduces reload time for Support Weapons")
                            elif(Ship_Mods[0] is 2):
                                next_mod = "Hand Carts"
                                print_centered("\n✓ Donation Access License: Support Weapons deploy with an extra magazine. ✓")
                                print_centered("\n✓ Streamlined Request Process: Reduces Support Weapon Stratagem cooldown ✓")
                                print_centered("\nHand Carts: Reduces Backpack Stratagem cooldown")
                                print_centered("\nSuperior Packing Methodology: Resupply Boxes fill support weapons to maximum ammo")
                                print_centered("\nPayroll Management System: Reduces reload time for Support Weapons")
                            elif(Ship_Mods[0] is 3):
                                next_mod = "Superior Packing Methodology"
                                print_centered("\n✓ Donation Access License: Support Weapons deploy with an extra magazine. ✓")
                                print_centered("\n✓ Streamlined Request Process: Reduces Support Weapon Stratagem cooldown ✓")
                                print_centered("\n✓ Hand Carts: Reduces Backpack Stratagem cooldown ✓")
                                print_centered("\nSuperior Packing Methodology: Resupply Boxes fill support weapons to maximum ammo")
                                print_centered("\nPayroll Management System: Reduces reload time for Support Weapons")
                            elif(Ship_Mods[0] is 4):
                                next_mod = "Payroll Management System"
                                print_centered("\n✓ Donation Access License: Support Weapons deploy with an extra magazine. ✓")
                                print_centered("\n✓ Streamlined Request Process: Reduces Support Weapon Stratagem cooldown ✓")
                                print_centered("\n✓ Hand Carts: Reduces Backpack Stratagem cooldown ✓")
                                print_centered("\n✓ Superior Packing Methodology: Resupply Boxes fill support weapons to maximum ammo ✓")
                                print_centered("\nPayroll Management System: Reduces reload time for Support Weapons")
                            elif(Ship_Mods[0] is 5):
                                print_centered("\n✓ Donation Access License: Support Weapons deploy with an extra magazine. ✓")
                                print_centered("\n✓ Streamlined Request Process: Reduces Support Weapon Stratagem cooldown ✓")
                                print_centered("\n✓ Hand Carts: Reduces Backpack Stratagem cooldown ✓")
                                print_centered("\n✓ Superior Packing Methodology: Resupply Boxes fill support weapons to maximum ammo ✓")
                                print_centered("\n✓ Payroll Management System: Reduces reload time for Support Weapons ✓")
                            if next_mod != "":
                                next_mod_cost = (Ship_Mods[0]+1) * 5000
                                print_centered(f"\n\nwould you like to purchase {next_mod} for {next_mod_cost} Requisition? (y/n)")
                                purchase = input(xHalfStr).strip().lower()
                                if purchase is 'y':
                                    if Requisition < next_mod_cost:
                                        clear()
                                        print_centered("You do not have enough Requisition to purchase this module")
                                        continue
                                    else:
                                        Requisition -= next_mod_cost
                                        Ship_Mods[0] += 1
                                        clear()
                                        continue
                                elif purchase is 'n':
                                    clear()
                                    print_centered("You have chosen not to purchase the module")
                                    break
                                else:
                                    clear
                                    print_centered("Invalid choice, please try again.")
                            else:
                                print_centered("\n\nYou have purchased all available modules for the Patriotic Administration Center")
                                print_centered("press any key to exit")
                                hide_cursor()
                                while True:
                                    if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                                        break
                                show_cursor()
                                break
                    elif Current_Decision is 2:
                        while True:
                            clear()
                            next_mod = ""
                            print_centered(f"Requisition: {str(Requisition)}R")
                            print("\n\n\n")
                            print_centered("| Orbital Cannons |\n")
                            os.system('color 06')
                            if(Ship_Mods[1] is 0):
                                next_mod = "Exploding Shrapnel"
                                print_centered("\nExploding Shrapnel: Increases damage of Orbital Stratagems")
                                print_centered("\nMore Guns: Barrage Orbital Stratagems fire more shots")
                                print_centered("\nZero-G Breech Loading: Reduces Orbital Stratagem cooldown")
                                print_centered("\nAtmospheric Monitoring: Increases accuracy of Orbital Stratagems.")
                                print_centered("\nNuclear Radar: Increases damage radius of Orbital Stratagems")
                                print_centered("\nHigh-Density Explosives: Explosive Orbital Stratagems deal more damage and have increased blast radius")
                            elif(Ship_Mods[1] is 1):
                                next_mod = "More Guns"
                                print_centered("\n✓ Exploding Shrapnel: Increases damage of Orbital Stratagems ✓")
                                print_centered("\nMore Guns: Barrage Orbital Stratagems fire more shots")
                                print_centered("\nZero-G Breech Loading: Reduces Orbital Stratagem cooldown")                                
                                print_centered("\nAtmospheric Monitoring: Increases accuracy of Orbital Stratagems.")
                                print_centered("\nNuclear Radar: Increases damage radius of Orbital Stratagems")
                                print_centered("\nHigh-Density Explosives: Explosive Orbital Stratagems deal more damage and have increased blast radius")
                            elif(Ship_Mods[1] is 2):
                                next_mod = "Zero-G Breech Loading"
                                print_centered("\n✓ Exploding Shrapnel: Increases damage of Orbital Stratagems ✓")
                                print_centered("\n✓ More Guns: Barrage Orbital Stratagems fire more shots ✓")
                                print_centered("\nZero-G Breech Loading: Reduces Orbital Stratagem cooldown")
                                print_centered("\nAtmospheric Monitoring: Increases accuracy of Orbital Stratagems.")
                                print_centered("\nNuclear Radar: Increases damage radius of Orbital Stratagems")
                                print_centered("\nHigh-Density Explosives: Explosive Orbital Stratagems deal more damage and have increased blast radius")
                            elif(Ship_Mods[1] is 3):
                                next_mod = "Atmospheric Monitoring"
                                print_centered("\n✓ Exploding Shrapnel: Increases damage of Orbital Stratagems ✓")                                
                                print_centered("\n✓ More Guns: Barrage Orbital Stratagems fire more shots ✓")
                                print_centered("\n✓ Zero-G Breech Loading: Reduces Orbital Stratagem cooldown ✓")
                                print_centered("\nAtmospheric Increases accuracy of Orbital Stratagems.")
                                print_centered("\nNuclear Radar: Increases damage radius of Orbital Stratagems")
                                print_centered("\nHigh-Density Explosives: Explosive Orbital Stratagems deal more damage and have increased blast radius")
                            elif(Ship_Mods[1] is 4):
                                next_mod = "Nuclear Radar"
                                print_centered("\n✓ Exploding Shrapnel: Increases damage of Orbital Stratagems ✓")
                                print_centered("\n✓ More Guns: Barrage Orbital Stratagems fire more shots ✓")
                                print_centered("\n✓ Zero-G Breech Loading: Reduces Orbital Stratagem cooldown ✓")
                                print_centered("\n✓ Atmospheric Monitoring: Increases accuracy of Orbital Stratagems. ✓")
                                print_centered("\nNuclear Radar: Increases damage radius of Orbital Stratagems")
                                print_centered("\nHigh-Density Explosives: Explosive Orbital Stratagems deal more damage and have increased blast radius")
                            elif(Ship_Mods[1] is 5):
                                next_mod = "High-Density Explosives"
                                print_centered("\n✓ Exploding Shrapnel: Increases damage of Orbital Stratagems ✓")
                                print_centered("\n✓ More Guns: Barrage Orbital Stratagems fire more shots ✓")
                                print_centered("\n✓ Zero-G Breech Loading: Reduces Orbital Stratagem cooldown ✓")
                                print_centered("\n✓ Atmospheric Monitoring: Increases accuracy of Orbital Stratagems. ✓")
                                print_centered("\n✓ Nuclear Radar: Increases damage radius of Orbital Stratagems ✓")
                                print_centered("\nHigh-Density Explosives: Explosive Orbital Stratagems deal more damage and have increased blast radius")
                            elif(Ship_Mods[1] is 6):
                                print_centered("\n✓ Exploding Shrapnel: Increases damage of Orbital Stratagems ✓")
                                print_centered("\n✓ More Guns: Barrage Orbital Stratagems fire more shots ✓")
                                print_centered("\n✓ Zero-G Breech Loading: Reduces Orbital Stratagem cooldown ✓")
                                print_centered("\n✓ Atmospheric Monitoring: Increases accuracy of Orbital Stratagems. ✓")
                                print_centered("\n✓ Nuclear Radar: Increases damage radius of Orbital Stratagems ✓")
                                print_centered("\n✓ High-Density Explosives: Explosive Orbital Stratagems deal more damage and have increased blast radius ✓")
                            if next_mod != "":
                                next_mod_cost = (Ship_Mods[1]+1) * 5000
                                print_centered(f"\n\nwould you like to purchase {next_mod} for {next_mod_cost} Requisition? (y/n)")
                                xHalfStr = ""
                                for _ in range(int(x/2)-1):
                                    xHalfStr += " "
                                purchase = input(xHalfStr).strip().lower()
                                if purchase is 'y':
                                    if Requisition < next_mod_cost:
                                        clear()
                                        print_centered("You do not have enough Requisition to purchase this module")
                                        continue
                                    else:
                                        Requisition -= next_mod_cost
                                        Ship_Mods[1] += 1
                                        clear()
                                        continue
                                elif purchase is 'n':
                                    clear()
                                    print_centered("You have chosen not to purchase the module")
                                    break
                                else:
                                    clear
                                    print_centered("Invalid choice, please try again.")
                            else:
                                print_centered("\n\nYou have purchased all available modules for the Orbital Cannons")
                                print_centered("press any key to exit")
                                hide_cursor()
                                while True:
                                    if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                                        break
                                show_cursor()
                                break
                    elif Current_Decision is 3:
                        while True:
                            clear()
                            next_mod = ""
                            print_centered(f"Requisition: {str(Requisition)}R")
                            print("\n\n\n")
                            print_centered("| Hangar |\n")
                            os.system('color 06')
                            if(Ship_Mods[2] is 0):
                                next_mod = "Liquid-Ventilated Cockpit"
                                print_centered("\nLiquid-Ventilated Cockpit: Eagle Stratagems cooldown time is reduced")
                                print_centered("\nPit Crew Hazard Pay: Reduces Rearm time of Eagle Stratagems")
                                print_centered("\nExpanded Weapons Bay: Increases number of Eagle Stratagems per Rearm by 1")
                                print_centered("\nXXL Weapons Bay: Explosive Eagle Stratagems drop 1 additional bomb(s)")
                                print_centered("\nAdvanced Crew Training: Further reduces Rearm time of Eagle Stratagems if there are remaining uses")
                            elif(Ship_Mods[2] is 1):
                                next_mod = "Pit Crew Hazard Pay"
                                print_centered("\n✓ Liquid-Ventilated Cockpit: Eagle Stratagems cooldown time is reduced ✓")
                                print_centered("\nPit Crew Hazard Pay: Reduces Rearm time of Eagle Stratagems")
                                print_centered("\nExpanded Weapons Bay: Increases number of Eagle Stratagems per Rearm by 1")
                                print_centered("\nXXL Weapons Bay: Explosive Eagle Stratagems drop 1 additional bomb(s)")
                                print_centered("\nAdvanced Crew Training: Further reduces Rearm time of Eagle Stratagems if there are remaining uses")
                            elif(Ship_Mods[2] is 2):
                                next_mod = "Expanded Weapons Bay"
                                print_centered("\n✓ Liquid-Ventilated Cockpit: Eagle Stratagems cooldown time is reduced ✓")
                                print_centered("\n✓ Pit Crew Hazard Pay: Reduces Rearm time of Eagle Stratagems ✓")
                                print_centered("\nExpanded Weapons Bay: Increases number of Eagle Stratagems per Rearm by 1")
                                print_centered("\nXXL Weapons Bay: Explosive Eagle Stratagems drop 1 additional bomb(s)")
                                print_centered("\nAdvanced Crew Training: Further reduces Rearm time of Eagle Stratagems if there are remaining uses")
                            elif(Ship_Mods[2] is 3):
                                next_mod = "XXL Weapons Bay"
                                print_centered("\n✓ Liquid-Ventilated Cockpit: Eagle Stratagems cooldown time is reduced ✓")
                                print_centered("\n✓ Pit Crew Hazard Pay: Reduces Rearm time of Eagle Stratagems ✓")
                                print_centered("\n✓ Expanded Weapons Bay: Increases number of Eagle Stratagems per Rearm by 1 ✓")
                                print_centered("\nXXL Weapons Bay: Explosive Eagle Stratagems drop 1 additional bomb(s)")
                                print_centered("\nAdvanced Crew Training: Further reduces Rearm time of Eagle Stratagems if there are remaining uses")
                            elif(Ship_Mods[2] is 4):
                                next_mod = "Advanced Crew Training"
                                print_centered("\n✓ Liquid-Ventilated Cockpit: Eagle Stratagems cooldown time is reduced ✓")
                                print_centered("\n✓ Pit Crew Hazard Pay: Reduces Rearm time of Eagle Stratagems ✓")
                                print_centered("\n✓ Expanded Weapons Bay: Increases number of Eagle Stratagems per Rearm by 1 ✓")
                                print_centered("\n✓ XXL Weapons Bay: Explosive Eagle Stratagems drop 1 additional bomb(s) ✓")
                                print_centered("\nAdvanced Crew Training: Further reduces Rearm time of Eagle Stratagems if there are remaining uses")
                            elif(Ship_Mods[2] is 5):
                                print_centered("\n✓ Liquid-Ventilated Cockpit: Eagle Stratagems cooldown time is reduced ✓")
                                print_centered("\n✓ Pit Crew Hazard Pay: Reduces Rearm time of Eagle Stratagems ✓")
                                print_centered("\n✓ Expanded Weapons Bay: Increases number of Eagle Stratagems per Rearm by 1 ✓")
                                print_centered("\n✓ XXL Weapons Bay: Explosive Eagle Stratagems drop 1 additional bomb(s) ✓")
                                print_centered("\n✓ Advanced Crew Training: Further reduces Rearm time of Eagle Stratagems if there are remaining uses ✓")
                            if next_mod != "":
                                next_mod_cost = (Ship_Mods[2]+1) * 5000
                                print_centered(f"\n\nwould you like to purchase {next_mod} for {next_mod_cost} Requisition? (y/n)")
                                xHalfStr = ""
                                for _ in range(int(x/2)-1):
                                    xHalfStr += " "
                                purchase = input(xHalfStr).strip().lower()
                                if purchase is 'y':
                                    if Requisition < next_mod_cost:
                                        clear()
                                        print_centered("You do not have enough Requisition to purchase this module")
                                        continue
                                    else:
                                        Requisition -= next_mod_cost
                                        Ship_Mods[2] += 1
                                        clear()
                                        continue
                                elif purchase is 'n':
                                    clear()
                                    print_centered("You have chosen not to purchase the module")
                                    break
                                else:
                                    clear
                                    print_centered("Invalid choice, please try again.")
                            else:
                                print_centered("\n\nYou have purchased all available modules for the Hangar")
                                print_centered("press any key to exit")
                                hide_cursor()
                                while True:
                                    if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                                        break
                                show_cursor()
                                break
                    elif Current_Decision is 4:
                        while True:
                            clear()
                            next_mod = ""
                            print_centered(f"Requisition: {str(Requisition)}R")
                            print("\n\n\n")
                            print_centered("| Bridge |\n")
                            os.system('color 06')
                            if(Ship_Mods[3] is 0):
                                next_mod = "Targeting Software Upgrade"
                                print_centered("\nTargeting Software Upgrade: Reduces cooldown of all Orbital Stratagems")
                                print_centered("\nNuclear Radar: Increases accuracy of Orbital Stratagems")
                                print_centered("\nPower Steering: Decreases call-in time of all Eagle Stratagems")
                                print_centered("\nEnhanced Combustion: Fire damage from Stratagems increased")
                                print_centered('\nMorale Augmentation: Reduces cooldown time for all Stratagems')
                            elif(Ship_Mods[3] is 1):
                                next_mod = "Nuclear Radar"
                                print_centered("\n✓ Targeting Software Upgrade: Reduces cooldown of all Orbital Stratagems ✓")
                                print_centered("\nNuclear Radar: Increases accuracy of Orbital Stratagems")
                                print_centered("\nPower Steering: Decreases call-in time of all Eagle Stratagems")
                                print_centered("\nEnhanced Combustion: Fire damage from Stratagems increased")
                                print_centered('\nMorale Augmentation: Reduces cooldown time for all Stratagems')
                            elif(Ship_Mods[3] is 2):
                                next_mod = "Power Steering"
                                print_centered("\n✓ Targeting Software Upgrade: Reduces cooldown of all Orbital Stratagems ✓")
                                print_centered("\n✓ Nuclear Radar: Increases accuracy of Orbital Stratagems ✓")
                                print_centered("\nPower Steering: Decreases call-in time of all Eagle Stratagems")
                                print_centered("\nEnhanced Combustion: Fire damage from Stratagems increased")
                                print_centered('\nMorale Augmentation: Reduces cooldown time for all Stratagems')
                            elif(Ship_Mods[3] is 3):
                                next_mod = "Enhanced Combustion"                                                                                                                                                                                                                                                                                                                                                                                                                       
                                print_centered("\n✓ Targeting Software Upgrade: Reduces cooldown of all Orbital Stratagems ✓")
                                print_centered("\n✓ Nuclear Radar: Increases accuracy of Orbital Stratagems ✓")
                                print_centered("\n✓ Power Steering: Decreases call-in time of all Eagle Stratagems ✓")
                                print_centered("\nEnhanced Combustion: Fire damage from Stratagems increased")
                                print_centered('\nMorale Augmentation: Reduces cooldown time for all Stratagems')
                            elif(Ship_Mods[3] is 4):
                                next_mod = "Morale Augmentation"
                                print_centered("\n✓ Targeting Software Upgrade: Reduces cooldown of all Orbital Stratagems ✓")
                                print_centered("\n✓ Nuclear Radar: Increases accuracy of Orbital Stratagems ✓")
                                print_centered("\n✓ Power Steering: Decreases call-in time of all Eagle Stratagems ✓")
                                print_centered("\n✓ Enhanced Combustion: Fire damage from Stratagems increased ✓")
                                print_centered('\nMorale Augmentation: Reduces cooldown time for all Stratagems')
                            elif(Ship_Mods[3] is 5):
                                print_centered("\n✓ Targeting Software Upgrade: Reduces cooldown of all Orbital Stratagems ✓")
                                print_centered("\n✓ Nuclear Radar: Increases accuracy of Orbital Stratagems ✓")
                                print_centered("\n✓ Power Steering: Decreases call-in time of all Eagle Stratagems ✓")
                                print_centered("\n✓ Enhanced Combustion: Fire damage from Stratagems increased ✓")
                                print_centered('\n✓ Morale Augmentation: Reduces cooldown time for all Stratagems ✓')
                            if next_mod != "":
                                next_mod_cost = (Ship_Mods[3]+1) * 5000
                                print_centered(f"\n\nwould you like to purchase {next_mod} for {next_mod_cost} Requisition? (y/n)")
                                xHalfStr = ""
                                for _ in range(int(x/2)-1):
                                    xHalfStr += " "
                                purchase = input(xHalfStr).strip().lower()
                                if purchase is 'y':
                                    if Requisition < next_mod_cost:
                                        clear()
                                        print_centered("You do not have enough Requisition to purchase this module")
                                        continue
                                    else:
                                        Requisition -= next_mod_cost
                                        Ship_Mods[3] += 1
                                        clear()
                                        continue
                                elif purchase is 'n':
                                    clear()
                                    print_centered("You have chosen not to purchase the module")
                                    break
                                else:
                                    clear
                                    print_centered("Invalid choice, please try again.")
                            else:
                                print_centered("\n\nYou have purchased all available modules for the Bridge")
                                print_centered("press any key to exit")
                                hide_cursor()
                                while True:
                                    if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                                        break
                                show_cursor()
                                break
                    elif Current_Decision is 5:
                        while True:
                            clear()
                            next_mod = ""
                            print_centered(f"Requisition: {str(Requisition)}R")
                            print("\n\n\n")
                            print_centered("| Engineering Bay |\n")
                            os.system('color 06')
                            if(Ship_Mods[4] is 0):
                                next_mod = "Synthetic Supplementation"
                                print_centered("\nSynthetic Supplementation: Reduces cooldown time for Defensive and Resupply Stratagems")
                                print_centered("\nAdvanced Construction: Increases health of Sentry Stratagems")
                                print_centered("\nRapid Launch System: All Emplacement Stratagems deploy instantly")
                                print_centered("\nCircuit Expansion: Arc and Energy damage increased")
                                print_centered("\nStreamlined Launch Process: All Support Weapon Stratagems deploy instantly")
                            elif(Ship_Mods[4] is 1):
                                next_mod = "Advanced Construction"
                                print_centered("\n✓ Synthetic Supplementation: Reduces cooldown time for Defensive and Resupply Stratagems ✓")
                                print_centered("\nAdvanced Construction: Increases health of Sentry Stratagems")
                                print_centered("\nRapid Launch System: All Emplacement Stratagems deploy instantly")
                                print_centered("\nCircuit Expansion: Arc and Energy damage increased")
                                print_centered("\nStreamlined Launch Process: All Support Weapon Stratagems deploy instantly")
                            elif(Ship_Mods[4] is 2):
                                next_mod = "Rapid Launch System"
                                print_centered("\n✓ Synthetic Supplementation: Reduces cooldown time for Defensive and Resupply Stratagems ✓")
                                print_centered("\n✓ Advanced Construction: Increases health of Sentry Stratagems ✓")
                                print_centered("\nRapid Launch System: All Emplacement Stratagems deploy instantly")
                                print_centered("\nCircuit Expansion: Arc and Energy damage increased")
                                print_centered("\nStreamlined Launch Process: All Support Weapon Stratagems deploy instantly")
                            elif(Ship_Mods[4] is 3):
                                next_mod = "Circuit Expansion"
                                print_centered("\n✓ Synthetic Supplementation: Reduces cooldown time for Defensive and Resupply Stratagems ✓")
                                print_centered("\n✓ Advanced Construction: Increases health of Sentry Stratagems ✓")
                                print_centered("\n✓ Rapid Launch System: All Emplacement Stratagems deploy instantly ✓")
                                print_centered("\nCircuit Expansion: Arc and Energy damage increased")
                                print_centered("\nStreamlined Launch Process: All Support Weapon Stratagems deploy instantly")
                            elif(Ship_Mods[4] is 4):
                                next_mod = "Streamlined Launch Process"
                                print_centered("\n✓ Synthetic Supplementation: Reduces cooldown time for Defensive and Resupply Stratagems ✓")
                                print_centered("\n✓ Advanced Construction: Increases health of Sentry Stratagems ✓")
                                print_centered("\n✓ Rapid Launch System: All Emplacement Stratagems deploy instantly ✓")
                                print_centered("\n✓ Circuit Expansion: Arc and Energy damage increased ✓")
                                print_centered("\nStreamlined Launch Process: All Support Weapon Stratagems deploy instantly")
                            elif(Ship_Mods[4] is 5):
                                print_centered("\n✓ Synthetic Supplementation: Reduces cooldown time for Defensive and Resupply Stratagems ✓")
                                print_centered("\n✓ Advanced Construction: Increases health of Sentry Stratagems ✓")
                                print_centered("\n✓ Rapid Launch System: All Emplacement Stratagems deploy instantly ✓")
                                print_centered("\n✓ Circuit Expansion: Arc and Energy damage increased ✓")
                                print_centered("\n✓ Streamlined Launch Process: All Support Weapon Stratagems deploy instantly ✓")
                            if next_mod != "":
                                next_mod_cost = (Ship_Mods[4]+1) * 5000
                                print_centered(f"\n\nwould you like to purchase {next_mod} for {next_mod_cost} Requisition? (y/n)")
                                xHalfStr = ""
                                for _ in range(int(x/2)-1):
                                    xHalfStr += " "
                                purchase = input(xHalfStr).strip().lower()
                                if purchase is 'y':
                                    if Requisition < next_mod_cost:
                                        clear()
                                        print_centered("You do not have enough Requisition to purchase this module")
                                        continue
                                    else:
                                        Requisition -= next_mod_cost
                                        Ship_Mods[4] += 1
                                        clear()
                                        continue
                                elif purchase is 'n':
                                    clear()
                                    print_centered("You have chosen not to purchase the module")
                                    break
                                else:
                                    clear
                                    print_centered("Invalid choice, please try again.")
                            else:
                                print_centered("\n\nYou have purchased all available modules for the Engineering Bay")
                                print_centered("press any key to exit")
                                hide_cursor()
                                while True:
                                    if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                                        break
                                show_cursor()
                                break        
                    elif Current_Decision is 6:
                        while True:
                            clear()
                            next_mod = ""
                            print_centered(f"Requisition: {str(Requisition)}R")
                            print("\n\n\n")
                            print_centered("| Robotics Workshop |\n")
                            os.system('color 06')
                            if(Ship_Mods[5] is 0):
                                next_mod = "Dynamic Tracking"
                                print_centered("\nDynamic Tracking: All Sentry Stratagems deploy instantly")
                                print_centered("\nShock Absorption Gel: Increases ammo for Sentry Stratagems")
                                print_centered("\nHigh-Quality Lubricant: Sentry Stratagems have increased fire rate")
                                print_centered("\nBlast Absorption: Sentry Stratagems take less damage from explosions")
                                print_centered("\nCross-Platform Compatibility: Mortar Sentry Stratagems target large enemies first")
                            elif(Ship_Mods[5] is 1):
                                next_mod = "Shock Absorption Gel"
                                print_centered("\n✓ Dynamic Tracking: All Sentry Stratagems deploy instantly ✓")
                                print_centered("\nShock Absorption Gel: Increases ammo for Sentry Stratagems")
                                print_centered("\nHigh-Quality Lubricant: Sentry Stratagems have increased fire rate")
                                print_centered("\nBlast Absorption: Sentry Stratagems take less damage from explosions")
                                print_centered("\nCross-Platform Compatibility: Mortar Sentry Stratagems target large enemies first")
                            elif(Ship_Mods[5] is 2):
                                next_mod = "High-Quality Lubricant"
                                print_centered("\n✓ Dynamic Tracking: All Sentry Stratagems deploy instantly ✓")
                                print_centered("\n✓ Shock Absorption Gel: Increases ammo for Sentry Stratagems ✓")
                                print_centered("\nHigh-Quality Lubricant: Sentry Stratagems have increased fire rate")
                                print_centered("\nBlast Absorption: Sentry Stratagems take less damage from explosions")
                                print_centered("\nCross-Platform Compatibility: Mortar Sentry Stratagems target large enemies first")
                            elif(Ship_Mods[5] is 3):
                                next_mod = "Blast Absorption"
                                print_centered("\n✓ Dynamic Tracking: All Sentry Stratagems deploy instantly ✓")
                                print_centered("\n✓ Shock Absorption Gel: Increases ammo for Sentry Stratagems ✓")
                                print_centered("\n✓ High-Quality Lubricant: Sentry Stratagems have increased fire rate ✓")
                                print_centered("\nBlast Absorption: Sentry Stratagems take less damage from explosions")
                                print_centered("\nCross-Platform Compatibility: Mortar Sentry Stratagems target large enemies first")
                            elif(Ship_Mods[5] is 4):
                                next_mod = "Cross-Platform Compatibility"
                                print_centered("\n✓ Dynamic Tracking: All Sentry Stratagems deploy instantly ✓")
                                print_centered("\n✓ Shock Absorption Gel: Increases ammo for Sentry Stratagems ✓")
                                print_centered("\n✓ High-Quality Lubricant: Sentry Stratagems have increased fire rate ✓")
                                print_centered("\n✓ Blast Absorption: Sentry Stratagems take less damage from explosions ✓")
                                print_centered("\nCross-Platform Compatibility: Mortar Sentry Stratagems target large enemies first")
                            elif(Ship_Mods[5] is 5):
                                print_centered("\n✓ Dynamic Tracking: All Sentry Stratagems deploy instantly ✓")
                                print_centered("\n✓ Shock Absorption Gel: Increases ammo for Sentry Stratagems ✓")
                                print_centered("\n✓ High-Quality Lubricant: Sentry Stratagems have increased fire rate ✓")
                                print_centered("\n✓ Blast Absorption: Sentry Stratagems take less damage from explosions ✓")
                                print_centered("\n✓ Cross-Platform Compatibility: Mortar Sentry Stratagems target large enemies first ✓")
                            if next_mod != "":
                                next_mod_cost = (Ship_Mods[5]+1) * 5000
                                print_centered(f"\n\nwould you like to purchase {next_mod} for {next_mod_cost} Requisition? (y/n)")
                                xHalfStr = ""
                                for _ in range(int(x/2)-1):
                                    xHalfStr += " "
                                purchase = input(xHalfStr).strip().lower()
                                if purchase is 'y':
                                    if Requisition < next_mod_cost:
                                        clear()
                                        print_centered("You do not have enough Requisition to purchase this module")
                                        continue
                                    else:
                                        Requisition -= next_mod_cost
                                        Ship_Mods[5] += 1
                                        clear()
                                        continue
                                elif purchase is 'n':
                                    clear()
                                    print_centered("You have chosen not to purchase the module")
                                    break
                                else:
                                    clear
                                    print_centered("Invalid choice, please try again.")
                            else:
                                print_centered("\n\nYou have purchased all available modules for the Robotics Workshop")
                                print_centered("press any key to exit")
                                hide_cursor()
                                while True:
                                    if keyboard.read_event().event_type is keyboard.KEY_DOWN:
                                        break
                                show_cursor()
                                break
                    elif Current_Decision is 7:
                        clear()
                        break
                    os.system('color 06')
            else:
                print("Invalid choice, please try again.")
    elif Current_Decision is 3:
        clear()
        print("You have entered the Equipment customization menu")
        print("Choose Weapons\n Primaries:\n1.) Liberator Penetrator\n2.) LAS-5 Scythe\n3.) PLAS-1 Scorcher\n4.) FLA-66 Torcher\n5.) Explosive Crossbow\n Secondaries:\n6.) LAS-7 Dagger\n7.) P-2 Peacemaker\n8.) P-19 Redeemer\n9.) CQC-19 Stun Lance\n10.) GP-31 Ultimatum\n11.) P4-Senator")
        if Current_Decision is 4:
            print("Choose Grenades\n 1.) G-6 Frag\n2.)G-12 High Explosive\n3.)G-16 Impact\n4.)G-4 Gas\n5.)G-10 Incindiary\n6.)G-123 Thermite\n")
    elif Current_Decision is 4:
        clear()
        print("Exiting game...\033[0m")
        exit()
    else:
        print("Invalid choice, please try again.")
clear()
while True:
    print("Which faction would you like to fight?\n\t1:The Terminid\n\t2:The Automatons\n\t3:The Illuminate")
    Current_Decision = int(input("Enter faction number: "))
    Faction="None"
    if Current_Decision is 1:
        Faction="Terminid"
        break
    elif Current_Decision is 2:
        Faction="Automatons"
        break
    elif Current_Decision is 3:
        Faction="Illuminate"
        break
    else:
        clear()
        print("Democracy Needs You! You MUST choose one of these enemies to liberate.")

print("Choose mission type\n\t1:Exterminate\n\t2:Evacuate Civilians\n\t3:Launch ICBM\n\t4:Raise flag\n\t5:Destroy outposts")
Current_Decision = int(input("Enter mission number: "))
if Current_Decision is 1:
    Mission_Type="Exterminate"
    Max_Maps = len(Exterminate)-1
elif Current_Decision is 2:
    Mission_Type="Evacuate Civilians"
    Max_Maps = len(Evac_Civs)-1
elif Current_Decision is 3:
    Mission_Type="Launch ICBM"
    Max_Maps = len(ICBM)-1
elif Current_Decision is 4:
    Mission_Type="Raise flag"
    Max_Maps = len(Raise_Flag)-1
elif Current_Decision is 5:
    Mission_Type="Destroy outposts"
    Max_Maps = len(Destroy_Outposts)-1
elif Current_Decision is -420:
    Mission_Type="Meme"
    Max_Maps = len(Meme_Maps)-1
else:
    print("Democracy Needs You! You MUST choose a mission type")

Mission=random.randint(0,Max_Maps)

print("It’s time to equip the most important tools in your arsenal. You have stratagems that are Support Weapons, Offensive, and Defensive. Choose wisely, your choices will have an impact on your mission success, that is also based upon your enemy chosen.")

print("Choose Stratagems\n \tSupport Weapons: \n 1.) Quasar Cannon \n 2.) EAT \n 3.) Recoilless Rifle (no backpack slot) \n 4.) Spear (no backback slot) \n 5.) Machine Gun \n 6.) Grenade Launcher \n 7.) Flamethrower \n 8.) Arc Thrower \n \tOffensive: \n 9.) 500 kg bomb \n 10.) 380mm Barrage \n 11.) Cluster Bomb \n 12.) Strafing Run \n 13.) Eagle Airstrike \n 14.) Rocket Pods \n 15.) Orbital Gatling \n 16.) Orbital Gas Strike \n \tDefensive: \n 17.)\n Gatling Sentry \n 18.) Machine Gun Sentry \n 19.) Rocket Sentry \n 20.) Autocannon Sentry \n 21.) Anti-Tank Emplacement \n 22.) Gas Mines \n 23.) Incendiary Mines \n 24.) Explosive Mines \n 25.) Anti-Tank Mines \n Backpacks: \n 26.) Supply Pack \n 27.) Shield Generator Pack \n 28.) Hellbomb Backpack \n 29.) Ballistic Shield \n 30.) Guard-Dog Regular \n 31.) Guard-Dog Laser \n 32.) Guard-Dog Gas")
Stratagem=0
n=0
All_Stratagems=[]
while n<4:
    # Weapon: [Stratagem type, Weapon, Damage, AP, Explosive, Uses(Ammo or uses before recharge), Cooldown, Aoe, Range, Mag Size, Chain AOE]
    # Offensive: [Stratagem type, Stratagem Name, Damage, AP, Explosive, Uses, Cooldown, Aoe, dps (0 for no dps), dps AP (0 for no dps), dps time(how long does the dps last)] # Dps only for long-term damage (e.g. gas, fire)
    # Defensive: [Stratagem type, Stratagem Name, Damage, AP, Explosive, Uses, Cooldown, Rideable(for emplacements), Range, HP, Armor, Mines(Boolean), mine type (0 for no mines, 1 for gas, 2 for incendiary, 3 for regular, 4 for anti-tank)]
    # Backpacks: [Stratagem type, Stratagem Name, Uses, Cooldown, Guard dog(Boolean, all other values are 0 for no guard dog), Damage, AP, Shots(amount of times the guard dog can shoot before needing to resupply), Recharge time(how many turns before the guard dog can shoot again)]
    # Weapon type key; 1 = weapon; 2 = backpack; 3 = weapon and backpack; 4 = offensive; 5 = defensive
    Chosen_Stratagems = input("")
    if Chosen_Stratagems is 1:
        Stratagem = list(copy.deepcopy(Quasar))
    elif Chosen_Stratagems is 2:
        Stratagem = list(copy.deepcopy(Expendible_Anti_Tank))
    elif Chosen_Stratagems is 3:
        Stratagem = list(copy.deepcopy(Recoilless_Rifle))
    elif Chosen_Stratagems is 4:
        Stratagem = list(copy.deepcopy(Spear))
    elif Chosen_Stratagems is 5:
        Stratagem = list(copy.deepcopy(Machine_gun))
    elif Chosen_Stratagems is 6:
        Stratagem = list(copy.deepcopy(Grenade_Launcher))
    elif Chosen_Stratagems is 7:
        Stratagem = list(copy.deepcopy(Flamethrower))
        if Ship_Mods[3] is 4 :
            Stratagem[2] = 12.5
    elif Chosen_Stratagems is 8:
        Stratagem = list(copy.deepcopy(Arcthrower))
    elif Chosen_Stratagems is 9:
        Stratagem = list(copy.deepcopy(bomb_500kg))
        if Ship_Mods[2] is 3:
            Stratagem[5] = 2
        elif Ship_Mods[2] is 0:
            Stratagem[5] = 1
    elif Chosen_Stratagems is 10:
        Stratagem = list(copy.deepcopy(Barrage_380mm))
    elif Chosen_Stratagems is 33:
        Stratagem = list(copy.deepcopy(Orbital_Precision_Strike))
        if Ship_Mods[3] is 0:
            Stratagem[6] = 2  
    elif Chosen_Stratagems is 11:
        Stratagem = list(copy.deepcopy(Cluster_bomb))
    elif Chosen_Stratagems is 12:
        Stratagem = list(copy.deepcopy(Strafing_run))
    elif Chosen_Stratagems is 13:
        Stratagem = list(copy.deepcopy(Eagle_airstrike))
    elif Chosen_Stratagems is 14:
        Stratagem = list(copy.deepcopy(Rocket_pods))
        
    elif Chosen_Stratagems is 15:
        Stratagem = list(copy.deepcopy(Orbital_Gatling))
        if Ship_Mods[3] is 0:
            Stratagem[6] = 2  
    elif Chosen_Stratagems is 16:
        Stratagem = list(copy.deepcopy(Orbital_Gas))
        if Ship_Mods[3] is 0:
            Stratagem[6] = 2  
    elif Chosen_Stratagems is 17:
        Stratagem = list(copy.deepcopy(Gatling_Sentry))
        if Ship_Mods[4] is 1 or 2 or 3 or 4:
            Stratagem[9] = 100               
    elif Chosen_Stratagems is 18:
        Stratagem = list(copy.deepcopy(Machine_Gun_Sentry))
        if Ship_Mods[4] is 1 or 2 or 3 or 4:
            Stratagem[9] = 100 
    elif Chosen_Stratagems is 19:
        Stratagem = list(copy.deepcopy(Rocket_Sentry))
        if Ship_Mods[4] is 1 or 2 or 3 or 4:
            Stratagem[9] = 100 
    elif Chosen_Stratagems is 20:
        Stratagem = list(copy.deepcopy(Autocannon_Sentry))
        if Ship_Mods[4] is 1 or 2 or 3 or 4:
            Stratagem[9] = 100 
    elif Chosen_Stratagems is 21:
        Stratagem = list(copy.deepcopy(Anti_Tank_Emplacement))
    elif Chosen_Stratagems is 22:
        Stratagem = list(copy.deepcopy(Gas_Mines))
    elif Chosen_Stratagems is 23:
        Stratagem = list(copy.deepcopy(Incendiary_Mines))
    elif Chosen_Stratagems is 24:
        Stratagem = list(copy.deepcopy(Regular_Mines))
    elif Chosen_Stratagems is 25:
        Stratagem = list(copy.deepcopy(Anti_Tank_Mines))
    elif Chosen_Stratagems is 26:
        Stratagem = list(copy.deepcopy(Supply_Pack))
        if Ship_Mods[0] is 0:
            Stratagem[3] = 4 
    elif Chosen_Stratagems is 27:
        Stratagem = list(copy.deepcopy(Shield_Generator_Pack))
        if Ship_Mods[0] is 0:
            Stratagem[3] = 4 
    elif Chosen_Stratagems is 28:
        Stratagem = list(copy.deepcopy(Hellbomb_Backpack))
        if Ship_Mods[0] is 0:
            Stratagem[3] = 4 
    elif Chosen_Stratagems is 29:
        Stratagem = list(copy.deepcopy(Balistic_Shield))
        if Ship_Mods[0] is 0:
            Stratagem[3] = 4 
    elif Chosen_Stratagems is 30:
        Stratagem = list(copy.deepcopy(Guard_Dog))
        if Ship_Mods[0] is 0:
            Stratagem[3] = 4 
    elif Chosen_Stratagems is 31:
        Stratagem = list(copy.deepcopy(Guard_Dog_Rover))
        if Ship_Mods[0] is 0:
            Stratagem[3] = 4 
    elif Chosen_Stratagems is 32:
        Stratagem = list(copy.deepcopy(Guard_Dog_Dog_Breath))
        if Ship_Mods[0] is 0:
            Stratagem[3] = 4 

    All_Stratagems[n]=Stratagem
    n+=1
    