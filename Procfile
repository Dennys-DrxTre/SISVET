web: gunicorn <el nombre de tu proyecto>.wsgi --log-file -
web: gunicorn CONFIG.wsgi:application -w ${WORKERS:-3} -b 0.0.0.0:$PORT -t 29
