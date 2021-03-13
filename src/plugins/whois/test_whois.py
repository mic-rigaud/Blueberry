# @Author: michael
# @Date:   24-Apr-2020
# @Filename: test_whois.py
# @Last modified by:   michael
# @Last modified time: 29-Apr-2020
# @License: GNU GPL v3


# @Author: michael
# @Date:   23-Apr-2020
# @Filename: test_virustotal.py
# @Last modified by:   michael
# @Last modified time: 29-Apr-2020
# @License: GNU GPL v3


from src.plugins.whois.whois import print_analyse


def test_print_analyse():
    analyse = {"WhoisRecord": {
        "createdDate": "1997-09-15T00:00:00-0700",
        "updatedDate": "2019-09-09T08:39:04-0700",
        "expiresDate": "2028-09-13T00:00:00-0700",
        "registrant": {
            "organization": "Google LLC",
            "state": "CA",
            "country": "UNITED STATES",
            "countryCode": "US",
            "rawText": "Registrant Organization: Google LLC\u000aRegistrant State/Province: CA\u000aRegistrant Country: US\u000aRegistrant Email: Select Request Email Form at https://domains.markmonitor.com/whois/google.com"
            },
        "administrativeContact": {
            "organization": "Google LLC",
            "state": "CA",
            "country": "UNITED STATES",
            "countryCode": "US",
            "rawText": "Admin Organization: Google LLC\u000aAdmin State/Province: CA\u000aAdmin Country: US\u000aAdmin Email: Select Request Email Form at https://domains.markmonitor.com/whois/google.com"
            },
        "technicalContact": {
            "organization": "Google LLC",
            "state": "CA",
            "country": "UNITED STATES",
            "countryCode": "US",
            "rawText": "Tech Organization: Google LLC\u000aTech State/Province: CA\u000aTech Country: US\u000aTech Email: Select Request Email Form at https://domains.markmonitor.com/whois/google.com"
            },
        "domainName": "google.com",
        "nameServers": {
            "rawText": "ns4.google.com\u000ans1.google.com\u000ans2.google.com\u000ans3.google.com\u000a",
            "hostNames": [
                "ns4.google.com",
                "ns1.google.com",
                "ns2.google.com",
                "ns3.google.com"
                ],
            "ips": [
                ]
            },
        "status": "clientUpdateProhibited clientTransferProhibited clientDeleteProhibited serverUpdateProhibited serverTransferProhibited serverDeleteProhibited",
        "rawText": "Domain Name",
        "footer": "\u000a",
        "audit": {
            "createdDate": "2020-04-29 11:01:19.000 UTC",
            "updatedDate": "2020-04-29 11:01:19.000 UTC"
            },
        "customField1Name": "RegistrarContactEmail",
        "customField1Value": "abusecomplaints@markmonitor.com",
        "registrarName": "MarkMonitor, Inc.",
        "registrarIANAID": "292",
        "whoisServer": "whois.markmonitor.com",
        "createdDateNormalized": "1997-09-15 07:00:00 UTC",
        "updatedDateNormalized": "2019-09-09 15:39:04 UTC",
        "expiresDateNormalized": "2028-09-13 07:00:00 UTC",
        "customField2Name": "RegistrarContactPhone",
        "customField3Name": "RegistrarURL",
        "customField2Value": "+1.2083895770",
        "customField3Value": "http://www.markmonitor.com",
        "registryData": {
            "createdDate": "1997-09-15T04:00:00Z",
            "updatedDate": "2019-09-09T15:39:04Z",
            "expiresDate": "2028-09-14T04:00:00Z",
            "domainName": "google.com",
            "nameServers": {
                "rawText": "NS1.GOOGLE.COM\u000aNS2.GOOGLE.COM\u000aNS3.GOOGLE.COM\u000aNS4.GOOGLE.COM\u000a",
                "hostNames": [
                    "NS1.GOOGLE.COM",
                    "NS2.GOOGLE.COM",
                    "NS3.GOOGLE.COM",
                    "NS4.GOOGLE.COM"
                    ],
                "ips": [
                    ]
                },
            "status": "clientDeleteProhibited clientTransferProhibited clientUpdateProhibited serverDeleteProhibited serverTransferProhibited serverUpdateProhibited",
            "rawText": "Domain Name",
            "parseCode": 251,
            "header": "",
            "strippedText": "Domain Name",
            "footer": "\u000a",
            "audit": {
                "createdDate": "2020-04-29 11:01:18.000 UTC",
                "updatedDate": "2020-04-29 11:01:18.000 UTC"
                },
            "customField1Name": "RegistrarContactEmail",
            "customField1Value": "abusecomplaints@markmonitor.com",
            "registrarName": "MarkMonitor Inc.",
            "registrarIANAID": "292",
            "createdDateNormalized": "1997-09-15 04:00:00 UTC",
            "updatedDateNormalized": "2019-09-09 15:39:04 UTC",
            "expiresDateNormalized": "2028-09-14 04:00:00 UTC",
            "customField2Name": "RegistrarContactPhone",
            "customField3Name": "RegistrarURL",
            "customField2Value": "+1.2083895740",
            "customField3Value": "http://www.markmonitor.com",
            "whoisServer": "whois.markmonitor.com"
            },
        "contactEmail": "abusecomplaints@markmonitor.com",
        "domainNameExt": ".com",
        "estimatedDomainAge": 8262
        }}
    reponse = print_analyse(analyse)
    assert "Général" in reponse

    # test mauvais
    reponse = print_analyse({"toto": 0})
    assert "[ERROR]" in reponse
