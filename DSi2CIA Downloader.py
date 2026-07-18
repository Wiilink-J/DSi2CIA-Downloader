import os
import threading
from pathlib import Path
from urllib.parse import unquote

import requests
import customtkinter as ctk
from tkinter import filedialog, messagebox


APP_TITLE = "DSi2CIA Downloader"

LANGS = {
    "English": "en",
    "Français": "fr",
    "Español": "es",
    "Italiano": "it",
    "Deutsch": "de",
    "Português": "pt",
    "Português (Brasil)": "pt_br",
    "Nederlands": "nl",
    "日本語": "ja",
    "Русский": "ru",
}

T = {
    "en": {
        "choose_lang": "Choose language",
        "done": "Done",
        "intro": "This program installs Nintendo DSi system app CIA files, including the files needed to make Nintendo DSi System Settings work on 3DS through a .cia app.",
        "back": "Back",
        "next": "Next",
        "cancel": "Cancel",
        "mode_title": "Select installation type",
        "quick": "Quick setup",
        "quick_desc": "Install all system apps directly.",
        "custom": "Custom setup",
        "custom_desc": "Choose which system apps to install.",
        "custom_apps": "Select the apps you want",
        "choose_dir": "Choose where to save the cia folder",
        "browse": "Browse",
        "success": "Success",
        "success_desc": "The files were installed correctly.",
        "close": "Close",
        "open": "Open folder",
        "select_one": "Select at least one item.",
        "select_dir": "Select a destination folder.",
        "installing": "Installing...",
        "dsi_settings": "DSi System Settings",
        "dsi_settings_desc": "Install both DSi System Settings CIA files together."
    },
    "fr": {
        "choose_lang": "Choisir la langue",
        "done": "Terminé",
        "intro": "Ce programme installe les fichiers CIA des applications système Nintendo DSi, y compris les fichiers nécessaires pour faire fonctionner les paramètres Nintendo DSi sur 3DS via une application .cia.",
        "back": "Retour",
        "next": "Suivant",
        "cancel": "Annuler",
        "mode_title": "Sélectionnez le type d'installation",
        "quick": "Installation rapide",
        "quick_desc": "Installe directement toutes les applications système.",
        "custom": "Installation personnalisée",
        "custom_desc": "Choisissez les applications système à installer.",
        "custom_apps": "Sélectionnez les applications souhaitées",
        "choose_dir": "Choisissez où enregistrer le dossier cia",
        "browse": "Parcourir",
        "success": "Succès",
        "success_desc": "Les fichiers ont été installés correctement.",
        "close": "Fermer",
        "open": "Ouvrir le dossier",
        "select_one": "Sélectionnez au moins un élément.",
        "select_dir": "Sélectionnez un dossier de destination.",
        "installing": "Installation...",
        "dsi_settings": "DSi System Settings",
        "dsi_settings_desc": "Installez ensemble les deux fichiers CIA de DSi System Settings."
    },
    "es": {
        "choose_lang": "Elegir idioma",
        "done": "Hecho",
        "intro": "Este programa instala archivos CIA de las aplicaciones del sistema Nintendo DSi, incluidos los archivos necesarios para que la Configuración de Nintendo DSi funcione en 3DS mediante una app .cia.",
        "back": "Atrás",
        "next": "Siguiente",
        "cancel": "Cancelar",
        "mode_title": "Selecciona el tipo de instalación",
        "quick": "Configuración rápida",
        "quick_desc": "Instala directamente todas las aplicaciones del sistema.",
        "custom": "Configuración personalizada",
        "custom_desc": "Elige qué aplicaciones del sistema instalar.",
        "custom_apps": "Selecciona las aplicaciones que quieres",
        "choose_dir": "Elige dónde guardar la carpeta cia",
        "browse": "Examinar",
        "success": "Éxito",
        "success_desc": "Los archivos se instalaron correctamente.",
        "close": "Cerrar",
        "open": "Abrir carpeta",
        "select_one": "Selecciona al menos un elemento.",
        "select_dir": "Selecciona una carpeta de destino.",
        "installing": "Instalando...",
        "dsi_settings": "DSi System Settings",
        "dsi_settings_desc": "Instala juntos los dos archivos CIA de DSi System Settings."
    },
    "it": {
        "choose_lang": "Scegli la lingua",
        "done": "Fatto",
        "intro": "Questo programma installa i file CIA delle app di sistema Nintendo DSi, compresi i file necessari per far funzionare le Impostazioni Nintendo DSi su 3DS tramite un'app .cia.",
        "back": "Indietro",
        "next": "Avanti",
        "cancel": "Annulla",
        "mode_title": "Seleziona il tipo di installazione",
        "quick": "Configurazione rapida",
        "quick_desc": "Installa direttamente tutte le app di sistema.",
        "custom": "Configurazione personalizzata",
        "custom_desc": "Scegli quali app di sistema installare.",
        "custom_apps": "Seleziona le app che vuoi",
        "choose_dir": "Scegli dove salvare la cartella cia",
        "browse": "Sfoglia",
        "success": "Successo",
        "success_desc": "I file sono stati installati correttamente.",
        "close": "Chiudi",
        "open": "Apri cartella",
        "select_one": "Seleziona almeno un elemento.",
        "select_dir": "Seleziona una cartella di destinazione.",
        "installing": "Installazione...",
        "dsi_settings": "DSi System Settings",
        "dsi_settings_desc": "Installa insieme i due file CIA di DSi System Settings."
    },
    "de": {
        "choose_lang": "Sprache wählen",
        "done": "Fertig",
        "intro": "Dieses Programm installiert CIA-Dateien der Nintendo-DSi-System-Apps, einschließlich der Dateien, die benötigt werden, damit die Nintendo DSi Einstellungen auf 3DS über eine .cia-App funktionieren.",
        "back": "Zurück",
        "next": "Weiter",
        "cancel": "Abbrechen",
        "mode_title": "Installationsart auswählen",
        "quick": "Schnelle Einrichtung",
        "quick_desc": "Installiert direkt alle System-Apps.",
        "custom": "Benutzerdefinierte Einrichtung",
        "custom_desc": "Wähle aus, welche System-Apps installiert werden sollen.",
        "custom_apps": "Wähle die gewünschten Apps aus",
        "choose_dir": "Wähle, wo der cia-Ordner gespeichert werden soll",
        "browse": "Durchsuchen",
        "success": "Erfolg",
        "success_desc": "Die Dateien wurden korrekt installiert.",
        "close": "Schließen",
        "open": "Ordner öffnen",
        "select_one": "Wähle mindestens ein Element aus.",
        "select_dir": "Wähle einen Zielordner aus.",
        "installing": "Installation...",
        "dsi_settings": "DSi System Settings",
        "dsi_settings_desc": "Beide DSi-System-Settings-CIA-Dateien zusammen installieren."
    },
    "pt": {
        "choose_lang": "Escolher idioma",
        "done": "Concluir",
        "intro": "Este programa instala arquivos CIA dos aplicativos de sistema do Nintendo DSi, incluindo os arquivos necessários para fazer as Configurações do Nintendo DSi funcionarem no 3DS por meio de um app .cia.",
        "back": "Voltar",
        "next": "Avançar",
        "cancel": "Cancelar",
        "mode_title": "Selecione o tipo de instalação",
        "quick": "Configuração rápida",
        "quick_desc": "Instala diretamente todos os aplicativos do sistema.",
        "custom": "Configuração personalizada",
        "custom_desc": "Escolha quais aplicativos do sistema instalar.",
        "custom_apps": "Selecione os aplicativos que deseja",
        "choose_dir": "Escolha onde salvar a pasta cia",
        "browse": "Procurar",
        "success": "Sucesso",
        "success_desc": "Os arquivos foram instalados corretamente.",
        "close": "Fechar",
        "open": "Abrir pasta",
        "select_one": "Selecione pelo menos um item.",
        "select_dir": "Selecione uma pasta de destino.",
        "installing": "Instalando...",
        "dsi_settings": "DSi System Settings",
        "dsi_settings_desc": "Instale juntos os dois arquivos CIA de DSi System Settings."
    },
    "pt_br": {
        "choose_lang": "Escolher idioma",
        "done": "Concluir",
        "intro": "Este programa instala arquivos CIA dos aplicativos de sistema do Nintendo DSi, incluindo os arquivos necessários para fazer as Configurações do Nintendo DSi funcionarem no 3DS por meio de um app .cia.",
        "back": "Voltar",
        "next": "Avançar",
        "cancel": "Cancelar",
        "mode_title": "Selecione o tipo de instalação",
        "quick": "Configuração rápida",
        "quick_desc": "Instala diretamente todos os aplicativos do sistema.",
        "custom": "Configuração personalizada",
        "custom_desc": "Escolha quais aplicativos do sistema instalar.",
        "custom_apps": "Selecione os aplicativos que deseja",
        "choose_dir": "Escolha onde salvar a pasta cia",
        "browse": "Procurar",
        "success": "Sucesso",
        "success_desc": "Os arquivos foram instalados corretamente.",
        "close": "Fechar",
        "open": "Abrir pasta",
        "select_one": "Selecione pelo menos um item.",
        "select_dir": "Selecione uma pasta de destino.",
        "installing": "Instalando...",
        "dsi_settings": "DSi System Settings",
        "dsi_settings_desc": "Instale juntos os dois arquivos CIA de DSi System Settings."
    },
    "nl": {
        "choose_lang": "Taal kiezen",
        "done": "Gereed",
        "intro": "Dit programma installeert CIA-bestanden van Nintendo DSi-systeemapps, inclusief de bestanden die nodig zijn om Nintendo DSi-instellingen op 3DS te laten werken via een .cia-app.",
        "back": "Terug",
        "next": "Volgende",
        "cancel": "Annuleren",
        "mode_title": "Selecteer installatietype",
        "quick": "Snelle installatie",
        "quick_desc": "Installeert direct alle systeemapps.",
        "custom": "Aangepaste installatie",
        "custom_desc": "Kies welke systeemapps je wilt installeren.",
        "custom_apps": "Selecteer de gewenste apps",
        "choose_dir": "Kies waar je de cia-map wilt opslaan",
        "browse": "Bladeren",
        "success": "Succes",
        "success_desc": "De bestanden zijn correct geïnstalleerd.",
        "close": "Sluiten",
        "open": "Map openen",
        "select_one": "Selecteer ten minste één item.",
        "select_dir": "Selecteer een doelmap.",
        "installing": "Installeren...",
        "dsi_settings": "DSi System Settings",
        "dsi_settings_desc": "Installeer beide DSi System Settings CIA-bestanden samen."
    },
    "ja": {
        "choose_lang": "言語を選択",
        "done": "完了",
        "intro": "このプログラムは、Nintendo DSi のシステムアプリの CIA ファイルをインストールします。3DS で Nintendo DSi の設定を .cia アプリで動作させるためのファイルも含みます。",
        "back": "戻る",
        "next": "次へ",
        "cancel": "キャンセル",
        "mode_title": "インストールの種類を選択",
        "quick": "簡易セットアップ",
        "quick_desc": "すべてのシステムアプリを直接インストールします。",
        "custom": "カスタムセットアップ",
        "custom_desc": "インストールするシステムアプリを選択します。",
        "custom_apps": "必要なアプリを選択",
        "choose_dir": "cia フォルダの保存先を選択",
        "browse": "参照",
        "success": "成功",
        "success_desc": "ファイルは正しくインストールされました。",
        "close": "閉じる",
        "open": "フォルダを開く",
        "select_one": "少なくとも1項目を選択してください。",
        "select_dir": "保存先フォルダを選択してください。",
        "installing": "インストール中...",
        "dsi_settings": "DSi System Settings",
        "dsi_settings_desc": "2つの DSi System Settings CIA をまとめてインストールします。"
    },
    "ru": {
        "choose_lang": "Выберите язык",
        "done": "Готово",
        "intro": "Эта программа устанавливает CIA-файлы системных приложений Nintendo DSi, включая файлы, необходимые для работы настроек Nintendo DSi на 3DS через .cia-приложение.",
        "back": "Назад",
        "next": "Далее",
        "cancel": "Отмена",
        "mode_title": "Выберите тип установки",
        "quick": "Быстрая установка",
        "quick_desc": "Устанавливает все системные приложения напрямую.",
        "custom": "Выборочная установка",
        "custom_desc": "Выберите, какие системные приложения установить.",
        "custom_apps": "Выберите нужные приложения",
        "choose_dir": "Выберите, куда сохранить папку cia",
        "browse": "Обзор",
        "success": "Успешно",
        "success_desc": "Файлы были установлены правильно.",
        "close": "Закрыть",
        "open": "Открыть папку",
        "select_one": "Выберите хотя бы один элемент.",
        "select_dir": "Выберите папку назначения.",
        "installing": "Установка...",
        "dsi_settings": "DSi System Settings",
        "dsi_settings_desc": "Установить оба CIA-файла DSi System Settings вместе."
    },
}

