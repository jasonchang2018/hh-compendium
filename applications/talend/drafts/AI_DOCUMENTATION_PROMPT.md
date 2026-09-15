# AI Documentation Enrichment Prompt

Use this prompt when feeding the extracted metadata to Claude or another AI.

---

## Prompt Template

```
You are a senior data platform engineer and technical writer, experienced in
Talend ETL and Qlik Cloud BI, who specializes in reverse-engineering
undocumented systems from implementation metadata alone. Write for the
engineers who now own this platform: be precise, avoid speculation presented
as fact, and call out anything that looks risky or undocumented-by-design.

I have extracted metadata from our Qlik + Talend data platform. The original
developer has left and there is no documentation. I need you to generate
comprehensive technical documentation from these metadata files.

The attached JSON files contain:
- @full-documentation\output\talend_metadata.json — Talend ETL job definitions (components, connections, schemas, context variables)

If you have file-write access in this repository (e.g. you are running as
Claude Code or another CLI coding agent, invoked from the repository root),
write each document directly to the file path given with it below,
overwriting that file's existing content, instead of only printing it in
this conversation. If you do not have file-write access (e.g. a plain
chat/API session with no filesystem), print each document under a heading
matching its file path so a human can save it by hand. File paths below are
relative to `documentation/`.

Please generate:

All six documents below should read as plain-English explainers a
non-Talend/non-Qlik engineer could follow — not just restructured metadata.
Where a section below asks for a table, technical term, or diagram, translate
jargon rather than repeating field names verbatim, and ground every claim in
the attached JSON (never invent a name, date, or setting).

1. **System Architecture Document** — **File:** `01_system_architecture.md`
   - **Overview** — one short paragraph on what the platform does end to end
     (sources → Talend ETL → Snowflake → Qlik Cloud).
   - **Detail table** — project/tenant name, total Talend jobs, total DB
     connections, total Qlik apps (use the extracted summary counts; omit a
     row if the metadata has none).
   - **Data flow** — the overall path from sources through Talend ETL into
     Snowflake and out to Qlik dashboards, as a Mermaid diagram.
   - **Glossary** — a short table translating recurring platform terms
     (e.g. Space, Reload task, Context group) into plain English.

2. **Job-by-Job Documentation** — **Files:** one per Talend job, at
   `talend/<ProjectName>/job_<JobName>.md` (same project and job names as in
   @full-documentation\output\talend_metadata.json). For each job, write a plain-English explainer
   using this structure:
   - **Overview** — one short paragraph on what the job does end to end.
   - **Detail table** — Job name, Version, Project, Author, Created, Last
     Modified (use the extracted values; omit a row if the metadata has none
     — never invent a name or date).
   - **Step-by-step data flow** — each stage in plain English (what it reads,
     what it changes, what it writes), not just a component list. Also, add it as a Mermaid diagram.
   - **Settings tables** — for each source/target component, show its
     configuration alongside a "what it means" column in plain English.
   - **Dependencies & configuration** — which other jobs it triggers or
     depends on, and which context variables it relies on and why.
   - **Glossary** — a short table translating the Talend component types used
     in this job (e.g. `tMap`, `tFileInputDelimited`) into plain English.
   - **Issues observed** (only if evident from the provided metadata, e.g.
     an unmapped/disconnected column, a missing schema) — state the specific
     evidence for the concern; do not speculate beyond what the metadata shows.

3. **Qlik App Documentation** — **Files:** one per Qlik app, at
   `qlik/app_<AppName>.md` (same app names as in @qlik_metadata.json). For
   each app, write a plain-English explainer using this structure:
   - **Overview** — one short paragraph on what the app is for and who it's
     likely for, based on its name/space.
   - **Detail table** — App name, Space, Published status (use extracted
     values; omit a row if the metadata has none).
   - **Data model** — what data it loads and from where, and the
     tables/relationships, in plain English rather than raw load-script text.
   - **Settings table** — data connections and reload schedule, alongside a
     "what it means" column.
   - **Glossary** — a short table translating Qlik-specific terms used (e.g.
     Load script, Resident table, Reload task) into plain English.
   - **Issues observed** (only if evident from the provided metadata) —
     state the specific evidence; do not speculate beyond it.

4. **Data Lineage Map** — **File:** `04_data_lineage_map.md`
   - **Overview** — one short paragraph on how to read the lineage trace
     that follows.
   - **Trace** — source → Talend job → Snowflake table → Qlik app, as a
     Mermaid flowchart, plus a plain-English walkthrough of each hop.
   - **Gaps** — any point in the chain that could not be determined from the
     metadata, stated explicitly as unknown rather than inferred.

5. **Operational Runbook** — **File:** `05_operational_runbook.md`
   - **Overview** — one short paragraph on what this runbook covers.
   - **How-to sections** — numbered, plain-English steps for: monitoring job
     / reload status, restarting a failed job, and troubleshooting the most
     likely failure modes evident from the metadata (e.g. missing schema,
     hardcoded connection values).
   - **Glossary** — a short table translating any ops-specific terms used
     that weren't already covered in the Job or Qlik App glossaries.

6. **Dependency Matrix** — **File:** `06_dependency_matrix.md`
   - **Overview** — one short paragraph on what the matrix shows and how to
     read it.
   - **Matrix table** — which jobs depend on which connections and context
     groups.
   - **Notes** — plain-English callouts for anything in the matrix that
     looks risky (e.g. many jobs sharing one connection, a job with no
     visible dependencies that seems like it should have some).

IMPORTANT:
- Do NOT invent information. If something cannot be determined from the
  metadata, say "Unable to determine from metadata — verify with team."
- Flag any components or patterns that look unusual or risky.
- Identify any hardcoded values that should be parameterized.
```

---

If you're already running as Claude Code (or another CLI coding agent) in
this repository, just run the prompt above directly — it will write the six
documents straight into `documentation/`. Otherwise, copy the prompt above,
attach the JSON files, send it to Claude, and save each document it prints
into the matching file path under `documentation/` by hand.
