1. Otwórz terminal w folderze GameShelf.Desktop.
2. Zainstaluj zależności:
   pip install -r requirements.txt
   pip install pyinstaller
3. Zbuduj aplikację:
   pyinstaller --clean --noconfirm GameShelf.spec
4. Sprawdź, czy działa plik:
   dist\GameShelf\GameShelf.exe
5. Otwórz Inno Setup Compiler.
6. Wczytaj plik:
   installer\GameShelf.iss
7. Kliknij Build > Compile.
8. Gotowy instalator będzie tutaj:
   installer\output\GameShelfSetup.exe
