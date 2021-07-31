package ca.utoronto.utm.mcs;

import java.net.URI;
import java.net.URISyntaxException;

import ca.utoronto.utm.mcs.Config;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.sun.net.httpserver.HttpServer;

import javax.inject.Inject;


import dagger.ObjectGraph;

public class App implements Runnable
{
    @Inject HttpServer server;
    @Inject Config config;
    @Inject MongoClient client;
    @Inject PostApi api;

    public void run()
    {	
        /* TODO: Add Working Context Here */
    	
        server.setExecutor(null);
        server.createContext("/api/v1/post", api);
        server.start();
        System.out.printf("Server started on port %d...\n", config.port);
        
        
    }

    public static void main(String[] args) throws URISyntaxException
    {


        //ObjectGraph.create(new ApiMethodHandlerModule()).get(PostApi.class);  
        ObjectGraph objectGraph = ObjectGraph.create(new DaggerModule(new Config()));
        objectGraph.get(PutHandler.class);
        objectGraph.get(DeleteHandler.class);
        objectGraph.get(GetHandler.class);
        objectGraph.get(DatabaseDAO.class);
        objectGraph.get(PostApi.class);
        App app = objectGraph.get(App.class);
        app.run();
    }
}
