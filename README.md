# Zadanie rekrutacyjne, AGH Space Systems Rocket Software jesień 2026

Moim celem w tym zadaniu było stworzenie prostej aplikacji wyświetlającej dane, które są niezbędne do przeprowadzenia lotu rakiety.
Dodatkowo przygotowałem skrypt automatyzujący start oraz lądowanie rakiety.

## Dokumentacja
### Setup
Aplikacja została stworzona przy pomocy nicegui. Znajduje się ona w folderze ```aplication```.
W tym folderze znajduje się również skrypt ```startup_protocol.py``` odpowiadający za automatyzacje startu i lądowanie rakiety.
Aby uruchomić aplikację należy wpisać: 
```bash
python aplication/apk.py
```

Aplikacja automatycznie uruchamia skrypt ```tcp_proxy.py```. Aby uruchomić symulator należy wcisnąć przycisk ```start sim```.
Analogicznie przycisk ```stop sim``` zamyka symulator.

Kiedy symulator jest włączony można uruchomić skrypt ```startup_protocol.py```, aby zinicjalizować start oraz kolejne akcje. 
Przycisk ```initialize start``` uruchamia ten skrypt (przycisk wyświetli się po uruchomieniu symulatora).

### Działanie aplikacji

W skrypcie ```tcp_simulator``` została dodana funkcja ```save_status()```, która zapisuje wszystkie dane do pilku ```rocket_status.json```.
Na tej samej zasadzie działa wyświetlanie errorów, które zapisywane są w pliku ```error_messages.json```.
Kiedy symulator jest wyłączony pliki te zostają usunięte.

### Działanie skryptu startup_protocol

Skrypt wysyła polecenia (tak jak zostało to przedstawione w skrypcie ```frame_sending_receiving_example.py```), które są oddzielone odpowiednimi interwałami czasowymi. 
Głównym narzędziem jest funkcja ```conditioner()```, która pozwala na określenie czy konkrety threshold został spełniony, jeżeli tak to przechodzi do następnego kroku.