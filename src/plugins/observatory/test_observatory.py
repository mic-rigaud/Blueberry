# @Author: michael
# @Date:   08-May-2020
# @Filename: test_observatory.py
# @Last modified by:   michael
# @Last modified time: 08-May-2020
# @License: GNU GPL v3


from plugins.observatory.observatory import (get_icon, print_analyse,
                                             print_scan, print_tls_result)

ANALYSE = {"algorithm_version": 2,
           "end_time": "Fri, 08 May 2020 08:10:51 GMT",
           "grade": "D-",
           "hidden": True,
           "likelihood_indicator": "MEDIUM",
           "response_headers": {"Alt-Svc": "v=\"46,43\"",
                                "Cache-Control": "private, max-age=0",
                                "Content-Encoding": "gzip",
                                "Content-Type": "text/html; charset=UTF-8",
                                "Date": "Fri, 08 May 2020 08:10:51 GMT",
                                "Expires": "-1",
                                "P3P": "CP=\"This is not a P3P policy! See g.co/p3phelp for more info.\"",
                                "Server": "gws",
                                "Set-Cookie": "1P_JAR=2020-05-08-08; expires=Sun, 07-Jun-2020 08:10:51 GMT; path=/; domain=.google.fr; Secure; SameSite=none, NID=204=nKJhqT7QJ1aMNPDZvEhg5RjziFB000j2YKsSXHJxFkXr9lH2qNBloiJIGf83-pd1MzixXBE-SXdIuojjjlPoHHRyL0oZrbOn_CaNaf0LkrnTuRq9FQxO1EVGfqBoYNA09-rRRJDfGRMXR_DtcE9qq1XMuMkvxFxhEJIEKkSTrBY; expires=Sat, 07-Nov-2020 08:10:51 GMT; path=/; domain=.google.fr; Secure; HttpOnly; SameSite=none",
                                "Strict-Transport-Security": "max-age=31536000",
                                "Transfer-Encoding": "chunked",
                                "X-Frame-Options": "SAMEORIGIN",
                                "X-XSS-Protection": "0"},
           "scan_id": 14234419,
           "score": 25,
           "start_time": "Fri, 08 May 2020 08:10:49 GMT",
           "state": "FINISHED",
           "status_code": 200,
           "tests_failed": 6,
           "tests_passed": 6,
           "tests_quantity": 12}

RESULT = {"content-security-policy": {"expectation": "csp-implemented-with-no-unsafe",
                                      "name": "content-security-policy",
                                      "output":
                                      {"data": None,
                                       "http": False,
                                       "meta": False,
                                       "policy": None},
                                      "pass": False,
                                      "result": "csp-not-implemented",
                                      "score_description": "Content Security Policy (CSP) header not implemented",
                                      "score_modifier": 25}}


def test_print_analyse():
    reponse = print_analyse("google.com", ANALYSE)
    assert "Note" in reponse

    # test mauvais
    reponse = print_analyse("mauvais", {"mauvais": 1})
    assert "[ERROR]" in reponse


def test_print_result():
    reponse = print_scan(RESULT)
    assert "•" in reponse

    # test mauvais
    reponse = print_scan({"mauvais": 1})
    assert "[ERROR]" in reponse
    reponse = print_scan({"mauvais": {"mauvais": 1}})
    assert "[ERROR]" in reponse


def test_get_icon():
    assert get_icon(True) == "✅"
    assert get_icon(False) == "❌"
    assert get_icon("toto") == "✅"
    assert get_icon(None) == "❌"
