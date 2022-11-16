import random, personajes, pygame, copy, time
from sys import exit

# programando la ventana
#   especificaciones:
ventanaW = 700
ventanaH = 500
ventanaC = [0,0,0]
fps = 60 
crx=150
IMGS = "assets/imgs/"
personajesL = [False,False]
sltd = False
# ejecutando ventana
pygame.init()
ventana = pygame.display.set_mode((ventanaW,ventanaH))
pygame.display.set_caption('RBSv0.0')

# objeto reloj que conr¿trola el framerate
clock = pygame.time.Clock()

# fuente de texto
fStyle = "assets/font/8bitOperatorPlus8-Regular.ttf"
fuente = pygame.font.Font(fStyle,50) # recibe un estilo y un tamaño

# desplegar imagenes, hay dos tipos de superficie:
    # display superficie: la ventana del juego, el display en si
    # regular superficie: deben estar sobre la display suface para verse, son cada una de las imagenes
        # pueden ser: color plano, imagenes renderizadas, texto.

# elementos de pantalla
btnPausa = pygame.image.load("assets/imgs/interfaces/boton-de-pausa.png").convert()
btnConfig = pygame.image.load("assets/imgs/interfaces/configuraciones.png").convert()
btnInfo = pygame.image.load("assets/imgs/interfaces/informacion.png").convert()
btnN = pygame.Surface((100,40))
btnPausaRct = btnPausa.get_rect(topleft = (600,15))
btnConfigRct= btnConfig.get_rect(topleft = (500,15))
btnInfoRct = btnInfo.get_rect(topleft = (400,15))
btnN_rect = btnN.get_rect(topleft=(0,0))
g_msgs = []
class ghost_msg:
    def __init__(self,datos:list):
        self.mensaje = datos[0]
        self.color = datos[1]
        self.x = (random.randint(85,115)/100)*datos[2]
        self.y = (random.randint(85,115)/100)*datos[3]
        self.alpha = 255
        self.dur = 800
        self.msg_text = pygame.font.Font(None,30).render(self.mensaje,False,self.color)
        self.msg_rect = self.msg_text.get_rect(center=(self.x+100,self.y))
    def dibujar(self):
        self.msg_text.set_alpha(255-(self.dur*-1))
        self.msg_rect.top += self.dur/1000
        ventana.blit(self.msg_text,self.msg_rect)
        self.dur -= 6
        if self.dur > 1:
            self.dibujar()


def navLabels(titulo="",color="black",tf=50,crx=crx): # posiciona el header y el footer
    ventana.fill("#ff5733")
    header = pygame.Surface((700,100))
    header.fill(color)
    fuente = pygame.font.Font(fStyle,tf)
    txt = fuente.render(titulo, False, "White") #crear una superficie en texto(texto,suavisado,color)
    txt_rect = txt.get_rect(center=((txt.get_width()/2)+10,50))
    header.blit(btnPausa,btnPausaRct)
    header.blit(btnConfig,btnConfigRct)
    header.blit(btnInfo,btnInfoRct)
    header.blit(txt,txt_rect)
    ventana.blit(header,(0,0))

    footer = pygame.Surface((700,75))
    footer.fill(color)
    fuente = pygame.font.Font(fStyle,20)
    cr = fuente.render("RBSv0.0 Copyright (c) 2022 Alex VB",False,"White")
    footer.blit(cr,(crx,25))
    ventana.blit(footer,(0,425))
    

def btnNext(texto,dir,x,y):

    #btn_rect = btnN.get_rect(center=(lugar.get_width()/2,lugar.get_height()/2)) si quisiera centrar el boton
    
    btnN.fill("Blue")
    btnN_rect.center = (x,y)
    fuente = pygame.font.Font(None,20)
    txt = fuente.render(texto,False,"White")
    txt_rect = txt.get_rect(center = (50,20))
    btnN.blit(txt,txt_rect)

    ventana.blit(btnN,btnN_rect)

    return dir
    


# paginas

def pageHome():
    navLabels("Home",crx=crx)
    
    fuente = pygame.font.Font("assets/font/8bitOperatorPlusSC-Bold.ttf",120)
    ttl = fuente.render("RBSv0",False,"Black")
    ttl_rect = ttl.get_rect(center = (350,180))
    fuente = pygame.font.Font(fStyle,50)
    ventana.blit(ttl,ttl_rect)
    salir = btnNext("iniciar",2,((ventanaW/2)),320)
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        salir = 2
    return salir
    

