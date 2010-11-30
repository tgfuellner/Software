#!/usr/bin/python

"""Read a vcard file (RFC 2426) and generate Archos VP6500 Addressbook XML
   Export from google cantact is working.
"""

import optparse
import sys
import time
import re
# from pyxmpp.jabber import vcard
from pycocumalib import vcard
try:
    import cElementTreexx as etree
except ImportError:
    import xml.etree.ElementTree as etree

# old pyxmpp.jabber version
def split_vcards(inputfile):
    """Split an input file into vcards. File should be open(U)'ed."""
    card = []
    for line in inputfile:
        card.append(line.strip())
        if not line.strip():
            yield "\r\n".join(card)
            card = []
    assert not card, "excess content in vcard file"

# old pyxmpp.jabber version
def parse_vcard(vcardtxt):
    card = vcard.VCard(vcardtxt)
    return card

# old pyxmpp.jabber version
def print_name(card):
    print card.fn

# old pyxmpp.jabber version
def test_vcard(card):
    for card in split_vcards(open(opts.vcf,"rU")):
        print repr(card)
        try:
            print_name(parse_vcard(card))
        except AttributeError:
            pass

# <Contact
# * Uid="-1181769659"
# Categories="-1181769896"
# * Title="Dr."
# * FirstName="test first name"
# * MiddleName="middle"
# * LastName="last"
# * Suffix="Sr."
# * FileAs="last, test first name middle"
# * JobTitle="title"
# * Department="bus dept"
# * Company="company"
# * BusinessPhone="bus phone"
# * BusinessFax="bus fax"
# * BusinessMobile="bus mob"
# * DefaultEmail="user@domain1"
# * Emails="user@domain1 user@domain2"
# * HomePhone="home phone"
# * HomeFax="home fax"
# * HomeMobile="home mob"
# * BusinessStreet="bus street
#   more bus street"
# * BusinessCity="bus city"
# * BusinessState="bus state"
# * BusinessZip="bus zip"
# * BusinessCountry="bus country"
# * BusinessPager="bus pager"
# * BusinessWebPage="bus url"
# Office="bus office"
# Profession="nus profession"
# Assistant="bus asst"
# Manager="bus manager"
# * HomeStreet="home street
#  more home street"
# * HomeCity="home city"
# * HomeState="home state"
# * HomeZip="home zip"
# * HomeCountry="home country"
# * HomeWebPage="home url"
# Spouse="home spouse"
# Gender="1"
# * Birthday="20070601"
# Anniversary="20070707"
# * Nickname="nick"
# Children="home kids"
# Notes="notes...
#  lots
#  of notes"
# LastNamePronunciation="pron last"
# FirstNamePronunciation="pron first"
# CompanyPronunciation="pron comp"
#   />


