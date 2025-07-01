import pygame
import random
import sys

##para fechar o jogo depois de rodar, clicar na tecla EXIT
###NÃO RODA EM IOS

pygame.init()

#  carrega os sons
som_aviso = pygame.mixer.Sound(r'Assets/Audio/notificacao.mp3')
som_beep = pygame.mixer.Sound(r'Assets/Audio/beep.mp3')
som_beep.set_volume(0.1)
som_musica = pygame.mixer.Sound(r'Assets/Audio/musicaMistica.mp3')

pygame.mixer.music.load(r'Assets/Audio/musicaMistica.mp3')
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1, 0.0)

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Navio Cata Moedas!!!")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 36)
MOEDA_TAMANHO = (10, 20)

# Carregar fundos para cada fase
fundo_bosque  = pygame.transform.smoothscale(pygame.image.load(r'Assets/fundoBosque.png').convert_alpha(), (WIDTH, HEIGHT))
fundo_casa    = pygame.transform.smoothscale(pygame.image.load(r'Assets/fundoEntrada.png').convert_alpha(), (WIDTH, HEIGHT))
fundo_varanda = pygame.transform.smoothscale(pygame.image.load(r'Assets/fundoVaranda2.png').convert_alpha(), (WIDTH, HEIGHT))

def get_background(nivel):
    if nivel == 1:
        return fundo_bosque
    elif nivel == 2:
        return fundo_casa
    elif nivel == 3:
        return fundo_varanda
    else:
        return fundo_bosque

barco_sprite_img = pygame.image.load(r'Assets\PNG\bruxa.png.png').convert_alpha()
barco_sprite_img = pygame.transform.smoothscale(barco_sprite_img, (160, 210))

def configurar_dificuldade(nivel):
    if nivel == 1:
        return 15, 2, 3
    elif nivel == 2:
        return 15, 2, 3
    elif nivel == 3:
        return 35, 4, 6
    else:
        return 15, 2, 3

def load_animation_frames(prefix, total_frames=10, tamanho=MOEDA_TAMANHO):
    frames = []
    for i in range(1, total_frames + 1):
        filename = f'{prefix}_{i}.png'
        image = pygame.image.load(filename).convert_alpha()
        image = pygame.transform.smoothscale(image, tamanho)
        frames.append(image)
    return frames

ouro_sprite = pygame.image.load(r'Assets/PNG/moedas/magiaRoxa.png').convert_alpha()
prata_sprite = pygame.image.load(r'Assets/PNG/moedas/magiaVerde.png').convert_alpha()
bronze_sprite = pygame.image.load(r'Assets/PNG/moedas/magiaRosa.png').convert_alpha()
ouro_sprite = pygame.transform.smoothscale(ouro_sprite, (80.5, 100))
prata_sprite = pygame.transform.smoothscale(prata_sprite, (80.5, 100))
bronze_sprite = pygame.transform.smoothscale(bronze_sprite, (80.5, 100))

VALOR_MOEDAS = {'ouro': 10, 'prata': 5, 'bronze': 1}



