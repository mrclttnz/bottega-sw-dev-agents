---
name: security-audit
description: Full security audit of the project (SAST, secrets in git history, dependencies, containers, IaC, configuration, pipeline, threat model verification and optional DAST on staging) with a release-readiness verdict. Use before every release, periodically, or when you want a snapshot of the security posture.
argument-hint: "[full | dependencies | secrets | config] (empty = full)"
---

# Security audit

Rules: `${CLAUDE_PLUGIN_ROOT}/references/security-standard.md` and `${CLAUDE_PLUGIN_ROOT}/references/review-contract.md`. Scope: `$ARGUMENTS`.

1. **Tools.** Check which ones are installed:
   ```bash
   for t in gitleaks semgrep trivy osv-scanner; do command -v "$t" >/dev/null && echo "OK  $t" || echo "--  $t"; done
   ```
   If tools relevant to the stack are missing, propose how to install them (system package, `pipx`, or official Docker image) and ask for consent before doing so. An audit run without tools must be declared **partial**.
2. **Audit.** Delegate to `bottega:security-engineer` in mode C (or limited to the requested scope), stating which tools are available and whether a staging environment exists for DAST.
3. **Summary for the user:**
   - the verdict: **FIT FOR RELEASE** or **NOT FIT FOR RELEASE**
   - finding counts by severity
   - the BLOCKERs explained in plain words: what an attacker could do, and what the fix is
   - the threat-model THRs not yet verified by a test
4. **Fixes.** Delegate each BLOCKER to the right developer or to devops, then run the security engineer again in re-check mode. Gate G6 stays closed until the verdict is FIT FOR RELEASE.
5. Update `docs/STATUS.md` with the date, verdict and report path.