FILES = {
    "3DS Transfer Tool": "https://repo.mariocube.com/Other%20Consoles/3DS/DSi%20Apps/3DS%20Transfer%20Tool.cia",
    "DS Download Play": "https://repo.mariocube.com/Other%20Consoles/3DS/DSi%20Apps/DS%20Download%20Play%20%28Dev%29%20%28Apache%20Thunder%29.cia",
    "DSi Browser": "https://repo.mariocube.com/Other%20Consoles/3DS/DSi%20Apps/DSi%20Browser.cia",
    "DSi Camera": "https://repo.mariocube.com/Other%20Consoles/3DS/DSi%20Apps/DSi%20Camera.cia",
    "DSi Sounds": "https://repo.mariocube.com/Other%20Consoles/3DS/DSi%20Apps/DSi%20Sound.cia",
    "Pictochat": "https://repo.mariocube.com/Other%20Consoles/3DS/DSi%20Apps/PictoChat.cia",
}

DSI_SETTINGS_FILES = {
    "DSi System Settings A": "https://repo.mariocube.com/Other%20Consoles/3DS/DSi%20Apps/DSi%20System%20Settings%20%28Invisible%29%20%28Works%20After%20Modifying%20TWLN%29.cia",
    "DSi System Settings B": "https://repo.mariocube.com/Other%20Consoles/3DS/DSi%20Apps/DSi%20System%20Settings%20CTR%20Mode%20Forwarder.cia",
}

