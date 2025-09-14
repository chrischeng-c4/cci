---
allowed-tools: ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Task", "TodoWrite", "WebSearch", "WebFetch"]
model: "claude-opus-4-1-20250805"
description: "Comprehensive security audit with threat modeling and automatic remediation"
argument-hint: "[--fix] [--level=<severity>] [--report-format=<type>]"
thinking-level: "ultrathink"
subagents: ["security-scanner", "vulnerability-analyzer", "threat-modeler", "remediation-expert"]
project-aware: true
---

# /cci-security

ultrathink about conducting a comprehensive security audit by analyzing code patterns, dependencies, configurations, secrets, and implementing automatic remediation strategies while maintaining detailed threat models.

## Project Context Integration

This command enforces CCI's security-first principles:
- Standards: Zero security vulnerabilities requirement from CLAUDE.md
- Architecture: Python application with CLI/TUI interfaces
- Dependencies: UV-managed packages requiring continuous monitoring
- Memory: Updates docs/security/ with audit history
- Compliance: Follows OWASP, CWE, and CVE standards

## Intelligent Security Analysis Strategy

### Phase 1: Threat Modeling & Risk Assessment

1. **Application Threat Model**
   @threat-modeler: Build comprehensive threat model:
   ```python
   threat_model = {
       "attack_surface": {
           "cli_inputs": "Command injection risks",
           "file_operations": "Path traversal vulnerabilities",
           "git_operations": "Code injection via commits",
           "network": "API key exposure, MITM attacks",
           "dependencies": "Supply chain attacks"
       },
       "threat_actors": ["External attackers", "Malicious dependencies"],
       "assets": ["Source code", "API keys", "User data", "Git history"],
       "risk_matrix": "Calculate likelihood × impact"
   }
   ```

2. **Context-Aware Risk Scoring**
   Evaluate risks based on project context:
   - Public vs private repository
   - Sensitive data handling
   - External API integrations
   - User privilege levels
   - Deployment environment

3. **Security Baseline**
   Establish and track security metrics:
   - Read docs/security/baseline.md
   - Compare against industry standards
   - Track improvement over time

### Phase 2: Deep Code Analysis

1. **Static Application Security Testing (SAST)**
   @security-scanner: Comprehensive code scanning:
   ```bash
   # Multiple security tools in parallel
   bandit -r src/ -f json -o bandit-report.json
   semgrep --config=auto src/
   safety check --json
   ```

2. **Pattern-Based Vulnerability Detection**
   Search for dangerous patterns:
   - SQL/NoSQL injection points
   - Command injection vulnerabilities
   - Path traversal risks
   - XSS/CSRF vulnerabilities
   - Insecure deserialization
   - Race conditions
   - Buffer overflows

3. **Custom Security Rules**
   Project-specific security checks:
   ```python
   custom_rules = [
       "No hardcoded API keys",
       "Input validation on all user inputs",
       "Secure subprocess execution",
       "No eval() or exec() usage",
       "Proper error handling without info leakage"
   ]
   ```

### Phase 3: Dependency & Supply Chain Security

1. **Dependency Vulnerability Scanning**
   @vulnerability-analyzer: Analyze all dependencies:
   ```bash
   # Check for known vulnerabilities
   pip-audit --desc --fix

   # License compliance check
   pip-licenses --with-urls

   # Dependency confusion check
   uv pip list --outdated
   ```

2. **Supply Chain Analysis**
   Verify dependency integrity:
   - Check package signatures
   - Verify maintainer reputation
   - Detect typosquatting attempts
   - Monitor for suspicious updates
   - Track transitive dependencies

3. **SBOM Generation**
   Create Software Bill of Materials:
   ```json
   {
       "packages": [...],
       "vulnerabilities": [...],
       "licenses": [...],
       "last_updated": "timestamp"
   }
   ```

### Phase 4: Secrets & Credential Detection

1. **Multi-Layer Secret Scanning**
   Comprehensive secret detection:
   ```bash
   # Git history scanning
   gitleaks detect --source . --verbose

   # Current codebase
   trufflehog filesystem . --json

   # Configuration files
   detect-secrets scan --all-files
   ```

