import os
def run_simulation(data):
    # Same netlogo commands as used for the PyNetLogo evaluation
    setup_commands = []
    setup_commands.append("random-seed " + str(data))
    #setup_commands.append("set mutation-rate 0.005")
    setup_commands.append("set death-rate 0.1")
    setup_commands.append("set immigrants-per-day 1")
    setup_commands.append("set immigrant-chance-cooperate-with-same 0.5")
    setup_commands.append("set immigrant-chance-cooperate-with-different 0.5")
    setup_commands.append("set initial-PTR 0.12")
    setup_commands.append("set cost-of-giving 0.01")
    setup_commands.append("set gain-of-receiving 0.03")
    setup_commands.append('setup-empty')
    return setup_commands