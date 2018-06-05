@echo on
if "%~1"==""	(
	ECHO Please enter the path to your NetLogo installation as an argument! 
	cmd /k
)
set netlogo_path="%~1"

FOR /L %%A IN (1,1,2) DO (
  python nl4py_gunaratne2018_5.wolfsheeppredation.pynetlogo.py %netlogo_path%
)

