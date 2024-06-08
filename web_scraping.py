import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk


def scrape_data(url):  # utworzenie funkcji do latwiejszego scrapowania danych uzywajac powtarzajacych sie elementów
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


# zapytanie dla cpu
soup = scrape_data('https://www.cpubenchmark.net/cpu_value_available.html')  # scrapowana strona
cpu = soup.find_all('span', class_="prdname")
cpu = [i.text for i in cpu]  # zapisanie nazw cpu do listy

cpu_prices = soup.find_all('span', class_="price-neww")  # pobranie danych odnosnie cen dla kazdego cpu
cpu_prices = [float(i.text.replace('$', '').replace(',', '')) for i in cpu_prices]
# oczyszczenie listy z cenami

cpu_scores = soup.find_all('span', class_="mark-neww")  # pobranie danych odnosnie oceny dla kazdego cpu
cpu_scores = [float(i.text.replace(',', '.')) for i in cpu_scores]  # oczyszczenie
cpu_scores = [round(i/max(cpu_scores), 2) for i in cpu_scores]  # oraz znormalizowanie listy cen
# (oceny dla kazdego produktu podawane sa w innej skali,
# w celu osiągniecia większej miarodajności oraz niezależności poszeczegolnego elementu, zostały one znormalizowane)

cpu_prices = dict(zip(cpu, cpu_prices))  # stworzenie slownika z cena kazdego cpu
cpu_scores = dict(zip(cpu, cpu_scores))  # stworzenie slownika z ocena kazdego cpu

# zapytanie dla gpu
soup = scrape_data('https://www.videocardbenchmark.net/gpu_value.html')  # scrapowana strona
gpu = soup.find_all('span', class_="prdname")
gpu = [i.text for i in gpu]  # zapisanie nazw gpu do listy

gpu_prices = soup.find_all('span', class_="price-neww")  # pobranie danych odnosnie cen dla kazdego gpu
gpu_prices = [float(i.text.replace('$', '').replace(',', '').replace('*', ''))
              for i in gpu_prices]  # oczyszczenie listy z cenami

gpu_scores = soup.find_all('span', class_="mark-neww")  # pobranie danych odnosnie oceny dla kazdego gpu
gpu_scores = [float(i.text.replace(',', '.')) for i in gpu_scores]
gpu_scores = [round(i/max(gpu_scores), 2) for i in gpu_scores]  # oczyszczenie oraz znormalizowanie listy cen

gpu_prices = dict(zip(gpu, gpu_prices))  # stworzenie slownika z cena kazdego gpu
gpu_scores = dict(zip(gpu, gpu_scores))  # stworzenie slownika z ocena kazdego gpu

# zapytanie dla hdd
soup = scrape_data('https://www.harddrivebenchmark.net/hdd_value.html')  # scrapowana strona
hdd = soup.find_all('span', class_="prdname")
hdd = [i.text for i in hdd]  # zapisanie nazw hdd do listy

hdd_prices = soup.find_all('span', class_="price-neww")  # pobranie danych odnosnie cen dla kazdego hdd
hdd_prices = [float(i.text.replace('$', '').replace(',', '').replace('*', ''))
              for i in hdd_prices]  # oczyszczenie listy z cenami

hdd_scores = soup.find_all('span', class_="mark-neww")  # pobranie danych odnosnie oceny dla kazdego hdd
hdd_scores = [float(i.text.replace(',', '.')) for i in hdd_scores]
hdd_scores = [round(i/max(hdd_scores), 2) for i in hdd_scores]  # oczyszczenie oraz znormalizowanie listy cen

hdd_prices = dict(zip(hdd, hdd_prices))  # stworzenie slownika z cena kazdego hdd
hdd_scores = dict(zip(hdd, hdd_scores))  # stworzenie slownika z ocena kazdego hdd

# Zapytania dla ram
soup = scrape_data('https://www.memorybenchmark.net/popular.html')  # Scrapowana strona
ram = soup.find_all('span', class_="prdname")
ram = [i.text for i in ram]  # zapisanie nazw ram do listy

