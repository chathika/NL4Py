//Originally authored by D Masad
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

public class HeadlessWorkspaceController {
	
	HeadlessWorkspace ws;
	private ArrayBlockingQueue<String> commandQueue;
	private Thread commandThread;
	boolean controllerNeeded = false;
	public HeadlessWorkspaceController() {
		//Create new workspace instance
		ws = HeadlessWorkspace.newInstance();
		commandQueue = new ArrayBlockingQueue<String>(100);
		commandThread = new Thread(new Runnable() {
			@Override
			public void run() {
				System.out.println("command thread started");
				controllerNeeded = true;
				while (controllerNeeded || !Thread.currentThread().interrupted()) {
					//get next command out of queue
					try{
						//System.out.println("taking next command");
						String nextCommand = commandQueue.take();
						if(nextCommand != "~stop~") {
							System.out.println("sending next command");							
							ws.command(nextCommand);
							System.out.println("command done");
						} else {
							controllerNeeded = false;
							Thread.currentThread().interrupt();
						}
					} catch (InterruptedException e){
						System.out.println("Shutting down command thread" + Thread.currentThread().getName());
						controllerNeeded = false;
						Thread.currentThread().interrupt();
						break;
					}
				}
			}
		});
		commandThread.start();
	}

	/**
	 * Create a new workspace
	 * Load a NetLogo model file into the headless workspace
	 * @param path: Path to the .nlogo file to load.
	 */
	public void openModel(String path) {
		
		System.out.println("opening" + path);
		try {
			ws.open(path);
		} catch (IOException e) {
			e.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		} 		
	}
	
	/**
	 * Close the Netlogo file.
	 * @param unique id for this model
	 */
	public void closeModel(){
		try {
			ws.dispose();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Create a new headless instance. 
	 * Use this after closeModel() to instantiate a
	 * new instance of Netlogo. Great for multiple runs!
	 */
	public void refresh(){
		try {
			ws.dispose();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		ws = HeadlessWorkspace.newInstance();
	}
	
	/**
	 * Export a view (the visualization area) to the Java file's working directory.
	 * @param filename: Name used to save the file. Include .png (ex: file.png)
	 */
	public void exportView(String filename){
		try {
			BufferedImage img = ws.exportView();
		    File outputfile = new File(filename);
		    ImageIO.write(img, "png", outputfile);
		} catch (IOException e) {
		    e.printStackTrace();
		}		
	}
	
	/**
	 * Send a command to the open NetLogo model.
	 * @param command: NetLogo command syntax.
	 */
	public void command(String command) {
		try {
			this.scheduleCommand(command);
		} catch (Exception e) {
			e.printStackTrace();
		} 
	}
	private void scheduleCommand(String newCommand) {
		try{
			commandQueue.put(newCommand);
		} catch (InterruptedException e){
			e.printStackTrace();
		}
	}
	/**
	 * Get the value of a variable in the NetLogo model.
	 * @param command: The value to report.
	 * @return Java Object containing return info
	 */
	public Object report(String command) {
		Object report = new Double(0.0);
		try {
			report = ws.report(command);
		} catch (Exception e) {
			// in case a run crashes due to a NetLogo side exception, return 0
			report = new Double(0.0);
			e.printStackTrace();
		} 
		return report;
	}
	
	public SearchSpace getParamList(String path) {
		String constraintsText = "";
		SearchSpace ss = null;
		try{
		constraintsText = bsearch.nlogolink.Utils.getDefaultConstraintsText(path);
		
		ss = new SearchSpace(java.util.Arrays.asList(constraintsText.split("\n")));
		for(ParameterSpec paramSpec : ss.getParamSpecs()) {
			System.out.println(paramSpec.getClass());
		}
		} catch (NetLogoLinkException e)
		{
			e.printStackTrace();			
		}
		return ss;
	}
	
	protected void disposeWorkspace(){
		this.closeModel();
		ws = null;
		try{
			commandQueue.put("~stop~");
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		controllerNeeded = false;
		commandThread.interrupt();
	}
}
