//Workspace controller pool developed by Chathika Gunaratne <chathikagunaratne@gmail.com>
package nl4py.server;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.HashMap;
import nl4py.server.HeadlessWorkspaceController;

public class HeadlessWorkspaceControllerPool {
    private HashMap<Integer,HeadlessWorkspaceController> allWorkers;
    private HashSet<HeadlessWorkspaceController> freeWorkers;
    private HashSet<HeadlessWorkspaceController> activeWorkers;
    private HashSet<HeadlessWorkspaceController> finishedWorkers;
    private HashMap<String, ArrayList<ArrayList<String>>> resultsMap;
    private ArrayList<Integer> notifier;
    private Integer countRunsDone;
    private Integer countRunsRequired;
    private String modelName;
    public HeadlessWorkspaceControllerPool(String modelName, Integer runsRequired, Integer processors){
        this.modelName = modelName;
        this.countRunsDone = 0;
        this.countRunsRequired = runsRequired;
        allWorkers = new HashMap<Integer,HeadlessWorkspaceController>();
        freeWorkers = new HashSet<HeadlessWorkspaceController>();
        activeWorkers = new HashSet<HeadlessWorkspaceController>();
        finishedWorkers = new HashSet<HeadlessWorkspaceController>();
        resultsMap = new HashMap<String, ArrayList<ArrayList<String>>>(); //run name -> results
        notifier = new ArrayList<Integer>();
        if (processors == -1) {
            processors = Runtime.getRuntime().availableProcessors();
        }
        if (runsRequired < processors){
            processors = runsRequired;
        }
        for (int i=0;i < processors; i++){
            HeadlessWorkspaceController ws = new HeadlessWorkspaceController(notifier);
            ws.openModel(modelName);
            allWorkers.put(ws.getSession(),ws);
            freeWorkers.add(ws);
        }
    }
    public HeadlessWorkspaceController getFreeWorkspace() {
        HeadlessWorkspaceController freeWorker = null;
        // If there aren't any known free workers.. 
        if (this.freeWorkers.isEmpty()) {
            // First check if any active workers have empty command queues
            for (HeadlessWorkspaceController inspectedWorker: ((HashSet<HeadlessWorkspaceController>)activeWorkers.clone())) {
                // If an active worker's command queue is empty handle them
                if (inspectedWorker.isFree()) {
                    // move the worker to finished set for result collection
                    this.activeWorkers.remove(inspectedWorker);
                    this.finishedWorkers.add(inspectedWorker);
                }
            }
            // If there still aren't any free workers...
            if (this.freeWorkers.isEmpty()) {
                // Pretty sure no workers have finished. So better wait till one of them notifies the pool
                try{
                    synchronized(this.notifier) {
                        notifier.wait();
                        // The notifying worker will have specified their session in the notifier
                        for (Integer workerSession: notifier) {
                            HeadlessWorkspaceController notifyingWorker = allWorkers.get(workerSession);
                            //processFinishedWorker(notifyingWorker); 
                            // move the worker to done set for result collection
                            this.activeWorkers.remove(notifyingWorker);
                            this.finishedWorkers.add(notifyingWorker);
                        }                        
                        notifier.clear();
                    // Ok. A worker finished
                    }
                } catch (InterruptedException e) {
                        e.printStackTrace();
                }
            }
            System.out.println(this.finishedWorkers.size() + " workers have finished and are waiting result collection.");
        }
        // Now that we know which workers are done, process them, and then move them to the free set.
        for (HeadlessWorkspaceController finishedWorker: ((HashSet<HeadlessWorkspaceController>)finishedWorkers.clone())) {
            // Grab the worker's results
            ArrayList<ArrayList<String>> results = finishedWorker.getScheduledReporterResults();
            // Add their results to the result map.
            this.resultsMap.put(finishedWorker.getRunName(),results);
            // Move the finished worker to free workers
            this.finishedWorkers.remove(finishedWorker);
            this.freeWorkers.add(finishedWorker);
            //Increment counter
            this.countRunsDone += 1;
        }
        // There are known free workers so provide one of them first
        System.out.println("Free workers available: " + Integer.toString(this.freeWorkers.size()));
        freeWorker = this.freeWorkers.iterator().next();
        freeWorkers.remove(freeWorker);
        activeWorkers.add(freeWorker);
        return freeWorker;
    }
    public HashMap<String,ArrayList<ArrayList<String>>> awaitResults() {
        System.out.print("Waiting results...");
        while (this.countRunsDone < this.countRunsRequired){
            //System.out.print("results...");
            HeadlessWorkspaceController ws = getFreeWorkspace();
            this.freeWorkers.remove(ws);
            this.activeWorkers.remove(ws);
            ws.disposeWorkspace();
            System.out.println("Runs done: " + Integer.toString(this.countRunsDone));
        }
        return this.resultsMap;
    }
}