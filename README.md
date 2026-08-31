# Full School Website + Server

A Flask school website with a database and CMS.

## Public pages
Home, About, Staff, News, Events, Gallery, Downloads, Contact.

## Admin CMS
Edit school information; upload logo and homepage image; manage staff, news, events, gallery photos and documents; read contact messages.

## Install
CMD:

    cd /d C:\Users\USER\Downloads\school_website_full
    py -m venv venv
    venv\Scripts\activate
    python -m pip install -r requirements.txt
    python seed.py
    python app.py

Or double-click `install.bat`, then `run_server.bat`.

Website: http://127.0.0.1:5000
Admin: http://127.0.0.1:5000/admin/login
Username: admin
Password: admin123

Database: instance\\school.db
Uploads: static\\uploads\\

For another PC/phone on the same network, use the server PC's IPv4 address, e.g. http://192.168.x.x:5000. Allow TCP 5000 through Windows Firewall if needed.

Change the default password and SECRET_KEY before public internet deployment.


## Institution configuration
This version is configured for KAIMOSI NATIONAL POLYTECHNIC – MBALE TOWN CAMPUS.
Official institutional facts, contact details, course lists, logos and photographs should be entered/verified through the CMS rather than invented.

## CMS v2
Added a professional responsive admin dashboard and dynamic homepage hero image support.
