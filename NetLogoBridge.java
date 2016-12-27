import py4j.GatewayServer;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

import org.nlogo.api.CompilerException;
import org.nlogo.api.LogoException;
import org.nlogo.headless.HeadlessWorkspace;

public class NetLogoBridge {
	
	HeadlessWorkspace ws;
	
	public NetLogoBridge() {
		ws = HeadlessWorkspace.newInstance();
	}

	/**
	 * Load a NetLogo model file into the headless workspace.
	 * @param path: Path to the .nlogo file to load.
	 */
	public void openModel(String path) {
		System.out.println("opening" + path);
		try {
			ws.open(path);
		} catch (IOException e) {
			e.printStackTrace();
		} catch (CompilerException e) {
			e.printStackTrace();
		} catch (LogoException e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * Close the Netlogo file.
	 * 
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
		} catch (CompilerException e) {
			e.printStackTrace();
		} catch (LogoException e) {
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
		} catch (CompilerException e) {
			e.printStackTrace();
		} catch (LogoException e) {
			e.printStackTrace();
		}
		return report;
	}
	
	/**
	 * Launch the Gateway Server.
	 */
	public static void main(String[] args) {
		GatewayServer gs = new GatewayServer(new NetLogoBridge());
		gs.start();
		System.out.println("Server running");

	}

}