2. **Intelligent Pattern Recognition**
   Detect various secret types:
   - API keys (AWS, GCP, Azure, etc.)
   - Database credentials
   - JWT tokens
   - SSH keys
   - Certificates
   - Webhook URLs
   - Encryption keys

3. **Secret Rotation Recommendations**
   For detected secrets:
   - Assess exposure risk
   - Generate rotation plan
   - Update documentation
   - Create secure storage strategy

### Phase 5: Configuration Security

1. **Security Misconfiguration Detection**
   Check configuration files:
   - CORS settings
   - Authentication configs
   - Logging verbosity
   - Debug mode flags
   - Default credentials
   - Insecure protocols

2. **Infrastructure as Code Security**
   If applicable, scan IaC:
   - Docker security
   - Kubernetes manifests
   - CI/CD pipelines
   - Cloud configurations

3. **Permission Analysis**
   File and process permissions:
   - Check file permissions
   - Validate execution rights
   - Review access controls

### Phase 6: Intelligent Remediation

1. **Automatic Fix Generation**
   @remediation-expert: Generate fixes:
   ```python
   remediation_strategies = {
       "input_validation": "Add sanitization functions",
       "sql_injection": "Use parameterized queries",
       "path_traversal": "Implement path validation",
       "weak_crypto": "Upgrade to secure algorithms",
       "hardcoded_secrets": "Move to environment variables"
   }
   ```

2. **Risk-Based Prioritization**
   Order fixes by severity:
   - Critical: Immediate action required
   - High: Fix within sprint
   - Medium: Plan for next release
   - Low: Track for future consideration

3. **Fix Validation**
   Verify remediation effectiveness:
   - Apply fixes in test environment
   - Re-run security scans
   - Validate no regressions
   - Update security baseline

### Phase 7: Reporting & Documentation

1. **Comprehensive Security Report**
   Generate detailed findings:
   ```markdown
   # Security Audit Report - [Date]

   ## Executive Summary
   - Overall Risk Score: [Critical|High|Medium|Low]
   - Vulnerabilities Found: X
   - Automatically Fixed: Y
   - Manual Review Required: Z

   ## Detailed Findings
   [Categorized vulnerabilities with remediation]

   ## Threat Model
   [Visual threat model diagram]

   ## Compliance Status
   - OWASP Top 10: [Status]
   - CWE Top 25: [Status]
   ```

2. **Update Project Memory**
   Document in docs/security/:
   - Audit history
   - Vulnerability trends
   - Remediation log
   - Security improvements

3. **Actionable Recommendations**
   Provide clear next steps:
   - Immediate actions
   - Short-term improvements
   - Long-term security roadmap
   - Training recommendations

## Self-Optimization Protocol

This command evolves its security capabilities:

1. **Learning from Patterns**
   - Build vulnerability pattern database
   - Track fix effectiveness
   - Improve detection accuracy
   - Reduce false positives

2. **Threat Intelligence Integration**
   - Monitor CVE databases
   - Track emerging threats
   - Update scanning rules
   - Adapt to new attack vectors

3. **Remediation Intelligence**
   - Learn successful fix patterns
   - Build remediation library
   - Improve fix suggestions
   - Track regression patterns

## Arguments

- `--fix`: Enable automatic remediation
- `--level=<severity>`: Minimum severity to report (critical|high|medium|low)
- `--report-format=<type>`: Output format (markdown|json|html|sarif)
- `--focus=<area>`: Specific security area (code|deps|secrets|config)
- `--compliance=<standard>`: Check specific compliance (owasp|cwe|pci)
- `--deep`: Enable deep scanning (slower but thorough)

## Subagent Specializations

### @security-scanner
- Expertise: SAST, pattern detection, code analysis
- Tools: Bandit, Semgrep, custom rules
- Output: Vulnerability findings

### @vulnerability-analyzer
- Expertise: CVE analysis, dependency security
- Tools: pip-audit, safety, OWASP dependency-check
- Output: Dependency risk assessment

### @threat-modeler
- Expertise: Attack surface analysis, risk assessment
- Tools: STRIDE, DREAD methodologies
- Output: Threat models and risk matrices

### @remediation-expert
- Expertise: Security fixes, best practices
- Tools: Auto-fix generators, secure coding patterns
- Output: Remediation code and guidance

