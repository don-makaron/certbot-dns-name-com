# certbot-dns-name-com

A certbot DNS plugin for `Name.com`. Supports wildcard domains.

Copy `.env.example` file to `.env` and fill with your data

### Usage:

Clone project to `/usr/local` or copy files to `/usr/local/certbot-dns-name-com`, otherwise - correct paths in scripts

`$ chmod u+x /usr/local/certbot-dns-name-com/certbot_dns_auth.sh`

check:  
```console
$ certbot-auto \
    renew \
    --cert-name yourdomain.com \
    --manual-auth-hook "/usr/local/certbot-dns-name-com/certbot_dns_auth.sh add" \
    --manual-cleanup-hook "/usr/local/certbot-dns-name-com/certbot_dns_auth.sh cleanup" \
    --dry-run
```

renew:  
```console
$ certbot-auto \
    renew \
    --cert-name yourdomain.com \
    --manual-auth-hook "/usr/local/certbot-dns-name-com/certbot_dns_auth.sh add" \
    --manual-cleanup-hook "/usr/local/certbot-dns-name-com/certbot_dns_auth.sh cleanup"
```

---

### Certonly:

```console
$ sudo certbot certonly \
    --server https://acme-v02.api.letsencrypt.org/directory \
    --agree-tos \
    --preferred-challenges dns-01 \
    --manual \
    --manual-public-ip-logging-ok \
    --manual-auth-hook "/usr/local/certbot-dns-name-com/certbot_dns_auth.sh add" \
    --manual-cleanup-hook "/usr/local/certbot-dns-name-com/certbot_dns_auth.sh cleanup" \
    -m acme@yourdomain.com \
    -d example.yourdomain.com
```
