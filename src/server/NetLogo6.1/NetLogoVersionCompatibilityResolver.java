package nl4py.server;

import org.nlogo.app.App;
import org.nlogo.headless.HeadlessWorkspace; 
import java.io.IOException;

public class NetLogoVersionCompatibilityResolver {	
    public static void open(HeadlessWorkspace ws,String path) throws IOException {
        ws.open(path,false);
    }
    public static void open(App ws,String path) throws IOException {
        App.app().open(path,false);
    }
}