ORDERED_ITEMS = list(FILES.keys())


README_TEXTS = {
    "en": """How to put DSi System Settings on 3DS (Tutorial) - by Wii-J

1) Put the .cia files into your cia folder on your SD Card.
2) Extract the .zip file (files-for-dsi-settings.zip). There will be a “shared1” folder, move that folder to the root of your SD card. (contains someone else’s user information, however you can change the info later.)
3) Take out from the computer your SD card and turn on your 3DS.
4) Open FBI, and tap the “SD” option, and go to the cia folder or the folder where the two CIAs are located.
5) Tap “current directory” and tap “Install and Delete CIAs” (or if there are other .cia files, install both of them singularly).
6) Go back to the root of your SD card, go to the “shared1” folder on the root.
7) Copy the contents of the folder.
8) Go back to the main menu of FBI, then, select “TWL NAND”.
9) Press A when it asks you to confirm.
10) Go to “current directory” and paste the contents.

You now have the DSi System Settings on your system.

*IMPORTANT: Do not access Data Management because then it will corrupt your DS games.

Have fun with your DSi System Apps :)

John 3:16-17
16 "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.
17 For God did not send his Son into the world to condemn the world, but to save the world through him."
""",
    "it": """Come installare DSi System Settings su 3DS (Tutorial) - by Wii-J

1) Metti i file .cia nella tua cartella cia sulla SD Card.
2) Estrai il file .zip (files-for-dsi-settings.zip). Ci sarà una cartella “shared1”, sposta quella cartella nella root della tua SD card. (contiene informazioni utente di qualcun altro, ma potrai modificarle in seguito.)
3) Rimuovi la SD card dal computer e accendi la tua 3DS.
4) Apri FBI, tocca l’opzione “SD” e vai nella cartella cia o nella cartella in cui si trovano i due CIA.
5) Tocca “current directory” e tocca “Install and Delete CIAs” (oppure, se ci sono altri file .cia, installali singolarmente).
6) Torna alla root della tua SD card, vai nella cartella “shared1” nella root.
7) Copia il contenuto della cartella.
8) Torna al menu principale di FBI, poi seleziona “TWL NAND”.
9) Premi A quando viene chiesta la conferma.
10) Vai su “current directory” e incolla il contenuto.

Ora hai le DSi System Settings sul tuo sistema.

*IMPORTANTE: Non accedere a Data Management, perché corromperebbe i tuoi giochi DS.

Divertiti con le tue DSi System Apps :)

John 3:16-17
16 "Perché Dio ha tanto amato il mondo, che ha dato il suo unigenito Figlio, affinché chiunque crede in lui non perisca, ma abbia vita eterna.
17 Poiché Dio non ha mandato il Figlio nel mondo per condannare il mondo, ma perché il mondo sia salvato per mezzo di lui."
""",
    "fr": """Comment installer DSi System Settings sur 3DS (Tutoriel) - by Wii-J

1) Placez les fichiers .cia dans votre dossier cia sur votre carte SD.
2) Extrayez le fichier .zip (files-for-dsi-settings.zip). Il y aura un dossier “shared1”, déplacez ce dossier à la racine de votre carte SD. (il contient les informations utilisateur de quelqu'un d'autre, mais vous pourrez modifier les informations plus tard.)
3) Retirez la carte SD de l'ordinateur et allumez votre 3DS.
4) Ouvrez FBI, appuyez sur l'option “SD”, puis allez dans le dossier cia ou le dossier où se trouvent les deux CIAs.
5) Appuyez sur “current directory” puis sur “Install and Delete CIAs” (ou, s'il y a d'autres fichiers .cia, installez-les séparément).
6) Revenez à la racine de votre carte SD, puis ouvrez le dossier “shared1” à la racine.
7) Copiez le contenu du dossier.
8) Revenez au menu principal de FBI, puis sélectionnez “TWL NAND”.
9) Appuyez sur A lorsque la confirmation est demandée.
10) Allez dans “current directory” et collez le contenu.

Vous avez maintenant DSi System Settings sur votre système.

*IMPORTANT : N'accédez pas à Data Management, car cela corromprait vos jeux DS.

Amusez-vous avec vos applications système DSi :)

John 3:16-17
16 "Car Dieu a tant aimé le monde qu'il a donné son Fils unique, afin que quiconque croit en lui ne périsse point, mais qu'il ait la vie éternelle.
17 Car Dieu n'a pas envoyé son Fils dans le monde pour condamner le monde, mais pour que le monde soit sauvé par lui."
""",
    "es": """Cómo poner DSi System Settings en 3DS (Tutorial) - by Wii-J

1) Coloca los archivos .cia en tu carpeta cia de tu tarjeta SD.
2) Extrae el archivo .zip (files-for-dsi-settings.zip). Habrá una carpeta “shared1”, mueve esa carpeta a la raíz de tu tarjeta SD. (contiene información de usuario de otra persona, sin embargo puedes cambiarla más tarde.)
3) Saca la tarjeta SD del ordenador y enciende tu 3DS.
4) Abre FBI, toca la opción “SD” y ve a la carpeta cia o a la carpeta donde estén los dos CIAs.
5) Toca “current directory” y pulsa “Install and Delete CIAs” (o, si hay otros archivos .cia, instálalos por separado).
6) Vuelve a la raíz de tu tarjeta SD y entra en la carpeta “shared1” en la raíz.
7) Copia el contenido de la carpeta.
8) Vuelve al menú principal de FBI y selecciona “TWL NAND”.
9) Pulsa A cuando te pida confirmación.
10) Ve a “current directory” y pega el contenido.

Ahora tienes DSi System Settings en tu sistema.

*IMPORTANTE: No accedas a Data Management porque corromperá tus juegos de DS.

Diviértete con tus DSi System Apps :)

John 3:16-17
16 "Porque de tal manera amó Dios al mundo, que ha dado a su Hijo unigénito, para que todo aquel que en él cree no se pierda, mas tenga vida eterna.
17 Porque Dios no envió a su Hijo al mundo para condenar al mundo, sino para salvar al mundo por él."
""",
    "de": """Wie man DSi System Settings auf 3DS installiert (Tutorial) - by Wii-J

1) Lege die .cia-Dateien in deinen cia-Ordner auf deiner SD-Karte.
2) Entpacke die .zip-Datei (files-for-dsi-settings.zip). Es wird einen Ordner „shared1“ geben, verschiebe diesen Ordner in das Stammverzeichnis deiner SD-Karte. (Enthält Benutzerdaten einer anderen Person, diese kannst du später ändern.)
3) Nimm die SD-Karte aus dem Computer und schalte deinen 3DS ein.
4) Öffne FBI, tippe auf die Option „SD“ und gehe zum cia-Ordner oder zu dem Ordner, in dem sich die beiden CIAs befinden.
5) Tippe auf „current directory“ und dann auf „Install and Delete CIAs“ (oder installiere andere .cia-Dateien einzeln).
6) Gehe zurück zum Stammverzeichnis deiner SD-Karte und öffne dort den Ordner „shared1“.
7) Kopiere den Inhalt des Ordners.
8) Gehe zurück zum Hauptmenü von FBI und wähle „TWL NAND“.
9) Drücke A, wenn du zur Bestätigung aufgefordert wirst.
10) Gehe zu „current directory“ und füge den Inhalt ein.

Jetzt hast du DSi System Settings auf deinem System.

*WICHTIG: Greife nicht auf Data Management zu, da sonst deine DS-Spiele beschädigt werden.

Viel Spaß mit deinen DSi System Apps :)

John 3:16-17
16 "Denn so sehr hat Gott die Welt geliebt, dass er seinen eingeborenen Sohn gab, damit jeder, der an ihn glaubt, nicht verloren geht, sondern ewiges Leben hat.
17 Denn Gott hat seinen Sohn nicht in die Welt gesandt, um die Welt zu verurteilen, sondern damit die Welt durch ihn gerettet wird."
""",
    "pt": """Como colocar DSi System Settings no 3DS (Tutorial) - by Wii-J

1) Coloque os arquivos .cia na sua pasta cia no cartão SD.
2) Extraia o arquivo .zip (files-for-dsi-settings.zip). Haverá uma pasta “shared1”; mova essa pasta para a raiz do seu cartão SD. (contém informações de usuário de outra pessoa, mas você poderá alterar depois.)
3) Tire o cartão SD do computador e ligue o seu 3DS.
4) Abra o FBI, toque na opção “SD” e vá até a pasta cia ou a pasta onde os dois CIAs estão localizados.
5) Toque em “current directory” e depois em “Install and Delete CIAs” (ou, se houver outros arquivos .cia, instale-os separadamente).
6) Volte para a raiz do cartão SD e vá para a pasta “shared1” na raiz.
7) Copie o conteúdo da pasta.
8) Volte ao menu principal do FBI e selecione “TWL NAND”.
9) Pressione A quando ele pedir confirmação.
10) Vá para “current directory” e cole o conteúdo.

Agora você tem o DSi System Settings no seu sistema.

*IMPORTANTE: Não acesse Data Management, porque isso corromperá seus jogos de DS.

Divirta-se com seus DSi System Apps :)

John 3:16-17
16 "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito, para que todo aquele que nele crê não pereça, mas tenha a vida eterna.
17 Porque Deus enviou o seu Filho ao mundo não para condenar o mundo, mas para que o mundo fosse salvo por meio dele."
""",
    "pt_br": """Como colocar DSi System Settings no 3DS (Tutorial) - by Wii-J

1) Coloque os arquivos .cia na sua pasta cia no cartão SD.
2) Extraia o arquivo .zip (files-for-dsi-settings.zip). Haverá uma pasta “shared1”; mova essa pasta para a raiz do seu cartão SD. (contém informações de usuário de outra pessoa, mas você poderá alterar depois.)
3) Tire o cartão SD do computador e ligue o seu 3DS.
4) Abra o FBI, toque na opção “SD” e vá até a pasta cia ou a pasta onde os dois CIAs estão localizados.
5) Toque em “current directory” e depois em “Install and Delete CIAs” (ou, se houver outros arquivos .cia, instale-os separadamente).
6) Volte para a raiz do cartão SD e vá para a pasta “shared1” na raiz.
7) Copie o conteúdo da pasta.
8) Volte ao menu principal do FBI e selecione “TWL NAND”.
9) Pressione A quando ele pedir confirmação.
10) Vá para “current directory” e cole o conteúdo.

Agora você tem o DSi System Settings no seu sistema.

*IMPORTANTE: Não acesse Data Management, porque isso corromperá seus jogos de DS.

Divirta-se com seus DSi System Apps :)

John 3:16-17
16 "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito, para que todo aquele que nele crê não pereça, mas tenha a vida eterna.
17 Porque Deus enviou o seu Filho ao mundo não para condenar o mundo, mas para que o mundo fosse salvo por meio dele."
""",
    "nl": """Hoe je DSi System Settings op 3DS zet (Handleiding) - by Wii-J

1) Zet de .cia-bestanden in je cia-map op je SD-kaart.
2) Pak het .zip-bestand uit (files-for-dsi-settings.zip). Er komt een map “shared1”; verplaats die map naar de root van je SD-kaart. (bevat gegevens van iemand anders, maar je kunt die later aanpassen.)
3) Haal de SD-kaart uit de computer en zet je 3DS aan.
4) Open FBI, tik op de optie “SD” en ga naar de cia-map of naar de map waar de twee CIAs staan.
5) Tik op “current directory” en dan op “Install and Delete CIAs” (of installeer andere .cia-bestanden afzonderlijk).
6) Ga terug naar de root van je SD-kaart en open daar de map “shared1”.
7) Kopieer de inhoud van de map.
8) Ga terug naar het hoofdmenu van FBI en kies “TWL NAND”.
9) Druk op A wanneer om bevestiging wordt gevraagd.
10) Ga naar “current directory” en plak de inhoud.

Nu heb je DSi System Settings op je systeem.

*BELANGRIJK: Open Data Management niet, want dan raken je DS-games beschadigd.

Veel plezier met je DSi System Apps :)

John 3:16-17
16 "Want alzo lief heeft God de wereld gehad, dat Hij zijn eniggeboren Zoon heeft gegeven, opdat ieder die in Hem gelooft niet verloren gaat, maar eeuwig leven heeft.
17 Want God heeft zijn Zoon niet in de wereld gezonden om de wereld te veroordelen, maar opdat de wereld door Hem behouden zou worden."
""",
    "ja": """3DS に DSi System Settings を入れる方法 (チュートリアル) - by Wii-J

1) .cia ファイルを SD カードの cia フォルダに入れます。
2) .zip ファイル (files-for-dsi-settings.zip) を解凍します。 “shared1” フォルダがあるので、そのフォルダを SD カードのルートに移動してください。(他人のユーザー情報が含まれていますが、後で変更できます。)
3) SD カードを PC から取り外して、3DS の電源を入れます。
4) FBI を開き、“SD” を選び、cia フォルダまたは 2 つの CIA があるフォルダへ移動します。
5) “current directory” を押し、“Install and Delete CIAs” を押します。(他に .cia ファイルがある場合は、個別にインストールしてください。)
6) SD カードのルートに戻り、“shared1” フォルダを開きます。
7) フォルダの中身をコピーします。
8) FBI のメインメニューに戻り、“TWL NAND” を選びます。
9) 確認を求められたら A を押します。
10) “current directory” に移動して中身を貼り付けます。

これで DSi System Settings がシステムに追加されました。

*重要: Data Management は開かないでください。DS ゲームが壊れる可能性があります。

DSi System Apps をお楽しみください :)

John 3:16-17
16 "神は実に、そのひとり子をお与えになったほどに世を愛された。それは御子を信じる者が一人も滅びないで、永遠のいのちを持つためである。
17 神が御子を世に遣わされたのは、世をさばくためではなく、御子によって世が救われるためである。"
""",
    "ru": """Как установить DSi System Settings на 3DS (Руководство) - by Wii-J

1) Поместите файлы .cia в папку cia на вашей SD-карте.
2) Распакуйте .zip файл (files-for-dsi-settings.zip). Там будет папка “shared1”; переместите её в корень SD-карты. (Она содержит данные пользователя другого человека, но вы сможете изменить их позже.)
3) Извлеките SD-карту из компьютера и включите 3DS.
4) Откройте FBI, выберите опцию “SD” и перейдите в папку cia или в папку, где находятся два CIA.
5) Нажмите “current directory” и затем “Install and Delete CIAs” (или установите другие .cia файлы по отдельности).
6) Вернитесь в корень SD-карты и откройте папку “shared1” в корне.
7) Скопируйте содержимое папки.
8) Вернитесь в главное меню FBI и выберите “TWL NAND”.
9) Нажмите A, когда потребуется подтверждение.
10) Перейдите в “current directory” и вставьте содержимое.

Теперь у вас есть DSi System Settings в системе.

*ВАЖНО: Не открывайте Data Management, иначе это повредит ваши игры DS.

Наслаждайтесь вашими DSi System Apps :)

John 3:16-17
16 "Ибо так возлюбил Бог мир, что отдал Сына Своего Единородного, дабы всякий, верующий в Него, не погиб, но имел жизнь вечную.
17 Ибо Бог послал Сына Своего в мир не для того, чтобы судить мир, но чтобы мир был спасён через Него."
""",
}

