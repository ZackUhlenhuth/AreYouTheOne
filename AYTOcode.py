import itertools
import pickle
#---------------------
# Are You The One? Code
# Calculates the likelihoods of each couple being a perfect match (assuming all matches are equally likely)
# Each week, update the weeks choices and number of matches (as well as the allWeeks list!).
# Each week, update the truth booth information
#--------------------


# Specifies whether the matches should be loaded from the match file
# For the first time you run, make sure this is set to False.
# Then you can change it to False in order to run faster.
load_from_file = False

# guys and girls in alphabetical order
guys = ["Asaf", "Cam", "Cameron", "Giovanni", "John", "Morgan", "Prosper", "Sam", "Stephen", "Tyler"]
girls = ["Alyssa", "Camille", "Emma", "Francesca", "Julia", "Kaylen", "Mikala", "Nicole", "Tori", "Victoria"]

# (guesses, number of matches)
# Corresponds to the guys list. ie: in week1, "Stacey" was therfore with "Alec"
week1 = (["Francesca", "Victoria", "Mikala", "Kaylen", "Emma", "Juia", "Camille", "Alyssa", "Nicole", "Tori"], 3)


#UPDATE THIS EVERY WEEK
# list of every weeks guesses
allWeeks = [week1]

# the matches that got denied in the truth booth
truthBooth_denied = [("Prosper", "Tori")]

# the matches that were confirmed in the truth booth
truthBooth_confirmed = []

# returns the number of matches in common between two match lists
def correlation(list1, list2):
    total = 0
    for i in range(len(list1)):
        if list1[i] == list2[i]:
            total = total + 1
    return total

# returns whether a matchlist breaks a rule
def isImpossible(matchlist):
    for match in truthBooth_denied:
        if (matchlist[guys.index(match[0])] == match[1]):
            return True
    for match in truthBooth_confirmed:
        if (matchlist[guys.index(match[0])] != match[1]):
            return True
    for week in allWeeks:
        if correlation(matchlist, week[0]) != week[1]:
            return True        
    return False           

#list of possible matches
possible = []

if load_from_file: #load matches if previously stored
    iterable = pickle.load( open("allmatches.p", "rb") )
else: #generate all possible matches
    iterable = itertools.permutations(girls,len(girls))
for matching in iterable:
    # skip match lists that break a rule
    if isImpossible(matching):
        continue
    else:
        possible.append(matching)
        
print("There are " + str(len(possible)) + " possible matchings!")




# initialize dictionary
match_dictionary = {}
for guy in guys:
    match_dictionary[guy] = [0] * len(girls)
print("done with dict init")

# fill in dictionary
for matching in possible:
    for guy in guys:
        match_dictionary[guy][girls.index(matching[guys.index(guy)])] += float(1)/len(possible)
print("done with dict fill")

#determine best matching
def determineBestMatching():
    best_match_score = 0
    best_matching = []
    for matching in possible:
        score = 0
        for guy in guys:
            score += match_dictionary[guy][girls.index(matching[guys.index(guy)])]
        #print("score " + str(score))
        if score > best_match_score:
            best_match_score = score
            best_matching = matching
    print("Best score " + str(best_match_score))

    best_string = ""
    for i in range(len(best_matching)):
        best_string += '''||style="background:#CFCFCF"|''' + """'''"""+ guys[i] + ", " +best_matching[i]+"""'''"""

def printBestMatching():
    determineBestMatching()
    print('''{| class="wikitable"''')
    print("|-")
    print(best_string[1:])
    print("""|}""")

# prints the percent of possible matchings that contain each couple
def printAll():
    for key in sorted(match_dictionary.keys()):
        print(key.upper())
        matchPercents = ""
        for i in range(len(match_dictionary[key])):
            matchPercents += " " + str(girls[i]) + " " + "%.1f%%" % (100*match_dictionary[key][i])
        print(matchPercents)

#prints the top match for each guy
def printMaxGuys():
    for key in sorted(match_dictionary.keys()):
        print(key.upper())
        matchPercents = ""
        maxPercent = 0
        maxIndex = 0
        for i in range(len(match_dictionary[key])):
            percent = match_dictionary[key][i]
            if percent > maxPercent:
                maxPercent = percent
                maxIndex = i
        
        matchPercents += " " + str(girls[maxIndex]) + " " + "%.1f%%" % (100*match_dictionary[key][maxIndex])
        print(matchPercents)

