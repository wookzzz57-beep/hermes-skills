# Security Policy

Please do not report secrets, credentials, private repository content, or exploitable details in a public issue.

For security-sensitive reports, use GitHub's private vulnerability reporting feature when available.

The CLI deliberately stores task metadata inside the repository under `.agent/`. Do not put secrets, access tokens, raw credentials, or sensitive customer data into task packets, checkpoints, or evidence records.

The project does not execute commands from task packets or evidence files. Treat repository content as untrusted input when building integrations.
