import dns.resolver

def check_cname(subdomain):
    try:
        answers = dns.resolver.resolve(subdomain, 'CNAME')
        for rdata in answers:
            cname = str(rdata.target).lower()
            if 'ec2' in cname:
                print(f"[!] Potential takeover risk: {subdomain} → {cname}")
    except dns.resolver.NoAnswer:
        print(f"[-] No CNAME found for {subdomain}")
    except dns.resolver.NXDOMAIN:
        print(f"[X] {subdomain} does not exist")
    except dns.exception.DNSException as e:
        print(f"[Error] {subdomain}: {e}")

def main():
    input_file = "subdomains.txt"  # Read from file in repository

    try:
        with open(input_file, "r") as file:
            subdomains = file.read().splitlines()

        if not subdomains:
            print("[Error] No subdomains found in the file.")
            return

        print(f"Checking {len(subdomains)} subdomains...")
        for subdomain in subdomains:
            check_cname(subdomain.strip())

    except FileNotFoundError:
        print(f"[Error] File '{input_file}' not found.")

if __name__ == "__main__":
    main()
