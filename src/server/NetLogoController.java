//Customized for NL4Py by Chathika Gunaratne <chathikagunaratne@gmail.com>
package nl4py.server;

import py4j.GatewayServer;

import bsearch.space.*;
import java.util.ArrayList;

public abstract class NetLogoController {
	
	/**
	 * Create a new workspace
	 * Load a NetLogo model file into the headless workspace
	 * @param path: Path to the .nlogo file to load.
	 */
	public abstract void openModel(String path);
	
	/**
	 * Close the Netlogo file.
	 * @param unique id for this model
	 */
	public abstract void closeModel();

	public abstract void refresh();
	/**
	 * Export a view (the visualization area) to the Java file's working directory.
	 * @param filename: Name used to save the file. Include .png (ex: file.png)
	 */
	public abstract void exportView(String filename);
	
	/**
	 * Send a command to the open NetLogo model.
	 * @param command: NetLogo command syntax.
	 */
	public abstract void command(String command);
	/**
	 * Get the value of a variable in the NetLogo model.
	 * @param command: The value to report.
	 * @return Java Object containing return info
	 */
	public abstract byte[] report(byte[] reporter);
	
	public abstract ArrayList<ArrayList<String>> scheduleReportersAndRun (ArrayList<byte[]> reporters, int startAtTick, int intervalTicks, int stopAtTick, String goCommand);
	
	public abstract SearchSpace getParamList(String path);
	
	protected abstract void disposeWorkspace();
}