## Dokumentation Blockchain Projekt

In dieser Dokumentation werden die wichtigsten Punkte, wie Konzept oder verwendete Technologien erläutert.

### 1. Vorgehensweise

Die Arbeit wird zwischen den Teammitgliedern Jan und Timm folgendermaßen aufgeteilt:
- Timm fokussiert sich auf die Konzeption und Umsetzung des Peer-to-Peer-Netzwerkes. Dazu gehört fürs erste beispielsweise die Entwicklung eines p2p-clients (der ebenso Server-Eigenschaften besitzt), der sich mit anderen Clients/Nodes verbinden kann und bestimmte Nachrichten senden und empfangen kann.
- Jan fokussiert sich auf die Konzeption und Umsetzung der Blockchain selbst. Dazu gehört fürs erste beispielsweise die Entwicklung einer einfachen Blockchain-Applikation, die Daten in Blöcke schreibt, diese über hashes zu einer Blockchain verbindet und diese Chain lokal speichern und abrufen kann.

Die einzelnen Aufgaben und der Arbeitsfortschrit werden in Github-Projects verwaltet.

### 2. Konzept

#### 2.1 Speicherung der Blöcke

- Jeder Node speichert unabhängig die gesamte Blockchain mit den bereits validierten Blöcken\
  -> Shared Nothing (Eigener CPU, RAM und Festplatte)
- Ein Block wird durch eine JSON-Datei abgebildet und gespeichert
- Der Dateiname besteht aus dem Index des Blocks (blk00001). Im Dateikörper werden der Hash, die Zeit der Erstellung,\
  Transaktionsdaten des Blocks, sowie der Hash des vorhergehenden Blocks festgehalten


#### 2.2 Peer-to-Peer-Netzwerk Architektur

- Unstrukturiertes Netzwerk
- Ein Node verbindet sich nur mit einer bestimmten Anzahl von anderen Nodes 
- Alle Nodes sind sowohl server als auch client (-> servent) 
  -> download- und upload-fähig
  -> gleiche Aufgaben, Funktionen und Rechte:
    - transaktionen erstellen
    - transaktionen validieren
    - blöcke minen
    - blockchain validieren und synchronisieren
- Es gibt keine verschieden node-Typen/Rollen. Z.B. keine pruned-nodes, die nicht die ganze Blockchain speichern, sondern nur full nodes
- Damit ein neuer Node eine erste Verbindung herstellen kann, werden ein paar IP-Adressen hardgecoded (wie bei Bitcoin) 
- Auserdem wird es einen Server geben der Ip Adressen von Nodes zurückgibt, die schonmal mit dem Server verbunden waren.

##### Alle Nodes können folgende Nachrichten senden und empfangen:

- version
- verack
- getAddr
- addr
- ping
- pong

- getBlocks
- inv
- getData
- block

im folgenden werden diese Nachrichten sowie deren Zweck, Inhalt und Ablauf genauer beschrieben:


##### Initial Block Download (IBD)

IBD wird ausgeführt wenn ein Node das erste mal gestartet wird und keine Blockchain vorhanden ist und anschließend in einem bestimmten Zeitintervall wiederholt, damit die Blockchain aktuell bleibt.

<img src="https://github.com/TimmMoetz/blockchain-lab/blob/gh-pages/docs/assets/blocks-first-flowchart.svg" alt="Image" class="inline"/>

<img src="https://github.com/TimmMoetz/blockchain-lab/blob/gh-pages/docs/assets/IBD.svg" alt="Image" class="inline"/>

Payload von getblocks: hash des obersten Blocks in der Blockchain des Nodes 

Payload von inv: Liste von hashes aller Blöcke in der Blockchain des Nodes, ab dem Block mit dem Hash aus der getblocks-Nachricht 

Payload von getdata: sie selbe Liste wie in inv

Payload von block: ein block im JSON-Format



Wenn ein Node neuen Block generiert (mining), schickt er eine inv-Nachricht (payload: hash des neuen Blocks) an seine Peers. Diese können dann den neuen block mit getdata anfordern.


###### Longest Chain

Die längste Chain ist die Chain mit den meisten Blöcken (so wie in Bitcoins erster version. Aktuell wird das anhand der benötigten energy zum minen der Cahin bestimmt, aber das ist zu sprengt unseren ramen und ist auch nicht relevant, weil wir auch keine difficulty verändern werden)

