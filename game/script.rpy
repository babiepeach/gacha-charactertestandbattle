
define tana = Character("Tana")
define firebird = Character("Firebird")

default firebirdHPmax = 25000
default firebirdHP = 25000
default firebirdATK = 1500
default firebirdDEF = 180
default firebirdBurstPoints = 0

default enemyBurn = False
default burnTurn = 2

default tanaHPmax = 10101
default tanaHP = 10101
default tanaSP = 1.2
default tanaATK = int(523 * tanaSP)
default tanaDEF = 581
default tanaBurstPoints = 0

init python:
    config.layers = [ 'master', 'transient', 'screens', 'overlay', 'mc' ]

label start:

    scene field_day

    show tana at left onlayer mc with dissolve
    tana "Such a nice day... sure do hope no bosses appear."

    show dragon at truecenter with dissolve

    firebird "The flames will never forget the way you cast me aside, mortal!"

    tana "Oh no! Time to battle!"

    show screen tanaStats
    show screen firebirdStats

    jump firebirdBattle

label firebirdBattle:
    if firebirdHP <0:
        "Firebird died!"
        hide dragon with dissolve
        firebird "Rawrr...."
        jump end
    elif tanaHP <= 0:
        "You died!"
        hide tana onlayer mc with dissolve
        $ line = renpy.random.randint(1,3)
        if line == 1:
            tana "N-No! I can't go out... not like this..."
        elif line == 2:
            tana "Looks like my flame... has died out..."
        else:
            tana "Nng... No... I'm too... young..."
        jump end
    else:
        pass

    "The Boss Firebird is about to attack! What will you do?"
    call screen tanaMoves

return

label turnTanaRUN:
    "You try to run away..."
    "...But it failed!"
    firebird "Trying to run, Mortal? The only thing that can run from the flames is death!"
jump firebirdBattle

label turnTanaNA:
    "You used Normal Attack 'Flame Punch'!"
    $ rana = renpy.random.randint(2,3)
    $ ranb = renpy.random.randint(2,3)
    $ ranc = renpy.random.randint(2,3)
    $ rand = renpy.random.randint(2,5)
    $ tempatka = int(tanaATK * rana / 10)
    $ tempatkb = int(tanaATK * ranb / 10)
    $ tempatkc = int(tanaATK * ranc / 10)
    $ tempatkd = int(tanaATK * rand / 10)
    with vpunch
    centered "[tempatka] + [tempatkb] + [tempatkc] + [tempatkd] damage!"
    $ firebirdHP -= (tempatka + tempatkb + tempatkc + tempatkd)
    jump turnFirebird

label turnTanaQS:
    $ enemyBurn = True
    "You used Quick Skill 'Soul Of Fire'!"
    tana "My souls on FIRE today!"
    $ tanaBurstPoints += 1
    if tanaBurstPoints == 3:
        $ tanaBurstPoints = 3
        $ renpy.notify("Tana's Burst 'Firebird's Devotion' is ready!")
    $ burnTurn = 3
    $ temp = int(tanaATK + (tanaATK * 0.2) - (firebirdDEF * 0.1))
    with vpunch
    centered "[temp] {color=#FF0000}FIRE{/c} damage!"
    $ firebirdHP -= temp
    jump turnFirebird

label turnTanaEB:
    $ enemyBurn = True
    "You used Elemental Burst 'Firebird's Devotion'!"
    $ lines = renpy.random.randint(1,3)
    if lines == 1:
        tana "Your devotion is your greatest WEAKNESS!"
    elif lines == 2:
        tana "Everything relies on the fate of a TRAITOR!"
    else:
        tana "Our devotion stands together!"
    $ tanaBurstPoints = 0
    $ burnTurn = 5
    $ temp = int(tanaATK + 500 + (tanaATK * 0.25) - (firebirdDEF * 0.1))
    with vpunch
    centered "[temp] {color=#FF0000}FIRE{/c} damage!"
    jump turnFirebird

label turnTanaQH:
    "You used 'Quick Heal'!"
    $ temphp = tanaHP
    if tanaHP >= tanaHPmax:
        "...But you're completely healed up, so you gained no health!"
        jump turnFirebird
    else:
        $ tanaHP += 1000
        if tanaHP >= tanaHPmax:
            $ tanaHP = tanaHPmax
        "...And you healed up!"
    jump turnFirebird



