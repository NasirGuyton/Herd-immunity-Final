import random
# random.seed(42)
from virus import Virus


class Person(object):
    # Define a person.
    def __init__(self, _id, is_vaccinated, infection=None):
        # A person has an id, is_vaccinated and possibly an infection
        self._id = _id
        self.is_vaccinated = is_vaccinated
        self.infection = infection
        self.is_alive = True

    def did_survive_infection(self):
        # Only called if infection attribute is not None.
        if self.infection is None:
            return True

        random_num = random.random()

        if random_num < self.infection.mortality_rate:
            self.is_alive = False
            self.infection = None
            return False
        else:
            self.is_vaccinated = True
            self.infection = None
            return True


if __name__ == "__main__":
    # Define a vaccinated person and check their attributes
    vaccinated_person = Person(1, True)
    assert vaccinated_person._id == 1
    assert vaccinated_person.is_alive is True
    assert vaccinated_person.is_vaccinated is True
    assert vaccinated_person.infection is None

    # Create an unvaccinated person and test their attributes
    unvaccinated_person = Person(2, False)
    assert unvaccinated_person._id == 2
    assert unvaccinated_person.is_alive is True
    assert unvaccinated_person.is_vaccinated is False
    assert unvaccinated_person.infection is None

    # Test an infected person. An infected person has an infection/virus
    virus = Virus("Dysentery", 0.7, 0.2)
    infected_person = Person(3, False, virus)
    assert infected_person._id == 3
    assert infected_person.is_alive is True
    assert infected_person.is_vaccinated is False
    assert infected_person.infection == virus

    # Check survival across many infected people
    people = []
    for i in range(1, 100):
        person = Person(i, False, virus)
        people.append(person)

    did_survive = 0
    did_not_survive = 0

    for person in people:
        person.did_survive_infection()
        if person.is_alive:
            did_survive += 1
        else:
            did_not_survive += 1

    print("Survived:", did_survive)
    print("Died:", did_not_survive)