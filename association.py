from disease import *
from target import *
from evidence import *
import math 
#Importamos todos los ficheros ya que esta clase los relaciona todos
class Association: #Clase que instancia  las relaciones
    def __init__(self, target : Target, disease : Disease, evidence : list[Evidence]):
        self.target = target # molécula diana
        self.disease =disease # enfermedad
        self.evidence = evidence #evidencias
        scores = []
        for i in self.evidence:
            scores.append(i.get_score())
        self.scores = scores # lista de scores para eficencia de código
        
    def get_total_score(self): # Método para obtener la media del nivel de fiabilidad
        if not self.scores or len(self.scores) == 0:
            return 0.0
        Main = (sum(self.scores)/len(self.scores))
        return Main
    
    def get_top_evidence(self): #Método para conseguir la evidencia más fiable
        maximum = max(self.scores)
        i = 0
        while maximum != self.scores[i]:
            i +=1
        return self.evidence[i]
    def __lt__(self, other):
        if not isinstance(other, Association):
            verif = NotImplemented
        else:
            verif = self.get_total_score() < other.get_total_score()
        return verif
    
######################
            
        
        