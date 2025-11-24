import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import filedialog
from tkinter import ttk
import csv


class HistoricoFrame(ctk.CTkFrame):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.pack(expand=True, fill="both", padx=10, pady=10)
        self.db_manager = db_manager
        self.current_data = []
        self.status_label = None

        self.setup_ui()

    def setup_ui(self):
        # FRA_APP_TITLE (estilo semelhante ao monitor.py)
        self.FRA_APP_TITLE = ctk.CTkFrame(self, corner_radius=0, fg_color="white")
        self.FRA_APP_TITLE.pack(fill="x", padx=5, pady=(0, 5))
        self.lbl_appTitle = ctk.CTkLabel(
            self.FRA_APP_TITLE,
            text="MONITORAMENTO LINHA RUSSA",
            justify="center",
            compound="center",
            anchor="center",
            font=ctk.CTkFont(size=32, weight="bold"),
        )
        self.lbl_appTitle.pack(padx=10, pady=10, fill="x")

        # Barra de controles (Período + Exportar)
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(control_frame, text="Período:").pack(side="left", padx=5)
        self.period_var = ctk.StringVar(value="1h")
        periods = ["1h", "6h", "12h", "24h", "7d", "30d", "60d", "90d"]
        period_menu = ctk.CTkOptionMenu(
            control_frame,
            values=periods,
            variable=self.period_var,
            command=self.update_data,
        )
        period_menu.pack(side="left", padx=5)

        ctk.CTkLabel(control_frame, text="Inicio:").pack(side="left", padx=5)
        self.start_entry = ctk.CTkEntry(
            control_frame,
            width=150,
            placeholder_text="YYYY-MM-DD HH:MM",
        )
        self.start_entry.pack(side="left", padx=5)

        ctk.CTkLabel(control_frame, text="Fim:").pack(side="left", padx=5)
        self.end_entry = ctk.CTkEntry(
            control_frame,
            width=150,
            placeholder_text="YYYY-MM-DD HH:MM",
        )
        self.end_entry.pack(side="left", padx=5)

        self.apply_btn = ctk.CTkButton(
            control_frame,
            text="Aplicar intervalo",
            command=self.apply_custom_range,
        )
        self.apply_btn.pack(side="left", padx=5)

        self.export_btn = ctk.CTkButton(control_frame, text="Exportar CSV", command=self.export_data)
        self.export_btn.pack(side="right", padx=5)

        self.status_label = ctk.CTkLabel(self, text="", text_color="gray40", anchor="w")
        self.status_label.pack(fill="x", padx=10, pady=(0, 5))

        # Container da Tabela (preenche toda área)
        self.table_container = ctk.CTkFrame(self)
        self.table_container.pack(expand=True, fill="both", padx=10, pady=10)
        self.table_container.grid_columnconfigure(0, weight=1)
        self.table_container.grid_rowconfigure(0, weight=1)

        # Treeview + Scrollbars
        self.tree = None
        self.vsb = ttk.Scrollbar(self.table_container, orient="vertical")
        self.hsb = ttk.Scrollbar(self.table_container, orient="horizontal")

        # Tabela default (ajusta dinamicamente após primeira consulta)
        self.build_tree(columns=[

            ("ts", "Data e Hora do Registro", 180, "w"),
            ("idprod", "Id Produto", 160, "e"),
            ("codcorr", "Cod. Corrida", 160, "e"),
            ("temp", "Temperatura do Forno", 160, "e"),
            ("press", "Pressão de Carga", 140, "e"),
            ("amps", "Corrente do Motor", 150, "e"),
            ("alt", "Altura da Matriz", 140, "e"),
        ])

        # Carregar dados iniciais
        self.update_data()

    def build_tree(self, columns):
        if self.tree is not None:
            try:
                self.tree.destroy()
            except Exception:
                pass

        self.tree = ttk.Treeview(
            self.table_container,
            columns=[c[0] for c in columns],
            show="headings",
            yscrollcommand=self.vsb.set,
            xscrollcommand=self.hsb.set,
            selectmode="browse",
        )

        for cid, heading, width, anchor in columns:
            self.tree.heading(cid, text=heading)
            self.tree.column(cid, width=width, anchor=anchor, stretch=True)

        # Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.vsb.config(command=self.tree.yview)
        self.hsb.config(command=self.tree.xview)
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.hsb.grid(row=1, column=0, sticky="ew")

    def update_data(self, *_args, start_date=None, end_date=None):
        # Calcular período
        period_map = {
            "1h": timedelta(hours=1),
            "6h": timedelta(hours=6),
            "12h": timedelta(hours=12),
            "24h": timedelta(days=1),
            "7d": timedelta(days=7),
            "30d": timedelta(days=30),
            "60d": timedelta(days=60),
            "90d": timedelta(days=90),
        }

        if start_date is None or end_date is None:
            end_date = datetime.now()
            start_date = end_date - period_map.get(self.period_var.get(), timedelta(hours=1))

        # Query
        data = self.db_manager.get_historical_data(start_date, end_date) or []
        self.current_data = data

        # Ajuste de colunas conforme esquema retornado
        first = data[0] if data else None
        if first:
            # Esquema esperado do banco (SELECT * historico):
            # time_stamp, IDProduto, CODCorrida, temperatura_forno, pressao_carga, corrente_motor, altura_Matriz
            if len(first) >= 7:
                columns = [
                    ("ts", "Data Registro", 180, "w"),
                    ("idprod", "Id Produto", 160, "w"),
                    ("codcorr", "Cod. Corrida", 160, "w"),
                    ("temp", "Temperatura do Forno", 160, "w"),
                    ("press", "Pressão de Carga", 140, "w"),
                    ("amps", "Corrente do Motor", 150, "w"),
                    ("alt", "Altura da Matriz", 140, "w"),
                ]
            self.build_tree(columns)

        # Limpar e inserir
        for iid in self.tree.get_children():
            self.tree.delete(iid)

        for row in data:
            values = []
            if len(row) >= 7:
                ts, idprod, codcorr, temp, press, amps, alt = row[:7]
                try:
                    ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    ts_str = str(ts)
                values.extend([
                    ts_str,
                    str(idprod) if idprod is not None else "",
                    str(codcorr) if codcorr is not None else "",
                    f"{float(temp):.2f}" if temp is not None else "",
                    f"{float(press):.2f}" if press is not None else "",
                    f"{float(amps):.2f}" if amps is not None else "",
                    f"{float(alt):.2f}" if alt is not None else "",
                ])
            self.tree.insert("", "end", values=values)

    def apply_custom_range(self):
        self.set_status("")
        start_str = self.start_entry.get().strip()
        end_str = self.end_entry.get().strip()

        if not start_str or not end_str:
            self.set_status("Informe inicio e fim no formato AAAA-MM-DD HH:MM.", "red")
            return

        dt_format = "%Y-%m-%d %H:%M"
        try:
            start_dt = datetime.strptime(start_str, dt_format)
            end_dt = datetime.strptime(end_str, dt_format)
        except ValueError:
            self.set_status("Formato invalido. Use AAAA-MM-DD HH:MM.", "red")
            return

        if start_dt >= end_dt:
            self.set_status("Data inicial deve ser menor que a final.", "red")
            return

        self.update_data(start_date=start_dt, end_date=end_dt)
        self.set_status("Intervalo aplicado ao historico.", "green")

    def set_status(self, message, color="gray40"):
        if self.status_label:
            self.status_label.configure(text=message, text_color=color)

    def export_data(self):
        # Nome padrão
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
        default_filename = f"prensa-russa-{timestamp}.csv"

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=default_filename,
            filetypes=[("CSV files", "*.csv")],
        )
        if not filename:
            return

        data = self.current_data or []

        if data and len(data[0]) >= 7:
            headers = [
                "Data Hora Registro",
                "Id Produto",
                "Cod. Corrida",
                "Temperatura do Forno",
                "Pressão de Carga",
                "Corrente do Motor",
                "Altura da Matriz",
            ]
        else:
            headers = [
                "Data Hora Registro",
                "Temperatura do Forno",
                "Pressão de Carga",
                "Corrente do Motor",
                "Altura da Matriz",
            ]

        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for row in data:
                if len(row) >= 7:
                    ts, idprod, codcorr, temp, press, amps, alt = row[:7]
                    try:
                        ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
                    except Exception:
                        ts_str = str(ts)
                    writer.writerow([
                        ts_str,
                        str(idprod) if idprod is not None else "",
                        str(codcorr) if codcorr is not None else "",
                        f"{float(temp):.2f}" if temp is not None else "",
                        f"{float(press):.2f}" if press is not None else "",
                        f"{float(amps):.2f}" if amps is not None else "",
                        f"{float(alt):.2f}" if alt is not None else "",
                    ])
