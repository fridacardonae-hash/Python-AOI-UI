
from .normal_inspector import NormalInspector
from .special5_inspector import Special5Inspector
from .specialRTV_inspector import SpecialRTVInspector
from .special4_inspector import SpecialMTS41Inspector

def get_inspector(imagen_nombre, imagen_absoluta, json_path, config, name_config):
    if imagen_nombre == "5.jpg"or imagen_nombre == "4-2.bmp":
        return Special5Inspector(imagen_absoluta, json_path, config)
    
    elif name_config == "ConfigMTSRTV.json":
        return SpecialRTVInspector(imagen_absoluta, json_path, config)
    
    elif name_config == "ConfigMTSTIM1.json" and imagen_nombre == "4-1.bmp":
        return SpecialMTS41Inspector(imagen_absoluta, json_path, config)
    
    else:
        return NormalInspector(imagen_absoluta, json_path, config)
    
    
    
