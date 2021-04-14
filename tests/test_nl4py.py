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
    
    def test_schedule_reporters(self):
        """
        Tests if schedule_reporters works properly
        """
        try:
            nl4py.initialize(self.nl_path)
        except:
            self.fail("NL4Py.intialize() fails!")
        workspace = nl4py.create_headless_workspace()
        workspace.open_model(self.ethnocentrism_model)
        workspace.command("setup-full")
        tick_count = 10
        reporters = ["ticks","count turtles"]
        results = workspace.schedule_reporters(reporters=reporters, start_at_tick = 0, 
            interval_ticks = 1, stop_at_tick = tick_count, go_command = 'go')
        self.assertEqual(len(results),tick_count)
        for idx, result in enumerate(results):
            self.assertEqual(len(result),len(reporters))
            self.assertEqual(eval(result[0]),idx+1)

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
        run_count = 20
        tick_count = 10
        reporters = ["ticks","count turtles"]
        all_runs_results = nl4py.run_experiment(model_name=self.ethnocentrism_model, setup_callback=setup_model, setup_data=range(run_count), 
            reporters=reporters, start_at_tick=0, interval_ticks=1, stop_at_tick=tick_count)
        self.assertEqual(all_runs_results.Run.unique().shape[0], run_count)
        for _, run_results in all_runs_results.groupby("Run"):
            self.assertEqual(run_results['Setup Commands'].iloc[0].replace(" ",""),setup_model(0).replace(" ",""))
            self.assertEqual(len(run_results['ticks'].unique()), tick_count)
            self.assertEqual(run_results.drop(['Run','Setup Commands'], axis=1).shape[1], len(reporters))
            self.assertEqual(run_results.ticks.astype(float).astype(int).tolist(), list(range(1,tick_count+1)))

 
if __name__ == '__main__':
    unittest.main()
