#!/usr/bin/python3
# -*- encoding: utf-8 -*-

"""Digea EPG parser, add mapping to CHANELS"""

from __future__ import print_function
import datetime
from xml.sax.saxutils import escape
from bs4 import BeautifulSoup
import requests


def _channel(channel, name):
    """Channel Id and Name"""
    print('  <channel id="{}">'.format(channel))
    print('    <display-name lang="el">{}</display-name>'.format(escape(name)))
    print('  </channel>')


def _programme(start, channel, title, desc):
    """Channel Programm using only start, end should be calculated"""
    print('  <programme start="{} +0200" channel="{}">'.format(start, channel))
    print('    <title lang="el">{}</title>'.format(escape(title)))
    print('    <desc>{}</desc>'.format(escape(desc)))
    print('  </programme>')


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.digea.gr',
    'Connection': 'keep-alive',
    'Referer': 'https://www.digea.gr/EPG/el',
}

CHANNELS = {
    '100': ('digea.alpha.gr', 'ALPHA'),
    '300': ('digea.ant1.gr', 'ANT1'),
    '800': ('digea.openbeyond.gr', 'OPEN BEYOND'),
    '400': ('digea.mtv.gr', 'M.tv'),
    '600': ('digea.skai.gr', 'SKAI'),
    '700': ('digea.star.gr', 'STAR'),
    '900': ('digea.mega.gr', 'MEGA'),
    '5700': ('digea.alfa.gr', 'ALFA'),
    '5710': ('digea.centertv.gr', 'CENTER TV'),
    '5720': ('digea.deltatv.gr', 'DELTA TV'),
    '5725': ('digea.diktyotv.gr', 'DIKTYO TV'),
    '5730': ('digea.smile.gr', 'SMILE'),
    '5735': ('digea.enachannel.gr', 'ENA CHANNEL'),
    '5755': ('digea.lydiatv.gr', 'LYDIA TV'),
    '5750': ('digea.orestiadatv.gr', 'ORESTIADA TV'),
    '5760': ('digea.tvrodopi.gr', 'TV RODOPI'),
    '5765': ('digea.starbellados.gr', 'STAR B. ELLADOS'),
    '5770': ('digea.thrakinet.gr', 'THRAKINET'),
    '5775': ('digea.tileepiloges.gr', 'TILE EPILOGES'),
    '5780': ('digea.aepsilonanmakthrakis.gr', 'a.Epsilon An. Mak. Thrakis'),
    '5790': ('digea.xanthichannel.gr', 'XANTHI CHANNEL'),
    '5850': ('digea.4e.gr', '4Ε'),
    '5855': ('digea.atlastv.gr', 'ATLAS TV'),
    '5860': ('digea.bergina.gr', 'BERGINA'),
    '5880': ('digea.europeone.gr', 'EUROPE ONE'),
    '5885': ('digea.aechannelthessaloniki.gr', 'AE CHANNEL THESSALONIKI'),
    '5905': ('digea.kanali9.gr', 'KANALI 9'),
    '5910': ('digea.nickelodeonplus.gr', 'NICKELODEON PLUS'),
    '5865': ('digea.diontv.gr', 'DION TV'),
    '5920': ('digea.eurochannel.gr', 'EURO CHANNEL'),
    '5925': ('digea.tv100.gr', 'TV 100'),
    '5922': ('digea.gnomitv.gr', 'GNOMI TV'),
    '6000': ('digea.diktyo.gr', 'DIKTYO'),
    '6005': ('digea.flashtv.gr', 'FLASH TV'),
    '6010': ('digea.osiosnikanor.gr', 'ΟΣΙΟΣ ΝΙΚΑΝΩΡ'),
    '6050': ('digea.topchannel.gr', 'TOP CHANNEL'),
    '6060': ('digea.westchannel.gr', 'WEST CHANNEL'),
    '7000': ('digea.arttv.gr', 'ART TV'),
    '7005': ('digea.axelwostv.gr', 'AXELWOS TV'),
    '7010': ('digea.bhmatv.gr', 'BHMA TV'),
    '7015': ('digea.corfutv.gr', 'CORFU TV'),
    '7050': ('digea.epirustv1.gr', 'EPIRUS TV1'),
    '7055': ('digea.itv.gr', 'ITV'),
    '7065': ('digea.starttv.gr', 'START TV'),
    '5000': ('digea.achaiachannel.gr', 'ACHAIA CHANNEL'),
    '5002': ('digea.arkadikitv.gr', 'ARKADIKI TV'),
    '5004': ('digea.axiontv.gr', 'AXION TV'),
    '5006': ('digea.besttv.gr', 'BEST TV'),
    '5012': ('digea.hlektratv.gr', 'HLEKTRA TV'),
    '5014': ('digea.ionianchannel.gr', 'IONIAN CHANNEL'),
    '5030': ('digea.lepanto.gr', 'LEPANTO'),
    '5048': ('digea.lychnos.gr', 'LYCHNOS'),
    '5034': ('digea.mesogeiostv.gr', 'MESOGEIOS TV'),
    '5036': ('digea.anet.gr', 'a.NET'),
    '5038': ('digea.ort.gr', 'ORT'),
    '5007': ('digea.plp.gr', 'PLP'),
    '5040': ('digea.rtpkentpo.gr', 'RTP KENTPO'),
    '5042': ('digea.super.gr', 'SUPER'),
    '5044': ('digea.superb.gr', 'SUPER B'),
    '5950': ('digea.astratv.gr', 'ASTRA TV'),
    '5955': ('digea.thessaliatv.gr', 'THESSALIA TV'),
    '5960': ('digea.trt.gr', 'TRT'),
    '5965': ('digea.tv10.gr', 'TV 10'),
    '5970': ('digea.smileplus.gr', 'SMILE PLUS'),
    '5100': ('digea.etv.gr', 'ETV'),
    '5104': ('digea.enake.gr', 'ENA K.E.'),
    '5108': ('digea.starke.gr', 'STAR K.E.'),
    '3074': ('digea.art.gr', 'ART'),
    '3000': ('digea.extrachannel.gr', 'EXTRA CHANNEL'),
    '3004': ('digea.action24.gr', 'ACTION24'),
    '3008': ('digea.atticatv.gr', 'ATTICA TV'),
    '3012': ('digea.bluesky.gr', 'BLUE SKY'),
    '3016': ('digea.channel9.gr', 'CHANNEL 9'),
    '3030': ('digea.aechannel.gr', 'AE CHANNEL'),
    '3034': ('digea.hightv.gr', 'HIGH TV'),
    '3038': ('digea.kontra.gr', 'KONTRA'),
    '3042': ('digea.madtv.gr', 'MAD TV'),
    '3060': ('digea.risetv.gr', 'RISE TV'),
    '3064': ('digea.nickelodeon.gr', 'NICKELODEON'),
    '3072': ('digea.smile.gr', 'SMILE'),
    '3068': ('digea.alert.gr', 'ALERT'),
    '7100': ('digea.notostv.gr', 'NOTOS TV'),
    '7105': ('digea.creta.gr', 'CRETA'),
    '7110': ('digea.kphthtv.gr', 'KPHTH TV'),
    '7115': ('digea.kphthtv1.gr', 'KPHTH TV 1'),
    '7130': ('digea.neatvcrete.gr', 'NEA TV CRETE'),
    '7135': ('digea.sitiatv.gr', 'SITIA TV'),
    '7140': ('digea.aetv.gr', 'AE TV'),
    '7150': ('digea.aigaiotv.gr', 'AIGAIOTV'),
    '7155': ('digea.dimotikitileorasiko.gr', 'DIMOTIKI TILEORASI KO'),
    '7160': ('digea.iridatv.gr', 'IRIDA TV'),
    '7170': ('digea.tharri.gr', 'THARRI'),
    '7175': ('digea.samiakitv.gr', 'SAMIAKI TV'),
    '7185': ('digea.kosmos.gr', 'KOSMOS'),
    '7205': ('digea.syrostv1.gr', 'SYROS TV1'),
    '7210': ('digea.volcano.gr', 'VOLCANO'),
    '5800': ('digea.alitheiatv.gr', 'ALITHEIA TV'),
    '5810': ('digea.patridatv.gr', 'PATRIDA TV'),
    '5815': ('digea.tvm.gr', 'TVM'),
}

