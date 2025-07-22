from pyfiglet import Figlet
import requests
import concurrent.futures
from datetime import datetime
import sys
import time
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# ========================
#      CONFIGURATION
# ========================
THREADS = 30  # Extreme performance
TIMEOUT = 2   # Aggressive timeout
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Z3X-Scanner-Pro"

# ========================
#       BANNER ART
# ========================
def show_banner():
    f = Figlet(font='slant')
    ascii_art = f.renderText("Z3X ULTIMATE")
    print(Fore.CYAN + ascii_art)
    print(Fore.MAGENTA + "▄" * 90)
    print(Fore.YELLOW + "ADMIN PANEL TERMINATOR | INDUSTRY-STRENGTH PENETRATION TOOL".center(90))
    print(Fore.YELLOW + f"Version 5.0 | {datetime.now().year} | By Z3X Security Division".center(90))
    print(Fore.MAGENTA + "▀" * 90 + "\n")

# ========================
#      URL VALIDATION
# ========================
def get_target_url():
    while True:
        url = input(Fore.BLUE + "[⌛] ENTER TARGET URL (http/https): " + Style.RESET_ALL).strip()
        if url.startswith(('http://', 'https://')):
            return url.rstrip('/')
        print(Fore.RED + "[✗] INVALID FORMAT! Must include protocol (http:// or https://)")

# ========================
#    ULTIMATE PATH DATABASE
# ========================
admin_paths = [
    # Core Admin Paths
    "/admin", "/adminpanel", "/admincp", "/admin_area", "/admin-login", "/admin_login", 
    "/administrator", "/moderator", "/webadmin", "/adminarea", "/controlpanel", "/admincontrol",
    
    # CMS Admin Paths
    "/wp-admin", "/wp-login.php", "/wordpress/wp-admin", "/wordpress/wp-login.php",
    "/joomla/administrator", "/administrator/index.php", "/administrator/login.php",
    "/drupal/admin", "/drupal/user/login", "/magento/admin", "/opencart/admin",
    "/prestashop/admin", "/umbraco/", "/sitecore/admin", "/bolt/", "/backend/",
    "/blazor-admin/", "/cpanel", "/whm", "/webmail", "/plesk-admin",
    
    # Authentication Paths
    "/login", "/log-in", "/signin", "/sign-in", "/auth", "/authentication",
    "/secure", "/account", "/user", "/member", "/staff", "/employee",
    
    # Database Admin
    "/phpmyadmin", "/myadmin", "/phpMyAdmin", "/PMA", "/dbadmin", "/mysql",
    "/adminer", "/adminer.php", "/webdb", "/websql", "/sqladmin", "/sqlmanager",
    
    # Hidden Paths
    "/_admin", "/_wpadmin", "/hidden", "/private", "/secret", "/server",
    "/internal", "/restricted", "/protected", "/sysadmin", "/system",
    
    # API Management
    "/api/admin", "/rest/admin", "/graphql/admin", "/admin/api", "/admin/console",
    "/admin/portal", "/admin/manager", "/admin/system",
    
    # Versioned Paths
    "/v1/admin", "/v2/admin", "/admin/v1", "/admin/v2", "/admin/1.0", "/admin/2.0",
    
    # Backup Files
    "/admin.bak", "/admin.old", "/admin.zip", "/admin_backup", "/admin.tar.gz",
    "/admin.sql", "/admin_backup.zip", "/admin.rar", "/admin.tgz",
    
    # Common Files
    "/admin.php", "/admin.aspx", "/admin.jsp", "/admin.cgi", "/admin.pl",
    "/admin.html", "/admin.htm", "/admin/config", "/admin/setup",
    
    # International Paths
    "/administracion", "/administratie", "/verwaltung", "/管理", "/админ", "/管理者",
    
    # Unusual Paths
    "/0admin", "/xadmin", "/admin123", "/admin888", "/admin@", "/admin#",
    "/admin_", "/admin-", "/admin!", "/admin*", "/admin+",
    
    # Development Paths
    "/admin-dev", "/admin-test", "/admin-prod", "/admin-staging", "/admin-uat",
    "/admin-qa", "/admin-demo", "/admin-live",
    
    # Framework Specific
    "/laravel/admin", "/symfony/admin", "/yii/admin", "/django/admin",
    "/flask/admin", "/rails/admin", "/spring/admin",
    
    # Cloud Admin
    "/aws/admin", "/azure/admin", "/gcp/admin", "/cloud/admin", "/k8s/admin",
    
    # Additional Security Paths
    "/admin/security", "/admin/config", "/admin/settings", "/admin/management",
    "/admin/tools", "/admin/console", "/admin/interface"
]

# ========================
#      SCANNER ENGINE
# ========================
def check_admin_path(path):
    admin_url = target_url + path
    try:
        response = requests.get(
            admin_url,
            timeout=TIMEOUT,
            headers={'User-Agent': USER_AGENT},
            allow_redirects=False
        )
        return (response.status_code, admin_url)
    except:
        return (None, admin_url)

# ========================
#    DYNAMIC DISPLAY
# ========================
def display_scan_status(current_path):
    sys.stdout.write(f"\r{Fore.CYAN}[🔎] {Fore.WHITE}Scanning: {Fore.YELLOW}{target_url}{Fore.WHITE} | Testing: {Fore.MAGENTA}{current_path}")
    sys.stdout.flush()

# ========================
#      MAIN SCANNER
# ========================
def ultimate_scan():
    print(Fore.CYAN + f"\n[ℹ] TARGET: {Fore.WHITE}{target_url}")
    print(Fore.CYAN + f"[ℹ] THREADS: {Fore.WHITE}{THREADS}{Fore.CYAN} | TIMEOUT: {Fore.WHITE}{TIMEOUT}s")
    print(Fore.MAGENTA + "▄" * 90)
    
    found = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        future_to_path = {executor.submit(check_admin_path, path): path for path in admin_paths}
        
        for future in concurrent.futures.as_completed(future_to_path):
            path = future_to_path[future]
            display_scan_status(path)
            
            try:
                status_code, url = future.result()
                
                if status_code == 200:
                    found.append(url)
                    print(f"\n{Fore.GREEN}[✓] ADMIN PANEL FOUND: {Fore.WHITE}{url}")
                
            except Exception as e:
                print(f"\n{Fore.RED}[✗] ERROR: {Fore.WHITE}{path} - {str(e)}")
    
    # Final Results
    print(Fore.MAGENTA + "\n" + "▀" * 90)
    if found:
        print(Fore.GREEN + f"[🎯] SCAN COMPLETE! FOUND {len(found)} ADMIN PANELS:")
        for url in found:
            print(Fore.WHITE + f"  → {url}")
    else:
        print(Fore.RED + "[✗] NO ADMIN PANELS FOUND")
    
    print(Fore.MAGENTA + "▄" * 90)
    print(Fore.CYAN + f"\n[⏱] FINISHED AT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ========================
#       MAIN FLOW
# ========================
if __name__ == "__main__":
    show_banner()
    target_url = get_target_url()
    ultimate_scan()
