package service;

import java.security.cert.Certificate;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class PrintCertInfo {

    private static final Pattern versionPattern = Pattern.compile("(Version): (.*)");
    private static final Pattern issuerNamePattern = Pattern.compile("(Issuer): CN=([^,]*)");
    private static final Pattern validityFromPattern = Pattern.compile("(Validity): \\[(From): ([^,]*)");
    private static final Pattern validityToPattern = Pattern.compile("(Validity): \\[From: [^,]*,[^T]*(To): ([^]]*)");
    private static final Pattern subjectPattern = Pattern.compile("(Subject): (.*)");
    private static final Pattern[] patterns = {
            versionPattern,
            issuerNamePattern,
            validityFromPattern,
            validityToPattern,
            subjectPattern
    };

    public static void printCertInfo(Certificate cert) {
        String certStr = cert.toString();

        for (Pattern pattern: patterns) {
            Matcher matcher = pattern.matcher(certStr);
            if (matcher.find()) {
                System.out.println(matcher.group(1) + ": "
                        + matcher.group(2)
                        + (matcher.groupCount() > 2 ? ": " + matcher.group(3) : ""));
            }
        }
        System.out.println("Public key algorithm: " + cert.getPublicKey().getAlgorithm());
        System.out.println("Public key: " + cert.getPublicKey());
    }
}
