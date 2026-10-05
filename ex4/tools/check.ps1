# The answer checks, shared by run.ps1 (answer.txt + Claude) and ask.ps1 (one question per bat).
# Identical in every exercise; dot-source it. Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.
#
# Rules in the header of <proj>_top.v (all optional - ex1-ex6 compare every answer to Y):
#   // SIGNAL: y3 = ~A & B & C          a fixed signal of the board (a decoder output) the answers may use
#   // CHECK: MUX = (~A & ~B & D0) | (~A & B & D1) | (A & ~B & D2) | (A & B & D3)
#                                       Y is checked on this circuit built from the answers; the answers
#                                       it uses (D0..D3) are its parts and are not compared to Y alone
#   // ONLY: <names> : <rules>          the board is programmed only when these hold
#   // GRADE: <names> : <rules>         ask.ps1 gives the code only when these hold too (run.ps1 ignores them -
#                                       there minimality stays with Claude's feedback)
#   // ASK Q1 SOP: SOP | <English text> one question of ask.ps1 (Q1_SOP.bat): the answer names it asks for
#   // TARGETS: Y3 Y2 Y1 Y0             several outputs: the rows are  4'b1000: Y = 4'b1000;  and an answer
#                                       named Y2 is compared to that column (the others to Y)
# Rules: SOP  POS        a sum of products / a product of sums of single variables or their NOT
#        CSOP CPOS       canonical: one minterm per 1-row / one maxterm per 0-row (X rows not listed)
#        MIN             with SOP or POS: the fewest terms, then the fewest literals (X rows may be used)
#        LITNOT          a NOT only on a single variable (De Morgan finished)
#        NAND  NOR       only NAND gates (every AND under a NOT, no OR) / only NOR gates
#        MAXLIT n        at most n literals
#        TOKENS a b c    only these tokens (and parentheses) - must be the last rule on the line

# ---------------------------------------------------------------- evaluate a Verilog expression
function Test-Expr([string]$expr, [hashtable]$val) {
	$script:tok = @([regex]::Matches($expr, "1'b[01]|[A-Za-z_]\w*|[~!&|^()]|\S") | ForEach-Object { $_.Value })
	$script:pos = 0
	function Peek { if ($script:pos -lt $script:tok.Count) { $script:tok[$script:pos] } else { "" } }
	function Next { $t = Peek; $script:pos++; $t }
	function POr  { $v = PXor; while ((Peek) -eq "|") { $null = Next; $v = $v -bor (PXor) }; $v }
	function PXor { $v = PAnd; while ((Peek) -eq "^") { $null = Next; $v = $v -bxor (PAnd) }; $v }
	function PAnd { $v = PNot; while ((Peek) -eq "&") { $null = Next; $v = $v -band (PNot) }; $v }
	function PNot {
		$t = Next
		if ($t -eq "~" -or $t -eq "!") { return 1 - (PNot) }
		if ($t -eq "(") { $v = POr; if ((Next) -ne ")") { throw "missing )" }; return $v }
		if ($t -eq "1'b0") { return 0 }
		if ($t -eq "1'b1") { return 1 }
		if ($val.ContainsKey($t)) { return $val[$t] }
		throw "cannot read '$t'"
	}
	$r = POr
	if ($script:pos -ne $script:tok.Count) { throw "cannot read '$(Peek)'" }
	$r
}

