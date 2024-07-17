# Crimping and Taping Operation Training Simulators

This repository contains the code for the crimping and taping operation training simulators. The code for each application is in the Python files, while the Arduino code is in the `project_01` folder.

## Important Notes

### Changing Machines
When switching machines, the code may no longer run because the COM port the Arduino connects to might be different. To resolve this:

1. Open the Device Manager on the new machine.
2. Expand the "COM & LPT" ports section.
3. Identify the COM port number the Arduino connects to (e.g., COM6).
4. Open the application Python file (`crimping.py` or `taping.py`).
5. Change the port number at the top of the file to the identified COM port number.

### Creating an Executable File

1. Install the `pyinstaller` Python module by running the following command:
    ```bash
    pip install pyinstaller
    ```
2. Navigate to the application directory:
    ```bash
    cd path/to/app_directory
    ```
3. Run the following command in the command prompt to create an executable file:
    ```bash
    pyinstaller.exe --onefile <chosen_application>.py
    ```
4. This will create a collection of files. The executable application will be located in the `dist` folder.
5. Move the executable application to the same directory as the `assets` folder.
6. The application is now ready to be moved to the chosen machine.

---

# Simulateurs de formation pour les opérations de sertissage et de rubanage

Ce dépôt contient le code pour les simulateurs de formation pour les opérations de sertissage et de rubanage. Le code de chaque application se trouve dans les fichiers Python, tandis que le code Arduino est dans le dossier `project_01`.

## Notes importantes

### Changement de machines
Lors du changement de machines, il est possible que le code ne fonctionne plus car le port COM auquel l'Arduino se connecte pourrait être différent. Pour résoudre ce problème :

1. Ouvrez le Gestionnaire de périphériques sur la nouvelle machine.
2. Développez la section des ports "COM & LPT".
3. Identifiez le numéro de port COM auquel l'Arduino se connecte (par exemple, COM6).
4. Ouvrez le fichier Python de l'application (`crimping.py` ou `taping.py`).
5. Changez le numéro de port en haut du fichier avec le numéro de port COM identifié.

### Création d'un fichier exécutable

1. Installez le module Python `pyinstaller` en exécutant la commande suivante :
    ```bash
    pip install pyinstaller
    ```
2. Naviguez vers le répertoire de l'application :
    ```bash
    cd chemin/vers/le_dossier_de_l'application
    ```
3. Exécutez la commande suivante dans l'invite de commande pour créer un fichier exécutable :
    ```bash
    pyinstaller.exe --onefile <chosen_application>.py
    ```
4. Cela créera une collection de fichiers. L'application exécutable se trouvera dans le dossier `dist`.
5. Déplacez l'application exécutable dans le même répertoire que le dossier `assets`.
6. L'application est maintenant prête à être déplacée vers la machine choisie.