###### Transaktionen und Longest Chain
1. Warum keine Transaktionen verschickt werden:
    1. Transaktion wird an weitere Nodes verschickt -> Bei erfolgreichem Anhängen von Node A an die Chain muss Transaktion bei anderen Nodes aus dem Memory Pool gelöscht werden
    2. Candidate Block Konzept nicht möglich, da kein Mining implementiert wird
2. Konzept zum erstellen von Transaktionen:
    1. Eine Transaktion (evtl. 2/3 Transaktionen) wird einem Block gespeichert
    2. Sobald der Block gespeichert wird, wird er der Blockchain angehängt
    3. Erst wenn ein weiterer Block der Chain hinzugefügt wird, ist die Transaktion in dem vorletzten Block gültig
3. Konzept der longest Chain und dem Austausch der Blöcke
    1. Wenn zwei Chains mit jeweils unterschiedlichen letzen Blöcken im Netzwerk existieren wird beim entstehen des nächsten Blocks eine neue längste Chain gebildet. Der Block in der anderen Chain fällt somit heraus und die Transaktion darin wird gelöscht.



## Durchlauf Start - Transaktion - Blockerstellung

##### Start
Beim Starten des Nodes wird geprüft, ob schon ein public, sowie private Key erstellt wurde, wenn dies noch nicht erfolgt ist, wird einer erstellt und in einer Datei gespeichert. Danach wird sich die aktuelle Chain durch den IBD (Initial Block Download) von einem anderen Node im Netzwerk geholt.

##### Transaktion und Memorypool
Ein Node kann über die Kommando Zeile eine Transaktion erstellen, wobei dieser den Public Key des Empfängers und den zu sendenden Betrag einträgt. Die Transaktion wird mit folgendem Inhalt erstellt:

1.	Receiver: Public Key des Empfängers (es gibt nur einen Receiver)
2.	Sender: Public Key des Senders
3.	Signature: Transaktionshash + Private Key vom Sender
4.	Amount: Betrag der versendet wird

Der Versand und die Validierung verlaufen nach dem Two Phase Commit und wird mit allen direkten Peers durchgeführt. Es werden zwei Sachen validiert:

1.	Prüfung, ob der Sender ausreichend Guthaben für die gewünschte Transaktion hat
2.	Signature validieren, wobei Hash A = Signature + Public Key des Senders ist und Hash B = der Hash der Transaktion ist. Somit muss Hash A = Hash B sein, damit die Transaktion als valide gilt.

Sobald die Transaktion von allen Peers validiert wurde, wird sie im Ordner Memorypool gespeichert und befindet sich im Status Pending Transaction. 

##### Mining und Anhängen des Blocks
Wenn ein Node dann den Befehl zum Minen in die Kommando Zeile eingibt, wird aus allen Transaktionen in dessen Memorypool ein Candidate Block mit den ersten zehn Transaktionen erstellt. Das mining funktioniert nach dem Proof of Work Mechanismus. Der Nonce wird so lange hochgezählt und neu gehashed, bis die festgelegte Schwierigkeit erfüllt wird. Sobald ein passender Nonce gefunden wurde wird der dazugehörige Block validiert. Dabei wird geschaut, ob alle Transaktionen validiert wurden, ob die Schwierigkeit erfüllt worden ist, ob der Hash dem neu kalkulierten Hash entspricht und ob die Transaktionen im Block bereits von einem anderen Node in einem Block gespeichert und an die Chain angehängt wurden. Der dann validierte Block wird an die direkten Peers versendet und die Transaktionen des Blocks werden aus dem Memorypool gelöscht und im letzten Schritt an die eigene Chain angehängt.
Die direkten Peers, die den neuen Block empfangen, validieren diesen ebenfalls anhand der oben beschriebenen Überprüfungen und senden diesen dann ebenfalls weiter. Wenn der vorherige Hash des neuen Blocks der eigene latest Block Hash ist, werden die Transaktionen ebenfalls aus dem eigenen Memorypool gelöscht und an die eigene Chain gehängt. Wenn dies nicht der Fall ist wird wie am Anfang der IBD durchgeführt.

