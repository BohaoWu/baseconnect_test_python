#!/bin/bash
echo "Post script from pipeline."
if [ -f /etc/environment ]; then
  export $(grep -v '^#' /etc/environment | xargs -r) || true
fi
cd news_scraping && nohup /home/ubuntu/baseconnect_test_python/venv/bin/python manage.py runserver 0.0.0.0:8000 --noreload --insecure >/dev/null 2>&1 &

exit 0
