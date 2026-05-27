# Tempivo — Zabbix integration

Import this template to pull **water and ambient temperature**, **humidity** (when enabled), **asset status**, and **alerts** from the [Tempivo](https://tempivo.com) REST API into Zabbix (alongside your other building sensors).

## Quick start

1. Download or clone this repository.
2. Import the YAML for your Zabbix version (**Data collection → Templates → Import**):
   - [7.0](template_tempivo_api/7.0/template_tempivo_api.yaml)
   - [7.4](template_tempivo_api/7.4/template_tempivo_api.yaml)
   - [8.0](template_tempivo_api/8.0/template_tempivo_api.yaml)
3. Create a Zabbix host (one per Tempivo organization) and link template **Tempivo by HTTP**.
4. Set host macros:
   - `{$TEMPIVO.API.BASEURL}` = `https://api.tempivo.com/v1`
   - `{$TEMPIVO.API.KEY}` = your API key from **Integrations** in the Tempivo app (store as **secret**).
5. Run discovery **Tempivo assets** → check **Monitoring → Latest data**.

Full steps: **[template_tempivo_api/7.0/README.md](template_tempivo_api/7.0/README.md)**.

Pull requests import each version into Zabbix 7.0, 7.4, and 8.0 in CI (same checks as [zabbix/community-templates](https://github.com/zabbix/community-templates)).

## Requirements

- Tempivo API key with permission to list assets (API integrations, Enterprise, or Cellular API on the organization).
- Zabbix server or proxy must reach `https://api.tempivo.com` over HTTPS.

## API documentation

- [https://api.tempivo.com/docs](https://api.tempivo.com/docs)

## License

MIT — see [LICENSE](LICENSE).
