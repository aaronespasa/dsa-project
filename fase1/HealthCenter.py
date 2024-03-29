# -*- coding: utf-8 -*-
"""Health Center class

Data Structures and Algorithms: Phase 1 - Covid-19 Vaccination Campaign

Authors:
    - Aarón Espasandín Geselmann (100451339).
    - Marina Buitrago Pérez (100428967).

Code style: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings
"""

from dlist import DList
from dlist import DNode

from Patient import Patient
import csv
import os.path

class HealthCenter(DList):
    """
    Obtain information on the status of the Covid-19 vaccination campaign
    in the health centers.

    Attribute:
        filetsv (str): Name of the tsv file. Ex.: LosFrailes.tsv.
    """
    def __init__(self, filetsv:bool = None):
        """Inits HealthCenter class"""
        super(HealthCenter, self).__init__()

        if filetsv is None or not os.path.isfile(filetsv):
            self.name = ''

        else:
            # print('loading the data for the health center from the file ', filetsv)

            self.name = filetsv.replace('.tsv', '') # LosFrailes.tsv -> LosFrailes
            tsv_file = open(filetsv)
            read_tsv = csv.reader(tsv_file, delimiter="\t")

            self.size = 0 # Modified

            for row in read_tsv:
                name = row[0]
                year = int(row[1])
                covid = False

                if int(row[2]) == 1:
                    covid = True

                vaccine = int(row[3])
                self.size += 1 # Modified
                self.addLast(Patient(name, year, covid, vaccine))

            tsv_file.close()

    def insert_before_patient_node(self, patient:object, patient_node:object, patient_node_when_initial_list:bool):
        """Insert a patient before the patient_node"""
        newNode = DNode(patient)

        if patient_node_when_initial_list:
            newNode.next = patient_node_when_initial_list
            newNode.prev = patient_node_when_initial_list.prev

            patient_node_when_initial_list.prev.next = newNode
            patient_node_when_initial_list.prev = newNode
        else:
            newNode.next = patient_node
            newNode.prev = patient_node.prev

            patient_node.prev.next = newNode
            patient_node.prev = newNode

        self._size += 1

    def insert_after_patient_node(self, patient:object, patient_node:object, patient_node_when_initial_list:bool):
        """Insert a patient after the patient_node"""
        newNode = DNode(patient)

        if patient_node_when_initial_list:
            newNode.next = patient_node_when_initial_list.next
            newNode.prev = patient_node_when_initial_list

            if patient_node_when_initial_list.next == None:
                self._tail = newNode

            patient_node_when_initial_list.next = newNode
            # patient_node_when_initial_list.next.prev = newNode
        else:
            newNode.next = patient_node.next
            newNode.prev = patient_node

            patient_node.next.prev = newNode
            patient_node.next = newNode

        self._size += 1

    def addPatient(self, patient:object, initial_list: object = None):
        """
        Adds patient to patients list (Sorted alphabetically)

        :patient: Information about a patient
        :initial_list: Allow us to work with another list as the main list

        Information about the method:
            - Insert the new patient in its corresponding position in the list
            - The patient is only added if he/she is not stored in the patients list.
            - Complexity: Linear
        """ 
        if self.isEmpty():
            self.addFirst(patient)
            return
        
        # We use a simple normalization making lowercase all the words
        name = patient.name.split(", ")[1].lower() 
        surname = patient.name.split(", ")[0].lower() # Lozano
        
        if initial_list:
            patient_node = initial_list._head
            patient_node_when_initial_list = self._head
        else:
            patient_node = self._head
            patient_node_when_initial_list = None

        # last_name_less_than_input_name = ""
        # "aab" > "aaa" -> True
        while patient_node:
            patient_node_name = patient_node.elem.name.split(", ")[1].lower()
            patient_node_surname = patient_node.elem.name.split(", ")[0].lower()

            list_head = self._head if not initial_list else initial_list._head

            if patient_node == list_head:
                if patient_node_surname > surname: # Lozano, Abad
                    # The patient should be at the beginning
                    self.addFirst(patient)
                    return
                elif patient_node_surname == surname: # Abad, Abad
                    # We have to compare the names:
                    if (patient_node_name > name):
                        # Insert the patient at the initial position
                        self.addFirst(patient)
                        return
                    elif (patient_node_name == name):
                        # If the names are the same, do nothing
                        return
            elif (patient_node.prev.elem.name.split(", ")[0].lower() < surname and
                  patient_node.elem.name.split(", ")[0].lower() > surname):
                # Insert the patient before the patient_node
                self.insert_before_patient_node(patient, patient_node, patient_node_when_initial_list)
                return
            elif patient_node_surname == surname:
                # Surnames are the same,
                # so we've to compare the names
                if (patient_node_name > name):
                    self.insert_before_patient_node(patient, patient_node, patient_node_when_initial_list)
                    return
                elif (patient_node_name < name) or ((patient_node_name == name) and initial_list):
                    self.insert_after_patient_node(patient, patient_node, patient_node_when_initial_list)
                    return
                elif (patient_node_name == name):
                    # If the names are the same, do nothing
                    return
            elif patient_node.next == None:
                # Patient should be at the end
                self.addLast(patient)
                return
            patient_node = patient_node.next
            if patient_node_when_initial_list and patient_node_when_initial_list.next != None:
                # We avoid converting patient_node_when_initial_list in None.
                # This way, it enters into the conditional when adding a new patient
                patient_node_when_initial_list = patient_node_when_initial_list.next 

    def searchPatients(self, year:int, covid:bool = None, vaccine:int = None) -> object:
        """
        Args:
            year: Birth year. Ex.: 1974.
            covid: Indicates if the patient suffered from covid (True) or not (False).
            vaccine: Indicates if the patient has been vaccinated. Cases:
                -  0: Not vaccinated.
                -  1: First dose received.
                -  2: Second dose received.
        Return:
            new_health_center: Patient list which meets the search criteria
        """
        if self.isEmpty():
            print("There are no patients to look for")
            return None

        new_health_center = HealthCenter()
        patient_node = self._head

        while patient_node:
            patient = patient_node.elem # patient object
            add_patient_to_new_center = False
            
            if year == 2021 or patient.year <= year:
                # The patient satisfies the year query
                if not covid and vaccine == None:
                    # Search only using the year query
                    add_patient_to_new_center = True
                elif covid and vaccine == None:
                    # Search only using the year and covid queries
                    if covid == patient.covid:
                        add_patient_to_new_center = True
                elif not covid and vaccine != None:
                    # Search only using the year and vaccine queries
                    if vaccine == patient.vaccine:
                        add_patient_to_new_center = True
                else:
                    # Search using all the three queries
                    if covid == patient.covid and vaccine == patient.vaccine:
                        add_patient_to_new_center = True

            if add_patient_to_new_center:
                new_health_center.addPatient(patient, self)

            # Update the patient_node
            patient_node = patient_node.next
        
        return new_health_center

    def statistics(self) -> tuple:
        """
        Return:
            numcovid: % of patients who suffered from covid 
            numcovid1950: % of patients who suffered from covid and were born in 1950 or before
            novaccine: % of patients who didn't receive a vaccine
            novaccine1950: % of patients who didn't receive a vaccine and were born in 1950 or before
            numvaccine1: % of patients who already received the first dose
            numvaccine2: % of patients who already received the second dose

        All percentages follow the following notation: 0.##
        """
        numcovid = round(len(self.searchPatients(2021, True, None)) / self._size, 2)
        numcovid1950 = round(len(self.searchPatients(1950, True, None)) / \
                             len(self.searchPatients(1950, None, None)), 2)
        novaccine = round(len(self.searchPatients(2021, None, 0)) / self._size, 2)
        novaccine1950 = round(len(self.searchPatients(1950, None, 0)) / \
                              len(self.searchPatients(1950, None, None)), 2)
        numvaccine1 = round(len(self.searchPatients(2021, None, 1)) / self._size, 2)
        numvaccine2 = round(len(self.searchPatients(2021, None, 2)) / self._size, 2)

        return (numcovid, numcovid1950, novaccine, novaccine1950, numvaccine1, numvaccine2)

    def merge(self, other: object) -> object:
        """
        Args:
            other: HealthCenter object (other center)
        Return:
	      new_health_center: merge(invoking center, other center)

        Information about the method:
            - List of patients must be sorted alphabetically
            - No duplicates allowed. In case of duplicates keep only patients from
                invoking center. 
            - Complexity: Linear 	 
        """
        new_health_center = HealthCenter() 

        invoking_list_node = self._head

        while invoking_list_node:
            new_health_center.addPatient(invoking_list_node.elem, self)
            invoking_list_node = invoking_list_node.next

        other_list_node = other._head

        while other_list_node:
            # name = str(other_list_node.elem.name.split(", ")[1].lower())

            # if name == "mark":
            #     print("######################")
            #     print("Attention")
            #     print("######################")

            new_health_center.addPatient(other_list_node.elem)
            other_list_node = other_list_node.next
            # print(f"{new_health_center}\nWe're adding {other_list_node.elem.name}", end="\n\n")

        return new_health_center

    def is_patient_in_the_list(self, patient:object, dlist:object) -> bool:
        """Check if the given patient is on dlist"""
        patient_node = dlist._head

        while patient_node:
            if patient_node.elem.name == patient.name:
                return True

            patient_node = patient_node.next

        return False

    def minus(self, other:object) -> object:
        """
        Args:
            other: Number of patients from HealthCenter class
       
        Return:
            new_health_center: Patients from invoking center and not belonging to 
            other center.

        Information about the method:
        - List of patients must be sorted alphabetically (no sorting algorithm allowed) 
        - No duplicates allowed. In case of duplicates keep only patients from
            invoking center. 
        - Efficent as possible.
        """
        new_health_center = HealthCenter()

        invoking_list_node = self._head

        while invoking_list_node:
            if not self.is_patient_in_the_list(invoking_list_node.elem, other):
                # If the patient is not in the invoking list, add it
                new_health_center.addPatient(invoking_list_node.elem, self)

            invoking_list_node = invoking_list_node.next

        return new_health_center

    def inter(self, other:object) -> object:
        """
        Args:
        Other(object): number of patients from HealthCenter class
     
        Return:
        new_health_center(list): patients belonging to invoking center and other 
        center.
        
        Information about the method:
        - List of patients must be sorted alphabetically (no sorting algorithm allowed) 
        - No duplicates allowed. In case of duplicates add once to the new center. 
        - Efficent as possible. Linear complexity?
            
        """
        new_health_center = HealthCenter()
        
        invoking_list_node = self._head

        while invoking_list_node:
            if self.is_patient_in_the_list(invoking_list_node.elem, other):
                # If the patient is not in the invoking list, add it
                new_health_center.addPatient(invoking_list_node.elem, self)

            invoking_list_node = invoking_list_node.next

        return new_health_center
