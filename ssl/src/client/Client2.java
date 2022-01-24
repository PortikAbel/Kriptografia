package client;

import service.PrintCertInfo;

import javax.net.ssl.SSLHandshakeException;
import javax.net.ssl.SSLSocket;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Reader;
import java.io.Writer;

import static service.SocketService.createSocket;

public class Client2 {

    static {
        // System.setProperty("javax.net.debug", "all");
        System.setProperty("jdk.tls.client.protocols", "TLSv1.2");
        System.setProperty("https.protocols", "TLSv1.2");
        System.setProperty("javax.net.ssl.trustStore", ".\\resources\\certificates\\faketruststore.jks");
        System.setProperty("javax.net.ssl.trustStorePassword", "changeit");
        System.setProperty("javax.net.ssl.keyStore", ".\\resources\\certificates\\fakekeystore.jks");
        System.setProperty("javax.net.ssl.keyStorePassword", "changeit");
    }

    private static final String message =
            """
            GET /Home.aspx HTTP/1.1\r
            Host: bnr.ro\r
            User-Agent: Mozilla/5.0\r
            Accept: text/xml,application/xml,application/xhtml+xml,text/html*/*\r
            Accept-Language: en-us\r
            Accept-Charset: ISO-8859-1,utf-8\r
            Connection: keep-alive\r
            \r
            """;

    public static void main(String[] args) throws Exception {

        try (SSLSocket socket = createSocket("bnr.ro", 443)) {
            Reader in = new InputStreamReader(socket.getInputStream());
            Writer out = new OutputStreamWriter(socket.getOutputStream());

            // send request
            out.write(message);
            out.flush();

            // save resp body
            char[] data = new char[1024];
            int len;
            StringBuilder sb = new StringBuilder();
            while((len = in.read(data)) > 0) {
                sb.append(new String(data, 0, len));
            }
            String response = sb.toString();
            int htmlStartIndex = response.indexOf("<!");
            try (BufferedWriter writer = new BufferedWriter(new FileWriter("bnr_home.html"))) {
                writer.write(response.substring(htmlStartIndex));
            }

            // print cert info
            PrintCertInfo.printCertInfo(socket.getSession().getPeerCertificates()[0]);
        } catch (SSLHandshakeException e) {
            System.out.println("!!!ALERT!!!");
            System.out.println("fake server");
        }
    }
}
