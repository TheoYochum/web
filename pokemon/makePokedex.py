#paste the output (or pipe the output) of this program to the pokedex.html file.
with open('pokemon.csv','r') as file:
    data = file.read().strip().split('\n')

i = 0
for i in range(len(data)):
    data[i] = data[i].split(',') #Splits on newline

for i in range(len(data)):
    for ii in range(len(data[i])):
        data[i][ii] = [data[i][ii]] #Converts every string into a list of strings so a class can be appended

#All of these create a list containing all of the values of the pokemon and then store the highest and lowest of the values
health = []
for i in data[1:]:
    health.append(int(i[5][0]))
hp_min = min(health)
hp_max = max(health)

attack = []
for i in data[1:]:
    attack.append(int(i[6][0]))
atk_min = min(attack)
atk_max = max(attack)

defense = []
for i in data[1:]:
    defense.append(int(i[7][0]))
def_min = min(defense)
def_max = max(defense)

spatk = []
for i in data[1:]:
    spatk.append(int(i[8][0]))
spa_min = min(spatk)
spa_max = max(spatk)

spdef = []
for i in data[1:]:
    spdef.append(int(i[9][0]))
spd_min = min(spdef)
spd_max = max(spdef)

speed = []
for i in data[1:]:
    speed.append(int(i[10][0]))
spe_min = min(speed)
spe_max = max(speed)

#This is a function that when given an attribute of a pokemon, the index of that attribute in a list, and the variable
#corresponding to the maximum and minimum valuse of that attribute it will convert the number to a number between 0 and 1 with
#1 being associated with the highest health value and zero the lowest and then return a string with the name of that variable and
#a number between 0 and 4 inclusive that indicates what percentile it is in
def gradient(attribute, index, min, max): 
    if ((int(data[i][index][0]) - min) / max) < 0.2:
        return (attribute + '0')
    elif ((int(data[i][index][0]) - min) / max) < 0.4:
        return (attribute + '1')
    elif ((int(data[i][index][0]) - min) / max) < 0.6:
        return (attribute + '2')
    elif ((int(data[i][index][0]) - min) / max) < 0.8:
        return (attribute + '3')
    else:
        return (attribute + '4')

#These lists are manually written and contain the name of each pokemon that is not present in that version of the game but is in the pokedex
#Source:https://www.ign.com/wikis/pokemon-red-blue-yellow-version/Pokemon_Red,_Blue,_and_Yellow_Version_Differences
notinred = ['Sandshrew', 'Sandslash', 'Vulpix', 'Ninetales', 'Meowth', 'Persian', 'Bellsprout', 'Weepinbell', 'Victreebel', 'Magmar', 'Pinsir']
notinblue = ['Ekans', 'Arbok', 'Oddish', 'Gloom', 'Vileplume', 'Mankey', 'Primeape', 'Growlithe', 'Arcanine', 'Scyther', 'Electabuzz']
notinyellow = ['Weedle', 'Kakuna', 'Beedrill', 'Ekans', 'Arbok', 'Raichu', 'Meowth', 'Persian', 'Koffing', 'Weezing', 'Jynx', 'Electabuzz', 'Magmar']

#This function takes the name of a pokemon and returns the string 'gen' plus the first letters of each version of pokemon it is present in
def generation(name):
    out = 'gen'
    if not name in notinred:
        out += 'r'
    if not name in notinblue:
        out += 'b'
    if not name in notinyellow:
        out += 'y'
    return out
        
#Appends the class of each data point so that they can have targetted css applied, some are basic like the number as they will have a unifrom styling
#and others use the functions defined earlier to assign a variety of classes based on the individual pokemon allowing for targetted styling
for i in range(1, len(data)):
    data[i][0].append('pokemon number')
    data[i][1].append(data[i][12][0])
    data[i][2].append(data[i][2][0].lower())
    if data[i][3][0] == '':
        data[i][3][0] = 'None'
    data[i][3].append(data[i][3][0].lower())
    data[i][5].append(gradient('health', 5, hp_min, hp_max))
    data[i][6].append(gradient('attack', 6, atk_min, atk_max))
    data[i][7].append(gradient('defense', 7, def_min, def_max))
    data[i][8].append(gradient('spatk', 8, spa_min, spa_max))
    data[i][9].append(gradient('spdef', 9, spd_min, spd_max))
    data[i][10].append(gradient('speed', 10, spe_min, spe_max))
    data[i][11].append(generation(data[i][1][0]))
    data[i][11][0] = ''
    data[i].pop(12)
    data[i].insert(0, ['<img src="img/front/' + data[i][0][0] +'.png" alt="Image of ' + data[i][1][0] + '">', 'image']) #Adds an image to the list with an image class
    data[i].pop(5) #Removes the total attribute
    
#Modifies the header of the table and adds a class as it would be difficult to put them in proper header tags
for i in range(len(data[0])):
    data[0][i].append('header')
data[0].insert(0, ['Image', 'header'])
data[0].pop(5)
data[0][11][0] = 'Game Version'
data[0].pop(12)

#Fairly standard function that creates a table from a 2d list, although this list is technically
#"3d" with the first element of the final list being the content and the second being the class
def makeHTMLTable(input):
    out = '''        <table>
'''
    for list in input:
        temp = '''            <tr ''' + 'class="' + list[2][1].lower() + '"' +  '''>
'''
        for value in list:
            temp += '''                <td ''' + ' class="' + str(value[1]) + '''">''' + str(value[0]) + '''</td>
'''
        temp += '''            </tr>
'''
        out += temp
    out += '''        </table>'''
    return out

pokedex = makeHTMLTable(data)

