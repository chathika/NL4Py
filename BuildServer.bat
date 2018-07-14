javac -d bin -cp "C:/Users/ch328575/AppData/Local/Continuum/Anaconda2/share/py4j/py4j0.10.6.jar;C:/Program Files/NetLogo 6.0.2/app/netlogo-6.0.2.jar;." src/server/bsearch/space/*.java src/server/bsearch/nlogolink/*.java src/server/*.java
cp src/server/Manifest.txt bin
cd bin
jar cvfm NetLogoControllerServer.jar Manifest.txt bsearch nl4py
xcopy /s "%~dp0\bin\NetLogoControllerServer.jar" "%~dp0\src\client\NL4Py\nl4py\nl4pyServer\"
xcopy /s "%~dp0\lib\py4j0.10.6.jar" "%~dp0\src\client\NL4Py\nl4py\nl4pyServer\"
cd ..

