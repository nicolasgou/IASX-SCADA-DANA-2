import customtkinter as ctk



#images
from PIL import Image, ImageTk, ImageEnhance
import os

#Graficos
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
from datetime import datetime
import matplotlib.dates as mdates

#LOCALs Imports
from clp_manager import CLPClient
from db_maneger import insert_dados


global IDProdlVal, CODCorrVal, PressCargVal, MotorAmpsVal, TempFornoVal, MatrixAltVal


class AppGUI(ctk.CTk):


    def __init__(self, clp_client, timer, frameWidth, app_size):

        def keepCommand():
            return

        # Define aparência e tema antes de criar a janela Ctk
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        super().__init__()# inicializa a Janela CTK

        self.clp = clp_client
        self.timer = timer

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        #app setup
        self.title("IASX Tecnologia - MONITORAMENTO LINHA RUSSA")
        self.iconbitmap(default='./assets/app.ico') # Definindo o ícone (apenas .ico no Windows)
        app_logo = ctk.CTkImage(Image.open(os.path.join('./assets/', "appLogo.png")), size=(130, 70))
        temp_ico = ctk.CTkImage(Image.open(os.path.join('./assets/', "temp_ico.png")), size=(50, 50))
        press_img = ctk.CTkImage(Image.open(os.path.join('./assets/', "press_img.png")), size=(300, 400))
        self.geometry(f"{app_size[0]}x{app_size[1]}") #app.geometry("1024x768")
        self._state_before_windows_set_titlebar_color = 'zoomed' # set Windows initial state to Maximized
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((1,2), weight=1)
        self.grid_rowconfigure((0,3,4), weight=0)
        #app.grid_rowconfigure((0,1,2,3,4), weight=1)

        #####################################################################################
        ########################## layout_monitor 
        #####################################################################################

        ########################## FRA_APP_TITLE
        self.FRA_APP_TITLE = ctk.CTkFrame(self, corner_radius=0)
        self.FRA_APP_TITLE.grid(row=0, column=0, pady=5, padx=5, sticky="new", columnspan=2)
        self.FRA_APP_TITLE.grid_columnconfigure((0, 1), weight=1)

        self.lbl_appTitle = ctk.CTkLabel(self.FRA_APP_TITLE, text="MONITORAMENTO LINHA RUSSA", justify="center", compound="center", anchor="center",font=ctk.CTkFont(size=50, weight="bold"))
        self.lbl_appTitle.grid(row=0, column=0, padx=20, pady=20, columnspan=2,sticky="nwes")

        self.lbl_appLogo = ctk.CTkLabel(self.FRA_APP_TITLE, text = "",
                                        image=(app_logo),
                                        compound="center",
                                        anchor="center")
        self.lbl_appLogo.grid(row=0, column=2, columnspan=2,sticky="w")

        ########################## FRA_MON_VAR
        self.FRA_MON_VAR = ctk.CTkFrame(self, corner_radius=0)
        self.FRA_MON_VAR.grid(row=1, column=0, pady=5, padx=5, columnspan=2,sticky="new")
        self.FRA_MON_VAR.grid_columnconfigure((0, 1, 2,3,4), weight=1)  
        self.FRA_MON_VAR.grid_rowconfigure((0,1), weight=1)


        self.FRA_PROC_ATUAL = ctk.CTkFrame(self.FRA_MON_VAR, corner_radius=0, fg_color="white")
        self.FRA_PROC_ATUAL.grid(row=0, column=0,sticky="nw", pady=10, padx=10)
        self.FRA_PROC_ATUAL.grid_columnconfigure((0, 1), weight=1)
        self.lbl_ProcAtualTitle = ctk.CTkLabel(self.FRA_PROC_ATUAL,pady=5, padx=5, text="PROCESSAO ATUAL",bg_color="gray", text_color="white",anchor="center", font=('', 18),width=frameWidth) 
        self.lbl_ProcAtualTitle.grid(row=0, column=0, pady=5, padx=5,columnspan=2,sticky="ew")
        
        self.lbl_IDProdTitle = ctk.CTkLabel(self.FRA_PROC_ATUAL,pady=5, padx=5, text="ID PRODUTO", text_color="gray",anchor="w", font=('', 18)) 
        self.lbl_IDProdTitle.grid(row=1, column=0, pady=5, padx=5,columnspan=1,sticky="ew")
        self.lbl_IDProdlVal = ctk.CTkLabel(self.FRA_PROC_ATUAL, text="????????", justify="left", compound="left", anchor="w",font=ctk.CTkFont(size=25, weight="bold") )
        self.lbl_IDProdlVal.grid(row=2, column=0, pady=5, padx=5, sticky="w")

        self.lbl_CODCorrTitle = ctk.CTkLabel(self.FRA_PROC_ATUAL,pady=5, padx=5, text="COD. CORRIDA", text_color="gray",anchor="w", font=('', 18)) 
        self.lbl_CODCorrTitle.grid(row=3, column=0, pady=5, padx=5,columnspan=1,sticky="ew")
        self.lbl_CODCorrVal = ctk.CTkLabel(self.FRA_PROC_ATUAL, text="????????", justify="left", compound="left", anchor="w",font=ctk.CTkFont(size=25, weight="bold") )
        self.lbl_CODCorrVal.grid(row=4, column=0, pady=5, padx=5, sticky="w")

        self.FRA_TEMP_FORNO = ctk.CTkFrame(self.FRA_MON_VAR, corner_radius=0, fg_color="white")
        self.FRA_TEMP_FORNO.grid(row=1, column=0,sticky="nw", pady=10, padx=10)
        self.FRA_TEMP_FORNO.grid_columnconfigure((0, 1,2), weight=1)
        self.lbl_TempFornoTitle = ctk.CTkLabel(self.FRA_TEMP_FORNO,pady=5, padx=5, text="TEMPERATURA FORNO",bg_color="gray", text_color="white",anchor="center", font=('', 18),width=frameWidth) 
        self.lbl_TempFornoTitle.grid(row=0, column=0, pady=5, padx=5,columnspan=3,sticky="ew")
        self.lbl_TempFornoVal = ctk.CTkLabel(self.FRA_TEMP_FORNO, image=(temp_ico), text="????????", justify="center", compound="left", anchor="e",font=ctk.CTkFont(size=25, weight="bold") )
        self.lbl_TempFornoVal.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        self.lbl_TempFornoUnit = ctk.CTkLabel(self.FRA_TEMP_FORNO,pady=5, padx=5, text="ºC",anchor="center", text_color="gray",font=('', 18)) 
        self.lbl_TempFornoUnit.grid(row=1, column=2, pady=5, padx=5,sticky="e")

        self.FRA_PRESS_CARG = ctk.CTkFrame(self.FRA_MON_VAR, corner_radius=0, fg_color="white")
        self.FRA_PRESS_CARG.grid(row=0, column=1,sticky="nw", pady=10, padx=10)
        self.FRA_PRESS_CARG.grid_columnconfigure((0, 1,2), weight=1)
        self.lbl_PressCargTitle = ctk.CTkLabel(self.FRA_PRESS_CARG,pady=5, padx=5, text="PRESSAO DA CARGA",bg_color="gray", text_color="white",anchor="center", font=('', 18),width=frameWidth) 
        self.lbl_PressCargTitle.grid(row=0, column=0, pady=5, padx=5,columnspan=3,sticky="ew")
        self.lbl_PressCargVal = ctk.CTkLabel(self.FRA_PRESS_CARG, image=(temp_ico), text="????????", justify="center", compound="left", anchor="e",font=ctk.CTkFont(size=25, weight="bold") )
        self.lbl_PressCargVal.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        self.lbl_PressCargUnit = ctk.CTkLabel(self.FRA_PRESS_CARG,pady=5, padx=5, text="KN",anchor="center", text_color="gray",font=('', 18)) 
        self.lbl_PressCargUnit.grid(row=1, column=2, pady=5, padx=5,sticky="e")

        self.FRA_PRESS_IMG = ctk.CTkFrame(self.FRA_MON_VAR, corner_radius=0, fg_color="white")
        self.FRA_PRESS_IMG.grid(row=0, column=2, rowspan=2, sticky="new")
        self.FRA_PRESS_IMG.grid_columnconfigure(0, weight=1)
        self.FRA_PRESS_IMG.grid_rowconfigure(0, weight=1)
        self.lbl_pressImg = ctk.CTkLabel(self.FRA_PRESS_IMG, text = "",
                                        image=(press_img),
                                        compound="center",
                                        anchor="center")
        self.lbl_pressImg.grid(row=0, column=0, sticky="nswe")

        self.FRA_MOTOR_AMPS = ctk.CTkFrame(self.FRA_MON_VAR, corner_radius=0, fg_color="white")
        self.FRA_MOTOR_AMPS.grid(row=0, column=3,sticky="ne", pady=10, padx=10)
        self.FRA_MOTOR_AMPS.grid_columnconfigure((0, 1,2), weight=1)
        self.lbl_MotorAmpsTitle = ctk.CTkLabel(self.FRA_MOTOR_AMPS,pady=5, padx=5, text="CORRENTE MOTOR",bg_color="gray", text_color="white",anchor="center", font=('', 18),width=frameWidth) 
        self.lbl_MotorAmpsTitle.grid(row=0, column=0, pady=5, padx=5,columnspan=3,sticky="ew")
        self.lbl_MotorAmpsVal = ctk.CTkLabel(self.FRA_MOTOR_AMPS, image=(temp_ico), text="????????", justify="center", compound="left", anchor="e",font=ctk.CTkFont(size=25, weight="bold") )
        self.lbl_MotorAmpsVal.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        self.lbl_MotorAmpsUnit = ctk.CTkLabel(self.FRA_MOTOR_AMPS,pady=5, padx=5, text="Amps",anchor="center", text_color="gray",font=('', 18)) 
        self.lbl_MotorAmpsUnit.grid(row=1, column=2, pady=5, padx=5,sticky="e")


        self.FRA_MATRIX_ALT = ctk.CTkFrame(self.FRA_MON_VAR, corner_radius=0, fg_color="white")
        self.FRA_MATRIX_ALT.grid(row=1, column=4,sticky="ne", pady=10, padx=10)
        self.FRA_MATRIX_ALT.grid_columnconfigure((0, 1,2), weight=1)
        self.lbl_MatrixAltTitle = ctk.CTkLabel(self.FRA_MATRIX_ALT,pady=5, padx=5, text="ALTURA DA MATRIZ",bg_color="gray", text_color="white",anchor="center", font=('', 18),width=frameWidth) 
        self.lbl_MatrixAltTitle.grid(row=0, column=0, pady=5, padx=5,columnspan=3,sticky="ew")
        self.lbl_MatrixAltVal = ctk.CTkLabel(self.FRA_MATRIX_ALT, image=(temp_ico), text="????????", justify="center", compound="left", anchor="e",font=ctk.CTkFont(size=25, weight="bold") )
        self.lbl_MatrixAltVal.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        self.lbl_MatrixAltUnit = ctk.CTkLabel(self.FRA_MATRIX_ALT,pady=5, padx=5, text="mm",anchor="center", text_color="gray",font=('', 18)) 
        self.lbl_MatrixAltUnit.grid(row=1, column=2, pady=5, padx=51,sticky="e")

        ########################## FRA_MON_GRAPHS
        self.FRA_MON_GRAPHS = ctk.CTkFrame(self, corner_radius=0)
        self.FRA_MON_GRAPHS.grid(row=2, column=0, pady=5, padx=5, columnspan=2,sticky="nsew")
        self.FRA_MON_GRAPHS.grid_columnconfigure((0, 1, 2), weight=1)  
        self.FRA_MON_GRAPHS.grid_rowconfigure(0, weight=0)
        self.FRA_MON_GRAPHS.grid_rowconfigure(1, weight=1)
        self.lbl_MonGraphTitle = ctk.CTkLabel(self.FRA_MON_GRAPHS,pady=5, padx=5, text="HISTORICO (24hrs)",bg_color="gray", text_color="white",anchor="center", font=('', 18),width=frameWidth) 
        self.lbl_MonGraphTitle.grid(row=0, column=0, pady=5, padx=5,columnspan=3,sticky="ew")  

        #Monta grafico temperatura Forno
        # armazenamento historico para os graficos
        self.TempFornoHist = deque(maxlen=50)
        self.TempFornoTime = deque(maxlen=50)

        # Gráfico Temperatura Forno
        self.TempFornoFig = Figure(figsize=(5, 3))
        self.TempFornoAx = self.TempFornoFig.add_subplot(111)
        self.TempFornoLine, = self.TempFornoAx.plot_date([], [], label="Temperatura Forno", fmt='r-', linewidth=2)

        self.TempFornoAx.set_title("Temperatura do Forno")
        self.TempFornoAx.set_xlabel("Hora")
        self.TempFornoAx.set_ylabel("Temperatura (°C)")
        self.TempFornoAx.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.TempFornoAx.legend()
        self.TempFornoAx.grid(True)

        self.TempFornoCanvas = FigureCanvasTkAgg(self.TempFornoFig, master=self.FRA_MON_GRAPHS)
        self.TempFornoCanvas.get_tk_widget().grid(row=1, column=0,sticky="w",pady=5, padx=5)

        #Monta grafico pressao da Carga
        # armazenamento historico para os graficos
        self.PressCargHist = deque(maxlen=50)
        self.PressCargTime = deque(maxlen=50)

        # Gráfico Pressao da Carga
        self.PressCargFig = Figure(figsize=(5, 3))
        self.PressCargAx = self.PressCargFig.add_subplot(111)
        self.PressCargLine, = self.PressCargAx.plot_date([], [], label="Pressao da Carga", fmt='b-', linewidth=2)

        self.PressCargAx.set_title("Pressao da Carga")
        self.PressCargAx.set_xlabel("Hora")
        self.PressCargAx.set_ylabel("Pressao (KN)")
        self.PressCargAx.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.PressCargAx.legend()
        self.PressCargAx.grid(True)

        self.PressCargCanvas = FigureCanvasTkAgg(self.PressCargFig, master=self.FRA_MON_GRAPHS)
        self.PressCargCanvas.get_tk_widget().grid(row=1, column=1,sticky="ew",pady=5, padx=5)

        #Monta grafico Corrente Motor
        # armazenamento historico para os graficos
        self.MotorAmpsHist = deque(maxlen=50)
        self.MotorAmpsTime = deque(maxlen=50)

        self.MotorAmpsFig = Figure(figsize=(5, 3))
        self.MotorAmpsAx = self.MotorAmpsFig.add_subplot(111)
        self.MotorAmpsLine, = self.MotorAmpsAx.plot_date([], [], label="Corrente Motor", fmt='g-', linewidth=2)

        self.MotorAmpsAx.set_title("Corrente Motor")
        self.MotorAmpsAx.set_xlabel("Hora")
        self.MotorAmpsAx.set_ylabel("Corrente (Amps)")
        self.MotorAmpsAx.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.MotorAmpsAx.legend()
        self.MotorAmpsAx.grid(True)

        self.MotorAmpsCanvas = FigureCanvasTkAgg(self.MotorAmpsFig, master=self.FRA_MON_GRAPHS)
        self.MotorAmpsCanvas.get_tk_widget().grid(row=1, column=2,sticky="e",pady=5, padx=5) 


        ########################## FRA_APP_BUTT
        self.FRA_APP_BUTT = ctk.CTkFrame(self, corner_radius=0)
        self.FRA_APP_BUTT.grid(row=3, column=0, pady=5, padx=5, columnspan=2,sticky="sew")
        self.FRA_APP_BUTT.grid_columnconfigure((0, 1, 2), weight=1)  
        self.FRA_APP_BUTT.grid_rowconfigure(0, weight=1)

        self.btn_monitor = ctk.CTkButton(self.FRA_APP_BUTT, text="MONITOR", state="disabled", anchor="center", height=50, width=250,font=ctk.CTkFont(size=20, weight="bold"),corner_radius=10,command=keepCommand)
        self.btn_monitor.grid(row=0, column=0, pady=5, padx=5, sticky="w")

        self.btn_historico = ctk.CTkButton(self.FRA_APP_BUTT, text="HISTORICO", state="disabled", anchor="center", height=50, width=250,font=ctk.CTkFont(size=20, weight="bold"),corner_radius=10,command=keepCommand)
        self.btn_historico.grid(row=0, column=1, pady=5, padx=5)

        self.btn_export = ctk.CTkButton(self.FRA_APP_BUTT, text="EXPORTAR", state="disabled", anchor="center", height=50, width=250,font=ctk.CTkFont(size=20, weight="bold"),corner_radius=10,command=keepCommand)
        self.btn_export.grid(row=0, column=2, pady=5, padx=5, sticky="e")

        ########################## FRA_APP_STATUS
        self.FRA_APP_STATUS = ctk.CTkFrame(self, corner_radius=0)
        self.FRA_APP_STATUS.grid(row=4, column=0, pady=5,sticky="sew", columnspan=2)
        self.FRA_APP_STATUS.grid_columnconfigure((0, 1), weight=1)

        self.lbl_status = ctk.CTkLabel(self.FRA_APP_STATUS, text="STATUS AQUI!!!", anchor="w", font=ctk.CTkFont(size=14, weight="bold"), text_color="white", bg_color="red", pady=5, padx=5)
        self.lbl_status.grid(row=0, column=0, pady=5, padx=5, columnspan=2,sticky="ew")

        self.update_data()


    ######################################################################################################
    ############################### ROTINA PERIODICA DE ATULIZACAO DE DADOS ##############################
    ######################################################################################################
    def update_data(self):
        if self.clp.is_connected():
            try:
                IDProdlVal = self.clp.read_string(db_number=2, start_byte=0, max_length = 20)
                self.lbl_IDProdlVal.configure(text=IDProdlVal)
                ###############################################################################
                CODCorrVal = self.clp.read_string(db_number=2, start_byte=22,max_length = 20)
                self.lbl_CODCorrVal.configure(text=CODCorrVal)
                ###############################################################################
                TempFornoVal = self.clp.read_real(db_number=2, start_byte=52)
                if TempFornoVal is not None:
                    self.lbl_TempFornoVal.configure(text=f"{TempFornoVal:.2f}")# Atualiza label com valor
                    # Atualiza histórico e gráfico
                    now = datetime.now()
                    self.TempFornoTime.append(now)
                    self.TempFornoHist.append(TempFornoVal)

                    self.TempFornoLine.set_data(self.TempFornoTime, self.TempFornoHist)

                    self.TempFornoAx.relim()
                    self.TempFornoAx.autoscale_view()

                    self.TempFornoCanvas.draw()
                else:
                    self.lbl_TempFornoVal.configure(text=f"---------")
                ###############################################################################
                PressCargVal = self.clp.read_real(db_number=2, start_byte=44)
                if PressCargVal is not None:
                    self.lbl_PressCargVal.configure(text=f"{PressCargVal:.2f}") # Atualiza label com valor
                    # Atualiza histórico e gráfico
                    now = datetime.now()
                    self.PressCargTime.append(now)
                    self.PressCargHist.append(PressCargVal)

                    self.PressCargLine.set_data(self.PressCargTime, self.PressCargHist)

                    self.PressCargAx.relim()
                    self.PressCargAx.autoscale_view()

                    self.PressCargCanvas.draw()
                else:
                    self.lbl_PressCargVal.configure(text=f"---------")
                ###############################################################################
                MotorAmpsVal = self.clp.read_real(db_number=2, start_byte=48)
                if MotorAmpsVal is not None:
                    self.lbl_MotorAmpsVal.configure(text=f"{MotorAmpsVal:.2f}") # Atualiza label com valor
                    # Atualiza histórico e gráfico
                    now = datetime.now()
                    self.MotorAmpsTime.append(now)
                    self.MotorAmpsHist.append(MotorAmpsVal)

                    self.MotorAmpsLine.set_data(self.MotorAmpsTime, self.MotorAmpsHist)

                    self.MotorAmpsAx.relim()
                    self.MotorAmpsAx.autoscale_view()

                    self.MotorAmpsCanvas.draw()
                else:
                    self.lbl_MotorAmpsVal.configure(text=f"---------")
                ###############################################################################
                MatrixAltVal = self.clp.read_real(db_number=2, start_byte=56)
                self.lbl_MatrixAltVal.configure(text=f"{MatrixAltVal:.2f}")
                
                self.lbl_status.configure(text="[OK] COMUNICACAO OK",bg_color="green")#Atualiza STATUS
            except Exception as e:
                self.lbl_status.configure(text="[Falha] Aquisicao Variaveis do CLP",bg_color="red")#Atualiza STATUS
                print(f"Erro na update_data {e}")
        else:
            self.lbl_status.configure(text="[Falha] CONEXAO CLP",bg_color="red")#Atualiza STATUS
            print(f"Erro conexao CLP")

        self.after(self.timer * 1000, self.update_data)  # Atualiza a cada <timer> segundo

