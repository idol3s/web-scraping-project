from numpy import median, mean, sqrt
from matplotlib import pyplot as plt


# Zadanie 8
def srednia_ocen(adr, oceny):
    licznik_w = 0
    licznik_m = 0
    sum_wiejski = 0
    sum_miejski = 0

    for i, j in zip(oceny, adr):
        if j == 'r':
            sum_wiejski += i
            licznik_w += 1
        elif j == 'u':
            sum_miejski += i
            licznik_m += 1

    srednia_wiejski = sum_wiejski / licznik_w if licznik_w != 0 else 0
    srednia_miejski = sum_miejski / licznik_m if licznik_m != 0 else 0

    return round(srednia_miejski, 2), round(srednia_wiejski, 2)


# Zadanie 9
def mediana_ocen(adr, oceny):
    wiejski = [i for i, j in zip(oceny, adr) if j == 'r']
    miejski = [i for i, j in zip(oceny, adr) if j == 'u']
    
    return median(oceny), median(miejski), median(wiejski)


# Zadanie 10/11
def sigma(x):
    return sqrt((sum([(i-mean(x))**2 for i in x])/len(x)))


# Zadanie 10/11
def odchyl_std(adr, oceny):
    wiejski = [i for i, j in zip(oceny, adr) if j == 'r']
    miejski = [i for i, j in zip(oceny, adr) if j == 'u']
    
    return sigma(oceny), sigma(miejski), sigma(wiejski)


# Zadanie 12
def obliczanie_mody(adr, oceny):
    wiejski = [i for i, j in zip(oceny, adr) if j == 'r']
    miejski = [i for i, j in zip(oceny, adr) if j == 'u']
    
    return moda(oceny), moda(miejski), moda(wiejski)


# Zadanie 12
def moda(liczby):
    najczesciej = {}
    for i in liczby:
        if i in najczesciej:
            najczesciej[i] += 1
        else:
            najczesciej[i] = 1
            
    max_licznik = 0
    najczesciej_liczba = 0
    
    for wartosc, licznik in najczesciej.items():
        if licznik > max_licznik:
            max_licznik = licznik
            najczesciej_liczba = wartosc
    
    return najczesciej_liczba


# Zadanie 13
def korelacja_regresja_r2(nobec, oceny):
    return korelacja(nobec, oceny), reg_liniowa(nobec, oceny), r2(nobec, oceny)


# Zadanie 13
def korelacja(x, y):
    return sum([(i-mean(x))*(j-mean(y)) for i, j in zip(x, y)])/sqrt(sum([(i-mean(x))**2 for i in x])
                                                                     * sum([(i-mean(y))**2 for i in y]))


# Zadanie 13
def reg_liniowa(x, y):
    a1 = sum([(i-mean(x))*(j-mean(y)) for i, j in zip(x, y)])/sum([(i-mean(x))**2 for i in x])
    a0 = mean(y-(a1*mean(x)))
    return f'{round(a0, 2)}x + {round(a1, 2)}'


# Zadanie 13
def r2(x, y):
    return 1-(sum((i-mean(y))**2 for i in y)/sum((j-i)**2 for i, j in zip(x, y)))


# Zadanie 14
def punkty_predykcja(nieobecnosci, grupy):
    liczba_zajec = 75
    punkty = []
    for liczba_nieobecnosci, grupa in zip(nieobecnosci, grupy):
        liczba_obecnosci = (liczba_zajec - liczba_nieobecnosci)
        punkty_obecnosci = liczba_obecnosci * 5
        if liczba_nieobecnosci == 0:
            punkty_obecnosci += 35
        if grupa == 'r':
            punkty_obecnosci += 2 * liczba_obecnosci
        punkty.append(punkty_obecnosci)

    return punkty


# Zadanie 15
def histogram_ocen(oceny):
    plt.hist(oceny, bins=20, edgecolor='black', color='orange')
    plt.xlabel('Oceny')
    plt.ylabel('Liczba uczniow')
    plt.title('Histogram ocen')
    plt.show()


# Zadanie 15
def histogram_punktow(oceny):
    plt.hist(oceny, bins=20, edgecolor='black', color='gold')
    plt.xlabel('Punkty')
    plt.ylabel('Liczba uczniow')
    plt.title('Histogram punktow')
    plt.show()


# Zadanie 15
def udzial_grup(oceny, adr):
    wiejski = [i for i, j in zip(oceny, adr) if j == 'r']
    miejski = [i for i, j in zip(oceny, adr) if j == 'u']
    
    plt.pie([len(wiejski)/len(oceny), len(miejski)/len(oceny)], labels=['obszar wiejski', 'obszar miejski'],
            autopct='%0.1f%%', colors=['lime', 'red'])
    plt.legend(['obszar wiejski', 'obszar miejski'], edgecolor='black', loc='upper left')
    plt.axis('equal')
    plt.title('% udział poszczególnych grup w klasie')
    plt.show()


