## Motivation
Über die Steuerung von elektronischen Bauteilen (Sensoren und Aktoren) durch Minicomputer, wie einen Raspberry Pi, existiert ein Flickenteppich aus Tutorials und Programm-Bibliotheken. Es fehlt ein einfacher und strukturierter Einstieg, sowie eine generische Schnittstelle zu den verschiedenen Bauteilen.

Mit einem gut dokumentierten Python-Modul fällt der Einstieg leichter und ein integriertes MQTT-Interface bildet die Schnittstelle für mehr Softwarevielfalt.

Das Modul "tentacle" kann als Werkzeug ins eigene Programm importiert werden, um dort direkt Bauteile zu steuern. Alternativ läuft es eigenständig und stellt via MQTT Echtzeitdaten und Optionen von angeschlossenen Bauteilen bereit.

Moritz Münch und Thorben Willert

Written with `<3` and python. License: MIT
