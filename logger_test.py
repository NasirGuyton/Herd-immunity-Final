from logger import Logger
import os


def test_logger():
    test_file = "test_log.txt"

    logger = Logger(test_file)
    logger.write_metadata(1000, 0.1, "Sniffles", 0.12, 0.5)
    logger.log_interactions(1, 100, 8)
    logger.log_infection_survival(1, 1000, 2)

    assert os.path.exists(test_file)

    with open(test_file, "r") as file:
        contents = file.read()
        assert "Simulation Start" in contents
        assert "Population Size" in contents
        assert "Step 1 Interactions" in contents
        assert "Step 1 Results" in contents

    os.remove(test_file)


if __name__ == "__main__":
    test_logger()
    print("logger_test passed")