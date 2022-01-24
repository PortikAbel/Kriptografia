package client;

import service.PrintCertInfo;
import service.SocketService;

import javax.net.ssl.SSLSocket;
import java.io.*;

public class Client1 {

    static {
        // System.setProperty("javax.net.debug", "all");
        System.setProperty("jdk.tls.client.protocols", "TLSv1.2");
        System.setProperty("https.protocols", "TLSv1.2");
        System.setProperty("javax.net.ssl.trustStore", "C:\\Program Files\\Java\\jdk-15\\lib\\security\\cacerts");
        System.setProperty("javax.net.ssl.trustStorePassword", "changeit");
        System.setProperty("javax.net.ssl.keyStore",  "C:\\Program Files\\Java\\jdk-15\\lib\\security\\cacerts");
        System.setProperty("javax.net.ssl.keyStorePassword", "changeit");
    }

    private static final String message =
            """
            GET /Home.aspx HTTP/1.1\r
            Host: bnr.ro\r
            User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0\r
            Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r
            Accept-Language: en-US,en;q=0.5\r
            Accept-Encoding: gzip, deflate, br\r
            Connection: keep-alive\r
            \r
            """;

    public static void main(String[] args) throws IOException {

        try (SSLSocket socket = SocketService.createSocket("bnr.ro", 443)) {

            // print cert info
            PrintCertInfo.printCertInfo(socket.getSession().getPeerCertificates()[0]);

            InputStream is = new BufferedInputStream(socket.getInputStream());
            OutputStream os = new BufferedOutputStream(socket.getOutputStream());

            os.write(message.getBytes());
            os.flush();

            byte[] data = new byte[2048];
            int len;
            StringBuilder sb = new StringBuilder();
            while((len = is.read(data)) > 0) {
                sb.append(new String(data, 0, len));
            }
            String response = sb.toString();
            int htmlStartIndex = response.indexOf("<!");
            try (BufferedWriter writer = new BufferedWriter(new FileWriter("bnr_home.html"))) {
                writer.write(response.substring(htmlStartIndex));
            }
        }
    }
}
