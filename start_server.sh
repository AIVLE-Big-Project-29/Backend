# backend/start_server.sh

#!/bin/bash

# 데이터베이스 마이그레이션
python manage.py migrate

# manage.py shell에서 import_excel 함수 실행
python manage.py shell <<EOF
from location.views import import_excel
import_excel('./전국_좌표데이터.xlsx')
exit
EOF

# Django 서버 실행
python manage.py runserver 0.0.0.0:8000