ram_prices = soup.find_all('span', class_="price-neww")  # pobrane cen dla kazdego ramu
ram_prices = [float(i.text.replace('*', '').replace('NA', '0')) for i in ram_prices]
# oczyszczenie listy

ram_scores = soup.find_all('span', class_="count")  # pobrane danych dla ocen (przed konwersja)
ram_scores = [float(i.text.replace(' %', '')) * 10.0 for i in ram_scores]
# konwersja z procentow na wyniki

# Usunięcie rekordów z ceną równą zero i dostosowanie normalizacji
ram_data = list(zip(ram, ram_prices, ram_scores))
ram_data = [(name, price, score) for name, price, score in ram_data if price > 0]

# Obliczenie maksymalnej wartości ocen ze zmodyfikowanych danych
max_ram_score = max(ram_data, key=lambda x: x[2])[2]

# Normalizacja ocen RAM na podstawie maksymalnej wartości z danych po usunięciu cen równych zero
ram = [data[0] for data in ram_data]
ram_prices = {data[0]: data[1] for data in ram_data}
ram_scores = {data[0]: data[2] / max_ram_score for data in ram_data}

# Zapytania dla płyt głównych
soup = scrape_data('https://versus.com/en/motherboard')
mother_board = soup.find_all('p', class_="BarsItem__name___3EC0w")
mother_board = [i.text for i in mother_board]

mother_board_prices = soup.find_all('div', class_="BarsItem__price___3dk0c")
mother_board_prices = [float(i.text[-5:].replace(',', '.')) * 100 if len(i.text) > 0 else None
                       for i in mother_board_prices]

mother_board_scores = soup.find_all('span', class_="pointsText")
mother_board_scores = [float(i.text.replace('points', '')) for i in mother_board_scores]
mother_board_scores = [round(i/max(mother_board_scores) * 0.3, 3) for i in mother_board_scores]

mother_board_data = list(zip(mother_board, mother_board_prices, mother_board_scores))
mother_board_data = [(name, price, score) for name, price, score in mother_board_data]

mother_board = [data[0] for data in mother_board_data]
mother_board_prices = {data[0]: data[1] for data in mother_board_data}
mother_board_scores = {data[0]: data[2] for data in mother_board_data}


# fragment odpowiedzialny za pobieranie walut
soup = scrape_data('https://www.money.pl/pieniadze/nbp/srednie/')  # scrapowana strona
site = soup.find_all('div', class_="rt-td")
currencies = []
values = []
for i in range(1, len(site), 5):
    # element div o klasie "rt-td" okazał sie mieć taką budowe, ze takie rozwiazanie jest chyba najlepsze
    currencies.append(site[i].text) 
for i in range(2, len(site), 5):
    values.append(site[i].text)
values = [float(i.replace(',', '.')) for i in values]  # standardowe czyszczenie

# ze wzgledu ze dane zostaly pobrane z polskiej strony, nie ma tam mozliwosci przeliczania PLN -> PLN (logiczne)
# jednak my chcemy dac mozliwosc wyswietlania uzytkownikowi cen w PLN
currencies.insert(0, "PLN")  # Dodajemy PLN na poczatek listy
values.insert(0, 1)  # domyslna cena jest w PLN, wiec mnoznik dla PLN jest po prostu 1
exchange_rates = dict(zip(currencies, values))  # stworzenie slownika z kursem dla kazdej waluty


