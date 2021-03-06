from datetime import datetime
import re

file = "ratebeer100000.txt"

#beer_options = {"name" : 10, "beerId" : 12 , "brewerId": 14, "ABV" : 9, "style" : 11}
#review_options = {"appearance" : 18, "aroma": 13, "palate" : 14, "taste" : 13, "overall" : 15, "time" : 12, "profileName" : 19, "text" : 12}
#json_template = '{"beer": {"name": {name}, "beerId": {ID}, "brewerId": {2}, "ABV": {3}, "style": "{4}"}, "review": {"appearance": "{5}", "aroma": "{6}", "palate": "{7}", "taste": "{8}", "overall": "{9}", "time": {10}, "profileName": "{11}", "text": "{12}"}}'

beer_poz = [11, 13, 15, 10, 12, 19, 14, 15, 14, 16, 13, 20, 13]  # od którego indeksu kopiujemy tekst
beerVal = []  # lista do magazynowania jednej recenzji
beerID = []  # lista gdzie wrzucamy wszystkie BeerID

newfile = "ratebeer.json"  # nazwa pliku do którego zapisujemy dane zamienione na JSON
newBeerIDfile = "beerID.txt"  # nazwa pliku do którego zapisujemy BeerID
output = open(newfile, 'w')
output2 = open(newBeerIDfile, 'w')

with open(file, "r", encoding="utf-8", errors='ignore') as rb_raw:
    output.write("[\n")
    i = 0
    a = 0
    b = 1  # numer ID ktory dodajemy do każdej recenzji
    for line in rb_raw:

        #zamiana na nawiasy
        line = line.replace('&#40;', '(')
        line = line.replace('&#41;', ')')

        if i == 13:  # jedna pełna recenzja ma 13 wierszy i 14 jest pusty, kiedy dojdziemy do 14 zapisujemy do pliku i zerujemy indeks
            # print(beerVal)

            text12 = beerVal[12]
            newText12 = text12.replace('"', '\\"')

            # usuniecie białych znaków i innych śmieci z którymi json ma problem z recenzji
            newText12 = re.sub('[^A-Za-z0-9.?!,$%\(\)-]+', ' ', newText12)

            # zamiana na Null
            if beerVal[3] == '-':
                beerVal[3] = 'null'

            # zamiania ocen w postaci stringow (np. 5/20) o różnym mianowniku na ogólnoą wartość procentową
            x, y = beerVal[5].split("/")
            appearance_val = int(x) / int(y)
            beerVal[5] = str(appearance_val)

            x, y = beerVal[6].split("/")
            aroma_val = int(x) / int(y)
            beerVal[6] = str(aroma_val)

            x, y = beerVal[7].split("/")
            palate_val = int(x) / int(y)
            beerVal[7] = str(palate_val)

            x, y = beerVal[8].split("/")
            taste_val = int(x) / int(y)
            beerVal[8] = str(taste_val)

            x, y = beerVal[9].split("/")
            overall_val = int(x) / int(y)
            beerVal[9] = str(overall_val)

            # zamiana timestamp na datę
            timestamp = int(beerVal[10])
            dt_object = datetime.fromtimestamp(timestamp)
            beerVal[10] = str(dt_object.date())




            if b != 1:
                JSONline = '\n{"beer name":' + '"' + beerVal[0] + '"' + ', "beerId":' + beerVal[1] + ', "brewerId":' + \
                           beerVal[2] + \
                           ', "ABV":' + beerVal[3] + ', "style":"' + beerVal[4] + '", "appearance":' + \
                           beerVal[5] + ', "aroma": ' + beerVal[6] + ', "palate":' + beerVal[7] + ', "taste":' + \
                           beerVal[8] + \
                           ', "overall":' + beerVal[9] + ', "time":"' + beerVal[10] + '", "profileName":"' + beerVal[
                               11] + \
                           '", "text":"' + newText12 + '"}'
            else:
                JSONline = '{"beer name":' + '"' + beerVal[0] + '"' + ', "beerId":' + beerVal[1] + ', "brewerId":' + \
                           beerVal[2] + \
                           ', "ABV":' + beerVal[3] + ', "style":"' + beerVal[4] + '", "appearance":' + \
                           beerVal[5] + ', "aroma": ' + beerVal[6] + ', "palate":' + beerVal[7] + ', "taste":' + \
                           beerVal[8] + \
                           ', "overall":' + beerVal[9] + ', "time":"' + beerVal[10] + '", "profileName":"' + beerVal[
                               11] + \
                           '", "text":"' + newText12 + '"}'

            beerID.append(beerVal[1] + "\n")
            output.write(JSONline)
            beerVal = []
            i = 0
            a = 0
            b += 1
        else:
            beerVal.append(line[beer_poz[a]:-1])  # towrzy listę wartości z recenzji, usuwa opisy
            # print(line[beer_poz[a]:])
            i += 1
            a += 1
print(len(beerID))
beerID = list(set(beerID))  # usunięcie duplikatów
print(len(beerID))
for poz in beerID:
    output2.write(poz)

#output.write("]")
output.close()
output2.close()