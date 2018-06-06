## 
## 
## // Einfache Blockchain in Python \\
##
## Version: 1.0 
##
## Author : Stefan Eickholz
## Datum:   01.06.2018
## Ort:     Potsdam
## Sprache: Python
## Version: 3.6.1
##

## In den folgend gezeigten Programmanweisungen werden Basisfunktionalitaeten
## einer Blockchain mittels Python funktionsfaehig umgesetzt.
## 
## Es wird eine freiwaehlbare Anzahl Bloecke erzeugt und verifiziert (siehe Zeile 353). 
## 

import time

class Block(object):
	def __init__(self, idx, preHash, timestamp, data, thisHash):
		self.blockIndex = idx
		self.previousHash = preHash
		self.timestamp = timestamp
		self.blockData = data
		self.blockHash = thisHash

# Zugriff auf Objekt Attribute
def getBlockIndex(myBlock):
	return myBlock.blockIndex

# Zugriff auf Objekt Attribute
def getPreHash(myBlock):
	return myBlock.previousHash

# Zugriff auf Objekt Attribute
def getTimestamp(myBlock):
	return myBlock.timestamp

# Zugriff auf Objekt Attribute
def getData(myBlock):
	return myBlock.blockData

# Zugriff auf Objekt Attribute
def getHash(myBlock):
	return myBlock.blockHash

# Generiere Zeitmarke
def getTime():
	myTime = time.time()
	return myTime

# Print Objektattribute
def printBlockAttributes(Block):
	print('Block.blockIndex: ',   Block.blockIndex)
	print('Block.previousHash: ', Block.previousHash)
	print('Block.timestamp: ',    Block.timestamp)
	print('Block.blockData: ',    Block.blockData)
	print('Block.blockHash: ',    Block.blockHash)
	print(' ')
	return None

# Liefert den vorhergenden Block zurueck
def getPreviousBlock(myList):
	
	# Speichere Laenge der Liste
	lastIdx = len(myList)

	# Vermeide Fehler bei Zugriff auf 
	# Genesisblock 
	# (kein Vorgaenger vorhanden! *List index out of range* error.)
	if lastIdx == 0:
		block = myList[0]
		return block

	# Sonst, letztes Element der Liste -1 auswählen
	else:
		# Zugriff auf Sequenz myList bzw. myBlockchain
		block = myList[lastIdx-1]
		
		# Rueckhabewert ist der gesuchte Block
		return block

def getGenesisBlock(myList):
	firstBlock = myList[0]
	return firstBlock

# Gibt einen neuen Blockindex zurueck
def getNewBlockIndex(myList):
	preBlock = getPreviousBlock(myList)
	idx = preBlock.blockIndex + 1
	return idx

# Gibt den Blockindex des Vorgaengers
# zurueck
def getPreviousIndex(myList):
	preBlock = getPreviousBlock(myList)
	Idx = preBlock.blockIndex
	return Idx

# Gibt den Hashwert des Vorgaengers
# zurueck
def getPreviousHash(myList):
	preBlock = getPreviousBlock(myList)
	Hsh = preBlock.blockHash
	return Hsh

# Gibt Nutzdaten des Vorgaengers 
# zurueck
def getPreviousData(myList):
	preBlock = getPreviousBlock(myList)
	data = preBlock.blockData
	return data

# Berechnet Hashwert für einen bestimmten Block
# und gibt ihn zurueck
def calculateHash(idx, preHash, time, data):
	# Alles in String umwandeln
	idx_str      = str(idx)
	time_str     = str(time)
	preHash_str  = str(preHash)
	data_str     = str(data)

	# addiere
	myStr = idx_str + preHash_str + time_str + data_str

	# Generiere Hashwert
	myHash = hash(myStr)
	
	# Liefert Hashwert zurueck
	return myHash	

# Ersten Block der Kette erstellen
def generateGenesisBlock(myList):

	# Erstelle Attribute
	thisIndex = 0
	Index_str = str(thisIndex)

	# Vorhergehender Hashwert
	preHash = hash(0)
	preHash_str = str(preHash)

	# Zeitmarke
	thisTimestamp = time.time()
	Time_str = str(thisTimestamp)

	# Daten
	thisData = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks."

	# Addiere einzelne Strings
	# zu einem Gesamtstring
	hashGenesis = Index_str + preHash_str + Time_str + thisData
	
	# Erzeuge Hashwert
	thisHash = hash(hashGenesis)
	thisHash_str = str(thisHash)

	# Ersten Block der Kette mit vorher 
	# definierten Werten erzeugen
	GenesisBlock = Block(idx=thisIndex, 
		preHash=preHash_str,
		timestamp=thisTimestamp,
		data=thisData,
		thisHash=thisHash_str)
	
	# Block zurueckgeben
	return GenesisBlock

