
//Customized for nl4py by Chathika Gunaratne <chathikagunaratne@gmail.com>
package nl4py.server;

import py4j.GatewayServer;
import java.util.HashMap;
import nl4py.server.HeadlessWorkspaceController;
import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;
import java.net.ServerSocket;
import java.io.IOException;  

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
	
	public HashMap<String, ArrayList<ArrayList<String>>> runPoolOfTasks(String modelName, ArrayList<ArrayList<String>> namesToInitStrings,
						ArrayList<byte[]> reporters, int startTick, int tickInterval, int stopTick, String goCommand,
						int numProcs) {
		if (numProcs > namesToInitStrings.size()) {
			numProcs = namesToInitStrings.size();
		}
		HeadlessWorkspaceCallable[] workspaceTasks = new HeadlessWorkspaceCallable[numProcs]; 
		Thread[] threads = new Thread[numProcs];
		int numTasksPerProcMin = namesToInitStrings.size() / numProcs;
		int numProcsWithExtraTask = namesToInitStrings.size() % numProcs;
		int taskID = 0;
		for (int i = 0; i < numProcs; i++) 
		{ 
			int numTasks = (int)numTasksPerProcMin;
			if (numProcsWithExtraTask > 0 ){
				numTasks = numTasks+1;
				numProcsWithExtraTask--;
			}
			ArrayList<ArrayList<String>> tasks = new ArrayList<ArrayList<String>>(namesToInitStrings.subList(taskID,taskID + numTasks));
			taskID += numTasks;
			
			HeadlessWorkspaceCallable runnable = new HeadlessWorkspaceCallable(modelName, tasks, reporters, 
							startTick, tickInterval, stopTick, goCommand); 
			workspaceTasks[i] = runnable; 
			Thread t = new Thread(workspaceTasks[i]); 
			threads[i]=t;
			t.start(); 
		} 
		for (int i = 0; i < numProcs; i++) 
		{ 
			try{
				threads[i].join();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		HashMap<String, ArrayList<ArrayList<String>>>  allResults = new HashMap<String, ArrayList<ArrayList<String>>>();
		for (int i = 0; i < numProcs; i++) 
		{
			try{
				allResults.putAll((HashMap<String, ArrayList<ArrayList<String>>> )workspaceTasks[i].getResult());
			} catch (Exception ex){
				ex.printStackTrace();
			}
		}
		return allResults;
	}
}


class HeadlessWorkspaceCallable implements Runnable 
{ 
	private String modelName;
    private ArrayList<ArrayList<String>> runNameInitStringPairs;    
    private ArrayList<byte[]> reporters;
    private Integer startTick;
    private Integer tickInterval;
    private Integer stopTick;
    private String goCommand;
	private HashMap<String, ArrayList<ArrayList<String>>> results;

	public HeadlessWorkspaceCallable(String modelName, ArrayList<ArrayList<String>> namesToInitStrings,
						ArrayList<byte[]> reporters, int startTick, int tickInterval, int stopTick, String goCommand) {
		this.modelName = modelName;
		this.runNameInitStringPairs = namesToInitStrings;
		this.reporters = reporters;
		this.startTick = startTick;
		this.tickInterval = tickInterval;
		this.stopTick = stopTick;
		this.goCommand = goCommand;
		this.results = new HashMap<String, ArrayList<ArrayList<String>>>();
	}
	public void run() {		
		GatewayServer gs = new GatewayServer();
		HeadlessWorkspaceController ws = new HeadlessWorkspaceController(gs);
		ws.openModel(modelName);
		for (int i = 0; i<runNameInitStringPairs.size(); i++) {
			ws.command(runNameInitStringPairs.get(i).get(1));
			ArrayList<ArrayList<String>> result = ws.scheduleReportersAndRun(reporters, startTick, tickInterval, stopTick, goCommand);
			results.put(runNameInitStringPairs.get(i).get(1), result);
		}
	} 
	public HashMap<String, ArrayList<ArrayList<String>>> getResult(){
		return this.results;
	}
}