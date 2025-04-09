import pygame
import random
import sys
import math

# Inicialização
pygame.init()
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG do JDFN")

# Cores para tema RPG
PARCHMENT = (240, 228, 196)
DARK_PARCHMENT = (210, 198, 166)
DARK_BROWN = (101, 67, 33)
GOLD = (212, 175, 55)
RED = (139, 0, 0)
DARK_RED = (100, 0, 0)
BLUE = (65, 105, 225)
DARK_BLUE = (25, 25, 112)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 80, 0)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fontes
try:
    title_font = pygame.font.Font(None, 48)
    medieval_font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 24)
    title_font.set_bold(True)
    medieval_font.set_bold(True)
except:
    title_font = pygame.font.SysFont("timesnewroman", 48, True)
    medieval_font = pygame.font.SysFont("timesnewroman", 32, True)
    small_font = pygame.font.SysFont("timesnewroman", 24)

# Variáveis do jogador
vida = 10
vida_max = 10
mana = 10
mana_max = 10
nivel = 1
xp = 0
xp_limite = 10
poções_vida = 1
poções_mana = 1
pontos_habilidade = 0
dano_bonus = 0
magia_bonus = 0
dinheiro = 10
masmorras_desbloqueadas = 1

# Funções de desenho aprimoradas
def draw_text(text, x, y, color=BLACK, font_type=medieval_font, shadow=True):
    if shadow:
        shadow_text = font_type.render(text, True, DARK_BROWN)
        screen.blit(shadow_text, (x+2, y+2))
    main_text = font_type.render(text, True, color)
    screen.blit(main_text, (x, y))

def draw_panel(x, y, width, height):
    panel = pygame.Surface((width, height), pygame.SRCALPHA)
    panel.fill((*PARCHMENT, 240))
    pygame.draw.rect(panel, DARK_BROWN, (0, 0, width, height), 3)
    screen.blit(panel, (x, y))
    pygame.draw.line(screen, GOLD, (x+5, y+5), (x+20, y+5), 2)
    pygame.draw.line(screen, GOLD, (x+5, y+5), (x+5, y+20), 2)
    pygame.draw.line(screen, GOLD, (x+width-5, y+5), (x+width-20, y+5), 2)
    pygame.draw.line(screen, GOLD, (x+width-5, y+5), (x+width-5, y+20), 2)
    pygame.draw.line(screen, GOLD, (x+5, y+height-5), (x+20, y+height-5), 2)
    pygame.draw.line(screen, GOLD, (x+5, y+height-5), (x+5, y+height-20), 2)
    pygame.draw.line(screen, GOLD, (x+width-5, y+height-5), (x+width-20, y+height-5), 2)
    pygame.draw.line(screen, GOLD, (x+width-5, y+height-5), (x+width-5, y+height-20), 2)

