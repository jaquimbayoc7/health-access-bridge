$tmpDir = "C:\Users\DELL\CascadeProjects\health-access-bridge\.github\scripts\tmp"

# HU-01 item ID en el proyecto
$hu01ItemId = "PVTI_lAHOBADC7M4BQPbrzgmPbmQ"
$projectId = "PVT_kwHOBADC7M4BQPbr"
$colFieldId = "PVTSSF_lAHOBADC7M4BQPbrzg-ax-4"
$inProgressOptionId = "778ca8a5"  # En Progreso

$colJson = '{"query":"mutation{updateProjectV2ItemFieldValue(input:{projectId:\"' + $projectId + '\",itemId:\"' + $hu01ItemId + '\",fieldId:\"' + $colFieldId + '\",value:{singleSelectOptionId:\"' + $inProgressOptionId + '\"}}){projectV2Item{id}}}"}'
$colFile = "$tmpDir\col-hu01-inprogress.json"
[System.IO.File]::WriteAllText($colFile, $colJson, (New-Object System.Text.UTF8Encoding $false))
$r = gh api graphql --input $colFile 2>&1
Write-Host "HU-01 -> En Progreso: $r"
