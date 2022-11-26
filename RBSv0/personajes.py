#para correr el codigo ejecuta en terminal > py index.py
import time, random, math, pygame
from colorama import init,Fore,Style 

class item: # items que un personaje puede usar
    # el item por defecto es un té
    def __init__(self,nombre="item desconocido", cantidad=3, dialogo=("\n --- té refrescante que cura 35hp🍵"), efectos=["hp"], valores=[70],img="/desconocido.png",consumible=True,cool=300):
        self.id = " "
        self.usuario = " "
        self.nombre = nombre
        self.cantidad = cantidad
        self.dialogo = dialogo
        self.efectos = efectos
        self.valores = valores
        self.img = img
        self.consumible = consumible
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
                self.cantidad-=1
                if self.cantidad <= 0: self.able = False
            else: self.usando = True
            return [self.efectos,self.valores,colores]
        else: return [["none"],[0],["White"]]

class personaje: # clase para la construccion de los personajes

    def __init__(self, nombre, salud, ataque, defensa, velocidad,bolsa=["cancelar",item()],imgRoot="Shrek/"):
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
        self.bolsa = bolsa
        self.inventario = []
        self.proteccion = False # escudo
        self.puntosMax = 100
        self.puntos = 50 # energia, una mecanica de intercambio 
        self.estado = "/stand.png"
        self.imgRoot = imgRoot 
        self.imgAct = imgRoot+self.estado
        self.x = 0
        self.y = 0
        self.velx = 0
        self.alto = 0
        self.ancho = 280 
        self.cool = 120
        self.cool_h = 0

    def atacar(self, oponente, potencia=20):
        print("\n *** %s ataca..." % (self.nombre))
        
        multip = random.randint(85,115)/100
        dagno = math.ceil(multip*(potencia*(self.ataque/oponente.defensa)))
        self.velx = 100

        if (oponente.proteccion and multip < 1.10): # el ataqque es efectivo si el enemigo no se proteje
            print(" ... ataque inefectivo!❌ %s se ha %sprotegido💥%s" % (oponente.nombre,Fore.BLUE,Style.RESET_ALL))
            oponente.proteccion = False
            return [["-0hp","White",oponente.x,oponente.y]]
        else:
            oponente.velx = -20
            color = "orange"
            if multip >= 1.10: #critico
                print ("%s ... %s rompe las defenas de %s con un %s impacto critico❗%s"%(Fore.YELLOW,self.nombre,oponente.nombre,Style.BRIGHT,Style.RESET_ALL))
                oponente.proteccion = False
                crit = ["CRIT!","Red",oponente.x,oponente.y]
                color = "red"
            else: crit = False

            print("%s ... ataque efectivo!💥%s"%(Fore.LIGHTGREEN_EX,Style.RESET_ALL))
            print(" ... %s sufre %s%s-%shp💔%s" % (oponente.nombre,Style.BRIGHT,Fore.RED,dagno,Style.RESET_ALL))
            
            oponente.salud -= dagno
            
            if random.randint(0,10) >= 8: #puntos
                pnts = random.randint(1,10)
                self.puntos += pnts
                print(" ... %s : %s+%s puntos%s" % (self.nombre,Fore.GREEN,pnts,Style.RESET_ALL))
                pnt = ["+%sPnt"%pnts,"Blue",self.x,self.y]
                if self.puntos > self.puntosMax:
                    self.puntos = self.puntosMax
            else: pnt = False
            
            return[["-%shp"%(dagno),color,oponente.x,oponente.y],pnt,crit] #devolucion de mensajes
        
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
        for item in self.bolsa:
            if item != "cancelar": desc+="  -- %s. %s x%s \n"%(self.bolsa.index(item),item.nombre,item.cantidad)
        print("\n*** Descripcion de %s ***" % (self.nombre))    
        print(desc)
        print("*** ********************* ***\n")

    def protect(self): 
        self.proteccion = True
        print("\n *** %s %sse proteje!🛡️%s" % (self.nombre,Fore.BLUE,Style.RESET_ALL))

        return [["ESCUDO","Cyan",self.x,self.y]]

    def boost(self): # aumenta el poder del personaje
        print("\n *** %s medita... " %(self.nombre));msg = "+0"
        if (self.puntos >= 80):
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
            self.ataque += math.ceil(3/self.ataque)
            self.defensa += math.ceil(3/self.defensa)
            self.velocidad += math.ceil(18/self.velocidad)
            self.puntos -= 50

            return [["+%sAtk +%sDef +%sVel"
            % (math.ceil(3/self.ataque), math.ceil(3/self.defensa), math.ceil(18/self.velocidad)),"Green",self.x,self.y]] #devolucion de mensajes
        elif self.puntos >= 30:
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

            return [[msg,"Lightgreen",self.x,self.y]] #devolucion de mensajes
        else:
            print(" ... %s casi se queda dormido 😴\n" % (self.nombre))

            return [["+0","gray",self.x,self.y]] #devolucion de mensajes

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
                if sel.consumible: # si el item seleccionado es consumible
                    if self.cool_h > 1: return [False] # si aun se esta enfriendo, devuelve false
                    self.cool_h = sel.cool # sino, empieza el enfriamiento
                else:
                    self.ataque = self.ataque_base
                    self.defensa = self.defensa_base
                    self.defensa = self.ataque_base
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
                    resultado.append(["+ %s %s"%(uso[1][uso[0].index(efect)],efect),uso[2][uso[0].index(efect)],self.x,self.y])
                if sel.cantidad <= 0: sel.able = False
                resultado.append(["***%s usa  %s ***"%(self.nombre,sel.nombre),"yellow",self.x,self.y])
                return resultado
            else: return False
        else: 
            return [["*** ❌ %s no tiene objetos! ❌ ***" % (self.nombre),"gray",self.x,self.y]]

    def combo(self, oponente):
        print("\n *** %s alista un combo ..."%(self.nombre))
        if (self.puntos == 100):
            resultado = []
            print("%s%s ... COMBO ! 🌟%s"%(Style.BRIGHT,Fore.GREEN,Style.RESET_ALL))
            multi = random.randint(2,5)
            for i in range(multi): resultado.append(self.atacar(oponente,random.randint(18,26))[0])
            resultado.append(self.protect()[0])
            
            resultado.append([" ... COMBO ! x %s"%multi,"yellow",self.x,self.y])
            self.velx+=300
            self.puntos -= 100
            
            return resultado

        elif (self.puntos >=40):
            self.puntos -= 20
            print(" ... pero no logra completarlo")
            if (random.randint(0, 10) >= 7):
                return self.atacar(oponente,22)
            else: return [[" ... fallido","yellow",self.x,self.y]]
            
        else:
            print(
                "\n ... pero no tiene energia suficiente")
            if (random.randint(0, 10) >= 7): # si un combo se hace sin puntos, es posible que el usuario se haga daño
                print(Fore.RED+" ... %s se hirio a si mismo! %s-10hp💥%s" % (self.nombre,Fore.RED,Style.RESET_ALL))
                self.salud -= 10
                return[["-10hp","red",self.x,self.y]] #devolucion de mensajes
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
            
            
            if keys[pygame.K_z]:cool = 0; self.desc(); accion =  False
            elif keys[pygame.K_x]: cool = 0; oponente.desc(); accion =  False
            elif keys[pygame.K_d]: cool = 150; accion = self.atacar(oponente)
            elif keys[pygame.K_a]: cool = 0; accion =  self.protect()
            elif keys[pygame.K_s]: cool = 400; accion = self.boost() 
            elif keys[pygame.K_SPACE]: cool = 200; accion = self.combo(oponente)
            else: cool = 0; self.proteccion = False; accion = False
            if keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_3] or keys[pygame.K_4]: accion = self.uBolsa(False)

            self.cool = math.floor(cool/(self.velocidad+1))
            return accion

        else: self.cool = 0;return False

    def vivo(self):
        if (self.salud > 2):return True
        else: return False
    def mover(self,b=False):
        if not b: self.x+=self.velx
        else: self.x-=self.velx
        if self.velx > 1 or self.velx < -1:
            self.velx-=self.velx/2
        else: self.velx = 0

