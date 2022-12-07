#para correr el codigo ejecuta en terminal > py index.py
import time, random, math, pygame, copy
from colorama import init,Fore,Style 

class item(): # items que un personaje puede usar
    # el item por defecto es un té
    def __init__(self,nombre="item desconocido", cantidad=3, dialogo=("\n --- té refrescante que cura 35hp🍵"), efectos=["hp"], valores=[70],img="/desconocido.png",consumible=True,equipable=True,cool=300):
        self.id = " "
        self.usuario = " "
        self.nombre = nombre
        self.cantidad = cantidad
        self.dialogo = dialogo
        self.efectos = efectos
        self.valores = valores
        self.img = pygame.image.load(f"assets/imgs/items"+img)
        self.consumible = consumible
        self.equible = equipable
        self.usando = False
        self.able = True
        self.cool = cool
    def usar(self):
        if not self.usando and self.able:
            print("  ... %s usa %s %s! %s"%(self.usuario,Fore.YELLOW,self.nombre,Style.RESET_ALL))
            colores = []
            for efect in self.efectos:
                textE = ("     ... %s: "%efect)
                if self.valores[self.efectos.index(efect)] >= 0: textE += Fore.GREEN+" +"; colores.append("Green")
                else: textE += Fore.RED; colores.append("Red")
                textE+= str(self.valores[self.efectos.index(efect)])
                print(textE+Style.RESET_ALL)
            if self.consumible: 
                self.cool = 300
                self.cantidad-=1
                if self.cantidad <= 0: self.able = False
            else: self.usando = True
            return [self.efectos,self.valores,colores]
        else: return [["none"],[0],["White"]]

# un personaje puede estar:
    # quieto (Stand)
    # protegido (Protect)
    # atacando (attack)
    # meditando (boost)
    # aturdido
# ademas ouede estar:
    #quemado
    #congelado
    #envenenado
    #somnoliento
    #etc

