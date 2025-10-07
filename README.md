
# Robotino Integration für Ausbildung und Automatisierungsprojekte

Dieses Repository enthält Programme, Skripte und Layouts zur Integration des **Festo Robotino** in Automatisierungsumgebungen.  
Ziel ist es, den Robotino über **Standard-Industriekomponenten** wie **SPS (Siemens S7-1500, TIA Portal)** und **HMI-Panels** steuerbar zu machen sowie ein **Docking an Stationen** zu ermöglichen.

Die Umsetzung kombiniert **OPC UA**, **REST API**, **Python-Skript** und **SPS-Programmierung**. Dadurch kann der Robotino direkt über eine SPS gesteuert oder durch zusätzliche Python-Bibliotheken erweitert werden.  
Unterstützt werden mehrere Robotinos gleichzeitig. Die Kommunikation läuft dabei über ein Python-Skript. Außerdem wurde ein Docking-Algorithmus entwickelt, mit dessen Hilfe der Robotino an CP-Lab-Stationen andocken und Werkstücke transportieren kann.

---

## 📂 Repository-Inhalte

- **`/python/`** – Python-Skript als Vermittler zwischen Robotino (REST API & RobotinoView) und SPS (OPC UA).  
- **`/tia-project/`** – Siemens TIA Portal Projekt (Datenbaustein für die OPC UA-Kommunikation, Funktionsbausteine `GoTo` und `DockTo`, Beispiel-HMI).  
- **`/robotino-view/`** – RobotinoView-Programme (Navigation, Joystick).  
- **`/docking/`** – Schrittkette und Layout für das Dockingprofil.  

---

## 🚀 Erste Schritte

### Voraussetzungen
- **Python 3.11+**  
  - benötigte Pakete: `requests`, `opcua`  
- **Siemens TIA Portal** (ab V18)  
- **SPS oder PLCSIM** mit aktiver OPC UA-Schnittstelle  
- **Festo Robotino 3 oder 4** (OS-Version: 4.20.10 mit REST API)  
- **RobotinoFactory** (für Karten und Posen)  
- **RobotinoView** (für Navigation)

### Anwendung

1. Falls notwendig: Robotino-Softwareupdate durchführen (siehe (https://wiki.openrobotino.org/Robotino3_usb_restore.html). Mit rufus (siehe (https://rufus.ie/de/) bootfähigen USB-Stick erstellen).  
2. Robotino konfigurieren: Monitor anschließen und im Webinterface (`127.0.0.1`) Netzwerkeinstellungen anpassen.  
3. Mit **RobotinoFactory** eine Karte der Umgebung erstellen und Posen, Sperrzonen sowie Wege definieren.  
4. Netzwerkverbindung zwischen Robotino, SPS und externem Rechner herstellen.  
5. SPS-Programm *Robotino* in die SPS laden, ggf. Netzwerkeinstellungen anpassen.  
6. **RobotinoView**-Programm *RobotinoNavigationPLC* auf dem Robotino starten. Sicherstellen, dass der OPC UA-Server aktiv ist.  
7. Python-Skript starten.  
