from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


#  Create Black magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 50, 860, "black")
quake = Spell("Quake", 65, 1200, "black")

# Create White Magic
cure = Spell("Cure", 28, 620, "white")
cura = Spell("Cura", 32, 1800, "white")
curaga = Spell("curaga", 50, 6000, "white")

# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-potion", "potion", "Heals for 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15 }, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

# Instantiate People
player1 = Person("Kirito:", 3260, 240, 740, 300, player_spells, player_items)
player2 = Person("Asuna :", 4160, 240, 510, 300, player_spells, player_items)
player3 = Person("Agil  :", 3089, 240, 380, 300, player_spells, player_items)

enemy1 = Person("Valos     ", 4500, 150, 580, 325, enemy_spells, [])           # Lower knight
enemy2 = Person("Heathcliff", 18200, 260, 570, 25, enemy_spells, [])    # High level Boss
enemy3 = Person("Hench     ", 4500, 160, 660, 325, enemy_spells, [])           # Lower Knight

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]


running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS" + bcolors.ENDC)

while running:
    print("===========================================")

    print("\n")
    print("NAME                 HP                                                  MP")
    for player in players:
        player.get_stats()

    print("\n\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, " points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough mp\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), " HP" + bcolors.ENDC)
            elif spell.type == "black":

                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), " points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]
        elif index == 2:
                player.choose_item()
                item_choice = int(input("    Choose item: ")) - 1

                if item_choice == -1:
                    continue

                item = player.items[item_choice]["item"]

                if player.items[item_choice]["quantity"] == 0:
                    print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                    continue
                player.items[item_choice]["quantity"] -= 1

                if item.type == "potion":
                    player.heal(item.prop)
                    print(bcolors.OKGREEN + "\n" + item.name + "heals for", str(item.prop), "HP" + bcolors.ENDC)
                elif item.type == "elixer":

                    if item.name == "MegaElixer":
                        for i in players:
                            i.hp = i.maxhp
                            i.mp = i.maxmp
                    else:
                        player.hp = player.maxhp
                        player.mp = player.maxmp
                        print(bcolors.OKGREEN + "\n" + item.name + " fully restored HP/MP" + bcolors.ENDC)
                elif item.type == "attack":
                    enemy = player.choose_target(enemies)
                    enemies[enemy].take_damage(item.prop)

                    print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), " points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                    if enemies[enemy].get_hp() == 0:
                        print(enemies[enemy].name.replace(" ", "") + " has died.")
                        del enemies[enemy]

    # Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if Player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    # Check if Enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + "The enemies have defeated you." + bcolors.ENDC)
        running = False

    print("\n")
    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # Chose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks" + players[target].name + " for ", enemy_dmg)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()

            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals" + enemy.name + " for", str(magic_dmg), " HP" + bcolors.ENDC)
            elif spell.type == "black":

                target = random.randrange(0, 3)

                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals", str(magic_dmg), " points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    del players[player]

            # print("Enemy chose", spell, "damage is", magic_dmg)