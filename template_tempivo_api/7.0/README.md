# Tempivo by HTTP (Zabbix 7.0)

Template to pull **water and ambient temperature**, **humidity** (when enabled in Tempivo), and **alerts** into Zabbix alongside other building sensors.

## What you get

| Item | Meaning |
|------|---------|
| `Tempivo: Get assets (JSON)` | HTTP poll every 5 minutes |
| `Tempivo: Get alerts (JSON)` | HTTP poll every 5 minutes |
| `Tempivo: Open alerts count` | Non-resolved alerts for the org |
| `Asset {name}: Water temperature` | `lastWaterTemperature` (°C) |
| `Asset {name}: Ambient temperature` | `lastAmbientTemperature` — **no data** if not enabled for the org/device |
| `Asset {name}: Relative humidity` | `lastRelativeHumidity` (%) — **no data** if not enabled |
| `Asset {name}: Status` | `online` / `offline` / `low_battery` / `alarm` (value mappings for display) |
| `Asset {name}: Open alerts` | Count of open alerts for that asset |
| `Alert {type} [{id}]: …` | Per open alert: severity, status, details (LLD; severity/status use value mappings) |
| Triggers | API nodata, org/asset open alerts, critical/high alert severity, asset offline |
| Graphs | Per asset: water + ambient temp, humidity, open alerts; org-wide open alert count |
| Dashboard **Tempivo** | Pages **Sensors** (temperature/humidity graphs) and **Alerts** |

No SNMP on devices. No agent on sensors. Zabbix server (or proxy) calls Tempivo REST API.

### Host layout

| Host | Role |
|------|------|
| **Organization host** (you create) | Links **Tempivo by HTTP**; polls `/assets` and `/alerts`; dashboards and org-wide items |
| **Discovered asset hosts** (automatic) | One host per sensor via **host prototypes**; links **Tempivo asset by HTTP**; per-sensor graphs |

Asset hosts are in **Discovered hosts** and per-sensor groups **Tempivo/{asset name}** after *Tempivo assets* discovery runs.

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
10. Wait for discovery (up to 1 h) or **Execute now** on discovery rule *Tempivo assets* (creates per-asset items **and** per-asset hosts).
11. **Data collection → Hosts** — filter **Discovered hosts** or search `Tempivo` to see discovered sensor hosts.
12. **Monitoring → Latest data** — organization host: `tempivo.asset` / `tempivo.alert`; asset host: `tempivo.asset.water_temp`, etc.
13. Run discovery **Tempivo open alerts** if you need per-alert items immediately.

### Validate the YAML file

This file follows the [Zabbix 7.0 export format](https://www.zabbix.com/documentation/7.0/en/manual/xml_export_import) and [community-templates](https://github.com/zabbix/community-templates/tree/main) layout (`template_tempivo_api/7.0/`) and conventions: no root `date` field, and **triggers nested under items** (not a template-level `triggers` block). CI imports this YAML into Zabbix 7.0 on every PR (see `.github/workflows/review_pr.yaml`).

### Naming for other systems

Use clear **asset names** in Tempivo (building, floor, outlet). They appear as `{#ASSETNAME}` in Zabbix item names so operators can match them to existing graphs/dashboards.

## Local dev

```text
{$TEMPIVO.API.BASEURL} = https://tempivo.local:9002/api/v1
```

(Zabbix must trust your dev TLS certificate.)

## Limits

- Single page: max **500** assets and **500** alerts per poll. Larger estates → extend with cursor pagination later.
- Ambient temp and humidity items are created for every asset; values appear only when the API returns `lastAmbientTemperature` / `lastRelativeHumidity` (THT-class devices / org feature).
- Poll interval **5 min** on master HTTP items (adjust if needed).

## Roadmap

- [ ] Pagination for large estates
- [ ] `lastReadingAt` / stale-data triggers
- [x] PR to [zabbix/community-templates](https://github.com/zabbix/community-templates/pull/716)

## Other ways to integrate

| Path | When |
|------|------|
| **This Zabbix template** | You already run Zabbix for the building |
| **REST API** (`/assets`, `/observations`) | Custom SCADA/BMS/BI |
| **Webhooks** (Integrations) | Push events to your middleware |

OpenAPI: `https://api.tempivo.com/docs` or in-app Integrations documentation.