# funkcja sluzaca obliczaniu wynikow po nacisnieciu odpowiedniego przycisku w GUI
def calculate():
    try:
        selected_cpu = cpu_combobox.get()
        selected_gpu = gpu_combobox.get()
        selected_hdd = hdd_combobox.get()
        selected_ram = ram_combobox.get()
        selected_currency = currency_combobox.get()
        selected_mother = mother_board_combobox.get()
        exchange_rate = exchange_rates[selected_currency]
    
        total_price = round((cpu_prices[selected_cpu] + gpu_prices[selected_gpu] + hdd_prices[selected_hdd] +
                             ram_prices[selected_ram] + mother_board_prices[selected_mother])*exchange_rates["USD"], 2)
        total_price = round(total_price / exchange_rate, 2)
        total_score = round(cpu_scores[selected_cpu] + gpu_scores[selected_gpu] + hdd_scores[selected_hdd] +
                            ram_scores[selected_ram] + mother_board_scores[selected_mother], 2)

        if total_score < 0.9:
            total_score_label.config(text=f"Łączny wynik: {total_score} (słaby)")
            total_score_label.config(foreground="red")
        elif 0.9 <= total_score < 1.15:
            total_score_label.config(text=f"Łączny wynik: {total_score} (średni)")
            total_score_label.config(foreground="yellow")
        else:
            total_score_label.config(text=f"Łączny wynik: {total_score} (świetny!)")
            total_score_label.config(foreground="green")

        # Update total price label
        total_price_label.config(text=f"Łączna cena: {total_price} {selected_currency}")

    except KeyError:
        total_score_label.config(text="Wybierz każdy komponent!")  # lekka, prymitywna kontrola bledow
        total_price_label.config(text="")  # lekka, prymitywna kontrola bledow


def show_prices():
    selected_cpu = cpu_combobox.get()
    selected_gpu = gpu_combobox.get()
    selected_hdd = hdd_combobox.get()
    selected_ram = ram_combobox.get()
    selected_mother_board = mother_board_combobox.get()
    selected_currency = currency_combobox.get()
    exchange_rate = exchange_rates[selected_currency]

    cpu_price = round(cpu_prices[selected_cpu] * exchange_rates["USD"] / exchange_rate, 2)
    gpu_price = round(gpu_prices[selected_gpu] * exchange_rates["USD"] / exchange_rate, 2)
    hdd_price = round(hdd_prices[selected_hdd] * exchange_rates["USD"] / exchange_rate, 2)
    ram_price = round(ram_prices[selected_ram] * exchange_rates["USD"] / exchange_rate, 2)
    mother_board_price = round(mother_board_prices[selected_mother_board] * exchange_rates["USD"] / exchange_rate, 2)

    prices_cpu_label.config(text=f"Cena CPU: {cpu_price} {selected_currency}")
    prices_gpu_label.config(text=f"Cena GPU: {gpu_price} {selected_currency}")
    prices_hdd_label.config(text=f"Cena HDD: {hdd_price} {selected_currency}")
    prices_ram_label.config(text=f"Cena RAM: {ram_price} {selected_currency}")
    prices_mother_label.config(text=f"Cena płyty głównej: {mother_board_price} {selected_currency}")


root = tk.Tk()  # utworzenie okna dla naszego GUI
root.title("Podsumowanie podzespołów")
root.configure(bg="#2e2e2e")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 500
window_height = 650
position_top = int(screen_height/2 - window_height/2)
position_right = int(screen_width/2 - window_width/2)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Fragment kodu sluzacy dla nadanie stylu naszym przyciskom, labelom, etykietom
style = ttk.Style()
style.configure("TLabel", background="#2e2e2e", foreground="white", font=("Arial", 14))
style.configure("TCombobox", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12, "bold"), background="black", foreground="white")

style.map("TButton",
          foreground=[('!active', 'black'), ('pressed', 'white'), ('active', 'black')],
          background=[('!active', 'black'), ('pressed', 'black'), ('active', 'white')])

# Sortowanie wynikow, aby podzespoly byly wypisywane alfabetycznie
cpu.sort()
gpu.sort()
hdd.sort()
ram.sort()
mother_board.sort()

# Tworzenie rozwijanych list oraz labeli
cpu_label = ttk.Label(root, text="Wybierz CPU:")  # label dla CPU
cpu_label.grid(row=0, column=0, padx=50, pady=10, sticky='w')
cpu_combobox = ttk.Combobox(root, values=cpu)  # rozwijana lista dla CPU
cpu_combobox.grid(row=0, column=1, padx=20, pady=10, sticky='e')

