//Workspace controller pool developed by Chathika Gunaratne <chathikagunaratne@gmail.com>
package nl4py.server;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.HashMap;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Phaser;
import java.util.Iterator;
import java.util.Map.Entry;
import java.lang.Math;
import nl4py.server.HeadlessWorkspaceController;

public class HeadlessWorkspaceControllerPool {
    private HashSet<HeadlessWorkspaceController> allWorkers;
    
    private ConcurrentHashMap<String, byte[][][]> resultsMap;
    private Phaser notifier;

    private Integer countProcessors;

    private String modelName;
    private ArrayList<ArrayList<ArrayList<String>>> runNameInitStringPairs;    
    private ArrayList<String> reporters;
    private Integer startTick;
    private Integer tickInterval;
    private Integer stopTick;
    private String goCommand;   


    
    public HeadlessWorkspaceControllerPool(String modelName, Integer processors, ArrayList<ArrayList<ArrayList<String>>> namesToInitStringsChunks, ArrayList<String> reporters, int startTick, int tickInterval, int stopTick, String goCommand){
        this.modelName = modelName;
        allWorkers = new HashSet<HeadlessWorkspaceController>();
        resultsMap = new ConcurrentHashMap<String, byte[][][]>(); //run name -> results
        notifier = new Phaser(1);
        runNameInitStringPairs = new ArrayList<ArrayList<ArrayList<String>>>(namesToInitStringsChunks);
        this.reporters = reporters;
        this.startTick = startTick;
        this.tickInterval = tickInterval;
        this.stopTick = stopTick;
        this.goCommand = goCommand;
        this.countProcessors = processors;
        if (countProcessors == -1) {
            this.countProcessors = Runtime.getRuntime().availableProcessors();
        }
        if (namesToInitStringsChunks.size() < countProcessors){
            this.countProcessors = namesToInitStringsChunks.size();
        }
    }
    public HashMap<String, byte[][][]> run() {
        int countWorkspacesStarted = 0;

        while(countWorkspacesStarted != countProcessors){
            HeadlessWorkspaceController ws = new HeadlessWorkspaceController(notifier);
            ws.openModel(modelName);
            allWorkers.add(ws);
            countWorkspacesStarted += 1;             
        }
        Iterator<HeadlessWorkspaceController> wsitr = allWorkers.iterator();
        int i = 0;
        while(wsitr.hasNext()){
            HeadlessWorkspaceController ws = wsitr.next();
            ArrayList<ArrayList<String>> tasksSubList = new ArrayList<ArrayList<String>>(runNameInitStringPairs.get(i));
            ws.attachPoolTasks(tasksSubList,this.reporters, this.startTick,this.tickInterval,this.stopTick,this.goCommand,this.resultsMap);
            i += 1;
        }
        notifier.arriveAndAwaitAdvance();
        allWorkers.clear();
        return new HashMap<String, byte[][][]>(resultsMap);
    }
}