import csv

with open(r"C:\Users\Elèves\Documents\Info\ventes.csv",encoding="utf-8",mode='r') as fichier_ouvert:
    table=list(csv.reader(fichier_ouvert))

#table[0].append("CA")
#print(table[0])


for ligne in table[1:]:
    ligne.append(float(ligne[2])*float(ligne[3]))
    #print(ligne)
'''

def tri(table):
    for i in range(1,len(table)):
        max = table[i][5]
        indice_max = i
        for j in range(i+1, len(table)):
            if table[j][5] > max :
                max = table[j][5]
                indice_max = j
        table[i], table[indice_max] = table[indice_max], table[i]
    return table


print(tri(table))

'''
print(sorted(table[1:], key=lambda x: x[5],reverse=True))