gpu_label = ttk.Label(root, text="Wybierz GPU:")  # label dla GPU
gpu_label.grid(row=1, column=0, padx=50, pady=10, sticky='w')
gpu_combobox = ttk.Combobox(root, values=gpu)  # rozwijana lista dla GPU
gpu_combobox.grid(row=1, column=1, padx=20, pady=10, sticky='e')

hdd_label = ttk.Label(root, text="Wybierz HDD/SSD:")  # label dla HDD
hdd_label.grid(row=2, column=0, padx=50, pady=10, sticky='w')
hdd_combobox = ttk.Combobox(root, values=hdd)  # rozwijana lista dla HDD
hdd_combobox.grid(row=2, column=1, padx=20, pady=10, sticky='e')

ram_label = ttk.Label(root, text="Wybierz RAM:")
ram_label.grid(row=3, column=0, padx=50, pady=10, sticky='w')
ram_combobox = ttk.Combobox(root, values=ram)
ram_combobox.grid(row=3, column=1, padx=20, pady=10, sticky='e')

mother_board_label = ttk.Label(root, text="Wybierz płytę główną:")  # label dla HDD
mother_board_label.grid(row=4, column=0, padx=50, pady=10, sticky='w')
mother_board_combobox = ttk.Combobox(root, values=mother_board)  # rozwijana lista dla HDD
mother_board_combobox.grid(row=4, column=1, padx=20, pady=10, sticky='e')

currency_label = ttk.Label(root, text="Wybierz walutę:")
currency_label.grid(row=5, column=0, padx=50, pady=10, sticky='w')
currency_combobox = ttk.Combobox(root, values=list(currencies))  # rozwijana lista dla walut
currency_combobox.grid(row=5, column=1, padx=20, pady=10, sticky='e')
currency_combobox.current(0)  # Domyślnie ustawiona na PLN

calculate_button = ttk.Button(root, text="Oblicz", command=calculate)
# utworzenie przycisku i wywolanie wcześniej napisanej funkcji calculate
calculate_button.grid(row=6, column=0, columnspan=2, pady=20)

# Etykieta do wyświetlania wyników
total_score_label = ttk.Label(root, text="Łączny wynik:") 
total_score_label.grid(row=7, column=0, columnspan=2, pady=5)

# Etykieta do wyświetlania cen
total_price_label = ttk.Label(root, text="Łączna cena:")
total_price_label.grid(row=8, column=0, columnspan=2, pady=5)

# utworzenie nowego przycisku
price_button = ttk.Button(root, text="Pokaż ceny szczegółowe", command=show_prices)
price_button.grid(row=9, column=0, columnspan=2, pady=20)

# Etykiety do wyświetlania cen szczegółowych
prices_cpu_label = ttk.Label(root, text="")
prices_cpu_label.grid(row=10, column=0, columnspan=2, pady=5, padx=50, sticky='w')

prices_hdd_label = ttk.Label(root, text="")
prices_hdd_label.grid(row=10, column=1, columnspan=2, pady=5, padx=45, sticky='w')

prices_gpu_label = ttk.Label(root, text="")
prices_gpu_label.grid(row=11, column=0, columnspan=2, pady=5, padx=50, sticky='w')

prices_ram_label = ttk.Label(root, text="")
prices_ram_label.grid(row=11, column=1, columnspan=2, pady=5, padx=45, sticky='w')

prices_mother_label = ttk.Label(root, text="")
prices_mother_label.grid(row=12, column=1, columnspan=2, pady=5, padx=45, sticky='w')

# Pzycisk wyjscia z naszego okienka
wyjscie = tk.Button(root, 
                    text='Wyjscie',
                    width=10,
                    bg='tomato',
                    command=root.destroy,
                    bd=4)
wyjscie.grid(column=1, row=13, padx=20, pady=20, sticky=tk.SE)

root.mainloop()