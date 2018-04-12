/*
 * Cluster and Cloud Computing Assignment 1 - HPC Data Processing
 * Name: Yasser Aldwyan
 * Student ID: 606486
 * April 2014
 */
import java.io.EOFException;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.concurrent.*;

public class StringSearchMT {
	
	public static final long BLOCK = 1024;
	// processID, num processes, number files,, term
	public static void main(String[] args) throws InterruptedException 
	{
		long startTimer = System.currentTimeMillis();
		
		//Program arguments ----------->>>>>>
		long nodeID = Long.parseLong( args[0].trim() );
		long numOfNodes = Long.parseLong( args[1].trim() );
		long ppn = Long.parseLong( args[2].trim() );		
		String path = args[3].trim();
		String term = args[4].trim();
		//end of arguements
		
		//The order of process on which the read is based
		long processID = ( (nodeID-1) * ppn) + 1;
		//Calculate the number of processes in order to divie the data into parts
		long numOfProcesses = numOfNodes * ppn;
		
		int bound = (int)(ppn * nodeID);;
		
		//Thread pool to run threads
		ExecutorService es = Executors.newCachedThreadPool();
		for(int i=(int)processID; i<=bound; i++)
		   es.submit(new Search(i, numOfProcesses, term, path));
		es.shutdown();
		es.awaitTermination(Long.MAX_VALUE, TimeUnit.SECONDS);
		
    	        //Prints the output
	        System.out.println(Search.matches);	

	}
}

class Search extends Thread
{
	public final long BLOCK = 1024;

	public  static long matches = 0;
	
	public long numOfProcesses = 1;
	public long processID = 1;
	String term = "";
	String path = "";
		
	public Search(long processID, long numOfProcesses, String term, String path)
	{
		this.processID = processID;
		this.numOfProcesses = numOfProcesses;
		this.term = term;
		this.path = path;
	}

	public void run()
	{
		search();
	}
	public long search( )
	{

		long numOfMatches = 0;
		long dataSize = 0, partDataSize = 0;
		long startPos = 0, endPos = 0;
    	RandomAccessFile randomAcc;
    	Matcher matcher;
    	char[] letters;
		long currentPos = 0;
		long nextPos = 0;
		int numOfBytes;
		byte[] buffer;
    	//The term to search for and the string from a file 
    	String str, termRegex;
    	  	
    	try
    	{
	        //read the input string from a file 
    		randomAcc = new RandomAccessFile(path, "rw");
	
			//Get the size of the data from the file
			dataSize = randomAcc.length(); 
			
			//===========START DATA SPLITTER==============
			
			//Calculate the size of partial data should be for each process
			partDataSize = dataSize / numOfProcesses;

			//Calculate the start position for the process to read from the file
			startPos = (processID-1) * partDataSize;
			
			//Makes sure the start position is a white space
			//if not, move forward until a white space found
			if( processID != 1 )
			{
				do
				{
					//Read start position's character
					randomAcc.seek(startPos);
					//Check the character at start position.
					if ( !Character.isWhitespace( (char)randomAcc.readByte() ) )
					{
						startPos++;
					}
					else
					{
						break;
					}
				}
				while(true);
			}
			
			//Calculates the end position for the process to stop reading from the file
			endPos = processID * partDataSize;
			
			//If last process, checks whether there are missing bytes should be read. 
			if( processID == numOfProcesses)
			{
				//if yes, check if there is missing bytes at the end of the data
				if( (dataSize % partDataSize) != 0)
				{
					//Edit the End position of last process, -1 for correct index
					endPos = dataSize-1;
					
				}
			}
			else // The process not last one, then check the end position
			{
				//Makes sure the start position is a white space
				//if not, move forward until a white space found				
				do
				{
					//Read end position's character
					randomAcc.seek(endPos);
					//Check the character at end position.
					if ( !Character.isWhitespace( (char)randomAcc.readByte() ) )
					{
						endPos++;
					}
					else
					{
						break;
					}
				}
				while(true);
			}
   	
			//================End DATA SPLITER===============================
			
			
			//============START SEARCHING FOR A TERM IN A PARTIAL DATA========
			
			currentPos = startPos;
			//Update the term to accept whether upper and lower case letters
	    	letters = term.toCharArray();
	    	termRegex = "";
	   
	    	//Lets the regex accepts small and capital letters
	    	for(int i = 0; i < letters.length; i++ )
	    	{
	    		if( Character.isAlphabetic(letters[i]) )
	    		{
	    			termRegex+= "(" + Character.toUpperCase(letters[i]) 
	    					   + "|" 
	    					   + Character.toLowerCase(letters[i]) 
	    					   + ")";
	    		}
	    		else
	    		{
	    			termRegex += letters[i];
	    		}
	    	}
    	
	    	//Get the regexp of the term
	    	String regexp = "\\W" + termRegex + "\\W";
	    	
	    	Pattern pattern = Pattern.compile(regexp);
        	    	
	        while( currentPos < endPos)
	        {
	        	//Starts reading characters until end position reached
		    	nextPos = currentPos + BLOCK -1;
		    	if( nextPos > endPos )
		    	{
		    		nextPos = endPos;
		    	}
	        	while(nextPos < endPos)
	        	{
	        		//Check the character at next position.
	        		randomAcc.seek(nextPos);
					if ( !Character.isWhitespace( (char)randomAcc.readByte() ) )
					{
						nextPos++;					
					}
					else
					{
						break;
					}
	        	}
	        	
	        	numOfBytes = (int)(nextPos - currentPos);
	        	buffer =  new byte[numOfBytes];
	        	randomAcc.seek(currentPos);
	        	randomAcc.readFully(buffer);
	        	//Updates the current position after the read
	    		currentPos = randomAcc.getFilePointer();


		        for(int i = 0; i < buffer.length;i++)
		        	if( (!Character.isAlphabetic(buffer[i])) && (!Character.isDigit(buffer[i])) && (!Character.isWhitespace(buffer[i])))
		        		buffer[i] = ' ';	
	
	    		//Starts find a term in a block
	    		str = new String(buffer);
			str = " " + str + " ";

	    		matcher = pattern.matcher( str ); 
	        	//Start searching for a given word in the text file       	        
	        	if(matcher.find())       
	        	{        
	        		numOfMatches++;           
	        		while (matcher.find(matcher.end())) //=========>>>>>>> -1 
	        		{
	        			numOfMatches++;
	        		}
	        	}
	        	//Matching process
	        		   
	        }
	        
			//============START SEARCHING FOR A TERM IN A PARTIAL DATA========

	        randomAcc.close();
	    }
        catch (FileNotFoundException e)
        {
        	e.printStackTrace();
        }
    	catch(EOFException e)
    	{
    		System.err.println("End of file exception.");
    		
    	}
        catch( IOException e)
        {
        	System.err.println("IO issue.");
        }     					
		synchronized(this)
		{
			matches+=numOfMatches;
		}
	
    	return numOfMatches;
	}
	
}



