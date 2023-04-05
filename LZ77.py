
#klasa wektora kodowego
class wektor:
    def __init__(self, pozycja_slownik, dlugosc_slowa, symbol_po_slowie):
        self.pozycja_slownik = pozycja_slownik
        self.dlugosc_slowa = dlugosc_slowa
        self.symbol_po_slowie = symbol_po_slowie

#funkcja dekodowania
def dekoduj(nazwaPliku, rozmiarSlownikBufor):
    try:
        file2 = open(nazwaPliku, "r") #plik z ktorego beda odczytywane wektory kodowe
    except:
        print("Problem z otwarciem pliku")
        exit()
    wektory2 = [] #lista wektorow kodowych
    wejscie2 = [] #lista wejscia z pliku
    for line in file2: #czytaj sekwencje zakodowana z pliku
        wejscie2.append(line[:-1]) #usun znak nowej lini
    for line in wejscie2: #dodaj elementy do tablicy
        wektory2.append(wektor(line.split(",", 2)[0], line.split(",", 2)[1], line.split(",", 2)[2])) #rozgrupu po przecinku
    slowo_zdekodowane = []
    sekwencja_zdekodowana = []
    sl = [] #slownik
    element = wektory2.pop(0)  # wez pierwszy wektor do dekodowania
    for x in range(rozmiarSlownikBufor):  # wypelnij slownik
        sl.append(element.symbol_po_slowie)
    sekwencja_zdekodowana.append(element.symbol_po_slowie)
    for obj in wektory2:
        for i in range(int(obj.dlugosc_slowa)):
            slowo_zdekodowane.append(sl[(int(obj.pozycja_slownik) + i)]) #symbole ze slownika przenies do slowa zdekodowanego
        for i in range(int(obj.dlugosc_slowa)):  # usun elementy ze slownika
            sl.pop(0)
        sl.pop(0)  # przesun slownik o 1 miejsce
        slowo_zdekodowane.append(obj.symbol_po_slowie) #dodaj do sekwencji zdekodowanej symbol po slowie z wektora kodowego
        for znak in slowo_zdekodowane:
            sekwencja_zdekodowana.append(znak)  # dodaj elementy do sekwencji zdekodowanej
        for i in range(len(slowo_zdekodowane)):
            sl.append(slowo_zdekodowane.pop(0))  # dodaj do slownika slowo zdekodowane

    try:
        file3 = open("TIK_sekwencja_zdekodowana.txt", "w")  # zapisz sekwencje zdekodowana do pliku
    except:
        print("Problem z otwarciem pliku")
        exit()
    sekwencja_zdekodowana_string = ""
    for x in sekwencja_zdekodowana:
        sekwencja_zdekodowana_string += x
    file3.write(sekwencja_zdekodowana_string)
    file2.close()
    file3.close()


#funkcja kodowania
def kodowanie(wejscie, rozmiarSlownikBufor):
    #dane podstawowe
    try:
        file2 = open("TIK_output.txt", "w")  # plik w ktorym zostana zapisane wektory kodowe
    except:
        print("Problem z otwarciem pliku")
        exit()
    wektory = []
    slownik = []
    buffor = []
    buffor_tmp = ""
    slownik_tmp = ""
    pierwszy_symbol = wejscie.pop(0) #wez pierwszy element z wejscia
    wektory.append(wektor(0, 0, pierwszy_symbol)) #dodaj wektor kodowy do listy
    for i in range(rozmiarSlownikBufor): #wypelnij slownik i bufor pierwszym symbolem z pliku
        slownik.append(pierwszy_symbol)
        buffor.append(wejscie.pop(0))
    for x in slownik:
        slownik_tmp += x
    for x in buffor:
        buffor_tmp += x

    while len(buffor) > 0 : #wykonuj dopóki buffor > 0
        buffor_tmp2 = buffor_tmp
        while len(buffor_tmp2) > 0: #sprawdz czy istnieje sekwencja w slowniku
            buffor_tmp2 = buffor_tmp2[:-1]  # zmniejsz rozmiar szukanej sekwencji o 1 element
            if (slownik_tmp.find(buffor_tmp2)) != -1: #znaleziono sekwencje w slowniku
                break
        dlugosc = len(buffor_tmp2) #dlugosc slowa
        symbol_bufor = buffor_tmp[dlugosc] #symbol po slowie
        pozycja_slownik = slownik_tmp.index(buffor_tmp2) #pozycja slowa w slowniku
        wektory.append(wektor(pozycja_slownik, dlugosc, symbol_bufor)) #dodaj element do listy wektorow kodowych
        for x in range(dlugosc + 1): #przesun slownik bufor wejscie
            if (len(wejscie) <= 0):
                slownik.append(buffor.pop(0)) #usun element z bufora i dodaj do slownika
                slownik.pop(0) #usun element ze slownika
            else:
                buffor.append(wejscie.pop(0)) #dodaj element na koniec bufora
                slownik.append(buffor.pop(0)) #dodaj element na koniec slownika z bufora
                slownik.pop(0) #usun element ze slownika
        buffor_tmp = ""
        slownik_tmp = ""
        for x in slownik: #wypelnij tymczasowny slownik
            slownik_tmp += x
        for y in buffor: #wypelnij tymczasowny bufor
            buffor_tmp += y
    for obj in wektory:
        file2.write(str(obj.pozycja_slownik) + "," + str(obj.dlugosc_slowa) + "," + obj.symbol_po_slowie + "\n")  # zapis do pliku
    file2.close()

#odczytywanie symboli z pliku
# 'main function'
file_name = input("Podaj nazwe pliku dla ktorego zostana zakodowane symbole: ")
file_name += ".txt"
try:
    file = open(file_name, "r") #plik z symbolami do zakodowania
except:
    print("Problem z otwarciem pliku")
    exit()
wejscie = [] # lista w ktorej zostaną zapisane wektory kodowe
while True: #czytaj z pliku
    char = file.read(1)
    if not char:
        break
    wejscie.append(char) #dodaj znak do lisy
file.close()
ile_znakow = wejscie.count('\n')
for i in range(ile_znakow):# usun znaki nowej lini jesli wystepuja
    wejscie.remove('\n')
rozmiarSlownikBufor = int(len(wejscie) - 1) #definiuj dlugosc slownika i bufora
#kodowanie
kodowanie(wejscie, rozmiarSlownikBufor)
#dekodowanie
dekoduj("TIK_output.txt", rozmiarSlownikBufor)

