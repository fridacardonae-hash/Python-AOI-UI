
import os
from inspectors.inspector_factory import get_inspector
#Interfaz para glue Inspection
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import json
import cv2
import os
import time
import threading
import datetime

class GlueInspection(ctk.CTk):
    def __init__(self):
        self.is_scanning=False
        self.is_scanning_online = False
        self.log_widget = None
        self.start_time = datetime.datetime.now()

        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.title("PMX Glue Inspection")
        self.root.geometry("1100x700")

        self.setup_gui()
        self.root.mainloop()
        

    def setup_gui(self):
        main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        tab_frame = ctk.CTkTabview(main_frame)
        tab_frame.pack(padx=10, pady=10,fill="both", expand=True)

        tab_offline = tab_frame.add("Offline Inspection")
        tab_online = tab_frame.add("Online Inspection")
        tab_config = tab_frame.add("Configuration")

        with open ("quickconfig.json", "r") as q_file:
            self.quick_config =json.load(q_file)

#TAB OFFLINE 

        left_panel = ctk.CTkFrame(tab_offline, corner_radius=10)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        left_panel.grid_rowconfigure((0, 1), weight=1)
        left_panel.grid_columnconfigure(0, weight=1)

        right_panel = ctk.CTkFrame(tab_offline, corner_radius=10)
        right_panel.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        right_panel.grid_rowconfigure((0, 1), weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(tab_offline, text="Glue Inspection Offline", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=2)
#LEFT PANEL

        label_space = ctk.CTkLabel(left_panel, text="         ", font=("Arial",14)).grid(row=0, column=0)
        label_off_path = ctk.CTkLabel(left_panel, text= "Images path", font=("Arial", 14)).grid(row=1, column=1, sticky="w")

        self.offline_var = ctk.StringVar()
        self.offline_entry = ctk.CTkEntry(left_panel, textvariable=self.offline_var, width=300)
        self.offline_entry.grid(row=1, column=2)

        self.button_openonf = ctk.CTkButton(left_panel, text="📂", command = self.openof_folder, width=50)
        self.button_openonf.grid(row=1, column=3, sticky="w")

        label_space2 = ctk.CTkLabel(left_panel, text="         ", font=("Arial",20)).grid(row=2, column=0)

        label_space4 = ctk.CTkLabel(left_panel, text="         ", font=("Arial",20)).grid(row=5, column=0)

        self.button_inspect = ctk.CTkButton(left_panel, text="🔎 Inspect folder", command = self.start_scan_thread, width=120)
        self.button_inspect.grid(row=6, column=2)
        
        label_space3 = ctk.CTkLabel(left_panel, text="         ", font=("Arial",20)).grid(row=7, column=0)

        self.button_stop = ctk.CTkButton(left_panel, text="⏹️ Stop Inspection", command = self.stop_scan_callback, width=120)
        self.button_stop.grid(row=8, column=2)

        canvas_width = int(self.screen_width*0.56)
        canvas_height = int(self.screen_height*0.5)
        self.canvas = ctk.CTkCanvas(right_panel, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.grid(row=0, column=0, sticky="s")

        log_label = ctk.CTkLabel(left_panel, text="Log Output", font=("Arial", 14))
        log_label.grid(row=3, column=2)
 
        self.log_widget = ctk.CTkTextbox(left_panel, height=200, width=450, state="normal")
        self.log_widget.grid(row=4, column=1, columnspan=3, sticky="")

        label_space1 = ctk.CTkLabel(left_panel, text="         ", font=("Arial",14)).grid(row=9, column=4)
#TAB ONLINE

        left_panel2 = ctk.CTkFrame(tab_online, corner_radius=10)
        left_panel2.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        left_panel2.grid_rowconfigure((0, 1), weight=1)
        left_panel2.grid_columnconfigure(0, weight=1)

        right_panel2 = ctk.CTkFrame(tab_online, corner_radius=10)
        right_panel2.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        right_panel2.grid_rowconfigure((0, 1), weight=1)
        right_panel2.grid_columnconfigure(0, weight=1)

        title_label2 = ctk.CTkLabel(tab_online, text="Glue Inspection Online", font=("Arial", 16))
        title_label2.grid(row=0, column=0, columnspan=2)

#LEFT PANEL

        
        #label_spacex = ctk.CTkLabel(left_panel2, text="         ", font=("Arial",14)).grid(row=0, column=0)
        #label_off_pathx = ctk.CTkLabel(left_panel2, text= "Images path", font=("Arial", 14)).grid(row=1, column=1, sticky="w")

        self.offline_var1 = ctk.StringVar()

        #label_space22 = ctk.CTkLabel(left_panel2, text="         ", font=("Arial",20)).grid(row=2, column=0)
        log_label2 = ctk.CTkLabel(left_panel2, text="Log Output", font=("Arial", 14))
        log_label2.grid(row=3, column=2)

        label_space42 = ctk.CTkLabel(left_panel2, text="         ", font=("Arial",20)).grid(row=5, column=0)

        self.button_inspect2 = ctk.CTkButton(left_panel2, text="🔎 Inspect folder", command = self.start_scan_thread_online, width=120)
        self.button_inspect2.grid(row=6, column=2)

        self.log_widget2 = ctk.CTkTextbox(left_panel2, height=200, width=450, state="normal")
        self.log_widget2.grid(row=4, column=1, columnspan=3, sticky="")

        label_space32 = ctk.CTkLabel(left_panel2, text="         ", font=("Arial",20)).grid(row=7, column=0)

        self.button_stop2 = ctk.CTkButton(left_panel2, text="⏹️ Stop Inspection", command = self.stop_scan_online_callback, width=120)
        self.button_stop2.grid(row=8, column=2)

        label_space12 = ctk.CTkLabel(left_panel2, text="         ", font=("Arial",14)).grid(row=9, column=4)

        canvas_width2 = int(self.screen_width*0.56)
        canvas_height2 = int(self.screen_height*0.5)
        self.canvas2 = ctk.CTkCanvas(right_panel2, width=canvas_width2, height=canvas_height2, bg="white")
        self.canvas2.pack(fill="both", expand=True)
        self.canvas2.grid(row=0, column=0, sticky="s")
    

#TAB CONFIG
        label_space10 = ctk.CTkLabel(tab_config, text="         ", font=("Arial",14)).grid(row=0, column=0)
        title_label2 = ctk.CTkLabel(tab_config, text="Model Configuration", font=("Arial", 16)).grid(row=1, column=4)

        label_model = ctk.CTkLabel(tab_config, text= "Model Config .json", font=("Arial", 14)).grid(row=2, column=1, sticky="w")
        
        self.model_var = ctk.StringVar()
        self.model_entry = ctk.CTkEntry(tab_config, textvariable=self.model_var, width=300)
        self.model_entry.grid(row=3, column=1, padx=5, pady=5)  
   
        self.button_openm = ctk.CTkButton(tab_config, text="📂", command = self.openmodel_folder, width=50)
        self.button_openm.grid(row=3, column=2, pady=5, padx=5)

        label_quick = ctk.CTkLabel(tab_config, text="Quick config", font=("Arial", 14)).grid(row=2, column=6)
        self.quick_menu = ctk.CTkOptionMenu(tab_config, values=list(self.quick_config.keys()), command=self.model_menu, width=60)
        self.quick_menu.grid(row=3, column=6)

        #self.model_config_var = ctk.StringVar() 
        '''self.log_folder_var = ctk.StringVar() 
        self.model_coordinates_var = ctk.StringVar()'''


 #/////////////////////       
        label_space11 = ctk.CTkLabel(tab_config, text="                ", font=("Arial",14)).grid(row=4, column=3)
        label_log = ctk.CTkLabel(tab_config, text= "Log Folder", font=("Arial", 14)).grid(row=5, column=1, sticky="w")
        
        self.log_folder = ctk.StringVar()
        self.log_entry = ctk.CTkEntry(tab_config, textvariable=self.log_folder, width=300)
        self.log_entry.grid(row=6, column=1, sticky="w")  

        self.button_opelog = ctk.CTkButton(tab_config, text="📂", command = self.openlog_folder, width=50)
        self.button_opelog.grid(row=6, column=2, pady=5, padx=5)

#///////////////////////
        label_space12 = ctk.CTkLabel(tab_config, text="                                                          ", font=("Arial",14)).grid(row=7, column=5)
        label_coordinates = ctk.CTkLabel(tab_config, text= "Model Coordinates Path", font=("Arial", 14)).grid(row=8, column=1, sticky="w")
        
        self.coor_var = ctk.StringVar()
        self.coor_entry = ctk.CTkEntry(tab_config, textvariable=self.coor_var, width=300)
        self.coor_entry.grid(row=9, column=1, padx=5, pady=5)  
  

        self.button_openc = ctk.CTkButton(tab_config, text="📂", command = self.opencoord_folder, width=50)
        self.button_openc.grid(row=9, column=2)

#///////////////////////
        label_space13 = ctk.CTkLabel(tab_config, text="                ", font=("Arial",14)).grid(row=10, column=6)
        label_images = ctk.CTkLabel(tab_config, text= "Images Path", font=("Arial", 14)).grid(row=11, column=1, sticky="w")
        
        self.online_var = ctk.StringVar()
        self.images_entry = ctk.CTkEntry(tab_config, textvariable=self.online_var, width=300)
        self.images_entry.grid(row=12, column=1, padx=5, pady=5)  
 
        self.onliner_var = ctk.StringVar()
        self.button_openi = ctk.CTkButton(tab_config, text="📂", command = self.openonl_folder, width=50)
        self.button_openi.grid(row=12, column=2)

#///////////////////////

        cr=Image.open("cinamonrol1.png")
        cr=cr.resize((110,130))
        bg_image = ctk.CTkImage(light_image=cr, dark_image=cr, size=(110, 130))

        bg_label = ctk.CTkLabel(tab_config, image=bg_image, text="")
        #bg_label.place(x=400, y=250, relwidth=1, relheight=1)
        bg_label.grid(row=15, column=6,)

        label_sign = ctk.CTkLabel(tab_config, text= "Developed by PMX_F0_AE", font=("Arial", 12)).grid(row=16, column=6)

#//////////////////////
        label_space14 = ctk.CTkLabel(tab_config, text="                ", font=("Arial",14)).grid(row=13, column=6)
        self.button_savec = ctk.CTkButton(tab_config, text="💾 Save Config", command = self.load_config, width=50)
        self.button_savec.grid(row=14, column=4)

        self.label_log = ctk.CTkLabel(tab_config, text= "", font=("Arial", 12))
        self.label_log.grid(row=16, column=1)

        

#/////FUNCTIONS
    
    #Offline directory images path
    def openof_folder(self):     
       offline_path = filedialog.askdirectory()
       if offline_path:
        self.offline_var.set(offline_path)
    
    def offlinelog_info(self, message):
        self.log_widget.configure(state="normal")
        self.log_widget.insert("end", f"{message}\n")
        self.log_widget.see("end")
        self.log_widget.configure(state="disabled")
    
    def onlinelog_info(self, message):
        self.log_widget2.configure(state="normal")
        self.log_widget2.insert("end", f"{message}\n")
        self.log_widget2.see("end")
        self.log_widget2.configure(state="disabled")
     
    def model_menu(self, choice):
        valor = self.quick_menu.get()
        print(valor)

        if valor:
            self.model_config_var=((self.quick_config[valor])["Model Config .json"])
            #print(f"modeLO {self.model_conf_var}")
            self.model_coor_var = (self.quick_config[valor])["Model Coordinates Path"]
            self.log_path = (self.quick_config[valor])["Log Folder"]

            #self.model_var.set(str(self.model_conf_var))
            self.model_var.set((self.quick_config[valor])["Model Config .json"])
            self.coor_var.set(self.model_coor_var)
            self.log_folder.set(self.log_path)
        


    #Model config    
    def openmodel_folder(self):     
       self.model_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
       #if self.model_path:
        #self.model_var.set(self.model_path)
    
    def openlog_folder(self):     
       log_path = filedialog.askdirectory()
       if log_path:
        self.log_folder.set(log_path)

    #Model coordinates directory 
    def opencoord_folder(self):     
       coordinates_path = filedialog.askdirectory()
       if coordinates_path:
        self.coor_var.set(coordinates_path)

    #Online directory images path
    def openonl_folder(self):     
       onliner_path = filedialog.askdirectory()
       if onliner_path:
        self.online_var.set(onliner_path) #images_path / images_var

     
    def start_scan_thread(self):
        if self.is_scanning:
            return
        self.is_scanning = True
        thread = threading.Thread(target=self.inspect_offline_folder)
        thread.daemon = True
        thread.start()
    
    def start_scan_thread_online(self):
        if self.is_scanning:
            return
        self.is_scanning_online = True
        thread = threading.Thread(target=self.online_monitor)
        thread.daemon = True
        thread.start()
   
#//////FUNCIONAMIENTO/////

    def load_config(self):
        #print(self.model_config_var)
        try:
            with open(self.model_config_var, 'r') as f:
                
            #with open(model_config_var.get(), 'r') as f:
                #print(self.model_var)
                self.config = json.load(f)
                #print("✔️ Configuración cargada correctamente")
                self.offlinelog_info("✔️ Config loaded correctly")
                self.onlinelog_info("✔️ Config loaded correctly")
                self.label_log.configure(text="✔️ Config loaded correctly")
                #print(self.model_config_var)

                partesname_config= self.model_config_var.split("/")
                #print(partesname_config)
                if partesname_config:                   
                    self.name_config = partesname_config[-1].strip()
                    print(self.name_config)
                

        except Exception as e:
            self.offlinelog_info(f"❌ Error loading the config: {e}")
            self.onlinelog_info(f"❌ Error loading the config: {e}")
            self.label_log.configure(text="❌ Error loading config, plase check log")
            self.stop_scan_callback()
            self.stop_scan_online_callback()


    def inspect_online_folder(self, ruta):
        
        imagenes_json = self.config["imagenes_json"]
        umbral = self.config["umbral"]
        umbral5 = self.config["umbral5"]
        minimo_porcentaje = self.config["minimo_porcentaje"]
        minimo_porcentaje5 = self.config["minimo_porcentaje5"]
        n_width = self.config["n_width"]
        n_height = self.config["n_height"]
        json_width = self.config["json_width"]
        json_height = self.config["json_height"]




        for archivo in os.listdir(ruta):
           
            if archivo.endswith(".jpg") or archivo.endswith(".bmp"):
                for imagen_nombre, json_nombre in imagenes_json.items():
                    #print(f"imagenjson{imagenes_json}")
                    if imagen_nombre in archivo:
                        #rute_archivo = os.path.join(ruta, archivo)
                        imagen_absoluta = os.path.join(ruta, imagen_nombre)
                        carpeta_imagen = os.path.dirname(imagen_absoluta)
                        isn = os.path.basename(os.path.dirname(carpeta_imagen))
                        nombre_mask_base = self.config["imagenes_json"][imagen_nombre]
                    

                        partes_nombre = isn.split("-")
                        indice_isn = next((i for i, parte in enumerate(partes_nombre) if parte.startswith("P")), None)
                        if indice_isn is not None:
                            isn = "-".join(partes_nombre[indice_isn:]) #para reconstruir el ISN donde empieza con P
                            partes_isn = isn.split("-")
                            version = None
                            if len(partes_isn)>=3:                      # la version siempre estara en esta posicion si el ISN siempre empieza con P
                                version = partes_isn[2].strip().upper()
                                if version in self.config["versiones"]:
                                    json_filename = f"{nombre_mask_base}_{version}.json"
                                else:
                                    self.onlinelog_info(f"Version {version} unknown, using base mask")
                                    json_filename = f"{nombre_mask_base}.json"
                        else:
                            self.onlinelog_info("No valid ISN found, please check")

                        nombre_archivo = os.path.basename(imagen_absoluta)
                        self.onlinelog_info(f"Procesando imagen: {nombre_archivo} (ISN: {isn})")

                        json_absoluto = os.path.join(self.coor_var.get(), json_filename)
                        if not os.path.exists(imagen_absoluta) or not os.path.exists(json_absoluto):
                            continue

                        if not self.is_scanning_online:
                            self.onlinelog_info("⏹️ Scanning detenido por el usuario")
                            return

                        inspector = get_inspector(imagen_nombre, imagen_absoluta, json_absoluto, self.config, self.name_config)
                        resultado, imagen_resultado, logs = inspector.analizar()

                        for log_msg in logs:
                            self.onlinelog_info(log_msg)

                        self.mostrar_imagen_canvas_online(imagen_resultado)

                        if resultado:
                            self.onlinelog_info(f"✅ {imagen_nombre} OK")
                        else:
                            self.onlinelog_info(f"❌ {imagen_nombre} Fallo en inspección")

                            now = datetime.datetime.now()
                            year = str(now.year)
                            month = f"{now.month:02}"
                            day = f"{now.day:02}"

                        # Log por ISN fallido
                            carpeta_imagen = os.path.dirname(imagen_absoluta)
                            
                            log_dir = self.log_folder.get()
                            #print(f"logdir{log_dir}")
                            #log_dir = str(self.log_folder)
                            #os.makedirs(log_dir, exist_ok=True)
                            
                            
                            if os.path.exists(log_dir):
                                #print(f"logdir{log_dir}")
                                name_config = self.name_config.replace('Config', '').strip() #nombre de carpeta segun modelo de config
                                model = name_config.replace('.json', '').strip()

                                carpeta_model = os.path.join(log_dir, model)
                                os.makedirs(carpeta_model, exist_ok=True)
                                #print(f"carpeta model{carpeta_model}") 

                                carpeta_anio = os.path.join(carpeta_model, year)
                                os.makedirs(carpeta_anio, exist_ok=True)
                                #print(f"carpeta anio {carpeta_anio}")

                                carpeta_mes = os.path.join(carpeta_anio, month)
                                os.makedirs(carpeta_mes, exist_ok=True)
                                #print(f"carpeta mes {carpeta_mes}")

                                carpeta_dia = os.path.join(carpeta_mes, day)
                                os.makedirs(carpeta_dia, exist_ok=True)
                                print(f"carpeta dia{carpeta_dia}")

                                log_carpeta = os.path.join(carpeta_dia, f"{isn}")
                                os.makedirs(log_carpeta, exist_ok=True)
                                #print(f"carpeta dia{carpeta_dia}")

                                log_path = os.path.join(log_carpeta, f"{isn}.log")
                                #print(f"log path{log_path}")

                                img_fail_path = os.path.join(log_carpeta, f"{isn}.jpg") 
                                #print(f"img fail path{img_fail_path}")

                                #guardar imagen
                                cv2.imwrite(img_fail_path, imagen_resultado)
                                #contenido del log 
                                with open(log_path, "a",  encoding="utf-8") as log_file:
                                    for log_msg in logs:
                                        #if log_msg.startswith()
                                        log_file.write(log_msg + "\n")
                                    

    def inspect_offline_folder(self):
        if not hasattr(self, "config"):
            print("❌ Carga primero la configuración del modelo.")
            return

        main_folder = self.offline_var.get()
        if not os.path.isdir(main_folder):
            print("❌ Ruta de imágenes no válida.")
            self.stop_scan_callback()
            return

        imagenes_json = self.config["imagenes_json"]
        umbral = self.config["umbral"]
        umbral5 = self.config["umbral5"]
        minimo_porcentaje = self.config["minimo_porcentaje"]
        minimo_porcentaje5 = self.config["minimo_porcentaje5"]
        n_width = self.config["n_width"]
        n_height = self.config["n_height"]
        json_width = self.config["json_width"]
        json_height = self.config["json_height"]

        for root, dirs, files in os.walk(main_folder):
            for imagen_nombre, json_nombre in imagenes_json.items():
                if imagen_nombre in files:
                    imagen_absoluta = os.path.join(root, imagen_nombre)
                    carpeta_imagen = os.path.dirname(imagen_absoluta)
                    isn = os.path.basename(os.path.dirname(carpeta_imagen))

                    nombre_mask_base = self.config["imagenes_json"][imagen_nombre]
                    partes_nombre = isn.split("-")
                    #print(partes_nombre)
                    indice_isn = next((i for i, parte in enumerate(partes_nombre) if parte.startswith("P")), None)
                    #print(indice_isn)

                    if indice_isn is not None:
                        isn = "-".join(partes_nombre[indice_isn:]) #para reconstruir el ISN donde empieza con P
                        partes_isn = isn.split("-")
                        version = None
                        if len(partes_isn)>=3:                      # la version siempre estara en esta posicion si el ISN siempre empieza con P
                            version = partes_isn[2].strip().upper()
                            if version in self.config["versiones"]:
                                json_filename = f"{nombre_mask_base}_{version}.json"
                            else:
                                self.offlinelog_info(f"Version {version} unknown, using base mask")
                                json_filename = f"{nombre_mask_base}.json"
                    else:
                        self.offlinelog_info("No valid ISN found, please check")

                    nombre_archivo = os.path.basename(imagen_absoluta)
                    self.offlinelog_info(f"Procesando imagen: {nombre_archivo} (ISN: {isn})")

                    json_absoluto = os.path.join(self.coor_var.get(), json_filename)
                    if not os.path.exists(imagen_absoluta) or not os.path.exists(json_absoluto):
                        continue

                    if not self.is_scanning:
                        self.offlinelog_info("⏹️ Scanning detenido por el usuario")
                        return

                    inspector = get_inspector(imagen_nombre, imagen_absoluta, json_absoluto, self.config, self.name_config)
                    resultado, imagen_resultado, logs = inspector.analizar()

                    for log_msg in logs:
                        self.offlinelog_info(log_msg)

                    self.mostrar_imagen_canvas(imagen_resultado)

                    if resultado:
                        self.offlinelog_info(f"✅ {imagen_nombre} OK")
                    else:
                        self.offlinelog_info(f"❌ {imagen_nombre} Fallo en inspección")

                        now = datetime.datetime.now()
                        year = str(now.year)
                        month = f"{now.month:02}"
                        day = f"{now.day:02}"

                    # Log por ISN fallido
                        carpeta_imagen = os.path.dirname(imagen_absoluta)
                        
                        log_dir = self.log_folder.get()
                        os.makedirs(log_dir, exist_ok=True)
                        #log_dir = str(self.log_folder)
                        #print(f"log folder {log_dir}")
                        #log_dir = os.path.join(os.getcwd(), "Logs_Fallos")
                        name_config = self.name_config.replace('Config', '').strip()
                        model = name_config.replace('.json', '').strip()
                        carpeta_model = os.path.join(log_dir, model)
                        os.makedirs(carpeta_model, exist_ok=True)
                        
                        carpeta_anio = os.path.join(carpeta_model, year)
                        os.makedirs(carpeta_anio, exist_ok=True)

                        carpeta_mes = os.path.join(carpeta_anio, month)
                        os.makedirs(carpeta_mes, exist_ok=True)

                        carpeta_dia = os.path.join(carpeta_mes, day)
                        os.makedirs(carpeta_dia, exist_ok=True)

                        log_carpeta = os.path.join(carpeta_dia, f"{isn}")
                        os.makedirs(log_carpeta, exist_ok=True)

                        log_path = os.path.join(log_carpeta, f"{isn}.log")
                        img_fail_path = os.path.join(log_carpeta, f"{isn}.jpg") 

                        #guardar imagen
                        cv2.imwrite(img_fail_path, imagen_resultado)
                        #contenido del log 
                        with open(log_path, "a",  encoding="utf-8") as log_file:
                            for log_msg in logs:
                                #if log_msg.startswith()
                                log_file.write(log_msg + "\n")




    def get_most_recent_subfolder(self, path):
        subfolders = [os.path.join(path, f) for f in os.listdir(path) if os.path.isdir(os.path.join(path,f))]
        #print(f"subfolders: {subfolders}")
        if not subfolders:
            return None
        return max(subfolders, key=os.path.getmtime)
    
    def online_monitor(self):
        if not hasattr(self, "config"):
            print("❌ Carga primero la configuración del modelo.")
            return

        self.main_folder = self.online_var.get()
        if not os.path.isdir(self.main_folder):
            print("❌ Ruta de imágenes no válida.")
            self.stop_scan_online_callback()
            return

        #self.is_scanning_online == True
        processed_isns = set()

        while self.is_scanning_online:
            print(f"buscando nuevas carpetas en {self.main_folder}")
            time.sleep(5)
            year_folder = self.get_most_recent_subfolder(self.main_folder)
            if not year_folder:
                continue
            mes_folder = self.get_most_recent_subfolder(year_folder)
            if not mes_folder:
                continue
            dia_folder = self.get_most_recent_subfolder(mes_folder)
            #print(f"dia{dia_folder}")
            if not dia_folder:
                continue
            for isn in os.listdir(dia_folder):
                isn_path = os.path.join(dia_folder, isn)
                print(f"ISNPATH {isn_path}")
                if not os.path.isdir(isn_path) or isn in processed_isns:
                    continue
                try:
                    creation_time = datetime.datetime.fromtimestamp(os.path.getctime(isn_path))
                    #print(f"dia folder {dia_folder}")
                    #print(f"isn{isn_path}")
                except Exception as e:
                    print(f"Creation time cannot be readed{creation_time}")
                    continue
                if creation_time > self.start_time:
                    print(f"start{self.start_time}")
                    try:

                        image_folder = os.path.join(isn_path, "image")
                        if os.path.isdir(image_folder):
                            print(f"Nuevo ISN detectado{isn}")
                            time.sleep(15)
                            self.inspect_online_folder(image_folder)
                            processed_isns.add(isn)
                            print(processed_isns)
                            time.sleep(2)
                    except Exception as e:
                        print(f"[ERROR] Failed to get picture from {isn_path}")
                #else:
                    #print(f"day folder {dia_folder} creatio time {creation_time}")
                


    def mostrar_imagen_canvas(self, imagen_cv):
        from PIL import Image, ImageTk
        import cv2
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        img_res = cv2.resize(imagen_cv,(canvas_w, canvas_h))
        img_rgb = cv2.cvtColor(img_res, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=img_tk)
        self.canvas.image = img_tk

    def mostrar_imagen_canvas_online(self, imagen_cv):
        from PIL import Image, ImageTk
        import cv2
        canvas_w = self.canvas2.winfo_width()
        canvas_h = self.canvas2.winfo_height()
        img_res = cv2.resize(imagen_cv,(canvas_w, canvas_h))
        img_rgb = cv2.cvtColor(img_res, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        self.canvas2.delete("all")
        self.canvas2.create_image(0, 0, anchor="nw", image=img_tk)
        self.canvas2.image = img_tk

    def stop_scan_callback(self):
        self.is_scanning = False
        self.offlinelog_info("Scanning stopped")
    
    def stop_scan_online_callback(self):
        self.is_scanning_online = False
        self.onlinelog_info("Scanning stopped") 

if __name__ == "__main__":
    app = GlueInspection()


    
