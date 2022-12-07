# -*- coding: utf-8 -*-
import random, personajes, pygame, copy, math
from sys import exit
from pytmx.util_pygame import load_pygame # necesario para cargar mapas de tiles

# programando la ventana
#   data:

data = {
    "jugador" : copy.copy(personajes.personajes_base[0]),
    "page" : "home",
    "pausa" : False,
    "ventanaW" : 700,
    "ventanaH" : 500,
    "ventanaC" : [0,0,0],
    "clk_cool": 0,
    "fps" : 60,
    "crx" : 150,
    "IMGS" : "assets/imgs/",
    "rPersonajes" : copy.copy(personajes.personajes_base),
    "personajesL" : [False,False],
    "sltd" : False, # pregunta si se han seleccionado ambos personajes
    "saludes" : [1,1],
    "b_iniciada" : [False],
    "colores" : [
        "black",
        "#0f052d",
        "#203671",
        "#36868f",
        "#5fc75d",
        "white",
    ],
    "batalla_poss_i" : [2,4],
    "batalla_poss" : [2,4],
    "frame_fase" : 300
}



# ejecutando ventana
pygame.init()
pygame_icon = pygame.image.load(f"{data['IMGS']}items/hacha.png")
pygame.display.set_icon(pygame_icon)
ventana = pygame.display.set_mode((data['ventanaW'],data['ventanaH']))
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

# cargar nivel

tmx_data = load_pygame("data/tmx/nivel0.tmx")

# maneras de extraer las capas
#print(tmx_data.layers)
#for layer in tmx_data.visible_layers: # mostrar todas las capas visibles
#    print(layer)
#print(tmx_data.get_layer_by_name("muros")) # consigueme una sola capa

# for objetos in tmx_data.objectgroups: #p para extraer la capa de objetos
#    print(objetos)

# extraer tiles individuales
#fondo = tmx_data.get_layer_by_name("fondo")
#for x,y,surf in fondo.tiles(): # obtener toda la informacion de una capa
#    print(x)
#    print(y)
#    print(surf)
#print(fondo.data) # otra manera de extraer toda la info de una capa
# extrae objetos
#muros = tmx_data.get_layer_by_name("muros")
#for muro in muros:
#    print(muro)

grupo_tiles = pygame.sprite.Group()
paredes = []
# funciones
def hover(rect):
        pygame.mouse.get_cursor()
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos): return True
        else: return False

def actualizar_personajes(jugador,oponente,npc=False):
    if jugador.estado == "attack": jugador.estado_imgs = jugador.attack_imgs
    elif jugador.estado == "protect": jugador.estado_imgs = jugador.protect_imgs
    elif jugador.estado == "boost": jugador.estado_imgs = jugador.boost_imgs
    else: jugador.estado_imgs = jugador.stand_imgs
    if jugador.cool < 1: # si el personaje no se esta enfriando
        if not npc: jAct = jugador.act(oponente) # invoca la accion del personaje
        else: jAct = jugador.autoAct(oponente) # invoca la accion automatica del personaje
        if isinstance(jAct,list): # si se realizo una accion tipo lista
            for msg in jAct: # para cada uno de los mensaje devueltos de la accion
                if msg: # genera un mensaje fantasma
                    g_msgs.append(ghost_msg(msg))
    else: jugador.cool -= 1 # sino reducele el cooldown
    if jugador.cool_h > 0: jugador.cool_h -= 1

# elementos de pantalla
m_pausa = pygame.image.load("assets/imgs/interfaces/pausa_menu.png").convert_alpha() 
nav =  pygame.image.load("assets/imgs/interfaces/nav.png").convert_alpha() 
nav_b = pygame.image.load("assets/imgs/interfaces/nav_b.png").convert_alpha()
btnPausa = pygame.image.load("assets/imgs/interfaces/pausa.png").convert_alpha()
btnPlay = pygame.image.load("assets/imgs/interfaces/play.png").convert_alpha()
btnN = pygame.Surface((100,40))
btnPausaRct = btnPausa.get_rect(center = (650,33))
btnPlayRct = btnPlay.get_rect(center = (350,300))
menu_items = pygame.image.load("assets/imgs/interfaces/menu-items.png").convert()
carta_p = pygame.image.load("assets/imgs/interfaces/carta-personaje.png").convert_alpha()

txt_pausa = fuente.render("PAUSA", True, data['colores'][5])
txt_pausa_rect = txt_pausa.get_rect(center = (300,100))

