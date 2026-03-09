class Virus(object):
    # Properties and attributes of the virus used in Simulation.
    def __init__(self, name, repro_rate, mortality_rate):
        self.name = name
        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate

# Test this class
if __name__ == "__main__":
    virus = Virus("HIV", 0.8, 0.3)
    assert virus.name == "HIV"
    assert virus.repro_rate == 0.8
    assert virus.mortality_rate == 0.3

    virus2 = Virus("Flu", 0.4, 0.05)
    assert virus2.name == "Flu"
    assert virus2.repro_rate == 0.4
    assert virus2.mortality_rate == 0.05

    virus3 = Virus("Ebola", 0.25, 0.7)
    assert virus3.name == "Ebola"
    assert virus3.repro_rate == 0.25
    assert virus3.mortality_rate == 0.7