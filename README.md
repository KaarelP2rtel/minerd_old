# Minerd
Minerd is a Pyhton based web server designed to monitor my Bitcoin miner. Because the miner is very unstable, it occasionally needs to be powercycled. Minerd achieves this by being connected to an arduino, which controls a relay. This however means, that the web server must run on a computer that is physically near the miner itself.
### Features
-   Data from multiple API's
-   CSS template from w3schools.com
-   Arduino/relay powered physical restart
-   Password authentication

### Detail
The program runs 2 threads. Thread one updates the variables set in the Apis object. Basic data is gathered from Coindesk, Coinmarketcap and Nicehash and the rest is calculated. The second thread runs a Flask web server, which returns a template with values from the Apis object. The webpage contains a password field and a submit button. Upon receiving a POST with the right password, a message is sent over a serial connection to the arduino, which cuts power from the miner. The webpage requires authentication. The username, password and restart password are read from a file named "conf". 