# -*- coding: utf-8 -*-


from binarysearchtree import BinarySearchTree

import csv      #read files csv, tsv
import os.path  #to work with files and directory https://docs.python.org/3/library/os.path.html
import queue    #package implementes a queueu, https://docs.python.org/3/library/queue.html
import re       #working with regular expressions

def checkFormatHour(time):
    """checks if the time follows the format hh:dd"""
    pattern = re.compile(r'\d{2}:\d{2}')  # busca la palabra foo
    
    if pattern.match(time):
        data=time.split(':')
        hour=int(data[0])
        minute=int(data[1])
        if hour in range(8,20) and minute in range(0,60,5):
            return True
    
    return False




#number of all possible appointments for one day
NUM_APPOINTMENTS=144

class Patient:
    """Class to represent a Patient"""
    def __init__(self,name,year,covid,vaccine,appointment=None):

        self.name=name
        self.year=year
        self.covid=covid
        self.vaccine=vaccine
        self.appointment=appointment     #string with format hour:minute

    def setAppointment(self,time):
        """gets a string with format hour:minute"""
        self.appointment=time
        
    def __str__(self):
        return self.name+'\t'+str(self.year)+'\t'+str(self.covid)+'\t'+str(self.vaccine)+'\t appointment:'+str(self.appointment)

    def __eq__(self,other):
        return  other!=None and self.name == other.name 



class HealthCenter2(BinarySearchTree):
    """Class to represent a Health Center. This class is a subclass of a binary search tree to 
    achive a better temporal complexity of its algorithms for 
    searching, inserting o removing a patient (or an appointment)"""


    def __init__(self,filetsv=None,orderByName=True):
        """
        This constructor allows to create an object instance of HealthCenter2. 
        It takes two parameters:
        - filetsv: a file csv with the information about the patients whe belong to this health center
        - orderByName: if it is True, it means that the patients should be sorted by their name in the binary search tree,
        however, if is is False, it means that the patients should be sorted according their appointments
        """

        #Call to the constructor of the super class, BinarySearchTree.
        #This constructor only define the root to None
        super(HealthCenter2, self).__init__()
        
        #Now we 
        if filetsv is None or not os.path.isfile(filetsv):
            #If the file does not exist, we create an empty tree (health center without patients)
            self.name=''
            #print('File does not exist ',filetsv)
        else: 
            order='by appointment'
            if orderByName:
                order='by name'

            #print('\n\nloading patients from {}. The order is {}\n\n'.format(filetsv,order))
            
            self.name=filetsv[filetsv.rindex('/')+1:].replace('.tsv','')
            #print('The name of the health center is {}\n\n'.format(self.name))
            #self.name='LosFrailes'

            fichero = open(filetsv)
            lines = csv.reader(fichero, delimiter="\t")
    
            for row in lines:
                #print(row)
                name=row[0] #nombre
                year=int(row[1]) #año nacimiento
                covid=False
                if int(row[2])==1:          #covid:0 o 1
                    covid=True
                vaccine=int(row[3])         #número de dosis
                try:
                    appointment=row[4]
                    if checkFormatHour(appointment)==False:
                        #print(appointment, ' is not a right time (hh:minute)')
                        appointment=None
                        
                except:
                    appointment=None    

                objPatient=Patient(name,year,covid,vaccine,appointment)
                #name is the key, and objPatient the eleme
                if orderByName:
                    self.insert(name,objPatient)
                else:
                    if appointment:
                        self.insert(appointment,objPatient)
                    else:
                        print(objPatient, " was not added because appointment was not valid!!!")
    
            fichero.close()





    def searchPatients(self,year=2021,covid=None,vaccine=None):
        """return a new object of type HealthCenter 2 with the patients who
        satisfy the criteria of the search (parameters). 
        The function has to visit all patients, so the search must follow a level traverse of the tree.
        If you use a inorder traverse, the resulting tree should be a list!!!"""
        
        
        result=HealthCenter2()

        if self._root == None:
            # The tree is empty
            return result

        # Search patient main code
        q = queue.Queue()
        q.put(self._root)

        while q.empty() == False:

            # dequeue for obtaining the patient
            # using level order traversal
            patient = q.get()

            add_patient_to_new_center = False

            if year == 2021 or patient.elem.year <= year:
                # The patient satisfies the year query
                if not covid and vaccine == None:
                    # Search only using the year query
                    add_patient_to_new_center = True
                elif covid and vaccine == None:
                    # Search only using the year and covid queries
                    if covid == patient.elem.covid:
                        add_patient_to_new_center = True
                elif not covid and vaccine != None:
                    # Search only using the year and vaccine queries
                    if vaccine == patient.elem.vaccine:
                        add_patient_to_new_center = True
                else:
                    # Search using all the three queries
                    if covid == patient.elem.covid and vaccine == patient.elem.vaccine:
                        add_patient_to_new_center = True

            if add_patient_to_new_center:
                result.insert(patient.key, patient.elem)

            # Enqueue the next elements of the tree
            if patient.left != None:
                q.put(patient.left)
            if patient.right != None:
                q.put(patient.right)
    
        return result
            


    def vaccine(self,name,vaccinated) -> bool:
        """This functions simulates the vaccination of a patient whose
        name is name. It returns True if the patient is vaccinated and False in any other case"""
        if not self.search(name):
            print("The patient does not exist in the invoking health center")
            return False
        elif self.find(name).elem.vaccine == 2:
            # Patient has received two doses
            print("This patient has already been vaccinated")
            vaccinated_patient = self.find(name)
            vaccinated.insert(vaccinated_patient.key, vaccinated_patient.elem)
            self.remove(vaccinated_patient.key)
            
            return False
        elif self.find(name).elem.vaccine == 1:
            # Patient has received one dose
            # Update the number of doses to two
            vaccinated_patient = self.find(name)
            vaccinated_patient.elem.vaccine += 1
            vaccinated.insert(vaccinated_patient.key, vaccinated_patient.elem)
            self.remove(vaccinated_patient.key)
            
            return True
        elif self.find(name).elem.vaccine == 0:
            # Patient hasn't received any doses
            vaccinated_patient = self.find(name)
            vaccinated_patient.elem.vaccine += 1
            return True
        
    def isTimeInSchedule(self, time, schedule):
        if schedule._root == None:
            # Schedule is empty
            return False

        return self._isTimeInSchedule(time, schedule._root)
    
    def _isTimeInSchedule(self, time, schedule_node):
        # Base case
        if schedule_node == None:
            return False
        if schedule_node.elem.appointment == time:
            return True
        # Recursive case
        if time < schedule_node.key:
            return self._isTimeInSchedule(time, schedule_node.left)
        if time > schedule_node.key:
            return self._isTimeInSchedule(time, schedule_node.right)

    def findBestTime(self, time, schedule):
        """Returns the most time-close slot"""
        return self._findBestTime(time, schedule, time)

    def _findBestTime(self, time_test, schedule, time, time_difference=5, direction="down", finalDown=False, finalUp=False):
        """time_test is the time to check if it's busy"""
        # Base case
        if not self.isTimeInSchedule(time_test, schedule):
            return time_test

        # Recursive case
        hours, minutes = int(time[:2]), int(time[3:])
        total_minutes = hours * 60 + minutes

        # 8 * 60 is the earliest time to take an appointment
        if total_minutes <= 8 * 60:
            finalDown = True
        elif total_minutes >= 19 * 60 + 55:
            finalUp = True

        
        if finalDown:
            total_minutes += time_difference
            time_difference += 5
        elif finalUp:
            total_minutes -= time_difference
            time_difference += 5
        elif direction == "up":
            total_minutes += time_difference
            direction = "down"
            time_difference += 5
        elif direction == "down":
            direction = "up"
            total_minutes -= time_difference

        hours = int(total_minutes / 60)
        minutes = total_minutes - hours * 60
        if len(str(hours)) == 1:
            hours = "0" + str(hours)
        if len(str(minutes)) == 1:
            minutes = "0" + str(minutes)
        time_test = f"{hours}:{minutes}"

        return self._findBestTime(time_test, schedule, time, time_difference, direction, finalDown, finalUp)

    def makeAppointment(self,name,time,schedule):
        """ for the patient whose name is name. The function returns True if the appointment 
        is created and False in any other case """        
        # Each hour has (60 / 5) slots. Since there are 12 hours in the interval,
        # we can conclude that there are (60 / 5) * 12 slots
        total_slots = (60 / 5) * 12
        if schedule.size() == total_slots:
            print("There are no available slots")
            return False
        elif int(time[0:2]) < 8 or (int(time[0:2]) == 19 and int(time[3:]) > 55) or int(time[0:2]) > 19:
            return False
        elif not self.search(name):
            print("The patient does not exist in the invoking health center")
            return False
        elif self.find(name).elem.vaccine == 2:
            # Patient has received two doses
            print("This patient has already been vaccinated")
            return False
        elif self.find(name).elem.vaccine == 1 or self.find(name).elem.vaccine == 0:
            # Patient has received one/zero doses
            if not self.isTimeInSchedule(time, schedule):
                # The time is free
                patient = self.find(name)
                patient.elem.appointment = time
                schedule.insert(time, patient.elem)
                
                return True
            
            # The time is not free
            new_appointment = self.findBestTime(time, schedule)

            patient = self.find(name)
            patient.elem.appointment = new_appointment

            schedule.insert(new_appointment, patient.elem)

            return True