site = '''<!DOCTYPE HTML>
<html>
''' + '''    <head>
        <title> The Pokedex Theo Yochum </title>
        <style>
        /*Basic page formatting*/
            @font-face {
                font-family: pokedex;
                src: url(https://theoyochum.github.io/web/gameboy.ttf);
            }

            body {
                text-align: center;
                padding-left: 5%;
                padding-right: 5%;
                padding-top: 2%;
                padding-bottom: 2%;
                font-family: pokedex;
            }

            table {
                border-collapse: collapse;
                margin-left: auto;
                margin-right: auto;
                border-bottom: solid 5px;
            }

            tr {
                border: solid 5px;
                border-bottom: none;
            }

            td {
                border-right: solid 1px;
                padding-left: 5px;
                padding-right: 5px;
            }

            td.header{
                padding-left: 10px;
                padding-right: 10px;
                padding-top: 5px;
                padding-bottom: 5px;
            }
            /* Attribute coloring */
            .health0 {
                background-color: #4de042;
            }

            .health1 {
                background-color: #44B73D;
            }

            .health2 {
                background-color: #3D9C36;
            }

            .health3 {
                background-color: #33822E;
            }

            .health4 {
                background-color: #19692d;
            }

            .attack0 {
                background-color: #ff1b1b;
            }

            .attack1 {
                background-color: #c91b1b;
            }

            .attack2 {
                background-color: #991919;
            }

            .attack3 {
                background-color: #9e1b1b;
            }

            .attack4 {
                background-color: #8b1818;
            }

            .defense0 {
                background-color: #1f1bff;
            }

            .defense1 {
                background-color: #391ecf;
            }

            .defense2 {
                background-color: #1f29b8;
            }

            .defense3 {
                background-color: #1d1f99;
            }

            .defense4 {
                background-color: #0d0f5e;
            }

            .spatk0 {
                background-color: #ff8119;
            }

            .spatk1 {
                background-color: #c9611b;
            }

            .spatk2 {
                background-color: #9e5816;
            }

            .spatk3 {
                background-color: #964b0e;
            }

            .spatk4 {
                background-color: #80380f;
            }

            .spdef0 {
                background-color: #19abff;
            }

            .spdef1 {
                background-color: #1ba6c9;
            }

            .spdef2 {
                background-color: #168c94;
            }

            .spdef3 {
                background-color: #0c5b74;
            }

            .spdef4 {
                background-color: #0f4d77;
            }

            .speed0 {
                background-color: #f8f8f8;
            }

            .speed1 {
                background-color: #c5c5c5;
            }

            .speed2 {
                background-color: #979797;
            }

            .speed3 {
                background-color: #727272;
            }

            .speed4 {
                background-color: #585858;
            }

            .genrby {
                background: linear-gradient(to right, #ff1111 0%, #ff1111 33%, #1111ff 34%, #1111ff 67%, #ffd733 68%, #ffd733 100%);
            }

            .genrb {
                background: linear-gradient(to right, #ff1111 0%, #ff1111 50%, #1111ff 50.1%, #1111ff 100%);
            }

            .genry {
                background: linear-gradient(to right, #ff1111 0%, #ff1111 50%, #ffd733 50.1%, #ffd733 100%);
            }

            .genby {
                background: linear-gradient(to right, #1111ff 0%, #1111ff 50%, #ffd733 50.1%, #ffd733 100%);
            }

            .genr {
                background-color: #ff1111;
            }

            .genb {
                background-color: #1111ff;
            }

            .geny {
                background-color: #ffd733;
            }
            
            .normal {
                background-color: #A8A77A;
            }

            .fire {
                background-color: #EE8130;
            }

            .water {
                background-color: #6390F0;
            }

            .electric {
                background-color: #F7D02C;
            }

            .grass {
                background-color: #7AC74C;
            }

            .ice {
                background-color: #96D9D6;
            }

            .fighting {
                background-color: #C22E28;
            }

            .poison {
                background-color: #A33EA1;
            }

            .ground {
                background-color: #E2BF65;
            }

            .flying {
                background-color: #A98FF3;
            }

            .psychic {
                background-color: #F95587;
            }

            .bug {
                background-color: #A6B91A;
            }

            .rock {
                background-color: #B6A136;
            }

            .ghost {
                background-color: #735797;
            }

            .dragon {
                background-color: #6F35FC;
            }

            .steel{
                background-color: #B7B7CE;
            }

            .fairy {
                background-color: #D685AD;
            }

            .none {
                background-color: grey;
            }

            tr.true {
                border-color: gold;
                border-bottom: solid gold 5px ;
            }

        </style>
    </head>
    <body>
        <h1>The Pokedex</h1>
        <h2>By Theodore Yochum</h2>
        <p>I have always enjoyed pokemon and as a kid the anime was one of my favorite things to watch, and one of my moms least favorite due to the fact that the pokemon constantly shout their own name over and over. I was never super into the games but they always looked fun. If I had to choose a favorite Gen 1 pokemon it would probably be Bulbasaur with pikachu coming in close second because of course. This project seemed like it would be pretty cool because you are given a lot of different numbers you can mess around with, and most of them have associated colors allowing you to do some pretty fun stuff with the styling. For this project I, made it so that the pokemon types are colored according to the original values, each attribute with a numerical value is colored on a gradient at 20% intervals with the lowest value being the lightest color and the highest being the darkest color, also each entry has a game version column which is colored corresponding to which version of pokemon it appeared in. The few pokemon that have gold colored borders are legendaries. The entire website uses a font that is inteded to replicate the original gameboy font.</p>
''' + pokedex + '''
    </body>
 </html>'''

print(site)

#Style sources:
#https://www.epidemicjohto.com/t882-type-colors-hex-colors
#https://www.schemecolor.com/pokemon-colors.php
#https://stackoverflow.com/questions/31195985/two-color-table-cell-background


