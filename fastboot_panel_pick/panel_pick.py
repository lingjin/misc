# requires Python 3.5+ and tested on Windows 10
# please put device on fastboot mode
import subprocess
import colorama
from colorama import Fore, Back, Style

def get_cid():
    byte_cid = subprocess.check_output(['fastboot', 'getvar', 'cid'], stderr=subprocess.STDOUT)
    string_cid = byte_cid.decode(encoding='UTF-8')
    str_cid = string_cid.split('cid: ')[1].split('\r\n')[0]
    return str_cid

def flash_bootloader(bootloader_name):
    subprocess.run(['fastboot', 'flash', 'bootloader', bootloader_name])
    subprocess.run(['fastboot', 'reboot-bootloader'])
    return 

def get_primary_display():
    byte_primary_display = subprocess.check_output(['fastboot', 'getvar', 'primary-display'], stderr=subprocess.STDOUT)
    string_primary_display = byte_primary_display.decode(encoding='UTF-8')
    str_primary_display = string_primary_display.split('primary-display: ')[1].split('\r\n')[0]
    return str_primary_display

def main():
    str_cid = get_cid()
    print('CID is', str_cid)

    if str_cid == '0x0001' : # ATT
        bridge_bootloader_name = 'bridge_bootloader_QPS30.205-Q3-87_att_cid1.img'
        ta_bootloader_name = 'ta_bootloader_QPS30.205-Q3-43-16-3R1_att_cid1.img'
    elif str_cid == '0x0021' or str_cid == '0x0015' : # TMO
        bridge_bootloader_name = 'bridge_bootloader_QPS30.205-Q3-87_tmo_cid21.img'
        ta_bootloader_name = 'ta_bootloader_QPS30.205-Q3-43-16-2R2_tmo_cid21.img'
    else :
        print('Unexpected CID, Quit!')
        return

    print('Start flashing bridge bootloader...', bridge_bootloader_name)
    flash_bootloader(bridge_bootloader_name)

    print('Detecting primary display...')
    str_display = get_primary_display()
    print('Display is', str_display)

    print('Start flashing original TA bootloader...', ta_bootloader_name)
    flash_bootloader(ta_bootloader_name)
    
    print()
    colorama.init()
    
    if str_display == 'csot_620_876x2142_cmd_display_v3' : # CSOT V3
        print(Fore.GREEN + 'Congratulations, display is CSOT v3 panel ' + Style.RESET_ALL + str_display)
    elif str_display == 'csot_620_876x2142_cmd_display_v2' : # CSOT V2
        print(Fore.RED + 'WARNING: display is CSOT v2 (old) panel ' + Style.RESET_ALL + str_display)
    else : 
        print(Fore.RED + 'WARNING: unknown display panel ' + Style.RESET_ALL + str_display)

    return

if __name__ == '__main__':
    main()