# -*- coding: utf-8 -*-
"""
fase1
"""

import csv
import os.path

from HealthCenter import HealthCenter    
from Patient import Patient
     
if __name__ == '__main__':
    gst = HealthCenter('data/LosFrailes.tsv')
    # print(gst) # See __str__ in dlist
    
    #Puedes añadir más llamadas a funciones para probarlas
    # patient = Patient("Lozano, Manolo", 2001, False, 2)
    # gst.addPatient(patient)

    search_result = gst.searchPatients(1950, None, None)
    print(search_result)
