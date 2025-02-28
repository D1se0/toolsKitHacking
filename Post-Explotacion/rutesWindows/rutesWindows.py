import os
import argparse
import re
from colorama import Fore, Style, init
import readline

# Inicializar colorama
init(autoreset=True)

# Ruta a la carpeta con los archivos .txt
DIRECTORY = "./rutesTXT"

# Comandos disponibles en la shell interactiva
COMMANDS = ["all", "section", "info", "os", "name", "clear", "exit"]

# Banner
BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}
███████╗██╗   ██╗████████╗███████╗███████╗██╗    ██╗██╗███╗   ██╗██████╗ ███████╗
██╔════╝██║   ██║╚══██╔══╝██╔════╝██╔════╝██║    ██║██║████╗  ██║██╔══██╗██╔════╝
███████╗██║   ██║   ██║   █████╗  █████╗  ██║ █╗ ██║██║██╔██╗ ██║██████╔╝███████╗
╚════██║██║   ██║   ██║   ██╔══╝  ██╔══╝  ██║███╗██║██║██║╚██╗██║██╔═══╝ ╚════██║
███████║╚██████╔╝   ██║   ███████╗███████╗╚███╔███╔╝██║██║ ╚████║██║     ███████║
╚══════╝ ╚═════╝    ╚═╝   ╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝     ╚══════╝
{Fore.YELLOW}{Style.BRIGHT}         === Tool to Filter and Display Windows Routes v1.0(d1se0)===
"""

# Auto-completar en la shell interactiva
def completer(text, state):
    options = [cmd for cmd in COMMANDS if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    return None

readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

def parse_file(content):
    section_match = re.search(r"Section:\s*(.+)", content)
    section_name = section_match.group(1).strip() if section_match else "Unknown Section"

    entry_blocks = re.split(r"(?=Name:)", content)
    entries = []

    for block in entry_blocks:
        name_match = re.search(r"Name:\s*(.+)", block)
        if name_match:
            entry = {"Name": name_match.group(1).strip()}
            description_match = re.search(r"Description:\s*(.*?)\n(?=Location:|Interpretation:|Name:|$)", block, re.S)
            entry["Description"] = description_match.group(1).strip() if description_match else "No Description Found"

            location_match = re.search(r"Location:\s*(.*?)\n(?=Interpretation:|Name:|$)", block, re.S)
            entry["Location"] = location_match.group(1).strip() if location_match else "No Location Found"

            interpretation_match = re.search(r"Interpretation:\s*(.*)", block, re.S)
            entry["Interpretation"] = interpretation_match.group(1).strip() if interpretation_match else "No Interpretation Found"

            entries.append(entry)

    return section_name, entries

def list_sections(directory):
    sections = set()
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                section_name, _ = parse_file(content)
                sections.add(section_name)
    return sorted(sections)

def filter_and_display(section_name, entries, show_all=False, filter_section=None, filter_name=None, filter_os=None):
    output = []

    if filter_section and filter_section.lower() != section_name.lower():
        return ""

    if filter_section:
        output.append(f"{Fore.MAGENTA}{Style.BRIGHT}=== Section: {section_name} ==={Style.RESET_ALL}")

    for entry in entries:
        if filter_name and filter_name.lower() != entry["Name"].lower():
            continue
        if filter_os and filter_os.lower() not in entry["Location"].lower():
            continue

        if filter_section:
            output.append(f"{Fore.YELLOW}{'-' * 50}{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}🔹 Name: {entry['Name']}")
        output.append(f"{Fore.CYAN}📝 Description:\n{entry['Description']}")
        output.append(f"{Fore.BLUE}📂 Location:\n{entry['Location']}")

        if show_all:
            output.append(f"{Fore.RED}📊 Interpretation:\n{entry['Interpretation']}")

        output.append(f"{Fore.YELLOW}{'-' * 50}{Style.RESET_ALL}")

    return "\n".join(output)

def interactive_shell():
    print(BANNER)
    print(f"{Fore.CYAN}Entering interactive shell. Type 'exit' to quit.{Style.RESET_ALL}")
    while True:
        try:
            command = input(f"{Fore.GREEN}{Style.BRIGHT}RW> {Style.RESET_ALL}")
        except KeyboardInterrupt:
            print("\n")
            continue

        if command == "exit":
            confirm = input(f"{Fore.RED}Are you sure you want to exit? (y/n): {Style.RESET_ALL}")
            if confirm.lower() == "y":
                print(f"{Fore.CYAN}Exiting... Goodbye!{Style.RESET_ALL}")
                break
        elif command == "clear":
            os.system("clear")
        elif command == "info":
            sections = list_sections(DIRECTORY)
            print(f"{Fore.CYAN}{Style.BRIGHT}\nAvailable Sections:{Style.RESET_ALL}")
            for section in sections:
                print(f" - {Fore.GREEN}{section}")
        elif command.startswith("section"):
            _, section_name = command.split(maxsplit=1)
            for filename in os.listdir(DIRECTORY):
                if filename.endswith(".txt"):
                    file_path = os.path.join(DIRECTORY, filename)
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                        section_name_file, entries = parse_file(content)
                        result = filter_and_display(section_name_file, entries, filter_section=section_name)
                        if result.strip():
                            print(f"\n{Fore.MAGENTA}{'=' * 10} {filename} {'=' * 10}{Style.RESET_ALL}\n")
                            print(result)
        elif command == "all":
            for filename in os.listdir(DIRECTORY):
                if filename.endswith(".txt"):
                    file_path = os.path.join(DIRECTORY, filename)
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                        section_name, entries = parse_file(content)
                        result = filter_and_display(section_name, entries, show_all=True)
                        if result.strip():
                            print(f"\n{Fore.MAGENTA}{'=' * 10} {filename} {'=' * 10}{Style.RESET_ALL}\n")
                            print(result)
        else:
            print(f"{Fore.RED}Invalid command. Type 'info' to see available commands.{Style.RESET_ALL}")

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="Filter and display information from structured files.")
    parser.add_argument("--section", help="Filter by specific section.", default=None)
    parser.add_argument("--name", help="Filter by specific name.", default=None)
    parser.add_argument("--os", help="Filter by operating system in Location.", default=None)
    parser.add_argument("--all", help="Show all information.", action="store_true")
    parser.add_argument("--info", help="Show available sections.", action="store_true")
    parser.add_argument("--shell", help="Enter interactive shell.", action="store_true")

    args = parser.parse_args()

    if not os.path.isdir(DIRECTORY):
        print(f"{Fore.RED}❌ The folder {DIRECTORY} does not exist. Please create it and add .txt files.{Style.RESET_ALL}")
        return

    if args.shell:
        interactive_shell()
        return

    if args.info:
        sections = list_sections(DIRECTORY)
        print(f"{Fore.CYAN}{Style.BRIGHT}\nAvailable Sections:{Style.RESET_ALL}")
        for section in sections:
            print(f" - {Fore.GREEN}{section}")
        return

    files_processed = 0
    for filename in os.listdir(DIRECTORY):
        if filename.endswith(".txt"):
            file_path = os.path.join(DIRECTORY, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                section_name, entries = parse_file(content)
                result = filter_and_display(
                    section_name,
                    entries,
                    show_all=args.all,
                    filter_section=args.section,
                    filter_name=args.name,
                    filter_os=args.os,
                )
                if result.strip():
                    print(f"\n{Fore.MAGENTA}{'=' * 10} {filename} {'=' * 10}{Style.RESET_ALL}\n")
                    print(result)
                    files_processed += 1

    if files_processed == 0:
        print(f"{Fore.YELLOW}⚠ No results found with the applied filters in the available files.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
