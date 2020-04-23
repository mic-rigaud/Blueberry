# @Author: michael
# @Date:   23-Apr-2020
# @Filename: test_virustotal.py
# @Last modified by:   michael
# @Last modified time: 23-Apr-2020
# @License: GNU GPL v3


from plugins.virustotal.virustotal import print_analyse


def test_print_analyse():
    analyse = {"data": {
        "attributes": {
            "categories": {},
            "first_submission_date": 1276511498,
            "html_meta": {
                "description": [
                    "Search the world's information, including webpages, images, videos and more. Google has many special features to help you find exactly what you're looking for."
                    ],
                "robots": [
                    "noodp"
                    ]
                },
            "last_analysis_date": 1587631029,
            "last_analysis_results": {
                "ADMINUSLabs": {
                    "category": "harmless",
                    "engine_name": "ADMINUSLabs",
                    "method": "blacklist",
                    "result": "clean"
                    },
                "AegisLab WebGuard": {
                    "category": "harmless",
                    "engine_name": "AegisLab WebGuard",
                    "method": "blacklist",
                    "result": "clean"
                    },
                "AlienVault": {
                    "category": "harmless",
                    "engine_name": "AlienVault",
                    "method": "blacklist",
                    "result": "clean"
                    },
                "Antiy-AVL": {
                    "category": "harmless",
                    "engine_name": "Antiy-AVL",
                    "method": "blacklist",
                    "result": "clean"
                    }
                },
            "last_analysis_stats": {
                "harmless": 73,
                "malicious": 0,
                "suspicious": 0,
                "timeout": 0,
                "undetected": 6
                },
            "last_final_url": "http://www.google.com/",
            "last_http_response_code": 200,
            "last_http_response_content_length": 39769,
            "last_http_response_content_sha256": "a71702ad6c27115ded49d99ada2649ba94594180c00bede227344c40022450ea",
            "last_http_response_cookies": {
                "1P_JAR": "2020-04-23-08",
                "NID": "203=Sk_c616-0V1ULsu7JOjcHd-GuDuWPpc8SDSX2R6v7EU8FMOdT2SowmM9D4fjXlyyX_nL5zAvw0eARot890wNlDqcVgr14W3ldX8TIkPDf-l3YJN4aYvQMSEjSjF-gkIwTNxHoQkV-X8ofYnwxsHQInPjTZSLtKyKOfUZEGMUWlM"
                },
            "last_http_response_headers": {
                "cache-control": "private, max-age=0",
                "content-length": "39769",
                "content-type": "text/html; charset=UTF-8",
                "date": "Thu, 23 Apr 2020 08:37:10 GMT",
                        "expires": "-1",
                        "p3p": "CP=\"This is not a P3P policy! See g.co/p3phelp for more info.\"",
                        "server": "gws",
                        "set-cookie": "1P_JAR=2020-04-23-08; expires=Sat, 23-May-2020 08:37:10 GMT; path=/; domain=.google.com; Secure, NID=203=Sk_c616-0V1ULsu7JOjcHd-GuDuWPpc8SDSX2R6v7EU8FMOdT2SowmM9D4fjXlyyX_nL5zAvw0eARot890wNlDqcVgr14W3ldX8TIkPDf-l3YJN4aYvQMSEjSjF-gkIwTNxHoQkV-X8ofYnwxsHQInPjTZSLtKyKOfUZEGMUWlM; expires=Fri, 23-Oct-2020 08:37:10 GMT; path=/; domain=.google.com; HttpOnly",
                        "x-frame-options": "SAMEORIGIN",
                        "x-xss-protection": "0"
                },
            "last_modification_date": 1587631032,
            "last_submission_date": 1587631029,
            "outgoing_links": [
                "http://www.youtube.com/?gl=US&tab=w1",
                "http://www.blogger.com/?tab=wj"
                ],
            "reputation": 2429,
            "tags": [],
            "targeted_brand": {},
            "times_submitted": 111857,
            "title": "Google",
            "total_votes": {
                "harmless": 1582,
                "malicious": 562
                },
            "trackers": {},
            "url": "http://google.com/"
            },
        "id": "cf4b367e49bf0b22041c6f065f4aa19f3cfe39c8d5abc0617343d1a66c6a26f5",
        "links": {
            "self": "https://www.virustotal.com/api/v3/urls/cf4b367e49bf0b22041c6f065f4aa19f3cfe39c8d5abc0617343d1a66c6a26f5"
            },
        "type": "url"
    }}
    reponse = print_analyse(analyse)
    assert "Antiy-AVL" in reponse

    # test mauvais
    reponse = print_analyse({"toto": 0})
    assert "[ERROR]" in reponse
