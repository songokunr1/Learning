import matplotlib


def podatek(zarobek, skladka, koszt):
    podatek = zarobek-skladka-koszt
    if podatek > 0:
        return podatek
    else:
        return 0

zarobki = range(100, 5000, 100)
koszt = [x*0.8 for x in zarobki]
podatatek_procentowy = [((zarobek-400)*0.085+400)/zarobek for zarobek in zarobki]
podatatek_procentowy_19 = [((zarobek-380)*0.19+380)/zarobek for zarobek in zarobki]
podatatek_procentowy_19_koszt = [(podatek(zarobek, 380, k)*0.19+380) for zarobek, k in zip(zarobki, koszt)]
podatatek_procentowy_19_proc = [netto/zarobek for netto, zarobek in zip(podatatek_procentowy_19_koszt, zarobki)]
# Comment out or remove the next line
matplotlib.use('Agg')


import matplotlib.pyplot as plt
import seaborn as sns
sns.lineplot(podatatek_procentowy_19_koszt)
plt.plot()

# sns.lineplot(x=zarobki, y=podatatek_procentowy)
# plt.show()
# for zarobek in podatatek_procentowy:
#     print(str(zarobek).replace('.',','))

# for zarobek in podatatek_procentowy_19_koszt:
#     print(str(zarobek).replace('.',','))
# #
# for zarobek in podatatek_procentowy_19_proc:
#     print(str(zarobek).replace('.',','))

