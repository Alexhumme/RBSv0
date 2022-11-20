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
rPersonajes = copy.copy(personajes.personajes)
personajesL = [False,False]
sltd = False # pregunta si se han seleccionado ambos personajes
saludes = [1,1]
b_iniciada = [False]

# ejecutando ventana
pygame.init()
pygame_icon = pygame.image.load(f"{IMGS}items/hacha.png")
pygame.display.set_icon(pygame_icon)
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
btnPausaRct = btnPausa.get_rect(center = (650,50))
btnConfigRct= btnConfig.get_rect(center = (550,50))
btnInfoRct = btnInfo.get_rect(center = (450,50))
btnN_rect = btnN.get_rect(topleft=(0,0))
txt_pausa = fuente.render("PAUSA", True, "Black")
txt_pausa_rect = txt_pausa.get_rect(center = (350,250))
g_msgs = []

class ghost_msg:
    def __init__(self,datos:list):
        self.mensaje = datos[0]
        self.color = datos[1]
        self.x = (random.randint(85,115)/100)*datos[2]
        self.y = (random.randint(85,115)/100)*datos[3]
        self.alpha = 255
        self.dur = 800
        self.msg_text = pygame.font.Font(fStyle,30).render(self.mensaje,False,self.color)
        self.msg_rect = self.msg_text.get_rect(center=(self.x+100,self.y))
    def dibujar(self):
        self.msg_text.set_alpha(255-(self.dur*-1))
        self.msg_rect.top += self.dur/1000
        ventana.blit(self.msg_text,self.msg_rect)
        self.dur -= 6
        if self.dur > 1:
            self.dibujar()


def navLabels(titulo="",color="black",tf=50,crx=crx, bgC = "#ff5733"): # posiciona el header y el footer
    if bgC: ventana.fill(bgC)
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

def conteo_reg(esp):
    if esp > 0 and not b_iniciada[0]:
        if esp > 90: fal = 3
        elif esp > 60: fal = 2
        elif esp > 30: fal = 1
        elif esp > 1: fal = "peleen!"
        else: b_iniciada[0] = True
        if esp > 1:
            txt = fuente.render(f"{fal}",False,"White")
            txt_rect = txt.get_rect(center=(ventanaW/2,ventanaH/2))
            ventana.blit(txt,txt_rect)
# paginas

def pageHome():
    navLabels("Home",crx=crx)
    
    fuente = pygame.font.Font("assets/font/8bitOperatorPlusSC-Bold.ttf",120)
    ttl = fuente.render("RBSv0",False,"Black")
    ttl_rect = ttl.get_rect(center = (350,180))
    fuente = pygame.font.Font(fStyle,50)
    ventana.blit(ttl,ttl_rect)
    salir = btnNext("iniciar",2,((ventanaW/2)),320)
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        page = 2
    return salir
    

def pageSelect(personajes:list):
    navLabels("Selecciona",crx=crx)
    sltd = False
    chars_r = []
    
    for char in personajes:
        if personajes.index(char) <=4: 
            px = 0
            fila = 120
        else: 
            px = 400
            fila = 230

        char_surf = pygame.Surface((70, 100))
        char_rect = char_surf.get_rect(topleft=(150+(personajes.index(char)*80)-px,fila))
        char_surf.fill("white")
        fuente = pygame.font.Font(fStyle,17)
        name = fuente.render(char.nombre,False,"Black").convert()
        
        name_rect = name.get_rect(center = (char_surf.get_width()/2,70))
        icon = pygame.image.load(IMGS+"personajes/"+char.imgRoot+"icon.png").convert_alpha()
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
                        personajesL[0] = copy.copy(personajes.pop(chars_r.index(char_r)))
                    elif not personajesL[1]:
                        print("oponente: "+personajes[chars_r.index(char_r)].nombre)
                        personajesL[1] = copy.copy(personajes.pop(chars_r.index(char_r)))
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

