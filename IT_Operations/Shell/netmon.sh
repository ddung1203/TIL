#!/bin/bash
COUNT=10
while :
do
        if [ $COUNT = 10 ]
        then
                printf "+--------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+ \n"
                printf "|  TIME  |ESTAB|LISTN|T_WAT|CLOSD|S_SEN|S_REC|C_WAT|F_WT1|F_WT2|CLOSI|L_ACK| \n"
                printf "+--------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+ \n"
                COUNT=0
        fi
        COUNT=`expr $COUNT + 1`
        TIME=`/bin/date +%H:%M:%S`
        printf "|%s" ${TIME}
        netstat -an | \
        awk 'BEGIN {
                CLOSED = 0;
                LISTEN = 0;
                SYN_SENT = 0;
                SYN_RECEIVED = 0;
                ESTABLISHED = 0;
                CLOSE_WAIT = 0;
                FIN_WAIT_1 = 0;
                FIN_WAIT_2 = 0;
                CLOSING = 0;
                LAST_ACK = 0;
                TIME_WAIT = 0;
                OTHER = 0;
                }
                $6 ~ /^CLOSED$/ { CLOSED++; }
                $6 ~ /^CLOSE_WAIT$/ { CLOSE_WAIT++; }
                $6 ~ /^CLOSING$/ { CLOSING++; }
                $6 ~ /^ESTABLISHED$/ { ESTABLISHED++; }
                $6 ~ /^FIN_WAIT1$/ { FIN_WAIT_1++; }
                $6 ~ /^FIN_WAIT2$/ { FIN_WAIT_2++; }
                $6 ~ /^LISTEN$/ { LISTEN++; }
                $6 ~ /^LAST_ACK$/ { LAST_ACK++; }
                $6 ~ /^SYN_SENT$/ { SYN_SENT++; }
                $6 ~ /^SYN_RECV$/ { SYN_RECEIVED++; }
                $6 ~ /^TIME_WAIT$/ { TIME_WAIT++; }

                END {
                        printf "| %4d| %4d| %4d| %4d| %4d| %4d| %4d| %4d| %4d| %4d| %4d|\n",ESTABLISHED,LISTEN,TIME_WAIT,CLOSED,SYN_SENT,SYN_RECEIVED,CLOSE_WAIT,FIN_WAIT_1,FIN_WAIT_2,CLOSING,LAST_ACK;
                }'
        sleep 2
done