import scapy.all as scapy
from scapy_http import http

def veri_toplama(interface):
    scapy.sniff(iface=interface,store=False,prn=veri_analiz)

def veri_analiz(paket):
    #paket.show()
    if paket.haslayer(http.HTTPRequest):
        if paket.haslayer(scapy.Raw):
            paket(scapy.Raw).load


veri_toplama("eth0")