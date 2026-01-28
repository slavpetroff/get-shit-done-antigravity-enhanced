# /sync-libs Workflow

<objective>
Synchronize GSD Library Intelligence with project dependencies.
</objective>

<process>

## 1. Scan and Fetch

**PowerShell:**

```powershell
python3 scripts/fetch_library_intel.py --scan
```

**Bash:**

```bash
python3 scripts/fetch_library_intel.py --scan
```

This will:

1. Scan `package.json` and `pyproject.toml`
2. Identify high-value libraries
3. Generate intelligence files in `.agent/libraries/` if missing

</process>
