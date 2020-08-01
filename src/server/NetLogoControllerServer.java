
//Nl4py by Chathika Gunaratne <chathikagunaratne@gmail.com>
package nl4py.server;

import java.util.HashMap;
import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;
import py4j.GatewayServer;
import nl4py.server.HeadlessWorkspaceController;

public class NetLogoControllerServer {
	
	static GatewayServer gs;
	
	public NetLogoControllerServer() {	
	}
	/**
	 * Launch the Gateway Server.
	 */
	public static void main(String[] args) {
		try {
			NetLogoControllerServer ncs = new NetLogoControllerServer();
			int port = Integer.parseInt(args[0]);
			gs = new GatewayServer(ncs, port);
			gs.start();
		} catch (Exception e){
			e.printStackTrace();
		}
	}
	/** 
	* Shutdown GatewayServer
	**/
	public void shutdownServer(){
		gs.shutdown(true);
	}
	/**
	 * Create a new gate way to handle comm for this workspace
	 * @return Py4J gateway server object
	 */
	public GatewayServer newGateway(){
		while (true) {
			int port = ThreadLocalRandom.current().nextInt(1025, 8081);
			try {
				GatewayServer gs = new GatewayServer(null, port);
				gs.start();
				return gs;
			} catch (Exception e) {
				continue;
			}
		}
	}
}