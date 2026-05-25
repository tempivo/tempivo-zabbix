# Tempivo — Zabbix integration

Import this template to pull **water temperature (°C)** and **asset status** from the [Tempivo](https://tempivo.com) REST API into Zabbix (alongside your other building sensors).

## Quick start

1. Download or clone this repository.
2. Import **`7.0/template_tempivo_api.yaml`** in Zabbix 7.0+ (**Data collection → Templates → Import**).
3. Create a Zabbix host (one per Tempivo organization) and link template **Tempivo by HTTP**.
4. Set host macros:
   - `{$TEMPIVO.API.BASEURL}` = `https://api.tempivo.com/v1`
   - `{$TEMPIVO.API.KEY}` = your API key from **Integrations** in the Tempivo app (store as **secret**).
5. Run discovery **Tempivo assets** → check **Monitoring → Latest data**.

Full steps: **[7.0/README.md](7.0/README.md)**.

## Requirements

- Tempivo API key with permission to list assets (API integrations, Enterprise, or Cellular API on the organization).
- Zabbix server or proxy must reach `https://api.tempivo.com` over HTTPS.

## API documentation

- [https://api.tempivo.com/docs](https://api.tempivo.com/docs)

## License

MIT — see [LICENSE](LICENSE).
