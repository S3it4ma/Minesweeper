import pygame
from funzioni_i import *
import os
import sys

smiley_height = 45                                 #altezza dello smile che servirà per la funzione calc_grid in funzioni_i
WIDTH = 900
HEIGHT = 700
BACKGROUND = (191, 191, 191)
WHITE = (255, 255, 255)

pygame.init()

FONT = pygame.font.Font(os.path.join("sounds_and_images\\minesweeper", "arcadeclassic\\ARCADECLASSIC.TTF"), 45)
NUM_FONT = pygame.font.Font(os.path.join("sounds_and_images\\minesweeper", "digital-7\\digital-7 (mono).ttf"), 55)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Minesweeper')

clock = pygame.time.Clock()


timer_rect = pygame.Rect(785, 30, 80, 45)
timer = pygame.draw.rect(WIN, (0,0,0), timer_rect)

mines_rect = pygame.Rect(35, 30, 80, 45)
mines_rect1 = pygame.draw.rect(WIN, (0,0,0), mines_rect)

smile = pygame.sprite.Sprite()
smile.image = pygame.transform.scale(pygame.image.load(os.path.join("sounds_and_images\\minesweeper", "all grid.png")), (120, 120))
smile.rect = smile.image.get_rect()
smile.rect.center = (450, 53)


beginner = pygame.sprite.Sprite()
beginner.image = FONT.render('Beginner', False, WHITE)
beginner.rect = pygame.Rect(0, 0, 320, 100)

intermidiate = pygame.sprite.Sprite()
intermidiate.image = FONT.render('Intermidiate', False, WHITE)
intermidiate.rect = pygame.Rect(0, 0, 320, 100)

expert = pygame.sprite.Sprite()
expert.image = FONT.render('Expert', False, WHITE)
expert.rect = pygame.Rect(0, 0, 320, 100)

beginner.rect.center, intermidiate.rect.center, expert.rect.center = (WIDTH/2, 230), (WIDTH/2, 350), (WIDTH/2, 465)

# misure in base alla difficoltà che ho standardizzato anche per evitare che i box fossero troppo grandi/piccoli,
# sono rispettivamente: num righe, num di colonne, num mine, 'taglia'
difficulty = {beginner : (9, 9, 10, 55), intermidiate : (16, 16, 40, 33), expert : (22, 22, 100, 25)}

start_group = pygame.sprite.Group(beginner, intermidiate, expert)


def find_zeros(box_dict, matrix, zeros_list, x, y):
    '''funzione ricorsiva che trova gli zero (caselle vuote) e li scopre, insieme ai numeri vicini'''

    for i in range(x-1, x+2):
            
        for j in range(y-1, y+2):

            if (i != x or j != y) and (0 <= i < len(matrix)) and (0 <= j < len(matrix[0])) and (box_dict[(i, j)].clicked == False):

                box_dict[(i, j)].clicked = True

                if matrix[i][j] == 0:
                    zeros_list.append((i, j))

    while len(zeros_list) > 0:
        (x, y) = zeros_list.pop()

        find_zeros(box_dict, matrix, zeros_list, x, y)



class Box(pygame.sprite.Sprite):
    '''Caselle di prato fiorito
    self.clicked --> indica se il box è stato cliccato ;
    self.value --> determina il valore del box (mina = -1, vuota = 0, box vicini a mine = 1 < x < 8) ;
    self.flag --> determina se sul box è stata posta la bandierina'''

    # num_mines indica il numero di mine e verrà cambiato una volta scelta la difficoltà 
    mine_clicked = False
    num_mines = 0

    def __init__(self, rect, value):
        super().__init__()
        self.image = None
        self.rect = rect
        self.value = value
        self.clicked = False
        self.flag = False
    
    def is_clicked(self, ev):
        '''cambia il valore di self.clicked; 
        determina se è stata cliccata una mina --> la variabile mine_clicked diventa True;
        cambia il conteggio delle mine'''

        click = ev.button
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos) and not Box.mine_clicked:
            if click == 1 and not self.flag:
                self.clicked = True

                if self.value == -1:
                    Box.mine_clicked = True

            if click == 3 and not self.clicked:
                self.flag = not self.flag
                if self.flag:
                    Box.num_mines -= 1
                else:
                    Box.num_mines += 1


    def update(self, box_lenght):
        '''funzione che aggiorna l'immagine delle mine'''

        if Box.mine_clicked:
            if self.clicked and self.value == -1:
                self.image = pygame.image.load(os.path.join("sounds_and_images\\minesweeper", "mineClicked.png"))

            elif self.flag and self.value != -1:
                self.image = pygame.image.load(os.path.join("sounds_and_images\\minesweeper", "mineFalse.png"))
            
            elif not self.clicked and self.value == -1:
                self.image = pygame.image.load(os.path.join("sounds_and_images\\minesweeper\\mine.png"))            

        else:
            if self.flag:
                self.image = pygame.image.load(os.path.join("sounds_and_images\\minesweeper\\flag.png"))

            if not self.clicked and not self.flag:
                self.image = pygame.image.load(os.path.join("sounds_and_images\\minesweeper\\Grid.png"))

            if self.clicked and not self.flag:
                if self.value > 0:
                    self.image = pygame.image.load(os.path.join(f"sounds_and_images\\minesweeper\\grid{self.value}.png"))
                elif self.value == 0:
                    self.image = pygame.image.load(os. path.join("sounds_and_images\\minesweeper\\empty.png"))
            
        self.image = pygame.transform.scale(self.image, (box_lenght, box_lenght))

    def draw(self):
        '''funzione che disegna l'immagine sullo schermo, senza aggiornarlo'''
        WIN.blit(self.image, self.rect)




