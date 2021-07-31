package ca.utoronto.utm.mcs;
import java.io.IOException;

import com.sun.net.httpserver.HttpExchange;

import org.json.JSONException;
import org.json.JSONObject;

public interface ApiMethodHandler {
	
	public HttpResponse handleApiMethod(JSONObject exchange) throws IOException, JSONException;

}