m_pausa.blit(txt_pausa,(txt_pausa_rect))
m_pausa.blit(btnPlay,(btnPlay.get_rect(center =(300,175))))

btnN_rect = btnN.get_rect(topleft=(0,0))
m_pausa_rect = m_pausa.get_rect(center = (350,250))
g_msgs = []

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

# crear los tiles
for capa in tmx_data.visible_layers: #para cada una de las capas visibles
    if hasattr(capa,"data"): # si esta tiene el atributo "data" (osea si es una capa de mozaicos y no objetos)
        for x,y,surf in capa.tiles():
            pos = (x*70,y*70)
            Tile(pos,surf,grupo_tiles)
# crear los objetos
for obj in tmx_data.objects:
    pos = (obj.x,obj.y)
    if obj.type in ("bloqueS"):
        Tile(pos,obj.image,grupo_tiles)

for obj in tmx_data.objects: # objetos invisibles
        if obj.type in ("muro"):
            paredes.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))
            
class ghost_msg:
    def __init__(self,datos:list):
        self.mensaje = datos[0]
        self.color = datos[1]
        self.x = (random.randint(85,115)/100)*datos[2]
        self.y = (random.randint(85,115)/100)*datos[3]
        self.alpha = 255
        self.dur = 800
        self.msg_text = pygame.font.Font(fStyle,30).render(self.mensaje,False,self.color)
        self.msg_rect = self.msg_text.get_rect(center=(self.x,self.y))
    def dibujar(self):
        self.msg_text.set_alpha(255-(self.dur*-1))
        self.msg_rect.top += self.dur/1000
        ventana.blit(self.msg_text,self.msg_rect)
        self.dur -= 6
        if self.dur > 1:
            self.dibujar()

def navLabels(titulo="",color="black",tf=50,crx=data['crx'], bgC = data['colores'][1], jugador = False): # posiciona el header y el footer
    if bgC: ventana.fill(bgC)
    _header = copy.copy(nav)
    
    fuente = pygame.font.Font(fStyle,tf)
    txt = fuente.render(titulo, False,  data['colores'][5]) #crear una superficie en texto(texto,suavisado,color)
    txt_rect = txt.get_rect(center=((txt.get_width()/2)+10,37))
    _header.blit(btnPausa,btnPausaRct)
    _header.blit(txt,txt_rect)
    
    if jugador:
        for item in jugador.bolsa: # para cada uno de los items
            item_surf = pygame.Surface((50,50), pygame.SRCALPHA,32) # crea una superficie tranparente
            pygame.draw.circle(item_surf, "#28484d", (25,25), 25) # dinuja un circulo
            if item.usando: pygame.draw.circle(item_surf, "Yellow", (25,25), 25,width = 2) # si lo estan usando dibuja un contorno amarillo
            elif item.cool <= 0 or not item.consumible or item.cantidad < 1: # sino, y o es consumible o se acabo ya, uno blanco 
                pygame.draw.circle(item_surf, "white", (25,25), 25,width = 1)
            elif item.consumible: # y si resulta ser consumible, muestra su carga
                pygame.draw.arc(item_surf, data['colores'][4], item_surf.get_rect(center = (25,25)),0,item.cool/50, width=2)
                item.cool -= 1
            if item.cantidad > 0:
                item_surf.blit((item.img).convert_alpha(),(0,0))
                fuente = pygame.font.Font(fStyle,17)
                if item.consumible: menu_items.blit(fuente.render(f"{item.cantidad}",False,"White"),(85+(jugador.bolsa.index(item)+1)*70,55))
            menu_items.blit(item_surf,(35+(jugador.bolsa.index(item)+1)*70,25))
        _header.blit(menu_items,(0,0))
    _header.blit(nav_b,(0,0))
    ventana.blit(_header,(3.5,0))

    _footer = copy.copy(nav)
    fuente = pygame.font.Font(fStyle,20)
    cr = fuente.render("RBSv0.0 Copyright (c) 2022 Alex VB",False,"White")
    _footer.blit(cr,(crx,25))
    _footer.blit(pygame.transform.flip(nav_b, False, True),(0,0))
    ventana.blit(_footer,(3.5,425))
    
