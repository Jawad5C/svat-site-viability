# SVAT — Site Viability Assessment Tool

Data-driven site assessment for green hydrogen projects. Answer **"Is this the right place to build?"** before the first dollar is spent.

> *"Every single reason a green hydrogen project fails can be assessed before the first dollar is spent. The data has always existed. Nobody built the tool to pull it together — until now."*

---

## The problem

- **$700B** is allocated to green hydrogen projects; only **7%** of announced projects finish on time.
- Projects drop at every stage: **100% announced → 20% reach FID → 12% under construction → 7% complete on schedule.**
- Root cause: **lack of site-level data** before capital is committed. It’s an information problem, not only a funding problem.

## What SVAT does

SVAT gives developers and investors a **site assessment before they commit** — so they can see what the data says about what makes hydrogen projects succeed or fail at each stage.

**MVP scope:** United States only. International scope is deferred to a later release.

---

## Three assessment options (where you are in your project)

| You are… | What we show |
|----------|----------------|
| **Haven’t started yet** | Full assessment — all metrics across all three gaps |
| **Have funding (past FID)** | Metrics that matter before/during construction (Gap 2) |
| **Already building** | Metrics that matter to finish on time (Gap 3) |

---

## Gaps and metrics (what we measure)

### Gap 1 — Announced → FID (80% of projects die here)
- **Buyers nearby?** (demand proximity)
- **Can we connect to the grid?** (grid availability)
- **What support can we get?** (policy & subsidy matcher)
- **Cost to produce here** (LCOH calculator)

### Gap 2 — FID → Construction (8% die here)
- **Ports, roads, pipelines** (infrastructure proximity)
- **Water available?** (water stress index)
- **Sun and wind at this site** (renewable resource data, e.g. NASA)

### Gap 3 — Construction → Complete (5% die here)
- **Financing risk in this region** (regional risk score)
- **Will electricity stay affordable?** (electricity price stability)
- **Can we get what we need?** (supply chain proximity)

If a metric is too hard or needs an API we can’t get, we either omit it or **suggest further research** (plain-language message; no score).

---

## Architecture

- **Backend:** API and all assessment logic. Versioned REST API; OpenAPI spec as the contract.
- **Frontend:** Separate; partners can replace or customize the UI. Any client that calls the API is valid.
- **Data (examples):** NASA POWER (solar/wind), WRI Aqueduct (water), IRA / US federal programs (policy), proximity data (grid, ports, buyers).

---

## Repo structure

- `backend/` — API and assessment logic (owner-maintained)
- Frontend lives in a separate repo or is owned by partners.

## License

TBD.
