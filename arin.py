#!/usr/bin/env python

import cgi, cgitb, sys, requests, json

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

def arinasn ( asn ):
	r = requests.get( "http://whois.arin.net/rest/asn/%s.json" % (asn))
        decoded = json.loads(r.text)
        jdname = decoded['asn']['orgRef']['@name']
        jdout = "AS%s \n Name: %s" % (asn,jdname)
        print jdout
        return;

def arinpoc ( poc ):
        r = requests.get( "http://whois.arin.net/rest/poc/%s.json" % (poc))
        decoded = json.loads(r.text)
	jdfname = decoded['poc']['firstName']['$']
	jdlname = decoded['poc']['lastName']['$']
	jdcity = decoded['poc']['city']['$']
	jdcompany = decoded['poc']['companyName']['$']
	jdpostal = decoded['poc']['postalCode']['$']
	jdstreet = decoded['poc']['streetAddress']['line']['$']
	jdpostal = decoded['poc']['postalCode']['$']
	jdstate = decoded['poc']['iso3166-2']['$']
        jdout = '%s\n%s %s\n%s\n%s, %s, %s\n%s' % (poc, jdfname,jdlname, jdcompany, jdstreet, jdcity, jdstate, jdpostal)
        print jdout
        return; 

def arincidr ( cidr ):
        r = requests.get( "http://whois.arin.net/rest/cidr/%s.json" % (cidr))
        decoded = json.loads(r.text)
        jdname = decoded['net']['orgRef']['@name']
	jdhandle = decoded['net']['orgRef']['@handle']
        jdout = "%s\n %s\n%s\n" % (cidr,jdhandle,jdname)
        print r.text
        return;

def arinip ( ip ):
        r = requests.get( "http://whois.arin.net/rest/ip/%s.txt" % (ip))
#        decoded = json.loads(r.text)
#        jdname = decoded['net']['orgRef']['@name']
#        jdhandle = decoded['net']['orgRef']['@handle']
#	jdlength = decoded['net']['netBlocks']['netBlock']['cidrLength']['$']
#        jdout = "%s/%s\n%s\n%s\n" % (ip,jdlength,jdhandle,jdname)
        print r.text
        return;

	

try:
        # These two basically grab all the headers from the POST. 
        # Slack puts anything after /slash as the "text" field
        # 
        form = cgi.FieldStorage()
        text = form.getvalue("text")
	items = text.split( )
	

	if items[0] == 'asn':
		nasn = items[1]
		arinasn(nasn)
	elif items[0] == 'poc':
		npoc = items[1]
		arinpoc(npoc)
	elif items[0] == 'cidr':
		ncidr = items[1]
		arincidr(ncidr)
	elif items[0] == 'ip':
		nip = items[1]
		arinip(nip)

except:

        error =  "No data found  (%s)\n" % text
	print error

