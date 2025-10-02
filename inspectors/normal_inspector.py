
import cv2
import json
import os
from .base_inspector import BaseInspector

class NormalInspector(BaseInspector):
    def analizar(self):
        imagen = cv2.imread(self.imagen_absoluta)
        #imagen_j = cv2.resize(imagen, (self.config["json_width"], self.config["json_height"]))
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        #_, binaria = cv2.threshold(gris, self.config["umbral"], 255, cv2.THRESH_BINARY)
        imagen_zonas = imagen.copy()

        with open(self.json_path, 'r') as f:
            config_mask = json.load(f)
        
        resultado_global = True
        logs = []
        img_name = os.path.basename(self.imagen_absoluta)

        if not config_mask.get("enabled", True):
            print("Inspeccion deshabilitada")
            imagen_r = cv2.resize(imagen_zonas, (self.config["n_width"], self.config["n_height"]))
            return resultado_global, imagen_r, logs
        else:
            try:
                zonas = config_mask["zonas"]
                template_info = config_mask.get("template", None)
                 
            except Exception as e:
                logs.append(f"Error: {e}, please check json file")
                imagen_r = cv2.resize(imagen_zonas, (self.config["n_width"], self.config["n_height"]))
                resultado_global = False
                return resultado_global, imagen_r, logs
            
            dx, dy = 0, 0

            if template_info:
                template_path = os.path.join(os.path.dirname(self.json_path), template_info["path"])
                template_img = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
                #cv2.imshow("ref", template_img)
            
                if template_img is not None: 
                    tx1 = template_info["x1"]
                    ty1 = template_info["y1"] 
                    tx2 = template_info["x2"]
                    ty2 = template_info["y2"]

                    current_ref  = gris #[ty1:ty2, tx1:tx2]
                    #cv2.imshow("current", current_ref)
                    
                    if current_ref.shape[0] >= template_img.shape[0] and current_ref.shape[1] >= template_img.shape[1]:

                        res = cv2.matchTemplate(current_ref, template_img, cv2.TM_CCOEFF_NORMED)
                        _, max_val, _, max_loc =cv2.minMaxLoc(res)
                        #print(max_loc)
                        #print(max_val)

                        if max_val > 0.75:
                            dx = max_loc[0] - template_info["x1"]
                            dy = max_loc[1] - template_info["y1"]
                            print(f"Offset detectado dx {dx}, dy {dy}")
                        else:
                            print("No hay coincidencia")
                    else:
                        print(f"Error al cargar la imagen de template")
        

            for zona in zonas:
                x1 = zona["x1"] + dx
                y1 = zona["y1"] + dy
                x2 = zona["x2"] + dx
                y2 = zona["y2"] + dy

                #imagen_j = cv2.resize(gris, (self.config["json_width"], self.config["json_height"]))
                _, binaria = cv2.threshold(gris, self.config["umbral"], 255, cv2.THRESH_BINARY)
                roi = binaria[y1:y2, x1:x2]
                #print(roi)
                blancos = cv2.countNonZero(roi)
                #print(blancos)
                #print(roi.size)
                porcentaje = (blancos / roi.size) * 100

                if porcentaje < self.config["minimo_porcentaje"]:
                    resultado_global = False
                    color = (0, 0, 255)
                    logs.append(f"{img_name}: ❌ Glue missing on ROI: {zona['nombre']}, {porcentaje:.2f}% coverage")
                else:
                    color = (0, 255, 0)
                    logs.append(f"{img_name}: ✅ Glue OK on ROI: {zona['nombre']}, {porcentaje:.2f}% coverage")
                cv2.rectangle(imagen_zonas, (x1, y1), (x2, y2), color, 5)

            imagen_r = cv2.resize(imagen_zonas, (self.config["n_width"], self.config["n_height"]))
            return resultado_global, imagen_r, logs
        
        

