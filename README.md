# certbot-dns-name-com

A certbot DNS plugin for `Name.com`. Supports wildcard domains.

Copy `.env.example` file to `.env` and fill with your data

### Usage:

Clone project to `/usr/local` or copy files to `/usr/local/certbot-dns-name-com`, otherwise - correct paths in scripts

`$ chmod u+x /usr/local/certbot-dns-name-com/certbot_dns_auth.sh`

#### Check:

```console
$ certbot-auto \
    renew \
    --cert-name yourdomain.com \
    --manual-auth-hook "/usr/local/certbot-dns-name-com/certbot_dns_auth.sh add" \
    --manual-cleanup-hook "/usr/local/certbot-dns-name-com/certbot_dns_auth.sh clean" \
    --dry-run
```

#### Renew:

```console
$ certbot-auto \
    renew \
    --cert-name yourdomain.com \
    --manual-auth-hook "/usr/local/certbot-dns-name-com/certbot_dns_auth.sh add" \
    --manual-cleanup-hook "/usr/local/certbot-dns-name-com/certbot_dns_auth.sh clean"
```

### Manually Update Renewal Configuration

If you have already installed a certificate before using this plugin, and are not yet able to renew, you can still configure the hooks for the next renewal. This is not ideal, but there is no way via the certbot commands to update this without renewing or creating a new cert.

**Note: Manually editing the renewal configuration file for your certificate is discouraged by the LetsEncrypt team.**

Ensure these properties are added to your renewal configuration. The file is found in `/etc/letsencrypt/renewal/{{certname}}.conf`

```
pref_challs = dns-01,
authenticator = manual
manual_auth_hook = "/usr/local/certbot-dns-name-com/certbot_dns_auth.sh add"
manual_cleanup_hook = "/usr/local/certbot-dns-name-com/certbot_dns_auth.sh clean"
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
    --manual-cleanup-hook "/usr/local/certbot-dns-name-com/certbot_dns_auth.sh clean" \
    -m acme@yourdomain.com \
    -d example.yourdomain.com
```