def draw_button(text, x, y, w, h, base_color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h), 0, 10)
        pygame.draw.rect(screen, GOLD, (x, y, w, h), 3, 10)
        if click[0] == 1 and action:
            pygame.time.delay(100)
            action()
    else:
        pygame.draw.rect(screen, base_color, (x, y, w, h), 0, 10)
        pygame.draw.rect(screen, DARK_BROWN, (x, y, w, h), 3, 10)
    
    draw_text(text, x + w//2 - medieval_font.size(text)[0]//2, 
             y + h//2 - medieval_font.size(text)[1]//2, GOLD)

def draw_stat_bar(x, y, width, height, value, max_value, color, bg_color):
    ratio = min(value / max_value, 1)
    pygame.draw.rect(screen, bg_color, (x, y, width, height), 0, height//2)
    
    if ratio > 0:
        for i in range(int(width * ratio)):
            alpha = 200 + int(55 * (i / (width * ratio)))
            shade = (min(color[0]+20, 255), min(color[1]+20, 255), min(color[2]+20, 255))
            pygame.draw.rect(screen, shade, (x + i, y, 1, height))
    
    pygame.draw.rect(screen, DARK_BROWN, (x, y, width, height), 2, height//2)
    
    if height > 20:
        stat_text = f"{value}/{max_value}"
        draw_text(stat_text, x + width//2 - small_font.size(stat_text)[0]//2, 
                 y - 2, WHITE, small_font)

def create_parchment_bg():
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill(PARCHMENT)
    
    for i in range(0, WIDTH, 30):
        pygame.draw.circle(bg, DARK_BROWN, (i, 0), 5)
        pygame.draw.circle(bg, DARK_BROWN, (i, HEIGHT), 5)
    
    for i in range(0, HEIGHT, 30):
        pygame.draw.circle(bg, DARK_BROWN, (0, i), 5)
        pygame.draw.circle(bg, DARK_BROWN, (WIDTH, i), 5)
    
    return bg

parchment_bg = create_parchment_bg()

# Telas atualizadas
def menu_inicial():
    while True:
        screen.blit(parchment_bg, (0, 0))
        
        title = "RPG do JDFN"
        title_x = WIDTH//2 - title_font.size(title)[0]//2
        
        for i in range(3):
            draw_text(title, title_x - i, 100 - i, GOLD, title_font, False)
        draw_text(title, title_x, 100, DARK_BROWN, title_font, False)
        
        draw_text("Uma Jornada Épica", WIDTH//2 - medieval_font.size("Uma Jornada Épica")[0]//2, 180, DARK_BROWN)
        
        draw_button("Iniciar Jornada", WIDTH//2 - 150, 300, 300, 60, DARK_GREEN, GREEN, game_screen)
        draw_button("Sair", WIDTH//2 - 150, 400, 300, 60, DARK_RED, RED, quit_game)
        
        pygame.draw.line(screen, DARK_BROWN, (WIDTH//2 - 180, 250), (WIDTH//2 + 180, 250), 2)
        pygame.draw.line(screen, DARK_BROWN, (WIDTH//2 - 180, 480), (WIDTH//2 + 180, 480), 2)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.update()

def game_screen():
    while True:
        screen.blit(parchment_bg, (0, 0))
        
        draw_panel(50, 50, 400, 250)
        draw_text(f"Herói Nível {nivel}", 70, 70, DARK_BROWN)
        
        draw_stat_bar(70, 120, 360, 25, vida, vida_max, RED, DARK_RED)
        draw_stat_bar(70, 170, 360, 25, mana, mana_max, BLUE, DARK_BLUE)
        
        draw_text("Progresso:", 70, 220, DARK_BROWN)
        draw_stat_bar(180, 220, 250, 15, xp, xp_limite, GOLD, DARK_BROWN)
        
        draw_text(f"💰 {dinheiro} peças de ouro", 70, 260, DARK_BROWN)
        
        draw_panel(500, 50, 450, 650)
        draw_text("Aventuras Disponíveis", 520, 70, DARK_BROWN)
        
        draw_button("Loja do Mercador", 520, 120, 400, 60, DARK_GREEN, GREEN, loja_screen)
        draw_button("Entrar na Masmorra", 520, 200, 400, 60, DARK_RED, RED, masmorra_screen)
        draw_button("Habilidades", 520, 280, 400, 60, DARK_BLUE, BLUE, tela_arvore_habilidades)
        
        pygame.draw.line(screen, DARK_BROWN, (520, 100), (920, 100), 2)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.update()

def loja_screen():
    while True:
        screen.blit(parchment_bg, (0, 0))
        
        draw_panel(100, 50, 824, 668)
        draw_text("🏪 Loja do Mercador", 150, 80, DARK_BROWN, title_font)
        
        draw_panel(150, 150, 350, 200)
        draw_text("Poção de Vida - 5💰", 170, 170, DARK_BROWN)
        draw_text("Restaura 5 pontos de vida", 170, 210, BLACK, small_font)
        draw_text(f"Disponível: {poções_vida}", 170, 240, DARK_BROWN, small_font)
        draw_button("Comprar", 170, 280, 120, 40, DARK_RED, RED, comprar_pocao_vida)
        
        draw_panel(550, 150, 350, 200)
        draw_text("Poção de Mana - 5💰", 570, 170, DARK_BROWN)
        draw_text("Restaura 5 pontos de mana", 570, 210, BLACK, small_font)
        draw_text(f"Disponível: {poções_mana}", 570, 240, DARK_BROWN, small_font)
        draw_button("Comprar", 570, 280, 120, 40, DARK_BLUE, BLUE, comprar_pocao_mana)
        
        draw_panel(350, 400, 350, 200)
        draw_text(f"Seu Dinheiro: {dinheiro}💰", 370, 420, GOLD)
        draw_text("Volte quando tiver", 370, 460, DARK_BROWN, small_font)
        draw_text("mais ouro, aventureiro!", 370, 490, DARK_BROWN, small_font)
        
        draw_button("Voltar", 450, 630, 150, 50, DARK_BROWN, GOLD, game_screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.update()

def comprar_pocao_vida():
    global poções_vida, dinheiro
    if dinheiro >= 5:
        poções_vida += 1
        dinheiro -= 5

def comprar_pocao_mana():
    global poções_mana, dinheiro
    if dinheiro >= 5:
        poções_mana += 1
        dinheiro -= 5

def tela_arvore_habilidades():
    def gastar_ponto(funcao):
        global pontos_habilidade
        if pontos_habilidade > 0:
            pontos_habilidade -= 1
            funcao()

    def aumentar_vida():
        global vida_max
        vida_max += 2

    def aumentar_mana():
        global mana_max
        mana_max += 2

    def aumentar_dano():
        global dano_bonus
        dano_bonus += 1

    def aumentar_magia():
        global magia_bonus
        magia_bonus += 1

    while True:
        screen.blit(parchment_bg, (0, 0))
        
        draw_panel(50, 50, 924, 668)
        draw_text("🌿 Árvore de Habilidades", 100, 80, DARK_GREEN, title_font)
        
        draw_panel(100, 150, 350, 200)
        draw_text("Vigor", 120, 170, DARK_RED)
        draw_text("+2 Vida Máxima", 120, 210, BLACK, small_font)
        draw_text(f"Custo: 1 ponto", 120, 240, DARK_BROWN, small_font)
        draw_button("Aprender", 120, 280, 120, 40, DARK_RED, RED, lambda: gastar_ponto(aumentar_vida))
        
        draw_panel(550, 150, 350, 200)
        draw_text("Meditação", 570, 170, DARK_BLUE)
        draw_text("+2 Mana Máxima", 570, 210, BLACK, small_font)
        draw_text(f"Custo: 1 ponto", 570, 240, DARK_BROWN, small_font)
        draw_button("Aprender", 570, 280, 120, 40, DARK_BLUE, BLUE, lambda: gastar_ponto(aumentar_mana))
        
        draw_panel(100, 400, 350, 200)
        draw_text("Força Bruta", 120, 420, DARK_RED)
        draw_text("+1 Dano Físico", 120, 460, BLACK, small_font)
        draw_text(f"Custo: 1 ponto", 120, 490, DARK_BROWN, small_font)
        draw_button("Aprender", 120, 530, 120, 40, (100, 30, 30), RED, lambda: gastar_ponto(aumentar_dano))
        
        draw_panel(550, 400, 350, 200)
        draw_text("Poder Arcano", 570, 420, PURPLE)
        draw_text("+1 Dano Mágico", 570, 460, BLACK, small_font)
        draw_text(f"Custo: 1 ponto", 570, 490, DARK_BROWN, small_font)
        draw_button("Aprender", 570, 530, 120, 40, PURPLE, (200, 100, 200), lambda: gastar_ponto(aumentar_magia))
        
        draw_panel(350, 620, 350, 80)
        draw_text(f"Pontos Disponíveis: {pontos_habilidade}", 370, 640, GOLD)
        
        draw_button("Voltar", 450, 720, 150, 50, DARK_BROWN, GOLD, game_screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.update()

def masmorra_screen():
    global vida

    masmorras = [
        {
            "nome": "Caverna dos Iniciantes",
            "monstros": [
                {"nome": "Ladrão de Almas", "vida": 10, "xp": random.randint(4, 6), "dano": (2, 4), "dinheiro": random.randint(5, 8)},
                {"nome": "Slime Sangrento", "vida": 6, "xp": random.randint(3, 5), "dano": (1, 3), "dinheiro": random.randint(3, 5)},
                {"nome": "Zumbi Mutante", "vida": 8, "xp": random.randint(4, 7), "dano": (2, 5), "dinheiro": random.randint(4, 7)},
            ],
            "nivel_requerido": 1,
            "cor": DARK_GREEN
        },
        {
            "nome": "Castelo das Sombras",
            "monstros": [
                {"nome": "Cavaleiro Negro", "vida": 15, "xp": random.randint(8, 12), "dano": (4, 6), "dinheiro": random.randint(8, 12)},
                {"nome": "Feiticeiro Maldito", "vida": 12, "xp": random.randint(7, 10), "dano": (3, 5), "dinheiro": random.randint(7, 10)},
                {"nome": "Gárgula de Pedra", "vida": 18, "xp": random.randint(10, 14), "dano": (5, 7), "dinheiro": random.randint(10, 14)},
            ],
            "nivel_requerido": 5,
            "cor": PURPLE
        },
        {
            "nome": "Abismo Infernal",
            "monstros": [
                {"nome": "Dragão Jovem", "vida": 25, "xp": random.randint(15, 20), "dano": (7, 10), "dinheiro": random.randint(15, 20)},
                {"nome": "Demônio Menor", "vida": 20, "xp": random.randint(12, 18), "dano": (6, 9), "dinheiro": random.randint(12, 18)},
                {"nome": "Lich Renegado", "vida": 22, "xp": random.randint(14, 19), "dano": (8, 11), "dinheiro": random.randint(14, 19)},
            ],
            "nivel_requerido": 10,
            "cor": DARK_RED
        }
    ]

    def selecionar_masmorra():
        nonlocal masmorras
        while True:
            screen.blit(parchment_bg, (0, 0))
            
            draw_panel(100, 50, 824, 668)
            draw_text("Escolha sua Masmorra", 150, 80, DARK_BROWN, title_font)
            draw_text(f"Masmorras Desbloqueadas: {masmorras_desbloqueadas}/3", 150, 120, DARK_BROWN, small_font)
            
            y_pos = 180
            for i, masmorra in enumerate(masmorras):
                if i < masmorras_desbloqueadas:
                    draw_panel(150, y_pos, 724, 100)
                    
                    if nivel >= masmorra["nivel_requerido"]:
                        draw_text(f"{masmorra['nome']} (Nível {masmorra['nivel_requerido']}+)", 170, y_pos+20, masmorra["cor"])
                        draw_button("Entrar", 750, y_pos+30, 100, 40, masmorra["cor"], GREEN, lambda m=masmorra: entrar_masmorra(m))
                    else:
                        draw_text(f"{masmorra['nome']} - Nível {masmorra['nivel_requerido']} requerido", 170, y_pos+20, DARK_BROWN)
                        draw_text("Você ainda não é forte o suficiente", 170, y_pos+50, BLACK, small_font)
                else:
                    draw_panel(150, y_pos, 724, 80)
                    draw_text(f"{masmorra['nome']} - Desbloqueie no nível {masmorra['nivel_requerido']}", 170, y_pos+20, DARK_BROWN)
                    draw_text("Continue progredindo para desbloquear", 170, y_pos+50, BLACK, small_font)
                
                y_pos += 120
            
            draw_button("Voltar", 450, y_pos+20, 150, 50, DARK_BROWN, GOLD, game_screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

            pygame.display.update()

    def entrar_masmorra(masmorra):
        monstro = random.choice(masmorra["monstros"])
        vida_monstro = monstro["vida"]
        nome_monstro = monstro["nome"]
        xp_monstro = monstro["xp"]
        dano_monstro = monstro["dano"]
        dinheiro_monstro = monstro["dinheiro"]
        log = ""

        def atacar_monstro():
            nonlocal vida_monstro, log
            global vida, dinheiro

            dano_jogador = random.randint(3, 5) + dano_bonus
            vida_monstro -= dano_jogador
            log = f"Você causou {dano_jogador} de dano!"

            if vida_monstro > 0:
                dano_recebido = random.randint(*dano_monstro)
                vida -= dano_recebido
                log += f" | {nome_monstro} causou {dano_recebido} de dano em você!"

            if vida_monstro <= 0:
                ganhar_xp(xp_monstro)
                dinheiro += dinheiro_monstro
                log = f"Você derrotou {nome_monstro} e ganhou {xp_monstro} XP e {dinheiro_monstro}💰!"
                pygame.time.wait(1500)
                selecionar_masmorra()

            if vida <= 0:
                game_over()

        def usar_magia():
            nonlocal vida_monstro, log
            global mana, vida, dinheiro

            if mana >= 5:
                mana -= 5
                dano_magia = random.randint(6, 9) + magia_bonus
                vida_monstro -= dano_magia
                log = f"Você usou magia e causou {dano_magia} de dano!"

                if vida_monstro > 0:
                    dano_recebido = random.randint(*dano_monstro)
                    vida -= dano_recebido
                    log += f" | {nome_monstro} causou {dano_recebido} de dano!"

                if vida_monstro <= 0:
                    ganhar_xp(xp_monstro)
                    dinheiro += dinheiro_monstro
                    log = f"Você derrotou {nome_monstro} com magia e ganhou {xp_monstro} XP e {dinheiro_monstro}💰!"
                    pygame.time.wait(1500)
                    selecionar_masmorra()

                if vida <= 0:
                    game_over()
            else:
                log = "Mana insuficiente!"

        def usar_pocao_vida():
            global vida, poções_vida
            if poções_vida > 0:
                vida += 5
                if vida > vida_max:
                    vida = vida_max
                poções_vida -= 1

        def usar_pocao_mana():
            global mana, poções_mana
            if poções_mana > 0:
                mana += 5
                if mana > mana_max:
                    mana = mana_max
                poções_mana -= 1

        while True:
            screen.blit(parchment_bg, (0, 0))
            
            draw_panel(100, 50, 824, 668)
            draw_text(f"{masmorra['nome']}", 150, 80, masmorra["cor"], title_font)
            
            draw_panel(150, 150, 350, 200)
            draw_text(f"Monstro: {nome_monstro}", 170, 170, DARK_BROWN)
            draw_text(f"Vida: {vida_monstro}", 170, 210, BLACK)
            
            draw_panel(550, 150, 350, 200)
            draw_text("Seu Status", 570, 170, DARK_BROWN)
            draw_text(f"HP: {vida}/{vida_max}", 570, 210, RED)
            draw_text(f"Mana: {mana}/{mana_max}", 570, 240, BLUE)
            draw_text(f"Poções: ❤️{poções_vida} 🔵{poções_mana}", 570, 270, DARK_BROWN, small_font)
            
            if log:
                draw_panel(150, 370, 724, 80)
                draw_text(log, 170, 390, DARK_RED, small_font)
            
            draw_button("Atacar", 150, 470, 200, 60, DARK_RED, RED, atacar_monstro)
            draw_button("Magia (-5 mana)", 150, 550, 200, 60, DARK_BLUE, BLUE, usar_magia)
            draw_button("Poção de Vida", 400, 470, 200, 60, DARK_RED, RED, usar_pocao_vida)
            draw_button("Poção de Mana", 400, 550, 200, 60, DARK_BLUE, BLUE, usar_pocao_mana)
            draw_button("Fugir", 650, 470, 200, 60, DARK_BROWN, GOLD, selecionar_masmorra)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

            pygame.display.update()

    selecionar_masmorra()

def game_over():
    global vida, mana, dinheiro
    dinheiro_perdido = dinheiro // 2
    
    while True:
        screen.fill((70, 0, 0))
        
        draw_panel(WIDTH//2 - 250, HEIGHT//2 - 200, 500, 400)
        draw_text("☠️ GAME OVER ☠️", WIDTH//2 - title_font.size("☠️ GAME OVER ☠️")[0]//2, HEIGHT//2 - 150, DARK_RED, title_font)
        draw_text("Você foi derrotado!", WIDTH//2 - medieval_font.size("Você foi derrotado!")[0]//2, HEIGHT//2 - 80, BLACK)
        draw_text(f"Perdeu {dinheiro_perdido}💰", WIDTH//2 - medieval_font.size(f"Perdeu {dinheiro_perdido}💰")[0]//2, HEIGHT//2 - 40, GOLD)
        draw_text("Revive com metade dos recursos", WIDTH//2 - medieval_font.size("Revive com metade dos recursos")[0]//2, HEIGHT//2, BLACK, small_font)
        
        draw_button("Continuar", WIDTH//2 - 100, HEIGHT//2 + 80, 200, 60, DARK_GREEN, GREEN, lambda: resetar_jogador(dinheiro_perdido))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        
        pygame.display.update()

def resetar_jogador(dinheiro_perdido):
    global vida, mana, dinheiro
    dinheiro -= dinheiro_perdido
    vida = max(1, vida_max // 2)
    mana = mana_max // 2
    game_screen()

def ganhar_xp(qtd):
    global xp, xp_limite, nivel, vida, mana, pontos_habilidade, dinheiro, masmorras_desbloqueadas
    xp += qtd
    dinheiro += random.randint(3, 7)
    
    nivel_anterior = nivel
    while xp >= xp_limite:
        xp -= xp_limite
        nivel += 1
        vida = vida_max
        mana = mana_max
        pontos_habilidade += 1
        xp_limite = int(xp_limite * 1.1)
    
    if nivel >= 5 and masmorras_desbloqueadas < 2:
        masmorras_desbloqueadas = 2
    elif nivel >= 10 and masmorras_desbloqueadas < 3:
        masmorras_desbloqueadas = 3

def usar_pocao(tipo):
    global vida, mana, poções_vida, poções_mana
    if tipo == "vida" and poções_vida > 0 and vida < vida_max:
        vida += 5
        if vida > vida_max:
            vida = vida_max
        poções_vida -= 1
    elif tipo == "mana" and poções_mana > 0 and mana < mana_max:
        mana += 5
        if mana > mana_max:
            mana = mana_max
        poções_mana -= 1

def quit_game():
    pygame.quit()
    sys.exit()

# Iniciar o jogo
menu_inicial()