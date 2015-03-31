#!/bin/bash
IFS=' ' read -a IPARRAY <<< $(ip a s|sed -ne '/127.0.0.1/!{s/^[ \t]*inet[ \t]*\([0-9.]\+\)\/.*$/\1/p}')
SERVERIP=${IPARRAY[0]}

for vpn in /proc/sys/net/ipv4/conf/*; do echo 0 > $vpn/accept_redirects; echo 0 > $vpn/send_redirects; done
iptables -t nat -A POSTROUTING -s 172.16.1.0/24 -o eth0 -j MASQUERADE
iptables -t nat -A POSTROUTING -j SNAT --to-source $SERVERIP -o eth+

ipsec_conf=$(cat /etc/ipsec.conf.template)
echo "${ipsec_conf/INSERTSERVERIPHERE/$SERVERIP}" > /etc/ipsec.conf

ipsec_secrets=$(cat /etc/ipsec.secrets)
for word in $ipsec_secrets
do
    echo "${ipsec_secrets/$word/$SERVERIP}" > /etc/ipsec.secrets
    break
done

/etc/init.d/ipsec restart
/etc/init.d/xl2tpd restart
