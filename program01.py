# -*- coding: utf-8 -*-
'''
I Caponians, una specie aliena proviente da un non ben specificato
pianeta della galassia, stanno pianificando da un bel po' l'invasione
del pianeta Terra. Per farlo, hanno creato e installato in vari punti
del pianeta varie *mind bending machine*, macchine che riducono
l'intelligenza degli umani attraverso la rete telefonica [1].

Terminata la fase di riduzione dell'intelligenza umana, il prossimo
passo verso la conquista della Terra sara' lo sbarco sul nostro
pianeta, che avverra' non appena i Caponians avranno trovato dei punti
sufficientemente spaziosi per far atterrare le loro astronavi.

Un'astronave vista dall'alto puo' essere rappresentata come un
rettangolo di dimensioni W (larghezza) e H (altezza). Nel considerare
lo spazio necessario ad un'astronave per atterrare vanno pero' aggiunti
sui 4 lati del rettangolo 4 aree in piu'. Le aree in piu' sono una una
per lato.
Le aree sporgono tutte di una stessa quantita' D, per permettere di
aprire su ogni lato un portellone di sbarco. Ogni portellone e' quindi
largo quanto il lato dell'astronave su cui si trova e lungo D, su
qualunque lato si trovi.

I Caponians vorrebbero sbarcare con le loro astronavi in alcune nostre
citta', di cui hanno scaricato le rispettive mappe. Una citta' puo'
essere rappresentata come un'immagine rettangolare nera, in cui ogni
palazzo e' rappresentato come un rettangolo colorato (ogni palazzo ha
un colore che lo identifica univocamente).

Per definire gli ultimi dettagli del piano di sbarco, i Caponians
hanno bisogno di un algoritmo che, data la mappa di una citta' e un
elenco di astronavi definite come sopra, confermi oppure no se
ciascuna astronave ha abbastanza spazio per atterrare in quella citta',
aprire i suoi 4 portelloni e sbarcare il suo contenuto. Le astronavi
non atterrano contemporaneamente nella citta', quindi vanno valutate
separatamente le une rispetto alle altre.

(1) Quindi, data un'immagine nera (citta') con dei rettangoli colorati
pieni (palazzi) disegnati sopra, con ogni rettangolo di un colore
diverso da tutti gli altri, bisognera':

- determinare posizione, dimensioni e colore di ogni rettangolo
- salvare in un file di testo un rettangolo per riga
- nel file, ogni rettangolo e' rappresentato con una sequenza di 7 valori:
     x, y, w, h, r, g, b
  separati da virgole, in ordine di coordinata y (numero di riga)
  decrescente e, a parimerito, di x (pixel della riga) crescente.

(2) Successivamente, e' dato un file di testo contente N terne di
interi.  Ogni terna separata internamente e dalle altre terne da un
qualunque numero di spazi, tabulazioni o ritorni a capo. Ogni terna
rappresenta larghezza W, altezza H e distanza minima D (vedere sotto)
di un rettangolo (astronave) che si vorrebbe aggiungere all'immagine
al punto (1):

- restituire una lista di N valori booleani, l'i-esimo valore nella
lista e' True se nell'immagine c'e' abbastanza spazio per inserire
l'i-esimo rettangolo

- un rettangolo puo' essere inserito nell'immagine se esiste almeno una
posizione nell'immagine in cui c'e' abbastanza spazio (cioe' un'area
costituita interamente da pixel neri) per contenere il rettangolo
stesso, piu' le 4 "estensioni" del rettangolo, ossia i 4 portelloni
dell'astronave.

Ad esempio, se un'astronave da inserire ha 2 pixel di
larghezza e 3 di altezza e D = 2, bisognera' cercare uno spazio
nell'immagine adatto a contenere la seguente figura:

                              **
                              **
                            **++**
                            **++**
                            **++**
                              **
                              **

in cui i simboli + sono i pixel del rettangolo/astronave 2x3 e i *
sono i pixel delle 4 estensioni/portelloni

Esempio:
Data la seguente immagine rappresentata con un carattere per ogni
pixel, dove "." e' un pixel nero mentre caratteri diversi da "." sono
pixel colorati (*=rosso, +=verde):

**....
**....
......
......
....++
....++

Il file con i rettangoli trovati da voi salvato deve contenere le
righe:
4,4,2,2,0,255,0
0,0,2,2,255,0,0

e dati le seguenti astronavi:

(3, 3, 0)
(2, 2, 4)
(1, 1, 3)
(4, 2, 1)
(2, 4, 1)

verra' restituita la lista: [True, False, False, False, False]
infatti solo la prima astronave puo' atterrare ad esempio nella
zona marcata da 'X' (non ha sportelloni, infatti D = 0)

**.XXX
**.XXX
...XXX
......
....++
....++

mentre le altre non entrano nella mappa perche', pur avendo un punto
in cui possono atterrare, non possono aprire tutti i portelloni


[1] https://en.wikipedia.org/wiki/Zak_McKracken_and_the_Alien_Mindbenders)
'''

