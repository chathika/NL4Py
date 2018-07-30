//Authored by Chathika Gunaratne <chathikagunaratne@gmail.com>
package nl4py.server;

import py4j.GatewayServer;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import bsearch.nlogolink.NetLogoLinkException;
import javax.imageio.ImageIO;
import bsearch.space.*;
import java.util.HashMap;
import org.nlogo.app.App;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.ArrayList;
import java.util.List;
import javax.swing.JFrame;
public class NetLogoAppController extends NetLogoController {

	private ArrayBlockingQueue<String> commandQueue;
	private Thread commandThread;
	boolean controllerNeeded = false;
	LinkedBlockingQueue<String> scheduledReporterResults = new LinkedBlockingQueue<String>();
	
	public NetLogoAppController() {
		
		App.main(new String[]{});
		commandQueue = new ArrayBlockingQueue<String>(100);
		commandThread = new Thread(new Runnable() {
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
			@Override
			public void run() {
				//System.out.println("command thread started");
				controllerNeeded = true;
				while (controllerNeeded || !Thread.currentThread().interrupted()) {
					//get next command out of queue
					try{
						//System.out.println("taking next command");
						String nextCommand = safelyGetNextCommand();
						if(nextCommand.equalsIgnoreCase("~ScheduledReporters~")){
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
							int ticksAtStart = ((Double)App.app().report("ticks")).intValue();
							if(ticksAtStart <= startAtTick ){
								int tickCounter = ticksAtStart;
								while (controllerNeeded && (tickCounter < stopAtTick || stopAtTick < 0)) {
									//tick the interval
									/*for (int i = 0; i < intervalTicks; i ++ ){
										//go
										App.app.command(goCommand);
										//increment counter
										tickCounter++;
									}*/
									App.app().command("repeat " + Integer.toString(intervalTicks) +" [" + goCommand + "]");
									tickCounter = tickCounter + intervalTicks;
									//run reporters
									ArrayList<String> reporterResults = new ArrayList<String>();
									try{
										for(String reporter : reporters) {
											//record results
											String reporterResult = App.app().report(reporter).toString();
											reporterResults.add(reporterResult);
										}
									} catch (org.nlogo.nvm.RuntimePrimitiveException e) {
										//This can throw a netlogo exception if the model is done running due to custom stop condition
										continue;
									}
									for(String resultI : reporterResults) {
										scheduledReporterResults.put(resultI);
									}
								}
							}
						} else {
							//System.out.println("sending next command");
							App.app().command(nextCommand);
							//System.out.println("command done");
						}	
						Thread.sleep(10);
					} catch (InterruptedException e){
						//System.out.println("Shutting down command thread" + Thread.currentThread().getName());
						controllerNeeded = false;
						Thread.currentThread().interrupt();
						break;
					} catch (NullPointerException e){
						if (App.app() == null) {
							break;
						}
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
		
		NL4PySecutiryManager secManager = new NL4PySecutiryManager();
		System.setSecurityManager(secManager);

		
		
		//System.out.println("opening" + path);
		try {
			java.awt.EventQueue.invokeAndWait(
			new Runnable() {
				public void run() {
					try {
						App.app().getLinkParent().setVisible(true);
						App.app().getLinkParent().setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
						App.app().open(path);					
					}
					catch(java.io.IOException ex) {
						System.out.println("You can only open one model at a time in GUI mode");
					}
					catch (Exception e) {
						e.printStackTrace();
					}
				}
			});
		} catch (SecurityException e) {
		
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
			App.app().getLinkParent().setVisible(false);
			//App.app().workspace.dispose();
		} catch (SecurityException e) {
			e.printStackTrace();
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
		//try {
		//	App.app().dispose();
		//} catch (InterruptedException e) {
		//	e.printStackTrace();
		//}
		//App.app() = HeadlessWorkspace.newInstance();
	}
	
	/**
	 * Export a view (the visualization area) to the Java file's working directory.
	 * @param filename: Name used to save the file. Include .png (ex: file.png)
	 */
	public void exportView(String filename){
		//try {
		//	BufferedImage img = App.app().exportView();
		//    File outputfile = new File(filename);
		//	ImageIO.write(img, "png", outputfile);
		//} catch (IOException e) {
		//    e.printStackTrace();
		//}		
		//Not Yet Implmeneted
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
			Thread.sleep(1);
			report = App.app().report(command);
		} catch (Exception e) {
			// in case a run crashes due to a NetLogo side exception, return 0
			report = new Double(0.0);
			//e.printStackTrace();
		} 
		return report;
	}
	
	public void scheduleReportersAndRun (String reporters[], int startAtTick, int intervalTicks, int stopAtTick, String goCommand){
		
		try{
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
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	public ArrayList<String> getScheduledReporterResults () {
		ArrayList<String> results  = new ArrayList<String>();
		try {
			scheduledReporterResults.drainTo(results);
		} catch (Exception e) {
			e.printStackTrace();
		}
		return results;
	}	
	
	
	protected void disposeWorkspace(){
		this.closeModel();
		//App.app() = null;
		try{
			commandQueue.put("~stop~");
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		controllerNeeded = false;
		commandThread.interrupt();
		System.gc();
	}
	
	public SearchSpace getParamList(String path) {
		String constraintsText = "";
		SearchSpace ss = null;
		try{
		constraintsText = bsearch.nlogolink.Utils.getDefaultConstraintsText(path);
		
		ss = new SearchSpace(java.util.Arrays.asList(constraintsText.split("\n")));
		for(ParameterSpec paramSpec : ss.getParamSpecs()) {
			//System.out.println(paramSpec.getClass());
		}
		} catch (NetLogoLinkException e)
		{
			e.printStackTrace();			
		}
		return ss;
	}
}

class NL4PySecutiryManager extends SecurityManager {
  @Override public void checkExit(int status) {
    throw new SecurityException();
  }

  @Override public void checkPermission(java.security.Permission perm) {
      // Allow other activities by default
  }
}