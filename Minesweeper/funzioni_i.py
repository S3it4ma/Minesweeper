import random
import pygame


def init_matrix(rows, columns, x = 0):
    '''matrice con c colonne e r righe di valore x. Se x non specificata di default è zero'''

    matrix = [[x] * columns for i in range(rows)]
    return matrix


def vicini(matrix, x, y):

    ris = []
    for i in range(x-1, x+2):
        
        for j in range(y-1, y+2):

            if (i != x or j != y) and 0 <= i < len(matrix) and 0 <= j < len(matrix[0]):

                ris.append((i, j))
    
    return ris


def calc_grid(WIDTH, HEIGHT, box_lenght, n, space_from_top = 0):

    '''permette di calcolare la posizione di ogni box (di lunghezza box_lenght) della gliglia quadrata (di dimensione n) di modo che quest'ultima
    sia centrata al livello della finestra di altezza HEIGHT e larghezza WIDTH. Restituisce un dizionario con chiave le coordinate del box (come idici di una matrice)
    e valore il pygame.Rect associato (calcolato dopo aver preso le coordinate dell'angolo in alto a sinistra).
    space_from_top permette di aggiungere delle quantità in modo da spostare la griglia più in basso rispetto al centro'''

    box_dict = {}
    i = 0                                                      #coordinate del box
    j = 0

    if n % 2 == 0:
        x = (WIDTH // 2) - (box_lenght * (n/2))
        y = (HEIGHT // 2) - (box_lenght * (n/2)) + space_from_top
    else:
        x = (WIDTH // 2) - (box_lenght * (n//2)) - (box_lenght / 2)
        y = (HEIGHT // 2) - (box_lenght * (n//2)) - (box_lenght / 2) + space_from_top


    while i < n:

        box_dict[(i, j)] = (x, y)                        
        
        x += box_lenght
        
        j += 1

        if j % n == 0 and j != 0:
            j = 0
            i += 1

            x -= box_lenght * n
            y += box_lenght

    
    for key, value in box_dict.items():

        x = value[0]
        y = value[1]

        box_rect = pygame.Rect(x, y, box_lenght, box_lenght)
        box_dict[key] = box_rect 
    
    return box_dict






def crea_mat(rows = 9, columns = 9, mines = 10):

    '''crea una matrice con valori pre-impostati per prato fiorito e restituisce, oltre alla matrice, anche una lista con le posizioni delle mine'''

    num_mines = 0

    matrix = init_matrix(rows, columns)
    mine_location =[]

    while num_mines < mines:

        x= random.randrange(0, rows)
        y= random.randrange(0, columns)
        
        if (x,y) not in mine_location:
            
            matrix[x][y]= -1
            mine_location.append((x, y))
            
            num_mines += 1
        
    print(mine_location)


    for (x,y) in mine_location:
        
        neighbours = vicini(matrix, x, y)

        for (i, j) in neighbours:
            if matrix[i][j] != -1:
                matrix[i][j] += 1

    return matrix, mine_location