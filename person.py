from virus import Virus
import random
random.seed(42)


class Person(object):
    ''' Person objects will populate the simulation. '''

    def __init__(self, _id, is_vaccinated=False, infection=None):
        ''' construct properties for Person object'''
        self._id = _id  # int
        self.is_alive = True  # boolean
        self.is_vaccinated = is_vaccinated  # boolean
        self.infection = infection  # Virus object or None

    def did_survive_infection(self):
        ''' Checks if the person survived'''
        if self.is_vaccinated == False:
            self.is_alive = False
            return False
        else:
            return True


''' These are simple tests to ensure that you are instantiating your Person class correctly. '''

def test_vacc_person_instantiation():
    # create some people to test if our init method works as expected
    person = Person(1, True)
    assert person._id == 1
    assert person.is_alive is True
    assert person.is_vaccinated is True
    assert person.infection is None


def test_not_vacc_person_instantiation():
    person = Person(2, False)
    assert person._id == 2
    assert person.is_alive is True
    assert person.is_vaccinated is False
    assert person.infection is None


def test_sick_person_instantiation():
    # Create a Virus object to give a Person object an infection
    virus = Virus("Dysentery", 0.7, 0.2)
    # Create a Person object and give them the virus infection
    person = Person(3, False, virus)
    assert person._id == 3
    assert person.is_alive is True
    assert person.is_vaccinated is False
    assert person.infection is virus


def test_did_survive_infection():

    virus = Virus("Dysentery", 0.7, 0.2)

    person = Person(4, False, virus)

    # Resolve whether the Person survives the infection or not
    survived = person.did_survive_infection()
    # Check if the Person survived or not
    if survived:
        assert person.is_alive is True
        assert person._id == 4
        assert person.is_vaccinated is True
        assert person.infection is None
    else:
        assert person.is_alive is False
        assert person._id == 4
        assert person.is_vaccinated is False
        assert person.infection is virus
