import random
import sys
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        self.logger = Logger("simulation_log.txt")

        self.virus = virus
        self.pop_size = pop_size
        self.vacc_percentage = vacc_percentage
        self.initial_infected = initial_infected

        self.newly_infected = []
        self.population = self._create_population()

    def _create_population(self):
        population = []

        vaccinated_count = int(self.pop_size * self.vacc_percentage)

        # Create vaccinated people
        for i in range(vaccinated_count):
            population.append(Person(i, True))

        # Create initially infected people
        for i in range(vaccinated_count, vaccinated_count + self.initial_infected):
            population.append(Person(i, False, self.virus))

        # Create remaining healthy, unvaccinated people
        for i in range(vaccinated_count + self.initial_infected, self.pop_size):
            population.append(Person(i, False))

        return population

    def _simulation_should_continue(self):
        infected_count = 0
        healthy_unvaccinated_living_count = 0
        living_count = 0

        for person in self.population:
            if person.is_alive:
                living_count += 1

                if person.infection is not None:
                    infected_count += 1

                if person.infection is None and not person.is_vaccinated:
                    healthy_unvaccinated_living_count += 1

        if living_count == 0:
            return False

        if infected_count == 0:
            return False

        if healthy_unvaccinated_living_count == 0:
            return False

        return True

    def run(self):
        # Write initial metadata once at the start
        self.logger.write_metadata(
            self.pop_size,
            self.vacc_percentage,
            self.virus.name,
            self.virus.mortality_rate,
            self.virus.repro_rate
        )

        time_step_counter = 0

        while self._simulation_should_continue():
            time_step_counter += 1
            self.time_step(time_step_counter)

        # Final summary counts
        living = 0
        dead = 0
        vaccinated = 0

        for person in self.population:
            if person.is_alive:
                living += 1
            else:
                dead += 1

            if person.is_vaccinated:
                vaccinated += 1

        with open(self.logger.file_name, "a") as file:
            file.write("\n=== Simulation End ===\n")
            file.write(f"Total Steps:\t{time_step_counter}\n")
            file.write(f"Living:\t{living}\n")
            file.write(f"Dead:\t{dead}\n")
            file.write(f"Vaccinated:\t{vaccinated}\n")

        print("Simulation complete.")
        print("Steps:", time_step_counter)
        print("Living:", living)
        print("Dead:", dead)
        print("Vaccinated:", vaccinated)

    def time_step(self, step_number):
        infected_people = []

        # Snapshot infected people at start of step
        for person in self.population:
            if person.is_alive and person.infection is not None:
                infected_people.append(person)

        interaction_count = 0

        # Each infected person interacts with 100 random living people
        for infected_person in infected_people:
            for _ in range(100):
                random_person = random.choice(self.population)

                # dead people do not interact
                while not random_person.is_alive:
                    random_person = random.choice(self.population)

                self.interaction(infected_person, random_person)
                interaction_count += 1

        new_infections_count = len(self.newly_infected)

        # Infect people only after all interactions are done
        self._infect_newly_infected()

        fatalities = 0

        # Resolve outcome for those who started this step infected
        for infected_person in infected_people:
            survived = infected_person.did_survive_infection()
            if not survived:
                fatalities += 1

        self.logger.log_interactions(step_number, interaction_count, new_infections_count)
        self.logger.log_infection_survival(step_number, self.pop_size, fatalities)

    def interaction(self, infected_person, random_person):
        # No effect if same person
        if infected_person._id == random_person._id:
            return

        # Dead people cannot be infected
        if not random_person.is_alive:
            return

        # Vaccinated people cannot be infected
        if random_person.is_vaccinated:
            return

        # Already infected people cannot be infected again
        if random_person.infection is not None:
            return

        # Healthy unvaccinated person can become infected
        random_num = random.random()
        if random_num < self.virus.repro_rate:
            if random_person not in self.newly_infected:
                self.newly_infected.append(random_person)

    def _infect_newly_infected(self):
        for person in self.newly_infected:
            person.infection = self.virus

        self.newly_infected = []


if __name__ == "__main__":
    if len(sys.argv) >= 6:
        pop_size = int(sys.argv[1])
        vacc_percentage = float(sys.argv[2])
        virus_name = sys.argv[3]
        mortality_rate = float(sys.argv[4])
        repro_rate = float(sys.argv[5])

        if len(sys.argv) >= 7:
            initial_infected = int(sys.argv[6])
        else:
            initial_infected = 1

        virus = Virus(virus_name, repro_rate, mortality_rate)
        sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)
        sim.run()
    else:
        # Default test run
        virus_name = "Sniffles"
        repro_rate = 0.5
        mortality_rate = 0.12
        virus = Virus(virus_name, repro_rate, mortality_rate)

        pop_size = 1000
        vacc_percentage = 0.1
        initial_infected = 10

        sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)
        sim.run()