label turnFirebird:
    if enemyBurn:
        $ firebirdHP -= 500
        $ burnTurn -= 1
        with vpunch
        "Firebird was burned for 500 damage!"
        if burnTurn == 0:
            "...But the burn wore off!"
            $ burnTurn = 2
            $ enemyBurn = False
    $ temp = renpy.random.randint(1,7)
    if firebirdBurstPoints == 5:
        "Firebird used Normal Attack 'Volcanic Fury'!"
        firebird "Your devotion to the art of fire is WEAK!"
        $ dmg = int(firebirdATK - (firebirdDEF * 0.7) + (firebirdHPmax * 0.05) - tanaDEF)
        with vpunch
        centered "[dmg] damage!"
        $ tanaHP -= dmg
        $ firebirdBurstPoints = 0
    elif temp == 1 or temp == 2 or temp == 3 or temp == 4:
        "Firebird used Quick Skill 'Claw Strike'!"
        $ dmg = int(firebirdATK - (firebirdDEF /  0.8) - tanaDEF)
        with vpunch
        centered "[dmg] damage!"
        $ tanaHP -= dmg
    elif temp == 5 or temp == 6 or temp == 7:
        "Firebird used Elemental Burst 'Blaze Within'!"
        firebird "The fire which bore by me will never forgive you!"
        $ dmg = int((firebirdATK * 0.5) + (firebirdHPmax * 0.05) - tanaDEF)
        with vpunch
        centered "[dmg] damage!"
        $ tanaHP -= dmg
        $ firebirdBurstPoints += 1
        if firebirdBurstPoints == 5:
            $ firebirdBurstPoints = 5
            $ renpy.notify("Firebird's burst 'Volcanic Fury' is ready!")
    else:
        "broke"
    jump firebirdBattle

label end:
    hide dragon
    hide tana onlayer mc
    hide screen tanastats
    hide screen firebirdstats
    with fade
    "Looks like everything is finished now."
    "You can go back and test other things if you'd like, or you can provide feedback here."
    "Now, if you wanna restart, hit 'main menu' and click 'start'."
return

##########################################################
##################   screen   ############################
##########################################################

screen tanaMoves:
    frame:
        xalign 0.5
        yalign 0.95
        hbox:
            null width 30
            null height 10
            vbox:
                imagebutton auto "tanaNA_%s.png":
                    xalign 0.5
                    action [ Hide("tanaMoves"), Jump("turnTanaNA") ]
                text "Normal Attack":
                    xalign 0.5
            null width 20
            vbox:
                imagebutton auto "tanaQS_%s.png":
                    xalign 0.5
                    action [ Hide("tanaMoves"), Jump("turnTanaQS") ]
                text "Quick Skill":
                    xalign 0.5
            null width 20
            if tanaBurstPoints == 3:
                vbox:
                    imagebutton auto "tanaEB_%s.png":
                        xalign 0.5
                        action [ Hide("tanaMoves"), Jump("turnTanaEB") ]
                    text "Elemental Burst":
                        xalign 0.5
                null width 20
            vbox:
                imagebutton auto "tanaQH_%s.png":
                    xalign 0.5
                    action [ Hide("tanaMoves"), Jump("turnTanaQH") ]
                text "Quick Heal":
                    xalign 0.5
            null width 20
            vbox:
                imagebutton auto "tanaRUN_%s.png":
                    xalign 0.5
                    action [ Hide("tanaMoves"), Jump("turnTanaRUN") ]
                text "Run":
                    xalign 0.5
            null width 30

screen tanaStats:
    frame:
        xalign 0.05
        yalign 0.6
        vbox:
            label "Tana Health:":
                text_bold True
                xalign 0.5
            text "[tanaHP] / [tanaHPmax]":
                xalign 0.5

screen firebirdStats:
    frame:
        xalign 0.9
        yalign 0.1
        vbox:
            label "Firebird Health:":
                text_bold True
                xalign 0.5
            text "[firebirdHP] / [firebirdHPmax]":
                xalign 0.5
            if enemyBurn:
                text "On fire!":
                    xalign 0.5
                    bold True
                text "-500 HP for 2-5x turns":
                    xalign 0.5
