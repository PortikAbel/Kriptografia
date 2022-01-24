package server;

import service.SocketService;

import javax.net.ssl.SSLServerSocket;
import javax.net.ssl.SSLSocket;
import java.io.*;

public class Server2 {

    static {
        // System.setProperty("javax.net.debug", "all");
        System.setProperty("jdk.tls.client.protocols", "TLSv1.2");
        System.setProperty("https.protocols", "TLSv1.2");
        System.setProperty("javax.net.ssl.trustStore", ".\\resources\\certificates\\faketruststore.jks");
        System.setProperty("javax.net.ssl.trustStorePassword", "changeit");
        System.setProperty("javax.net.ssl.keyStore",  ".\\resources\\certificates\\fakekeystore.jks");
        System.setProperty("javax.net.ssl.keyStorePassword", "changeit");
    }

    public static void main(String[] args) {

        int port = 443;
        try (SSLServerSocket socketListener = SocketService.createServerSocket(port)) {

            while (true) {
                try (SSLSocket socket = (SSLSocket) socketListener.accept();
                     BufferedReader br = new BufferedReader(new FileReader("bnr_home_copy.html"))) {

                    Writer os = new OutputStreamWriter(socket.getOutputStream());

                    System.out.println("received request");

                    os.write("HTTP/1.1 200 OK\r\n");
                    os.write("Content-Type: text/html; charset=utf-8\r\n");
                    os.write("\r\n\r\n");

                    String currentLine;
                    while ((currentLine = br.readLine()) != null) {
                        os.write(currentLine);
                    }
                    os.flush();

                    System.out.println("sent response");
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
