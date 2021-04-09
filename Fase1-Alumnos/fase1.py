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

    # search_result = gst.searchPatients(1950, None, None)
    # print(search_result)

    input1 = HealthCenter('data/LosFrailes.tsv')
    input2 = HealthCenter('data/Libertad.tsv')

    result = input1.merge(input2)
    expected = HealthCenter('data/LosFrailes+Libertad.tsv')

    assert(len(result), len(expected), 'FAIL: lenghts are different')

    print("##############################")
    print("Resulting list:")
    print(result)
    print("##############################\n\n")

    print("##############################")
    print("Expected list:")
    print(expected)
    print()
    print("##############################\n\n")

    for i in range(len(result)):
        assert(result.getAt(i).name, expected.getAt(i).name, 'FAIL: patients are not equal')
    print()
