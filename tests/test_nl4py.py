import unittest
import os

import json

import nl4py


class TestNL4Py(unittest.TestCase):

    def setUp(self):
        tests_dir = "tests"
        with open(os.path.join(tests_dir,"config.json")) as f:
            self.config = json.load(f)
        self.nl_path = self.config["nl_path"]
        self.ethnocentrism_model = os.path.join(tests_dir,self.config["ethnocentrism_model"])

    def test_int(self):
        """
        Test that nl4py intializes
        """
        try:
            nl4py.initialize(self.nl_path)
        except:
            self.fail("NL4Py.intialize() fails!")
        try:
            nl4py.initialize(self.nl_path)
        except:
            self.fail("NL4Py.intialize() fails when called more than once!")

    def test_basic_model_execution(self):
        """
        Tests model running basics with the Ethnocentrism.nlogo model.
        """
        try:
            nl4py.initialize(self.nl_path)
        except:
            self.fail("NL4Py.intialize() fails!")
        workspace = nl4py.create_headless_workspace()
        workspace.open_model(self.ethnocentrism_model)
        workspace.command("setup-empty")
        ticks = workspace.report("ticks")
        turtle_count = workspace.report("count turtles")
        self.assertEqual(ticks,0)
        self.assertEqual(turtle_count,0)
        workspace.command("setup-full")
        ticks = workspace.report("ticks")
        turtle_count = workspace.report("count turtles")
        self.assertEqual(ticks,0)
        self.assertGreater(turtle_count,0)
        workspace.command("repeat 10 [go]")
        ticks = workspace.report("ticks")
        self.assertEqual(ticks,10)
    
    def test_run_experiment(self):
        """
        Tests if run_experiment works properly
        """
        try:
            nl4py.initialize(self.nl_path)
        except:
            self.fail("NL4Py.intialize() fails!")
        def setup_model(run):
            return "setup-full"
        run_count = 10
        results = nl4py.run_experiment(model_name=self.ethnocentrism_model, setup_callback=setup_model, setup_data=range(run_count), 
            reporters=["count turtles"], start_at_tick=0, interval=1, stop_at_tick=10)
        self.assertEqual(len(results), run_count)
 
if __name__ == '__main__':
    unittest.main()