# ---------------------------------------------------------------- a Verilog expression as a gate tree
# Each node is @(op, children); op = or / xor / and / not / leaf (a leaf keeps its token in Tok)
function Get-Tree([string]$expr) {
	$script:ft = @([regex]::Matches($expr, "1'b[01]|[A-Za-z_]\w*|[~!&|^()]|\S") | ForEach-Object { $_.Value }); $script:fp = 0
	function FPeek { if ($script:fp -lt $script:ft.Count) { $script:ft[$script:fp] } else { "" } }
	function FBin($op, $sym, $next) {
		$k = @(& $next)
		while ((FPeek) -eq $sym) { $script:fp++; $k += , (& $next) }
		if ($k.Count -eq 1) { return , $k[0] }
		return , @($op, $k)
	}
	function FormOr  { FBin "or" "|" { FormXor } }
	function FormXor { FBin "xor" "^" { FormAnd } }
	function FormAnd { FBin "and" "&" { FormNot } }
	function FormNot {
		$t = FPeek; $script:fp++
		if ($t -eq "~" -or $t -eq "!") { return , @("not", @(, (FormNot))) }
		if ($t -eq "(") { $x = FormOr; $script:fp++; return , $x }
		return , @("leaf", @(), $t)
	}
	return , (FormOr)
}
function IsLit($x) { return ($x[0] -eq "leaf" -or ($x[0] -eq "not" -and $x[1][0][0] -eq "leaf")) }
function Get-Leaves($x) {
	if ($x[0] -eq "leaf") { return @(, $x[2]) }
	$o = @(); foreach ($k in $x[1]) { $o += @(Get-Leaves $k) }; return $o
}
# Terms and literals of a SOP (or POS) tree; constants are not literals
function Get-Cost($tree, $outer) {
	$terms = @(if ($tree[0] -eq $outer) { $tree[1] } else { , $tree })
	$lits = @(Get-Leaves $tree | Where-Object { $_ -notmatch "^1'b" }).Count
	return @($terms.Count, $lits)
}

# ---------------------------------------------------------------- the exact minimal SOP / POS of the table
# Cubes over n variables ('0' '1' '-'); a cube is usable when it covers no row of the other value.
# Returns @(terms, literals) of the cheapest cover of the 1-rows (SOP) or the 0-rows (POS); X rows are free.
function Get-MinCost($rows, [int]$n, [bool]$pos) {
	$want = if ($pos) { 0 } else { 1 }
	$on = @($rows | Where-Object { -not $_.Dc -and $_.Y -eq $want } | ForEach-Object { $_.Bits })
	$off = @($rows | Where-Object { -not $_.Dc -and $_.Y -ne $want } | ForEach-Object { $_.Bits })
	if ($on.Count -eq 0) { return @(1, 0) }	# a constant
	$cubes = @()
	foreach ($i in 0..([math]::Pow(3, $n) - 1)) {
		$c = ""; $x = $i
		for ($k = 0; $k -lt $n; $k++) { $c += "01-"[$x % 3]; $x = [math]::Floor($x / 3) }
		$cov = { param($c, $b) for ($k = 0; $k -lt $c.Length; $k++) { if ($c[$k] -ne '-' -and $c[$k] -ne $b[$k]) { return $false } }; $true }
		if (@($off | Where-Object { & $cov $c $_ }).Count) { continue }
		$hit = @(0..($on.Count - 1) | Where-Object { & $cov $c $on[$_] })
		if ($hit.Count -eq 0) { continue }
		$mask = 0; foreach ($h in $hit) { $mask = $mask -bor (1 -shl $h) }
		$cubes += [pscustomobject]@{ Mask = $mask; Lits = ($c.ToCharArray() | Where-Object { $_ -ne '-' }).Count; Cube = $c }
	}
	# keep only cubes that no other cube beats (same or bigger cover, fewer or equal literals)
	$cubes = @($cubes | Sort-Object Lits | Where-Object { $me = $_; -not @($cubes | Where-Object { $_ -ne $me -and ($_.Mask -bor $me.Mask) -eq $_.Mask -and $_.Lits -lt $me.Lits }).Count })
	$all = (1 -shl $on.Count) - 1
	if (@($cubes | Where-Object { $_.Lits -eq 0 }).Count) { $script:minCover = @("-" * $n); return @(1, 0) }
	$best = $null
	for ($t = 1; $t -le $cubes.Count -and -not $best; $t++) {
		# every choice of t cubes (n <= 4, so this is small)
		$idx = @(0..($t - 1))
		while ($true) {
			$m = 0; $l = 0
			foreach ($i in $idx) { $m = $m -bor $cubes[$i].Mask; $l += $cubes[$i].Lits }
			if ($m -eq $all -and (-not $best -or $l -lt $best[1])) { $best = @($t, $l); $script:minCover = @($idx | ForEach-Object { $cubes[$_].Cube }) }
			$j = $t - 1
			while ($j -ge 0 -and $idx[$j] -eq $cubes.Count - $t + $j) { $j-- }
			if ($j -lt 0) { break }
			$idx[$j]++; for ($k = $j + 1; $k -lt $t; $k++) { $idx[$k] = $idx[$k - 1] + 1 }
		}
	}
	return $best
}

