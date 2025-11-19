import customtkinter as ctk
from collections import deque
from datetime import datetime
import os

# Optional PIL (images)
try:
    from PIL import Image
    HAS_PIL = True
except Exception:
    HAS_PIL = False

# Optional Matplotlib (graphs)
try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.dates as mdates
    HAS_MPL = True
except Exception:
    HAS_MPL = False


class MonitorFrame(ctk.CTkFrame):
    def __init__(self, parent, plc_client):

        super().__init__(parent)
        self.pack(expand=True, fill="both", padx=10, pady=10)
        self.plc_client = plc_client

        # Layout config similar to monitor-2.py
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((1, 2), weight=1)
        self.grid_rowconfigure((0, 3, 4), weight=0)

        # Assets
        self._app_logo = None
        self._temp_icon = None
        self._press_img = None
        assets_dir = os.path.join('.', 'assets')
        if HAS_PIL and os.path.isdir(assets_dir):
            try:
                self._app_logo = ctk.CTkImage(Image.open(os.path.join(assets_dir,'logo', 'appLogo.png')), size=(130, 70))
            except Exception:
                self._app_logo = None
            try:
                self._temp_icon = ctk.CTkImage(Image.open(os.path.join(assets_dir,'icons', 'temp_ico.png')), size=(50, 50))
            except Exception:
                self._temp_icon = None
            try:
                self._press_img = ctk.CTkImage(Image.open(os.path.join(assets_dir,'imgs', 'press_img.png')), size=(300, 400))
            except Exception:
                self._press_img = None

        # FRA_APP_TITLE
        self.FRA_APP_TITLE = ctk.CTkFrame(self, corner_radius=0, fg_color="white")
        self.FRA_APP_TITLE.grid(row=0, column=0, pady=5, padx=5, sticky="new", columnspan=2)
        self.FRA_APP_TITLE.grid_columnconfigure((0, 1), weight=1)

        self.lbl_appTitle = ctk.CTkLabel(
            self.FRA_APP_TITLE,
            text="MONITORAMENTO LINHA RUSSA",
            justify="center",
            compound="center",
            anchor="center",
            font=ctk.CTkFont(size=32, weight="bold"),
        )
        self.lbl_appTitle.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="nwes")

        self.lbl_appLogo = ctk.CTkLabel(
            self.FRA_APP_TITLE,
            text="",
            image=self._app_logo if self._app_logo else None,
            compound="center",
            anchor="center",
        )
        self.lbl_appLogo.grid(row=0, column=2, columnspan=2, sticky="w")

        # FRA_MON_VAR
        self.FRA_MON_VAR = ctk.CTkFrame(self, corner_radius=0, fg_color="white")
        self.FRA_MON_VAR.grid(row=1, column=0, pady=5, padx=5, columnspan=2, sticky="new")
        self.FRA_MON_VAR.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.FRA_MON_VAR.grid_rowconfigure((0, 1), weight=1)

        # FRA_PROC_ATUAL
        self.FRA_PROC_ATUAL = ctk.CTkFrame(self.FRA_MON_VAR, corner_radius=0, fg_color="white")
        self.FRA_PROC_ATUAL.grid(row=0, column=0, sticky="nw", pady=10, padx=10)
        self.FRA_PROC_ATUAL.grid_columnconfigure((0, 1), weight=1)
        self.lbl_ProcAtualTitle = ctk.CTkLabel(
            self.FRA_PROC_ATUAL,
            pady=5,
            padx=5,
            text="PROCESSAO ATUAL",
            bg_color="gray",
            text_color="white",
            anchor="center",
            font=("", 16),
        )
        self.lbl_ProcAtualTitle.grid(row=0, column=0, pady=5, padx=5, columnspan=2, sticky="ew")

        self.lbl_IDProdTitle = ctk.CTkLabel(
            self.FRA_PROC_ATUAL, pady=5, padx=5, text="ID PRODUTO", text_color="gray", anchor="w", font=("", 14)
        )
        self.lbl_IDProdTitle.grid(row=1, column=0, pady=5, padx=5, sticky="ew")
        self.lbl_IDProdlVal = ctk.CTkLabel(
            self.FRA_PROC_ATUAL, text="--------", justify="left", compound="left", anchor="w", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.lbl_IDProdlVal.grid(row=2, column=0, pady=5, padx=5, sticky="w")

        self.lbl_CODCorrTitle = ctk.CTkLabel(
            self.FRA_PROC_ATUAL, pady=5, padx=5, text="COD. CORRIDA", text_color="gray", anchor="w", font=("", 14)
        )
        self.lbl_CODCorrTitle.grid(row=3, column=0, pady=5, padx=5, sticky="ew")
        self.lbl_CODCorrVal = ctk.CTkLabel(
            self.FRA_PROC_ATUAL, text="--------", justify="left", compound="left", anchor="w", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.lbl_CODCorrVal.grid(row=4, column=0, pady=5, padx=5, sticky="w")

        # FRA_TEMP_FORNO
        self.FRA_TEMP_FORNO = ctk.CTkFrame(self.FRA_MON_VAR, corner_radius=0, fg_color="white")
        self.FRA_TEMP_FORNO.grid(row=1, column=0, sticky="nw", pady=10, padx=10)
        self.FRA_TEMP_FORNO.grid_columnconfigure((0, 1, 2), weight=1)
        self.lbl_TempFornoTitle = ctk.CTkLabel(
            self.FRA_TEMP_FORNO, pady=5, padx=5, text="TEMPERATURA FORNO", bg_color="gray", text_color="white", anchor="center", font=("", 16)
        )
        self.lbl_TempFornoTitle.grid(row=0, column=0, pady=5, padx=5, columnspan=3, sticky="ew")
        self.lbl_TempFornoVal = ctk.CTkLabel(
            self.FRA_TEMP_FORNO,
            image=self._temp_icon if self._temp_icon else None,
            text="---------",
            justify="center",
            compound="left",
            anchor="e",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.lbl_TempFornoVal.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        self.lbl_TempFornoUnit = ctk.CTkLabel(self.FRA_TEMP_FORNO, pady=5, padx=5, text="°C", anchor="center", text_color="gray", font=("", 14))
        self.lbl_TempFornoUnit.grid(row=1, column=2, pady=5, padx=5, sticky="e")

        # FRA_PRESS_CARG
        self.FRA_PRESS_CARG = ctk.CTkFrame(self.FRA_MON_VAR, corner_radius=0, fg_color="white")
        self.FRA_PRESS_CARG.grid(row=0, column=1, sticky="nw", pady=10, padx=10)
        self.FRA_PRESS_CARG.grid_columnconfigure((0, 1, 2), weight=1)
        self.lbl_PressCargTitle = ctk.CTkLabel(
            self.FRA_PRESS_CARG, pady=5, padx=5, text="PRESSAO DA CARGA", bg_color="gray", text_color="white", anchor="center", font=("", 16)
        )
        self.lbl_PressCargTitle.grid(row=0, column=0, pady=5, padx=5, columnspan=3, sticky="ew")
        self.lbl_PressCargVal = ctk.CTkLabel(
            self.FRA_PRESS_CARG,
            image=self._temp_icon if self._temp_icon else None,
            text="---------",
            justify="center",
            compound="left",
            anchor="e",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.lbl_PressCargVal.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        self.lbl_PressCargUnit = ctk.CTkLabel(self.FRA_PRESS_CARG, pady=5, padx=5, text="KN", anchor="center", text_color="gray", font=("", 14))
        self.lbl_PressCargUnit.grid(row=1, column=2, pady=5, padx=5, sticky="e")

        # FRA_PRESS_IMG
        self.FRA_PRESS_IMG = ctk.CTkFrame(self.FRA_MON_VAR, corner_radius=0, fg_color="white")
        self.FRA_PRESS_IMG.grid(row=0, column=2, rowspan=2, sticky="new")
        self.FRA_PRESS_IMG.grid_columnconfigure(0, weight=1)
        self.FRA_PRESS_IMG.grid_rowconfigure(0, weight=1)
        self.lbl_pressImg = ctk.CTkLabel(
            self.FRA_PRESS_IMG,
            text="",
            image=self._press_img if self._press_img else None,
            compound="center",
            anchor="center",
        )
        self.lbl_pressImg.grid(row=0, column=0, sticky="nswe")

        # FRA_MOTOR_AMPS
        self.FRA_MOTOR_AMPS = ctk.CTkFrame(self.FRA_MON_VAR, corner_radius=0, fg_color="white")
        self.FRA_MOTOR_AMPS.grid(row=0, column=3, sticky="ne", pady=10, padx=10)
        self.FRA_MOTOR_AMPS.grid_columnconfigure((0, 1, 2), weight=1)
        self.lbl_MotorAmpsTitle = ctk.CTkLabel(
            self.FRA_MOTOR_AMPS, pady=5, padx=5, text="CORRENTE MOTOR", bg_color="gray", text_color="white", anchor="center", font=("", 16)
        )
        self.lbl_MotorAmpsTitle.grid(row=0, column=0, pady=5, padx=5, columnspan=3, sticky="ew")
        self.lbl_MotorAmpsVal = ctk.CTkLabel(
            self.FRA_MOTOR_AMPS,
            image=self._temp_icon if self._temp_icon else None,
            text="---------",
            justify="center",
            compound="left",
            anchor="e",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.lbl_MotorAmpsVal.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        self.lbl_MotorAmpsUnit = ctk.CTkLabel(self.FRA_MOTOR_AMPS, pady=5, padx=5, text="Amps", anchor="center", text_color="gray", font=("", 14))
        self.lbl_MotorAmpsUnit.grid(row=1, column=2, pady=5, padx=5, sticky="e")

        # FRA_MATRIX_ALT
        self.FRA_MATRIX_ALT = ctk.CTkFrame(self.FRA_MON_VAR, corner_radius=0, fg_color="white")
        self.FRA_MATRIX_ALT.grid(row=1, column=4, sticky="ne", pady=10, padx=10)
        self.FRA_MATRIX_ALT.grid_columnconfigure((0, 1, 2), weight=1)
        self.lbl_MatrixAltTitle = ctk.CTkLabel(
            self.FRA_MATRIX_ALT, pady=5, padx=5, text="ALTURA DA MATRIZ", bg_color="gray", text_color="white", anchor="center", font=("", 16)
        )
        self.lbl_MatrixAltTitle.grid(row=0, column=0, pady=5, padx=5, columnspan=3, sticky="ew")
        self.lbl_MatrixAltVal = ctk.CTkLabel(
            self.FRA_MATRIX_ALT,
            image=self._temp_icon if self._temp_icon else None,
            text="---------",
            justify="center",
            compound="left",
            anchor="e",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.lbl_MatrixAltVal.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        self.lbl_MatrixAltUnit = ctk.CTkLabel(self.FRA_MATRIX_ALT, pady=5, padx=5, text="mm", anchor="center", text_color="gray", font=("", 14))
        self.lbl_MatrixAltUnit.grid(row=1, column=2, pady=5, padx=5, sticky="e")

        # FRA_MON_GRAPHS
        self.FRA_MON_GRAPHS = ctk.CTkFrame(self, corner_radius=0, fg_color="white")
        self.FRA_MON_GRAPHS.grid(row=2, column=0, pady=5, padx=5, columnspan=2, sticky="nsew")
        self.FRA_MON_GRAPHS.grid_columnconfigure((0, 1, 2), weight=1)
        self.FRA_MON_GRAPHS.grid_rowconfigure(0, weight=0)
        self.FRA_MON_GRAPHS.grid_rowconfigure(1, weight=1)
        self.lbl_MonGraphTitle = ctk.CTkLabel(
            self.FRA_MON_GRAPHS,
            pady=5,
            padx=5,
            text="HISTORICO (24hrs)",
            bg_color="gray",
            text_color="white",
            anchor="center",
            font=("", 16),
        )
        self.lbl_MonGraphTitle.grid(row=0, column=0, pady=5, padx=5, columnspan=3, sticky="ew")

        self._graphs_enabled = HAS_MPL
        if self._graphs_enabled:
            # Temperature graph
            self.TempFornoHist = deque(maxlen=50)
            self.TempFornoTime = deque(maxlen=50)
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
            self.TempFornoCanvas.get_tk_widget().grid(row=1, column=0, sticky="w", pady=5, padx=5)

            # Pressure graph
            self.PressCargHist = deque(maxlen=50)
            self.PressCargTime = deque(maxlen=50)
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
            self.PressCargCanvas.get_tk_widget().grid(row=1, column=1, sticky="ew", pady=5, padx=5)

            # Motor current graph
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
            self.MotorAmpsCanvas.get_tk_widget().grid(row=1, column=2, sticky="e", pady=5, padx=5)
        else:
            ctk.CTkLabel(self.FRA_MON_GRAPHS, text="Gráficos indisponíveis (Matplotlib não encontrado)").grid(
                row=1, column=0, columnspan=3, padx=10, pady=10
            )

        # FRA_APP_BUTT (disabled placeholders to match monitor-2 layout)
        self.FRA_APP_BUTT = ctk.CTkFrame(self, corner_radius=0, fg_color="white")
        self.FRA_APP_BUTT.grid(row=3, column=0, pady=5, padx=5, columnspan=2, sticky="sew")
        self.FRA_APP_BUTT.grid_columnconfigure((0, 1, 2), weight=1)
        self.FRA_APP_BUTT.grid_rowconfigure(0, weight=1)
        self.btn_monitor = ctk.CTkButton(self.FRA_APP_BUTT, text="MONITOR", state="disabled", height=40)
        self.btn_monitor.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.btn_historico = ctk.CTkButton(self.FRA_APP_BUTT, text="HISTORICO", state="disabled", height=40)
        self.btn_historico.grid(row=0, column=1, pady=5, padx=5)
        self.btn_export = ctk.CTkButton(self.FRA_APP_BUTT, text="EXPORTAR", state="disabled", height=40)
        self.btn_export.grid(row=0, column=2, pady=5, padx=5, sticky="e")

        # FRA_APP_STATUS
        self.FRA_APP_STATUS = ctk.CTkFrame(self, corner_radius=0, fg_color="white")
        self.FRA_APP_STATUS.grid(row=4, column=0, pady=5, sticky="sew", columnspan=2)
        self.FRA_APP_STATUS.grid_columnconfigure((0, 1), weight=1)
        self.lbl_status = ctk.CTkLabel(
            self.FRA_APP_STATUS,
            text="STATUS",
            anchor="w",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white",
            bg_color="red",
            pady=5,
            padx=5,
        )
        self.lbl_status.grid(row=0, column=0, pady=5, padx=5, columnspan=2, sticky="ew")

    def update_values(self, data):
        if not data:
            self.lbl_status.configure(text="[Falha] Sem dados", bg_color="red")
            return

        try:
            # Process identifiers (if provided in 'data')
            if isinstance(data, dict):
                id_prod = data.get('IDProdlVal')
                cod_corr = data.get('CODCorrVal')
                if id_prod:
                    self.lbl_IDProdlVal.configure(text=str(id_prod))
                if cod_corr:
                    self.lbl_CODCorrVal.configure(text=str(cod_corr))

            # Values
            temp = data.get('temperatura_forno')
            press = data.get('pressao_carga')
            amps = data.get('corrente_motor')
            alt = data.get('altura_Matriz')
            ts = data.get('time_stamp') or datetime.now()

            if temp is not None:
                self.lbl_TempFornoVal.configure(text=f"{temp:.2f}")
                if self._graphs_enabled:
                    self.TempFornoTime.append(ts)
                    self.TempFornoHist.append(temp)
                    self.TempFornoLine.set_data(self.TempFornoTime, self.TempFornoHist)
                    self.TempFornoAx.relim(); self.TempFornoAx.autoscale_view()
                    self.TempFornoCanvas.draw()
            else:
                self.lbl_TempFornoVal.configure(text="---------")

            if press is not None:
                self.lbl_PressCargVal.configure(text=f"{press:.2f}")
                if self._graphs_enabled:
                    self.PressCargTime.append(ts)
                    self.PressCargHist.append(press)
                    self.PressCargLine.set_data(self.PressCargTime, self.PressCargHist)
                    self.PressCargAx.relim(); self.PressCargAx.autoscale_view()
                    self.PressCargCanvas.draw()
            else:
                self.lbl_PressCargVal.configure(text="---------")

            if amps is not None:
                self.lbl_MotorAmpsVal.configure(text=f"{amps:.2f}")
                if self._graphs_enabled:
                    self.MotorAmpsTime.append(ts)
                    self.MotorAmpsHist.append(amps)
                    self.MotorAmpsLine.set_data(self.MotorAmpsTime, self.MotorAmpsHist)
                    self.MotorAmpsAx.relim(); self.MotorAmpsAx.autoscale_view()
                    self.MotorAmpsCanvas.draw()
            else:
                self.lbl_MotorAmpsVal.configure(text="---------")

            if alt is not None:
                self.lbl_MatrixAltVal.configure(text=f"{alt:.2f}")
            else:
                self.lbl_MatrixAltVal.configure(text="---------")

            self.lbl_status.configure(text=f"[OK] Atualizado às {ts.strftime('%H:%M:%S')}", bg_color="green")
        except Exception as e:
            self.lbl_status.configure(text="[Falha] Atualização da UI", bg_color="red")
            print(f"Erro na atualização do monitor: {e}")