class btn_n:
    def __init__(self,dir,texto,posicion:tuple,colores:tuple = (data['colores'][5],False,False),colores_h:tuple = (data['colores'][4],False,False)):
        self.dir = dir
        self.texto = texto
        self.colores = colores
        self.colores_h = colores_h
        self.surf = pygame.Surface((100,40), pygame.SRCALPHA,32)
        self.x = posicion[0]
        self.y = posicion[1]
        self.rect = self.surf.get_rect(center = (self.x,self.y))
        self.rect1 = self.surf.get_rect(center = (50,15))
        self.rect2 = self.surf.get_rect(center = (50,20))
        self.act = False
    def dibujar(self):
        fuente = pygame.font.Font(fStyle,20)
        if not hover(self.rect): 
            actColores = self.colores
            #pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else: 
            actColores = self.colores_h
            self.click()
            #pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        txt_surf = fuente.render(self.texto,False,actColores[0])
        pygame.draw.rect(self.surf, actColores[2],self.rect2)
        pygame.draw.rect(self.surf, actColores[1],self.rect1)
        self.surf.blit(txt_surf,txt_surf.get_rect(center=(50,20)))
        ventana.blit(self.surf,self.rect)
        return self.act
    def click(self):
        if pygame.mouse.get_pressed()[0] and data["clk_cool"] == 0:
            data["clk_cool"] = 30
            print(f"estas en la pagina{(data['page'])}")
            print(f"ir a la pagina {self.dir}")
            data["page"] = (self.dir)
            self.act = True
        else:
            self.act = False

def conteo_reg(esp):
    data["batalla_poss"] = data["batalla_poss_i"]
    if esp > 0 and not data['b_iniciada'][0]:
        if esp > 90: fal = 3
        elif esp > 60: fal = 2
        elif esp > 30: fal = 1
        elif esp > 1: fal = "peleen!"
        else: data['b_iniciada'][0] = True
        if esp > 1:
            txt = fuente.render(f"{fal}",False,data['colores'][5])
            txt_rect = txt.get_rect(center=(data['ventanaW']/2,data['ventanaH']/2))
            ventana.blit(txt,txt_rect)
            return True
        else: return False

# paginas

def pageHome():
    navLabels("Home",crx=data['crx'])
    
    fuente = pygame.font.Font("assets/font/8bitOperatorPlusSC-Bold.ttf",120)
    ttl = fuente.render("RBSv0",False,data['colores'][0])
    ttl_rect = ttl.get_rect(center = (350,180))
    ventana.blit(ttl,ttl_rect)
    ttl = fuente.render("RBSv0",False,data['colores'][4])
    ttl_rect = ttl.get_rect(center = (350,160))
    ventana.blit(ttl,ttl_rect)

    btn_n("mode","iniciar",((data['ventanaW']/2),320),(data['colores'][5],data['colores'][2],data['colores'][0]),(data['colores'][5],data['colores'][4],data['colores'][3])).dibujar()
    if pygame.key.get_pressed()[pygame.K_SPACE]: data["page"] = "mode"

def pageMode():
    navLabels("Home",crx=data['crx'])
    
    fuente = pygame.font.Font("assets/font/8bitOperatorPlusSC-Bold.ttf",120)
    
    ttl = fuente.render("RBSv0",False,data['colores'][0])
    ttl_rect = ttl.get_rect(center = (350,180))
    ventana.blit(ttl,ttl_rect)
    ttl = fuente.render("RBSv0",False,data['colores'][4])
    ttl_rect = ttl.get_rect(center = (350,160))
    ventana.blit(ttl,ttl_rect)
    
    salir = [
        btn_n("aventura","AVENTURA",((data['ventanaW']/2),270)).dibujar(),
        btn_n(False,"ONLINE",((data['ventanaW']/2),310),(data["colores"][2],False,False),(data["colores"][2],False,False)).dibujar(),
        btn_n(False,"B.ONLINE",((data['ventanaW']/2),350),(data["colores"][2],False,False),(data["colores"][2],False,False)).dibujar(),
        btn_n("batalla_seleccion","BATALLA",((data['ventanaW']/2),390)).dibujar()
    ]
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        data["page"] = 2
    return salir

