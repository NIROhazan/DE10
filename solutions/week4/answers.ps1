# Week 4 ex8..ex10 (the console questions): a student's own questions and the right answers (instructor only).
#   answers.bat w4-ex9 3160009489       -> every question as the student sees it on the first try, with the answer
#   answers.ps1 ex9 3160009489 -K 2     -> the numbers after 2 wrong tries (results.txt shows the try number)
# Hidden board answers (ex8 delays, ex9 functions) come from key.json, written by gen_w4.py next to ANSWERS.md.
# Week 4 ex1..ex7 (K-maps, truth tables) go through ..\answers.ps1 like week 3.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.
param([Parameter(Mandatory = $true)][string]$Ex, [Parameter(Mandatory = $true)][string]$Sid, [int]$K = 0, [string]$Repo = "C:\DE10\week4")
$ErrorActionPreference = "Stop"
$name = $Ex.ToLower()
$dir = Join-Path $Repo $name
if (-not (Test-Path (Join-Path $dir "tools\questions.ps1"))) { Write-Host "No $name under $Repo"; exit 1 }
$script:Ex = "w4-$name"		# the label: seeds the numbers, names the codes
. (Join-Path $dir "tools\common.ps1")
. (Join-Path $dir "tools\questions.ps1")
Read-Secrets
$keyFile = Join-Path $PSScriptRoot "$name\key.json"
$key = @{}
if (Test-Path $keyFile) { (Get-Content $keyFile -Raw | ConvertFrom-Json).PSObject.Properties | ForEach-Object { $key[$_.Name] = $_.Value } }

Write-Host "$($script:Ex)   ID $Sid   try $($K + 1)"
foreach ($item in Get-QuestionList) {
	$q = Get-Question $Sid $item.Id $K
	$ans = @($q.Checks | ForEach-Object { if ($_.Secret) { $key[$_.Secret] } else { $_.Value } }) -join "   "
	# a SOP answer is checked by its truth table + cost; key.json keeps one expression to show (and to test with)
	if ($q.Checks[0].Parts -contains "sop") { $ans = $key["expr|" + $(if ($q.Checks[0].Secret) { $q.Checks[0].Secret } else { $q.Asked })] }
	Write-Host ""
	Write-Host "$($item.Id) $($item.Name):  $($q.Lines -join ' / ')"
	Write-Host "   answer: $ans    code: $(Get-Code $Sid "$($script:Ex)-$($item.Id)")"
	# Machine-readable line for tests: ANSWER Qn <answer>
	if ($env:W4_TEST) { Write-Output "ANSWER $($item.Id) $ans" }
}
