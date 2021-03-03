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
            print('loading the data for the health center from the file ', filetsv)

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

    def addPatient(self, patient):
        """
        Adds patient to patients list (Sorted alphabetically)

        :patient (object): Information about a patient

        Information about the method:
            - Insert the new patient in its corresponding position in the list
            - The patient is only added if he/she is not stored in the patients list.
            - Complexity: Linear <- TimSort to sort aphabetically
        """ 
        name = patient.name.split(", ")[0] # Lozano

        first_name = self.getAt(0).name.split(", ")[0]
        last_name = self.getAt(self.size - 1).name.split(", ")

        print(name)
        if name[0] == last_name[0]:
            # The patient we're adding should be at the end
            
            position_found = False
            # We use the index to obtain the position of the word.
            # If index=1, name=Yuya and last_name=Yoyo,
            # we will check if u (name[1]) is greater, less or equal
            # than the o.
            # It starts by 1 because we want to check the letters
            # from this point forward
            index = 1

            while not position_found:
                if name[1] > last_name[1]:
                    pass
                elif name[1] < last_name[1]:
                    pass
                else:
                    # name[i] == name[i + 1]
                    pass

            
        elif name[0] == first_name[0]:
            # The patient we're adding should be at the beginning
            pass
        else:
            # The initial of the patient is not the same than the intial one
            # nor than the last one
            for i in range(self.size):
                if name[0] > self.getAt(i - 1).name.split(", ")[0] and name[0] < self.getAt(i + 1).name.split(", ")[0]:
                    # Check if the patient we're adding is between two patients
                    pass

    def searchPatients(self, year, covid=None, vaccine=None):
        """
        Args:
            :
        Return:
            :newCenter (object): Different center where the list patients
        """
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