def pageSelect(personajes:list):
    navLabels("Selecciona",crx=crx)
    sltd = False
    chars_r = []
    
    for char in personajes:
        char_surf = pygame.Surface((70, 100)).convert()
        char_rect = char_surf.get_rect(topleft=(150+(personajes.index(char)*80),120))
        char_surf.fill("white")
        fuente = pygame.font.Font(fStyle,17)
        name = fuente.render(char.nombre,False,"Black").convert()
        name_rect = name.get_rect(center = (char_surf.get_width()/2,70))
        icon = pygame.image.load(IMGS+"personajes/"+char.imgRoot+"icon.png").convert()
        char_surf.blit(icon,(10,10))
        char_surf.blit(name,name_rect)
        ventana.blit(char_surf,char_rect)
        chars_r.append(char_rect)
    
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # para poder salir
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for char_r in chars_r:
                if char_r.collidepoint(mouse_pos): 
                    if not personajesL[0]:
                        print("jugador: "+personajes[chars_r.index(char_r)].nombre)
                        personajesL[0] = personajes.pop(chars_r.index(char_r))
                    elif not personajesL[1]:
                        print("oponente: "+personajes[chars_r.index(char_r)].nombre)
                        personajesL[1] = personajes.pop(chars_r.index(char_r))
    if personajesL[0]:
        info_p = pygame.Surface((150, 325))
        info_p_rect = info_p.get_rect(topleft=(0,100))
        info_p.fill("Black")
        info_p_img = pygame.image.load(IMGS+"personajes/"+personajesL[0].imgRoot+"stand.png").convert_alpha()
        info_p_img_rect = info_p_img.get_rect(center=(info_p_rect.width/2,(info_p_rect.height/2)-20))
        
        info_p_hp = fuente.render("Hp: %s"%personajesL[0].saludMax,False,"White")
        info_p_atk = fuente.render("Atk: %s"%personajesL[0].ataque,False,"White") 
        info_p_def = fuente.render("Def: %s"%personajesL[0].defensa,False,"White") 
        info_p_vel = fuente.render("Vel: %s"%personajesL[0].velocidad,False,"White")
        info_p.blit(info_p_img,info_p_img_rect)
        
        info_p.blit(info_p_hp,(10,250))
        info_p.blit(info_p_atk,(10,270))
        info_p.blit(info_p_def,(10,290))
        info_p.blit(info_p_vel,(10,310))
        
        fuente = pygame.font.Font(fStyle,25)
        info_p_n = fuente.render(personajesL[0].nombre,False,"White")
        info_p.blit(info_p_n,((info_p_rect.width/2)-info_p_n.get_width()/2,10))
        
        ventana.blit(info_p,info_p_rect)
        fuente = pygame.font.Font(fStyle,17)
        
    if personajesL[1]:
        info_p2 = pygame.Surface((150, 325))
        info_p2_rect = info_p2.get_rect(topleft=(550,100))
        info_p2.fill("Black")
        info_p2_img = pygame.transform.flip(pygame.image.load(IMGS+"personajes/"+personajesL[1].imgRoot+"stand.png").convert_alpha(),True,False)
        info_p2_img_rect = info_p2_img.get_rect(center=(info_p2_rect.width/2,info_p2_rect.height/2))
        
        info_p2_hp = fuente.render("Hp: %s"%personajesL[1].saludMax,False,"White")
        info_p2_atk = fuente.render("Atk: %s"%personajesL[1].ataque,False,"White") 
        info_p2_def = fuente.render("Def: %s"%personajesL[1].defensa,False,"White") 
        info_p2_vel = fuente.render("Vel: %s"%personajesL[1].velocidad,False,"White")
        info_p2.blit(info_p2_img,info_p2_img_rect)
        
        info_p2.blit(info_p2_hp,(10,250))
        info_p2.blit(info_p2_atk,(10,270))
        info_p2.blit(info_p2_def,(10,290))
        info_p2.blit(info_p2_vel,(10,310))
        
        fuente = pygame.font.Font(fStyle,25)
        info_p2_n = fuente.render(personajesL[1].nombre,False,"White")
        info_p2.blit(info_p2_n,((info_p2_rect.width/2)-info_p2_n.get_width()/2,10))
        
        ventana.blit(info_p2,info_p2_rect)
        sltd = True
    if sltd: return btnNext("empezar",4,ventana.get_width()/2,400)
    else: return False

