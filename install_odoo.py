# https://www.rosehosting.com/blog/how-to-install-odoo-17-on-ubuntu-24-04/
import os
import subprocess
import sys

# -------------------------CONSTANTS--------------------------------
GITHUB_ODOO_URL= "https://www.github.com/odoo/odoo"
BRANCH = "18.0" # odoo version
PYTHON_VERSION = "python3.11"
PROJECT_NAME = f"odoo_{BRANCH}"
CUSTOM_MODULE_NAME = "custom_module" # sales_extension business_customizations

ODOO_ADMIN_PASSWORD = "Srt0ngh0ld0d00"
ODOO_PSQL_USER = f"user_odoo{BRANCH}"
ODOO_PSQL_USER_PASSWORD = "P$ql@Odoo758"
ODOO_PORT = 8069

VIRTUAL_ENVIRONMENT_NAME = "venv"
# -------------------------------------------------------------------

ODOO_VERSION = f"odoo{BRANCH}"
BASE_DIR = os.getcwd()
PROJECT_DIR = os.path.join(BASE_DIR, PROJECT_NAME)
CUSTOM_ADDONS_DIR = os.path.join(PROJECT_DIR, "custom_addons")
CONFIG_DIR = os.path.join(PROJECT_DIR, "config")
ODOO_CLONE_DIR = os.path.join(PROJECT_DIR, ODOO_VERSION)
ODOO_BIN = os.path.join(ODOO_CLONE_DIR, "odoo-bin")
ODOO_ADDONS_DIR = os.path.join(ODOO_CLONE_DIR, "addons")

# Define the Project folder structure
PROJECT_DIR_STRUCTURE = [
    CUSTOM_ADDONS_DIR,
    CONFIG_DIR,
    ODOO_CLONE_DIR,
]

ODOO_CONFIG_FILE = os.path.join(CONFIG_DIR, "odoo.conf")
REQUIREMENTS_FILE = os.path.join(ODOO_CLONE_DIR, "requirements.txt")

VIRTUAL_ENVIRONMENT_DIR = os.path.join(PROJECT_DIR, VIRTUAL_ENVIRONMENT_NAME)
# -------------------------------------------------------------------


# ============================================================
def create_project_structure():
    # Create directories
    for folder_path in PROJECT_DIR_STRUCTURE:
        os.makedirs(folder_path, exist_ok=True)
        print(f"Directory '{folder_path}' has been created or already exists.")

        
    print("All directories have been created or already exist.")

# ============================================================
def create_conf_file():

    with open(ODOO_CONFIG_FILE, 'w') as file:
        file.write(f"""
[options]
admin_passwd = {ODOO_ADMIN_PASSWORD}
db_host = False
db_port = False
db_user = {ODOO_PSQL_USER}
db_password = {ODOO_PSQL_USER_PASSWORD}
xmlrpc_port = {ODOO_PORT}
default_productivity_apps = True

; =============== Pycharm ===============
; Working Directory: {PROJECT_DIR}
; Script: {ODOO_BIN}
; Script Parameters -c {ODOO_CONFIG_FILE} -u iwss_reports

; =============== Hello World ===============
addons_path = {ODOO_ADDONS_DIR},{CUSTOM_ADDONS_DIR}
; This filter matches databases that start with
; dbfilter = ^OdooDB*$
; This filter forces Odoo to use only the
; dbfilter = ^MyDBonly$
; This filter forces Odoo to use multiple
; dbfilter = ^(database1|database2|database3)$
; ===========================================

; log_level = debug
; logfile = /Desktop/odoo.log
; workers = 1
; limit_time_real = 60
; limit_time_cpu = 30
; test_enable = True
; import_partial = True
; logrotate = True
; db_maxconn = 10
; proxy_mode = True
; timezone = Europe/Berlin

""")

    print(f"Created: {ODOO_CONFIG_FILE}")



# ============================================================
def setup_virtual_environment():
    
    # python3.11 -m venv odoo17-venv
    # source odoo17-venv/bin/activate
    # pip3 install wheel setuptools pip --upgrade
    # pip3 install -r odoo17/requirements.txt
    
    
    subprocess.run([PYTHON_VERSION, "-m", "venv", VIRTUAL_ENVIRONMENT_DIR])
    print(f"Virtual environment created with Python {PYTHON_VERSION} at: {VIRTUAL_ENVIRONMENT_DIR}")

    # Activate the virtual environment and upgrade pip
    if os.name == "nt":  # For Windows
        activate_script = os.path.join(VIRTUAL_ENVIRONMENT_DIR, "Scripts", "activate.bat")
        #subprocess.run([activate_script, "&&", "pip", "install", "--upgrade", "pip"], shell=True)
        #subprocess.run([activate_script, "&&", "pip", "install", "-r", REQUIREMENTS_FILE], shell=True)
        subprocess.run(f"{activate_script} && pip3 install wheel setuptools pip --upgrade", shell=True)
        subprocess.run(f"{activate_script} && pip3 install -r {REQUIREMENTS_FILE}", shell=True)
    else:  # For Unix/Linux/Mac
        activate_script = os.path.join(VIRTUAL_ENVIRONMENT_DIR, "bin", "activate")
        #subprocess.run(f"source {activate_script} && pip install --upgrade pip", shell=True, executable="/bin/bash")
        #subprocess.run(f"source {activate_script} && pip install -r {REQUIREMENTS_FILE}", shell=True, executable="/bin/bash")
        subprocess.run(f"source {activate_script} && pip3 install wheel setuptools pip --upgrade", shell=True, executable="/bin/bash")
        subprocess.run(f"source {activate_script} && pip3 install -r {REQUIREMENTS_FILE}", shell=True, executable="/bin/bash")


