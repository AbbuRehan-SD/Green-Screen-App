; GreenScreenApp Installer Script for Inno Setup

[Setup]
AppName=Green Screen App
AppVersion=1.0
DefaultDirName={pf}\GreenScreenApp
DefaultGroupName=GreenScreenApp
OutputDir=dist
OutputBaseFilename=GreenScreenAppInstaller
Compression=lzma
SolidCompression=yes
AllowNoIcons=yes
SetupIconFile=app.ico

[Files]
Source: "dist\GreenScreenApp\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Green Screen App"; Filename: "{app}\GreenScreenApp.exe"
Name: "{group}\Uninstall Green Screen App"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\GreenScreenApp.exe"; Description: "Launch Green Screen App"; Flags: nowait postinstall skipifsilent