# Einen neuen Block erstellen
# (abgesehen von Genesisblock)
def generateBlock(myData, myList):

	# Wenn kein GenesisBlock vorhanden ist,
	# versuche ihn ein 2. Mal zu generieren.
	if len(myList) == 0:
		newGenesisBlock = generateGenesisBlock(myList)
		insertBlock(newGenesisBlock, myList)
		if len(myList) > 0:
			print('Genesisblock konnte im zweiten Versuch erstellt werden.\n')
			return newGenesisBlock
		else:
			print('Genesisblock lasst sich auch im zweiten Versuch nicht erzeugen! Fehler!')
			print('Kontaktieren Sie den Entwickler. Die Anweisungen klemmen. :/\n')
			return None

	# Genesisblock ist vorhanden, daher:
	else:
		# Sonst
	 	# Beziehe Index und vorhergenenden
		# Hashwert ueber die Sequenz myList
		newIdx = getNewBlockIndex(myList)
		preHash  = getPreviousHash(myList)
		newTime  = getTime()
		newTime_str = str(newTime)
		
		# Zaehlvariablel an Daten anfuegen
		preBlock = getPreviousBlock(myList)

		# Generiere neuen Hashwert ueber Funktion
		newHash = calculateHash(newIdx, preHash, newTime, myData)

		# Erstelle Block mit Objektkonstruktor
		thisBlock = Block(newIdx, preHash, newTime, myData, newHash)

		# Liefer Block als Rueckgabewert
		return thisBlock

# Fuege den Block in die Kette ein
def insertBlock(newBlock, myList):
	myList.append(newBlock)
	return None

# Verifiziere den neuen Block
# Liefert True fuer verifizierten Block
# sonst False
def isValidBlock(checkMeBlock, preBlock, myList):
	
	# Wenn der Genesisblock geprueft wird
	if checkMeBlock.blockIndex == 0:
		# Keine Pruefung, dieser Block ist immer gut.
		return True

	# Es wird ein vom Genesisblock verschiedener Block
	# geprueft
	else:
		# Erstelle Pruefindex
		preIdx = getPreviousIndex(myList)
		resolvedIdx = preIdx + 1

		# Zugriff auf Attribute
		preHash = getPreHash(checkMeBlock)
		time    = getTimestamp(checkMeBlock)
		data    = getData(checkMeBlock)

		# Hashwert des zu pruefenden Blocks neu berechnen
		# print('Re-calculating Hash...')
		recalculatedHash = calculateHash(resolvedIdx, preHash, time, data)
		saved_hash = getHash(checkMeBlock)

		# Testfall 1
		# 
		# Entspricht der Blockindex dem zu erwartenden
		# Index? Ungleicher Index liefert false.
		if resolvedIdx != checkMeBlock.blockIndex:
			print('(Testfall 1)\n Bad block error: Falscher Blockindex!')
			return False

		# Testfall 2
		#
		# Vergleiche Blockhash des Vorgaengers mit gespeicherten Vorgaengerhash 
		# im neuen Block. Sind die Attributwerte nicht identisch, liefere
		# false
		elif preBlock.blockHash != checkMeBlock.previousHash:
			print('(Testfall 2)\n Bad block error: Gespeichertes Attribut *Hashwert von Vorgaengerblock* entspricht nicht dem zu erwartenden Hashwert!')
			return False

		# Testfall 3
		# 
		# Sind gespeicherter Hashwert im Block und der neu
		# berechnete Hashwert identisch?
		# Wenn nein, gebe false zurueck
		elif recalculatedHash != saved_hash:
			print('(Testfall 3)\n Bad block error: Neu berechneter Blockhashwert entspricht nicht dem gespeicherten Attributwert!')
			return False

		# Testfaelle 1-3 bestanden. 
		# Block ist verifiziert.
		# Funktion liefert True zurueck.	
		return True

# Hier (noch) nicht eingebaut, Funktion soll Block
# von einem anderen Knoten erhalten
def receivedBlock():
	pass

##############################
 ###-=/// Main-Loop \\\=- ###
##############################

print('\nProgrammstart.\n')

# 1. Erzeuge sequenziellen Datentyp für Blockchain
#
# Hier werden die Bloecke gespeichert. In einer 
# erweiterten Version wird die Sequenz in jedem
# Knoten des Netzwerks vorgehalten und bei der 
# Erstellung neuer Bloecke synchronisiert.
print("Erstelle Blockchain.")
myBlockchain = []

