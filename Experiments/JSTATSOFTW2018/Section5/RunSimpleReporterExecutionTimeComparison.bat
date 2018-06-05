@echo on
if "%~1"==""	(
	ECHO Please enter the path to your NetLogo installation as an argument! 
	cmd /k
)
set netlogo_path="%~1"
FOR /L %%A IN (1,1,10) DO (
  python nl4py_gunaratne2018_5.2.fire.nl4py.py %netlogo_path%
)
FOR /L %%A IN (1,1,10) DO (
  python nl4py_gunaratne2018_5.2.fire.pynetlogo.py %netlogo_path%
)
FOR /L %%A IN (1,1,10) DO (
  python nl4py_gunaratne2018_5.2.ethnocentrism.nl4py.py %netlogo_path%
)
FOR /L %%A IN (1,1,10) DO (
  python nl4py_gunaratne2018_5.2.ethnocentrism.pynetlogo.py %netlogo_path%
)
FOR /L %%A IN (1,1,10) DO (
  python nl4py_gunaratne2018_5.2.wolfsheeppredation.nl4py.py %netlogo_path%
)
FOR /L %%A IN (1,1,10) DO (
  python nl4py_gunaratne2018_5.2.wolfsheeppredation.pynetlogo.py %netlogo_path%
)

