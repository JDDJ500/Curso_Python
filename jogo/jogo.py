import pygame
import random
import sys
import math
import json
import os

# Inicialização
pygame.init()
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dark RPG - JDFN Edition")

# Configurações do sistema de salvamento
SAVE_FILE = "rpg_save.json"

# Cores para tema Dark Fantasy
DARK_BG = (20, 20, 25)
DARK_PANEL = (30, 30, 40)
DARK_ACCENT = (50, 50, 70)
DARK_TEXT = (200, 200, 210)
DARK_HIGHLIGHT = (70, 130, 180)
DARK_RED = (150, 40, 40)
DARK_GREEN = (40, 120, 60)
DARK_PURPLE = (80, 40, 120)
DARK_GOLD = (180, 150, 50)
DARK_SHADOW = (10, 10, 15)

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

# Sistema de Salvamento
def salvar_jogo():
    dados = {
        "vida": vida,
        "vida_max": vida_max,
        "mana": mana,
        "mana_max": mana_max,
        "nivel": nivel,
        "xp": xp,
        "xp_limite": xp_limite,
        "poções_vida": poções_vida,
        "poções_mana": poções_mana,
        "pontos_habilidade": pontos_habilidade,
        "dano_bonus": dano_bonus,
        "magia_bonus": magia_bonus,
        "dinheiro": dinheiro,
        "masmorras_desbloqueadas": masmorras_desbloqueadas
    }
    
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(dados, f, indent=4)
        return True
    except Exception as e:
        print(f"Erro ao salvar jogo: {e}")
        return False

def carregar_jogo():
    global vida, vida_max, mana, mana_max, nivel, xp, xp_limite
    global poções_vida, poções_mana, pontos_habilidade, dano_bonus
    global magia_bonus, dinheiro, masmorras_desbloqueadas
    
    try:
        if not os.path.exists(SAVE_FILE):
            return False
            
        with open(SAVE_FILE, "r") as f:
            dados = json.load(f)
        
        vida = dados.get("vida", 10)
        vida_max = dados.get("vida_max", 10)
        mana = dados.get("mana", 10)
        mana_max = dados.get("mana_max", 10)
        nivel = dados.get("nivel", 1)
        xp = dados.get("xp", 0)
        xp_limite = dados.get("xp_limite", 10)
        poções_vida = dados.get("poções_vida", 1)
        poções_mana = dados.get("poções_mana", 1)
        pontos_habilidade = dados.get("pontos_habilidade", 0)
        dano_bonus = dados.get("dano_bonus", 0)
        magia_bonus = dados.get("magia_bonus", 0)
        dinheiro = dados.get("dinheiro", 10)
        masmorras_desbloqueadas = dados.get("masmorras_desbloqueadas", 1)
        
        return True
    except Exception as e:
        print(f"Erro ao carregar jogo: {e}")
        return False

def resetar_jogador():
    global vida, vida_max, mana, mana_max, nivel, xp, xp_limite
    global poções_vida, poções_mana, pontos_habilidade, dano_bonus
    global magia_bonus, dinheiro, masmorras_desbloqueadas
    
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

# Funções de desenho
def draw_text(text, x, y, color=DARK_TEXT, font_type=medieval_font, shadow=True):
    if shadow:
        shadow_text = font_type.render(text, True, DARK_SHADOW)
        screen.blit(shadow_text, (x+2, y+2))
    main_text = font_type.render(text, True, color)
    screen.blit(main_text, (x, y))

def draw_panel(x, y, width, height):
    panel = pygame.Surface((width, height), pygame.SRCALPHA)
    panel.fill((*DARK_PANEL, 230))
    pygame.draw.rect(panel, DARK_GOLD, (0, 0, width, height), 3, border_radius=5)
    screen.blit(panel, (x, y))

def draw_tooltip(text, x, y):
    lines = text.split('\n')
    max_width = max(small_font.size(line)[0] for line in lines)
    height = len(lines) * small_font.get_height() + 12
    
    tooltip_x = min(x, WIDTH - max_width - 20)
    tooltip_y = max(y - height - 10, 10)
    
    tooltip_panel = pygame.Surface((max_width + 20, height), pygame.SRCALPHA)
    tooltip_panel.fill((*DARK_ACCENT, 240))
    pygame.draw.rect(tooltip_panel, DARK_GOLD, (0, 0, max_width + 20, height), 2, border_radius=4)
    
    for i, line in enumerate(lines):
        text_surf = small_font.render(line, True, DARK_TEXT)
        tooltip_panel.blit(text_surf, (10, 6 + i * small_font.get_height()))
    
    pygame.draw.polygon(screen, (*DARK_ACCENT, 240), [(x, y), (x-8, y-10), (x+8, y-10)])
    pygame.draw.polygon(screen, DARK_GOLD, [(x, y-1), (x-8, y-10), (x+8, y-10)], 1)
    
    screen.blit(tooltip_panel, (tooltip_x, tooltip_y))

