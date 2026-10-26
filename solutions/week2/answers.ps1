# Week 2 (week2\ex1..ex6): a student's own questions and the right answers (instructor only).
#   answers.bat w2-ex5 3160009489        -> every question as the student sees it on the first try, with the answer
#   answers.ps1 ex5 3160009489 -K 2   -> the numbers after 2 wrong tries (results.txt shows the try number)
# The board answers (secret bytes, gates) come from key.json, written by gen.py next to ANSWERS.md.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.
param([Parameter(Mandatory = $true)][string]$Ex, [Parameter(Mandatory = $true)][string]$Sid, [int]$K = 0, [string]$Repo = "C:\DE10\week2")
$ErrorActionPreference = "Stop"
$name = $Ex.ToLower()
$dir = Join-Path $Repo $name
if (-not (Test-Path (Join-Path $dir "tools\questions.ps1"))) { Write-Host "No $name under $Repo"; exit 1 }
$script:Ex = "w2-$name"		# the label: seeds the numbers, names the codes
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
	Write-Host ""
	Write-Host "$($item.Id) $($item.Name):  $($q.Lines -join ' / ')"
	Write-Host "   answer: $ans    code: $(Get-Code $Sid "$($script:Ex)-$($item.Id)")"
	# Machine-readable line for tests: ANSWER Qn <answer>
	if ($env:W2_TEST) { Write-Output "ANSWER $($item.Id) $ans" }
}
