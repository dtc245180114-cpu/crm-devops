#!/bin/bash
set -e

ADMIN_PASS="Admin@CRM2026!"
STAFF_PASS="Staff@CRM2026!"
PGADMIN_PASS="Admin@CRM2026!"
GRAFANA_PASS="Admin@CRM2026!"
DB_SUPER_PASS="Admin@CRM2026!"
DB_APP_PASS="App@CRM2026!"
DB_EXPORTER_PASS="Exporter@CRM2026!"
PGADMIN_EMAIL="dtc245180114@ictu.edu.vn"

echo "=================================================================="
echo "          THIẾT LẬP TÀI KHOẢN MẶC ĐỊNH CHO TẤT CẢ DỊCH VỤ        "
echo "=================================================================="

# 1. Sinh password hash qua container web
echo "[1/5] Sinh password hash qua web container..."
ADMIN_HASH=$(docker compose -f /home/quangiu/crm/docker-compose.yml exec -T web python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('$ADMIN_PASS'))" | tr -d '\r')
STAFF_HASH=$(docker compose -f /home/quangiu/crm/docker-compose.yml exec -T web python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('$STAFF_PASS'))" | tr -d '\r')

echo " -> Admin hash: ${ADMIN_HASH:0:25}..."
echo " -> Staff hash: ${STAFF_HASH:0:25}..."

# 2. Cập nhật .env
echo "[2/5] Cập nhật file .env trên máy chủ..."
cat << EOF > /home/quangiu/crm/.env
# ==============================================================================
# HỆ THỐNG CRM CHĂM SÓC KHÁCH HÀNG - CẤU HÌNH MÔI TRƯỜNG MẶC ĐỊNH
# MSSV: dtc245180114 - NGUYEN MINH QUANG
# ==============================================================================

# 1. PostgreSQL Configuration
POSTGRES_DB=crm
POSTGRES_USER=crm_admin
POSTGRES_PASSWORD=$DB_SUPER_PASS

# 2. Dedicated Application DB Role (Non-superuser)
APP_DB_USER=crm_app
APP_DB_PASSWORD=$DB_APP_PASS

# 3. Dedicated Monitoring DB Role (pg_monitor, Non-superuser)
POSTGRES_EXPORTER_PASSWORD=$DB_EXPORTER_PASS

# 4. Flask App Configuration
SECRET_KEY=CRM2026SecretKeySecurityDevOpsNguyenMinhQuangDTC245180114
FLASK_ENV=production

# 5. pgAdmin Configuration
PGADMIN_DEFAULT_EMAIL=$PGADMIN_EMAIL
PGADMIN_DEFAULT_PASSWORD=$PGADMIN_PASS

# 6. CRM Users Default Passwords
ADMIN_PASSWORD=$ADMIN_PASS
STAFF1_PASSWORD=$STAFF_PASS
STAFF2_PASSWORD=$STAFF_PASS

# 7. Grafana Configuration
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=$GRAFANA_PASS
EOF

chmod 600 /home/quangiu/crm/.env
echo " -> Đã ghi đè /home/quangiu/crm/.env với quyền 600."

# 3. Cập nhật Database
echo "[3/5] Cập nhật mật khẩu role Database và bảng users..."
docker compose -f /home/quangiu/crm/docker-compose.yml exec -T db psql -U crm_admin -d crm << EOF
ALTER USER crm_admin WITH PASSWORD '$DB_SUPER_PASS';
ALTER USER crm_app WITH PASSWORD '$DB_APP_PASS';
ALTER USER exporter WITH PASSWORD '$DB_EXPORTER_PASS';

UPDATE users SET password_hash = '$ADMIN_HASH' WHERE username = 'admin';
UPDATE users SET password_hash = '$STAFF_HASH' WHERE username IN ('nhanvien01', 'nhanvien02');
EOF

echo " -> Đã cập nhật database roles và user credentials."

# 4. Reset mật khẩu Grafana
echo "[4/5] Reset mật khẩu admin Grafana..."
docker compose -f /home/quangiu/crm/docker-compose.yml exec -T grafana grafana-cli admin reset-admin-password "$GRAFANA_PASS"

# 5. Khởi động lại các service cần áp dụng .env
echo "[5/5] Cập nhật lại pgAdmin, Web App và Exporter..."
cd /home/quangiu/crm
docker compose stop pgadmin || true
docker compose rm -f pgadmin || true
docker volume rm crm_pgadmin_data || true
docker compose up -d pgadmin web postgres-exporter

echo "=================================================================="
echo " HOÀN TẤT ĐẶT TÀI KHOẢN MẶC ĐỊNH CHO TẤT CẢ DỊCH VỤ!"
echo " Web CRM admin:    admin       / $ADMIN_PASS"
echo " Web CRM staff:    nhanvien01  / $STAFF_PASS"
echo " pgAdmin:          $PGADMIN_EMAIL / $PGADMIN_PASS"
echo " Grafana:          admin       / $GRAFANA_PASS"
echo " Database Super:   crm_admin   / $DB_SUPER_PASS"
echo " Database App:     crm_app     / $DB_APP_PASS"
echo "=================================================================="