def clean_filename(url: str) -> str:
    return unquote(Path(url.split("?")[0]).name)

def download_file(url: str, target_path: Path):
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(target_path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)

def create_readme(dest_folder: Path, lang: str):
    readme_folder = dest_folder / "cia" / "DSi System Settings files"
    readme_folder.mkdir(parents=True, exist_ok=True)
    text = README_TEXTS.get(lang, README_TEXTS["en"])
    readme_path = readme_folder / "DSi System Settings Setup - README.txt"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(text)
    return readme_path

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title(APP_TITLE)
        self.geometry("960x620")
        self.minsize(960, 620)
        self.lang = "en"
        self.install_mode = "quick"
        self.dest = ""
        self.frame = None
        self.vars = {}
        self.dsi_var = ctk.IntVar(value=1)
        self.progress_bar = None
        self.progress_label = None
        self.show_language()

    def tr(self, key):
        return T[self.lang][key]

    def clear(self):
        if self.frame:
            self.frame.destroy()
        self.frame = ctk.CTkFrame(self, corner_radius=18)
        self.frame.pack(fill="both", expand=True, padx=18, pady=18)
        return self.frame

    def nav(self, back_cmd=None, next_cmd=None, disable_back=False):
        row = ctk.CTkFrame(self.frame, fg_color="transparent")
        row.pack(side="bottom", fill="x", pady=10)
        if disable_back:
            ctk.CTkButton(row, text=self.tr("back"), state="disabled", width=120).pack(side="left", padx=10)
        else:
            ctk.CTkButton(row, text=self.tr("back"), width=120, command=back_cmd).pack(side="left", padx=10)
        ctk.CTkButton(row, text=self.tr("cancel"), width=120, fg_color="#b23b3b", hover_color="#992f2f", command=self.destroy).pack(side="right", padx=10)
        ctk.CTkButton(row, text=self.tr("next"), width=120, command=next_cmd).pack(side="right", padx=10)

    def show_language(self):
        f = self.clear()
        ctk.CTkLabel(f, text=self.tr("choose_lang"), font=ctk.CTkFont(size=30, weight="bold")).pack(pady=(60, 24))
        self.lang_menu = ctk.CTkOptionMenu(f, values=list(LANGS.keys()), width=300)
        self.lang_menu.set("English")
        self.lang_menu.pack(pady=18)
        ctk.CTkButton(f, text=self.tr("done"), width=180, command=lambda: (self.set_language(self.lang_menu.get()), self.show_intro())).pack(pady=18)

    def set_language(self, name):
        self.lang = LANGS.get(name, "en")

    def show_intro(self):
        f = self.clear()
        ctk.CTkLabel(f, text=APP_TITLE, font=ctk.CTkFont(size=30, weight="bold")).pack(pady=(30, 16))
        ctk.CTkLabel(f, text=self.tr("intro"), wraplength=820, justify="left", font=ctk.CTkFont(size=18)).pack(padx=32, pady=22)
        self.nav(disable_back=True, next_cmd=self.show_mode)

    def show_mode(self):
        f = self.clear()
        ctk.CTkLabel(f, text=self.tr("mode_title"), font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(24, 18))
        self.mode = ctk.StringVar(value="quick")
        for title, desc, value in [(self.tr("quick"), self.tr("quick_desc"), "quick"), (self.tr("custom"), self.tr("custom_desc"), "custom")]:
            card = ctk.CTkFrame(f, corner_radius=16)
            card.pack(fill="x", padx=70, pady=12)
            ctk.CTkRadioButton(card, text=title, variable=self.mode, value=value).pack(anchor="w", padx=18, pady=(14, 4))
            ctk.CTkLabel(card, text=desc, text_color="#b9c0cc").pack(anchor="w", padx=42, pady=(0, 14))
        self.nav(back_cmd=self.show_intro, next_cmd=self.after_mode)

    def after_mode(self):
        self.install_mode = self.mode.get()
        if self.install_mode == "custom":
            self.show_custom()
        else:
            self.show_directory()

    def show_custom(self):
        f = self.clear()
        ctk.CTkLabel(f, text=self.tr("custom_apps"), font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(24, 18))
        self.vars = {}
        scroll = ctk.CTkScrollableFrame(f, corner_radius=14)
        scroll.pack(fill="both", expand=True, padx=50, pady=10)
        for name in ORDERED_ITEMS:
            row = ctk.CTkFrame(scroll, corner_radius=12)
            row.pack(fill="x", padx=10, pady=8)
            var = ctk.IntVar(value=1)
            self.vars[name] = var
            ctk.CTkCheckBox(row, text=name, variable=var).pack(anchor="w", padx=16, pady=12)
        dsi_card = ctk.CTkFrame(scroll, corner_radius=12)
        dsi_card.pack(fill="x", padx=10, pady=8)
        ctk.CTkCheckBox(dsi_card, text=self.tr("dsi_settings"), variable=self.dsi_var).pack(anchor="w", padx=16, pady=(12, 2))
        ctk.CTkLabel(dsi_card, text=self.tr("dsi_settings_desc"), text_color="#b9c0cc").pack(anchor="w", padx=16, pady=(0, 12))
        self.nav(back_cmd=self.show_mode, next_cmd=self.show_directory)

    def show_directory(self):
        f = self.clear()
        ctk.CTkLabel(f, text=self.tr("choose_dir"), font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(24, 16))
        bar = ctk.CTkFrame(f, fg_color="transparent")
        bar.pack(fill="x", padx=40, pady=20)
        self.dest_var = ctk.StringVar(value=self.dest or str(Path.home()))
        ctk.CTkEntry(bar, textvariable=self.dest_var).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(bar, text=self.tr("browse"), width=120, command=self.browse_folder).pack(side="right")
        self.nav(back_cmd=self.show_mode if self.install_mode == "quick" else self.show_custom, next_cmd=self.start_install)

    def browse_folder(self):
        d = filedialog.askdirectory()
        if d:
            self.dest_var.set(d)

    def start_install(self):
        self.dest = self.dest_var.get().strip()
        if not self.dest:
            messagebox.showerror(APP_TITLE, self.tr("select_dir"))
            return
        self.show_progress()
        threading.Thread(target=self.install_worker, daemon=True).start()

    def show_progress(self):
        f = self.clear()
        ctk.CTkLabel(f, text=self.tr("installing"), font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(70, 20))
        self.progress_bar = ctk.CTkProgressBar(f, width=520)
        self.progress_bar.pack(pady=16)
        self.progress_bar.set(0.15)
        self.progress_label = ctk.CTkLabel(f, text="", font=ctk.CTkFont(size=16))
        self.progress_label.pack(pady=10)

    def get_selected_items(self):
        chosen = []
        if self.install_mode == "quick":
            chosen.extend([(k, v) for k, v in FILES.items()])
            chosen.extend([(k, v) for k, v in DSI_SETTINGS_FILES.items()])
        else:
            for name in ORDERED_ITEMS:
                if self.vars.get(name, ctk.IntVar(value=0)).get() == 1:
                    chosen.append((name, FILES[name]))
            if self.dsi_var.get() == 1:
                chosen.extend([(k, v) for k, v in DSI_SETTINGS_FILES.items()])
        return chosen

    def install_worker(self):
        try:
            chosen = self.get_selected_items()
            if not chosen:
                self.after(0, lambda: messagebox.showerror(APP_TITLE, self.tr("select_one")))
                return

            base = Path(self.dest) / "cia"
            base.mkdir(parents=True, exist_ok=True)
            dsi_folder = base / "DSi System Settings files"
            dsi_folder.mkdir(parents=True, exist_ok=True)

            total = len(chosen)
            for idx, (name, url) in enumerate(chosen, start=1):
                if name in DSI_SETTINGS_FILES:
                    target = dsi_folder / clean_filename(url)
                else:
                    target = base / clean_filename(url)
                self.after(0, lambda n=name, i=idx, t=total: self.update_progress(n, i, t))
                download_file(url, target)

            create_readme(Path(self.dest), self.lang)
            self.after(0, self.show_success)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror(APP_TITLE, str(e)))

    def update_progress(self, name, idx, total):
        if self.progress_bar:
            self.progress_bar.set((idx - 1) / total)
        if self.progress_label:
            self.progress_label.configure(text=f"{name} ({idx}/{total})")

    def show_success(self):
        f = self.clear()
        ctk.CTkLabel(f, text=self.tr("success"), font=ctk.CTkFont(size=30, weight="bold")).pack(pady=(60, 12))
        ctk.CTkLabel(f, text=self.tr("success_desc"), font=ctk.CTkFont(size=18)).pack(pady=12)
        row = ctk.CTkFrame(f, fg_color="transparent")
        row.pack(pady=30)
        ctk.CTkButton(row, text=self.tr("close"), width=180, command=self.destroy).pack(side="left", padx=10)
        ctk.CTkButton(row, text=self.tr("open"), width=180, command=lambda: (os.startfile(str(Path(self.dest) / "cia")), self.destroy())).pack(side="left", padx=10)


if __name__ == "__main__":
    App().mainloop()