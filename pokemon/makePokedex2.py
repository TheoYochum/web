#pastethe output (or pipe the output) of this program to the pokedex.html file.
with open('pokemon.csv','r') as file:
    data = file.read().strip().split('\n')

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
    data[i][11][0] = '' #Sets the text of the genreation column to empty
    data[i].insert(0, ['<img src="img/front/' + data[i][0][0] +'.png" alt="Image of ' + data[i][1][0] + '">', 'image']) #Adds an image to the list with an image class
    data[i].pop(13) #Removes the Legendary attribute after its value is appended to the name so it can be later applied to the table row
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



#The styling so it can be written to a css file 
style = '''/*Basic page formatting*/
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
    width: auto;
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

/* Navbar */

nav li {
    display: inline-block;
    position: relative;
    padding-right: 10px;
    padding-left: 10px;
}

nav li ul {
    display: none;
    position: absolute;
    width: 450px;
    top: 100%;
    padding: 0;
    padding-top: 5px;
    background-color: white;
    margin-left: -225px;
    left: 50%;
}

nav li ul li {
    padding-left: 0;
    padding-right: 0;
    border: solid 1px black;
    width: 140px;
    margin-bottom: 5px;
}

nav li:hover > ul {
    display: block;
}

a {
    padding-left: 5px;
    padding-right: 5px;
    text-align: center;
    text-decoration: none;
    color: blue;
}

a:visited {
    color: blue;
}

a.active {
    color: black;
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
}'''

#Style sources:
#https://www.epidemicjohto.com/t882-type-colors-hex-colors
#https://wordpress.org/support/topic/centering-dropdown-menu/
#https://stackoverflow.com/questions/10710801/css-dropdown-menu-with-horizontal-submenu
#https://stackoverflow.com/questions/5054415/fill-div-with-2-colors
#https://graphicdesign.stackexchange.com/questions/6368/looking-for-a-good-video-game-retro-pixel-like-web-safe-font

#Writes a css file of all the sitewide styling
# css = open('pokestyle.css', 'w')
# css.write(style)
# css.close()

#Writes the typelist
typelist = []
for pokemon in data[1:]:
    if not pokemon[3][0] in typelist:
        typelist.append(pokemon[3][0])
    if not pokemon[4][0] in typelist:
        typelist.append(pokemon[4][0])
typelist.remove('None')

#Stores the navbar code in a vairable so it can be universally assigned
def navbar(pageType):
    navbar = '''
        <nav>
            <ul>\n'''
    if pageType == 'homepage':
        navbar += '                <li><a href="homepage.html" class="active">Homepage</a></li>\n'
    else:
        navbar += '                <li><a href="homepage.html">Homepage</a></li>\n'
    if pageType in typelist:
        navbar += '''                <li><a class="active">Types</a>
                    <ul>
'''
    else:
        navbar +=  '''                <li><a>Types</a>
                    <ul>
'''
    for value in typelist:
        if pageType == value:
            navbar += '                        <li><a href="' + value + '.html" class="active">' + value + '</a></li>\n'
        else:
            navbar += '                        <li><a href="' + value + '.html">' + value + '</a></li>'
    navbar += '''                    </ul>
                </li>'''
    if pageType == 'all':
        navbar += '                <li><a href="allpokemon.html" class="active">All Pokemon</a></li>\n'
    else:
        navbar += '                <li><a href="allpokemon.html">All Pokemon</a></li>\n'
    if pageType == 'extremes':
        navbar += '                <li><a href="extremes.html" class="active">The Extremes</a></li>\n'
    else:
        navbar += '                <li><a href="extremes.html">The Extremes</a></li>\n'
    navbar += '''            </ul>
        </nav>'''
    return navbar

#A function that creates an HTML file containing all the pokemon entries matching the passed pokemon type
def makeTypePageFile(type, dataList):
    reduced = [dataList[0]]
    for pokemon in dataList:
        if pokemon[3][0] == type or pokemon[4][0] == type:
            reduced.append(pokemon)
    output = '''<!DOCTYPE HTML>
<html>
''' + '''    <head>
        <title> ''' + type + ''' Pokemon </title>
        <link rel="stylesheet" href="pokestyle.css">
    </head>
    <body>''' + navbar(type) + '''
        <h1> ''' + type + ''' Types </h1>
        <p>All of the pokemon of the ''' + str(type) + ''' type</p>
''' + makeHTMLTable(reduced) + '''
    </body>
</html>'''
    filename = type + '.html'
    fileout = open(filename, 'w')
    fileout.write(output)
    fileout.close()

#Makes the homepage

homeData = data[:2] + [data[25]]
homeTable = makeHTMLTable(homeData)

home = '''<!DOCTYPE HTML>
<html>
''' + '''    <head>
        <title> All Pokemon </title>
        <link rel="stylesheet" href="pokestyle.css">
    </head>
    <body>''' + navbar('homepage') + '''
        <h1>The Pokedex</h1>
        <h2>By Theodore Yochum</h2>
        <p>As a kid I had the standard amount of exposure to pokemon, I watched the original anime and dabled in the card game, but I never played any of the games that were in the original format and only dabled in a Wii game as a kid, the tutorial of which I never figured out how to finish. From my exposure I would say that my favorite pokemon has to be bulbasaur because he is adorable, with pikachu obviously as the runner up. This project seemed like it would offer a lot of creativity for how to approach it due to the sheer amount of data and corresponding styling. Pokemon is a very colorful game and they have already designed a color scheme for you, which allows you to make a really interesting and colorful table with minimal effort.</p> ''' + homeTable 

