//Originally authored by D Masad
//Customized for EMD by Chathika Gunaratne <chathikagunaratne@gmail.com>
package emd.server;

import py4j.GatewayServer;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import bsearch.nlogolink.NetLogoLinkException;
import javax.imageio.ImageIO;
import bsearch.space.*;
import java.util.HashMap;
import org.nlogo.headless.HeadlessWorkspace; 


public class HeadlessWorkspaceController {
	
	HeadlessWorkspace ws;
	
	public HeadlessWorkspaceController() {
		ws = HeadlessWorkspace.newInstance();
	}

	/**
	 * Create a new workspace
	 * Load a NetLogo model file into the headless workspace
	 * @param path: Path to the .nlogo file to load.
	 */
	public void openModel(String path) {
		//Create new workspace instance
		ws = HeadlessWorkspace.newInstance();
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
	 * @param command: The value to report.
	 * @return Floating point number
	 */
	public Double report(String command) {
		double report = 0.0;
		try {
			report = (Double)ws.report(command);
		} catch (Exception e) {
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
}
