from matplotlib import pyplot as plt
from math import log as ln, exp, tanh


def modelowanie_krzywych_VES(r, h, ro, n):
    dict_fj = {
        3: 0.0225,
        2: -0.0499,
        1: 0.1064,
        0: 0.1854,
        -1: 1.972,
        -2: -1.5716,
        -3: 0.4018,
        -4: -0.0814,
        -5: 0.0148
    }

    dy = (ln(10)) / 3
    x = ln(r)
    y0 = x + 0.0488
    j = 4
    pa = 0

    while j > -5:
        j -= 1
        yj = y0 + j * dy
        lj = exp(-yj)
        tj = ro[-1] * n
        i = len(h) - 1

        while i >= 0:
            z = lj * h[i]
            tj = (tj + ro[i] * tanh(z)) / (1 + (tj / ro[i]) * tanh(z))
            i -= 1

        pa += tj * dict_fj[j]

    return pa


def podaj_dane():
    print('Witaj użytkowniku!')
    warstwy = int(input('Podaj ilość wartstw '))
    rho = []
    hh = []
    for i in range(warstwy):
        rho.append(int(input(f'Podaj opornosc dla warstwy {i + 1} = ')))
        if i != warstwy - 1:
            hh.append(int(input(f'Podaj miąszość dla warstwy {i + 1} = ')))

    return warstwy, rho, hh


pod_rozstaw = [1.47, 2.15, 3.16, 4.64, 6.81, 10, 14.7, 21.5, 31.6, 46.4, 68.1, 100]

pod_n_warstw, pod_ro, pod_h = podaj_dane()

x = []
y = []
for i in pod_rozstaw:
    x.append(i)
    y.append(modelowanie_krzywych_VES(i, pod_h, pod_ro, pod_n_warstw))

plt.scatter(x, y)

plt.xscale('log')
plt.yscale('log')

plt.xlabel('AB/2 [m]')
plt.ylabel('oporność pozorna')
plt.title('Krzywa teoretyczna')
plt.xticks([10 ** 0, 10 ** 1, 10 ** 2])
plt.yticks([10 ** 0, 10 ** 1, 10 ** 2, 10 ** 3])
plt.grid(True, which='both', linestyle='--')

plt.savefig('krzywaVES.png')
plt.show()

with open(f"wyniki_VES.txt", 'w', encoding='utf-8') as plik:
    plik.write("=" * 25)
    plik.write('\nModel:\n')

    plik.write('-----Oporność-----\n')
    for i in range(pod_n_warstw):
        plik.write(f'Warstwa {i + 1} = {pod_ro[i]}\n')

    plik.write('-----Miąszość-----\n')
    for i in range(pod_n_warstw - 1):
        plik.write(f'Warstwa {i + 1} = {pod_h[i]}\n')

    plik.write("=" * 25 + '\n')
    plik.write(f'AB/2\t\troa\n')
    for i, j in zip(x, y):
        plik.write(f'{i}\t\t{j}\n')
