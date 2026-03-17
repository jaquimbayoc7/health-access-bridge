$PROJECT_ID = "PVT_kwHOBADC7M4BQPbr"
$SP_FIELD_ID = "PVTF_lAHOBADC7M4BQPbrzg-axWM"
$COL_FIELD_ID = "PVTSSF_lAHOBADC7M4BQPbrzg-ax-4"
$BACKLOG_OPTION_ID = "6bab3a38"
$TMPFILE = "C:\Users\DELL\CascadeProjects\health-access-bridge\.github\scripts\tmp\query.json"

New-Item -ItemType Directory -Force -Path (Split-Path $TMPFILE) | Out-Null

function Invoke-GQL($jsonBody) {
    [System.IO.File]::WriteAllText($TMPFILE, $jsonBody, [System.Text.Encoding]::UTF8)
    return gh api graphql --input $TMPFILE
}

$issues = @(
    @{ id = "I_kwDORY973s7uLDeF"; sp = 0  },
    @{ id = "I_kwDORY973s7t8XF-"; sp = 8  },
    @{ id = "I_kwDORY973s7t8Xep"; sp = 13 },
    @{ id = "I_kwDORY973s7t8Xn7"; sp = 5  },
    @{ id = "I_kwDORY973s7t8X0W"; sp = 21 },
    @{ id = "I_kwDORY973s7t8X-0"; sp = 13 },
    @{ id = "I_kwDORY973s7t8YE4"; sp = 8  },
    @{ id = "I_kwDORY973s7t8YMB"; sp = 21 },
    @{ id = "I_kwDORY973s7t8YSB"; sp = 13 },
    @{ id = "I_kwDORY973s7t8YZM"; sp = 8  },
    @{ id = "I_kwDORY973s7t8Yqo"; sp = 5  }
)

foreach ($issue in $issues) {
    $issueId = $issue.id
    $sp = $issue.sp

    # Step 1: Add issue to project
    $q1 = '{"query":"mutation{addProjectV2ItemById(input:{projectId:\"' + $PROJECT_ID + '\",contentId:\"' + $issueId + '\"}){item{id}}}"}'
    $r1 = Invoke-GQL $q1
    $itemId = ($r1 | ConvertFrom-Json).data.addProjectV2ItemById.item.id
    Write-Host "Added $issueId -> $itemId"

    if (-not $itemId) { Write-Host "  ERROR: no itemId, skipping"; continue }

    # Step 2: Set Story Points
    $q2 = '{"query":"mutation{updateProjectV2ItemFieldValue(input:{projectId:\"' + $PROJECT_ID + '\",itemId:\"' + $itemId + '\",fieldId:\"' + $SP_FIELD_ID + '\",value:{number:' + $sp + '}}){projectV2Item{id}}}"}'
    Invoke-GQL $q2 | Out-Null
    Write-Host "  SP: $sp"

    # Step 3: Set Columna SCRUM = Backlog
    $q3 = '{"query":"mutation{updateProjectV2ItemFieldValue(input:{projectId:\"' + $PROJECT_ID + '\",itemId:\"' + $itemId + '\",fieldId:\"' + $COL_FIELD_ID + '\",value:{singleSelectOptionId:\"' + $BACKLOG_OPTION_ID + '\"}}){projectV2Item{id}}}"}'
    Invoke-GQL $q3 | Out-Null
    Write-Host "  Columna: Backlog"
}

Write-Host "Completado."
