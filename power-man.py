import subprocess
import os

result = subprocess.run(['powerprofilesctl', 'list'], capture_output=True, text=True)
actual = subprocess.run(['powerprofilesctl', 'get'], capture_output=True, text=True).stdout.strip()

parsed = result.stdout.split("\n")

def clean(text: str) -> str:
    clean = text.replace(":", "").replace("*", "").strip()
    return clean

options = [clean(parsed[i]) for i in [0, 5, 9]] 

options_with_indicator = [f"* {option}" if option == actual else option for option in options]

zenity_options = " ".join([f"'{option}'" for option in options_with_indicator])  

command = f"zenity --list --title='Seleziona Profilo di Potenza' --text='Scegli un profilo:' --column='Profili' {zenity_options}"

selected_option = subprocess.run(command, shell=True, capture_output=True, text=True)

if selected_option.returncode == 0:
    parsed_option = selected_option.stdout.strip().replace("*", "").strip()  

    if parsed_option != actual:
        os.system(f"powerprofilesctl set {parsed_option}")
        print(f"Set to {parsed_option}")

