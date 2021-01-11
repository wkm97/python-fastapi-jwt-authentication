DROP TABLE users, client_information

CREATE TABLE IF NOT EXISTS active_sessions (
   token varchar(255) NOT NULL,
   exp bigint NOT NULL,
   iat bigint NOT NULL,
   token_type varchar(255) NOT NULL,
   PRIMARY KEY(token_type, token)
);

CREATE TABLE IF NOT EXISTS client_information(
   client_id varchar(255) NOT NULL,
   public_key TEXT NOT NULL,
   PRIMARY KEY(client_id)
);

CREATE TABLE IF NOT EXISTS user_information(
   id serial,
	username VARCHAR (255) UNIQUE NOT NULL,
	password VARCHAR (255) NOT NULL,
   PRIMARY KEY(id)
);

INSERT INTO public.user_information
(username, "password")
VALUES('JDoe', '123456');


INSERT INTO public.client_information
(client_id, public_key)
VALUES('GlobeOSS', '''-----BEGIN CERTIFICATE-----
MIIDVzCCAj8CFHpb1AVm0dMr8DXW1NZvp/Hf7N75MA0GCSqGSIb3DQEBCwUAMGcx
CzAJBgNVBAYTAk1ZMREwDwYDVQQIDAhTZWxhbmdvcjEPMA0GA1UEBwwGU3ViYW5n
MREwDwYDVQQKDAhHbG9iZW9zczERMA8GA1UECwwIU29mdHdhcmUxDjAMBgNVBAMM
BXdrbTk3MCAXDTIxMDEwNTA4MjExNloYDzMwMDEwMzA5MDgyMTE2WjBnMQswCQYD
VQQGEwJNWTERMA8GA1UECAwIU2VsYW5nb3IxDzANBgNVBAcMBlN1YmFuZzERMA8G
A1UECgwIR2xvYmVvc3MxETAPBgNVBAsMCFNvZnR3YXJlMQ4wDAYDVQQDDAV3a205
NzCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAOBziB46SEwHOl1u5xOK
a7t+pjwsaIoe/Of/9s89vTZLYzte13i0QnhGdLg7DK3W+UPtdZ9Uy+fpChGoIaNe
uXQcX60tpDJ0xg82AMmv/BDeEVbX9rhBxtTkxHYKyGDEtR+MQA9Z5a8Fc4JE8wTK
O0Eq9Qm16mtaAGYgX5tV7/ngVjX5EvCMc1SmkGJZzcXa07j0azthVuYCzwDFSuKb
S6wBC8TlWSZk0rTA25GvgqjygDacdp1cfRb5dCkpMYkhpqfJDiDgfvvi+KwVNKIs
ZRH//tua9/ESiJ1WFTFy6Sh5pZpYTt2KO8/qPMwN9kdZ5M+zB3ABK/AjwMu4W5Kn
al8CAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAo0FzyMFR54zjDkDBdDLkseoG3dPO
Dlh50ITH0S3X1E/fEtseqa1/9zvjnGsNSKPGYlt9MFkorDVjvaSIVke8LeWZrCFD
G/VsGS+5Hlw+OUdohaXqX72+eHjYrgHZ97p7nuIo3Y+kv63a44yEAzPn/4bJyy5+
eURf5XC/Lu4s4aRTf+tF+jswRi9iHzKGejZRRrQWcG/8z9bN7gm8lNDpLkigZ2fC
EUTlCXTJ0mCgyAcPc3SWAmoWmHwWPZnBZuf6Sm099H/0WnOw+rgY/UT735Fl9Tp9
QkZHcbC2qGefS6XOJR+NJolzps7K/JgAvBytkYTkO0L8c+upsPCHavlwGw==
-----END CERTIFICATE-----
''');
