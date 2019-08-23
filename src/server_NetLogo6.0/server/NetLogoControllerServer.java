
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
import java.util.HashMap;
import org.nlogo.headless.HeadlessWorkspace; 
import nl4py.server.HeadlessWorkspaceController;
import nl4py.server.NetLogoAppController;
import nl4py.server.NetLogoController;
import java.util.ArrayList;
import java.util.concurrent.Phaser;

public class NetLogoControllerServer {
	
	ConcurrentHashMap<Integer,NetLogoController> controllerStore;
	Phaser ph;
	static GatewayServer gs;
	long startTime;
	static boolean serverOn = false;
	Thread statusThread;
	public NetLogoControllerServer() {
		controllerStore = new ConcurrentHashMap<Integer,NetLogoController>();
		ph = new Phaser(1);
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
		HeadlessWorkspaceController controller = new HeadlessWorkspaceController(this.ph);
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
		getControllerFromStore(session).command(command);
	}
	/**
	 * Get the value of a variable in the NetLogo model.
	 * @param command: The value to report.
	 * @return Java Object containing return info
	 */
	public Object report(int session, String command) {
		return getControllerFromStore(session).report(command);
	}
	/** Schedules reporters and runs the provided workspaces. This is a nonblocking method and does not wait for the end of the workspace execution.
	 * Results of the reporters can be retrieved through HeadlessWorkspaceColtroller.getScheduledReporterResults(int session).
	 * @param session: session id of HeadlessWorkspaceController to schedule and execute
	 * @param reporters: String array of netlogo reporters to be scheduled
	 * @param startAtTick: Simulation tick to start reporters at
	 * @param intervalTicks: Simulation tick duration between reporter execution (default is to measure at every simulation tick)
	 * @param stopAtTick: Simulation tick to stop reporters at
	 * @param goCommand: String with NetLogo command to execut model
	 */
	public void scheduleReportersAndRun(int session, ArrayList<String> reporters, int startAtTick, int intervalTicks, int stopAtTick, String goCommand){
		getControllerFromStore(session).scheduleReportersAndRun(reporters, startAtTick, intervalTicks, stopAtTick, goCommand, false);
	}
	
	public ArrayList<String> getScheduledReporterResults (int session){
		return getControllerFromStore(session).getScheduledReporterResults();
	}
	/**
	 * Schedules reporters on the NetLogo Headless Workspaces controlled by the HeadlessWorkspaceControllers of the provided session ids,
	 * runs the provided workspaces with the goCommand,
	 * and waits for the simulation results of all executing workspaces and returns an array of the results. This is a blocking method.
	 * @param sessions: array of session ids of HeadlessWorkspaceControllers to run
	 * @param reporters: String array of netlogo reporters to be scheduled
	 * @param startAtTick: Simulation tick to start reporters at
	 * @param intervalTicks: Simulation tick duration between reporter execution (default is to measure at every simulation tick)
	 * @param stopAtTick: Simulation tick to stop reporters at
	 * @param goCommand: String with NetLogo command to execut model
	 * @return: Returns results of all executing workspaces.
	 */
	public HashMap<Integer,ArrayList<String>> runReportersOnWorkspaces (ArrayList<Integer> sessions, ArrayList<String> reporters, int startAtTick, int intervalTicks, int stopAtTick, String goCommand){
		HashMap<Integer, ArrayList<String>> workspacesResults = new HashMap<Integer, ArrayList<String>>();
		for (int session: sessions) {
			getControllerFromStore(session).scheduleReportersAndRun(reporters, startAtTick, intervalTicks, stopAtTick, goCommand, true);
		}
		System.out.println(ph.getRegisteredParties());
		System.out.println(ph.getArrivedParties());
		System.out.println(ph.getPhase());
		System.out.println(ph.getRegisteredParties());
		System.out.println(ph.getArrivedParties());
		ph.arriveAndAwaitAdvance();
		System.out.println(ph.getRegisteredParties());
		System.out.println(ph.getArrivedParties());
		System.out.println(ph.getPhase());
		System.out.println(ph.getRegisteredParties());
		System.out.println(ph.getArrivedParties());
		for (int session: sessions) {
			workspacesResults.put(session,getControllerFromStore(session).getScheduledReporterResults());
		}
		return workspacesResults;
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
	private NetLogoController getControllerFromStore(int session){
		//Get controller from store
		NetLogoController controller = controllerStore.get(session);
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
		System.gc();
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
			//System.out.println("Shutting down Server");
			gs.shutdown(false);
			System.exit(0);
		}
	}	

	/**
	 * Create a new workspace for this request
	 * @return the session id of the model 
	 */
	public int newNetLogoApp(){
		//Create new controller instance
		NetLogoAppController controller = new NetLogoAppController();
		//Add it to controllerStore
		int session = controller.hashCode();
		controllerStore.put(session, controller);
		return session;
	}
}