# Crypto_Wallet
## Opis
Program napisany w pythonie tworzący funkcjonujący portfel na kryptowaluty. Do pobierania informacji na temat kryptowalut i ich cen użyto CoinGecko API (https://www.coingecko.com/pl/api#explore-api).  

## Pliki
### Wallet.py
Plik zawierający całość potrzebnego kodu do poprawnego funkcjonowania portfela.
### Wallet_file.json
Plik json w którym znajdować się będzie zapisany porfel z kryptowalutami użytkownika.

## Klasy
### ChoiceWin
Klasa tworząca okno w którym następuje wybór zakresu czasu prezentowanego na wykresie cen kryptowalut. Możliwe przedziały to: 1 dzień, 7 dni oraz 30 dni.
### PlotWin
Klasa tworząca okno z wykresem zmieny ceny jednej wybranej kryptowaluty w zakresie podanym w klasie **ChoiceWin**.

## Metody
### crypto_info
Metoda API, która zwraca plik json z ogólnymi informacjami na temat kryptowaluty (nazwa, cena, itd.).
### crypto_price_range
Metoda API, która  zwraca plik json z listą dat oraz cen kryptowaluty w podanym interwale czasu (interwał mierzony w dniach).
### api_status
Metoda API, sprawdzająca aktualny status API.
### add_to_wallet
Metoda dodająca podaną liczbę kryptowaluty do portfela użytkownika.
### reset_wallet
Metoda resetująca zawartość portfela użytkownika. Metoda nie zmienia wartości porfela zapisanego w pliku Wallet_file.json.
### save_wallet
Metoda zapisująca obecną zawartość portfela użytkownika do pliku Wallet_file.json.
### upload_wallet
Metoda wczytująca porfel z pliku Wallet_file.json do aplikacji.
### walet_value
Metoda prezentująca wartość portfela użytkownika w USD (dolary amerykańskie). Przedstawia ona również różnicę wartości porfela z wartością wartością porfela 24 godzin temu.
### Change_wallet
Metoda pozwalająca użytkownikowi na zmianę liczby kryptowaluty w jego porfelu na inną wartość.
### Main
Tworzenie interfejsu graficznego.

