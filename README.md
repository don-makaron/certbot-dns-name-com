# certbot-dns-name-com

A certbot DNS plugin for `Name.com`. Supports wildcard domains.

Copy `.env.example` file to `.env` and fill with your data

### Usage:

Clone project to `/usr/local` or copy files to `/usr/local/certbot-dns-name-com`, otherwise - correct paths in scripts

check:
`$ certbot-auto renew --cert-name yourdomain.com --manual-auth-hook /usr/local/certbot-dns-name-com/certbot_dns_auth.sh --dry-run`

renew:
`$ certbot-auto renew --cert-name yourdomain.com --manual-auth-hook /usr/local/certbot-dns-name-com/certbot_dns_auth.sh`