## Enhanced Output Format

```
🔒 Security Audit - CCI Project
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Risk Assessment: MEDIUM
   Attack Surface: 7 entry points identified
   Threat Level: Standard (public repository)

🔍 Scanning Progress
  Code Analysis...        ████████████ Complete
  Dependency Check...     ████████████ Complete
  Secret Detection...     ████████████ Complete
  Config Security...      ████████████ Complete

📊 Findings Summary
  🔴 Critical: 0
  🟠 High: 2
  🟡 Medium: 5
  🟢 Low: 8
  ℹ️ Info: 12

🔴 High Severity Issues

1. Insecure Subprocess Execution
   File: src/cci/core/git.py:45
   Risk: Command injection possible

   Vulnerable Code:
   ```python
   subprocess.run(f"git {user_input}", shell=True)
   ```

   ✅ Auto-Fix Available:
   ```python
   subprocess.run(["git"] + shlex.split(user_input))
   ```

2. Hardcoded API Endpoint
   File: src/cci/services/api.py:12
   Risk: Information disclosure

   💡 Recommendation:
   Move to environment variable or config file

🟡 Medium Severity Issues

1. Missing Input Validation (3 instances)
2. Weak Random Number Generation (1 instance)
3. Verbose Error Messages (1 instance)

🔐 Secrets Scan: CLEAN
  ✅ No secrets detected in codebase
  ✅ Git history clean (last 100 commits)

📦 Dependency Analysis
  Total Dependencies: 23
  ⚠️ Outdated: 2
    - package1: 1.2.3 → 1.2.5 (security patch)
    - package2: 2.0.0 → 2.1.0 (bug fixes)

  ✅ No known vulnerabilities in dependencies
  ✅ All licenses compatible (MIT, Apache 2.0)

🛡️ Security Configuration
  ✅ Debug mode disabled
  ✅ Logging configured securely
  ✅ No default credentials
  ⚠️ Consider enabling rate limiting

🔧 Remediation Applied (--fix enabled)
  ✅ Fixed: 3 issues automatically
  ⏳ Manual Review: 2 high priority items
  📝 Generated: security-fixes.patch

📈 Security Posture
  Current Score: B+ (82/100)
  Previous Score: C+ (75/100)
  Improvement: +7 points

  Compliance:
  OWASP Top 10: 9/10 addressed
  CWE Top 25: 23/25 addressed

📄 Reports Generated
  - Full Report: reports/security-audit-2024-01-15.md
  - SARIF: reports/security.sarif
  - Fixes: patches/security-fixes.patch

✨ Recommendations
  1. Apply provided patches for high-severity issues
  2. Update outdated dependencies
  3. Implement rate limiting for API endpoints
  4. Add security headers to responses
  5. Consider security training for SQL injection

Memory Updated: docs/security/audit-2024-01-15.md
```

## Error Handling

1. **Tool Failures**
   - Fallback to alternative scanners
   - Partial results with warnings
   - Clear error descriptions

2. **False Positives**
   - Intelligent filtering
   - Context-aware analysis
   - Whitelist management

3. **Performance Issues**
   - Incremental scanning options
   - Cached results for unchanged files
   - Parallel execution optimization

## Integration Points

- `/cci-test`: Include security in test suite
- `/cci-implement`: Security-by-design in features
- `/cci-uat`: Security validation before release
- `/cci-status`: Security metrics in status
- CI/CD: Automated security gates

## Examples

### Quick Security Check
```
/cci-security
# Standard security audit with report
```

### Auto-Fix Security Issues
```
/cci-security --fix
# Scan and automatically fix what's possible
```

### Deep Security Analysis
```
/cci-security --deep --compliance=owasp
# Thorough scan with OWASP compliance check
```

### Dependency Focus
```
/cci-security --focus=deps --fix
# Focus on dependency vulnerabilities with fixes
```

## Continuous Intelligence

This command demonstrates advanced security capabilities:
1. **Threat Modeling**: Understands application-specific risks
2. **Multi-Layer Scanning**: Comprehensive security coverage
3. **Intelligent Remediation**: Context-aware fix generation
4. **Compliance Tracking**: Standards-based validation
5. **Continuous Learning**: Improves detection and fixes over time