homepage = open('homepage.html', 'w')
homepage.write(home)
homepage.close()

#Makes a webpage of all the pokemon
pokedex = makeHTMLTable(data)
full = '''<!DOCTYPE HTML>
<html>
''' + '''    <head>
        <title> All Pokemon </title>
        <link rel="stylesheet" href="pokestyle.css">
    </head>
    <body> ''' + navbar('all') + '''
        <h1>All of the pokemon</h1>
        <p>This is a list of all of the pokemon in the first generation, the entire webpage is using a replica gameboy font from <a href="https://graphicdesign.stackexchange.com/questions/6368/looking-for-a-good-video-game-retro-pixel-like-web-safe-font"> here</a>. Each Pokemon is listed with its number, its name, and its primary and secondary type with the type backgrounds colored according to <a href="https://www.epidemicjohto.com/t882-type-colors-hex-colors"> this website </a>. Each attribute of the pokemon is colored on a gradient from 0 to 1 with 1 being the highest value, for example chansey with 250 health, and 0 being the lowest, diglet with 10 health. There is a linear scale on the gradients and the coloring is done on a 20% interval with the colors getting darker as the value gets higher, the colors were chosen by whatever made sense to me and I eyeballed a gradient that seemed to get progressively darker while retaining the core color. The generation entry of the original data set is replaced by a game version entry with the table cell containing the color of each version of generation 1 the pokemon appeared in, red blue and yellow according to <a href="https://www.ign.com/wikis/pokemon-red-blue-yellow-version/Pokemon_Red,_Blue,_and_Yellow_Version_Differences">this website</a>, for exapmple ekans only appeared in pokemon red, while sandshrew appeared in blue and yellow. The legendary entry has been removed entirely as it was false for the vast majority and has been replaced by a gold border on any legendary pokemon. All of these stylings are consistent between type pages.</p>''' + pokedex + '''
    </body>
</html>'''

allpokemon = open('allpokemon.html', 'w')
allpokemon.write(full)
allpokemon.close()

#Makes a webpage of the pokemon with the highest and lowest stats in each category
#Sets up and adds to a list every index of the pokemon with the highest and lowest stands of each category
extremes = []
for i in range(1, len(data[1:])):
    if hp_min == int(data[i][5][0]):
        extremes.append(i)
    if hp_max == int(data[i][5][0]):
        extremes.append(i)

for i in range(1, len(data[1:])):
    if atk_min == int(data[i][6][0]):
        extremes.append(i)
    if atk_max == int(data[i][6][0]):
        extremes.append(i)

for i in range(1, len(data[1:])):
    if def_min == int(data[i][7][0]):
        extremes.append(i)
    if def_max == int(data[i][7][0]):
        extremes.append(i)

for i in range(1, len(data[1:])):
    if spa_min == int(data[i][8][0]):
        extremes.append(i)
    if spa_max == int(data[i][8][0]):
        extremes.append(i)

for i in range(1, len(data[1:])):
    if spd_min == int(data[i][9][0]):
        extremes.append(i)
    if spd_max == int(data[i][9][0]):
        extremes.append(i)

for i in range(1, len(data[1:])):
    if spe_min == int(data[i][10][0]):
        extremes.append(i)
    if spe_max == int(data[i][10][0]):
        extremes.append(i)

#Sorts the list and removes any repeating entries
extremes.sort()
sortedExtremes = extremes + []
extremes = []
for i in sortedExtremes:
    if not i in extremes:
        extremes.append(i)

#Turns the extremes data into a table
extremesData = [data[0]]
for i in extremes:
    extremesData.append(data[i])
extremesTable = makeHTMLTable(extremesData)

extremesHTML = '''<!DOCTYPE HTML>
<html>
''' + '''    <head>
        <title>The Extremes</title>
        <link rel="stylesheet" href="pokestyle.css">
    </head>
    <body> ''' + navbar('extremes') + '''
        <h1>The Extremes</h1>
        <p>This is a list containing all pokemon with the maximum and minimum values for each stat. While I intended to make a top 10 and simply omit speed, the assumption that each stat would have a single lowest and highest and that each pokemon would only appear once was proven false. Someone at Nintendo had the bright idea of making Chansey have both the maximum health, but also the minimum attack and defense. Also Magikarp has the lowest Sp. Atk and Sp. Def because Magikarp, as well as being tied with caterpie and weedle for the lowest Sp. Def. I decided that reaching an even 10 would be impossible so I also added speed and changed it to a table of the extremes, each pokemon appears only once.</p> ''' + extremesTable + '''
    </body>
</html>'''

theExtremes = open('extremes.html', 'w')
theExtremes.write(extremesHTML)
theExtremes.close()

#Creates a webpage corresponding to each element of typeList
for type in typelist:
    makeTypePageFile(type,data)