def pageSelect(personajes:list):
    navLabels("Selecciona",crx=data['crx'])
    sltd = False
    chars_r = []

    for char in personajes:
        if personajes.index(char) <= 4: 
            px = 0
            fila = 95
        else: 
            px = 400
            fila = 205

        char_surf = pygame.Surface((70, 100), pygame.SRCALPHA,32)

        char_rect = char_surf.get_rect(topleft=(150+(personajes.index(char)*80)-px,fila))
        
        fuente = pygame.font.Font(fStyle,17)

        if hover(char_rect):
            pygame.draw.rect(char_surf, data["colores"][4], char_surf.get_rect(center = (35,50)))
            pygame.draw.rect(char_surf, data["colores"][2], char_surf.get_rect(center = (35,45)))
            name = fuente.render(char.nombre,False,data['colores'][4]).convert()
        else:
            pygame.draw.rect(char_surf, data["colores"][2], char_surf.get_rect(center = (35,50)))
            pygame.draw.rect(char_surf, data["colores"][1], char_surf.get_rect(center = (35,45)))
            name = fuente.render(char.nombre,False,data['colores'][3]).convert()
       
        
        name_rect = name.get_rect(center = (char_surf.get_width()/2,80))
        icon = char.icon
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
                    if not data['personajesL'][0]:
                        print("jugador: "+personajes[chars_r.index(char_r)].nombre)
                        data['personajesL'][0] = copy.copy(personajes.pop(chars_r.index(char_r)))
                    elif not data['personajesL'][1]:
                        print("oponente: "+personajes[chars_r.index(char_r)].nombre)
                        data['personajesL'][1] = copy.copy(personajes.pop(chars_r.index(char_r)))
    if data['personajesL'][0]:
        info_p1 = copy.copy(carta_p)
        info_p_rect = info_p1.get_rect(topleft=(0,75))
        
        info_p_img = data["personajesL"][0].stand_imgs[math.floor(data["frame_fase"]/100)].convert_alpha()
        info_p_img_rect = info_p_img.get_rect(center=(info_p_rect.width/2,(info_p_rect.height/2)-20))
        fuente = pygame.font.Font(fStyle,15)
        info_p_hp = fuente.render("Hp: %s"%data['personajesL'][0].saludMax,False,"White")
        info_p_atk = fuente.render("Atk: %s"%data['personajesL'][0].ataque,False,"White") 
        info_p_def = fuente.render("Def: %s"%data['personajesL'][0].defensa,False,"White") 
        info_p_vel = fuente.render("Vel: %s"%data['personajesL'][0].velocidad,False,"White")
        info_p1.blit(info_p_img,info_p_img_rect)
        
        info_p1.blit(info_p_hp,(10,250))
        info_p1.blit(info_p_atk,(10,270))
        info_p1.blit(info_p_def,(10,290))
        info_p1.blit(info_p_vel,(10,310))
        
        fuente = pygame.font.Font(fStyle,25)
        info_p_n = fuente.render(data['personajesL'][0].nombre,False,"White")
        info_p1.blit(info_p_n,((info_p_rect.width/2)-info_p_n.get_width()/2,10))
        
        ventana.blit(info_p1,info_p_rect)
        fuente = pygame.font.Font(fStyle,15)
        
    if data['personajesL'][1]:
        info_p2 = copy.copy(carta_p)
        info_p2_rect = info_p2.get_rect(topleft=(550,75))
        
        info_p2_img = pygame.transform.flip(data["personajesL"][1].stand_imgs[math.floor(data["frame_fase"]/100)].convert_alpha(),True,False)
        info_p2_img_rect = info_p2_img.get_rect(center=(info_p2_rect.width/2,(info_p2_rect.height/2)-20))
        
        info_p2_hp = fuente.render("Hp: %s"%data['personajesL'][1].saludMax,False,"White")
        info_p2_atk = fuente.render("Atk: %s"%data['personajesL'][1].ataque,False,"White") 
        info_p2_def = fuente.render("Def: %s"%data['personajesL'][1].defensa,False,"White") 
        info_p2_vel = fuente.render("Vel: %s"%data['personajesL'][1].velocidad,False,"White")
        info_p2.blit(info_p2_img,info_p2_img_rect)
        
        info_p2.blit(info_p2_hp,(10,250))
        info_p2.blit(info_p2_atk,(10,270))
        info_p2.blit(info_p2_def,(10,290))
        info_p2.blit(info_p2_vel,(10,310))
        
        fuente = pygame.font.Font(fStyle,25)
        info_p2_n = fuente.render(data['personajesL'][1].nombre,False,"White")
        info_p2.blit(info_p2_n,((info_p2_rect.width/2)-info_p2_n.get_width()/2,10))
        
        ventana.blit(info_p2,info_p2_rect)
        sltd = True
    btn_n("mode","volver",((data["ventanaW"]/2),350),(data['colores'][2],False,data["colores"][1]),(data['colores'][3],False,data['colores'][2])).dibujar()
    
    if sltd:  # cuando ya esten seleccionados
        btn_n("batalla","empezar!",((data["ventanaW"]/2)+60,400),(data['colores'][5],data['colores'][2],data['colores'][0]),(data['colores'][5],data['colores'][4],data['colores'][3])).dibujar()
        r = btn_n("batalla_seleccion","reset",((data["ventanaW"]/2)-60,400),(data['colores'][3],data['colores'][5],data['colores'][2]),(data['colores'][5],"red","darkred")).dibujar()
        if r: # limpiar 
            personajes.append(data["personajesL"].pop(0))
            personajes.append(data["personajesL"].pop(0))
            data["personajesL"].append(False)
            data["personajesL"].append(False)
            print ("reset")