# 2. Erzeuge den ersten Block der Blockchain
# 
# (dieser wird immer erzeugt und ist immer in der 
#  Blockchain vorhanden. Deswegen wird seine Erstellung
#  ausserhalb der Hauptschleife angewiesen.)

# Erstelle Genesisblock
Genesisblock = generateGenesisBlock(myBlockchain)

# An Blockchain anfuegen.
insertBlock(Genesisblock, myBlockchain)

# Ist Genesisblock ok?
if len(myBlockchain) != 0:
	# Genesisblock ist nicht schlecht, 
	# also wurde der Block erstellt. 
	print('Genesisblock erzeugt.')
	print('Genesisblock in Blockchain eingefügt.\n')

else:
	print('Genesisblock konnte nicht erzeugt werden. Die Anzahl an Bloecken in der Kette entspricht Null.')
	print('Versuche neuen Startblock zu erzeugen...')
	neuerGenesisBlock = generateBlock('Genesisblock im zweiten Versuch erstellt.', myBlockchain)
	
# 3. Erzeuge alle weiteren Bloecke
#
# Nachdem die Blockchainsequenz und der erste 
# Block erstellt worden sind, ist es nun an 
# der Zeit, weitere Bloecke zu erstellen und 
# in die Blockchain einzugliedern.

# Erstelle Zaehlvariable fuer Hauptschleife
# i ist 1, weil ein Block bereits in der 
# Kette ist.
i=1

# Beginne mit Hauptschleife
while True:

	# Abbruchkriterium
	# 
	# Gib an, wieviele Bloecke erstellt 
	# werden sollen. Veraendere dem-
	# entsprechend die zu vergleichende
	# Variable i. 

	# Zb i == 11 bedeutet,
	# dass 10 Blocke erstellt werden +
	# 1xGenesisblock (also 11 Bloecke 
	# in der Liste sind).
	# 
	# Wenn i erreicht wird,
	# endet das Programm.
	# (spaeter i ueber Kommandozeile uebergeben)

	# Wird i == 0 gewaehlt, werden Bloecke erzeugt, 
	# bis Python keinen Speicher mehr zur Verfuegung hat.
	# (mach das nicht ;) )

	if i==3000000:
		# Drucke testweise die Attribute
		# des ersten und letzten Blocks.
		anzahl = len(myBlockchain)
		print('\nDie Blockchain enthaelt Anzahl Bloecke:', anzahl)
		print('\nOutput Attribute von Block mit Index 0 und letztem Block: \n')

		# Attribute 1 Block (Genesisblock)
		ersterBlock = getGenesisBlock(myBlockchain)
		printBlockAttributes(ersterBlock)

		# Attribute letzter Block
		letzterBlock = getPreviousBlock(myBlockchain)
		printBlockAttributes(letzterBlock)

		# Ende
		print('Programmende.\n')
		break

	# Sonst, erzeuge neue Bloecke
	else:
		# Haenge die Anzahl an Bloecken
		# an das Datenpaket jedes Blocks 
		# an (jeder Block soll andere
		# Daten enthalten)
		anzahlVorgaengerBloecke = len(myBlockchain)

		#(+1 weil die Anzahl der Elemente noch 
		#  fuer die Laenge des Vorgaengers gilt, 
		#  also bis Programmzeile 389)
		anzahlBloecke = anzahlVorgaengerBloecke + 1

		# Umwandeln in String
		anzahlBloecke_str = str(anzahlBloecke)

		# Strings addieren
		myData = 'meine_Daten_abc123 Anzahl Blöcke in der Blockchain: ' + anzahlBloecke_str

		# Erstelle neuen Block
		receivedBlock = generateBlock(myData, myBlockchain)

		# 2. Validiere Block
		# 
		# Welcher Block soll ueberprueft werden?
		# Der von diesem Knoten erzeugt oder von 
		# einem anderen Knoten erhaltene Block
		blockToCheck = receivedBlock

		# Zugriff auf Vorgaenger
		preBlock = getPreviousBlock(myBlockchain)

		# Starte den Test
		# (Wird der naechste Kommentar einkommentiert, erhoeht sich die Laufzeit deutlich)
		# 
		# checkIdx = blockToCheck.blockIndex
		# print('\nVerifiziere neuen Block mit dem Index: ', checkIdx)
		if isValidBlock(blockToCheck, preBlock, myBlockchain) == True:
			
			# print('Block is valid!\n')
			insertBlock(blockToCheck, myBlockchain)

		else: 
			print('Block konnte nicht verifiziert werden! Block nicht in die Kette eingefuegt.\n')
			print('Break!\n')
			break

		# Zaehlvariable um 1 erhoehen
		i=i+1

# Zurueck zum Schleifenanfang, bis Abbruchkriterium greift
