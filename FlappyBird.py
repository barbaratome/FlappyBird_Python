import pygame
import os
import random
import time
#CONSTANTES (NORMALMENTE DEFINIDAS EM LETRA MAIÚSCULA)
TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]
# FONTE DA TELA (PONTOS)
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('Montserrat', 50)


class Passaro:
    IMGS = IMAGENS_PASSARO
# ANIMAÇÃO DE ROTAÇÃO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5
# ATRIBUTOS DO PASSARO DE COMO ELE INICIA
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

# A VELOCIDADE DE PULAR (PRA CIMA) EIXO Y É -10 POR CAUSA DA BIBLIOTECA PYGAMES 
    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

# CALCULAR O DESLOCAMENTO
    def mover(self):
        self.tempo += 1
## USA A FORMULA DE ACELERAÇÃO (SORTEVÃO KKK) S = so + vot + at(ao quadrado)/2        
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

# RESTRINGIR O DESLOCAMENTO
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

# DEFINIR O ANGULO DO PASSARO DE ACORDO COM A POSIÇÃO DELE (SUBINDO OU CAINDO) É APENAS A ANIMAÇÃO
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

# FUNÇÃO ONDE VAI DEFINIR A IMAGEM DO PASSARO, PRA PARECER QUE ELE TA BATENDO A ASA
    def desenhar(self, tela):
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0


# SE O PASSARO TIVER CAINDO A ASA PARA DE BATER
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

# ROTACIONAR A IMAGEM DO PASSARO, PRA ELE TER MAIS MOVIMENTO
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)
# DIVIDE A IMAGEM EM VARIOS PIXELS PARA SABER EXATAMENTE ONDE ESTA O PASSARO, COM AS CURVAS ETC.. FUNÇÃO DO PYGAMES (DOCUMENTAÇÃO)
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5
# FUNÇÃO PARA INICIAR
    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))
# BOOL PRA VER SE EXISTE UM PONTO DE COLISAO COM O PASSARO
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE
# MOVIMENTANDO O CHAO (CRIADO DOIS CHAO PARA UM IR TOMANDO LUGAR DO OUTRO E NAO DEIXAR A TELA VAZIA)
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

#FUNÇÃO AUXILIAR PARA DESENHAR A TELA
def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros: #ESTA DENTRO DO FOR PORQUE TEMA OPÇÃO DE TER VARIOS PASSAROS NA TELA
        passaro.desenhar(tela) # SE FOSSE SÓ UM (SERIA SÓ ESSA LINHA.)
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()


def main():
    passaros = [Passaro(230, 350)] # DEFININDO OS VALORES INICIAIS DE X E Y
    chao = Chao(730) # DEFININDO OS VALORES INICIAIS DE X 
    canos = [Cano(700)] # DEFININDO OS VALORES INICIAIS DE X 
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    jogo_iniciado = False
    delay_inicial = True

    while rodando:
        relogio.tick(30)
# INTERAÇÃO COM O USUARIO (CLICAR O MOUSE POR EXEMPLO) FUNÇÃO DA BIBLIOTECA PYGAME
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and jogo_iniciado:
                    for passaro in passaros:
                        passaro.pular()
                elif evento.key == pygame.K_SPACE and not jogo_iniciado:
                    jogo_iniciado = True
                    delay_inicial = False

        if not jogo_iniciado:
            if not delay_inicial:
                tela.blit(IMAGEM_BACKGROUND, (0, 0))
                texto_inicio = FONTE_PONTOS.render("Pressione ESPAÇO para iniciar", 1, (255, 255, 255))
                tela.blit(texto_inicio, (TELA_LARGURA // 2 - texto_inicio.get_width() // 2, TELA_ALTURA // 2))
            else:
                tela.blit(IMAGEM_BACKGROUND, (0, 0))
                texto_inicio = FONTE_PONTOS.render("Prepare-se!", 1, (255, 255, 255))
                tela.blit(texto_inicio, (TELA_LARGURA // 2 - texto_inicio.get_width() // 2, TELA_ALTURA // 2))
                pygame.display.update()
                time.sleep(3)
                delay_inicial = False
        else:
            for passaro in passaros:
                passaro.mover()
            chao.mover()

            adicionar_cano = False
            remover_canos = []
            for cano in canos:
                for i, passaro in enumerate(passaros):
                    if cano.colidir(passaro):
                        passaros.pop(i)
                        jogo_iniciado = False
                    if not cano.passou and passaro.x > cano.x:
                        cano.passou = True
                        adicionar_cano = True
                cano.mover()
                if cano.x + cano.CANO_TOPO.get_width() < 0:
                    remover_canos.append(cano)

            if adicionar_cano:
                pontos += 1
                canos.append(Cano(600))
            for cano in remover_canos:
                canos.remove(cano)

            for i, passaro in enumerate(passaros):
                if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                    passaros.pop(i)

            desenhar_tela(tela, passaros, canos, chao, pontos)

if __name__ == '__main__':
    pygame.init()
    main()
