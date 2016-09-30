import py4j.GatewayServer;
import java.io.IOException;
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