def check_win(box_dict):
    '''verifica se l'utente ha vinto'''

    if not Box.mine_clicked:
        for box in box_dict.values():
            if box.value != -1 and not box.clicked:
                return False
        return True



def draw_WIN(time, box_dict):
    '''gestisce l'aspetto grafico della finestra ad esclusione dei box (per cui vi sono le apposite funzioni) e aggiorna lo schermo'''

    #rettangolo in cui si trovano il conteggio delle mine, lo smile e il timer
    container = pygame.image.load(os.path.join("sounds_and_images\\minesweeper\\container.png"))
    WIN.blit(container, (0,0))


    if Box.mine_clicked:
        smile.image = pygame.image.load(os.path.join("sounds_and_images\\minesweeper", "lost_grid.png"))

        you_lost_text = FONT.render('You   lost!', False, WHITE)

        pygame.draw.rect(WIN, BACKGROUND, (290, 300, 320, 100))
        WIN.blit(you_lost_text, (WIDTH/2 - you_lost_text.get_width()//2, HEIGHT/2 - you_lost_text.get_height()//2))
        pygame.draw.rect(WIN, WHITE, (290, 300, 320, 100), 4, 4)

    elif check_win(box_dict):
        smile.image = pygame.image.load(os.path.join('sounds_and_images\\minesweeper', 'eyeglass_grid.png'))

        you_won_text = FONT.render('You   won!', False, WHITE)

        pygame.draw.rect(WIN, BACKGROUND, (290, 300, 320, 100))
        WIN.blit(you_won_text, (WIDTH/2 - you_won_text.get_width()//2, HEIGHT/2 - you_won_text.get_height()//2))
        pygame.draw.rect(WIN, WHITE, (290, 300, 320, 100), 4, 4)

    else:
        smile.image = pygame.image.load(os.path.join("sounds_and_images\\minesweeper", "all grid.png"))


    smile.image = pygame.transform.scale(smile.image, (120, 120))
    WIN.blit(smile.image, smile.rect)


    # text_surf e mines_surf sono rispettivamente il timer e il numero di mine, a cui sono associati rect che vengono disegnati sullo schermo
    text_surf = NUM_FONT.render(f'{int(time)}', False, (230, 0, 0))
    mines_surf = NUM_FONT.render(f'{Box.num_mines}', False, (230, 0, 0))

    timer = pygame.draw.rect(WIN, (0,0,0), timer_rect)
    mines_rect1 = pygame.draw.rect(WIN, (0,0,0), mines_rect)

    WIN.blit(text_surf, (timer.right- text_surf.get_size()[0]-5, timer.y + 2))
    WIN.blit(mines_surf, (mines_rect1.right- mines_surf.get_size()[0]-5, mines_rect1.y + 2))

    pygame.display.flip()



def draw_start(start_group):
    '''disegna i rect di scelta della difficoltà, contenuti in start_group'''

    for sprite in start_group:

        image_width = sprite.image.get_width()
        image_height = sprite.image.get_height()

        WIN.blit(sprite.image, (sprite.rect.centerx - (image_width//2), sprite.rect.centery - (image_height//2)))        
        pygame.draw.rect(WIN, (WHITE), sprite.rect, 4, 4)        



def playing_setup(rows, columns, mines, box_lenght):
    '''crea i box di prato fiorito (per maggiori informazioni il procedimento è desccritto in calc_grid) ai quali sono associati elementi di una matrice,
    che saranno l'attributo self.value dei box'''

    box_dict = calc_grid(WIDTH, HEIGHT, box_lenght, rows, smiley_height)
    matrix, mine_location = crea_mat(rows, columns, mines)

    for key, rect in box_dict.items():
        i, j = key[0], key[1]
        box_dict[key] = Box(rect, matrix[i][j])

    for box in box_dict.values():
        box.update(box_lenght)
        box.draw()

    return box_dict, mine_location, matrix



def main(start_group):

    Box.mine_clicked = False
    time = 0

    init_time = False
    start = True
    done = False

    WIN.fill(BACKGROUND)

    while not done:

        clock.tick(30)

        while start:

            draw_start(start_group)

            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    start = False
                    done = True
                    pygame.quit()
                    sys.exit()

                elif ev.type == pygame.MOUSEBUTTONUP:
                    click = ev.button
                    if click == 1:
                        pos = pygame.mouse.get_pos()
                        for sprite in start_group:
                            if sprite.rect.collidepoint(pos):

                                rows, columns, mines, box_lenght = difficulty[sprite]
                                Box.num_mines = mines

                                WIN.fill(BACKGROUND)
                                box_dict, mine_location, matrix = playing_setup(rows, columns, mines, box_lenght)

                                start = False

                pygame.display.update()


        draw_WIN(time, box_dict)

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                    done = True

            if ev.type == pygame.MOUSEBUTTONUP:
                if not Box.mine_clicked and not check_win(box_dict):

                    for coordinates, box in box_dict.items():
                                
                        box.is_clicked(ev)

                        if box.clicked:
                            
                            #solo dopo il primo click il timer inizia a contare
                            init_time = True

                            if box.value == 0:
                                x = coordinates[0]
                                y = coordinates[1]
                                find_zeros(box_dict, matrix, [], x, y)
                    
                    #i box vengono aggiornati e ridisegnati
                    for box in box_dict.values():
                        box.update(box_lenght)
                        box.draw()

                if smile.rect.collidepoint(pygame.mouse.get_pos()):
                    done = True
                    main(start_group)


        if not check_win(box_dict) and not Box.mine_clicked and init_time:
            time += 1/30                          


if __name__ == '__main__':
    main(start_group)


pygame.quit()
sys.exit()