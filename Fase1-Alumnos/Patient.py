"""Patient class

Data Structures and Algorithms: Phase 1 - Covid-19 Vaccination Campaign

Authors:
    - Aarón Espasandín Geselmann (100451339).
    - Marina Buitrago Pérez ().

Code style: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings
"""

class Patient:
    """
    Patient information.

    Attributes:
        name (str): Surname and Name of the patient. Ex.: "Segura, Isabel".
        year (int): Birth year. Ex.: 1974.
        covid (bool): Indicates if the covid has been passed (True) or not (False).
        vaccine (int): Indicates if the patient has been vaccinated. Cases:
            -  0: Not vaccinated.
            -  1: First dose received.
            -  2: Second dose received.
    """

    def __init__(self, name, year, covid, vaccine):
        """Inits Patient class"""
        self.name = name
        self.year = year
        self.covid = covid
        self.vaccine = vaccine
    
    def __str__(self):
        return self.name+'\t'+str(self.year)+'\t'+str(self.covid)+'\t'+str(self.vaccine)