if __name__ == '__main__':
    
    ###Testing the constructor. Creating a health center where patients are sorted by name
    o=HealthCenter2('data/LosFrailes2.tsv')
    o.draw()
    print()


    print('Patients who were born in or before than 1990, had covid and did not get any vaccine')
    result=o.searchPatients(1990, True,0)
    result.draw()
    print()

    print('Patients who were born in or before than 1990, did not have covid and did not get any vaccine')
    result=o.searchPatients(1990, False,0)
    result.draw()
    print()

    print('Patients who were born in or before than 1990 and got one dosage')
    result=o.searchPatients(1990, None,1)
    result.draw()
    print()

    print('Patients who were born in or before than 1990 and had covid')
    result=o.searchPatients(1990, True)
    result.draw()
    print()


    ###Testing the constructor. Creating a health center where patients are sorted by name
    schedule=HealthCenter2('data/LosFrailesCitas.tsv',False)
    schedule.draw(False)
    print()
    
    

    o.makeAppointment("Perez","08:00",schedule)
    o.makeAppointment("Losada","19:55",schedule)
    o.makeAppointment("Jaen","16:00",schedule)
    o.makeAppointment("Perez","16:00",schedule)
    o.makeAppointment("Jaen","16:00",schedule)

    o.makeAppointment("Losada","15:45",schedule)
    o.makeAppointment("Jaen","08:00",schedule)

    o.makeAppointment("Abad","08:00",schedule)
    o.makeAppointment("Omar","15:45",schedule)
    
    
    schedule.draw(False)

    vaccinated=HealthCenter2('data/vaccinated.tsv')
    vaccinated.draw(False)

    name='Ainoza'  #doest no exist
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)

    name='Abad'   #0 dosages
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)
    
   

    name='Font' #with one dosage
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)
    
    name='Omar' #with two dosage
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)