def pageAventura(plyr = data["jugador"]):

    grupo_tiles.draw(ventana)
    #for rect in paredes: pygame.draw.rect(ventana, False, rect)
    
    navLabels("Aventura",crx=data["crx"],bgC=False,jugador = data["jugador"]) 
    ventana.blit(plyr.estado_imgs[math.floor(data["frame_fase"]/100)],(plyr.x,plyr.y))
    
    """
    jAct =  plyr.act(plyr) # invoca la accion automatica del personaje
    if isinstance(jAct,list): # si se realizo una accion tipo lista
        for msg in jAct: # para cada uno de los mensaje devueltos de la accion
            if msg: # genera un mensaje fantasma
                g_msgs.append(ghost_msg(msg))
    for msg in g_msgs: msg.dibujar()
    if len(g_msgs) > 5: g_msgs.pop(0)
    """
    plyr.mover_adv()

    if plyr.salud <= 10: # si el jugador muere, muestra el boton de continuar
        return btn_n("gameover","continue",
        (ventana.get_width()/2,400),
        (data["colores"][5],False,data["colores"][5]),
        (data["colores"][4],False,data["colores"][4])).dibujar()

    for tile in grupo_tiles.sprites(): # mover camara
        tile.rect.x-=plyr.velx
        tile.rect.y-=plyr.vely

def pageBatalla(chars:list):
    jugador = chars[0]
    oponente = chars[1]

    jugador.x = 1
    jugador.y = 290
    oponente.x = 1
    oponente.y = 290
    
    navLabels(" ",tf=35,crx=data['crx'],jugador=jugador)
    fondo = pygame.image.load("assets/imgs/interfaces/escenario.png").convert()
    ventana.blit(fondo,(0,100))

    # movimiento de personaje
    jugador.mover(oponente)
    oponente.mover(jugador,True)

    # buscar images actual del jugador y el oponente
    jugadorImg = jugador.estado_imgs[math.floor(data['frame_fase']/100)].convert_alpha()
    oponenteImg = pygame.transform.flip(oponente.estado_imgs[math.floor(data['frame_fase']/100)].convert_alpha(),True,False)
    
    ventana.blit(jugadorImg,(jugadorImg.get_rect(center = (jugador.x,jugador.y))))
    ventana.blit(oponenteImg,(oponenteImg.get_rect(center = (oponente.x,oponente.y))))

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
    
    puntosJ = pygame.transform.flip(pygame.Surface((113*(jugador.puntos/jugador.puntosMax),15)),True,False)
    puntosJ.fill(data['colores'][3])
    puntosO = pygame.Surface((113*(oponente.puntos/oponente.puntosMax),15))
    puntosO.fill(data['colores'][3])
    ventana.blit(puntosJ,(183,163))
    ventana.blit(puntosO,(394,163))
    
    if len(g_msgs) > 5: g_msgs.pop(0) #elimina primer mensaje fantasma para no desbordar la lista

    data['saludes'][0] = jugador.salud
    data['saludes'][1] = oponente.salud 
    
    if conteo_reg(jugador.cool): # conteo regresivo
        jugador.pos = data["batalla_poss_i"][0]
        oponente.pos = data["batalla_poss_i"][1]
    
    for msg in g_msgs: msg.dibujar() #dibuja los mensajes 5 fantasma existentes

    """
    info_j = fuente.render(f"{jugador.pos}",False,"red") #mostrar informacion de jugador en tiempo real
    info_j_rect = info_j.get_rect(topleft = (0,0))
    ventana.blit(info_j, (info_j_rect))

    info_o = fuente.render(f"{oponente.pos}",False,"red") #mostrar informacion del oponente en tiempo real
    info_o_rect = info_o.get_rect(topleft = (0,50))
    ventana.blit(info_o, (info_o_rect))
    """
    # circulos de estado y estados
    pygame.draw.circle(ventana, data['colores'][1], (30,jugador.y), 20)
    pygame.draw.circle(ventana, data['colores'][1], (670,oponente.y), 20)
    pygame.draw.circle(ventana, data['colores'][5], (30,jugador.y), 20, width = 1)
    pygame.draw.circle(ventana, data['colores'][5], (670,oponente.y), 20, width = 1)

    if jugador.estado != "stand":
        estadoJ = pygame.image.load(f"{data['IMGS']}/interfaces/{jugador.estado}.png")
        estadoJ_rect = estadoJ.get_rect(center = (30,jugador.y))
        ventana.blit(estadoJ,estadoJ_rect)
    if oponente.estado != "stand":
        estadoJ = pygame.image.load(f"{data['IMGS']}/interfaces/{oponente.estado}.png")
        estadoJ_rect = estadoJ.get_rect(center = (670,oponente.y))
        ventana.blit(estadoJ,estadoJ_rect)
    
    if data['saludes'][0] <= 1 or data['saludes'][1] <= 1: # si no esta vivo alguno de los dos, muestra el boton de continuar
        for personaje in [jugador,oponente]:
            if personaje.salud <= 1:
                personaje.estado_imgs = personaje.derrota_imgs
            else: 
                personaje.estado_imgs = personaje.victoria_imgs
            for item in personaje.bolsa: item.usando = False
        
        return btn_n("gameover","continue",(ventana.get_width()/2,400),(data["colores"][5],False,data["colores"][5]),(data["colores"][4],False,data["colores"][4])).dibujar()
    else : # pero si lo estan ambos, que actuen
        actualizar_personajes(jugador,oponente,False)
        actualizar_personajes(oponente,jugador,True)
        return False
    
