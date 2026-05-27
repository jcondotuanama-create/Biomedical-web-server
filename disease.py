
class Disease: #Clase para instanciar a las enfermedades
    def __init__(self, id :str, name : str, phenotype_objects = list[str]):
        if  not id.startswith("EFO_") or name =="": #Validación para que se introduzca un nombre y un id correcto
            raise ValueError("Error. You enter any name or your id entered does not start with 'EFO_'.")
        self.id = id #id de la enfermedad
        self.name = name #nombre de la enfermedad
        self.phenotype_objects = phenotype_objects #rasgos de la enfermedad
    
    def has_phenotype(self, Name): ### método que nos permite saber si una enfermedad tiene el fenotipo que le introducimos
        Name_lower = Name.lower()
        for i in self.phenotype_objects:
            if i.lower()== Name_lower:
                return True
        return False