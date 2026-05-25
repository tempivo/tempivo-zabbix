# Tempivo by HTTP (Zabbix 7.0)

Minimal template to pull **water temperature (°C)** from Tempivo into Zabbix so a property owner can see it **next to other building sensors** (HVAC, energy, access, and so on) in one monitoring stack.

## What you get (v1)

| Item | Meaning |
|------|---------|
| `Tempivo: Get assets (JSON)` | One HTTP poll every 5 minutes |
| `Asset {name}: Water temperature` | `lastWaterTemperature` per sensor (LLD) |
| `Asset {name}: Status` | `online` / `offline` / `low_battery` / `alarm` |
| Trigger | No API data for 30 minutes |

No SNMP on devices. No agent on sensors. Zabbix server (or proxy) calls Tempivo REST API.

## Prerequisites

1. **API key** — Tempivo app → **Integrations** → generate key.
2. **Permission to list assets** — API integrations add-on, Enterprise plan, or Cellular API (same key as integrations docs).
3. **Zabbix 7.0+** with HTTP agent (server or proxy must reach `api.tempivo.com`).

## Quick start (Zabbix UI import)

Follow [Importing templates](https://www.zabbix.com/documentation/current/en/manual/xml_export_import/templates#importing):

1. Go to **Data collection → Templates**.
2. Click **Import** (upper-right).
3. Select `template_tempivo_api.yaml` (YAML is the default export format).
4. Click **Import** on the form.
5. **First import:** defaults are fine (creates the new template). For a **re-import** after you changed the YAML, open **Advanced options** and use **Update existing** + **Create new**; enable **Delete missing** only if you want a clean replace (removes old template items and their history).
6. On the review screen, check that elements are green (new) or as expected, then confirm **Import**. A success or failure message is shown in the UI.
7. Create a host, e.g. `Tempivo – {organization name}` (one host per Tempivo org).
8. **Data collection → Templates** → link **Tempivo by HTTP** to that host (or add the template on the host’s **Templates** tab).
9. On the host, set macros (host-level overrides template defaults):
   - `{$TEMPIVO.API.BASEURL}` = `https://api.tempivo.com/v1`
   - `{$TEMPIVO.API.KEY}` = your `sk_live_…` key (use **Secret** macro type in the UI)
10. Wait for discovery (up to 1 h) or **Execute now** on discovery rule *Tempivo assets*.
11. **Monitoring → Latest data** — filter by `tempivo.asset.water_temp`.

### Validate the YAML file

This file was written to match the [export format](https://www.zabbix.com/documentation/current/en/manual/xml_export_import/templates#export-format) (`zabbix_export`, `version`, UUIDs, template groups). It was **not** exported from a live Zabbix instance. If import fails, build the same logic in the UI on Zabbix 7.0+ and **Export → YAML**, then replace this file (that is the most reliable way to match the manual).

### Naming for other systems

Use clear **asset names** in Tempivo (building, floor, outlet). They appear as `{#ASSETNAME}` in Zabbix item names so operators can match them to existing graphs/dashboards.

## Local dev

```text
{$TEMPIVO.API.BASEURL} = https://tempivo.local:9002/api/v1
```

(Zabbix must trust your dev TLS certificate.)

## Limits (v1)

- Single page: max **500** assets per poll. More than 500 → extend template later (cursor pagination).
- Temperature only (not ambient/humidity unless add-on exposes them in API).
- Poll interval **5 min** (adjust on master item if needed).

## Roadmap (extend this template)

- [ ] Pagination for large estates
- [ ] `lastReadingAt` / stale-data triggers
- [ ] Open alerts count (`GET /alerts`)
- [ ] Ambient temp & humidity items
- [ ] PR to [zabbix/community-templates](https://github.com/zabbix/community-templates)

## Other ways to integrate

| Path | When |
|------|------|
| **This Zabbix template** | You already run Zabbix for the building |
| **REST API** (`/assets`, `/observations`) | Custom SCADA/BMS/BI |
| **Webhooks** (Integrations) | Push events to your middleware |

OpenAPI: `https://api.tempivo.com/docs` or in-app Integrations documentation.
