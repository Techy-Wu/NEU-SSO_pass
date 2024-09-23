# NEU-SSO_pass

A python lib / programme for sso authentcation of NEU (Smart NEU Universal Authentication)

智慧东大统一身份认证库/程序

## Usage

### Calling by python

Import this lib into your script environment and simply use function sso_pass() to get pass url

### Calling by system command

Run this script with python and get pass url from output shell

## Variables

| Function Variable | CMD Key     | Description                      |
| ----------------- | ----------- | -------------------------------- |
| user_name         | -n / --name | Login user name                  |
| password          | -p / --pwd  | Login password                   |
| inquiry_url       | -u / --url  | URL of inquiry app               |
| plain_headers     | -j / --json | Default Headers, e.g. User-Agent |
| \                 | -w / --warn | Switch whether show warnings     |

For 'plain_headers', input a dict if you are using Python calling otherwise specify a json file path with headers

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](./LICENSE) file for details.