package ca.utoronto.utm.mcs;



import java.io.IOException;
import java.net.InetSocketAddress;
import com.sun.net.httpserver.HttpServer;

import javax.inject.Inject;
import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;

@Module (injects = {
      App.class,
			DatabaseDAO.class,
			GetHandler.class,
			DeleteHandler.class,
      PutHandler.class,
      PostApi.class
			
		}, library = true) //TODO: Add in any new classes here

    class DaggerModule {
    Config config;
    MongoClient client;
    DatabaseDAO dao;

    DaggerModule(Config cfg) {
        config = cfg;
    }

    @Provides
    @Singleton
    PostApi providePostApi() {
      return new PostApi(
          provideDeleteHandler(),
          provideGetHandler(),
          providePutHandler()
        );
    }

    @Provides
    @Singleton
    MongoClient provideMongoClient() {
      if (this.client == null) client = MongoClients.create();
    	return client;
    }

    @Provides
    @Singleton
    DatabaseDAO provideDatabaseDAO() {
      if (dao == null) dao = new DatabaseDAO(provideMongoClient());
      return dao;
    }
    
    @Provides 
    @Singleton
    HttpServer provideHttpServer() {
        /* TODO: Fill in this function */
        try {
			return HttpServer.create(new InetSocketAddress(config.ip, config.port), 0);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
    }
  }

    @Provides
    public GetHandler provideGetHandler() {
      return new GetHandler(provideDatabaseDAO());
      
    }
    
    @Provides
    public PutHandler providePutHandler() {
      return new PutHandler(provideDatabaseDAO());
    }
    
    @Provides
    public DeleteHandler provideDeleteHandler() {
      return new DeleteHandler(provideDatabaseDAO());
    }
}