# Zadanie 15
def punktowy(oceny, adr, nobec):
    o_wiejski = [i for i, j in zip(oceny, adr) if j == 'r']
    o_miejski = [i for i, j in zip(oceny, adr) if j == 'u']
    
    n_wiejski = [i for i, j in zip(nobec, adr) if j == 'r']
    n_miejski = [i for i, j in zip(nobec, adr) if j == 'u']
    
    plt.scatter(o_wiejski, n_wiejski, color='lime')
    plt.scatter(o_miejski, n_miejski, color='red')
    
    plt.title('Punktowy wykres ocen dla dwóch grup')
    plt.ylabel('Nieobecności')
    plt.xlabel('Oceny')
    plt.legend(['Wieś', 'Miasto'], edgecolor='black')
    plt.show()


# Zadanie 15
def wykres_punktowy_predykcji(predykcja, grupa):
    punkty_wsi = [predykcja[i] for i in range(len(predykcja)) if grupa[i] == 'r']
    punkty_miasta = [predykcja[i] for i in range(len(predykcja)) if grupa[i] == 'u']

    plt.scatter(punkty_miasta, [i for i in range(len(punkty_miasta))], color='blue', label='Miasto')
    plt.scatter(punkty_wsi, [i for i in range(len(punkty_wsi))], color='green', label='Wieś')

    plt.xlabel('Przewidziane punkty')
    plt.ylabel('ID ucznia')
    plt.title('Przewidziane punkty dla uczniów')
    plt.legend(edgecolor='black')
    plt.show()


# Zadanie 16
def zawody_rodzicow(m_zawod, o_zawod):
    job_counts_mother = {}
    job_counts_father = {}

    for job in m_zawod:
        if job not in job_counts_mother:
            job_counts_mother[job] = 0
        job_counts_mother[job] += 1

    for job in o_zawod:
        if job not in job_counts_father:
            job_counts_father[job] = 0
        job_counts_father[job] += 1

    jobs = list(set(m_zawod + o_zawod))
    counts_mother = [job_counts_mother.get(job, 0) for job in jobs]
    counts_father = [job_counts_father.get(job, 0) for job in jobs]

    x = range(len(jobs))
    width = 0.4

    plt.figure(figsize=(12, 6))
    plt.bar(x, counts_mother, width=width, label='Matka', align='center', color='violet', edgecolor='black')
    plt.bar([p + width for p in x], counts_father, width=width, label='Ojciec', align='center', color='coral',
            edgecolor='black')

    plt.xlabel('Zawód', fontsize=14)
    plt.ylabel('Liczba wystąpień', fontsize=14)
    plt.title('Dominujące zawody rodziców uczniów', fontsize=16)
    plt.xticks([p + width / 2 for p in x], jobs, rotation=45, fontsize=12)
    plt.legend(fontsize=15, edgecolor='black')
    plt.tight_layout()
    plt.show()

    return job_counts_mother, job_counts_father


with (open("dane_szkola.txt", encoding='utf8') as plik):
    header = plik.readline()
    dane = []
    
    for i in plik:
        dane.append(i.replace('\n', '').split(','))

    adres = [dane[i][0].lower() for i in range(len(dane))]
    nieobecnosc = [int(dane[i][1]) for i in range(len(dane))]
    mjob = [dane[i][2] for i in range(len(dane))]
    fjob = [dane[i][3] for i in range(len(dane))]
    ocena = [int(dane[i][4]) for i in range(len(dane))]

    sr_miasta, sr_wsi = srednia_ocen(adres, ocena)
    print(f'Średnia dla miasta wynosi {sr_miasta}, a dla wsi {sr_wsi}')
    print('---' * 50)

    med_ocen, med_miasta, med_wsi = mediana_ocen(adres, ocena)
    print(f'Mediana wszystkich ocen wynosi {med_ocen}, dla miasta {med_miasta}, dla wsi {med_wsi}')
    print('---' * 50)
    
    odch_ocen, odch_miasta, odch_wsi = odchyl_std(adres, ocena)
    print(f'Odchylenie standartowe wszystkich ocen wynosi {round(odch_ocen, 2)}, dla miasta {round(odch_miasta, 2)},'
          f' dla wsi {round(odch_wsi, 2)}')
    print('---' * 50)
    
    moda_oceny, moda_miasto, moda_wies = obliczanie_mody(adres, ocena)
    print(f'Moda dal wszystkich ocen wynosi {moda_oceny}, dla miasta {moda_miasto}, dla wsi {moda_wies}')
    print('---' * 50)
    
    r, reg, wspol_r2 = korelacja_regresja_r2(nieobecnosc, ocena)
    print(f'Wspołczynnik korelacji imedzy nieobecnoscia a oceną wyniosi {round(r, 2)}, regresja linoiwa {reg},'
          f' R2= {round(wspol_r2, 2)}')
    print('---' * 50)

    predykcja_wynik = punkty_predykcja(nieobecnosc, adres)
    print(f'Punkty za obecnosci: {predykcja_wynik}.')
    print('---' * 50)

    histogram_ocen(ocena)
    histogram_punktow(predykcja_wynik)
    udzial_grup(ocena, adres)
    punktowy(ocena, adres, nieobecnosc)
    wykres_punktowy_predykcji(predykcja_wynik, adres)
    zawody_rodzicow(mjob, fjob)
