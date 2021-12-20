from tkinter import *
from tkinter import ttk
from tkinter import messagebox as message
import DBgestor as DBG
import random 


class TriviaTest:
    def __init__(self, windows, path):
        self.DB = DBG.DBgestor(path)
        self.wind = windows
        self.wind.title("TriviaTest")
    
        self.userName = ""
        self.StringVar = ""
        self.nivel = 1 
        self.pregunta = ""
        self.opciones = ""
        self.respuesta = 0
        self.score = 0
        
    
        #Structure  
        self.ipadW = 40
        self.ipadH = 30
        NFrame = Label(self.wind).grid(row=0, column=1,  ipady=self.ipadH)
        WFrame = Label(self.wind).grid(row=0, column=0, rowspan=3, ipadx=self.ipadW)
        SFrame = Label(self.wind).grid(row=2, column=1,  ipady=self.ipadH)
        EFrame = Label(self.wind).grid(row=0, column=2, rowspan=3, ipadx=self.ipadW)

        self.login()

    def login(self):
        #login
        self.frameUser = LabelFrame(self.wind, text="Log in")
        self.EntryUser = Entry(self.frameUser)
        #Frame Label user
        self.frameUser.grid(row=1, column=1)
        #->Label user
        Label(self.frameUser, text="Nombre de usuario").grid(row=1, column=1 )
        #->Entry user
        self.EntryUser.grid(row=2, column=1, pady=10, padx=20 )
        #->Button Play
        ttk.Button(self.frameUser, text="Login", command=self.valideUser).grid(row=3, column=1)
    
    def password(self, login):
        self.StringVar = login
        #Frame Label password
        self.framePassw = LabelFrame(self.wind, text=self.StringVar)
        self.framePassw.grid(row=1, column=1)
        #->Label password
        Label(self.framePassw, text="Contraseña").grid(row=0, column=1 )
        #->Entry password
        self.EntryPassw = Entry(self.framePassw, show="*")
        self.EntryPassw.grid(row=1, column=1, pady=10, padx=20 )
        
        if self.StringVar=='Register':
            Label(self.framePassw, text="Nuevamente la contraseña").grid(row=2, column=1 )
            self.EntryPassw2 = Entry(self.framePassw, show="*")
            self.EntryPassw2.grid(row=3, column=1, pady=10, padx=20 )
            ttk.Button(self.framePassw, text=self.StringVar, command=self.registerPassW).grid(row=4, column=1)
        
        else:
            ttk.Button(self.framePassw, text=self.StringVar, command=self.validatePassW).grid(row=4, column=1)

    def game(self):    
        #game
        self.frameQuestion = LabelFrame(self.wind, text=self.userName)
        self.LabelLevel = Label(self.frameQuestion)
        self.LabelScore = Label(self.frameQuestion)
        self.LabelTries = Label(self.frameQuestion)
        self.LabelQuestion = Label(self.frameQuestion)
        self.LabelOption = Label(self.frameQuestion)
        self.EntryAnswer = Entry(self.frameQuestion)  
        
        
        self.frameQuestion.grid(row=1, column=1)

        self.LabelLevel.grid(row=0, column=0)
        self.LabelScore.grid(row=0, column=1)
        self.LabelTries.grid(row=0, column=2)
       
        self.LabelQuestion.grid(row=1, column=1,  rowspan=2, columnspan=3)
        self.LabelOption.grid(row=3, column=1, columnspan=3 )
        self.EntryAnswer.grid(row=5, column=1, pady=10, padx=20 )

        ttk.Button(self.frameQuestion, text="Responder", command=self.validateAnswer).grid(row=5, column=2)
        ttk.Button(self.frameQuestion, text="Retirarse",  command=self.retirarse).grid(row=5, column=3)
        ttk.Button(self.frameQuestion, text="salir", command=self.salir).grid(row=0, column=3)
        self.playGame()
    
    def podio(self):
        puestos = self.DB.topPodio()
        self.framePodio = LabelFrame(self.wind, text="Lo mejor de lo mejor").grid(row=1, column=1)
        if len(puestos)>=1:
            Label(self.framePodio, text="Primer puesto: ").grid(row=0, column=0)
            self.LabelPrimero = Label(self.framePodio, text=f"{puestos[0][1]}  puntaje: {puestos[0][3]}").grid(row=0, column=1)
        if len(puestos)>=2:
            Label(self.framePodio, text="Segundo puesto: ").grid(row=1, column=0)
            self.LabelPrimero = Label(self.framePodio, text=f"{puestos[1][1]}  puntaje: {puestos[1][3]}").grid(row=1, column=1)
        if len(puestos)>=3:
            Label(self.framePodio, text="Tercer puesto: ").grid(row=2, column=0)
            self.LabelPrimero = Label(self.framePodio, text=f"{puestos[2][1]}  puntaje: {puestos[2][3]}").grid(row=2, column=1)

        
        ttk.Button(self.framePodio, text="salir",  command=self.quit).grid(row=5, column=2)


    
    def destroid(self, frame):
        for i in frame.winfo_children():
            i.destroy()
        frame.destroy()

    def valideUser(self):
        user = self.EntryUser.get()
        self.userName = user
        sms2 = user + " no es un usuario registrado\n¿Desea registrarse?"
        sms3 = "Debe llenar el campo usuario"
        if user!="":
            if self.DB.existUser(user):
                self.destroid(self.frameUser)
                self.password('Login')
            else:
                ans = message.askquestion(message=sms2, title="iniciando partida")
                print(ans)
                if  ans == "yes":
                    self.destroid(self.frameUser)
                    self.password('Register')
                else:
                    self.EntryUser.delete(0,"end")
        else:
            message.showinfo(message=sms3, title="iniciando partida")

    def validatePassW(self):
        EpassW  = self.EntryPassw.get()
        DBpassW = self.DB.getPassW(self.userName)
        sms     = "La contraseña no es valida"
        sms1 = "Bienvenido a TrivaTest "
        if DBpassW==EpassW:
            message.showinfo(message=sms1, title="iniciando partida")
            self.destroid(self.framePassw )
            self.game()
        else:
            message.showwarning(message=sms, title="Password Error")
            self.EntryPassw.delete(0,"end")


    def registerPassW(self):
        passw1 = self.EntryPassw.get()
        passw2 = self.EntryPassw2.get()

        if passw1 == passw2 and passw1!="":
            sms = f"Se realizó el egistro de usuario:\nName: {self.userName}\nScore: 0\nTries: 0"
            self.DB.insertUser(self.userName, passw1, 0, 0)
            message.showinfo(message=sms,  title="Register user")
            self.destroid(self.framePassw)
            self.game()
        else:
            sms = "No coinciden las contraseñas"
            message.showerror(message=sms, title="Error password")
            self.EntryPassw2.delete(0,"end")
        
        

    def fillInteface(self, ID):
        datos = self.DB.loadQuestions(ID)[0]
        self.tries = self.DB.loadUser(self.userName)[4] + 1
        
        self.nivel = datos[1]
        self.pregunta = datos[2]
        self.opciones = datos[3]
        self.respuesta = datos[4]
        
        self.LabelLevel['text'] = 'Nivel: ' + str(self.nivel)
        self.LabelScore['text'] = 'Puntaje: ' + str(self.score)
        self.LabelTries['text'] = 'Intentos: ' + str(self.tries)
        self.LabelQuestion['text'] = self.pregunta 
        self.LabelOption['text'] = self.opciones
 
        

    def playGame(self):
        if self.nivel == 1:
            ID = random.randrange(1,6)
        elif self.nivel == 2:
            ID = random.randrange(6,11)
        elif self.nivel == 3:
            ID = random.randrange(11, 16)
        elif self.nivel == 4:
            ID = random.randrange(16, 21)
        elif self.nivel == 5:
            ID = random.randrange(21, 26)
        self.fillInteface(ID)
        self.EntryAnswer.delete(0,"end")

    def validateAnswer(self):
        ans = self.EntryAnswer.get()
        if ans == str(self.respuesta):
            self.score += self.nivel*10
            self.nivel += 1
            if self.nivel > 5:
                self.winPlay()
            else:
                self.playGame()
        else:
            sms = "Perdiste :('"
            self.score = 0
            message.showinfo(message=sms, title="Game over")
            self.destroid(self.frameQuestion)
            self.DB.updateUser(self.userName, self.score, self.tries)
            self.podio()
            
    
    def winPlay(self):
        self.DB.updateUser(self.userName, self.score, self.tries)
        sms = f"{self.userName} has ganado!!!\nPuntaje: {self.score}\nintentos: {self.tries}"
        message.showinfo(message=sms, title="You win")
        self.destroid(self.frameQuestion)
        self.podio()
        
    def retirarse(self):
        sms = "¿Deseas retirarte de la partida?"
        r = message.askquestion(message=sms, title="You win")
        if r == "yes":
            self.DB.updateUser(self.userName, self.score, self.tries)
            self.destroid(self.frameQuestion)
            self.podio()
    
    def salir(self):
        sms = "¿Deseas salira?"
        r = message.askquestion(message=sms, title="You win")
        if r == "yes":
            self.DB.updateUser(self.userName, 0, self.tries)
            self.destroid(self.frameQuestion)
            self.podio()
            
    
    def quit(self):
        global root
        root.quit()
        
        

if __name__ == "__main__":
    root = Tk()
    Aplication = TriviaTest(root,'triviaTest.db')
    root.mainloop()