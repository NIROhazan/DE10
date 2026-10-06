# week 4 ex8 - critical path and short path (lecture 4: timing, tpd, tcd, critical / short path).
# Q1-Q2: the board is the circuit of the lecture in slow motion with hidden gate delays - the student measures them.
# Q3-Q4: a circuit on paper with the student's own gate delays (ps). Get-Question returns Lines, Format, Checks, Asked.
# Kept ASCII so Windows PowerShell 5.1 reads it without a BOM.

$script:Title = "Exercise 8 - critical path and short path"
$script:BoardHelp = @(
	"Board: A = SW0, B = SW1, C = SW2, D = SW3.  Puzzle = SW9..SW7 (0-7, in binary).",
	"Circuit:  n1 = A AND B,  n2 = NOT C,  n3 = n1 OR n2,  Y = n3 AND D.   LEDG0 = Y.",
	"Slow motion: every gate needs some ticks (1 tick = 0.1 s) before its output follows its inputs.",
	"All gates of the same type have the same delay; the delays depend on the puzzle.",
	"After you flip ONE switch: HEX3 HEX2 = ticks until the LAST change of Y, HEX1 HEX0 = until the FIRST",
	"change (00 = Y did not change), LEDR3..0 = how many times Y changed.")

function Get-QuestionList {
	@([pscustomobject]@{ Id = "Q1"; Name = "GATES" }, [pscustomobject]@{ Id = "Q2"; Name = "TPD_TCD" },
	  [pscustomobject]@{ Id = "Q3"; Name = "PAPER" }, [pscustomobject]@{ Id = "Q4"; Name = "FASTER" })
}

# ---------------------------------------------------------------- the paper circuits: gates in order, inputs A..D
$script:Nets = @(
	@(@("n1", "AND", "A", "B"), @("n2", "OR", "n1", "C"), @("Y", "AND", "n2", "D")),
	@(@("n1", "NOT", "A"), @("n2", "AND", "n1", "B"), @("n3", "OR", "C", "D"), @("Y", "OR", "n2", "n3")),
	@(@("n1", "NAND", "A", "B"), @("n2", "NOT", "C"), @("n3", "NOR", "n1", "n2"), @("Y", "XOR", "n3", "D")),
	@(@("n1", "AND", "A", "B"), @("n2", "OR", "A", "C"), @("n3", "NOT", "n2"), @("Y", "OR", "n1", "n3")),
	@(@("n1", "XOR", "A", "B"), @("n2", "AND", "n1", "C"), @("n3", "NOT", "D"), @("Y", "NOR", "n2", "n3")),
	@(@("n1", "NOR", "A", "B"), @("n2", "NAND", "C", "D"), @("n3", "AND", "n1", "n2"), @("Y", "OR", "n3", "A")))

# This student's circuit and gate delays for one question: tpd 20..95 ps, tcd 5..15 ps less (all multiples of 5)
function Get-Paper($sid, $tag, $k) {
	$net = $script:Nets[(Get-Num $sid "${tag}net" $k $script:Nets.Count)]
	$types = @($net | ForEach-Object { $_[1] } | Select-Object -Unique)
	$tpd = @{}; $tcd = @{}
	foreach ($t in $types) {
		$tpd[$t] = 20 + 5 * (Get-Num $sid "${tag}p$t" $k 16)
		$tcd[$t] = $tpd[$t] - 5 * (1 + (Get-Num $sid "${tag}c$t" $k 3))
	}
	return @{ Net = $net; Types = $types; Tpd = $tpd; Tcd = $tcd }
}
# Latest (tpd) and earliest (tcd) arrival at Y, inputs at time 0
function Get-Arrival($net, $tpd, $tcd) {
	$max = @{ A = 0; B = 0; C = 0; D = 0 }; $min = @{ A = 0; B = 0; C = 0; D = 0 }
	foreach ($g in $net) {
		$ins = @($g | Select-Object -Skip 2)
		$max[$g[0]] = ($ins | ForEach-Object { $max[$_] } | Measure-Object -Maximum).Maximum + $tpd[$g[1]]
		$min[$g[0]] = ($ins | ForEach-Object { $min[$_] } | Measure-Object -Minimum).Minimum + $tcd[$g[1]]
	}
	return @($max["Y"], $min["Y"])
}
function Format-Paper($pp) {
	$l = @("Circuit (each line is one gate):")
	$l += @($pp.Net | ForEach-Object { "    $($_[0]) = $($_[1]) ($((@($_ | Select-Object -Skip 2)) -join ', '))" })
	$l += "Gate delays:  " + (@($pp.Types | ForEach-Object { "$_ tpd $($pp.Tpd[$_]) ps, tcd $($pp.Tcd[$_]) ps" }) -join ";  ")
	return $l
}