# One minimal SOP (or POS) of the table in the student's notation, e.g. A'B + AC  /  (A + B)(A' + C)
function Get-MinExpr($rows, [string[]]$vars, [bool]$pos) {
	$script:minCover = @()
	$null = Get-MinCost $rows $vars.Count $pos
	$terms = @($script:minCover | ForEach-Object {
		$c = $_
		$lits = @(0..($vars.Count - 1) | Where-Object { $c[$_] -ne '-' } | ForEach-Object {
			# SOP: a 1 in the cube is the variable, a 0 its NOT; POS (cubes of 0-rows): the other way round
			if (($c[$_] -eq '1') -xor $pos) { $vars[$_] } else { $vars[$_] + "'" } })
		if ($pos) { if ($lits.Count -gt 1) { "(" + ($lits -join " + ") + ")" } else { $lits -join "" } } else { $lits -join "" } })
	if ($terms.Count -eq 0 -or ($terms.Count -eq 1 -and $terms[0] -eq "")) { return $(if ($pos) { "0" } else { "1" }) }
	if ($pos) { return ($terms -join "") }
	return ($terms -join " + ")
}

# ---------------------------------------------------------------- the form rules
# $ctx: Rows, Vars (for CSOP CPOS MIN). Returns "" when every rule holds, else what is wrong.
function Test-Rules([string]$expr, [string]$rules, $ctx) {
	$tok = @([regex]::Matches($expr, "1'b[01]|[A-Za-z_]\w*|[~!&|^()]|\S") | ForEach-Object { $_.Value })
	$words = @($rules -split '\s+' | Where-Object { $_ })
	$tree = Get-Tree $expr
	for ($w = 0; $w -lt $words.Count; $w++) {
		$r = $words[$w]
		if ($r -eq "TOKENS") {
			$ok = @($words[($w + 1)..($words.Count - 1)]) + @("(", ")")
			$bad = @($tok | Where-Object { $ok -notcontains $_ } | Select-Object -Unique)
			if ($bad.Count) { return "uses $($bad -join ' ') - allowed: $($words[($w + 1)..($words.Count - 1)] -join ' ')" }
			return ""
		}
		if ($r -eq "MAXLIT") {
			$w++; $max = [int]$words[$w]
			$n = @(Get-Leaves $tree | Where-Object { $_ -notmatch "^1'b" }).Count
			if ($n -gt $max) { return "has $n literals - it can be done with $max" }
			continue
		}
		if ($r -eq "LITNOT") {
			$script:formErr = ""
			function WalkNot($x) {
				if ($x[0] -eq "not" -and $x[1][0][0] -ne "leaf" -and $x[1][0][0] -ne "not") { $script:formErr = "has a NOT over a group, like (A+B)' - De Morgan is not finished" }
				foreach ($k in $x[1]) { WalkNot $k }
			}
			WalkNot $tree
			if ($script:formErr) { return $script:formErr }
			continue
		}
		if ($r -in "SOP", "POS", "CSOP", "CPOS") {
			$isSop = $r -like "*SOP"
			$outer = if ($isSop) { "or" } else { "and" }
			$inner = if ($isSop) { "and" } else { "or" }
			$terms = @(if ($tree[0] -eq $outer) { $tree[1] } else { , $tree })
			foreach ($t in $terms) {
				if (IsLit $t) { continue }
				if ($t[0] -eq $inner -and -not @($t[1] | Where-Object { -not (IsLit $_) }).Count) { continue }
				return $(if ($isSop) { "is not in SOP form (a sum of products of single variables or their NOT)" } else { "is not in POS form (a product of sums of single variables or their NOT)" })
			}
			if ($r -like "C*") {
				$want = if ($isSop) { 1 } else { 0 }
				$need = @($ctx.Rows | Where-Object { -not $_.Dc -and $_.Y -eq $want }).Count
				$seen = @{}
				foreach ($t in $terms) {
					$vs = @(Get-Leaves $t | Sort-Object)
					if (($vs -join ",") -ne (@($ctx.Vars | Sort-Object) -join ",")) {
						return "is not canonical: every $(if ($isSop) { 'minterm' } else { 'maxterm' }) must have each of $($ctx.Vars -join ' ') exactly once"
					}
					$lits = @(if (IsLit $t) { , $t } else { $t[1] })
					$key = (@($lits | ForEach-Object { if ($_[0] -eq "not") { "~" + $_[1][0][2] } else { $_[2] } }) | Sort-Object) -join ","
					$seen[$key] = 1
				}
				if ($seen.Count -ne $need) {
					return "is not canonical: it needs exactly $need $(if ($isSop) { 'minterms, one per row with Y = 1' } else { 'maxterms, one per row with Y = 0' }) - you have $($seen.Count)"
				}
			}
			continue
		}
		if ($r -eq "MIN") {
			$pos = $words -contains "POS"
			$mine = Get-Cost $tree $(if ($pos) { "and" } else { "or" })
			$best = Get-MinCost $ctx.Rows $ctx.Vars.Count $pos
			if ($mine[0] -gt $best[0] -or ($mine[0] -eq $best[0] -and $mine[1] -gt $best[1])) {
				return "is not minimal - you have $($mine[0]) $(if ($pos) { 'sums' } else { 'terms' }) and $($mine[1]) literals - it can be done with $($best[0]) and $($best[1])"
			}
			continue
		}
		if ($r -eq "NAND" -or $r -eq "NOR") {
			$gate = if ($r -eq "NAND") { "and" } else { "or" }
			$other = if ($r -eq "NAND") { "or" } else { "and" }
			$script:formErr = ""
			function Walk($node, $parent) {
				$op = $node[0]
				if ($op -eq "xor" -or $op -eq $other) { $script:formErr = "uses $(if ($op -eq 'xor') { 'XOR' } else { $other.ToUpper() }) - only $r gates are allowed" }
				if ($op -eq $gate -and $parent -ne "not") { $script:formErr = "has an $($gate.ToUpper()) without a NOT right after it - that is not a $r gate" }
				foreach ($k in $node[1]) { Walk $k $op }
			}
			Walk $tree ""
			if ($script:formErr) { return $script:formErr }
			continue
		}
	}
	return ""
}

