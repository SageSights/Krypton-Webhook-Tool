import threading
import requests
from pystyle import Colors, Colorate, Center
import time
import os
import webbrowser
import base64
from tkinter import filedialog as fd

# colors because I cannot remember to change it everytime

black = "\033[1;30m"
titletext = " [-- Krypton --]"
red = "\033[1;31m"
green = "\033[1;32m"
blue = "\033[1;33m"
blue = "\033[1;34m"
purple = "\033[1;35m"
cyan = "\033[1;36m"
white = "\033[1;37m"
invalidurl = f"{red}[!]{white} Invalid url!"
# test = "" test webhook, dont forget to remove :3

socials = {
    "github": {"link": "https://github.com/SageSights"},
}  # You can update this list, and it will dynamically update.

logo = """
▄ •▄ ▄▄▄   ▄· ▄▌ ▄▄▄·▄▄▄▄▄       ▐ ▄ 
█▌▄▌▪▀▄ █·▐█▪██▌▐█ ▄█•██  ▪     •█▌▐█
▐▀▀▄·▐▀▀▄ ▐█▌▐█▪ ██▀· ▐█.▪ ▄█▀▄ ▐█▐▐▌
▐█.█▌▐█•█▌ ▐█▀·.▐█▪·• ▐█▌·▐█▌.▐▌██▐█▌
·▀  ▀.▀  ▀  ▀ • .▀    ▀▀▀  ▀█▄▀▪▀▀ █▪
"""

for platform, info in socials.items():
    link = info["link"].replace("https://", "")
    logo += f"      > [{platform.capitalize()}]: {link}\n"

logo = Center.XCenter(logo)


def choice():
    print(Center.XCenter("""
[1] Webhook Information
[2] Rename Webhook
[3] Change pfp
[4] Spam Webhook
[5] Send Message
[6] Delete Webhook
[0] Log Out
"""))


def printascii():
    print(Colorate.Horizontal(Colors.cyan_to_green, logo, 1))


def clear():
    os.system(
        'clear' if os.name != 'nt' else 'cls')  # should be a better one-liner, because let's be real if its unsupported they are on some next wacky shit
    # if os.name == 'posix':  # Unix/Linux/MacOS
    #     os.system('clear')
    # elif os.name == 'nt':  # Windows
    #     os.system('cls')
    # else:
    #     print("Unsupported operating system")
    #     raise SystemExit


def pause(text: str = None):
    if text:
        print(text)
    os.system(
        'read -n 1 -s -r -p ""' if os.name != 'nt' else 'pause >nul')  # should be a better one-liner, because let's be real if its unsupported they are on some next wacky shit
    # if os.name == 'posix':  # Unix/Linux/macOS
    #     os.system('read -n 1 -s -r -p ""')
    # elif os.name == 'nt':  # Windows
    #     os.system('pause >nul')
    # else:
    #     print("Unsupported operating system")
    #     raise SystemExit


def intromenu():
    clear()
    printascii()
    choice()

# Options start here

# '''
# # might make this idk or might remove it
# def sendembed(url):
#     tit = input(f"{blue}[+]{white}Title for the embed: ")
#     des = input(f"{blue}[+]{white}Description: ")
#     color = input(f"{blue}[+]{white}Hex-Color: ")
#     colormain = f"0x{color}"
#     embed = discord.Embed(title=tit, description=des, color=colormain)
#     requests.post(url,json={"embed":embed})
# '''

