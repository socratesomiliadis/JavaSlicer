/*
 * HelloRunnable.java
 *
 * creates threads using a class implementing Runnable. 
 * 
 */
public class HelloRunnable {

    public static void main(String[] args) {

        /* allocate array of thread objects */
        int numThreads = 20;
        Thread[] threads = new Thread[numThreads];

        /* create and start threads */
        for (int i = 0; i < numThreads; ++i) {
            System.out.println("In main: create and start thread " + i);
            threads[i] = new Thread(new MyRunnable(i, numThreads));
            threads[i].start();
        }

        /* wait for threads to finish */
        for (int i = 0; i < numThreads; ++i) {
            try {
                threads[i].join();
            }
            catch (InterruptedException e) {
                System.err.println("this should not happen");
            }
        }

        System.out.println("In main: threads all done");
    }
}

/* class containing code for each thread to execute */
class MyRunnable implements Runnable {

    /* instance variables */
    private int myID;
    private int totalThreads;

    /* constructor */
    public MyRunnable(int myID, int totalThreads) {
        this.myID = myID;
        this.totalThreads = totalThreads;
    }

    /* thread code */
    public void run() {
        System.out.println("hello from thread " + myID + " out of " + totalThreads);
        System.out.println("thread " + myID + " exits");
    } 

}

