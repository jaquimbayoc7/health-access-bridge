$tmpDir = "C:\Users\DELL\CascadeProjects\health-access-bridge\.github\scripts\tmp"
$projectId = "PVT_kwHOBADC7M4BQPbr"
$colFieldId = "PVTSSF_lAHOBADC7M4BQPbrzg-ax-4"

# Columnas
$backlog      = "6bab3a38"
$inProgress   = "778ca8a5"
$done         = "fac746cc"

# Item IDs del proyecto (obtenidos previamente)
$items = @(
    # EPICA-01 -> Done (ya cerrada)
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmPbW0"; col = $done;       label = "EPICA-01" },
    # HU-01 -> En Progreso (backend listo, frontend pendiente)
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmPbmQ"; col = $inProgress; label = "HU-01" },
    # HU-02 -> Backlog
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmPbmo"; col = $backlog;    label = "HU-02" },
    # HU-03 -> Backlog
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmPbnE"; col = $backlog;    label = "HU-03" },
    # HU-04 -> En Progreso (modelo predictivo integrado en HybridModelDisability)
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmPbng"; col = $inProgress; label = "HU-04" },
    # HU-05 -> Backlog
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmPbnw"; col = $backlog;    label = "HU-05" },
    # HU-06 -> Backlog
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmPboM"; col = $backlog;    label = "HU-06" },
    # HU-07 -> Backlog
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmPbok"; col = $backlog;    label = "HU-07" },
    # HU-08 -> Backlog
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmPbo0"; col = $backlog;    label = "HU-08" },
    # HU-09 -> Backlog
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmPbpA"; col = $backlog;    label = "HU-09" },
    # HU-10 -> Backlog
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmPbpc"; col = $backlog;    label = "HU-10" },
    # EPICA-02 -> Backlog
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmP35U"; col = $backlog;    label = "EPICA-02" },
    # EPICA-03 -> Backlog
    @{ itemId = "PVTI_lAHOBADC7M4BQPbrzgmP36U"; col = $backlog;    label = "EPICA-03" }
)

foreach ($item in $items) {
    $json = '{"query":"mutation{updateProjectV2ItemFieldValue(input:{projectId:\"' + $projectId + '\",itemId:\"' + $item.itemId + '\",fieldId:\"' + $colFieldId + '\",value:{singleSelectOptionId:\"' + $item.col + '\"}}){projectV2Item{id}}}"}'
    $file = "$tmpDir\kanban-$($item.label).json"
    [System.IO.File]::WriteAllText($file, $json, (New-Object System.Text.UTF8Encoding $false))
    $r = gh api graphql --input $file 2>&1
    if ($r -match '"id"') {
        Write-Host "OK  $($item.label)"
    } else {
        Write-Host "ERR $($item.label): $r"
    }
}
Write-Host "Done."