#from pngmatrix import load_png8

#def ex(file_png, file_txt, file_out):
    #pass

#if __name__ == "__main__":
    #pass
from pngmatrix import load_png8

def parse_numbers_from_file(file_txt):
    with open(file_txt) as f:
        numbers = []
        for line in f:
            line = line.strip().replace('\t', ' ').replace('\n', ' ')
            numbers += [int(num) for num in line.split()]
        return [tuple(numbers[i:i+3]) for i in range(0, len(numbers), 3)]

def extract_rectangles(image):
    width = len(image[0])
    height = len(image)
    dizionario = {}
    rectangles = []
    for y in range(height):
        for x in range(width):
            color = image[y][x]
            if color != (0, 0, 0):
                if color not in dizionario:
                    dizionario[color] = {'x_start': x, 'x_end': x, 'y_start': y, 'y_end': y}
                else:
                    dizionario[color]['x_end'] = max(dizionario[color]['x_end'], x)
                    dizionario[color]['y_end'] = max(dizionario[color]['y_end'], y)
                    
    for color, coords in dizionario.items():
        rectangles.append((coords['x_start'], coords['y_start'], coords['x_end'] - coords['x_start'] + 1, coords['y_end'] - coords['y_start'] + 1, color[0], color[1], color[2]))
        
    rectangles.sort(key=lambda x: (-x[1], x[0]))
    return rectangles

def create_spaceship_matrix(w, h, d):
    matrix = []
    ht = h + 2 * d
    wt = w + 2 * d
    for i in range(ht):
        row = []
        for j in range(wt):
            if d <= j < wt - d:
                row.append((0, 0, 0))
            else:
                if d <= i < ht - d:
                    row.append((0, 0, 0))                   
                else:
                    row.append((255, 255, 255))               
        matrix.append(row)
    return matrix

def find_free_space_in_image(image, matrix):
    for row in range(len(image) - len(matrix) + 1):
        for col in range(len(image[0]) - len(matrix[0]) + 1):
            match = True
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if matrix[i][j] == (0, 0, 0) and image[row + i][col + j] != (0, 0, 0):
                        match = False
                        break
                if not match:
                    break
            if match:
                return True
    return False

def ex(file_png, file_txt, file_out):
    image = load_png8(file_png)
    
    
    
    with open(file_out, "w") as f:
        for tuple in extract_rectangles(image):
            numbers_str = ",".join(str(num) for num in tuple)
            f.write(numbers_str + "\n")

    astronave = parse_numbers_from_file(file_txt)
    print(astronave)
    result=[]
    for ast in astronave:
        width, height, extension_length = ast
        matrix = create_spaceship_matrix(width, height, extension_length)

        result.append(find_free_space_in_image(image, matrix))    

    return result
    pass

if __name__ == "__main__":
    #print(ex('image7.png','rectangles7.txt','astronave7.txt'))
    #print(extract_rectangles('image0.png'))
    #print(parse_numbers_from_file('example.txt'))
    pass