def emit_contact(card, uid=None):
    attrs = {}
    # Ringtone
    attrs["tone"] = "/usr/local/etc/SystemRingTones/01-Dring1.desktop"
    # <Contact Uid="-1181769651" 
    # Uid is pretty clearly creation-time in unix seconds, negative.
    attrs["Uid"] = uid or unicode(-int(time.time()))
    # Categories="-1181769896"
    # that may be the time stamp of the creation of the category name, hmm.
    # -- name --
    # Title="Dr."
    attrs["Title"] = card.n.prefixes.get()
    # FirstName="test first name"
    if " " in card.n.given.get():
        # MiddleName="middle"
        attrs["FirstName"], attrs["MiddleName"] = card.n.given.get().split(" ", 1)
    else:
        attrs["FirstName"] = card.n.given.get()
    # LastName="last"
    attrs["LastName"] = card.n.family.get()
    # Suffix="Sr."
    attrs["Suffix"] = card.n.suffixes.get()
    # FileAs="last, test first name middle"
    attrs["Nickname"] = card.nickname.get()
    if not card.bday.is_empty():
        # Birthday="20070601"
        attrs["Birthday"] = card.bday.getDate().replace("-","")
    # FileAs="last, test first name middle"
    attrs["FileAs"] = card.getDisplayName()
    # -- work --
    # JobTitle="title"
    attrs["JobTitle"] = card.title.get()
    # Department="bus dept"
    if not card.org.units.is_empty():
        attrs["Department"] = card.org.units.get()
    # Company="company"
    if not card.org.org.is_empty():
        attrs["Company"] = card.org.org.get()
    for tel in card.tel:
        # pref isn't actually used...
        # see vC_tel_types
        telparms = tel.params.get("type")
        if "work" in telparms or "WORK" in telparms:
            telpat = "Business%s"
        elif "home" in telparms or "HOME" in telparms:
            telpat = "Home%s"
        else:
            if not card.org.org.is_empty():
                telpat = "Business%s"
            else:
                # default to home, if we don't have anything
                telpat = "Home%s"

        # BusinessFax="bus fax"
        # HomeFax="home fax"
        if "fax" in telparms or "FAX" in telparms:
            attrs[telpat % "Fax"] = format_tel(tel.get())
        # BusinessMobile="bus mob"
        # HomeMobile="home mob"
        elif "cell" in telparms or "CELL" in telparms:
            attrs[telpat % "Mobile"] = format_tel(tel.get())
        # BusinessPager="bus pager"
        elif "pager" in telparms or "PAGER" in telparms:
            attrs["BusinessPager"] = format_tel(tel.get())
        # BusinessPhone="bus phone"
        # HomePhone="home phone"
        elif "voice" in telparms or "VOICE" in telparms:
            attrs[telpat % "Phone"] = format_tel(tel.get())
        else:
            # good enough.  The one "MSG" entry I have is fake
            k = telpat % "Phone"
            if k in attrs:
                attrs[telpat % "Pc"] = format_tel(tel.get())
            else:
                attrs[telpat % "Phone"] = format_tel(tel.get())

    # DefaultEmail="user@domain1"
    for email in card.email:
        # see also vC_email_types
        if "PREF" in email.params.get("type") or "pref" in email.params.get("type"):
            attrs["DefaultEmail"] = email.get()
        # Emails="user@domain1 user@domain2"
        attrs["Emails"] = " ".join(filter(None, attrs.get("Emails","").split(" ") + [email.get()]))
    for adr in card.adr:
        # ignoring: "extended", "pobox".  also not splitting street...
        if "HOME" in adr.params.get("type"):
            adrpat = "Home%s"
        elif "WORK" in adr.params.get("type"):
            adrpat = "Business%s"
        else:
            print ">>",adr,"<<"
            assert 0, "need to handle unspecified address type"
        # HomeStreet="home street
        #  more home street"
        # BusinessStreet="bus street
        #   more bus street"
        attrs[adrpat % "Street"] = adr.street.get()
        # BusinessCity="bus city"
        # HomeCity="home city"
        attrs[adrpat % "City"] = adr.city.get()
        # BusinessState="bus state"
        # HomeState="home state"
        attrs[adrpat % "State"] = adr.region.get()
        # BusinessZip="bus zip"
        # HomeZip="home zip"
        attrs[adrpat % "Zip"] = adr.postcode.get()
        # BusinessCountry="bus country"
        # HomeCountry="home country"
        attrs[adrpat % "Country"] = adr.country.get()

    if not card.url.is_empty():
        if not card.org.org.is_empty():
            # BusinessWebPage="bus url"
            attrs["BusinessWebPage"] = card.url.get()
        else:
            # HomeWebPage="home url"
            attrs["HomeWebPage"] = card.url.get()

    # BusinessCard="TRUE"  />
    # filter...
    for k in attrs.keys():
        if not attrs[k]:
            del attrs[k]
    return attrs

def format_tel(tel):
    """Strip blanks, use 00 fror plus, delete all non digits and *"""
    tel = re.sub(r'^\+',r'00',tel)
    tel = re.sub(r'[^*0-9]',r'',tel)
    return tel

def add_contact(xmltree, attrs):
    """Add a <Contact> with the given attributes"""
    contact = etree.Element("Contact", attrib=attrs)
    contact.tail = "\n"
    xmltree.find("Contacts").insert(1, contact)

# yes, the doctype is Addressbook and the tag is AddressBook.
# we'll hope the parser is "real XML" enough to not care...
addressbook_xml_template = '''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE Addressbook ><AddressBook>
<Groups>
</Groups>
<Contacts>
</Contacts>
</AddressBook>'''

if __name__ == "__main__":
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option("--vcf")
    parser.add_option("--xml")
    parser.add_option("--test", action="store_true")
    opts, args = parser.parse_args()

    if args:
        parser.print_help()
        sys.exit("no args")

    if not opts.vcf:
        parser.print_help()
        sys.exit("--vcf input VCard File")
    if not opts.xml and not opts.test:
        parser.print_help()
        sys.exit("--xml output Addressbook XML file")

    if opts.test:
        cards = vcard.vCardList()
        cards.LoadFromFile(opts.vcf)
        for card in cards.sortedlist():
            emit_contact(cards[card])
        sys.exit()

        etree.fromstring

    cards = vcard.vCardList()
    cards.LoadFromFile(opts.vcf)
        
    xmlout = etree.fromstring(addressbook_xml_template)
    for card in cards.sortedlist():
        add_contact(xmlout, emit_contact(cards[card]))
    # print etree.tostring(xmlout)
    print >> file(opts.xml, "w"), etree.tostring(xmlout, encoding="UTF-8")

# "version", "n", "fn", "nickname", "bday", "tel", "adr", "label", "email",
# "mailer", "org", "title", "role", "note", "categories", "sort_string", 
# "url", "key", "rev", "uid", "tz", "geo", "photo", "logo"
