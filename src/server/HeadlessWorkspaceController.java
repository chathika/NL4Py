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
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Phaser;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class HeadlessWorkspaceController extends NetLogoController {
	
	HeadlessWorkspace ws;
	private ArrayBlockingQueue<String> commandQueue;
	private CommandThread commandThread;
	private Object commandThreadLock = new Object();
	boolean controllerNeeded = false;
	LinkedBlockingQueue<ArrayList<String>> scheduledReporterResults = new LinkedBlockingQueue<ArrayList<String>>();
	volatile boolean scheduleDone = true;	
	private Phaser notifier;
	private int phaseTarget = 0;
	private final Integer session = this.hashCode();
	
	//Pool Related
	private ArrayList<ArrayList<String>> poolTasks = null;	
	private ArrayList<String> reporters;
	private Integer startTick;
	private Integer tickInterval;
	private Integer stopTick;
	private String goCommand;   
	private ConcurrentHashMap<String, ArrayList<ArrayList<String>>> poolResultsMap;
	///////

	class CommandThread extends Thread {	
		//private HashMap<String, ArrayList<ArrayList<String>>> poolWorkerResults;
		/**
		* Checks if the queue has been poisoned with the thread stop condition
		* If yes, interrupt and free resources.
		* If no, return the intended command String
		* Blocks on the commandQueue
		*/			
		private String safelyGetNextCommand() throws InterruptedException{
			String nextCommand = commandQueue.take();
			if(nextCommand.equalsIgnoreCase("~stop~")) {
				nextCommand = "";
				controllerNeeded = false;
				Thread.currentThread().interrupt();
			}
			return nextCommand;
		}		
		public CommandThread (){//register phaser for pool 
			//notifier.register();
		}
		@Override
		public void run() {
			controllerNeeded = true;
			String runName = "Unnamed";
			while (controllerNeeded || !Thread.currentThread().interrupted()) {
				try{
					if(poolTasks != null){
						if (!poolTasks.isEmpty()) {
							ArrayList<String> runNameInitStringPair = poolTasks.remove(0);
							runName = runNameInitStringPair.get(0);
							ws.command(runNameInitStringPair.get(1));
							commandQueue.put("~ScheduledReporters~");
							for (String reporter : reporters) {
								commandQueue.put(reporter);
							}
							commandQueue.put("~StartAt~");
							commandQueue.put(Integer.toString( startTick));
							commandQueue.put("~Interval~");
							commandQueue.put(Integer.toString(tickInterval));
							commandQueue.put("~StopAt~");
							commandQueue.put(Integer.toString(stopTick));
							commandQueue.put("~RunReporters~");
							commandQueue.put(goCommand);
						} else {
							// pool work has finished 
							//poolResultsMap.putAll(poolWorkerResults);
							notifier.arriveAndDeregister();
							poolTasks = null;
							ws.dispose();
							return;
						}
					} 
					//get next command out of queue											
					String nextCommand = safelyGetNextCommand();
					if(nextCommand.equalsIgnoreCase("~ScheduledReporters~") ){
						//register a non-pool schedule
						if (poolTasks == null ){
							phaseTarget += 1;
							notifier.register();
						}
						scheduleDone = false;
						//Read in the schedule
						ArrayList<String> reporters = new ArrayList<String>();
						nextCommand = safelyGetNextCommand();
						while (!nextCommand.equalsIgnoreCase("~StartAt~")) {
							reporters.add(nextCommand);
							nextCommand = safelyGetNextCommand();
							if (nextCommand == null ) {nextCommand = "";}
						} 
						int startAtTick = Integer.parseInt(safelyGetNextCommand());
						nextCommand = safelyGetNextCommand();
						int intervalTicks = Integer.parseInt(safelyGetNextCommand());
						nextCommand = safelyGetNextCommand();
						int stopAtTick = Integer.parseInt(safelyGetNextCommand());
						nextCommand = safelyGetNextCommand();
						String goCommand = safelyGetNextCommand();
						//Now execute the schedule
						//Has start time passed?
						int ticksOnModel = ((Double)ws.report("ticks")).intValue();
						if(ticksOnModel <= startAtTick ){
							boolean modelStopped = false;
							if(ticksOnModel < startAtTick) {
								//catch up if necessary
								ws.command("repeat " + Double.toString(startAtTick - ticksOnModel) +" [go]");
							}
							String commandString = "let nl4pyData (list) repeat " + Integer.toString(stopAtTick - startAtTick) +" [ " + goCommand + " let resultsThisTick (list " ; 
							for(String reporter : reporters) {
								commandString = commandString + "( " +reporter + " ) ";
							}
							commandString = commandString + ") set nl4pyData lput resultsThisTick nl4pyData ] ask patch 0 0 [set plabel nl4pyData]";
							ws.command(commandString);						
							scala.collection.Iterator resultsIterator = ((org.nlogo.core.LogoList)ws.report("[plabel] of patch 0 0")).toIterator();
							while(resultsIterator.hasNext()) {
								ArrayList<String> resultsThisTickArray = new ArrayList<String>();
								org.nlogo.core.LogoList resultsThisTick = (org.nlogo.core.LogoList)resultsIterator.next();
								scala.collection.Iterator resultsThisTickIterator = resultsThisTick.toIterator();
								while(resultsThisTickIterator.hasNext()){
									resultsThisTickArray.add(resultsThisTickIterator.next().toString());
								}
								scheduledReporterResults.put(resultsThisTickArray);										
							}
							//ArrayList resultsArray = new ArrayList(((org.nlogo.core.LogoList)ws.report("[plabel] of patch 0 0")).toJava());
							//scheduledReporterResults.put(resultsArray);
							ws.command("ask patch 0 0 [set plabel 0]");
						}
						scheduleDone = true;
						if (poolTasks == null){	
							//deregister non schedule pool	
							notifier.arriveAndDeregister();
						} else {
							// add results to pool results
							ArrayList<ArrayList<String>> results  = new ArrayList<ArrayList<String>>();
							scheduledReporterResults.drainTo(results);
							poolResultsMap.put(runName,results);
						}
					} else {
						if (nextCommand.equalsIgnoreCase("~PoolAttached~")){
							//poolWorkerResults = new HashMap<String, ArrayList<ArrayList<String>>>();
						} else {
							ws.command(nextCommand);
						}
					}
					// If there are no other commands left, the command thread can wait for now.
					/* if (pool == null && commandQueue.size() == 0 ) {
						synchronized(commandThreadLock) {
							commandThreadLock.wait();
						}
					}*/
				} catch (InterruptedException e){
					controllerNeeded = false;
					Thread.currentThread().interrupt();
					break;
				} catch (NullPointerException e){
					if (ws == null) {
						break;
					}
				} catch (Exception e) {
					e.printStackTrace();
					System.out.println(commandQueue);
				} finally {
					scheduleDone = true;
				}
			}
		}
	}
	public HeadlessWorkspaceController(Phaser notifier) {
		//Create new workspace instance
		ws = HeadlessWorkspace.newInstance();
		this.notifier = notifier;
		commandQueue = new ArrayBlockingQueue<String>(100);
		commandThread = new CommandThread();
		commandThread.start();
	}
	
	/**
	 * Create a new workspace
	 * Load a NetLogo model file into the headless workspace
	 * @param path: Path to the .nlogo file to load.
	 */
	public void openModel(String path) {
		try {
			NetLogoVersionCompatibilityResolver.open(ws,path);
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
			ws.halt();
			ws.init();
		} catch (Exception e) {
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
			synchronized(commandQueue){
				commandQueue.put(newCommand);
			}
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
			//Thread.sleep(1);
			report = ws.report(command);
		} catch (Exception e) {
			// in case a run crashes due to a NetLogo side exception, return 0
			report = "NetLogo Exception";//new Double(0.0);
			return report;
			//e.printStackTrace();
		} 
		return report;
	}
	
	public void scheduleReportersAndRun (ArrayList<String> reporters, int startAtTick, int intervalTicks, int stopAtTick, String goCommand){
		try{
			
			synchronized(commandQueue){
				commandQueue.put("~ScheduledReporters~");
				for (String reporter : reporters) {
					commandQueue.put(reporter);
				}
				commandQueue.put("~StartAt~");
				commandQueue.put(Integer.toString(startAtTick));
				commandQueue.put("~Interval~");
				commandQueue.put(Integer.toString(intervalTicks));
				commandQueue.put("~StopAt~");
				commandQueue.put(Integer.toString(stopAtTick));
				commandQueue.put("~RunReporters~");
				commandQueue.put(goCommand);
			}
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	public ArrayList<ArrayList<String>> awaitScheduledReporterResults() {
		ArrayList<ArrayList<String>> results  = null;
		// Change the notifier to point to the one provided by the client
		notifier.awaitAdvance(this.phaseTarget);
		results = getScheduledReporterResults();
		System.out.println(notifier.getPhase());
		return results;
	}
	public ArrayList<ArrayList<String>> getScheduledReporterResults () {
		ArrayList<ArrayList<String>> results  = new ArrayList<ArrayList<String>>();		
		try {	
			if(scheduleDone) {
				synchronized(scheduledReporterResults){
					scheduledReporterResults.drainTo(results);
				}
			} 			
		} catch (Exception e) {
			e.printStackTrace();
		}		
		return results;
	}	
	protected void attachPoolTasks(ArrayList<ArrayList<String>> poolTasks,ArrayList<String> reporters, Integer startTick,Integer tickInterval, Integer stopTick, String goCommand, ConcurrentHashMap<String, ArrayList<ArrayList<String>>> poolResultsMap) {
		this.reporters = reporters;
		this.poolTasks = poolTasks;
		this.startTick = startTick;
		this.tickInterval = tickInterval;
		this.stopTick = stopTick;
		this.goCommand = goCommand;
		this.poolResultsMap = poolResultsMap;
		try{
			synchronized(commandQueue){
				commandQueue.put("~PoolAttached~");
			}
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	public SearchSpace getParamList(String path) {
		String constraintsText = "";
		SearchSpace ss = null;
		try{
		constraintsText = bsearch.nlogolink.Utils.getDefaultConstraintsText(path);
		
		ss = new SearchSpace(java.util.Arrays.asList(constraintsText.split("\n")));
		for(ParameterSpec paramSpec : ss.getParamSpecs()) {
		}
		} catch (NetLogoLinkException e)
		{
			e.printStackTrace();			
		}
		return ss;
	}
	
	protected void disposeWorkspace(){
		this.closeModel();
		
		try{	commandQueue.put("~stop~");
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (Exception e){
			e.printStackTrace();
		}
		controllerNeeded = false;
		try{
			commandThread.interrupt();
		} catch (Exception e){
			e.printStackTrace();
		}
		try{
			ws.dispose();
		} catch (Exception e){
			e.printStackTrace();
		}
		ws = null;
		System.gc();
	}

	public Integer getSession() {
		return this.session;
	}
}