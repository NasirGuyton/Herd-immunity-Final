from simulation import Simulation
from virus import Virus


def test_simulation_population():
    virus = Virus("TestVirus", 0.5, 0.1)
    sim = Simulation(virus, 100, 0.2, 5)

    assert len(sim.population) == 100

    vaccinated_count = 0
    infected_count = 0
    healthy_count = 0

    for person in sim.population:
        if person.infection is not None:
            infected_count += 1
        elif person.is_vaccinated:
            vaccinated_count += 1
        else:
            healthy_count += 1

    assert vaccinated_count == 20
    assert infected_count == 5
    assert healthy_count == 75


def test_simulation_continue():
    virus = Virus("TestVirus", 0.5, 0.1)
    sim = Simulation(virus, 20, 0.0, 1)

    assert sim._simulation_should_continue() is True


if __name__ == "__main__":
    test_simulation_population()
    test_simulation_continue()
    print("simulation_test passed")