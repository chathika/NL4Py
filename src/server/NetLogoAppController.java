//Authored by Chathika Gunaratne <chathikagunaratne@gmail.com>
package nl4py.server;

import py4j.GatewayServer;

import java.io.IOException;
import bsearch.nlogolink.NetLogoLinkException;
import javax.imageio.ImageIO;
import bsearch.space.*;
import org.nlogo.app.App;
import java.util.ArrayList;
import javax.swing.JFrame;
import nl4py.server.NetLogoVersionCompatibilityResolver;

public class NetLogoAppController extends NetLogoController {

	GatewayServer gs;

	public NetLogoAppController(GatewayServer gs) {
		this.gs = gs;
		App.main(new String[]{});
	}
	
	/**
	 * Create a new workspace
	 * Load a NetLogo model file into the headless workspace
	 * @param path: Path to the .nlogo file to load.
	 */
	public void openModel(String path) {
		NL4PySecutiryManager secManager = new NL4PySecutiryManager();
		System.setSecurityManager(secManager);
		try {
			java.awt.EventQueue.invokeAndWait(
			new Runnable() {
				public void run() {
					try {
						App.app().getLinkParent().setVisible(true);
						App.app().getLinkParent().setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
						NetLogoVersionCompatibilityResolver.open(App.app(),path);
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
		/**try {
			App.app().dispose();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		App.app() = HeadlessWorkspace.newInstance();*/
	}
	
	/**
	 * Export a view (the visualization area) to the Java file's working directory.
	 * @param filename: Name used to save the file. Include .png (ex: file.png)
	 */
	public void exportView(String filename){
		System.out.println("Not Implemented.");
		/*try {
			BufferedImage img = App.app().exportView();
			File outputfile = new File(filename);
		    ImageIO.write(img, "png", outputfile);
		} catch (IOException e) {
		    e.printStackTrace();
		}*/	
	}
	
	/**
	 * Send a command to the open NetLogo model.
	 * @param command: NetLogo command syntax.
	 */
	public void command(String command) {
		try {
			App.app().command(command);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/**
	 * Get the value of a variable in the NetLogo model.
	 * @param reporter: The value to report.
	 * @return Java Object containing return info
	 */	
	public byte[] report(byte[] reporter) {
		Object result = null;
		try {
			result = App.app().report(new String(reporter));
		} catch (Exception e) {
			e.printStackTrace();
			result = e.getMessage();
		}
		return result.toString().getBytes();
	}
	
	public ArrayList<ArrayList<String>> scheduleReportersAndRun (ArrayList<byte[]> reporters, int startAtTick, int intervalTicks, int stopAtTick, String goCommand){
		ArrayList<ArrayList<String>> scheduledReporterResults = new ArrayList<ArrayList<String>> ();//String[(int)((stopAtTick-startAtTick)/intervalTicks)][reporters.size()];
		//Has start time passed?
		int ticksOnModel = ((Double)App.app().report("ticks")).intValue();
		if(ticksOnModel < startAtTick) {
			//catch up if necessary
			App.app().command("repeat " + Double.toString(startAtTick - ticksOnModel) +" [" + goCommand + "]");
		}
		String commandString = "let nl4pyData (list) repeat " + Integer.toString(stopAtTick - ticksOnModel) +" [ " + goCommand + " let resultsThisTick (list " ; 
		for(byte[] reporter : reporters) {
			commandString = commandString + "( " + new String(reporter) + " ) ";
		}
		commandString = commandString + ") set nl4pyData lput resultsThisTick nl4pyData ] ask patch 0 0 [set plabel nl4pyData]";
		App.app().command(commandString);						
		scala.collection.Iterator resultsIterator = ((org.nlogo.core.LogoList)App.app().report("[plabel] of patch 0 0")).toIterator();
		for (int i = 0; i<(int)((stopAtTick-ticksOnModel)/intervalTicks); i++){
			org.nlogo.core.LogoList resultsThisTick = (org.nlogo.core.LogoList)resultsIterator.next();
			scala.collection.Iterator resultsThisTickIterator = resultsThisTick.toIterator();
			ArrayList<String> resultsThisTickArrayList = new ArrayList<String>();
			for (int j = 0; j<reporters.size(); j++){
				resultsThisTickArrayList.add(resultsThisTickIterator.next().toString());
			}
			scheduledReporterResults.add(i,resultsThisTickArrayList);
		}
		return scheduledReporterResults;
	}	
	
	protected void disposeWorkspace(){
		this.closeModel();
		/*try{
			App.app().dispose();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}*/
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
    //throw new SecurityException();
  }

  @Override public void checkPermission(java.security.Permission perm) {
      // Allow other activities by default
  }
  
}