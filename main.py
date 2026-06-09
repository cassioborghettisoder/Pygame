import pygame
import random
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
from recursos.trabalho import calcular_nivel
import pyttsx3
engine = pyttsx3.init()

limpar_tela()
inicializarBancoDeDados()

resultado = maior_pontuador()
nome_maior = resultado[0]
maior_pontos = resultado[1]
dataJogada = resultado[2]
horaJogada = resultado[3] if len(resultado) > 3 else "00:00:00"
if nome_maior is None:
    nome_maior = "Nenhum"
    maior_pontos = 0
    dataJogada = "--/--/----"
    horaJogada = "--:--:--"
pygame.init()

while True:
    nome = input("Nickname: ")
    if len(nome) > 0: 
        break
    else:
        print("Nome Inválido!")
        
tamanho = (1000,700)
pygame.display.set_caption("Trabalho pensamento computacional")
icone  = pygame.image.load("bases/icone.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
branco = (255, 255, 255)
preto = (0, 0, 0)

fundo = pygame.image.load("bases/background.jpg")
fundoDead = pygame.image.load("bases/backgroundDead.jpg")
fundoStart = pygame.image.load("bases/backgroundStart.jpg")

iron = pygame.image.load("bases/IronMan.png")
iron = pygame.transform.scale(iron, (116,51))
missel = pygame.image.load("bases/missile.png")
missel = pygame.transform.scale(missel, (125,25))
missileSound = pygame.mixer.Sound("bases/missile.wav")
explosaoSound = pygame.mixer.Sound("bases/explosao.wav")
pygame.mixer.music.load("bases/ironsound.mp3")
fonteMenu = pygame.font.SysFont("comicsans",18)

def jogar():
    raioSol = 15
    pulsando = 1    
    decoX = random.randint(0, 700)
    decoY = random.randint(0, 150)
    decoVelX = random.choice([-2, -1, 1, 2])
    decoVelY = random.choice([-2, -1, 1, 2])
    fundoMov1 = 0
    fundoMov2 = 1129
    posicaoXPersona = 0
    posicaoYPersona = 60
    movimentoXPersona = 0   
    movimentoYPersona = 0
    velocidadeMovPersona = 3
    posicaoXMissel = 1000
    posicaoYMissel = random.randint(0,675)
    velocidadeMissel = 2
    pontos = 0
    pausado = False
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    dificuldade = 20
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
                movimentoXPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
                movimentoYPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                movimentoYPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = not pausado
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                quit()
        
        if movimentoXPersona != 0:
            posicaoXPersona = posicaoXPersona + movimentoXPersona
            movimentoYPersona = 0
        elif movimentoYPersona != 0:
            posicaoYPersona = posicaoYPersona + movimentoYPersona
            movimentoXPersona = 0
        
        if pausado:
            textoBig = fonteMenu.render("PAUSE", True, branco)
            tela.blit(textoBig, (475, 375))
            pygame.display.update()
            relogio.tick(60)
            continue    
    
          
        if posicaoXPersona < 0 :
            posicaoXPersona = 0
        elif posicaoXPersona > 884:
            posicaoXPersona = 884
        if posicaoYPersona < 0 :
            posicaoYPersona = 0
        elif posicaoYPersona > 649:
            posicaoYPersona = 649
            
            
        posicaoXMissel = posicaoXMissel - velocidadeMissel
        if posicaoXMissel < -125:
            pygame.mixer.Sound.play(missileSound)
            posicaoXMissel = 1000
            pontos = pontos + 1
            velocidadeMissel = velocidadeMissel + 1
            posicaoYMissel = random.randint(0,675)
                            
        tela.fill(branco)
        tela.blit(fundo, (fundoMov1,0) )
        tela.blit(fundo, (fundoMov2,0) )
        fundoMov1 -= 1
        fundoMov2 -= 1
        if fundoMov1 <= -1129:
            fundoMov1 = 1129
        elif fundoMov2 <= -1129:
            fundoMov2 = 1129
        
        
        tela.blit(iron, (posicaoXPersona,posicaoYPersona))
        tela.blit( missel, (posicaoXMissel, posicaoYMissel) )
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (700,15))
        
        nivel = calcular_nivel(pontos)
        textoNivel = fonteMenu.render("Nivel: "+nivel, True, branco)
        tela.blit(textoNivel, (680, 35))  

        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+116))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+51))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + 125))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + 25))
        if  len( list( set(pixelsMisselY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsMisselX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                escreverDados(nome, pontos)
                dead()
                
            else:
                print("Ainda Vivo, mas por pouco!")
        else:
            print("Ainda Vivo")
                # move o objeto decorativo
        decoX += decoVelX
        decoY += decoVelY

  
        if decoX <= 0 or decoX >= 995:
            decoVelX = -decoVelX
        if decoY <= 0 or decoY >= 695:
            decoVelY = -decoVelY

        raioSol += 0.05 * pulsando
        if raioSol >= 20:
            pulsando = -1
        elif raioSol <= 10:
            pulsando = 1
        pygame.draw.circle(tela, (255, 215, 0), (970, 20), int(raioSol))
        pygame.draw.circle(tela, (255, 215, 0), (decoX, decoY), 5)

        textoPause = fonteMenu.render("Press Space to Pause Game", True, branco)
        tela.blit(textoPause, (425, 670))
        pygame.display.update()
        relogio.tick(60)

def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    
    engine.say(f"Game over! Melhor pontuador: {nome_maior} com {maior_pontos} pontos")
    engine.runAndWait()

    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    startButton = pygame.Rect(10, 10, 150, 40)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                quit()
                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()

            
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        


        textoBest = fonteMenu.render(f"The Best: {nome_maior} - {maior_pontos} pts - {dataJogada} {horaJogada}", True, branco)
        tela.blit(textoBest, (10, 160)) 
        pygame.display.update()
        relogio.tick(60)


def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
        tela.fill(preto)
        tela.blit(fundoStart, (0, 0))  # reutiliza o mesmo fundo

        textoNome = fonteMenu.render(f"Bem-vindo, {nome}!", True, branco)
        tela.blit(textoNome, (10, 10))
        
        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        texto = fonteMenu.render(f"The Best - {nome_maior} - {maior_pontos} - {dataJogada} - {horaJogada}", True, preto)
        textoMecanica = fonteMenu.render("Use as setas para desviar dos misseis!", True, preto)
        tela.blit(textoMecanica, (10, 60))
        tela.blit(texto, (10, 90))
        pygame.display.update()
        relogio.tick(60)
           
start()