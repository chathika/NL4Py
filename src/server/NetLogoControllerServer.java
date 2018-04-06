
//Customized for EMD by Chathika Gunaratne <chathikagunaratne@gmail.com>
package emd.server;
import py4j.GatewayServer;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import bsearch.nlogolink.NetLogoLinkException;
import javax.imageio.ImageIO;
import bsearch.space.*;
import java.util.concurrent.ConcurrentHashMap;
import org.nlogo.headless.HeadlessWorkspace; 
import emd.server.HeadlessWorkspaceController;

public class NetLogoControllerServer {
	
	ConcurrentHashMap<Integer,HeadlessWorkspaceController> controllerStore;
	
	static GatewayServer gs;
	long startTime;
	
	public NetLogoControllerServer() {
		controllerStore = new ConcurrentHashMap<Integer,HeadlessWorkspaceController>();
		startTime = System.currentTimeMillis();
		
		//Start monitor thread
		Thread statusThread = new Thread(new Runnable() {
			@Override
			public void run() {
				while(true){
					try{
						Thread.sleep(20000);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
					System.out.println("Status checking...");
					statusCheck();
				}
			}
		});		
		statusThread.start();
	}
	/**
	 * Launch the Gateway Server.
	 */
	public static void main(String[] args) {
		gs = new GatewayServer(new NetLogoControllerServer());
		gs.start();
		System.out.println("Server running");
	}
	/** 
	* Shutdown GatewayServer
	**/
	public void shutdownServer(){
		System.out.println("Shutting Down Server");
		gs.shutdown();
	}
	
	
	//Below functions take the session id and call the 
	//requested method on the corresponding controller
	/**
	 * Create a new workspace for this request
	 * Load a NetLogo model file into the headless workspace
	 * Return a unique session id for this request
	 * @param path: Path to the .nlogo file to load.
	 * @return the session id of the model 
	 */
	public int openModel(String path) {
		//Create new controller instance
		HeadlessWorkspaceController controller = new HeadlessWorkspaceController();
		//Add it to controllerStore
		int session = controller.hashCode();
		controllerStore.put(session, controller);
		
		controller.openModel(path);
		return session;
	}
	
	/**
	 * Remove the controller and initiate close sequence
	 * @param unique id for this model
	 */
	public void closeModel(int session){
		getControllerFromStore(session).closeModel();
		removeControllerFromStore(session);
	}
	
	/**
	 * Create a new headless instance. 
	 * Use this after closeModel() to instantiate a
	 * new instance of Netlogo. Great for multiple runs!
	 */
	public void refresh(int session){
		getControllerFromStore(session).refresh();
	}
	
	/**
	 * Export a view (the visualization area) to the Java file's working directory.
	 * @param filename: Name used to save the file. Include .png (ex: file.png)
	 */
	public void exportView(int session, String filename){
		getControllerFromStore(session).exportView(filename);
	}
	
	/**
	 * Send a command to the open NetLogo model.
	 * @param command: NetLogo command syntax.
	 */
	public void command(int session, String command) {
		getControllerFromStore(session).command(command);
	}
	/**
	 * Get the value of a variable in the NetLogo model.
	 * @param command: The value to report.
	 * @return Floating point number
	 */
	public Double report(int session, String command) {
		return getControllerFromStore(session).report(command);
	}
	
	public SearchSpace getParamList(int session, String path) {
		return getControllerFromStore(session).getParamList(path);
	}
	/////////////////////////////////////////////////////////////////////
	/**
	 * Internal method to retrieve workspace from store using session id
	 * @param session id to get
	 * @return NetLogo HeadlessWorkspace
	 */
	private HeadlessWorkspaceController getControllerFromStore(int session){
		//Get controller from store
		HeadlessWorkspaceController controller = controllerStore.get(session);
		//Check if null throw an exception
		if (controller == null) {
			throw new NullPointerException("No NetLogo HeadlessWorkspace exists for that session id");
		}
		return controller;
	}
	/** 
	 * Internal method to remove the controller from the store
	 * @param session id to get
	 */
	private void removeControllerFromStore(int session){
		controllerStore.remove(session);
	}
	
	/**
	 * This is run by a monitor thread that regularly reports the status
	 * of the controllerStore
	 */
	private void statusCheck(){
		
		System.out.println("This server has been up for " + ( System.currentTimeMillis() - startTime ) + " milliseconds. " ); 
		System.out.println("There are currently " + controllerStore.size() + " NetLogo workspaces on this server");
	}	
}
