//Customized for NL4Py by Chathika Gunaratne <chathikagunaratne@gmail.com>
package nl4py.server;

import py4j.GatewayServer;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import bsearch.nlogolink.NetLogoLinkException;
import javax.imageio.ImageIO;
import bsearch.space.*;
import java.util.HashMap;
import org.nlogo.headless.HeadlessWorkspace; 
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.ArrayList;
import java.util.List;

public abstract class NetLogoController {
	
	HeadlessWorkspace ws;
	private ArrayBlockingQueue<String> commandQueue;
	private Thread commandThread;
	boolean controllerNeeded = false;
	LinkedBlockingQueue<String> scheduledReporterResults = new LinkedBlockingQueue<String>();
	
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
	public abstract Object report(String command);
	
	public abstract void scheduleReportersAndRun (ArrayList<String> reporters, int startAtTick, int intervalTicks, int stopAtTick, String goCommand);

	public abstract ArrayList<ArrayList<String>> awaitScheduledReporterResults();

	public abstract ArrayList<ArrayList<String>> getScheduledReporterResults ();
	
	public abstract SearchSpace getParamList(String path);
	
	protected abstract void disposeWorkspace();
}