# ============================================================
def clone_odoo_repository():

    clone_command = ["git", "clone", "--depth", "1", "--branch", BRANCH, GITHUB_ODOO_URL, ODOO_CLONE_DIR]
    
    #clone_command = ["git", "clone", "--branch", BRANCH, GITHUB_ODOO_URL, ODOO_CLONE_DIR]

    # Clone the Odoo repository and ensure success before proceeding
    try:
        result = subprocess.run(clone_command, check=True)
        print(f"{ODOO_VERSION} repository cloned into: {ODOO_CLONE_DIR}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone Odoo repository. Error: {e}")
        sys.exit(1)  # Exit if the clone fails


# ============================================================
def run_command(commands):

    for command in commands:
        try:
            # Use subprocess.run to execute the command
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running command: {command}\n{e.stderr.decode()}")


# ============================================================
def create_custom_addons():
    command = f"{ODOO_BIN} scaffold {CUSTOM_MODULE_NAME} {CUSTOM_ADDONS_DIR}"
    activate_script = os.path.join(VIRTUAL_ENVIRONMENT_DIR, "bin", "activate")

    try:
        # Use subprocess.run to execute the command
        # result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = subprocess.run(f"source {activate_script} && {command}", shell=True, executable="/bin/bash",check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running command: {command}\n{e.stderr.decode()}")


# ============================================================
def main():
#     https://www.rosehosting.com/blog/how-to-install-odoo-17-on-ubuntu-24-04/

#     commands = [
#         f"sudo apt install {PYTHON_VERSION} {PYTHON_VERSION}-venv {PYTHON_VERSION}-dev {PYTHON_VERSION}-distutils -y",
#         f"curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py",
#         f"sudo {PYTHON_VERSION} get-pip.py",
#         f"sudo add-apt-repository ppa:deadsnakes/ppa -y",
#         f"sudo apt update"
#     ]
    commands = [
        f"sudo apt install {PYTHON_VERSION} {PYTHON_VERSION}-venv {PYTHON_VERSION}-dev {PYTHON_VERSION}-distutils -y",
        f"sudo apt install build-essential wget git libfreetype-dev libxml2-dev libzip-dev libsasl2-dev node-less libjpeg-dev zlib1g-dev libpq-dev libxslt1-dev libldap2-dev libtiff5-dev libopenjp2-7-dev libcap-dev -y",
    ]
    run_command(commands)

    # Step 3. Install PostgreSQL
    # apt install postgresql
    # su - postgres -c "createuser -s odoo17"
    commands = [
        f"sudo apt install postgresql postgresql-client -y",
        f"""sudo -u postgres psql -c "CREATE USER {ODOO_PSQL_USER} WITH CREATEDB NOCREATEROLE NOSUPERUSER PASSWORD '{ODOO_PSQL_USER_PASSWORD}';" """
    ]
    run_command(commands)
    
    # Step 5. Install Odoo 17
    # git clone https://www.github.com/odoo/odoo --depth 1 --branch 17.0 odoo17
    
    clone_odoo_repository()

    create_project_structure()

    create_conf_file()

    setup_virtual_environment()

    create_custom_addons()

    print("Project setup complete!")
    
    # Step 6. Create Odoo Systemd Unit file
    # nano /etc/systemd/system/odoo17.service
     
#     [Unit]
#     Description=odoo17
#     Requires=postgresql.service
#     After=network.target postgresql.service
#     
#     [Service]
#     Type=simple
#     SyslogIdentifier=odoo17
#     PermissionsStartOnly=true
#     User=odoo17
#     Group=odoo17
#     ExecStart=/opt/odoo17/odoo17-venv/bin/python3 /opt/odoo17/odoo17/odoo-bin -c /etc/odoo17.conf
#     StandardOutput=journal+console
#     
#     [Install]
#     WantedBy=multi-user.target


# systemctl daemon-reload
# systemctl enable --now odoo17
# systemctl status odoo17


if __name__ == "__main__":
    main()

