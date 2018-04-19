
//Customized for nl4py by Chathika Gunaratne <chathikagunaratne@gmail.com>
package nl4py.server;
import py4j.GatewayServer;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import bsearch.nlogolink.NetLogoLinkException;
import javax.imageio.ImageIO;
import bsearch.space.*;
import java.util.concurrent.ConcurrentHashMap;
import org.nlogo.headless.HeadlessWorkspace; 
import nl4py.server.HeadlessWorkspaceController;
import java.util.List;

public class NetLogoControllerServer {
	
	ConcurrentHashMap<Integer,HeadlessWorkspaceController> controllerStore;
	
	static GatewayServer gs;
	long startTime;
	static boolean serverOn = false;
	Thread statusThread;
	public NetLogoControllerServer() {
		controllerStore = new ConcurrentHashMap<Integer,HeadlessWorkspaceController>();
		startTime = System.currentTimeMillis();
		//System.out.println("Start");
		//Start monitor thread
		statusThread = new Thread(new Runnable() {
			@Override
			public void run() {
				while(!Thread.interrupted()){
					try{
						Thread.sleep(100);
					} catch (InterruptedException e) {
						//e.printStackTrace();
						Thread.currentThread().interrupt();
					}
					//System.out.println("Status checking...");
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
		try {
			NetLogoControllerServer ncs = new NetLogoControllerServer();
			gs = new GatewayServer(ncs);
			serverOn = true;
			gs.start();
			//diagnose
			//String model_path = System.getenv("NETLOGO_APP") + "/models/Sample Models/Earth Science/Fire.nlogo";
			//int s = ncs.newHeadlessWorkspaceController();
			//ncs.openModel(s,model_path);
			//ncs.closeModel(s);
			//ncs.removeControllerFromStore(s);
		} catch (Exception e){
			System.out.println("NETLOGO_APP not set right!");
			e.printStackTrace();
			System.exit(1);
		}
		//System.out.println("Server running");
	}
	/** 
	* Shutdown GatewayServer
	**/
	public void shutdownServer(){
		gs.shutdown(true);
		serverOn = false;
		statusThread.interrupt();
	}
	/**
	 * Create a new workspace for this request
	 * @return the session id of the model 
	 */
	public int newHeadlessWorkspaceController(){
		//Create new controller instance
		HeadlessWorkspaceController controller = new HeadlessWorkspaceController();
		//Add it to controllerStore
		int session = controller.hashCode();
		controllerStore.put(session, controller);
		return session;
	}
	//Below functions take the session id and call the 
	//requested method on the corresponding controller
	/**
	 * Load a NetLogo model file into the headless workspace
	 * Return a unique session id for this request
	 * @param path: Path to the .nlogo file to load.
	 * 
	 */
	public void openModel(int session, String path) {
		controllerStore.get(session).openModel(path);
	}
	
	/**
	 * Remove the controller and initiate close sequence
	 * @param unique id for this model
	 */
	public void closeModel(int session){
		getControllerFromStore(session).closeModel();
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
		HeadlessWorkspaceController workSpaceController = getControllerFromStore(session);	
		workSpaceController.command(command);
	}
	/**
	 * Get the value of a variable in the NetLogo model.
	 * @param command: The value to report.
	 * @return Java Object containing return info
	 */
	public Object report(int session, String command) {
		return getControllerFromStore(session).report(command);
	}
	public void scheduleReportersAndRun(int session, String reporters[], int startAtTick, int intervalTicks, int stopAtTick, String goCommand){
		getControllerFromStore(session).scheduleReportersAndRun(reporters, startAtTick, intervalTicks, stopAtTick, goCommand);
	}
	
	public List<String> getScheduledReporterResults (int session){
		return getControllerFromStore(session).getScheduledReporterResults();
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
	public void removeControllerFromStore(int session){
		controllerStore.get(session).closeModel();
		controllerStore.get(session).disposeWorkspace();
		controllerStore.remove(session);
	}
	
	/**
	 * This is run by a monitor thread that regularly reports the status
	 * of the controllerStore
	 */
	private void statusCheck(){
		
		//System.out.println("This server has been up for " + ( System.currentTimeMillis() - startTime ) + " milliseconds. " ); 
		//System.out.println("There are currently " + controllerStore.size() + " NetLogo workspaces on this server");
		
		if(!serverOn) {
			GatewayServer.turnLoggingOff();
			System.out.println("Shutting down Server");
			gs.shutdown(false);
			System.exit(0);
		}
	}	
}
