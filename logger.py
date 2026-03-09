class Logger(object):
    def __init__(self, file_name):
        # store the filename so other methods can write to it
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        # create/overwrite the file and write starting information
        with open(self.file_name, "w") as file:
            file.write("=== Simulation Start ===\n")
            file.write(f"Population Size:\t{pop_size}\n")
            file.write(f"Vaccination Percentage:\t{vacc_percentage}\n")
            file.write(f"Virus Name:\t{virus_name}\n")
            file.write(f"Mortality Rate:\t{mortality_rate}\n")
            file.write(f"Basic Reproduction Number:\t{basic_repro_num}\n")
            file.write("\n")

    def log_interactions(self, step_number, number_of_interactions, number_of_new_infections):
        with open(self.file_name, "a") as file:
            file.write(f"Step {step_number} Interactions:\t")
            file.write(f"Total Interactions = {number_of_interactions}\t")
            file.write(f"New Infections = {number_of_new_infections}\n")

    def log_infection_survival(self, step_number, population_count, number_of_new_fatalities):
        with open(self.file_name, "a") as file:
            file.write(f"Step {step_number} Results:\t")
            file.write(f"Population = {population_count}\t")
            file.write(f"New Fatalities = {number_of_new_fatalities}\n")

if __name__ == "__main__":
    logger = Logger("log.txt")
    logger.write_metadata(1000, 0.1, "Sniffles", 0.12, 0.5)
    logger.log_interactions(1, 100, 8)
    logger.log_infection_survival(1, 1000, 2)
    print("Logger test complete. Check log.txt")        