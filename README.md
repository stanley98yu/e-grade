E-Grade
=======

Python script for emailing grades and feedback directly from a Google Drive spreadsheet. Written to make my life easier as a TA for CSEE 3827.

## Tools

* Used the [Google Drive REST API][gdrive-api] to pull grades and feedback from a spreadsheet on Google Drive.
* Used Python's built-in [smtplib][smtplib] module for sending emails using SMTP.

## Notes

* In order to allow the script to access your Google Drive files using OAuth 2.0, you must have access to valid Google API credentials. Visit the [Google API Console][gapi-console] to obtain OAuth 2.0 credentials.
* To run using Python 3, simply run `python grade.py` and follow the command-line instructions.

## Troubleshooting

* I receive an `smtplib.SMTPAuthenticationError` when trying to login to my Gmail account despite my account name and password being correct.
    * Google has flagged this method of logging in as "less secure", so you must specifically grant access to less secure apps using this [link][less-secure]. Note that if your Gmail account uses 2-Step Verification, this setting is not available. In this case, you must generate an [App Password][app-pass]

[app-pass]: https://support.google.com/accounts/answer/185833
[gapi-console]: https://console.developers.google.com
[gdrive-api]: https://developers.google.com/drive/
[less-secure]: https://www.google.com/settings/security/lesssecureapps
[smtplib]: https://docs.python.org/3/library/smtplib.html