def changepfp(url):
    input(f"{blue}[+]{white} Press enter to select file or skip this to input the path/url")
    image_path = fd.askopenfilename(filetypes=[("Profile Pictures", "*.png;*.jpg;*.jpeg")])
    if image_path is None or image_path == "":
        clear()
        image_path = input(f"{blue}[+]{white} Path/URL to image: ")
    
    try:
        if image_path.startswith(('http://', 'https://')):
            response = requests.get(image_path)
            response.raise_for_status()
            encoded_image = base64.b64encode(response.content).decode('utf-8')
        else:
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        data = {
            "avatar": f"data:image/jpeg;base64,{encoded_image}"
        }
        response = requests.patch(url, json=data)
        response.raise_for_status()
        print(f"{green}[+]{white} Profile picture changed successfully.")
    except FileNotFoundError:
        print(f"{red}[!] File not found. Please provide a valid file path or image url.")
    except requests.exceptions.HTTPError as errh:
        print(f"{red}[!] HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"{red}[!] Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"{red}[!] Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"{red}[!] Request Exception: {err}")

def deletehook(url):
    print(f"{cyan}[+]{white} Trying to delete webhook...")
    try:
        response = requests.delete(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        print(f"{green}[+]{white} Webhook deleted successfully.")
    except requests.exceptions.HTTPError as errh:
        print(f"{red}[!] HTTP Error: {errh}")

    except requests.exceptions.ConnectionError as errc:
        print(f"{red}[!] Error Connecting: {errc}")

    except requests.exceptions.Timeout as errt:
        print(f"{red}[!] Timeout Error: {errt}")

    except requests.exceptions.RequestException as err:
        print(f"{red}[!] Request Exception: {err}")

def sendmessage(url):
    msg = input(f"{blue}[+]{white} Message: ")
    try:
        response = requests.post(url, json={"content": msg})
        response.raise_for_status()
        print(f"{green}[+]{white} Message sent successfully.")

    except requests.exceptions.HTTPError as errh:
        print(f"{red}[!] HTTP Error: {errh}")

    except requests.exceptions.ConnectionError as errc:
        print(f"{red}[!] Error Connecting: {errc}")

    except requests.exceptions.Timeout as errt:
        print(f"{red}[!] Timeout Error: {errt}")

    except requests.exceptions.RequestException as err:
        print(f"{red}[!] Request Exception: {err}")

def renamehook(url):
    name = input(f"{blue}[+]{white} Webhook Name: ")
    print(f"{cyan}[+]{white} Trying to change username...")
    try:
        response = requests.patch(url, json={"name": name})
        response.raise_for_status()
        print(f"{green}[+]{white} Webhook name changed successfully.")

    except requests.exceptions.HTTPError as errh:
        print(f"{red}[!] HTTP Error: {errh}")

    except requests.exceptions.ConnectionError as errc:
        print(f"{red}[!] Error Connecting: {errc}")

    except requests.exceptions.Timeout as errt:
        print(f"{red}[!] Timeout Error: {errt}")

    except requests.exceptions.RequestException as err:
        print(f"{red}[!] Request Exception: {err}")

def spamhook(url):
    print(f"{cyan}[+]{white} Trying to spam webhook...")
    msg = input(f"{blue}[+]{white} Spam Text: ")
    timeout = float(input(f"{blue}[+]{white} Timeout (to avoid api-ratelimit): "))
    try:
        print(f"{red}[!] Spam has started, Relaunch the tool to stop spam and use it again.")
        while True:
            response = requests.post(url, json={"content": msg})
            response.raise_for_status()
            print(f"{green}[+]{white} Sent message")
            time.sleep(timeout)
    except requests.exceptions.HTTPError as errh:
        print(f"{red}[!] HTTP Error: {errh}")

    except requests.exceptions.ConnectionError as errc:
        print(f"{red}[!] Error Connecting: {errc}")

    except requests.exceptions.Timeout as errt:
        print(f"{red}[!] Timeout Error: {errt}")

    except requests.exceptions.RequestException as err:
        print(f"{red}[!] Request Exception: {err}")

webhook = {}
os.system("Krypton")
while True:
    clear()
    printascii()
    while True:
        try:
            url = input(f"{cyan}[>]{white} url: ")
            response = requests.get(url)
            if response.status_code == 200:
                webhook = response.json()
                break
            else:
                print(f"[{response.status_code}]: Invalid Webhook")
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                raise SystemExit
            print("Invalid Webhook")
    while True:
        intromenu()
        webhook_name = webhook["name"]
        print(f"\n\n\n{green}[+]{white} Logged into webhook: {webhook_name}")
        ch = int(input(f"{cyan}[>]{white} --> "))
        if ch == 5:
            clear()
            sendmessage(url)
            pause("Press any key to return to menu...")
        elif ch == 6:
            clear()
            deletehook(url)
            pause("Press any key to return to menu...")
        elif ch == 2:
            clear()
            renamehook(url)
            pause("Press any key to return to menu...")
        elif ch == 4:
            clear()
            spamhook(url)
            pause("Press any key to return to menu...")
        elif ch == 1:
            if webhook["application_id"]:
                print("Application ID: {}".format(webhook["application_id"]))
            print("Server Information\n    Guild ID: {}\n    Channel ID: {}".format(webhook["guild_id"], webhook["channel_id"]))
            print("Webhook Information\n    Webhook ID: {}\n    Name: {}\n    Type: {}\n    Token: {}".format(webhook["id"], webhook["name"], webhook["type"], webhook["token"]))
            user = webhook["user"]
            print("User Information (Creator)\n    Username: {}\n    User ID: {}".format(user["username"] + "#" + user["discriminator"], user["id"]))
            pause("\nPress any key to return to menu...")
        elif ch == 0:
            os.system("title Logging out...")
            print("Logging out, please wait..")
            break
        
        elif ch == 3:
            clear()
            changepfp(url)
            pause("Press any key to return to menu...")