#prints the top match for each girl
def printMaxGirls():
    for i in range(len(guys)):
        print(girls[i].upper())
        maxPercent = 0
        maxIndex = 0
        matchPercents = ""
        for key in sorted(match_dictionary.keys()):
            percent = match_dictionary[key][i]
            if percent > maxPercent:
                maxPercent = percent
                maxIndex = key

        matchPercents += " " + str(maxIndex) + " " + "%.1f%%" % (100*match_dictionary[maxIndex][i])
        print(matchPercents)


# prints the table in wikitable format
def printTable():
    #Key/table colors
    colorKey = "#CFCFCF"
    color0 = "#F9F9F9" # 0
    color1 = "#FF9999" # 0->9
    color2 = "#FF6666" # 10->24
    color3 = "#FF3333" # 24->49
    color4 = "#E60000" # 50->74
    color5 = "#990000" # 75-99
    color6 = "#00CC00" # 100
    colWidth = "60px" #specifies the width of each column in the table
    
    #print key
    print('{| class="wikitable"')
    print('|-')
    print("""| style="background:"""+colorKey+""""|'''Key'''||style="background:"""+color0+""""|'''0%'''|| style="background:"""+color1+""""|'''0-9%'''|| style="background:"""+color2+""""|'''10-24%'''|| style="background:"""+color3+""""|'''25-49%'''|| style="background:"""+color4+""""|'''50-74%'''||style="background:"""+color5+""""|'''75-99%'''||style="background:"""+color6+""""|'''100%'''
|}""")
    
    print('{| class="wikitable" style="text-align:right"')
    print("|-")
    #table header
    print('! !! style="width:'+ colWidth+ '"|Alyssa !! style="width:'+colWidth+'"|Camille !! style="width:'+colWidth+'"|Emma !! style="width:'+colWidth+'"|Francesca !! style="width:'+colWidth+'"|Julia !! style="width:'+colWidth+'"|Kaylen !! style="width:'+colWidth+'"|Mikala !! style="width:'+colWidth+'"|Nicole !! style="width:'+colWidth+'"|Tori !! style="width:'+colWidth+'"|Victoria')
    # table cells
    for key in sorted(match_dictionary.keys()):
        print("|-")
        matchPercents = "| <b>" + str(key) + "</b>"
        for i in range(len(match_dictionary[key])):
            if int(round(100*match_dictionary[key][i])) == 0:
                matchPercents += '||style="background:' + color0 +'"| <b>' + "%.0f%%" % (100*match_dictionary[key][i]) + "</b>"
            elif 10 > int(round(100*match_dictionary[key][i])) > 0:
                matchPercents += '||style="background:' + color1 + '"| <b>' + "%.0f%%" % (100*match_dictionary[key][i]) + "</b>"
            elif 25 > int(round(100*match_dictionary[key][i])) >= 10:
                matchPercents += '||style="background:' + color2 + '"| <b>' + "%.0f%%" % (100*match_dictionary[key][i]) + "</b>"
            elif 50 > int(round(100*match_dictionary[key][i])) >= 25:
                matchPercents += '||style="background:' + color3 + '"| <b>' + "%.0f%%" % (100*match_dictionary[key][i]) + "</b>"
            elif 75 > int(round(100*match_dictionary[key][i])) >= 50:
                matchPercents += '||style="background:' + color4 + '"| <b>' + "%.0f%%" % (100*match_dictionary[key][i]) + "</b>"
            elif 100> int(round(100*match_dictionary[key][i])) >= 75:
                matchPercents += '||style="background:' + color5 + '"| <b>' + "%.0f%%" % (100*match_dictionary[key][i]) + "</b>"
            elif int(round(100*match_dictionary[key][i])) == 100:
                matchPercents += '||style="background:' + color6 + '"| <b>' + "%.0f%%" % (100*match_dictionary[key][i]) + "</b>"
            else:
                matchPercents += "|| " + "%.0f%%" % (100*match_dictionary[key][i])
        print(matchPercents)
    print("|}")

printTable()


#if not load_from_file: #save matches into a file
#    pickle.dump(possible, open("allmatches.p", "wb"))


