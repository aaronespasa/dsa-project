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
    def __init__(self, filetsv=None):
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

    def addPatient(self, patient):
        """
        Adds patient to patients list (Sorted alphabetically)

        :patient (object): Information about a patient

        Information about the method:
            - Insert the new patient in its corresponding position in the list
            - The patient is only added if he/she is not stored in the patients list.
            - Complexity: Linear
        """ 
        if self.isEmpty():
            self.addFirst(patient)
        
        # We use a simple normalization making lowercase all the words
        name = patient.name.split(", ")[1].lower() 
        surname = patient.name.split(", ")[0].lower() # Lozano
        patient_node = self._head

        i = 0
        # last_name_less_than_input_name = ""
        # "aab" > "aaa" -> True
        while patient_node:
            patient_node_name = patient_node.elem.name.split(", ")[1].lower()
            patient_node_surname = patient_node.elem.name.split(", ")[0].lower()

            if patient_node == self._head:
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
            elif patient_node.next == None:
                # Patient should be at the end
                self.addLast(patient)
                return
            elif (patient_node.prev.elem.name.split(", ")[0].lower() < surname and
                  patient_node.elem.name.split(", ")[0].lower() > surname):
                # Insert the patient at the current position
                newNode = DNode(patient)

                newNode.next = patient_node
                newNode.prev = patient_node.prev

                patient_node.prev.next = newNode
                patient_node.prev = newNode 

                self._size += 1
                return
            elif patient_node_surname == surname:
                # We have to compare the names:
                if (patient_node_name > name):
                    # Insert the patient before the name
                    newNode = DNode(patient)

                    newNode.next = patient_node
                    newNode.prev = patient_node.prev

                    patient_node.prev.next = newNode
                    patient_node.prev = newNode

                    self._size += 1
                    return
                elif (patient_node_name < name):
                    # Insert the patient after the name
                    newNode = DNode(patient)

                    newNode.next = patient_node.next
                    newNode.prev = patient_node

                    patient_node.next = newNode

                    self._size += 1
                    return
                elif (patient_node_name == name):
                    # If the names are the same, do nothing
                    return

            patient_node = patient_node.next
            i += 1 

    def searchPatients(self, year, covid=None, vaccine=None):
        """
        Args:
            :
        Return:
            :newCenter (object): Different center where the list patients
        """
        # newCenter = HealthCenter(filetsv=None)
        # if self.isEmpty():
        #     print("There are no patients to look for")
        #     return None
            
        # # case in which only year is given & covid & vaccine remain by default
        # if self.year: 
        pass

    def stastics(self):
        """
        Args:
            :
        Return:
            :
        """
        pass

    def merge(self, other):
        """
        Args:
        Other(object): number of patients from HealthCenter class
        Return:
	      new_health_center (list): patients of invoking center and patients
        of the other center

        Information about the method:
        - List of patients must be sorted alphabetically (no sorting algorithm allowed) 
				- No duplicates allowed. In case of duplicates keep only patients from
					invoking center. 
				- Complexity: Linear 	 
        """
        pass

    def minus(self, other):
        """
        Args:
        Other(object): number of patients from HealthCenter class
       
        Return:
        new_health_center(list): patients from invoking center and not belonging to 
        other center.

        Information about the method:
        - List of patients must be sorted alphabetically (no sorting algorithm allowed) 
				- No duplicates allowed. In case of duplicates keep only patients from
					invoking center. 
				- Efficent as possible. Linear complexity?
        """
        pass

    def inter(self, other):
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
        pass