# ---------------------------------------------------------------- the table and the rules of <proj>_top.v
function Get-Board([string]$topFile) {
	$top = [IO.File]::ReadAllText($topFile)
	if ($top -notmatch 'case\s*\(\{([^}]*)\}\)') { throw "Cannot find the truth table in $topFile." }
	$vars = @($Matches[1] -split ',' | ForEach-Object { $_.Trim() })
	$rows = @([regex]::Matches($top, "\d+'b([01]+):\s*(?:begin\s*)?Y\s*=\s*\d+'b([01]+);(\s*dc\s*=\s*1'b1)?") |
		ForEach-Object { $y = $_.Groups[2].Value; [pscustomobject]@{ Bits = $_.Groups[1].Value; Y = $(if ($y.Length -eq 1) { [int]$y } else { $y }); Dc = $_.Groups[3].Success } })
	$rows = @($rows | Sort-Object Bits)
	if ($rows.Count -ne [math]::Pow(2, $vars.Count)) { throw "The truth table in $topFile has $($rows.Count) rows - expected $([math]::Pow(2, $vars.Count))." }
	$targets = @(if ($top -match '(?m)^//\s*TARGETS:\s*(.+?)\s*$') { $Matches[1] -split '\s+' })	# @() even when there are none
	$b = [pscustomobject]@{ Vars = $vars; Rows = $rows; Signals = [ordered]@{}; Checks = [ordered]@{}; Only = @{}; Grade = @{}; Asks = @(); Targets = $targets }
	foreach ($m in [regex]::Matches($top, '(?m)^//\s*SIGNAL:\s*(\w+)\s*=\s*(.+?)\s*$')) { $b.Signals[$m.Groups[1].Value] = $m.Groups[2].Value }
	foreach ($m in [regex]::Matches($top, '(?m)^//\s*CHECK:\s*(\w+)\s*=\s*(.+?)\s*$')) { $b.Checks[$m.Groups[1].Value] = $m.Groups[2].Value }
	foreach ($m in [regex]::Matches($top, '(?m)^//\s*(ONLY|GRADE):\s*([\w ]+?)\s*:\s*(.+?)\s*$')) {
		$to = if ($m.Groups[1].Value -eq "ONLY") { $b.Only } else { $b.Grade }
		foreach ($n in ($m.Groups[2].Value -split '\s+')) { $to[$n] = (("" + $to[$n]) + " " + $m.Groups[3].Value).Trim() }
	}
	foreach ($m in [regex]::Matches($top, '(?m)^//\s*ASK\s+(Q\d+)\s+(\w+):\s*([\w ]+?)\s*\|\s*(.+?)\s*$')) {
		$b.Asks += [pscustomobject]@{ Id = $m.Groups[1].Value; Title = $m.Groups[2].Value; Names = @($m.Groups[3].Value -split '\s+'); Text = $m.Groups[4].Value }
	}
	return $b
}

