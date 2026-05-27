
class Evidence: # Clase madre para instanciar todas las evidencias
    def __init__(self, id : str, score : float, datatypeId : str): 
        if not (0 <= score <=1): #Validación del rango de fiabilidad
            raise ValueError(f"Error! Score musts be between 0 and 1.")
        self.id = id # Id de la evidencia
        self.score = score #Nivel de fiabilidad
        self.datatypeId = datatypeId # Tipo de evidencia
    
    def get_score(self): return self.score #Método para obtener el nivel de fiabilidad

################
class GeneticEvidence(Evidence): # Clase de evidencia genética heredada
    def __init__(self, id : str, score : float, datatypeId :str, sourceId = float):
        super().__init__(id, score, datatypeId)
        if sourceId == "gwas_catalog" and score< 0.5:
            raise ValueError("Error!")
        self.sourceId = sourceId # Nuevo atributo, fuente de información
              
              
###################
class IndirectEvidence(Evidence): #Clase de evidencia indirecta heredada
    def get_score(self): 
        return self.score*0.8 #Polimorfismo para reducir el nivel de fiabilidad
    #Estaa clase se puede heredar sin la necesidad de la función super()
#############
            
    
    
    
        