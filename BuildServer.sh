mkdir -p bin/NetLogo6.0/
mkdir -p bin/NetLogo6.1/
#Compile NetLogo 6.0 server
#provide path to netlogo jar file (include jar file name)
NetLogo6_0_Path="$1"
javac -d bin/NetLogo6.0/ -cp "./lib/py4j0.10.6.jar:$NetLogo6_0_Path:." src/server_NetLogo6.0/server/bsearch/space/*.java src/server_NetLogo6.0/server/bsearch/nlogolink/*.java src/server_NetLogo6.0/server/*.java
#provide path to netlogo jar file (include jar file name)
#Compile NetLogo 6.1 server
NetLogo6_1_Path="$2"
javac -d bin/NetLogo6.1/ -cp "./lib/py4j0.10.6.jar:$NetLogo6_1_Path:." src/server_NetLogo6.1/server/bsearch/space/*.java src/server_NetLogo6.1/server/bsearch/nlogolink/*.java src/server_NetLogo6.1/server/*.java
#Copy over manifests
cp src/server_NetLogo6.0/server/Manifest.txt bin/NetLogo6.0/
cp src/server_NetLogo6.1/server/Manifest.txt bin/NetLogo6.1/
#Build jars 
cd "bin/NetLogo6.0/"
jar cvfm NetLogoControllerServer.jar Manifest.txt bsearch nl4py
mkdir -p ../../src/client/NL4Py/nl4py/nl4pyServer/NetLogo6.0
cp NetLogoControllerServer.jar ../../src/client/NL4Py/nl4py/nl4pyServer/NetLogo6.0
cp ../../lib/py4j0.10.6.jar ../../src/client/NL4Py/nl4py/nl4pyServer/NetLogo6.0
cd "../NetLogo6.1/"
jar cvfm NetLogoControllerServer.jar Manifest.txt bsearch nl4py
mkdir -p ../../src/client/NL4Py/nl4py/nl4pyServer/NetLogo6.1
cp NetLogoControllerServer.jar ../../src/client/NL4Py/nl4py/nl4pyServer/NetLogo6.1
cp ../../lib/py4j0.10.6.jar ../../src/client/NL4Py/nl4py/nl4pyServer/NetLogo6.1
cd ../..
