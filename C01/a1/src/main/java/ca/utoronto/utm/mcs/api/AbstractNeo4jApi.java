package ca.utoronto.utm.mcs.api;

import java.io.IOException;
import java.io.OutputStream;

import org.json.JSONException;
import org.json.JSONObject;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

import ca.utoronto.utm.mcs.Neo4jMethodHandler;
import ca.utoronto.utm.mcs.entities.Actor;

// This is basically an abstract class, and the base class for the implementations of all
// the api. I did it like this because 1. every api needs a handler and 2. to use the
// template design pattern. I'll explain the pattern in a bit.
public abstract class AbstractNeo4jApi implements HttpHandler {

	protected Neo4jMethodHandler handler;

	public AbstractNeo4jApi(Neo4jMethodHandler handler) {
		this.handler = handler;
	}

	// Handle is what gets called when we send a request with POST or curl.
	// You probably already knew this.
	// Im not gonna go into detail but if you need more clarification of whats ahppening here,
	// shoot me a text.
	public void handle(HttpExchange r) {
        try {
            
        	String requestMethod = r.getRequestMethod();
        
            if (requestMethod.equals("PUT")) {
                handlePut(r);
            } else if (requestMethod.equals("GET")) {
            	handleGet(r);
            }
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
	
	// Handles GET Requests
	protected void handleGet(HttpExchange r) throws IOException, JSONException 
	{
		// These two lines basically parse the request body and give you an object you can use (duh) 
		String body = Utils.convert(r.getRequestBody());
        JSONObject deserialized = new JSONObject(body);


        int responseNumber = getResponseNumber(deserialized);
        
        // This is where the template pattern kicks in.
        // When this function gets called, it'll execute the overidden version of the method in the
        // child class.
        // Scroll down to the getAction and putAction methods when youre done reading this 
        // function.
		String response = getAction(deserialized);
		
		// Obviously sends the response.
        r.sendResponseHeaders(responseNumber, response.length());
        OutputStream os = r.getResponseBody();
        os.write(response.getBytes());
        os.close();
	}

	// Handles PUT Requests
	protected void handlePut(HttpExchange r) throws IOException, JSONException {
		
		String body = Utils.convert(r.getRequestBody());
        JSONObject deserialized = new JSONObject(body);

		String response = putAction(deserialized);
		
        r.sendResponseHeaders(200, response.length());
        OutputStream os = r.getResponseBody();
        os.write(response.getBytes());
        os.close();
	}
	
	// So, the template design pattern. You use this pattern when an algorithm is the
	// same except for a certain part of it.
	// For the part of of the algorithm thats different, you implement a base method in
	// the parent class, then override part of the algorithm in the child class.
	// When the base method gets called, itll run normally, then use the children's
	// overridden version when when it gets to that point in the algorithm
	// Notice how no matter what we do with an HttpExchange, we always have to
	// deserialize it, and send a response? Thats the part that stays the same.
	// The part of the algorithm thats different is what we actually do with the data.
	// That's what the getAction and putAction methods are for.
	// Take a look at AddActorApi and AddMovieApi. They both implement putAction.
	// Those are the methods that get called when handlePut/handleGet are executing.
	public String getAction(JSONObject deserialized) throws JSONException {
		return "";
	}	
	
    protected String putAction(JSONObject deserialized) throws JSONException 
    {
    	return "";
    }
    
    protected int getResponseNumber(JSONObject deserialized) {
    	return 200;
    }
    // Now that thats done, I'll explain how neo4j nodes work.
    // Open up Actor.java.

}
