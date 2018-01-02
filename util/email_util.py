from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
# from __future__ import unicode_literals
#
# from builtins import str
# from past.builtins import basestring


# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import importlib
import logging
import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate
from util.email_conf import SMTP_HOST as C_SMTP_HOST\
    , SMTP_PORT as C_SMTP_PORT\
    , SMTP_USER as C_SMTP_USER\
    , SMTP_PASSWORD as C_SMTP_PASSWORD\
    , SMTP_STARTTLS as C_SMTP_STARTTLS\
    , SMTP_SSL as C_SMTP_SSL\
    , SMTP_MAIL_FROM as C_SMTP_MAIL_FROM

# from airflow import configuration

def send_email_smtp(to, subject, html_content, files=None, dryrun=False):
    """
    Send an email with html content

    # >>> send_email('test@example.com', 'foo', '<b>Foo</b> bar', ['/dev/null'], dryrun=True)
    """
    SMTP_MAIL_FROM = C_SMTP_MAIL_FROM

    if isinstance(to, basestring):
        if ',' in to:
            to = to.split(',')
        elif ';' in to:
            to = to.split(';')
        else:
            to = [to]

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SMTP_MAIL_FROM
    msg['To'] = ", ".join(to)
    msg['Date'] = formatdate(localtime=True)
    #mime_text = MIMEText(html_content, 'html')
    # mime_text.set_charset('utf-8')
    mime_text = MIMEText(html_content, _subtype='html', _charset="utf-8")
    #mime_text = MIMEText(html_content, _subtype='html', _charset='utf-8')
    #mime_text = MIMEText(html_content,  _charset="utf-8")
    msg.attach(mime_text)

    for fname in files or []:
        basename = os.path.basename(fname)
        with open(fname, "rb") as f:
            msg.attach(MIMEApplication(
                f.read(),
                Content_Disposition='attachment; filename="%s"' % basename,
                Name=basename
            ))

    send_MIME_email(SMTP_MAIL_FROM, to, msg, dryrun)


def send_MIME_email(e_from, e_to, mime_msg, dryrun=False):
    SMTP_HOST = C_SMTP_HOST
    SMTP_PORT = C_SMTP_PORT
    SMTP_USER = C_SMTP_USER
    SMTP_PASSWORD = C_SMTP_PASSWORD
    SMTP_STARTTLS = C_SMTP_STARTTLS
    SMTP_SSL = C_SMTP_SSL

    if not dryrun:
        s = smtplib.SMTP_SSL(
            SMTP_HOST,
            SMTP_PORT) if SMTP_SSL else smtplib.SMTP(
            SMTP_HOST,
            SMTP_PORT)
        if SMTP_STARTTLS:
            s.starttls()
        if SMTP_USER and SMTP_PASSWORD:
            s.login(SMTP_USER, SMTP_PASSWORD)
        logging.info("Sent an alert email to " + str(e_to))
        s.sendmail(e_from, e_to, mime_msg.as_string())
        s.quit()

