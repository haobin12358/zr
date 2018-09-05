#!/bin/bash
P=5001
worker=1
host="0.0.0.0"
case "$@" in
    start)
        gunicorn -b $host:$P -w $worker run:app -D
        ;;
    stop)
        kill -9 `ps aux|grep gunicorn|grep $P|awk '{print $2}'|xargs`
        ;;
    restart)
        kill -9 `ps aux|grep gunicorn|grep $P|awk '{print $2}'|xargs`
        sleep 1
        gunicorn -b $host:$P -w $worker run:app -D
        ;;
    reload)
        ps aux |grep gunicorn |grep $P | awk '{print $2}'|xargs kill -HUP
        ;;
    status)
    pids=$(ps aux|grep gunicorn|grep $P)
        echo "$pids"
    ;;
    *)
        echo 'unknown arguments args(start|stop|restart|status|reload)'
        exit 1
        ;;
esac