def pageGameover(saludes):
    g_msgs.clear()
    data['b_iniciada'][0] = False
    data['personajesL'][0] = False
    data['personajesL'][1] = False
    navLabels("GAME OVER",crx=data['crx'],bgC=False)
    espacioGO = pygame.Surface((700, 500))
    espacioGO.fill("Black")
    espacioGO.set_alpha(10)
    if data['saludes'][0]>1: txt = fuente.render("VICTORIA",False,"Green")
    else: txt = fuente.render("DERROTA",False,"Red")
    txt_rect = txt.get_rect(center = (350,250))
    espacioGO.blit(txt,txt_rect)
    ventana.blit(espacioGO,(0,0))
    
    return btn_n("batalla_seleccion","volver",(600,385),("white",False,False),("green",False,"green")).dibujar()
    

# bucle principal

while True:
    for event in pygame.event.get(): # detecta todos los eventos en pantalla
        if event.type == pygame.QUIT: # para poder salir
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:# configurando la deteccion delos botones header

            mouse_pos = pygame.mouse.get_pos()
            
            if btnPausaRct.collidepoint(mouse_pos):
                data["pausa"] = True
            if btnPlayRct.collidepoint(mouse_pos):
                print("continuar")
                data["pausa"] = False

    if not data["pausa"]:
        if(data["page"]=="home"):
            pageHome()
        elif(data["page"]=="batalla_seleccion"):
            pageSelect(data['rPersonajes'])
        elif(data["page"] == "mode"):
            pageMode()
        elif(data["page"]=="aventura"):
            pageAventura()
        elif(data["page"]=="batalla"):
            pageBatalla(data['personajesL'])
        elif(data["page"]=="gameover"):
            data['rPersonajes'] = copy.copy(personajes.personajes_base)
            pageGameover(data['saludes'])
            
        data['crx']-=3
        if data['crx'] < -370: data['crx'] = data['ventanaW']
    else:  ventana.blit(m_pausa,m_pausa_rect) # que se muestre la pantallas de pausa
    if data["clk_cool"] > 0: data["clk_cool"] -= 1 
    if data["frame_fase"] > 0: data["frame_fase"] -= 10
    else: data["frame_fase"] = 300
    pygame.display.update()
    clock.tick(data["fps"]) # indica que el bucle qhile no puede reproducirse mas rapido que la cantidad indicada de frames