def pageBatalla(personajes:list):
    jugador = personajes[0]
    oponente = personajes[1]

    jugador.x = 100
    jugador.y = 160
    oponente.x = 400
    oponente.y = 160
    #navLabels(" %s VS  %s " % (jugador.nombre, oponente.nombre),tf=35,crx=crx)
    #navLabels(" %s VS  %s " % (jugador.cool, oponente.cool),tf=35,crx=crx)
    navLabels(" ",tf=35,crx=crx)
    menu_items = pygame.image.load("assets/imgs/interfaces/menu-items.png").convert()
    fondo = pygame.image.load("assets/imgs/interfaces/escenario.png").convert()
    ventana.blit(menu_items,(0,0))
    ventana.blit(fondo,(0,100))
    
    jugador.mover()
    oponente.mover(True)
    jugadorImg = pygame.image.load("assets/imgs/personajes/"+jugador.imgAct).convert_alpha()
    oponenteImg = pygame.transform.flip(pygame.image.load("assets/imgs/personajes/"+oponente.imgAct).convert_alpha(),True,False)
    ventana.blit(jugadorImg,(jugador.x,jugador.y))
    ventana.blit(oponenteImg,(oponente.x,oponente.y))

    # barras de salud y de mana funcionales
    if jugador.salud > jugador.saludMax/2: colSaludJ = "Green"
    elif jugador.salud > jugador.saludMax/4: colSaludJ = "Yellow"
    else: colSaludJ = "Red"
    if oponente.salud > oponente.saludMax/2: colSaludO = "Green"
    elif oponente.salud > oponente.saludMax/4: colSaludO = "Yellow"
    else: colSaludO = "Red"
    if jugador.salud > 1: saludJ = pygame.transform.flip(pygame.Surface((215*(jugador.salud/jugador.saludMax),17)),True,False)
    else: saludJ = pygame.Surface((1,17)); 
    saludJ.fill(colSaludJ)
    if oponente.salud > 1: saludO = pygame.Surface((215*(oponente.salud/oponente.saludMax),17))
    else: saludO = pygame.Surface((1,17)); 
    saludO.fill(colSaludO)
    ventana.blit(saludJ,(80,131))
    ventana.blit(saludO,(397,131))

    for item in jugador.bolsa:
        ventana.blit(pygame.image.load("assets/imgs/items"+item.img).convert_alpha(),(35+(jugador.bolsa.index(item)+1)*70,25))
        fuente = pygame.font.Font(fStyle,17)
        ventana.blit(fuente.render("x%s"%item.cantidad,False,"Black"),(80+(jugador.bolsa.index(item)+1)*70,55))

    puntosJ = pygame.transform.flip(pygame.Surface((113*(jugador.puntos/jugador.puntosMax),15)),True,False)
    puntosJ.fill("Blue")
    puntosO = pygame.Surface((113*(oponente.puntos/oponente.puntosMax),15))
    puntosO.fill("Blue")
    ventana.blit(puntosJ,(183,163))
    ventana.blit(puntosO,(394,163))
    
    def consid(jugador,oponente,npc=False):
        if jugador.cool < 1: # si el personaje no se esta enfriando
            if not npc: jAct = jugador.act(oponente) # invoca la accion del personaje
            else: jAct = jugador.autoAct(oponente) # invoca la accion automatica del personaje
            if isinstance(jAct,list): # si se realizo una accion tipo lista
                for msg in jAct: # para cada uno de los mensaje devueltos de la accion
                    if msg: # genera un mensaje fantasma
                        g_msgs.append(ghost_msg(msg))
        else: jugador.cool -= 1 # sino reducele el cooldown
    
    if len(g_msgs) > 5: g_msgs.pop(0) #elimina primer mensaje fantasma para no desbordar la lista

    # movimiento de personaje
    
    consid(jugador,oponente,False)
    consid(oponente,jugador,True)
    

    for msg in g_msgs: msg.dibujar() #dibuja los mensajes fantasma
    
    fuente = pygame.font.Font(fStyle,20)
    coolJ = fuente.render("x Jugador: %s"%jugador.x,False,"Red")
    coolJ_rect = coolJ.get_rect(topleft = (10,10))
    ventana.blit(coolJ,coolJ_rect)
    coolO = fuente.render("x Oponente: %s"%oponente.x,False,"Red")
    coolO_rect = coolO.get_rect(topleft = (10,30))
    ventana.blit(coolO,coolO_rect)
    

# bucle principal
page = 1
pausa = False
while True:
    for event in pygame.event.get(): # detecta todos los eventos en pantalla
        if event.type == pygame.QUIT: # para poder salir
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:# configurando la deteccion delos botones header
            print(page)
            mouse_pos = pygame.mouse.get_pos()
            
            if btnPausaRct.collidepoint(mouse_pos):
                print("pausa")
            elif btnConfigRct.collidepoint(mouse_pos):
                print("Configuracion")
            elif btnInfoRct.collidepoint(mouse_pos):
                print("informacion")
            elif btnN_rect.collidepoint(mouse_pos):
                print("siguente")
                page = dirN

    if(page==1):
        dirN = pageHome()
    elif(page==2):
        dirN = pageSelect(personajes.personajes)
    elif(page==4):
        pageBatalla(personajesL)
        #pageBatalla(copy.copy([personajes.personajes[1],personajes.personajes[0]]))
        #pageBatalla(copy.copy([random.choice(personajes.personajes),random.choice(personajes.personajes)]))


    crx-=3
    if crx < -370:
        crx = ventanaW
    pygame.display.update()
    clock.tick(fps) # indica que el bucle qhile no puede reproducirse mas rapido que la cantidad indicada de frames