# The rows with Y = the column of one output (several outputs), or the rows as they are
function Get-TargetRows($board, $name) {
	$i = [array]::IndexOf(@($board.Targets), $name)
	if ($i -lt 0) { return $board.Rows }
	return @($board.Rows | ForEach-Object { [pscustomobject]@{ Bits = $_.Bits; Y = [int]("" + $_.Y[$i]); Dc = $_.Dc } })
}

# ---------------------------------------------------------------- check answers against the table
# $answers: ordered name -> Verilog. Prints one line per answer; returns the number of failed answers.
# -Grade also applies the GRADE rules and returns their failures in $script:gradeFail (not counted as wrong).
function Test-Answers($board, $answers, [switch]$Grade) {
	$parts = @{}
	$checks = [ordered]@{}
	foreach ($c in $board.Checks.Keys) {
		$mine = @($answers.Keys | Where-Object { $board.Checks[$c] -match "\b$_\b" })
		if ($mine.Count) { $checks[$c] = $board.Checks[$c]; foreach ($n in $mine) { $parts[$n] = $true } }
	}
	$ctx = @{}
	foreach ($n in $answers.Keys) { $ctx[$n] = [pscustomobject]@{ Rows = (Get-TargetRows $board $n); Vars = $board.Vars } }
	$col = @{}; foreach ($n in $answers.Keys) { $col[$n] = [array]::IndexOf(@($board.Targets), $n) }
	$bad = @{}; $broken = @{}
	foreach ($n in @($answers.Keys) + @($checks.Keys)) { $bad[$n] = @() }
	foreach ($r in $board.Rows) {
		if ($r.Dc) { continue }
		$val = @{}
		for ($i = 0; $i -lt $board.Vars.Count; $i++) { $val[$board.Vars[$i]] = [int]("" + $r.Bits[$i]) }
		foreach ($s in $board.Signals.Keys) { $val[$s] = Test-Expr $board.Signals[$s] $val }
		$here = ($board.Vars -join '') + "=" + $r.Bits
		foreach ($n in $answers.Keys) {
			if ($broken[$n]) { continue }
			try { $v = Test-Expr $answers[$n] $val } catch { $broken[$n] = "could not be read ($($_.Exception.Message))"; continue }
			$val[$n] = $v
			$want = if ($col[$n] -ge 0) { [int]("" + $r.Y[$col[$n]]) } else { $r.Y }
			if (-not $parts[$n] -and $v -ne $want) { $bad[$n] += "${here}: yours $v, $(if ($col[$n] -ge 0) { $n } else { 'Y' }) $want" }
		}
		foreach ($c in $checks.Keys) {
			if ($broken[$c]) { continue }
			try { $v = Test-Expr $checks[$c] $val } catch { $broken[$c] = "one of its parts could not be read"; continue }
			if ($v -ne $r.Y) { $bad[$c] += "${here}: yours $v, Y $($r.Y)" }
		}
	}
	$wrong = 0
	$script:gradeFail = @()
	foreach ($n in @($answers.Keys | Where-Object { -not $parts[$_] }) + @($checks.Keys)) {
		$tn = if ($answers.Contains($n) -and $col[$n] -ge 0) { $n } else { "Y" }	# the column it must equal
		$form = if ($board.Only[$n] -and $answers.Contains($n)) { Test-Rules $answers[$n] $board.Only[$n] $ctx[$n] } else { "" }
		if ($broken[$n]) { $wrong++; Write-Host "  $n : NOT checked - $($broken[$n])" -ForegroundColor Red }
		elseif ($bad[$n].Count -gt 0) {
			$wrong++
			Write-Host "  $n : NOT equal to $tn on $($bad[$n].Count) row$(if ($bad[$n].Count -gt 1) { 's' }):" -ForegroundColor Red
			$bad[$n] | ForEach-Object { Write-Host "      $_" -ForegroundColor Red }
		}
		elseif ($form) { $wrong++; Write-Host "  $n : equals $tn, but $form" -ForegroundColor Red }
		else {
			$g = if ($Grade -and $board.Grade[$n] -and $answers.Contains($n)) { Test-Rules $answers[$n] $board.Grade[$n] $ctx[$n] } else { "" }
			if ($g) { $script:gradeFail += "$n $g"; Write-Host "  $n : equals $tn on every row, but it $g" -ForegroundColor Yellow }
			else { Write-Host "  $n : equals $tn on every row" -ForegroundColor Green }
		}
	}
	# The parts of a CHECK only have form rules
	foreach ($n in @($answers.Keys | Where-Object { $parts[$_] })) {
		$form = if ($board.Only[$n]) { Test-Rules $answers[$n] $board.Only[$n] $ctx[$n] } else { "" }
		if ($broken[$n]) { $wrong++; Write-Host "  $n : NOT checked - $($broken[$n])" -ForegroundColor Red }
		elseif ($form) { $wrong++; Write-Host "  $n : $form" -ForegroundColor Red }
	}
	return $wrong
}

