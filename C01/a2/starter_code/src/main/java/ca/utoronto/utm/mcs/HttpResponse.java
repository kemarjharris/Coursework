package ca.utoronto.utm.mcs;

import com.sun.net.httpserver.HttpExchange;
import java.io.IOException;
import java.io.OutputStream;


public class HttpResponse {


	private int responseNumber = -1;
	private String responseBody = "";
	
	public void setResponseNumber(int responseNumber) {
		this.responseNumber = responseNumber;
	}
	
	public void setResponseBody(String responseBody) {
		this.responseBody = responseBody;
	}
	
	public void send(HttpExchange r) throws IOException {
		if (responseNumber < 0) {
			throw new IllegalArgumentException("Response number not set");
		} 
		
		r.sendResponseHeaders(responseNumber, responseBody.length());
        OutputStream os = r.getResponseBody();
        os.write(responseBody.getBytes());
        os.close();
	}
}
