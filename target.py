

class TractabilityItem:      #Clase para tratatar las propiedades de la molécula diana para reaccionar a un fármaco
    def __init__(self, label : str, modality : str, value = bool):
        self.label = label    # Estado del fármaco
        self.modality = modality   #Intervención terapéutica
        self.value = value # Aprobación
        
        
###############################

class Target:    # Clase para instanciar las moléculas dianas
    def __init__(self, id : str, approvedSymbol : str, biotype : str, tractibilityItem : list[TractabilityItem]):
        if not id.startswith("ENSG"):
            raise ValueError(f"ERROR! invalid id: {id} (it musts start with 'ENSG').")
        self.id = id ### id para la base de datos
        self.approvedSymbol = approvedSymbol ### id legible
        self.biotype = biotype   #naturaleza de la molécula
        self.tractibilityItem = tractibilityItem  ###Lista pra saber por cuantos fármacos puede ser atacada la célula diana y de qué maneras
    
    def is_druggable(self):### Método para comprobar que si existe un fármaco para la molécula
        for i in self.tractibilityItem:
            if i.label == "Approved Drug" and i.value == True:
                return True 
        return False
            
    def __eq__(self, another): ### Método para comprobar que dos targets son iguales a través de su id único de la base de datos
        if not isinstance(another, Target):
            return False
        else:
            return self.id == another.id
    
            
#######################################