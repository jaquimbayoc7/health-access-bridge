$tmpDir = "C:\Users\DELL\CascadeProjects\health-access-bridge\.github\scripts\tmp"

$epicas = @(
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmPbW0"; sp = 26; label = "epica01" },
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmP35U"; sp = 42; label = "epica02" },
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmP36U"; sp = 47; label = "epica03" }
)

foreach ($e in $epicas) {
    # Story Points
    $spJson = '{"query":"mutation{updateProjectV2ItemFieldValue(input:{projectId:\"PVT_kwHOBADC7M4BQPbr\",itemId:\"' + $e.itemId + '\",fieldId:\"PVTF_lAHOBADC7M4BQPbrzg-axWM\",value:{number:' + $e.sp + '}}){projectV2Item{id}}}"}'
    $spFile = "$tmpDir\sp2-$($e.label).json"
    [System.IO.File]::WriteAllText($spFile, $spJson, (New-Object System.Text.UTF8Encoding $false))
    $r = gh api graphql --input $spFile 2>&1
    Write-Host "SP $($e.label): $r"

    # Columna SCRUM = Backlog
    $colJson = '{"query":"mutation{updateProjectV2ItemFieldValue(input:{projectId:\"PVT_kwHOBADC7M4BQPbr\",itemId:\"' + $e.itemId + '\",fieldId:\"PVTSSF_lAHOBADC7M4BQPbrzg-ax-4\",value:{singleSelectOptionId:\"6bab3a38\"}}){projectV2Item{id}}}"}'
    $colFile = "$tmpDir\col2-$($e.label).json"
    [System.IO.File]::WriteAllText($colFile, $colJson, (New-Object System.Text.UTF8Encoding $false))
    $r2 = gh api graphql --input $colFile 2>&1
    Write-Host "COL $($e.label): $r2"
}
Write-Host "Done"
