# Fake certificate

in the `certificates` directory

  + `keytool -genkey -keypass changeit -storepass changeit -keystore fakekeystore.jks -keyalg RSA -keysize 2048 -validity 35`
  + `keytool -export -storepass changeit -file fake.cer -keystore fakekeystore.jks`
  + `keytool -import -v -trustcacerts -file fake.cer -keypass changeit -storepass changeit -keystore faketruststore.jks`

# Creating and signing certificates with openssl

in the `certificates` directory

## RootCA:
+ Navigate to `root` directory
+ Create root EC key with ecparam:\
   + `openssl ecparam -genkey -noout -out RootCA.key -name brainpoolP256t1`
+ Create root certificate with req:\
   + `openssl req -new -x509 -days 35 -key RootCA.key -out RootCA.crt`

## ServerCA
+ Navigate to `server` directory
+ Create server EC private key:\
   + `openssl ecparam -genkey -noout -out ServerCA.key -name brainpoolP256t1`
+ Create server certificate:\
   + `openssl req -new -sha256 -key ServerCA.key -out ServerCA.csr`
+ Sign server certificate by RootCA:\
   + `openssl x509 -req -days 35 -in ServerCA.csr -CA ../root/RootCA.crt -CAkey ../root/RootCA.key -CAcreateserial -out ServerCA.crt`

## ClientCA
+ Navigate to `client` directory
+ Create client EC private key:\
   + `openssl ecparam -genkey -noout -out ClientCA.key -name brainpoolP256t1`
+ Create client certificate:\
   + `openssl req -new -sha256 -key ClientCA.key -out ClientCA.csr`
+ Sign client certificate by RootCA:\
   + `openssl x509 -req -days 35 -in ClientCA.csr -CA ../root/RootCA.crt -CAkey ../root/RootCA.key -CAcreateserial -out ClientCA.crt`

## Server certificate
+ Navigate to `server` directory
+ Create server private key:\
   + `keytool -genkeypair -keyalg RSA -keysize 2048 -sigalg SHA256withRSA -validity 35 -alias server -storetype JKS -keystore ../serverkeystore.jks -storepass changeit`
+ Create server certificate:\
   + `keytool -certreq -alias server -file server.csr -keystore ../serverkeystore.jks`
+ Sign server certificate by ServerCA:\
   + `openssl x509 -req -days 35 -in server.csr -CA ServerCA.crt -CAkey ServerCA.key -CAcreateserial -out server.crt`

## Client certificate
+ Navigate to `client` directory
+ Create server private key:
   + `keytool -genkeypair -keyalg RSA -keysize 2048 -sigalg SHA256withRSA -validity 35 -alias client -storetype JKS -keystore ../clientkeystore.jks -storepass changeit`
+ Create server certificate:
   + `keytool -certreq -alias client -file client.csr -keystore ../clientkeystore.jks`
+ Sign server certificate by ServerCA:
   + `openssl x509 -req -days 35 -in client.csr -CA ClientCA.crt -CAkey ClientCA.key -CAcreateserial -out client.crt`

## Import signed certificates
+ navigate back to `certificates` directory
  + `keytool -import -alias serverSigned -keystore serverkeystore.jks -file server/server.crt`
  + `keytool -import -alias clientSigned -keystore clientkeystore.jks -file client/client.crt`