class Moeda(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        self.tipo = tipo
        self.image = {'ouro': ouro_sprite, 'prata': prata_sprite, 'bronze': bronze_sprite}[tipo]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.uniform(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-50, -10)
            self.speed = random.uniform(2, 5)

class Barco(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.transform.smoothscale(
            pygame.image.load(r'Assets/PNG/bruxa.png.png').convert_alpha(), (160, 210)
        )
        self.image = self.original_image
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 100))
        self.speed = 8
        self.carga = 0
        self.max_carga = 150
        self.facing_left = False

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if not self.facing_left:
                self.image = pygame.transform.flip(self.original_image, True, False)
                self.facing_left = True
        elif keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.facing_left:
                self.image = pygame.transform.flip(self.original_image, False, False)
                self.facing_left = False

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def voltar_ao_porto(self):
        self.rect.midbottom = (WIDTH // 2, HEIGHT - 1)

nivel = 1
qtd_moedas, v_min, v_max = configurar_dificuldade(nivel)
moedas = pygame.sprite.Group()
em_descarga = False
tempo_descarga = 0
pontos = 0
mensagem_fase = ""
tempo_mensagem = 0


for _ in range(qtd_moedas):
    tipo = random.choice(['ouro', 'prata', 'bronze'])
    x = random.randint(0, WIDTH - 20)
    y = random.randint(-100, -10)
    moedas.add(Moeda(x, y, tipo))

barco = Barco()

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    keys = pygame.key.get_pressed()

    if not em_descarga and barco.carga >= barco.max_carga:
        som_aviso.play()
        moedas_no_ceu = [m for m in moedas if m.rect.y < HEIGHT / 2]
        while moedas_no_ceu:
            moedas.remove(moedas_no_ceu.pop())
            pontos = max(0, pontos - 10)
        em_descarga = True
        tempo_descarga = pygame.time.get_ticks()

    if em_descarga:
        barco.voltar_ao_porto()
        if pygame.time.get_ticks() - tempo_descarga > 1000:
            barco.carga = 0
            em_descarga = False
        screen.blit(get_background(nivel), (0, 0))
        moedas.draw(screen)
        screen.blit(barco.image, barco.rect)
        screen.blit(FONT.render(f'Magias: {barco.carga}/{barco.max_carga}', True, (255, 255, 255)), (10, 10))
        screen.blit(FONT.render(f'Nível: {nivel}', True, (255, 255, 255)), (10, 50))
        pygame.display.flip()
        continue

    barco.update(keys)
    moedas.update()

    colisoes = pygame.sprite.spritecollide(barco, moedas, True)
    for moeda in colisoes:
        barco.carga += VALOR_MOEDAS[moeda.tipo]
        som_beep.play()
        pontos += 1

    while len(moedas) < qtd_moedas:
        tipo = random.choice(['ouro', 'prata', 'bronze'])
        x = random.randint(0, WIDTH - 20)
        y = random.randint(-100, -10)
        moedas.add(Moeda(x, y, tipo))

    screen.blit(get_background(nivel), (0, 0))
    score_surface = FONT.render(f"Pontos: {pontos}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 80))
    moedas.draw(screen)
    screen.blit(barco.image, barco.rect)
    screen.blit(FONT.render(f'Magias: {barco.carga}/{barco.max_carga}', True, (255, 255, 255)), (10, 10))
    screen.blit(FONT.render(f'Nível: {nivel}', True, (255, 255, 255)), (10, 50))

    if barco.carga >= barco.max_carga:
        nivel += 1
        if nivel > 3:
            nivel = 3
        qtd_moedas, v_min, v_max = configurar_dificuldade(nivel)

        # Exibir mensagem da nova fase
    if nivel == 2:
        mensagem_fase = "Parabéns! Você entrou na Cabana da Bruxa."
    elif nivel == 3:
        mensagem_fase = "Você chegou até a Varanda Encantada!"
    else:
        mensagem_fase = ""

    tempo_mensagem = pygame.time.get_ticks()  # Salva o tempo de início da mensagem

    qtd_moedas, v_min, v_max = configurar_dificuldade(nivel)

    # Mostrar mensagem de fase com contorno preto por 3 segundos
    if mensagem_fase:
        tempo_passado = pygame.time.get_ticks() - tempo_mensagem
        if tempo_passado < 1000:  # Mostra por 3 segundos
            cor_texto = (255, 255, 0)  # ou (255, 255, 255) para branco
            cor_contorno = (0, 0, 0)

            texto_msg = FONT.render(mensagem_fase, True, cor_texto)
            texto_rect = texto_msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))

            for dx in [-2, 0, 2]:
                for dy in [-2, 0, 2]:
                    if dx != 0 or dy != 0:
                        contorno = FONT.render(mensagem_fase, True, cor_contorno)
                        screen.blit(contorno, texto_rect.move(dx, dy))

            screen.blit(texto_msg, texto_rect)
        else:
            mensagem_fase = ""  # Limpa a mensagem após 3 segundos

    pygame.display.flip()

pygame.quit()
sys.exit()