# ---------------------------------------------------------------- the student's notation -> Verilog
# A'B + C(A+B)'  ->  (~A & B) | (C & ~(A | B)).   ' ~ ! = NOT, AB * & . = AND, + | = OR, ^ = XOR, 0 1.
# $names: the variables / signals that exist. Throws a short English message when it cannot read it.
function ConvertTo-Verilog([string]$text, [string[]]$names) {
	$text = ($text -replace '\[[^\]]*\]', '').Trim()	# a [theorem] after a step is not part of it
	# the words work too: NOT A + NOT B,  A AND B,  NOT (A OR B),  A XOR B  (any case)
	$text = [regex]::Replace($text, '(?i)\bNOT\b', ' ~ ')
	$text = [regex]::Replace($text, '(?i)\bXOR\b', ' ^ ')
	$text = [regex]::Replace($text, '(?i)\bAND\b', ' * ')
	$text = [regex]::Replace($text, '(?i)\bOR\b', ' + ')
	$script:ct = @([regex]::Matches($text, "y\d|[A-Za-z]|[01]|'|\S") | ForEach-Object { $_.Value } | Where-Object { $_ -notmatch '^\s$' })
	# a lowercase letter is the same variable (a = A), unless the lowercase name itself exists (y0..y7)
	$script:ct = @($script:ct | ForEach-Object { if ($_ -cmatch '^[a-z]$' -and $names -cnotcontains $_ -and $names -ccontains $_.ToUpper()) { $_.ToUpper() } else { $_ } })
	foreach ($t in $script:ct) {
		if ($t -match '^[A-Za-z]$|^y\d$') { if ($names -cnotcontains $t) { throw "'$t' is not one of $($names -join ' ') (NOT, AND, OR need a space around them: NOT A, A AND B)" } }
		elseif ($t -notmatch "^[01'~!+|*&.^()]$") { throw "cannot read '$t' - use ' + * ( ) 0 1 and the variables" }
	}
	$script:cp = 0
	function CPeek { if ($script:cp -lt $script:ct.Count) { $script:ct[$script:cp] } else { "" } }
	function CvOr {
		$l = CvXor
		while ((CPeek) -eq "+" -or (CPeek) -eq "|") { $script:cp++; $l = "$l | $(CvXor)" }
		return $l
	}
	function CvXor {
		$l = CvAnd
		while ((CPeek) -eq "^") { $script:cp++; $l = "$l ^ $(CvAnd)" }
		return $l
	}
	function CvAnd {
		$l = CvUn
		while ($true) {
			$p = CPeek
			if ($p -eq "*" -or $p -eq "&" -or $p -eq ".") { $script:cp++ }
			elseif ($p -notmatch "^([A-Za-z]|y\d|[01(~!])$") { break }
			$l = "$l & $(CvUn)"
		}
		return $l
	}
	function CvUn {
		$p = CPeek
		if ($p -eq "~" -or $p -eq "!") { $script:cp++; $x = CvUn; return "~$x" }
		$x = CvAtom
		while ((CPeek) -eq "'") { $script:cp++; $x = "~$x" }
		return $x
	}
	function CvAtom {
		$p = CPeek; $script:cp++
		if ($p -eq "(") {
			$x = CvOr
			if ((CPeek) -ne ")") { throw "missing )" }
			$script:cp++
			return "($x)"
		}
		if ($p -eq "0") { return "1'b0" }
		if ($p -eq "1") { return "1'b1" }
		if ($p -match '^([A-Za-z]|y\d)$') { return $p }
		if ($p -eq "") { throw "the expression ends too early" }
		throw "unexpected '$p'"
	}
	if ($script:ct.Count -eq 0) { throw "empty" }
	$v = CvOr
	if ($script:cp -lt $script:ct.Count) { throw "unexpected '$(CPeek)'" }
	return $v
}

# The canonical SOP of the table as Verilog (X rows taken as 0) - fills the board outputs nobody asked for
function Get-CanonVerilog($board, $name = "") {
	$t = @((Get-TargetRows $board $name) | Where-Object { $_.Y -eq 1 -and -not $_.Dc } | ForEach-Object {
		$b = $_.Bits
		"(" + ((0..($board.Vars.Count - 1) | ForEach-Object { if ($b[$_] -eq '1') { $board.Vars[$_] } else { "~" + $board.Vars[$_] } }) -join " & ") + ")" })
	if ($t.Count -eq 0) { return "1'b0" }
	return ($t -join " | ")
}
