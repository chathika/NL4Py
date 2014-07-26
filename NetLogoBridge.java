package Py2NetLogo;

import py4j.GatewayServer;
import org.nlogo.headless.HeadlessWorkspace;

public class NetLogoBridge {
	
	HeadlessWorkspace ws;
	
	public NetLogoBridge() {
		ws = HeadlessWorkspace.newInstance();
	}
	
	/**
	 * Load a NetLogo model file into the headless workspace.
	 * @param path: Path to the .nlogo file to load.
	 */
	public void openModel(String path) {
		ws.open(path);
	}
	
	/**
	 * Send a command to the open NetLogo model.
	 * @param command: NetLogo command syntax.
	 */
	public void command(String command) {
		ws.command(command);
	}
	/**
	 * Get the value of a variable in the NetLogo model.
	 * @param command: The value to report.
	 * @return Floating point number
	 */
	public Double report(String command) {
		return (Double)ws.report(command);
	}
	
	/**
	 * Launch the Gateway Server.
	 */
	public static void main(String[] args) {
		GatewayServer gs = new GatewayServer(new NetLogoBridge());
		gs.start();
		System.out.println("Server running");

	}

}
