## Dokumentation Blockchain Projekt

In dieser Dokumentation werden die wichtigsten Punkte, wie Konzept oder verwendete Technologien erläutert.


### 1. Vorgehensweise

Die Arbeit wird zwischen den Teammitgliedern Jan und Timm folgendermaßen aufgeteilt:
- Timm fokussiert sich auf die Umsetzung des Peer-to-Peer-Netzwerkes. Dazu gehört fürs erste beispielsweise die Entwicklung eines p2p-clients (der ebenso Server-Eigenschaften besitzt), der sich mit anderen Clients/Nodes verbinden kann und bestimmte Nachrichten sendet und empfängt.
- Jan fokussiert sich auf die Konzeption und Umsetzung der Blockchain selbst. Dazu gehört fürs erste beispielsweise die Entwicklung einer einfachen Blockchain-Applikation, die Daten in Blöcke schreibt, diese über Hashes zu einer Blockchain verbindet und diese Chain lokal speichern und abrufen kann.


### 2. Konzept

Die Punkte 2.1 und 2.2 beinhalten die Überlegungen, die im Vorhinein getätigt wurden. Dieses wird sich im Laufe des Projekts aufgrund von Zeitdruck und der Schwierigkeit bei der Umsetzung mancher Probleme verändern. Die beschriebenen Konzepte und überlegungen in 2.3, 2.4 und 2.5 wurden im Dezember (circa Hälfte des Projekts) angestellt, die allerdings ebenfalls nicht voll umfänglich oder in der Form umgesetzt werden konnten. 2.6 und alle Unterpunkte sind im Januar entstanden, also gegen Ende des Projekts. Selbst dort sind noch Umsetzungsschwierigkeiten aufgetreten, die dann beim Endprodukt nicht mehr enthalten waren und einige Features nicht umgesetzt werden konnten.

#### 2.1 Peer-to-Peer-Netzwerk Architektur

Bei der Netzwerk Architektur handelt es sich um ein unstrukturiertes Netzwerk. Ein Node verbindet sich mit einer bestimmten Anzahl von anderen Nodes, wobei alle Nodes sowohl als Server, als auch als Client fungieren (-> Servent). Sie sind download- sowie uploadfähig und haben die gleichen Funktionen, Aufgaben und Rechte. Diese beinhalten die Erstellung und Validierung von Transaktionen, das "Schürfen" der Blöcke mit den darin befindlichen Transaktionen und schlussendlich die Validierung und Synchronisation der Blockchain. Da es keine unterschiedlichen Nodetypen gibt und die Blockchain immer komplett gespeichert wird handelt es sich um sogenannte Full-Nodes.
Damit ein neuer Node eine erste Verbindung herstellen kann, werden ein paar IP-Adressen hardgecoded. Dieses Prinzip orientiert sich an der Bitcoin Netzwerk Architektur. Außerdem gibt es einen Server, der IP-Adressen von Nodes zurückgibt, die schonmal mit dem Server verbunden waren.


#### 2.2 Speicherung der Blöcke

Wie bereits erwähnt speichert jeder Node unabhängig die gesamte Blockchain mit den bereits validierten Blöcken. Dies erfolgt anhand des Shared Nothing Ansatzes. Das bedeutet, dass jeder Node seine eigene CPU, Festplatte und seinen eigenen RAM hat.
Ein Block wird durch eine JSON-Datei abgebildet und gespeichert. Der Dateiname besteht dabei asu dem indes des Blocks (blk000001). Im Dateikörper werden der Hash, die Zeit der Erstellung, Transaktionsdaten des Blocks, sowie der Hash des vorhergehendes Blocks festgehalten.


#### 2.3 Initial Block Download (IBD)

Der IBD wird ausgeführt, wenn ein Node das erste mal gestartet wird und keine Blockchain vorhanden ist. Dies wird in einem bestimmten Zeitintervall wiederholt, damit die Blockchain aktuell bleibt. 
Die Nodes können dabei folgende Nachrichten senden und empfangen:
version, verack, getAddr, addr, ping, pong, getBlocks, inv, getData, block

Nachfolgend ein Überblick über den IBD:
<img src="https://github.com/TimmMoetz/blockchain-lab/blob/gh-pages/docs/assets/blocks-first-flowchart.svg" alt="Image"/>

Sequenzdiagramm des IBD mit anschließender Erklärung des Payloads der einzelnen Nachrichten:
<img src="https://github.com/TimmMoetz/blockchain-lab/blob/gh-pages/docs/assets/IBD.svg" alt="Image"/>