class personaje: # clase para la construccion de los personajes

    def __init__(self, nombre, salud, ataque, defensa, velocidad,bolsa=[item()],imgRoot="test1/",itemE = item(equipable = True)):
        self.id = " "
        self.nombre = nombre
        self.saludMax = salud #maxima salud posible
        self.salud = salud #salud actual
        self.ataque = ataque
        self.defensa = defensa
        self.velocidad = velocidad
        self.ataque_base = ataque
        self.defensa_base = defensa
        self.velocidad_base = velocidad
        self.icon = pygame.image.load(f"assets/imgs/personajes/{imgRoot}icon.png")
        self.stand_imgs = [
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}stand1.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}stand2.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}stand3.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}stand4.png")
            ]
        '''
        self.attack_imgs = [
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}attack1.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}attack2.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}attack3.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}attack4.png")
            ]
        self.protect_imgs = [
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}protect1.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}protect2.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}protect3.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}protect4.png")
            ]
        self.boost_imgs = [
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}boost1.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}boost2.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}boost3.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}boost4.png")
            ]
        self.victoria_imgs = [
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}victoria1.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}victoria2.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}victoria3.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}victoria4.png")
            ]
        self.derrota_imgs = [
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}derrota1.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}derrota2.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}derrota3.png"),
            pygame.image.load(f"assets/imgs/personajes/{imgRoot}derrota4.png")
            ]
        '''
        self.bolsa = bolsa
        self.inventario = []
        self.itemE = itemE
        self.proteccion = False # escudo
        self.puntosMax = 100
        self.puntos = 50 # energia, una mecanica de intercambio 
        self.estado = "stand"
        self.estados_esp = []
        self.estado_imgs = self.stand_imgs
        self.imgRoot = imgRoot 

        self.x = 0
        self.y = 100
        self.velx = 0
        self.vely = 0
        self.height = self.estado_imgs[0].get_height()
        self.width = self.estado_imgs[0].get_width()
        self.alto = 0
        self.ancho = 280 
        self.cool = 120
        self.cool_h = 0
        self.cool_m = 0
        self.pos = 2
    def atacar(self, oponente, potencia=20):
        print("\n *** %s ataca..." % (self.nombre))

        multip = random.randint(85,115)/100
        dagno = math.ceil(multip*(potencia*(self.ataque/oponente.defensa)))
        self.velx = 100
        
        self.estado = "attack"

        if (oponente.proteccion and multip < 1.10): # el ataqque es efectivo si el enemigo no se proteje
            print(" ... ataque inefectivo!❌ %s se ha %sprotegido💥%s" % (oponente.nombre,Fore.BLUE,Style.RESET_ALL))
            oponente.proteccion = False
            return [["-0hp","White",oponente.x,oponente.y-100]]
        else:#if not (oponente.pos < self.pos-1 or oponente.pos > self.pos+1):
            #self.cool_m = math.floor(400/(self.velocidad+1)) # enfriamiento para moverse
            oponente.velx = -20
            color = "orange"
            if multip >= 1.10: #critico
                print ("%s ... %s rompe las defenas de %s con un %s impacto critico❗%s"%(Fore.YELLOW,self.nombre,oponente.nombre,Style.BRIGHT,Style.RESET_ALL))
                oponente.proteccion = False
                crit = [" ","Red",oponente.x,oponente.y-100]
                color = "red"
            else: crit = False

            print("%s ... ataque efectivo!💥%s"%(Fore.LIGHTGREEN_EX,Style.RESET_ALL))
            print(" ... %s sufre %s%s-%shp💔%s" % (oponente.nombre,Style.BRIGHT,Fore.RED,dagno,Style.RESET_ALL))
            
            oponente.estado = "aturdido"
            oponente.salud -= dagno
            
            if random.randint(0,10) >= 8: #puntos
                pnts = random.randint(1,10)
                self.puntos += pnts
                print(" ... %s : %s+%s puntos%s" % (self.nombre,Fore.GREEN,pnts,Style.RESET_ALL))
                pnt = ["+%sPnt"%pnts,"Blue",self.x,self.y-self.height/2]
                if self.puntos > self.puntosMax:
                    self.puntos = self.puntosMax
            else: pnt = False
            
            return[["-%shp"%(dagno),color,oponente.x,oponente.y-100],pnt,crit] #devolucion de mensajes
        
    def desc(self): # para obtener la info de un personaje
        desc = f"""
hp: {self.salud}
Ataque base: {self.ataque_base}
Ataque: {self.ataque}
Defensa base: {self.defensa_base}
Defensa: {self.defensa}
Velocidad base: {self.velocidad_base}
Velocidad: {self.velocidad}
Proteccion: {self.proteccion}
Puntos: {self.puntos}
Bolsa: 
"""
        for item in self.bolsa: desc+="  -- %s. %s x%s \n"%(self.bolsa.index(item),item.nombre,item.cantidad)
        print("\n*** Descripcion de %s ***" % (self.nombre))    
        print(desc)
        print("*** ********************* ***\n")

    def protect(self): 