personajes = [
    personaje("Alfonse", 400, 2, 5, 17,[
        item("té",4,img="/te.png"),
        item("tiza",1,"usada para hacer cirulos",efectos=["atk","vel"],valores=[2,-3],consumible=False),
        item("piedra filosofal",1,efectos=["hp","vel","atk","def"],valores=[25,5,5,5],img="/piedra_filosofal.png")
        ],"Alfonse/"),
    personaje("Shrek", 440, 1, 4, 15,[
        item("té",img="/te.png"),
        item("cebolla",2,efectos=["hp","def"],valores=[30,7],img="/cebolla.png"),
        item("caramelo",2,efectos=["vel","atk","hp"],valores=[2,1,-5],img="/caramelo.png")
        ],"Shrek/"),
    personaje("Pablo",200,1,2,18,[
        item("té",9,img="/te.png"),
        item("imaginacion",1,efectos=["hp","atk","def","vel"],valores=[50,50,50,50],consumible=False,img="/imaginacion.png"),
        ],"Pablo/"),
    personaje("Kong",600,4,5,9,[
        item("te",1,img="/te.png"),
        item("hacha",1,efectos=["atk","vel"],valores=[5,-3],consumible=False,img="/hacha.png"),
        item("Dawn",1,efectos=["atk","def","vel"],valores=[3,4,2],img="/dawn.png")
        ],"Kong/"),
    personaje("Maka",330,2,3,17,[
        item("té",img="/te.png"),
        item("libro",1,efectos=["atk"],valores=[2],consumible=False,img="/libro.png"),
        item("locura",2,efectos=["hp","atk","def"],valores=[-35,7,7],img="/locura.png"),
        item("Soul", 1,efectos=["hp","atk","def","pnt"],valores=[20,4,5,1],consumible=False,img="/soul.png"),
        item("hacha",1,efectos=["atk","vel"],valores=[5,-3],consumible=False,img="/hacha.png"),
        ],"Maka/"),
    personaje("Godzilla",1400,7,5,7,[
        item(),
        ]),
]