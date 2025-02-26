import os
import time
from colorama import init, Fore, Style


init(autoreset=True)


MUSIC_DIR = r"music"  
OUTPUT_FILE = "soundevents_roundendsound.vsndevts"  
BASE_CONFIG_NAME = "roundendsound.base"


base_config = {
    "type": "csgo_music",
    "priority": 5.0,
    "stop_music": "true",
    "volume_fade_out_input_max": 1.6,
    "loop_track": "false",
    "should_queue_track": "true",
    "block_won_lost": "true",
    "startpoint_01": 0.0,
    "startpoint_02": 0.0,
    "startpoint_03": 0.0,
    "endpoint_01": 0.0,
    "endpoint_02": 0.0,
    "endpoint_03": 0.0,
    "syncpoints_01": [0.0],
    "syncpoints_02": [0.0],
    "syncpoints_03": [0.0]
}


def write_base_config(f):
    f.write(f'    {BASE_CONFIG_NAME} =\n')
    f.write('    {\n')
    for key, value in base_config.items():
        if isinstance(value, list):
            f.write(f'        {key} = \n        [\n')
            for item in value:
                f.write(f'            {item},\n')
            f.write('        ]\n')
        elif isinstance(value, str):
            f.write(f'        {key} = "{value}"\n')
        else:
            f.write(f'        {key} = {value}\n')
    f.write('    }\n\n')


def animated_progress(total, current, bar_length=30):
    progress = current / total
    filled_length = int(bar_length * progress)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    percentage = f"{progress * 100:.1f}%"
    return f"{Fore.CYAN}[{bar}] {Fore.MAGENTA}{percentage}"


def write_pulse_configs(music_dir, f):
    
    mp3_files = [file for file in os.listdir(music_dir) if file.lower().endswith(".mp3")]
    total_files = len(mp3_files)
    
    print(Fore.YELLOW + "Начинаем обработку песен...")
    for pulse_number, mp3_file in enumerate(mp3_files, start=1):
        vsnd_name = f"{pulse_number}_pulse"
        vsnd_file = f"sounds/music/{vsnd_name}.vsnd"
        
        
        print(f"\r{animated_progress(total_files, pulse_number)}", end="")
        time.sleep(0.1)  
        
        
        for volume_level in range(10, 0, -1):  
            volume = round(volume_level * 0.1, 1)
            key = f"pulse{pulse_number}.{11 - volume_level}"  
            f.write(f'    {key} =\n')
            f.write('    {\n')
            f.write(f'        base = "{BASE_CONFIG_NAME}"\n')
            f.write(f'        vsnd_files = "{vsnd_file}"\n')
            f.write(f'        volume = {volume:.6f}\n')  
            f.write('    }\n\n')
    
    print("\n" + Fore.GREEN + "Обработка завершена!")


def main():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write('{\n')
        
        
        write_base_config(f)
        
        
        write_pulse_configs(MUSIC_DIR, f)
        
        f.write('}\n')
    
    print(Fore.CYAN + f"Конфигурация успешно создана и сохранена в {OUTPUT_FILE}")

if __name__ == "__main__":
    main()