def draw_button(text, x, y, w, h, base_color, hover_color, action=None, tooltip=None):
    mouse = pygame.mouse.get_pos()
    hover = x < mouse[0] < x + w and y < mouse[1] < y + h
    
    if hover:
        glow = pygame.Surface((w+20, h+20), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*hover_color, 30), (0, 0, w+20, h+20), border_radius=15)
        screen.blit(glow, (x-10, y-10))
    
    color = hover_color if hover else base_color
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=8)
    pygame.draw.rect(screen, DARK_GOLD, (x, y, w, h), 2, border_radius=8)
    
    text_surf = medieval_font.render(text, True, DARK_GOLD if hover else DARK_TEXT)
    text_rect = text_surf.get_rect(center=(x+w//2, y+h//2))
    
    if hover:
        text_shadow = medieval_font.render(text, True, (50, 40, 10))
        screen.blit(text_shadow, (text_rect.x+2, text_rect.y+2))
    
    screen.blit(text_surf, text_rect)
    
    if hover and tooltip:
        draw_tooltip(tooltip, mouse[0], mouse[1])
    
    if hover and pygame.mouse.get_pressed()[0] == 1 and action:
        pygame.time.delay(100)
        if action != quit_game:
            fade_transition(action)
        else:
            action()

def draw_stat_bar(x, y, width, height, value, max_value, color, bg_color, tooltip=None):
    ratio = min(value / max_value, 1)
    pygame.draw.rect(screen, bg_color, (x, y, width, height), border_radius=height//2)
    
    if ratio > 0:
        progress_width = int(width * ratio)
        progress_surface = pygame.Surface((progress_width, height), pygame.SRCALPHA)
        
        for i in range(progress_width):
            alpha = 150 + int(105 * (i / progress_width))
            shade = (min(color[0]+20, 255), min(color[1]+20, 255), min(color[2]+20, 255), alpha)
            pygame.draw.rect(progress_surface, shade, (i, 0, 1, height))
        
        if ratio < 0.3:
            pulse = int(10 * math.sin(pygame.time.get_ticks() / 200))
            pygame.draw.rect(progress_surface, (255, 255, 255, 30), (0, 0, progress_width, height), border_radius=height//2)
        
        screen.blit(progress_surface, (x, y))
    
    pygame.draw.rect(screen, DARK_GOLD, (x, y, width, height), 2, border_radius=height//2)
    
    if height > 20:
        stat_text = f"{value}/{max_value}"
        text_surf = small_font.render(stat_text, True, DARK_TEXT)
        screen.blit(text_surf, (x + width//2 - text_surf.get_width()//2, y - 20))
    
    mouse = pygame.mouse.get_pos()
    if (x < mouse[0] < x + width and y < mouse[1] < y + height) and tooltip:
        draw_tooltip(tooltip, mouse[0], mouse[1])

def create_dark_bg():
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill(DARK_BG)
    return bg

dark_bg = create_dark_bg()

# Funções de transição
def fade_transition(new_screen_func, fade_speed=10):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(DARK_BG)
    
    for alpha in range(0, 255, fade_speed):
        fade_surface.set_alpha(alpha)
        screen.blit(pygame.display.get_surface(), (0, 0))
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)
    
    new_screen_func()
    
    current_screen = pygame.display.get_surface().copy()
    for alpha in range(255, 0, -fade_speed):
        fade_surface.set_alpha(alpha)
        new_screen_func()
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)

# Telas do jogo
def menu_inicial():
    while True:
        screen.blit(dark_bg, (0, 0))
        
        title = "Dark RPG"
        title_x = WIDTH//2 - title_font.size(title)[0]//2
        
        for i in range(3, 0, -1):
            color = (DARK_GOLD[0]+i*20, DARK_GOLD[1]+i*10, DARK_GOLD[2]-i*10)
            draw_text(title, title_x - i, 100 - i, color, title_font, False)
        draw_text(title, title_x, 100, DARK_GOLD, title_font, False)
        
        draw_text("Uma Jornada Sombria", WIDTH//2 - medieval_font.size("Uma Jornada Sombria")[0]//2, 180, DARK_TEXT)
        
        draw_button("Novo Jogo", WIDTH//2 - 150, 300, 300, 60, DARK_ACCENT, DARK_HIGHLIGHT, 
                  lambda: [resetar_jogador(), fade_transition(game_screen)], "Comece uma nova aventura")
        
        if os.path.exists(SAVE_FILE):
            draw_button("Carregar Jogo", WIDTH//2 - 150, 380, 300, 60, DARK_ACCENT, DARK_PURPLE, 
                      lambda: [carregar_jogo(), fade_transition(game_screen)], "Continue sua jornada salva")
        
        draw_button("Sair", WIDTH//2 - 150, 460, 300, 60, DARK_ACCENT, DARK_RED, 
                  quit_game, "Abandonar o reino das trevas")
        
        pygame.draw.line(screen, DARK_GOLD, (WIDTH//2 - 180, 250), (WIDTH//2 + 180, 250), 2)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fade_transition(quit_game)

        pygame.display.update()

def game_screen():
    save_message = ""
    save_message_time = 0
    
    while True:
        screen.blit(dark_bg, (0, 0))
        
        draw_panel(50, 50, 400, 250)
        draw_text(f"Herói Nível {nivel}", 70, 70, DARK_GOLD)
        
        draw_stat_bar(70, 120, 360, 25, vida, vida_max, DARK_RED, (80, 20, 20), 
                    f"Vida: {vida}/{vida_max}\nSe chegar a 0, você morre!")
        draw_stat_bar(70, 170, 360, 25, mana, mana_max, DARK_HIGHLIGHT, (30, 60, 100), 
                    f"Mana: {mana}/{mana_max}\nNecessária para usar magias")
        
        draw_text("Progresso:", 70, 220, DARK_GOLD)
        draw_stat_bar(180, 220, 250, 15, xp, xp_limite, DARK_GOLD, DARK_ACCENT, 
                    f"XP: {xp}/{xp_limite}\nGanhe XP derrotando monstros")
        
        draw_text(f"💰 {dinheiro} peças de ouro", 70, 260, DARK_GOLD)
        
        draw_panel(500, 50, 450, 650)
        draw_text("Aventuras Disponíveis", 520, 70, DARK_GOLD)
        
        draw_button("Loja do Mercador", 520, 120, 400, 60, DARK_ACCENT, DARK_HIGHLIGHT, 
                   loja_screen, "Compre poções e equipamentos")
        draw_button("Entrar na Masmorra", 520, 200, 400, 60, DARK_ACCENT, DARK_RED, 
                   masmorra_screen, "Enfrente monstros para ganhar XP e ouro")
        draw_button("Habilidades", 520, 280, 400, 60, DARK_ACCENT, DARK_PURPLE, 
                   tela_arvore_habilidades, "Gaste pontos para melhorar suas habilidades")
        draw_button("Salvar Jogo", 520, 360, 400, 60, DARK_ACCENT, DARK_GOLD, 
                   lambda: [salvar_jogo(), set_save_message("Jogo Salvo!")], "Salve seu progresso atual")
        
        if pygame.time.get_ticks() - save_message_time < 2000:
            draw_text(save_message, 720, 370, DARK_GOLD, small_font)
        
        pygame.draw.line(screen, DARK_GOLD, (520, 100), (920, 100), 2)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if salvar_jogo():
                    fade_transition(quit_game)
                else:
                    fade_transition(quit_game)

        pygame.display.update()

def set_save_message(message):
    global save_message, save_message_time
    save_message = message
    save_message_time = pygame.time.get_ticks()

def loja_screen():
    while True:
        screen.blit(dark_bg, (0, 0))
        
        draw_panel(100, 50, 824, 668)
        draw_text("🏪 Loja do Mercador das Sombras", 150, 80, DARK_GOLD, title_font)
        
        draw_panel(150, 150, 350, 200)
        draw_text("Poção de Vida - 5💰", 170, 170, DARK_GOLD)
        draw_text("Restaura 5 pontos de vida", 170, 210, DARK_TEXT, small_font)
        draw_text(f"Disponível: {poções_vida}", 170, 240, DARK_TEXT, small_font)
        draw_button("Comprar", 170, 280, 120, 40, DARK_ACCENT, DARK_RED, 
                   comprar_pocao_vida, "Restaura 5 pontos de vida\nCusto: 5 peças de ouro")
        
        draw_panel(550, 150, 350, 200)
        draw_text("Poção de Mana - 5💰", 570, 170, DARK_GOLD)
        draw_text("Restaura 5 pontos de mana", 570, 210, DARK_TEXT, small_font)
        draw_text(f"Disponível: {poções_mana}", 570, 240, DARK_TEXT, small_font)
        draw_button("Comprar", 570, 280, 120, 40, DARK_ACCENT, DARK_HIGHLIGHT, 
                   comprar_pocao_mana, "Restaura 5 pontos de mana\nCusto: 5 peças de ouro")
        
        draw_panel(350, 400, 350, 200)
        draw_text(f"Seu Dinheiro: {dinheiro}💰", 370, 420, DARK_GOLD)
        draw_text("Volte quando tiver", 370, 460, DARK_TEXT, small_font)
        draw_text("mais ouro, aventureiro!", 370, 490, DARK_TEXT, small_font)
        
        draw_button("Voltar", 450, 630, 150, 50, DARK_ACCENT, DARK_GOLD, 
                   game_screen, "Voltar para a tela principal")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fade_transition(quit_game)

        pygame.display.update()

def comprar_pocao_vida():
    global poções_vida, dinheiro
    if dinheiro >= 5:
        poções_vida += 1
        dinheiro -= 5
        salvar_jogo()

def comprar_pocao_mana():
    global poções_mana, dinheiro
    if dinheiro >= 5:
        poções_mana += 1
        dinheiro -= 5
        salvar_jogo()

def tela_arvore_habilidades():
    def gastar_ponto(funcao):
        global pontos_habilidade
        if pontos_habilidade > 0:
            pontos_habilidade -= 1
            funcao()
            salvar_jogo()

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
        screen.blit(dark_bg, (0, 0))
        
        draw_panel(50, 50, 924, 668)
        draw_text("🌑 Árvore de Habilidades Obscuras", 100, 80, DARK_PURPLE, title_font)
        
        draw_panel(100, 150, 350, 200)
        draw_text("Vigor das Trevas", 120, 170, DARK_RED)
        draw_text("+2 Vida Máxima", 120, 210, DARK_TEXT, small_font)
        draw_text(f"Custo: 1 ponto", 120, 240, DARK_TEXT, small_font)
        draw_button("Aprender", 120, 280, 120, 40, DARK_ACCENT, DARK_RED, 
                  lambda: gastar_ponto(aumentar_vida), "Aumenta sua vida máxima em 2 pontos")
        
        draw_panel(550, 150, 350, 200)
        draw_text("Meditação Profana", 570, 170, DARK_HIGHLIGHT)
        draw_text("+2 Mana Máxima", 570, 210, DARK_TEXT, small_font)
        draw_text(f"Custo: 1 ponto", 570, 240, DARK_TEXT, small_font)
        draw_button("Aprender", 570, 280, 120, 40, DARK_ACCENT, DARK_HIGHLIGHT, 
                  lambda: gastar_ponto(aumentar_mana), "Aumenta sua mana máxima em 2 pontos")
        
        draw_panel(100, 400, 350, 200)
        draw_text("Força Maldita", 120, 420, (150, 40, 40))
        draw_text("+1 Dano Físico", 120, 460, DARK_TEXT, small_font)
        draw_text(f"Custo: 1 ponto", 120, 490, DARK_TEXT, small_font)
        draw_button("Aprender", 120, 530, 120, 40, DARK_ACCENT, (180, 60, 60), 
                  lambda: gastar_ponto(aumentar_dano), "Aumenta seu dano físico em 1 ponto")
        
        draw_panel(550, 400, 350, 200)
        draw_text("Poder Arcano Negro", 570, 420, DARK_PURPLE)
        draw_text("+1 Dano Mágico", 570, 460, DARK_TEXT, small_font)
        draw_text(f"Custo: 1 ponto", 570, 490, DARK_TEXT, small_font)
        draw_button("Aprender", 570, 530, 120, 40, DARK_ACCENT, (120, 60, 150), 
                  lambda: gastar_ponto(aumentar_magia), "Aumenta seu dano mágico em 1 ponto")
        
        draw_panel(350, 620, 350, 80)
        draw_text(f"Pontos Disponíveis: {pontos_habilidade}", 370, 640, DARK_GOLD)
        
        draw_button("Voltar", 450, 720, 150, 50, DARK_ACCENT, DARK_GOLD, 
                  game_screen, "Voltar para a tela principal")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fade_transition(quit_game)

        pygame.display.update()

def masmorra_screen():
    global vida

    masmorras = [
        {
            "nome": "Caverna dos Condenados",
            "monstros": [
                {"nome": "Ladrão de Almas", "vida": 10, "xp": random.randint(4, 6), "dano": (2, 4), "dinheiro": random.randint(5, 8)},
                {"nome": "Slime Sombrio", "vida": 6, "xp": random.randint(3, 5), "dano": (1, 3), "dinheiro": random.randint(3, 5)},
                {"nome": "Zumbi Renegado", "vida": 8, "xp": random.randint(4, 7), "dano": (2, 5), "dinheiro": random.randint(4, 7)},
            ],
            "nivel_requerido": 1,
            "cor": DARK_GREEN
        },
        {
            "nome": "Castelo das Almas Perdidas",
            "monstros": [
                {"nome": "Cavaleiro Negro", "vida": 15, "xp": random.randint(8, 12), "dano": (4, 6), "dinheiro": random.randint(8, 12)},
                {"nome": "Feiticeiro Maldito", "vida": 12, "xp": random.randint(7, 10), "dano": (3, 5), "dinheiro": random.randint(7, 10)},
                {"nome": "Gárgula da Tormenta", "vida": 18, "xp": random.randint(10, 14), "dano": (5, 7), "dinheiro": random.randint(10, 14)},
            ],
            "nivel_requerido": 5,
            "cor": DARK_PURPLE
        },
        {
            "nome": "Abismo do Pesadelo",
            "monstros": [
                {"nome": "Dragão das Trevas", "vida": 25, "xp": random.randint(15, 20), "dano": (7, 10), "dinheiro": random.randint(15, 20)},
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
            screen.blit(dark_bg, (0, 0))
            
            draw_panel(100, 50, 824, 668)
            draw_text("Portais para Masmorras", 150, 80, DARK_GOLD, title_font)
            draw_text(f"Masmorras Desbloqueadas: {masmorras_desbloqueadas}/3", 150, 120, DARK_TEXT, small_font)
            
            y_pos = 180
            for i, masmorra in enumerate(masmorras):
                if i < masmorras_desbloqueadas:
                    draw_panel(150, y_pos, 724, 100)
                    
                    if nivel >= masmorra["nivel_requerido"]:
                        draw_text(f"{masmorra['nome']} (Nível {masmorra['nivel_requerido']}+)", 170, y_pos+20, masmorra["cor"])
                        draw_button("Entrar", 750, y_pos+30, 100, 40, DARK_ACCENT, masmorra["cor"], 
                                  lambda m=masmorra: entrar_masmorra(m), f"Explore {masmorra['nome']}")
                    else:
                        draw_text(f"{masmorra['nome']} - Nível {masmorra['nivel_requerido']} requerido", 170, y_pos+20, DARK_TEXT)
                        draw_text("Você ainda não é forte o suficiente", 170, y_pos+50, DARK_TEXT, small_font)
                else:
                    draw_panel(150, y_pos, 724, 80)
                    draw_text(f"{masmorra['nome']} - Desbloqueie no nível {masmorra['nivel_requerido']}", 170, y_pos+20, DARK_TEXT)
                    draw_text("Continue progredindo para desbloquear", 170, y_pos+50, DARK_TEXT, small_font)
                
                y_pos += 120
            
            draw_button("Voltar", 450, y_pos+20, 150, 50, DARK_ACCENT, DARK_GOLD, 
                      game_screen, "Voltar para a tela principal")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fade_transition(quit_game)

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
                salvar_jogo()
                pygame.time.wait(1500)
                selecionar_masmorra()

            if vida <= 0:
                fade_transition(game_over)

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
                    salvar_jogo()
                    pygame.time.wait(1500)
                    selecionar_masmorra()

                if vida <= 0:
                    fade_transition(game_over)
            else:
                log = "Mana insuficiente!"

        def usar_pocao_vida():
            global vida, poções_vida
            if poções_vida > 0:
                vida += 5
                if vida > vida_max:
                    vida = vida_max
                poções_vida -= 1
                salvar_jogo()

        def usar_pocao_mana():
            global mana, poções_mana
            if poções_mana > 0:
                mana += 5
                if mana > mana_max:
                    mana = mana_max
                poções_mana -= 1
                salvar_jogo()

        while True:
            screen.blit(dark_bg, (0, 0))
            
            draw_panel(100, 50, 824, 668)
            draw_text(f"{masmorra['nome']}", 150, 80, masmorra["cor"], title_font)
            
            draw_panel(150, 150, 350, 200)
            draw_text(f"Monstro: {nome_monstro}", 170, 170, DARK_GOLD)
            draw_text(f"Vida: {vida_monstro}", 170, 210, DARK_TEXT)
            
            draw_panel(550, 150, 350, 200)
            draw_text("Seu Status", 570, 170, DARK_GOLD)
            draw_text(f"HP: {vida}/{vida_max}", 570, 210, DARK_RED)
            draw_text(f"Mana: {mana}/{mana_max}", 570, 240, DARK_HIGHLIGHT)
            draw_text(f"Poções: ❤️{poções_vida} 🔵{poções_mana}", 570, 270, DARK_TEXT, small_font)
            
            if log:
                draw_panel(150, 370, 724, 80)
                draw_text(log, 170, 390, DARK_RED, small_font)
            
            draw_button("Atacar", 150, 470, 200, 60, DARK_ACCENT, DARK_RED, atacar_monstro, "Ataque físico básico")
            draw_button("Magia (-5 mana)", 150, 550, 200, 60, DARK_ACCENT, DARK_HIGHLIGHT, usar_magia, "Ataque mágico poderoso")
            draw_button("Poção de Vida", 400, 470, 200, 60, DARK_ACCENT, (150, 40, 40), usar_pocao_vida, "Restaura 5 pontos de vida")
            draw_button("Poção de Mana", 400, 550, 200, 60, DARK_ACCENT, (40, 80, 150), usar_pocao_mana, "Restaura 5 pontos de mana")
            draw_button("Fugir", 650, 470, 200, 60, DARK_ACCENT, DARK_GOLD, selecionar_masmorra, "Voltar para seleção de masmorra")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fade_transition(quit_game)

            pygame.display.update()

    selecionar_masmorra()

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
    
    salvar_jogo()

def game_over():
    global vida, mana, dinheiro
    dinheiro_perdido = dinheiro // 2
    
    while True:
        screen.fill(DARK_BG)
        
        draw_panel(WIDTH//2 - 250, HEIGHT//2 - 200, 500, 400)
        draw_text("☠️ VOCÊ MORREU ☠️", WIDTH//2 - title_font.size("☠️ VOCÊ MORREU ☠️")[0]//2, HEIGHT//2 - 150, DARK_RED, title_font)
        draw_text("Sua jornada chegou ao fim...", WIDTH//2 - medieval_font.size("Sua jornada chegou ao fim...")[0]//2, HEIGHT//2 - 80, DARK_TEXT)
        draw_text(f"Perdeu {dinheiro_perdido}💰", WIDTH//2 - medieval_font.size(f"Perdeu {dinheiro_perdido}💰")[0]//2, HEIGHT//2 - 40, DARK_GOLD)
        draw_text("Revive com metade dos recursos", WIDTH//2 - medieval_font.size("Revive com metade dos recursos")[0]//2, HEIGHT//2, DARK_TEXT, small_font)
        
        draw_button("Continuar", WIDTH//2 - 100, HEIGHT//2 + 80, 200, 60, DARK_ACCENT, DARK_GREEN, 
                  lambda: [resetar_jogador_apos_morte(dinheiro_perdido), fade_transition(game_screen)], "Voltar ao jogo com metade dos recursos")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fade_transition(quit_game)
        
        pygame.display.update()

def resetar_jogador_apos_morte(dinheiro_perdido):
    global vida, mana, dinheiro
    dinheiro -= dinheiro_perdido
    vida = max(1, vida_max // 2)
    mana = mana_max // 2
    salvar_jogo()

def quit_game():
    salvar_jogo()
    pygame.quit()
    sys.exit()

# Iniciar o jogo
if __name__ == "__main__":
    fade_transition(menu_inicial, fade_speed=5)