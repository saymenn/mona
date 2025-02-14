import os
import sys
import time

base_path = os.getcwd()


def new_sub(domain):
    try:
        new_sub_path = base_path + "/" + domain
        os.mkdir(new_sub_path)
        os.system(f"subfinder -d {domain} -all -o {new_sub_path}/{domain}")
    except Exception as err:
        print("[-] ERROR at new_sub func", err)
        sys.exit(0)

def monitor(domain):
    domain_path = base_path + "/" + domain + "/" + domain
    if os.path.exists(domain_path):
        try:
            os.system(f"subfinder -d {domain} -all | anew {domain_path} | /root/go/bin/httpx -timeout 30 -p 80,443,8080,8443,3000,10000,9443 -sc -title -td -location | notify -pc ~/.config/notify/provider-config.yaml -bulk")
        except Exception as err:
            print("[-] ERROR at the monitor func ", err)
            sys.exit(0)
    else:
        print("[-] FATAL monitor trying to load a non existent path")
        sys.exit(0)


def main():
    root_domains = base_path + "/" + "root_domains.txt"
    if os.path.exists(root_domains):
        with open(root_domains, 'r') as roots_file:
            for root in roots_file:
                root = root.strip()
                root_path = base_path + "/" + root
                if not os.path.exists(root_path):
                    new_sub(root)
                else:
                    monitor(root)
    else:
        print("[-] No root_domains.txt file exiting ...")
        sys.exit(0)


while True:
    main()
    print("[+] ==> The script is currently done until the next attempt ...")
    time.sleep(21600)
