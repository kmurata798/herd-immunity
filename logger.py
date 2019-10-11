import io
from person import Person
from virus import Virus


class Logger(object):
    '''logger class writes the info into the log.txt file'''
    def __init__(self, file_name):
        '''constructs the properties for Logger class'''
        self.file_name = file_name

        new_file = open(self.file_name, mode='w+')
        print(new_file.read())
        new_file.close()

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        '''writes down the population info at the start of the program'''
        with open(self.file_name, mode='w') as new_file:
            metadata = f'Population Size: {pop_size}\nVaccination Percentage: {vacc_percentage}\nVirus Name: {virus_name}\nMortality Rate: {mortality_rate}\nBasic Reproduction Number: {basic_repro_num}\n'
            new_file.write(metadata)
        new_file.close()

    def log_interaction(self, person, random_person, random_person_sick=None,
                        random_person_vacc=None, did_infect=None):
        ''''writes down the interactions between people in the population'''
        with open(self.file_name, mode='a') as new_file:
            new_file.write('Interaction Logs: \n')
            if did_infect:
                infection_status = str(person._id) + \
                    ' infects ' + str(random_person._id) + '\n'
            elif random_person.is_vaccinated:
                infection_status = str(
                    person._id) + ' did not infect ' + str(random_person._id) + '\n'
            else:
                infection_status = str(person._id) + ' did not infect ' + str(
                    random_person._id) + ' because ' + str(random_person._id) + ' is vaccinated or already sick.' + '\n'
                # print('Infection Status --> ', infection_status)
            new_file.write(infection_status)
            new_file.close()

    def log_infection_survival(self, person, did_die_from_infection):
        '''writes down the data for survival of infection'''
        with open(self.file_name, mode='a') as new_file:
            new_file.write('Infection Survival: \n')
            if not did_die_from_infection:
                infection_status = str(person._id) + \
                    ' survived infection.' + '\n'
            else:
                infection_status = str(person._id) + ' died from infection.' + '\n'
            new_file.write(infection_status)    
            new_file.close()

    def log_time_step(self, virus_name, time_step_number, additional_infected, additional_deaths, additional_vacc, total_infected, total_dead, total_vaccinated):
        '''Writes down the data for population'''
        with open(self.file_name, mode='a') as new_file:
            new_file.write(f'----------------------\nVIRUS: {virus_name}\nInfections during this step: {additional_infected}\nTotal infections: {total_infected}\nDeaths during this step: {additional_deaths}\nVaccinations during this step: {additional_vacc}\nTotal Vaccinations: {total_vaccinated}\n')
            time_step_status = str(f'Time step {time_step_number} ended -- Beginning '
            f'{time_step_number + 1}\n')
            new_file.write(time_step_status)
            new_file.close()
