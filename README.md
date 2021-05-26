# Crypto_Wallet
## Opis
Program napisany w pythonie tworzący funkcjonujący portfel na kryptowaluty.

## Pliki
### Wallet_App.py
Plik zawierający całość potrzebnego kodu do poprawnego funkcjonowania portfela.
### Wallet_file.json
Plik json w którym znajdować się będzie zapisany porfel z kryptowalutami użytkownika.

## Klasy
### ChoiceWin
Klasa tworząca okno w którym następuje wybór zakresu czasu prezentowanego na wykresie cen kryptowalut.
### PlotWin
Klasa tworząca okno z wykresem zmieny ceny jednej wybranej kryptowaluty w zakresie podanym w klasie **ChoiceWin**.

## Metody
### crypto_info
Metoda API, która zwraca plik json z ogólnymi informacjami na temat kryptowaluty (nazwa, cena, itd.).
### crypto_price_range
Metoda API, która  zwraca plik json z parami cena kryptowaluty oraz czas w którym kryptowaluta miała podaną cenę. Zakres czasu pobieranych wyrażona w dniach.

