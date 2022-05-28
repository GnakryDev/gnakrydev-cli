# Gnakrydev-cli

CLI tool in order to interact with the gnakrydev mobile app.

## Simple notification

``` bash
usage: gnakrydev message [-h] --apikey APIKEY --title TITLE --content CONTENT [--type TYPE]

optional arguments:
  -h, --help         show this help message and exit
  --apikey APIKEY    apiKey available on the mobile-app
  --title TITLE      Message title
  --content CONTENT  Message content
  --type TYPE        Message type: info, warning, success, error. Default= info
```
## Website Health-Check
``` bash
usage: gnakrydev health [-h] --config CONFIG --apikey APIKEY [--verbose]

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  YML config file
  --apikey APIKEY  apiKey available on the mobile-app
  --verbose        Show request details in stdout
```

``` yaml
endpoints:
  - name: "SG-Mooc"
    url: https://mooc.savoirguinee.com/

  - name: "Meteo-Guinée"
    url: https://meteoguinee.net/
```

## Contributing
