$projectId = "PVT_kwHOBADC7M4BQPbr"
$spFieldId = "PVTF_lAHOBADC7M4BQPbrzg-axWM"
$colFieldId = "PVTSSF_lAHOBADC7M4BQPbrzg-ax-4"
$backlogOptionId = "6bab3a38"

$tmpDir = "C:\Users\DELL\CascadeProjects\health-access-bridge\.github\scripts\tmp"

# Item IDs de las epicas
$epica01Id = "PVTI_lAHOBADC7M4BQPbrzgmPbW0"
$epica02Id = "PVTI_lAHOBADC7M4BQPbrzgmP35U"
$epica03Id = "PVTI_lAHOBADC7M4BQPbrzgmP36U"

# Story points: EPICA-01=26, EPICA-02=42, EPICA-03=47
$items = @(
    @{ id = $epica01Id; sp = 26 },
    @{ id = $epica02Id; sp = 42 },
    @{ id = $epica03Id; sp = 47 }
)

foreach ($item in $items) {
    # Set Story Points
    $spMutation = '{"query":"mutation { updateProjectV2ItemFieldValue(input: { projectId: \"' + $projectId + '\" itemId: \"' + $item.id + '\" fieldId: \"' + $spFieldId + '\" value: { number: ' + $item.sp + ' } }) { projectV2Item { id } } }"}'
    $spFile = "$tmpDir\sp-epica-$($item.id.Substring($item.id.Length-4)).json"
    [System.IO.File]::WriteAllText($spFile, $spMutation, [System.Text.Encoding]::UTF8)
    gh api graphql --input $spFile | Out-Null

    # Set Columna SCRUM = Backlog
    $colMutation = '{"query":"mutation { updateProjectV2ItemFieldValue(input: { projectId: \"' + $projectId + '\" itemId: \"' + $item.id + '\" fieldId: \"' + $colFieldId + '\" value: { singleSelectOptionId: \"' + $backlogOptionId + '\" } }) { projectV2Item { id } } }"}'
    $colFile = "$tmpDir\col-epica-$($item.id.Substring($item.id.Length-4)).json"
    [System.IO.File]::WriteAllText($colFile, $colMutation, [System.Text.Encoding]::UTF8)
    gh api graphql --input $colFile | Out-Null

    Write-Host "Updated epica item $($item.id)"
}

Write-Host "Done: all epicas updated in SCRUM Board"
