E-Grade
=======

Python script for emailing grades and feedback directly from a Google Drive spreadsheet. Written to make my life easier as a TA for CSEE 3827.

## Tools

* Used the [Google Drive REST API][gdrive-api] to pull grades and feedback from a spreadsheet on Google Drive.

## Notes

* In order to allow the script to access your Google Drive files using OAuth 2.0, you must have access to valid Google API credentials. Visit the [Google API Console][gapi-console] to obtain OAuth 2.0 credentials.

[gapi-console]: https://console.developers.google.com
[gdrive-api]: https://developers.google.com/drive/