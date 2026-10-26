# Exercise 0 - a student's own questions and one right answer for each (instructor only).
# Usage:  powershell -File answers.ps1 3160009489
param([Parameter(Mandatory = $true)][string]$Sid)
Set-Location "C:\DE10\week3\ex0_eq"
. .\tools\eq.ps1; . .\tools\student.ps1
$re = '^\s*Q(\d+):\s*Y\s*=\s*(.+?)\s*\|\s*(SW|HEX:\s*[YCBA?](?:\s*[YCBA?]){3})\s*(?:\|\s*MAX:\s*(\d+)\s*)?(?:\|\s*IF:\s*(.*))?$'
Write-Host "ID $Sid"
foreach ($line in [IO.File]::ReadAllLines((Resolve-Path "questions.txt"), [Text.Encoding]::UTF8)) {
	if ($line -notmatch $re) { continue }
	$q = [pscustomobject]@{ Id = "Q" + $Matches[1]; Eq = $Matches[2]; Kind = $(if ($Matches[3] -eq "SW") { "SW" } else { "HEX" })
		Show = ($Matches[3] -replace '^HEX:|\s', ''); Max = [int]$Matches[4]; If = $Matches[5] }
	$null, $f = Read-Equation $q.Eq
	$g = New-Question $q $Sid
	if ($q.Kind -eq "SW") {
		$a = Get-Display $f @([regex]::Matches($g, '\d') | ForEach-Object { [int]$_.Value })
		"{0,-4} Y = {1,-20} SW {2,-22} -> {3}" -f $q.Id, $q.Eq, $g, (($a.ToCharArray()) -join ' ')
	} else {
		$w = $g -replace '\s', ''
		$all = @(0..1023 | Where-Object { Test-Pattern (Get-DisplayOf $f $_) $w } | ForEach-Object { $v = $_; (0..9 | Where-Object { $v -band (1 -shl $_) }) -join ' ' })
		"{0,-4} Y = {1,-20} HEX {2,-21} -> {3}" -f $q.Id, $q.Eq, $g, ($all -join '   or   ')
	}
	"     code {0}" -f (Get-Code $Sid $q.Id)
}
