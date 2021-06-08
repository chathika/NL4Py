//NL4Py by Chathika Gunaratne <chathikagunaratne@gmail.com>
package nl4py.server;

import py4j.GatewayServer;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import java.io.IOException;
import bsearch.nlogolink.NetLogoLinkException;
import bsearch.space.*;
import org.nlogo.headless.HeadlessWorkspace;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Arrays;

public class HeadlessWorkspaceController extends NetLogoController {
	
	GatewayServer gs;
	HeadlessWorkspace ws;
	
	public HeadlessWorkspaceController(GatewayServer gs) {
		this.gs = gs;
		//Create new workspace instance
		ws = HeadlessWorkspace.newInstance();
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
			ws.command(command);
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
			result = ws.report(new String(reporter));
		} catch (Exception e) {
			e.printStackTrace();
			result = e.getMessage();
		}
		return result.toString().getBytes();
	}
	
	public ArrayList<ArrayList<String>> scheduleReportersAndRun (ArrayList<byte[]> reporters, int startAtTick, int intervalTicks, int stopAtTick, String goCommand){
		ArrayList<ArrayList<String>> scheduledReporterResults = new ArrayList<ArrayList<String>> ();//String[(int)((stopAtTick-startAtTick)/intervalTicks)][reporters.size()];
		//Has start time passed?
		int ticksOnModel = ((Double)ws.report("ticks")).intValue();
		if(ticksOnModel < startAtTick) {
			//catch up if necessary
			ws.command("repeat " + Double.toString(startAtTick - ticksOnModel) +" [" + goCommand + "]");
		}
		String commandString = "let nl4pyData (list) repeat " + Integer.toString(stopAtTick - ticksOnModel) +" [ " + goCommand + " let resultsThisTick (list " ; 
		for(byte[] reporter : reporters) {
			commandString = commandString + "( " + new String(reporter) + " ) ";
		}
		commandString = commandString + ") set nl4pyData lput resultsThisTick nl4pyData ] ask patch 0 0 [set plabel nl4pyData]";
		ws.command(commandString);						
		scala.collection.Iterator resultsIterator = ((org.nlogo.core.LogoList)ws.report("[plabel] of patch 0 0")).toIterator();
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
	
	public void disposeWorkspace(){
		this.closeModel();
		try{
			ws.dispose();
		} catch (Exception e){
			e.printStackTrace();
		}
		ws = null;
		gs.shutdown();
		System.gc();
	}
}