EPG_URL = 'https://www.digea.gr/ajax_epg.php'

REGIONS = [
    'Nationwide',
    'E-Macedonia-Thrace-R-Z-1',
    'C-Macedonia-R-Z-2-3',
    'W-Macedonia-R-Z-4',
    'W-Greece-R-Z-5',
    'Peloponnese-R-Z-6',
    'Thessaly-R-Z-7',
    'C-Greece-R-Z-8',
    'Attica-R-Z-9',
    'Crete-R-Z-10',
    'Dodecanese-Samos-R-Z-11',
    'Cyclades-R-Z-12',
    'NE-Aegean-R-Z-13',
]

MATRIX = [(d, r) for d in (datetime.date.today() + datetime.timedelta(n)
                           for n in range(6)) for r in REGIONS]

def get_data(day, region):
    """get data for a single day and region"""
    data = {
        'tab': region,
        'curdate1': '%s 00:00:00' % day.strftime('%Y-%m-%d'),
        'curdate2': '%s 23:59:59' % day.strftime('%Y-%m-%d'),
        'lng': ''
    }
    # get epg
    res = requests.post(EPG_URL, headers=HEADERS, data=data)
    return res.json()

def parse_html(html, day, channel):
    """parse the html returned from get data"""
    soup = BeautifulSoup(html, 'lxml')
    for lis in soup.findAll('li'):
        _time = lis.find('p', attrs={'class':'time'}).text
        _title = lis.find('p', attrs={'class':None}).text.strip()
        _di = lis.find('a', href=True)['href'][1:]
        _desc = soup.find('div', id=_di).text.strip()
        _start = '%s%s00' % (day.strftime('%Y%m%d'), _time.replace(':', ''))
        _programme(_start, channel, _title, _desc)

CHC = []

for d, r in MATRIX:
    js = get_data(d, r)
    for ci in js['programs']:
        nci = CHANNELS.get(ci, None)
        if not nci:
            continue
        if nci not in CHC:
            CHC.append(nci)
            _channel(nci[0], nci[1])
        _html = js['programs'][ci]['html']
parse_html(_html, d, nci[0])