#        self.cool_m = math.floor(30/(self.velocidad+1)) # enfriamiento para moverse
        self.proteccion = True
        print("\n *** %s %sse proteje!🛡️%s" % (self.nombre,Fore.BLUE,Style.RESET_ALL))
        self.estado = "protect"
        #return [["ESCUDO","Cyan",self.x,self.y-self.height/2]]
        return False

    def boost(self): # aumenta el poder del personaje
        print("\n *** %s medita... " %(self.nombre));msg = "+0"
        self.estado = "boost"
        self.puntos += 0.5
        if (self.puntos >= 100):
            print(Fore.GREEN+" ... la meditacion aumenta su poder!⬆️")
            print(Style.BRIGHT+
                """
                +%sAtk 
                  +%sDef
                    +%sVel
                """% (math.ceil(3/self.ataque), math.ceil(3/self.defensa), math.ceil(18/self.velocidad))
            )
            print(Style.RESET_ALL,end="")
            # El aumento es inversamente proporcional al valor actual de la estadistica
            # Se redondea hacia arriba
            atkb = random.randint(1,3)
            defb = random.randint(1,3)
            velb = random.randint(1,3)
            hpb = random.randint(30,60)
            self.ataque += atkb
            self.defensa += defb
            self.velocidad += velb
            self.salud += hpb
            self.puntos -= 50
            if self.salud > self.saludMax: self.salud = self.saludMax
            return [
                [f"+{atkb}Atk","lightgreen",self.x,self.y-self.height/2],
                [f"+{defb}Def","lightgreen",self.x,self.y-self.height/2],
                [f"+{velb}Vel","lightgreen",self.x,self.y-self.height/2],
                [f"+{hpb}Hp","lightgreen",self.x,self.y-self.height/2],
            ] #devolucion de mensajes

            stats = ["non","hp","atk","def","vel","pnt","non"] 
            stat = random.choice(stats)
            print(Fore.GREEN,end="")
            if stat == "hp": 
                self.salud += 30
                if self.salud > self.saludMax: self.salud = self.saludMax # si su salud actual es mayor al maximo, que se iguales 
                msg = "+Hp"
            elif stat == "atk": self.ataque += 1; print(" ... %s canaliza su ira ⬆️\n" % (self.nombre)); msg = "+Atk"
            elif stat == "def": self.defensa += 1; print(" ... la piel de %s se endurece ⬆️\n" % (self.nombre)); msg = "+Def"
            elif stat == "vel": self.velocidad += 0.1; print(" ... el cuerpo de %s se aligera ⬆️\n" % (self.nombre)); msg = "+Vel"
            elif stat == "pnt": self.puntos += 30; print(" ... %s busca su fuerza interior ⬆️\n" % (self.nombre)); msg = "+10Pnt"
            elif stat == "non": print(Style.RESET_ALL+" ... %s casi se queda dormido 😴\n" % (self.nombre)) ; msg = "... fallido"
            
            print(Style.RESET_ALL,end="")
            self.puntos -= 30

            return [[msg,"Lightgreen",self.x,self.y-self.height/2]] #devolucion de mensajes
        else:
            print(" ... %s casi se queda dormido 😴\n" % (self.nombre))

            return False #devolucion de mensajes

    def uBolsa(self,rand=False):
        if len(self.bolsa) > 0:
            
            print("\n%s *** bolsa de %s 🎒%s"%(Fore.YELLOW,self.nombre,Style.RESET_ALL))
            # mostrar items en la mochila
            for item in self.bolsa: 
                if item!="cancelar":print(" ... %s. %s x%s"%(self.bolsa.index(item),item.nombre,item.cantidad))
                else: print(" ... %s. %s "%(self.bolsa.index(item),item))
            if not rand: # seleccion no aleatoria, manual.
                keys = pygame.key.get_pressed()
                if keys[pygame.K_1] and len(self.bolsa)>0: sel = self.bolsa[0]
                elif keys[pygame.K_2] and len(self.bolsa)>1: sel = self.bolsa[1]
                elif keys[pygame.K_3] and len(self.bolsa)>2: sel = self.bolsa[2]
                elif keys[pygame.K_4] and len(self.bolsa)>3: sel = self.bolsa[3]
                else: return True
            else: # seleccion aleatoria, pude ser cualquer cosa menos cancelar.
                sel = random.choice(self.bolsa)

            if not sel.usando and sel.able: # si no esta usando a este item y su cantidad es mayor a 0
                if sel.consumible and sel.cool > 1: # si el item seleccionado es consumible
                    return [False] # si aun se esta enfriando, devuelve false
                else:
                    self.ataque = self.ataque_base
                    self.defensa = self.defensa_base
                    self.velocidad = self.velocidad_base
                    for item in self.bolsa: item.usando = False
                
                sel.usuario = self.nombre
                
                uso = sel.usar()
                resultado = [False]
                for efect in uso[0]:
                    if efect == "hp":
                        self.salud += uso[1][uso[0].index(efect)]
                        if self.salud > self.saludMax: self.salud = self.saludMax # si su salud actual es mayor al maximo, que se iguales 
                    elif efect == "atk":
                        if sel.consumible: 
                            self.ataque_base += uso[1][uso[0].index(efect)]
                            self.ataque = self.ataque_base
                        else: self.ataque += uso[1][uso[0].index(efect)]
                    elif efect == "def":
                        if sel.consumible: 
                            self.defensa_base += uso[1][uso[0].index(efect)]
                            self.defensa = self.defensa_base
                        else: self.defensa += uso[1][uso[0].index(efect)]
                    elif efect == "vel":
                        if sel.consumible: 
                            self.velocidad_base += uso[1][uso[0].index(efect)]
                            self.velocidad = self.velocidad_base
                        else: self.velocidad += uso[1][uso[0].index(efect)]
                    elif efect == "pnt":
                        self.puntos += uso[1][uso[0].index(efect)]
                    resultado.append(["+ %s %s"%(uso[1][uso[0].index(efect)],efect),uso[2][uso[0].index(efect)],self.x,self.y-self.height/2])
                if sel.cantidad <= 0: sel.able = False
                resultado.append(["***%s usa  %s ***"%(self.nombre,sel.nombre),"yellow",self.x,self.y-self.height/2])
                return resultado
            else: return False
        else: 
            return [["*** ❌ %s no tiene objetos! ❌ ***" % (self.nombre),"gray",self.x,self.y-self.height/2]]

    def combo(self, oponente):
        print("\n *** %s alista un combo ..."%(self.nombre))
        if (self.puntos == 100):
            resultado = []
            print("%s%s ... COMBO ! 🌟%s"%(Style.BRIGHT,Fore.GREEN,Style.RESET_ALL))
            multi = random.randint(2,5)
            for i in range(multi): resultado.append(self.atacar(oponente,random.randint(20,30))[0])
            
            resultado.append([" ... COMBO ! x %s"%multi,"yellow",self.x,self.y-self.height/2])
            self.velx += 300
            self.puntos -= 100
            
            return resultado

        elif (self.puntos >=40):
            self.puntos -= 20
            print(" ... pero no logra completarlo")
            if (random.randint(0, 10) >= 7):
                return self.atacar(oponente,22)
            else: return [[" ... fallido","yellow",self.x,self.y-self.height/2]]
            
        else:
            print(
                "\n ... pero no tiene energia suficiente")
            if (random.randint(0, 10) >= 7): # si un combo se hace sin puntos, es posible que el usuario se haga daño
                print(Fore.RED+" ... %s se hirio a si mismo! %s-10hp💥%s" % (self.nombre,Fore.RED,Style.RESET_ALL))
                self.salud -= 10
                return[["-10hp","red",self.x,self.y-self.height/2]] #devolucion de mensajes
            else: return False

    def autoAct(self, oponente):
        # este condicional define las probabilidades de hacer una u otra accion, e imposibilita algunos en determinados casos 
        # cuantas mas veces se repita un valor, mas probable es que caiga
        opc=["1"]
        
        if self.vivo():
            
            if self.puntos >= 70:
                opc = ["1", "1", "1", "1", "1", "2", "3", "4", "4"]
            elif self.puntos >= 35:
                opc = ["1", "1", "1", "1","2", "2", "3", "4"]
            else:
                opc = ["1", "1", "2"]
            if self.salud <= self.saludMax*3/4 and len(self.bolsa) > 0: # si tiene menos de 3 cuartos de su salud maxima, podra intentar curarse
                opc.append("5")
            if self.salud <= self.saludMax/4:
                opc.append("2")
                opc.append("2")

            sel = random.choice(opc)  # la accion es aleatoria
            
            if   sel == "1": cool = 150; accion = self.atacar(oponente)
            elif sel == "2": cool = 150; accion = self.protect()
            elif sel == "3": cool = 200; accion = self.combo(oponente)
            elif sel == "4": cool = 250; accion = self.boost()
            elif sel == "5": cool = 400; accion = self.uBolsa(True)

            self.cool = math.floor(cool/(self.velocidad+1))
            return accion

    def act(self, oponente):
        if self.vivo():
 
            keys = pygame.key.get_pressed() 
            
            if keys[pygame.K_z]: cool = 0; self.desc(); accion =  False
            elif keys[pygame.K_x]: cool = 0; oponente.desc(); accion =  False
            elif keys[pygame.K_d]: 
                if self.enfrente(oponente): cool = 150; accion = self.atacar(oponente)
                else: cool = 0; accion =  self.protect()
            elif keys[pygame.K_a]:
                if self.enfrente(oponente): cool = 0; accion =  self.protect()
                else: cool = 150; accion = self.atacar(oponente)
            elif keys[pygame.K_s]: cool = 30; accion = self.boost() 
            elif keys[pygame.K_SPACE]: cool = 200; accion = self.combo(oponente)
            else: cool = 0; self.proteccion = False; accion = False; self.estado = "stand"
            if keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_3] or keys[pygame.K_4]: accion = self.uBolsa(False)
            
            self.cool = math.floor(cool/(self.velocidad+1))
            return accion

        else: self.cool = 0;return False

    def vivo(self):
        if (self.salud > 2):return True
        else: return False

    def mover(self,oponente,b=False):
        # cambio de posicion
        
        """
        if self.estado == "attack" and self.cool_m <= 1: 
            if self.enfrente(oponente):
                if not oponente.pos == self.pos+1 and self.pos<5: self.pos+=1
            if oponente.enfrente(self):
                if not oponente.pos == self.pos-1 and self.pos>1: self.pos-=1
        elif self.estado == "protect" and self.cool_m <= 1:
            if self.enfrente(oponente):
                if not oponente.pos == self.pos-1 and self.pos>1: self.pos-=1
            if oponente.enfrente(self):
                if not oponente.pos == self.pos+1 and self.pos<5: self.pos+=1
        """
        self.x += (self.pos * 115)
        

         # aceleracion
        
        if not b: self.x+=self.velx
        else: self.x-=self.velx
        
        if self.velx > 1 or self.velx < -1:
            self.velx-=self.velx/2
        else: self.velx = 0

        if self.cool_m > 1: self.cool_m -= 1

    def mover_adv(self,plyr = False):
        keys = pygame.key.get_pressed() 
        
        if keys[pygame.K_w]: self.vely = -10 
        if keys[pygame.K_d]: self.velx += 1  
        if keys[pygame.K_a]: self.velx -= 1 
        if keys[pygame.K_s]: self.vely += 1

        self.x += self.velx
        self.y += self.vely
        if self.vely <= -1: self.vely+=1 

    def enfrente(self,oponente):
        if oponente.pos > self.pos:
            return True
        else: return False
        if oponente.pos > self.pos and not oponente.pos == self.pos+1: self.pos += 1
        if oponente.pos < self.pos and not oponente.pos == self.pos-1: self.pos -= 1


