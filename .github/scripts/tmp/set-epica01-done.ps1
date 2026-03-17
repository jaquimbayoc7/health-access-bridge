$tmpDir = "C:\Users\DELL\CascadeProjects\health-access-bridge\.github\scripts\tmp"

# EPICA-01 item ID en el proyecto
$epica01ItemId = "PVTI_lAHOBADC7M4BQPbrzgmPbW0"
$projectId = "PVT_kwHOBADC7M4BQPbr"
$colFieldId = "PVTSSF_lAHOBADC7M4BQPbrzg-ax-4"
$doneOptionId = "fac746cc"  # Done

# Mover EPICA-01 a Done
$colJson = '{"query":"mutation{updateProjectV2ItemFieldValue(input:{projectId:\"' + $projectId + '\",itemId:\"' + $epica01ItemId + '\",fieldId:\"' + $colFieldId + '\",value:{singleSelectOptionId:\"' + $doneOptionId + '\"}}){projectV2Item{id}}}"}'
$colFile = "$tmpDir\col-epica01-done.json"
[System.IO.File]::WriteAllText($colFile, $colJson, (New-Object System.Text.UTF8Encoding $false))
$r = gh api graphql --input $colFile 2>&1
Write-Host "EPICA-01 -> Done: $r"
