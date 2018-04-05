javac -d bin -cp "C:/Users/ch328575/AppData/Local/Continuum/Anaconda2/share/py4j/py4j0.10.6.jar;C:/Program Files/NetLogo 6.0.2/app/netlogo-6.0.2.jar;." src/bsearch/space/*.java src/bsearch/nlogolink/*.java src/emd/server/*.java
cp src/Manifest.txt bin
cd bin
jar cvfm NetLogoControllerServer.jar Manifest.txt emd/server/NetLogoControllerServer.class bsearch emd
cd ..

