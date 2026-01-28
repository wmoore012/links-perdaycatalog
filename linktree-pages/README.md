Links — CatalogLAB™

This is a minimal, static LinkTree for `links.perdaycatalog.com` intended for Cloudflare Pages.

How to use locally:

```bash
# serve locally (any static server) e.g.
npx serve .
```

Cloudflare Pages setup (recommended):
- Create a new Pages project in Cloudflare Dashboard.
- Connect the repository created below.
- Build command: (leave empty)
- Output directory: `/` or `.`

DNS quick-setup (2 minutes):
1. In your DNS provider add a CNAME for `links` pointing to the Pages subdomain Cloudflare assigns (shown during Pages setup).
2. Wait a few minutes for propagation; Cloudflare will handle TLS.

Repository: push this folder to a new GitHub repo and create a Pages project.