items_base = {
    "te" : item("te",img="/te.png"),
    "tiza" : item("tiza",1,"usada para hacer cirulos",efectos=["atk","vel"],valores=[2,-3],consumible=False),
    "piedra filosofal" : item("piedra filosofal",1,efectos=["hp","vel","atk","def"],valores=[25,5,5,5],img="/piedra_filosofal.png"),
    "cebolla" : item("cebolla",2,efectos=["hp","def"],valores=[30,7],img="/cebolla.png"),
    "caramelo" : item("caramelo",2,efectos=["vel","atk","hp"],valores=[2,1,-5],img="/caramelo.png"),
    "imaginacion" : item("imaginacion",1,efectos=["hp","atk","def","vel"],valores=[50,50,50,50],consumible=False,img="/imaginacion.png"),  
    "hacha" : item("hacha",1,efectos=["atk","vel"],valores=[5,-3],consumible=False,img="/hacha.png"),
    "Dawn" : item("Dawn",1,efectos=["atk","def","vel"],valores=[3,4,2],img="/dawn.png"),
    "libro" : item("libro",1,efectos=["atk"],valores=[2],consumible=False,img="/libro.png"),
    "locura" : item("locura",2,efectos=["hp","atk","def"],valores=[-35,7,7],img="/locura.png"),
    "Soul" : item("Soul", 1,efectos=["hp","atk","def","pnt"],valores=[20,4,5,1],consumible=False,img="/soul.png"),

}   
personajes_base = [
    personaje(
        "des",100,2,100,10,[
            copy.copy(items_base["libro"])
            ],
            "des/"
    ),
    personaje(
        "test1",100,2,100,10,[
            copy.copy(items_base["tiza"]),
            items_base["imaginacion"],
            copy.copy(items_base["te"])
            ]
    ),
    
]
'''
    personaje("Alfonse", 400, 2, 5, 17,[
        copy.copy(items_base["te"]),
        copy.copy(items_base["tiza"]),
        copy.copy(items_base["piedra filosofal"]),
        ],"Alfonse/"),
    personaje("Shrek", 440, 1, 4, 15,[
        copy.copy(items_base["te"]),
        copy.copy(items_base["cebolla"]),
        copy.copy(items_base["caramelo"]),
        copy.copy(items_base["te"]),
        ],"Shrek/"),
    personaje("Pablo",200,1,2,18,[
        copy.copy(items_base["te"]),
        copy.copy(items_base["imaginacion"]),
        ],"Pablo/"),
    personaje("Kong",600,4,5,9,[
        copy.copy(items_base["te"]),
        copy.copy(items_base["hacha"]),
        copy.copy(items_base["Dawn"]),
        ],"Kong/"),
    personaje("Maka",330,2,3,17,[
        copy.copy(items_base["te"]),
        copy.copy(items_base["libro"]),
        copy.copy(items_base["Soul"]),
        copy.copy(items_base["locura"]),
        ],"Maka/"),
    personaje("Godzilla",14000,7,5,7,[
        copy.copy(items_base["te"]),
        ]),
    '''