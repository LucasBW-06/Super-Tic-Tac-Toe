import pygame

# checa o vencedor de um tabuleiro 3x3
def check(jogo,id):
    for i in range(3):
        if all(jogo[i][j] == id for j in range(3)) or all(jogo[j][i] == id for j in range(3)):
            return 'V'
    if all(jogo[i][i] == id for i in range(3)) or all(jogo[i][2-i] == id for i in range(3)):
        return 'V'
    if all(jogo[i][j] != ' ' for i in range(3) for j in range(3)):
        return 'E'
    return 'F'

def game():
    table_sub = [[[[' ' for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)] #cria a tabela dos sub jogos
    table_prin = [[' ' for _ in range(3)] for _ in range(3)] #cria a tabela do jogo principal
    
    pygame.init()

    # define tamanho e nome da janela
    window = pygame.display.set_mode((700, 700))
    pygame.display.set_caption('Super Tic Tac Toe')

    # cria as fontes
    font_1 = pygame.font.SysFont('arial',35)
    font_2 = pygame.font.SysFont('arial',150)
    font_3 = pygame.font.SysFont('arial',100)

    pos_sel = 0 # define uma variável que será utilizada futuramente para determinar o tabuleiro selecionado

    x_and_o = {1:'X' , -1:'O'} # define lista com X e  O | também poderia ser uma lista: [None, 'X', 'O']
    turn = 1 # define a vez de quem vai jogar || 1 para X & -1 para O
 
    squares = [pygame.Rect(100 + (i // 9) * 55 + 5 * (i//9//3), 100 + (i % 9) * 55 + 5 * (i%9//3), 50, 50) for i in range(81)] # define quadrados do tabuleiro

    vic = '' # define o vencedor

    # loop do jogo
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # encerra o programa caso a janela do pygame seja fechada
                pygame.quit()
                return
            
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed() == (True, False, False): # detecta botão direito do mouse pressionado
                for i in range(81):
                    if (pos_sel == 0 or pos_sel == [i%9//3, i//9//3]) and squares[i].collidepoint(pygame.mouse.get_pos()) and table_sub[i%9//3][i//9//3][i%9%3][i//9%3] == ' ': # detecta o quadrado que foi clicado
                        table_sub[i%9//3][i//9//3][i%9%3][i//9%3] = x_and_o[turn] # add o X ou o O no quadrado clicado

                        # detecta se o jogador que acabou de jogar ganhou ou empatou o tabuleirinho
                        if check(table_sub[i%9//3][i//9//3],x_and_o[turn]) == 'V':
                            table_prin[i%9//3][i//9//3] = x_and_o[turn]
                        elif check(table_sub[i%9//3][i//9//3],x_and_o[turn]) == 'E':
                            table_prin[i%9//3][i//9//3] = ''

                        # detecta se o jogador que acabou de jogar ganhou ou empatou o tabuleiro principal
                        if check(table_prin,x_and_o[turn]) == 'V':
                            vic = x_and_o[turn]
                            playing = False
                        elif check(table_prin,x_and_o[turn]) == 'E':
                            vic = 'E'
                            playing = False

                        # troca a vez de quem vai jogar
                        turn *= -1
                        if table_prin[i%9%3][i//9%3] != ' ':
                            pos_sel = 0
                        else: 
                            pos_sel = [i%9%3, i//9%3]

        window.fill((255,255,255)) # preenche a tela de branco
        pygame.draw.rect(window,(0,0,0),(100,100,500,500)) # cria quadrado preto no centro da tela
        
        # desenha o tabuleiro principal e as posições preenchidas, caso tenham
        for i in range(9):
            rect = pygame.Rect((100 + (i//3) * 160 + (i//3) * 10,100 + (i%3) * 160 + (i%3) * 10,160,160))
            pygame.draw.rect(window,(255,255,255),rect)
            if table_prin[i%3][i//3] == 'X':
                render = font_2.render(table_prin[i%3][i//3],True,(150,0,0))
                window.blit(render, render.get_rect(center=rect.center))
            elif table_prin[i%3][i//3] == 'O':
                render = font_2.render(table_prin[i%3][i//3],True,(0,0,150))
                window.blit(render, render.get_rect(center=rect.center))

        # desenha os quadrados que podem ser jogados dos tabuleirinhos e as posições preenchidas, caso tenham
        for i in range(81):
            if table_prin[i%9//3][i//9//3] == ' ':
                if pos_sel != 0:
                    if i%9//3 == pos_sel[0] and i//9//3 == pos_sel[1]:
                        if squares[i].collidepoint(pygame.mouse.get_pos()):
                            pygame.draw.rect(window,(200,200,200),squares[i])
                        else:
                            pygame.draw.rect(window,(150,150,150),squares[i])
                    else:
                        pygame.draw.rect(window,(255,255,255),squares[i])
                else:
                    if squares[i].collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(window,(200,200,200),squares[i])
                    else:
                        pygame.draw.rect(window,(150,150,150),squares[i])

                pos = table_sub[i%9//3][i//9//3][i%9%3][i//9%3]
                if pos == 'X':
                    render = font_1.render(table_sub[i%9//3][i//9//3][i%9%3][i//9%3],True,(150,0,0))
                    window.blit(render, render.get_rect(center=squares[i].center))
                elif pos == 'O':
                    render = font_1.render(table_sub[i%9//3][i//9//3][i%9%3][i//9%3],True,(0,0,150))
                    window.blit(render, render.get_rect(center=squares[i].center))

        window.blit(font_3.render(x_and_o[turn],True,(151-151**(0.5-0.5*turn),0,151-151**(0.5+0.5*turn))), font_3.render(x_and_o[turn],True,(151-151**(0.5-0.5*turn),0,151-151**(0.5+0.5*turn))).get_rect(center=(350,50))) # escreve a vez de quem está jogando

        pygame.display.flip() # atualiza tela

    # pos jogo
    while not playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # encerra o programa caso a janela do pygame seja fechada
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN: # reinicia o jogo caso qualquer tecla seja precionada
                pygame.quit()
                game()
        window.fill((255,255,255)) # preenche tela de branco
        
        # exibe o vencedor ou se foi empate
        if vic != 'E':
            render = font_1.render(f'{vic} won!',True,(0,0,0))
        else:
            render = font_1.render('Draw!',True,(0,0,0))

        window.blit(render, render.get_rect(center=(350,330)))
        render = font_1.render('Click any key to play again', True, (0,0,0))
        
        window.blit(render, render.get_rect(center=(350,370)))
        pygame.display.flip() # atualiza tela
game()