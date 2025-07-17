Proiect practică
================
Scopul aplicației:
Aplicația propusă trebuie să permită accesarea unor formulare generate automat (prin intermediul unui browser), pe baza unor fișiere cu format la alegere.
Răspunsurile oferite de utilizatori trebuie stocate într-o bază de date, iar formularele care dispun de câmpuri precum „Nume complet” sau „Email” trebuie să autocompleteze aceste câmpuri, dacă în baza de date există informații stocate care să fie relevante. (Prin urmare, apare necesitatea implementării unui sistem de înregistrare și autentificare a utilizatorilor). Totodată, există și formulare care ar putea fi completate și sub anonimat.

Funcționalități implementate:
- Server web prin intermediul Python + Flask.
- Generare formulare web pe baza unor fișiere .json prin intermediul HTML + Flask.
- Sistem de înregistrare și autentificare cu ajutorul unei baze de date T-SQL (în SSMS20), conectată la server cu ajutorul pyodbc.
- Transmiterea răspunsurilor oferite de către utilizator, la baza de date și stocarea acestora într-o tabelă.
- Opțiunea de modificare a răspunsului dat la formular, de către utilizator.
- Opțiunea de a exporta sub format PDF răspunsurile dintr-un formular, cu ajutorul uneltelor oferite de reportlab.
- Pagină de autentificare, pagină de înregistrare, pagină meniu, pagini pentru fiecare formular generat, verificarea corectitudinii datelor de autentificare.
- Opțiunea de a completa formulare sub anonimat (fără înregistrare sau autentificare). 
* Stilizarea paginilor și a elementelor de interfață (butoane, câmpuri input) a fost realizată cu fișiere CSS asociate paginilor.
* Fontul utilizat pe site este un font disponibil pe Google Fonts.

---
Pentru rulare Visual Studio Code + Python și:
- comenzile în terminal pentru instalare:
pip install flask
pip install pyodbc
pip install reportlab

