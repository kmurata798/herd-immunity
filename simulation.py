from virus import Virus
from logger import Logger
from person import Person
import random
import sys
random.seed(42)


class Simulation(object):
    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=1):
        self.pop_size = pop_size  # Int
        self.virus = virus  # Virus object
        self.initial_infected = initial_infected  # Int
        self.vacc_percentage = vacc_percentage  # float between 0 and 1
        self.total_vaccinated = 0
        self.next_person_id = 0  # Int
        self.total_infected = 0  # Int
        self.current_infected = 0  # Int
        self.additional_deaths = 0
        self.additional_vacc = 0
        self.total_dead = 0  # Int
        self.population = self._create_population(
            self.initial_infected)  # List of Person objects
        self.file_name = "log.txt"
        self.logger = Logger(self.file_name)
        self.newly_infected = []

        self.logger.write_metadata(self.pop_size, self.vacc_percentage,
                                   self.virus.name, self.virus.mortality_rate,
                                   self.virus.repro_rate)

    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''
        popu = []
        vacc_num = int(self.pop_size * self.vacc_percentage)
        for person_count in range(self.pop_size):
            if person_count < initial_infected:
                popu.append(Person(person_count, False, self.virus))
                self.total_infected += 1
            elif person_count < initial_infected + vacc_num:
                popu.append(Person(person_count, True))
                self.total_vaccinated += 1
            else:
                popu.append(Person(person_count, False))
        return popu

        # for count in range(self.initial_infected):
        #     infected_person = Person(person_id, False, self.virus)
        #     pop.append(infected_person)
        #     person_id += 1
        # for count in range(self.initial_vaccinated):
        #     vaccinated_person = Person(person_id, True)
        #     pop.append(vaccinated_person)
        #     person_id += 1
        # for count in self.population:
        #     normal = Person(person_id)
        #     pop.append(normal)
        #     person_id += 1
        # return pop

    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        if len(self.get_infected()) == 0:
            return False
        else:
            return True

    def get_infected(self):
        infected_list = []
        self.current_infected = 0
        for person in self.population:
            if person.infection != None and person.is_alive:
                infected_list.append(person)
                self.current_infected += 1

        return infected_list

    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        time_step_count = 0
        should_continue = True

        while should_continue:
            time_step_count += 1
            self.time_step()
            self.logger.log_time_step(self.virus.name, time_step_count, self.current_infected,
                                      self.additional_deaths, self.additional_vacc,
                                      self.total_infected, self.total_dead,
                                      self.total_vaccinated)
            should_continue = self._simulation_should_continue()

        print(f'The simulation has ended after {time_step_count} turns.')

    def time_step(self):
        ''' This method should containˀ all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        self.additional_deaths = 0
        self.additional_vacc = 0
        infected_list = self.get_infected()

        for person in infected_list:
            interaction_count = 0
            while interaction_count < 100:
                random_person = random.choice(self.population)
                while random_person.is_alive == False:
                    random_person = random.choice(self.population)
                self.interaction(person, random_person)
                interaction_count += 1
                print(interaction_count)

        # Check if infected people survive the infection
        for person in infected_list:
            survived = person.did_survive_infection()
            if survived == True:
                self.total_vaccinated += 1
                self.additional_vacc += 1
                self.logger.log_infection_survival(person, False)
            else:
                self.total_dead += 1
                self.additional_deaths += 1
                self.logger.log_infection_survival(person, True)

        # Infect newly infected people
        self._infect_newly_infected()
        self.get_infected()

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

        if random_person.is_vaccinated:
            self.logger.log_interaction(
                person, random_person, True, False, False)
        elif random_person.infection is not None:
            self.logger.log_interaction(
                person, random_person, True, False, False)

        else:
            infected_chance = random.random()
            if (infected_chance < person.infection.repro_rate):
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(
                    person, random_person, False, False, True)
            else:
                self.logger.log_interaction(
                    person, random_person, False, False, False)

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        for person in self.newly_infected:
            self.population[person].infection = self.virus
            self.total_infected += 1
        self.newly_infected.clear()


def test_infect_newly_infected():
    virus = Virus("test", 0.8, 0.2)
    sim = Simulation(100, 0.5, virus, 10)

    sim._infect_newly_infected()
    assert sim.total_infected == 10


def test_create_population():
    virus = Virus("Test", 0.8, 0.2)
    #             name, repro, mortality rate
    sim = Simulation(100, 0.5, virus, 10)
    #           popsize, vacc%, virus, initial infected

    infected_list = []
    vacc_list = []

    print("Total Population:", len(sim.population))
    assert len(sim.population) == 100

    for person in sim.population:
        if person.infection != None:
            infected_list.append(person)
        elif person.is_vaccinated:
            vacc_list.append(person)

    print("Infected", len(infected_list))
    assert len(infected_list) == 10

    print("Vaccinated", len(vacc_list))
    assert len(vacc_list) == 50

    assert sim.total_vaccinated == len(vacc_list)


def test_simulation_should_continue():
    virus = Virus("test", 0.8, 0.2)
    sim = Simulation(100, 0.5, virus, 10)
    # assert (len(sim.get_infected()) == 0) == False
    assert sim._simulation_should_continue() == True


def test_constructor():
    virus = Virus("test", 0.8, 0.2)
    sim = Simulation(100, 0.5, virus, 10)

    assert sim.pop_size == 100
    assert sim.vacc_percentage == 0.5
    assert sim.virus == virus
    assert sim.initial_infected == 10
# def test_run():
#     virus = Virus("Test", 0.8, 0.2)
#     #             name, repro, mortality rate
#     sim = Simulation(100, 0.5, virus, 10)
#     #           popsize, vacc%, virus, initial infected
#     sim.run()
#     assert print() == 'The simulation has ended after 2 turns.'


if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_rate = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_rate, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, virus, initial_infected)

    sim.run()
    # python3 simulation.py Ebola 0.25 0.70 200 0.90 10
    #                       name repro morta pop vac% infected

    # python3 simulation.py YellowFever 0.03 0.07 200 0.90 10
                    #             name repro morta pop vac% infected