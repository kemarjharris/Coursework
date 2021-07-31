package ca.utoronto.utm.mcs;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.util.HashMap;
import java.util.Map;

import org.neo4j.driver.v1.AuthTokens;
import org.neo4j.driver.v1.Driver;
import org.neo4j.driver.v1.GraphDatabase;
import org.neo4j.driver.v1.Session;
import org.neo4j.driver.v1.Value;
import org.neo4j.driver.v1.Values;

import com.sun.net.httpserver.HttpServer;

import ca.utoronto.utm.mcs.api.AddActorApi;
import ca.utoronto.utm.mcs.api.AddMovieApi;
import ca.utoronto.utm.mcs.api.AddRelationshipApi;
import ca.utoronto.utm.mcs.api.ComputeBaconNumberApi;
import ca.utoronto.utm.mcs.api.ComputeBaconPathApi;
import ca.utoronto.utm.mcs.api.GetActorApi;
import ca.utoronto.utm.mcs.api.GetMovieApi;
import ca.utoronto.utm.mcs.api.HasRelationshipApi;
public class App 
{
	
    static int PORT = 8080;
    public static void main(String[] args) throws IOException
    {
    	// This driver is basically what lets us connect to the neo4j database.
    	// we assume were connected on port 7687, and we have to sign in too.
    	// the auth tokens are basically the username and password. This should work for you, but
    	// if not try changing "secret" to "neo4j".
    	// You also have to already have the neo4j server started. to do this open up a command
    	// line and hit that mf neo4j console
    	Driver driver = GraphDatabase.driver("bolt://localhost:7687", AuthTokens.basic("neo4j", "secret"));
    	
    	// The neo4j method handler is by me. It's basically an access point to the neo4jdatabase.
    	// Anytime I interact with the database, I use this handler.
    	// I did the architecture this way to decouple the rest api and the neo4j database access.
    	Neo4jMethodHandler neo4jMethodHandler = new Neo4jMethodHandler(driver);
    	
    	// This creates the server (Obviously). This is where were sending and receiving things.
        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", PORT), 0);
        
        // So, the way I implemented this was, each class handles one api (considering we
        // didnt get taught how to do it any other way). I created all these api classes
        // manually. To add new api you'll have to do the same thing.
        // Also, note how I gave every api a handler? This is called dependency injection.
        // If you need an explanation on why I used dependency injection, text me and ill explain.
        server.createContext("/api/v1/addActor", new AddActorApi(neo4jMethodHandler));
        server.createContext("/api/v1/addMovie", new AddMovieApi(neo4jMethodHandler));
        server.createContext("/api/v1/addRelationship", new AddRelationshipApi(neo4jMethodHandler));
        server.createContext("/api/v1/getActor", new GetActorApi(neo4jMethodHandler));
        server.createContext("/api/v1/getMovie", new GetMovieApi(neo4jMethodHandler));
        server.createContext("/api/v1/hasRelationship", new HasRelationshipApi(neo4jMethodHandler));
        server.createContext("/api/v1/computeBaconNumber", new ComputeBaconNumberApi(neo4jMethodHandler));
        server.createContext("/api/v1/computeBaconPath", new ComputeBaconPathApi(neo4jMethodHandler));
        
        server.start();
        System.out.printf("Server started on port %d...\n", PORT);
        
        // Next up, I'll explain the REST api and how i did the architecture. I'm assuming you
        // understand POST, PUT, and GET, so I won't go into detail.
        // Open up AbstractNeo4jApi for the next step.
    }
}
