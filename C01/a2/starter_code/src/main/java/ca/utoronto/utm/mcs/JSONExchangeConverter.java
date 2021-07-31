package ca.utoronto.utm.mcs;

import com.sun.net.httpserver.*;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.stream.Collectors;

import org.json.JSONException;
import org.json.JSONObject;

public class JSONExchangeConverter {

    public static JSONObject convert(HttpExchange exchange) throws IOException, JSONException {
 
        BufferedReader br = new BufferedReader(new InputStreamReader(exchange.getRequestBody()));
            String body = br.lines().collect(Collectors.joining(System.lineSeparator()));
            JSONObject json = new JSONObject(body);
            return json;
    }
}