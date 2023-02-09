import colorama
import libfilehash
import libgpt as gpt3
import lief
import logger
import sys
import os

from colorama import Fore, Style
from time import gmtime, strftime
from random import randint

# Initialize colorama with fixes for print()
colorama.init(autoreset=True)

# Log this session
log_name = strftime("%Y-%m-%d_%H:%M:%S_session_") + str(randint(1000,9999)) + '_artifacts.txt'
log = logger.log(log_name)

def print_banner():                              
        print("""                                
███╗   ███╗ █████╗ ██████╗ ██████╗ 
████╗ ████║██╔══██╗██╔══██╗██╔══██╗
██╔████╔██║███████║██████╔╝██████╔╝
██║╚██╔╝██║██╔══██║██╔══██╗██╔═══╝ 
██║ ╚═╝ ██║██║  ██║██████╔╝██║     
╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝     
Malware Analysis Bot Platform v0.1
        """)

def get_hashes(binary):
    hashes = libfilehash.HashHelper(binary)
    artifact = hashes.provide_hashes(hashes.hash_list)

    log.info(artifact)
    for hash_val in artifact:
        print(hash_val)

    return hashes

def get_headers(binary):
    """ Retrieve various binary headers """
    headers = []
    headers.append(f'{Fore.GREEN}[+] PE Header\n{Style.RESET_ALL}{binary.header}')
    headers.append(f'{Fore.GREEN}[+] DOS Header\n{Style.RESET_ALL}{binary.dos_header}')
    headers.append(f'{Fore.GREEN}[+] Image Optional Header\n{Style.RESET_ALL}{binary.optional_header}')
    for artifact in headers:
        log.info(artifact)
    return headers

def get_sections(binary):
    """ Retrieve PE sections """
    sections = {}
    for section in binary.sections:
        sections[section.name] = section.size
    for artifact in sections:
        log.info(artifact)
    return sections

def get_iat(binary):
    """ Populate a dictionary with all imports """
    iat = {}
    for imported_library in binary.imports:
        if imported_library.name == "KERNEL32.dll":
            for function_name in imported_library.entries:
                if not function_name.is_ordinal:
                    import_name = function_name.name
                    iat[import_name] = imported_library.name

    log.info(iat)
    
    if bool(iat) == False:
        no_iat_detected()

    return iat

def no_iat_detected():
    print(gpt3.query("I just analyzed a sample that did not appear to have any imports. What happened?"))
    return

def check_iat(iat_entries):
    """ Parses IAT entries, and runs winapis through GPT3 for analysis"""
    
    winapi_stack = []
    for i in iat_entries:
        winapi_stack.append(i)

    result = gpt3.query(f'I have a sample with these imports: {winapi_stack}. Are any of these common?')

    log.info(result)

    return result

def get_file():
    binpath = input("Enter file path: ")
    binpath = os.path.abspath(binpath)

    print(f'{Fore.GREEN}[+] File Hashes{Style.RESET_ALL}')

    get_hashes(binpath)
    print()

    with open(binpath, 'rb') as f:
        binobj = f.read()
    
    binary = lief.parse(binobj)
    
    return binary

def learn():
    print(gpt3.query("Provide a random, but detailed technical tip about the malware analysis process, techniques, or tools."))

def clear_screen():
    os.system("clear")

def print_help():
        help_msg = "\nAvailable commands:\n\n"
        help_msg += "- banner       Display ASCII art\n"
        help_msg += "- analyze_file Analyze a binary\n"
        help_msg += "- make_yara    Generate Yara rules\n"
        help_msg += "- clear        Clear terminal\n"
        help_msg += "- help         Display this menu\n"
        help_msg += "- quit         Exit the script\n"
        help_msg += "- exit         If you forget quit\n\n"
        print(f"{help_msg}")

def broker_analyze():
    binary = get_file()
    analyze_file(binary)

def broker_yara():
    sample_filename = input('Sample filename: ')
    sample_hash = input('Sample hash: ')
    sample_winapis = input('Suspicious Winapis: ')

    result = gpt3.query(f"Generate a yara rule to alert on the filename {sample_filename} and hash {sample_hash} with winapis {sample_winapis}")
    log.info(result)
    print(result)

def analyze_file(binary):
    """ Analyze the binary """
    headers = get_headers(binary)
    for header in headers:
        print(header)

    print(f'{Fore.GREEN}[+] Sections:\n{Style.RESET_ALL}{get_sections(binary)}')
    print(f'\n{Fore.GREEN}[+] Import Address Table:{Style.RESET_ALL}')

    iat_entries = get_iat(binary)
    for i in iat_entries:
        print(f"{iat_entries[i]}:{i}")

    choice = input(f"\n{Fore.GREEN}Check GPT-3 for suspicious IAT? (Y/N) {Style.RESET_ALL}")
    if choice in ('y','Y'):
        print(check_iat(iat_entries))
        print('\n[!] Basic Yara rules for this sample can be prompted via the `make_yara` command.')
        return
    if choice in ('n','N'):
        return

def main():
        commands = {
                "banner": print_banner,
                "learn": learn,
                "analyze_file": broker_analyze,
                "make_yara": broker_yara,
                "clear": clear_screen,
                "help": print_help,
                "quit": sys.exit,
                "exit": sys.exit # for me :(
        }

        while True:
                try:
                        prompt = input(f'{Fore.GREEN}Input>{Style.RESET_ALL} ')
                        command = None

                        for key in commands:
                                if key == prompt:
                                        command = commands[key]
                                        break

                        if command:
                                command()
                        else:
                                answer = gpt3.query(prompt)
                                print(answer)

                except Exception as e:
                        print(repr(e))

if __name__ == "__main__":
        print_banner()
        print(f'Log file for this session: {log_name}')
        main()