def pageBatalla(chars:list):
    jugador = chars[0]
    oponente = chars[1]

    jugador.x = 100
    jugador.y = 160
    oponente.x = 400
    oponente.y = 160
    
    navLabels(" ",tf=35,crx=crx)
    menu_items = pygame.image.load("assets/imgs/interfaces/menu-items.png").convert()
    fondo = pygame.image.load("assets/imgs/interfaces/escenario.png").convert()
    ventana.blit(menu_items,(0,0))
    ventana.blit(fondo,(0,100))

    # movimiento de personaje
    jugador.mover()
    oponente.mover(True)

    jugadorImg = pygame.image.load(f"{IMGS}personajes/{jugador.imgAct}").convert_alpha()
    oponenteImg = pygame.transform.flip(pygame.image.load(f"{IMGS}personajes/{oponente.imgAct}").convert_alpha(),True,False)
    
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

    # mostrar los items del jugador
    for item in jugador.bolsa:
        item_surf = pygame.Surface((50,50), pygame.SRCALPHA,32)
        pygame.draw.circle(item_surf, "#28484d", (25,25), 25)
        if item.usando: pygame.draw.circle(item_surf, "Yellow", (25,25), 25,width = 2)
        else: pygame.draw.circle(item_surf, "white", (25,25), 25,width = 1)
        if item.cantidad > 0:
            item_surf.blit(pygame.image.load(f"{IMGS}/items"+item.img).convert_alpha(),(0,0))
            fuente = pygame.font.Font(fStyle,17)
            if item.consumible: ventana.blit(fuente.render(f"{item.cantidad}",False,"White"),(85+(jugador.bolsa.index(item)+1)*70,55))
        ventana.blit(item_surf,(35+(jugador.bolsa.index(item)+1)*70,25))

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
        if jugador.cool_h > 0: jugador.cool_h -= 1
    
    if len(g_msgs) > 5: g_msgs.pop(0) #elimina primer mensaje fantasma para no desbordar la lista

    saludes[0] = jugador.salud
    saludes[1] = oponente.salud    
    
    conteo_reg(jugador.cool) # conteo regresivo
    
    for msg in g_msgs: msg.dibujar() #dibuja los mensajes 5 fantasma existentes
    
    if jugador.cool_h > 1:
        cool_h_j = pygame.Surface((30, 30)) #mostrar el cooldown de los items
        cool_h_j_rect = cool_h_j.get_rect(topleft = (jugador.x,jugador.y))
        pygame.draw.arc(ventana, "blue", cool_h_j_rect,0,jugador.cool_h/50, width=5)
    if oponente.cool_h > 1:
        cool_h_o = pygame.Surface((30, 30)) #mostrar el cooldown de los items
        cool_h_o_rect = cool_h_o.get_rect(topleft = (oponente.x+200,oponente.y))
        pygame.draw.arc(ventana, "blue", cool_h_o_rect,0,oponente.cool_h/50, width=5)

    fuente = pygame.font.Font(fStyle,20)
    coolJ = fuente.render("cool_h Jugador: %s"%(jugador.cool_h/60),False,"Red")
    coolJ_rect = coolJ.get_rect(topleft = (10,10))
    ventana.blit(coolJ,coolJ_rect)
    coolO = fuente.render("cool_h Oponente: %s"%(oponente.cool_h/60),False,"Red")
    coolO_rect = coolO.get_rect(topleft = (10,30))
    ventana.blit(coolO,coolO_rect)

    if saludes[0] <= 1 or saludes[1] <= 1: # si no esta vivo alguno de los dos, muestra el boton de continuar
        for personaje in chars: 
            for item in personaje.bolsa: item.usando = False

        return btnNext("continuar",5,ventana.get_width()/2,400)
    else : # pero si lo estan ambos, que actuen
        consid(jugador,oponente,False)
        consid(oponente,jugador,True)
        return False
    
    
def pageGameover(saludes):
    g_msgs.clear()
    b_iniciada[0] = False
    personajesL[0] = False
    personajesL[1] = False
    navLabels("GAME OVER",crx=crx,bgC=False)
    espacioGO = pygame.Surface((700, 325))
    espacioGO.fill("Black")
    espacioGO.set_alpha(10)
    if saludes[0]>1: txt = fuente.render("VICTORIA",False,"Green")
    else: txt = fuente.render("DERROTA",False,"Red")
    txt_rect = txt.get_rect(center = (350,162))
    espacioGO.blit(txt,txt_rect)
    ventana.blit(espacioGO,(0,100))
    
    return btnNext("reintentar",2,600,400)
    

# bucle principal
page = 1
pausa = False
while True:
    for event in pygame.event.get(): # detecta todos los eventos en pantalla
        if event.type == pygame.QUIT: # para poder salir
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:# configurando la deteccion delos botones header

            mouse_pos = pygame.mouse.get_pos()
            
            if btnPausaRct.collidepoint(mouse_pos):
                pausa = not pausa
                print("pausa")
            elif btnConfigRct.collidepoint(mouse_pos):
                print("Configuracion")
            elif btnInfoRct.collidepoint(mouse_pos):
                print("informacion")
            elif btnN_rect.collidepoint(mouse_pos):
                print("siguente")
                page = dirN
    if not pausa:

        if(page==1):
            dirN = pageHome()
        elif(page==2):
            dirN = pageSelect(rPersonajes)
        elif(page==4):
            dirN = pageBatalla(personajesL)
        elif(page==5):
            rPersonajes = copy.copy(personajes.personajes)
            dirN = pageGameover(saludes)
            #pageBatalla(copy.copy([personajes.personajes[1],personajes.personajes[0]]))
            #pageBatalla(copy.copy([random.choice(personajes.personajes),random.choice(personajes.personajes)]))
        crx-=3
        if crx < -370: crx = ventanaW
    else:  ventana.blit(txt_pausa,txt_pausa_rect) # que se muestre la pantallas de pausa

    pygame.display.update()
    clock.tick(fps) # indica que el bucle qhile no puede reproducirse mas rapido que la cantidad indicada de frames