# Ethical and Legal Safeguards

DecoyAI is designed only for authorized education on the computer running it.
This document is general project guidance, not legal advice.

## Mandatory Boundaries

- Bind the fake service and dashboard only to `127.0.0.1`.
- Use only the included simulator or other instructor-approved local inputs.
- Never enter or store real passwords, tokens, private keys, or personal data.
- Never expose the project using port forwarding, tunneling, or a public server.
- Never use collected data to retaliate, scan, exploit, or accuse another party.
- Do not represent classification as proof of malicious intent.

## Privacy Controls

- Input is limited to 1,024 bytes per interaction.
- Non-printable characters are replaced in previews.
- Dashboard content is HTML-escaped.
- Data stays in a local SQLite file.
- Generated databases and evaluation results are excluded from Git.

## Before Any Future Real Deployment

Obtain explicit written authorization, define scope and retention, isolate the
environment, consult institutional policy and applicable law, create an incident
response plan, minimize collected data, and obtain supervisor or ethics approval.
The current code is intentionally not designed for that deployment.