function Get-Question($sid, $qid, $k) {
	switch ($qid) {
		"Q1" {
			$p = Get-Num $sid "Q1" $k 8
			return @{ Asked = "puzzle $p"; Format = "three numbers of ticks: AND OR NOT, e.g. 4 7 2"
				Lines = @("Puzzle $p (SW9..SW7 = $(Get-Bin $p 3)).  Measure the delay of ONE AND gate, ONE OR gate and the NOT gate.",
					"Choose the other switches so that the switch you flip really reaches Y (a path that is 'open'),",
					"then read HEX3 HEX2. A path through two gates shows their sum - subtract what you already know.")
				Checks = @(@{ Parts = "dec", "dec", "dec"; Secret = "gates$p" }) }
		}
		"Q2" {
			$p = Get-Num $sid "Q2" $k 8
			return @{ Asked = "puzzle $p"; Format = "two numbers of ticks: tpd tcd, e.g. 19 4"
				Lines = @("Puzzle $p (SW9..SW7 = $(Get-Bin $p 3)).  tpd = the delay of the LONGEST path from an input to Y (the critical path),",
					"tcd = the delay of the SHORTEST path. What are tpd and tcd of this puzzle?  (measure the paths, compare them)")
				Checks = @(@{ Parts = "dec", "dec"; Secret = "tpd$p" }) }
		}
		"Q3" {
			$pp = Get-Paper $sid "Q3" $k
			$a = Get-Arrival $pp.Net $pp.Tpd $pp.Tcd
			return @{ Asked = "net $([array]::IndexOf($script:Nets, $pp.Net)) tpd $($a[0]) tcd $($a[1])"; Format = "two numbers in ps: tpd tcd, e.g. 145 60"
				Lines = @(Format-Paper $pp) + @("On paper (no board): what are tpd and tcd of Y?  Every path counts - also the ones through a single gate.")
				Checks = @(@{ Parts = "dec", "dec"; Value = "$($a[0]) $($a[1])" }) }
		}
		"Q4" {
			$pp = Get-Paper $sid "Q4" $k
			$t = $pp.Types[(Get-Num $sid "Q4t" $k $pp.Types.Count)]
			$x = 5 * (1 + (Get-Num $sid "Q4x" $k ([math]::Max(1, [math]::Min(6, ($pp.Tcd[$t] / 5) - 1)))))
			$fast = @{}; foreach ($y in $pp.Types) { $fast[$y] = $pp.Tpd[$y] }; $fast[$t] -= $x
			$a = Get-Arrival $pp.Net $fast $pp.Tcd
			return @{ Asked = "net $([array]::IndexOf($script:Nets, $pp.Net)) $t -$x new tpd $($a[0])"; Format = "one number in ps, e.g. 130"
				Lines = @(Format-Paper $pp) + @("Every $t gate is made $x ps faster (its tpd only). What is the new tpd of Y?",
					"Careful: the critical path may now be a different path.")
				Checks = @(@{ Parts = "dec"; Value = "$($a[0])" }) }
		}
	}
}