Die Nachricht getblock beinhaltet den Hash des obersten Blocks in der Blockchain eines Nodes. In der inv Nachricht ist eine Liste von Hashes aller Blöcke in der Blockchain eines Nodes aufgeführt, diese Liste beginnt mit dem Hash des Blocks aus der getblocks Nachricht. Getdata beinhaltet die gleiche Liste, wie die inv Nachricht. Der Payload von block besteht aus einem Block im JSON-Format.


#### 2.4 Longest Chain

Die Longest Chain in einer Blockchain ist die Kette mit den meisten angehängten Blöcken. Dabei wird das Konzept wie es in der ersten Bitcoin Version war verwendet. Mittlerweile wird die Longest Chain anhand der benötigten Energie zum minen bestimmt, dies würde allerdings den Aufwand sprengen.
Wenn zwei Chains mit jeweils unterschiedlichen letzen Blöcken im Netzwerk existieren wird beim entstehen des nächsten Blocks eine neue längste Chain gebildet. Der Block in der anderen Chain fällt somit heraus und die Transaktion darin wird gelöscht.


#### 2.5 Transaktionen

Da bei erfolgreichem Anhängen eines Blocks die darin enthaltenen Transaktionen bei anderen Nodes aus dem Memory Pool gelöscht werden müssten werden keine Transaktionen verschickt, weil der Aufwand dessen zu groß wäre. Ebenso ist das Konzepts des Candidate Blocks wie bei Bitcoin nicht umsetztbar, da kein Mining implementiert wird.
Eine Transaktion (evtl. mehrere) wird in einem Block gespeichert. Sobald dies erfolgt wird der Block an die Blockchain angehängt. Erst wenn ein weiterer Block der Chain hinzugefügt wird ist die Transaktion in dem vorletzten Block gültig.


#### 2.6 Durchlauf Start - Transaktion - Blockerstellung

##### 2.6.1 Start
Beim Starten des Nodes wird geprüft, ob schon ein public, sowie private Key erstellt wurde, wenn dies noch nicht erfolgt ist, wird jeweils einer der beiden Keys erstellt und in einer Datei gespeichert. Danach wird sich die aktuelle Chain durch den IBD (Initial Block Download) von einem anderen Node im Netzwerk geholt.

##### 2.6.2 Transaktion und Memorypool
Ein Node kann über die Kommando Zeile eine Transaktion erstellen, wobei dieser den Public Key des Empfängers und den zu sendenden Betrag einträgt. Die Transaktion wird mit folgendem Inhalt erstellt:

1.	Receiver: Public Key des Empfängers (es gibt nur einen Receiver)
2.	Sender: Public Key des Senders
3.	Signature: Transaktionshash + Private Key vom Sender
4.	Amount: Betrag der versendet wird

Der Versand und die Validierung verlaufen nach dem Two Phase Commit und wird mit allen direkten Peers durchgeführt. Es werden zwei Sachen validiert:

1.	Prüfung, ob der Sender ausreichend Guthaben für die gewünschte Transaktion hat
2.	Signature validieren, wobei Hash A = Signature + Public Key des Senders ist und Hash B = der Hash der Transaktion ist. Somit muss Hash A = Hash B sein, damit die Transaktion als valide gilt.

Sobald die Transaktion von allen Peers validiert wurde, wird sie im Ordner Memorypool gespeichert und befindet sich im Status Pending Transaction. 

##### 2.6.3 Mining und Anhängen des Blocks
Wenn ein Node dann den Befehl zum Minen in die Kommando Zeile eingibt, wird aus allen Transaktionen in dessen Memorypool ein Candidate Block mit den ersten zehn Transaktionen erstellt. Das mining funktioniert nach dem Proof of Work Mechanismus. Der Nonce wird so lange hochgezählt und neu gehashed, bis die festgelegte Schwierigkeit erfüllt wird. Sobald ein passender Nonce gefunden wurde wird der dazugehörige Block validiert. Dabei wird geschaut, ob alle Transaktionen validiert wurden, ob die Schwierigkeit erfüllt worden ist, ob der Hash dem neu kalkulierten Hash entspricht und ob die Transaktionen im Block bereits von einem anderen Node in einem Block gespeichert und an die Chain angehängt wurden. Der dann validierte Block wird an die direkten Peers versendet und die Transaktionen des Blocks werden aus dem Memorypool gelöscht und im letzten Schritt an die eigene Chain angehängt.
Die direkten Peers, die den neuen Block empfangen, validieren diesen ebenfalls anhand der oben beschriebenen Überprüfungen und senden diesen dann ebenfalls weiter. Wenn der vorherige Hash des neuen Blocks der eigene latest Block Hash ist, werden die Transaktionen ebenfalls aus dem eigenen Memorypool gelöscht und an die eigene Chain gehängt. Wenn dies nicht der Fall ist wird wie am Anfang der IBD durchgeführt.


### 3 Tatsächlich umgesetzt

