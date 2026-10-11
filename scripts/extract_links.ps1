$content = [System.IO.File]::ReadAllText('C:\Users\Sam\.gemini\antigravity\brain\423a7e7c-328c-4da5-b6e6-81eca21f020c\.system_generated\logs\transcript_full.jsonl', [System.Text.Encoding]::UTF8)
$pattern = '\[(\\\\?\[?\d{6}\\\\?\]?[^\]\)]+)\]\((https://drive\.google\.com/file/d/[^\)\s]+)\)'
$regex = New-Object System.Text.RegularExpressions.Regex($pattern)
$matches = $regex.Matches($content)
$results = @()
$seen = @{}
foreach ($m in $matches) {
    $t = $m.Groups[1].Value.Replace('\[', '[').Replace('\]', ']').Trim()
    $u = $m.Groups[2].Value.Trim()
    if (-not $seen.ContainsKey($u)) {
        $seen[$u] = $true
        $results += [PSCustomObject]@{ Title = $t; Url = $u }
    }
}
$json = $results | ConvertTo-Json -Depth 3
[System.IO.File]::WriteAllText('C:\Users\Sam\Documents\GitHub\homelab-ops\scripts\gdrive_all.json', $json, [System.Text.Encoding]::UTF8)
Write-Output "Extracted: $($results.Count)"
