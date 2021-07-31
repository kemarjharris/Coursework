package ca.utoronto.utm.mcs;

import java.io.IOException;

import javax.inject.Inject;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

import org.json.JSONException;
import org.json.JSONObject;

import dagger.Provides;

public class PostApi implements HttpHandler {
	
	@Inject DeleteHandler delete;
	@Inject GetHandler get;
	@Inject PutHandler put;
	

	@Inject PostApi(DeleteHandler delete, GetHandler get, PutHandler put) {
		this.delete = delete;
		this.get = get;
		this.put = put;
	}

	@Override
	public void handle(HttpExchange exchange) throws IOException{
		
		System.out.println(delete);

		HttpResponse r;

		try {
			JSONObject json = JSONExchangeConverter.convert(exchange);
			
			if (exchange.getRequestMethod().equals("GET")) {
				r = get.handleApiMethod(json);
			} else if (exchange.getRequestMethod().equals("PUT")) {
				r = put.handleApiMethod(json);
			} else if (exchange.getRequestMethod().equals("DELETE")) {
				r = delete.handleApiMethod(json);
			} else {
				r = new HttpResponse();
				r.setResponseNumber(405);
			}

			r.send(exchange);
		} catch (JSONException e) {
			e.printStackTrace();
			r = new HttpResponse();
			r.setResponseNumber(400);
			r.send(exchange);

		
		} catch (Exception e) {
			e.printStackTrace();
			r = new HttpResponse();
			r.setResponseNumber(500);
			r.send(exchange);
		}
		
	}

}
