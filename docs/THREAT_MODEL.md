# Threat Model

## Assets

- Host computer
- Laboratory event database
- Dashboard integrity
- User privacy

## Main Risks and Controls

| Risk | Control | Residual limitation |
| --- | --- | --- |
| Accidental internet exposure | Code rejects non-loopback binds | Local malware could still connect |
| Command execution | Payloads are classified only as strings | Future code must preserve this rule |
| Oversized input | Service reads at most 1,024 bytes | Many local connections can consume resources |
| Dashboard script injection | Payload previews are HTML-escaped; CSP is set | Dashboard is not independently authenticated |
| Sensitive data committed | Database and results are Git-ignored | Users must avoid real data in source files |
| Misclassification | Reasons, scores, and limitations are visible | Rules remain simplistic |

## Out of Scope

This version does not defend against a malicious local administrator, denial of
service, database tampering, operating-system compromise, or internet attackers.
