#define AppName "GameShelf"
#define AppVersion "1.0.0"
#define AppPublisher "GameShelf"
#define AppExeName "GameShelf.exe"
#define SourceRoot ".."

[Setup]
AppId={{8E4F6B51-08A7-4E86-9B9B-179E24F86C71}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
OutputDir={#SourceRoot}\installer\output
OutputBaseFilename=GameShelfSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
SetupIconFile={#SourceRoot}\assets\GameShelf.ico
UninstallDisplayIcon={app}\{#AppExeName}
PrivilegesRequired=lowest

[Languages]
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"

[Tasks]
Name: "desktopicon"; Description: "Utwórz skrót na pulpicie"; GroupDescription: "Dodatkowe skróty:"; Flags: unchecked

[Files]
Source: "{#SourceRoot}\dist\GameShelf\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourceRoot}\.env"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\assets\GameShelf.ico"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\assets\GameShelf.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Uruchom GameShelf"; Flags: nowait postinstall skipifsilent
