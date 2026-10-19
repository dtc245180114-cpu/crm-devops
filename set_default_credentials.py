import subprocess
import os
from werkzeug.security import generate_password_hash

ADMIN_PASS = "Admin@CRM2026!"
STAFF_PASS = "Staff@CRM2026!"
PGADMIN_PASS = "Admin@CRM2026!"
GRAFANA_PASS = "Admin@CRM2026!"
DB_SUPER_PASS = "Admin@CRM2026!"
DB_APP_PASS = "App@CRM2026!"
DB_EXPORTER_PASS = "Exporter@CRM2026!"
PGADMIN_EMAIL = "dtc245180114@ictu.edu.vn"

admin_hash = generate_password_hash(ADMIN_PASS)
staff_hash = generate_password_hash(STAFF_PASS)

print("[1] Updating .env file...")
env_content = f"""# ==============================================================================
# HỆ THỐNG CRM CHĂM SÓC KHÁCH HÀNG - CẤU HÌNH MÔI TRƯỜNG MẶC ĐỊNH
# MSSV: dtc245180114 - NGUYEN MINH QUANG
# ==============================================================================

# 1. PostgreSQL Configuration
POSTGRES_DB=crm
POSTGRES_USER=crm_admin
POSTGRES_PASSWORD={DB_SUPER_PASS}

# 2. Dedicated Application DB Role (Non-superuser)
APP_DB_USER=crm_app
APP_DB_PASSWORD={DB_APP_PASS}

# 3. Dedicated Monitoring DB Role (pg_monitor, Non-superuser)
POSTGRES_EXPORTER_PASSWORD={DB_EXPORTER_PASS}

# 4. Flask App Configuration
SECRET_KEY=CRM2026SecretKeySecurityDevOpsNguyenMinhQuangDTC245180114
FLASK_ENV=production

# 5. pgAdmin Configuration
PGADMIN_DEFAULT_EMAIL={PGADMIN_EMAIL}
PGADMIN_DEFAULT_PASSWORD={PGADMIN_PASS}

# 6. CRM Users Default Passwords
ADMIN_PASSWORD={ADMIN_PASS}
STAFF1_PASSWORD={STAFF_PASS}
STAFF2_PASSWORD={STAFF_PASS}

# 7. Grafana Configuration
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD={GRAFANA_PASS}
"""

with open("/home/quangiu/crm/.env", "w") as f:
    f.write(env_content)
os.chmod("/home/quangiu/crm/.env", 0o600)
print(" -> [DONE] .env updated.")

print("\n[2] Updating PostgreSQL user credentials and web user hashes in database...")
sql_commands = f"""
ALTER USER crm_admin WITH PASSWORD '{DB_SUPER_PASS}';
ALTER USER crm_app WITH PASSWORD '{DB_APP_PASS}';
ALTER USER exporter WITH PASSWORD '{DB_EXPORTER_PASS}';

UPDATE users SET password_hash = '{admin_hash}' WHERE username = 'admin';
UPDATE users SET password_hash = '{staff_hash}' WHERE username IN ('nhanvien01', 'nhanvien02');
"""

cmd = ["docker", "compose", "-f", "/home/quangiu/crm/docker-compose.yml", "exec", "-T", "db", "psql", "-U", "crm_admin", "-d", "crm"]
proc = subprocess.run(cmd, input=sql_commands, text=True, capture_output=True)
if proc.returncode == 0:
    print(" -> [DONE] Database roles and users password hashes updated successfully.")
else:
    print(" -> [WARN] DB update output:", proc.stderr or proc.stdout)

print("\n[3] Resetting Grafana admin password...")
cmd_gf = ["docker", "compose", "-f", "/home/quangiu/crm/docker-compose.yml", "exec", "-T", "grafana", "grafana-cli", "admin", "reset-admin-password", GRAFANA_PASS]
proc_gf = subprocess.run(cmd_gf, capture_output=True, text=True)
print(" -> [DONE] Grafana output:", proc_gf.stdout.strip())

print("\n[4] Recreating pgAdmin with new default password...")
# pgAdmin uses internal SQLite db in pgadmin_data volume. Recreating container with new password:
subprocess.run(["docker", "compose", "-f", "/home/quangiu/crm/docker-compose.yml", "down", "pgadmin"], capture_output=True)
subprocess.run(["docker", "volume", "rm", "crm_pgadmin_data"], capture_output=True)
subprocess.run(["docker", "compose", "-f", "/home/quangiu/crm/docker-compose.yml", "up", "-d", "pgadmin", "web", "postgres-exporter"])

print("\n==================================================================")
print(" HOÀN TẤT ĐẶT TÀI KHOẢN MẶC ĐỊNH CHO TẤT CẢ DỊCH VỤ!")
print(f" Web CRM admin:    admin       / {ADMIN_PASS}")
print(f" Web CRM staff:    nhanvien01  / {STAFF_PASS}")
print(f" pgAdmin:          {PGADMIN_EMAIL} / {PGADMIN_PASS}")
print(f" Grafana:          admin       / {GRAFANA_PASS}")
print(f" Database Super:   crm_admin   / {DB_SUPER_PASS}")
print(f" Database App:     crm_app     / {DB_APP_PASS}")
print("==================================================================")
