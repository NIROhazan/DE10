# -*- coding: utf-8 -*-
# Hebrew screen texts of the 30 lesson questions (by question NAME). Rule: a line is either Hebrew or English -
# switch names, formulas and letters always go on a line of their own (the console cannot mix the two directions).
# exec'd by gen.py after the questions are built; replaces title / B / P / step texts, never the answers.

DOWN4 = "SW7 SW6:   down-down,   down-up,   up-down,   up-up"
POS4 = ["1st -> SW0     2nd -> SW1     3rd -> SW2     4th -> SW3"]
NUM7 = ["1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2    5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0"]
NUM12 = ["1 = SW0          2 = SW1          3 = SW1+SW0       4 = SW2           5 = SW2+SW0       6 = SW2+SW1",
         "7 = SW2+SW1+SW0  8 = SW3          9 = SW3+SW0      10 = SW3+SW1      11 = SW3+SW1+SW0  12 = SW3+SW2"]
NUM8 = ["0 = all down   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"]
NUM4 = ["0 = all down    1 = SW0    2 = SW1    3 = SW1+SW0"]
ROWS3 = ["SW9 SW8 SW7:   000   001   010   011   100   101   110   111      (0 = down, 1 = up)"]
ROWS2 = ["SW9 SW8:   00   01   10   11      (0 = down, 1 = up)"]
COPY = ["העתיקו את הנורות למתגים: נורה דולקת = מתג למעלה."]
GCODE = ["AND = both down     OR = SW0     NAND = SW1     NOR = SW1 + SW0"]
GRULE = ["AND = 1 only if both are 1      OR = 0 only if both are 0",
         "NAND = 0 only if both are 1     NOR = 1 only if both are 0"]
TAB3 = ["A B C    Y", "0 0 0", "0 0 1", "0 1 0", "0 1 1", "1 0 0", "1 0 1", "1 1 0", "1 1 1"]

def cand_steps(n, what, right):
    """the 3 steps of the 'students' answers' questions (n lights, compare with your own work)"""
    last = "דולקות" if False else ""
    return [
        ["הביטוי שלכם:", "@P", "פתרו אותו בעצמכם, על דף, ומלאו את הטבלה:"] + TAB3 +
        ["כמה פעמים יצא 1? שימו את המספר:"] + NUM7,
        ["שימו את שלושת המתגים למטה:", "SW9 SW8 SW7 = down down down",
         f"העתיקו את {n} הנורות למתגים: נורה דולקת = מתג למעלה."],
        [f"השוו כל נורה לטבלה שלכם, בכל 8 המצבים.",
         f"הרימו מתג לכל נורה {what}:", f"LEDGi -> SWi"],
    ]

HE = {
"GATE": dict(title="איזה שער מוסתר בלוח?",
    B=["A = SW9     B = SW8     Y = LEDG0 (green)     answer: SW3..SW0"],
    S=[["שימו את שני המתגים למטה:", "SW9 = down   SW8 = down",
        "האם הנורה הירוקה דולקת?", "דולקת - הרימו:", "SW0", "כבויה - השאירו הכל למטה."],
       ["נסו את 4 המצבים של שני המתגים, ורשמו בכל אחד אם הנורה דולקת:",
        "SW9 SW8:   down-down,   down-up,   up-down,   up-up",
        "לכל מצב שהנורה דלקה - הרימו מתג:"] + POS4,
       ["איזה שער זה? השוו את מה שרשמתם לשערים:"] + GRULE +
       ["XOR = 1 when they differ        XNOR = 1 when they are equal",
        "הרימו את המתגים של השער:",
        "AND = all down   OR = SW0   XOR = SW1   NAND = SW1+SW0   NOR = SW2   XNOR = SW2+SW0"]]),

"SIGMA": dict(title="מינטרמים ומקסטרמים של פונקציה מוסתרת",
    B=["A = SW9     B = SW8     C = SW7     F = LEDG0 (green)     answer: SW3..SW0"],
    S=[["שימו את שלושת המתגים למטה:", "SW9 SW8 SW7 = down down down",
        "הנורה הירוקה דולקת? דולקת - הרימו:", "SW0", "כבויה - השאירו למטה."],
       ["סבב 1 מתוך 2. החזיקו למטה:", "SW9 = down",
        "נסו 4 מצבים, ובכל אחד רשמו אם הנורה דולקת:", "SW8 SW7:   down-down,   down-up,   up-down,   up-up",
        "לכל מצב שהנורה דלקה - הרימו מתג:"] + POS4,
       ["סבב 2 מתוך 2. אותו דבר, אבל החזיקו למעלה:", "SW9 = up",
        "SW8 SW7:   down-down,   down-up,   up-down,   up-up",
        "לכל מצב שהנורה דלקה - הרימו מתג:"] + POS4,
       ["כמה פעמים הנורה דלקה, בשני הסבבים יחד (מתוך 8)?",
        "כל מצב כזה נקרא מינטרם.", "שימו את המספר:"] + NUM7,
       ["כמה פעמים הנורה הייתה כבויה (8 פחות התשובה הקודמת)?",
        "כל מצב כזה נקרא מקסטרם.", "שימו את המספר:"] + NUM7]),

"TERMS": dict(title="איזו נורה היא מינטרם, ואיזו מקסטרם?",
    B=["A = SW9     B = SW8     C = SW7     4 terms = LEDG3..LEDG0 (green)     answer: SW3..SW0"],
    S=[["כל נורה ירוקה היא איבר אחד (מכפלה או סכום) של האותיות:", "A, B, C",
        "הרימו את שלושת המתגים:", "SW9 SW8 SW7 = up up up"] + COPY +
       ["LEDGi -> SWi"],
       ["עברו על 8 המצבים, ובכל מצב רשמו אילו נורות דולקות:"] + ROWS3 +
       ["בכמה מצבים דולקת הנורה", "LEDG0?", "שימו את המספר:"] + NUM7,
       ["מינטרם דולק במצב אחד בלבד.", "איזו נורה דלקה רק פעם אחת? הרימו את המתג שלה:", "LEDGi -> SWi"],
       ["מקסטרם כבוי במצב אחד בלבד.", "איזו נורה כבתה רק פעם אחת? הרימו את המתג שלה:", "LEDGi -> SWi"]]),

"MATTER": dict(title="איזו כניסה לא משנה?",
    B=["A = SW9     B = SW8     C = SW7     F = LEDG0 (green)     answer: SW3..SW0"],
    S=[["עברו על 8 המצבים, ובכל מצב רשמו אם הנורה דולקת:"] + ROWS3 +
       ["בכמה מצבים היא דלקה? שימו את המספר:"] + NUM7,
       ["האם הכניסה הזו משנה משהו?", "A (SW9)", "השוו זוגות של מצבים שנבדלים רק בה:",
        "000-100    001-101    010-110    011-111",
        "אם הנורה שונה באחד הזוגות - הרימו:", "SW0", "אם היא תמיד אותו דבר - השאירו למטה."],
       ["אותו דבר בשביל", "B (SW8):", "000-010    001-011    100-110    101-111",
        "משנה - הרימו:", "SW0", "לא משנה - השאירו למטה."],
       ["כניסה אחת אף פעם לא משנה. איזו? (בדקו גם את", "C:  000-001   010-011   100-101   110-111",
        ") הרימו מתג אחד:", "A = SW2     B = SW1     C = SW0"]]),

"SIGMA4": dict(title="מינטרמים ומקסטרמים - ארבע כניסות",
    B=["A = SW9     B = SW8     C = SW7     D = SW6     F = LEDG0 (green)     answer: SW3..SW0"],
    S=[["יש 16 מצבים, אז עובדים ב-4 סבבים של 4 מצבים.", "סבב 1. החזיקו כל הסבב:", "SW9 = down   SW8 = down",
        "נסו 4 מצבים ורשמו בכל אחד אם הנורה דולקת:", DOWN4, "לכל מצב שהנורה דלקה - הרימו מתג:"] + POS4,
       ["סבב 2 - כמו סבב 1, רק החזיקו:", "SW9 = down   SW8 = up", DOWN4,
        "לכל מצב שהנורה דלקה - הרימו מתג:"] + POS4,
       ["סבב 3 - כמו סבב 1, רק החזיקו:", "SW9 = up   SW8 = down", DOWN4,
        "לכל מצב שהנורה דלקה - הרימו מתג:"] + POS4,
       ["סבב 4 - כמו סבב 1, רק החזיקו:", "SW9 = up   SW8 = up", DOWN4,
        "לכל מצב שהנורה דלקה - הרימו מתג:"] + POS4,
       ["כמה פעמים הנורה דלקה, בכל 4 הסבבים (מתוך 16)? אלה המינטרמים.", "שימו את המספר:"] + NUM12,
       ["כמה פעמים היא הייתה כבויה (16 פחות התשובה הקודמת)? אלה המקסטרמים.", "שימו את המספר:"] + NUM12]),

"THEOREMS": dict(title="אינדוקציה מלאה: אילו טענות נכונות?",
    B=["statement = SW9 SW8     A = SW7     B = SW6     LEFT = LEDG1     RIGHT = LEDG0     answer: SW3..SW0",
       "statements:   A + AB = A     A + A'B = A + B     (AB)' = A' + B'     (A + B)' = A' + B'"],
    S=[["כל טענה היא: צד שמאל = צד ימין. הלוח מראה את שני הצדדים בשתי נורות.",
        "טענה נכונה = שתי הנורות תמיד שוות (שתיהן דולקות או שתיהן כבויות).",
        "בחרו טענה 0:", "SW9 = down   SW8 = down",
        "נסו את 4 המצבים, ובכל אחד בדקו אם שתי הנורות שוות:", "SW7 SW6:   down-down,   down-up,   up-down,   up-up",
        "שוות תמיד - הרימו:", "SW0", "שונות אפילו פעם אחת - השאירו למטה."],
       ["אותה בדיקה לכל 4 הטענות:", "statement 0 = down-down   1 = down-up   2 = up-down   3 = up-up",
        "הרימו מתג לכל טענה נכונה:", "statement 0 -> SW0   1 -> SW1   2 -> SW2   3 -> SW3"],
       ["הטענה שלכם:", "@P", "חשבו על דף את שני הצדדים שלה ב-4 המצבים:",
        "A B    LEFT   RIGHT", "0 0", "0 1", "1 0", "1 1",
        "מצאו את מספר הטענה שהנורות שלה מראות בדיוק את זה. שימו את המספר:"] + NUM4]),

"THEOREMS8": dict(title="אינדוקציה מלאה: 8 טענות",
    B=["statement = SW9 SW8 SW7     A = SW6     B = SW5     C = SW4     LEFT = LEDG1     RIGHT = LEDG0     answer: SW3..SW0"],
    S=[["כל טענה היא: צד שמאל = צד ימין. טענה נכונה = שתי הנורות תמיד שוות.",
        "בחרו טענה 0:", "SW9 SW8 SW7 = down down down",
        "נסו את 8 המצבים, ובכל אחד בדקו אם שתי הנורות שוות:",
        "SW6 SW5 SW4:   000   001   010   011   100   101   110   111      (0 = down, 1 = up)",
        "שוות תמיד - הרימו:", "SW0", "שונות אפילו פעם אחת - השאירו למטה."],
       ["אותה בדיקה לכל 8 הטענות. מספר הטענה:",
        "SW9 SW8 SW7:   0 = ddd   1 = ddu   2 = dud   3 = duu   4 = udd   5 = udu   6 = uud   7 = uuu",
        "כמה טענות נכונות? שימו את המספר:"] + NUM8,
       ["הטענה שלכם:", "@P", "חשבו על דף את שני הצדדים שלה ב-8 המצבים:",
        "A B C    LEFT   RIGHT", "0 0 0", "0 0 1", "0 1 0", "0 1 1", "1 0 0", "1 0 1", "1 1 0", "1 1 1",
        "מצאו את מספר הטענה שהנורות שלה מראות בדיוק את זה. שימו את המספר:"] + NUM8]),

"MINSOP": dict(title="סכום מכפלות מינימלי",
    B=["A = SW9     B = SW8     C = SW7     F = LEDG0 (green)     answer: SW3..SW0"],
    S=[["הפונקציה בשאלה הזו היא הנורה הירוקה:", "F = LEDG0",
        "עברו על 8 המצבים, ובכל מצב רשמו אם הנורה דולקת:"] + ROWS3 +
       ["זו טבלת האמת של הפונקציה. בכמה מצבים היא 1? שימו את המספר:"] + NUM7,
       ["מהטבלה שלכם: כתבו איבר אחד לכל מצב שבו הנורה דלקה. למשל המצב 101 הוא האיבר:",
        "A B' C",
        "עכשיו אחדו כל שני איברים שנבדלים באות אחת בלבד, למשל:",
        "A B C  +  A B C'   =   A B",
        "חזרו על זה עד שאי אפשר יותר. כמה איברים נשארו? שימו את המספר:"] + NUM7,
       ["כמה אותיות יש בכל האיברים שנשארו, יחד? למשל:",
        "A'B + C   ->   3",
        "שימו את המספר:"] + NUM7]),

"LITERAL": dict(title="הליטרל המוסתר",
    B=["A = SW9     B = SW8     C = SW7     Y = LEDG0 (green)     answer: SW3..SW0"],
    S=[["עברו על 8 המצבים, ובכל מצב רשמו אם הנורה דולקת:"] + ROWS3 +
       ["בכמה מצבים היא דלקה? שימו את המספר:"] + NUM7,
       ["הביטוי שלכם:", "@P", "יש בו אות מוסתרת במקום", "?",
        "נסו כל אחת מהאפשרויות, חשבו את הטבלה על דף, והשוו לטבלה מהלוח.",
        "רק אחת מתאימה. הרימו את המתגים שלה:",
        "A = SW0    A' = SW1    B = SW1+SW0    B' = SW2    C = SW2+SW0    C' = SW2+SW1"],
       ["פשטו את הביטוי (עם האות הנכונה) כמה שאפשר.", "כמה אותיות נשארו? למשל",
        "A'B + C  ->  3", "שימו את המספר:"] + NUM7]),

"STORY": dict(title="מסיפור למשוואה",
    B=["your letters = SW9 SW8 SW7 (see below)     4 students' circuits = LEDG3..LEDG0     answer: SW3..SW0"],
    S=[["הסיפור שלכם:", "@P", "כתבו אותו על דף כמשוואה.", "הרימו את שלושת המתגים:", "SW9 SW8 SW7 = up up up"] + COPY +
       ["LEDGi -> SWi"],
       ["לפי המשוואה שלכם (על דף): מה יוצא במצב הזה?", "SW9 = up   SW8 = down   SW7 = up",
        "יוצא 1 - הרימו:", "SW0", "יוצא 0 - השאירו למטה."],
       ["איזו נורה היא המשוואה שלכם? מלאו את הטבלה לפי המשוואה:"] + TAB3 +
       ["והשוו לכל נורה ב-8 המצבים. הרימו את המתג של הנורה שמתאימה בכולם:", "LEDGi -> SWi"]]),

"DEMORGAN": dict(title="דה-מורגן: איזו תשובה נכונה?",
    B=["A = SW9     B = SW8     C = SW7     4 answers = LEDG3..LEDG0     answer: SW3..SW0"],
    S=[["הביטוי שלכם:", "@P", "הורידו על דף את הקו העליון (מבחוץ פנימה):",
        "(XY)' = X' + Y'        (X + Y)' = X'Y'", "ומלאו את הטבלה של התוצאה:"] + TAB3 +
       ["כמה פעמים יצא 1? שימו את המספר:"] + NUM7,
       ["שימו את שלושת המתגים למטה:", "SW9 SW8 SW7 = down down down",
        "העתיקו את 4 הנורות למתגים: נורה דולקת = מתג למעלה.", "LEDGi -> SWi"],
       ["השוו כל נורה לטבלה שלכם, בכל 8 המצבים. הרימו את המתג של הנורה הנכונה:", "LEDGi -> SWi"]]),

"ERRORS": dict(title="טעויות נפוצות: אילו פישוטים שגויים?",
    B=["A = SW9     B = SW8     C = SW7     4 students' results = LEDG3..LEDG0     answer: SW3..SW0"],
    S=cand_steps(4, "שגויה (שונה מהטבלה שלכם במצב כלשהו) - שתי נורות", False)),

"MULTIPLY": dict(title="הכפלה ופירוק: אילו תשובות נכונות?",
    B=["A = SW9     B = SW8     C = SW7     4 students' results = LEDG3..LEDG0     answer: SW3..SW0"],
    S=cand_steps(4, "נכונה (שווה לטבלה שלכם בכל המצבים) - שתי נורות", True)),

"STORY4": dict(title="מסיפור למשוואה - ארבע אותיות",
    B=["your letters = SW9 SW8 SW7 SW6 (see below)     4 circuits = LEDG3..LEDG0     answer: SW3..SW0"],
    S=[["הסיפור שלכם:", "@P", "כתבו אותו על דף כמשוואה.", "הרימו את ארבעת המתגים:", "SW9 SW8 SW7 SW6 = up up up up"] + COPY +
       ["LEDGi -> SWi"],
       ["לפי המשוואה שלכם (על דף): מה יוצא במצב הזה?", "SW9 = up   SW8 = down   SW7 = up   SW6 = down",
        "יוצא 1 - הרימו:", "SW0", "יוצא 0 - השאירו למטה."],
       ["איזו נורה היא המשוואה שלכם? השוו כל נורה למשוואה ב-16 המצבים",
        "(מצב שבו הם שונים פוסל את הנורה). הרימו את המתג של הנורה שמתאימה בכולם:", "LEDGi -> SWi"]]),

"DEMORGAN4": dict(title="דה-מורגן עם ארבע אותיות",
    B=["A = SW9     B = SW8     C = SW7     D = SW6     4 answers = LEDG3..LEDG0     answer: SW3..SW0"],
    S=[["שימו את ארבעת המתגים למטה:", "SW9 SW8 SW7 SW6 = down down down down"] + COPY + ["LEDGi -> SWi"],
       ["עכשיו את ארבעת המתגים למעלה:", "SW9 SW8 SW7 SW6 = up up up up"] + COPY + ["LEDGi -> SWi"],
       ["הביטוי שלכם:", "@P", "הורידו על דף את הקו העליון, והשוו כל נורה לתוצאה.",
        "הרימו מתג לכל נורה נכונה (אחת או שתיים):", "LEDGi -> SWi"]]),

"ERRORS5": dict(title="טעויות נפוצות - חמישה פישוטים",
    B=["A = SW9     B = SW8     C = SW7     5 students' results = LEDG4..LEDG0     answer: SW4..SW0"],
    S=[["הביטוי שלכם:", "@P", "פתרו אותו בעצמכם, על דף, ומלאו את הטבלה:"] + TAB3 +
       ["כמה פעמים יצא 1? שימו את המספר:"] + NUM7,
       ["שימו את שלושת המתגים למטה:", "SW9 SW8 SW7 = down down down",
        "העתיקו את 5 הנורות למתגים: נורה דולקת = מתג למעלה.", "LEDGi -> SWi"],
       ["השוו כל נורה לטבלה שלכם, בכל 8 המצבים.", "הרימו מתג לכל נורה שגויה:", "LEDGi -> SWi"]]),

"MULTIPLY4": dict(title="הכפלה ופירוק - שש תשובות",
    B=["A = SW9     B = SW8     C = SW7     D = SW6     6 answers = LEDG5..LEDG0     answer: SW5..SW0"],
    S=[["שימו את ארבעת המתגים למטה:", "SW9 SW8 SW7 SW6 = down down down down",
        "העתיקו את 6 הנורות למתגים: נורה דולקת = מתג למעלה.", "LEDGi -> SWi"],
       ["עכשיו את ארבעת המתגים למעלה:", "SW9 SW8 SW7 SW6 = up up up up",
        "העתיקו את 6 הנורות למתגים.", "LEDGi -> SWi"],
       ["הביטוי שלכם:", "@P", "הכפילו או פרקו אותו על דף, והשוו כל נורה לתוצאה.",
        "הרימו מתג לכל נורה נכונה (שתיים):", "LEDGi -> SWi"]]),

"MUX": dict(title="מה מחובר למרבב?",
    B=["S1 = SW9     S0 = SW8     C = SW7     Y = LEDG0 (green)     answer: SW1 SW0",
       "mux 4:1:   S1 S0 = 00 -> D0     01 -> D1     10 -> D2     11 -> D3"],
    S=[["המרבב שולח ליציאה כניסה אחת. שימו:", "SW9 = down   SW8 = down     (Y shows D0)",
        "הסתכלו על הנורה פעמיים:", "SW7 = down, then SW7 = up",
        "הרימו מתג אם הנורה דלקה:", "SW0 = with SW7 down      SW1 = with SW7 up"]] +
      [["מה מחובר ל-", f"D{k}?", "שימו:", f"SW9 SW8 = {['down down', 'down up', 'up down', 'up up'][k]}",
        "ובדקו את הנורה פעם עם", "SW7 = down, then SW7 = up",
        "הכלל, לפי שתי הבדיקות:", "0,0 -> 0      1,1 -> 1      0,1 -> C      1,0 -> C'",
        "הרימו:", "0 = both down     1 = SW0     C = SW1     C' = SW1 + SW0"] for k in range(4)]),

"DECODER": dict(title="מפענח: איזו נורה היא איזו יציאה?",
    B=["A = SW9     B = SW8     4 outputs = LEDG3..LEDG0 (hidden order)     answer: SW3..SW0"],
    S=[[("בכל מצב דולקת בדיוק נורה אחת." if k == 0 else "אותו דבר במצב הבא."), "שימו:",
        f"SW9 SW8 = {['down down', 'down up', 'up down', 'up up'][k]}",
        "איזו נורה דולקת? הרימו את המתג שלה, ורשמו על דף:", f"LEDGi -> SWi        (row {k >> 1}{k & 1} -> LEDG?)"]
       for k in range(4)] +
      [["הפונקציה שלכם:", "@P", "היא שער או של שתי יציאות.", "לפי מה שרשמתם: אילו שתי נורות? הרימו את המתגים שלהן:",
        "LEDGi -> SWi"]]),

"PRIORITY": dict(title="מעגל עדיפויות: מי מנצח?",
    B=["A3 = SW9     A2 = SW8     A1 = SW7     A0 = SW6     Y3..Y0 = LEDG3..LEDG0     answer: SW3..SW0",
       "Yi = 1 when Ai = 1 and no stronger input is 1"],
    S=[["הרימו רק את", "SW9", "(כל השאר למטה). איזו נורה דולקת? הרימו את המתג שלה:", "LEDGi -> SWi"],
       ["הרימו שניים:", "SW9 + SW8", "רק החזק מביניהם מדליק נורה. איזו? הרימו את המתג שלה:", "LEDGi -> SWi"],
       ["הרימו את כל הארבעה:", "SW9 SW8 SW7 SW6", "הנורה שדולקת שייכת לחזק ביותר. הרימו את המתג שלה:",
        "LEDGi -> SWi"],
       ["מי החלש ביותר? מכל הארבעה למעלה: הורידו את המנצח, ראו מי מנצח עכשיו, הורידו גם אותו...",
        "האחרון שנשאר הוא החלש. הרימו מתג אחד:", "A3 = SW3     A2 = SW2     A1 = SW1     A0 = SW0"]]),

"MUXLOGIC": dict(title="בונים פונקציה ממרבב",
    B=["A = SW9     B = SW8     C = SW7     F = LEDG0 (green)     answer: SW1 SW0"],
    S=[["עברו על 8 המצבים, ובכל מצב רשמו אם הנורה דולקת:"] + ROWS3 +
       ["בכמה מצבים היא דלקה? שימו את המספר:"] + NUM7] +
      [[f"מה צריך להיות ב-", f"D{k}?",
        f"בטבלה שלכם, מצאו את שני המצבים שבהם קווי הבחירה שלכם (למעלה) הם", f"S1 S0 = {k >> 1} {k & 1}",
        "(one with X = 0, one with X = 1)",
        "הכלל, לפי שני המצבים:", "0,0 -> 0      1,1 -> 1      0,1 -> X      1,0 -> X'",
        "הרימו:", "0 = both down     1 = SW0     X = SW1     X' = SW1 + SW0"] for k in range(4)]),

"DEC38": dict(title="מפענח 3:8: איזו נורה היא איזו יציאה?",
    B=["A = SW9     B = SW8     C = SW7     8 outputs = LEDG7..LEDG0 (hidden order)     answer: SW2..SW0"],
    S=[["שימו את שלושת המתגים למטה. דולקת בדיוק נורה אחת.", "SW9 SW8 SW7 = down down down",
        "מה המספר שלה? שימו אותו:", "(for example LEDG5 -> 5)"] + NUM8,
       ["עכשיו את שלושתם למעלה:", "SW9 SW8 SW7 = up up up", "איזו נורה דולקת? שימו את המספר שלה:"] + NUM8,
       ["המינטרם שלכם:", "@P", "שימו את המצב שלו על המתגים. איזו נורה דולקת? שימו את המספר שלה:"] + NUM8]),

"NANDNOR": dict(title="שתי רמות: NAND או NOR?",
    B=["A = SW9     B = SW8     C = SW7     n1 = LEDG2     n2 = LEDG1     Y = LEDG0     answer: SW5..SW0",
       "all three gates are NAND, or all three are NOR"],
    S=[["שימו את שלושת המתגים למטה:", "SW9 SW8 SW7 = down down down",
        "העתיקו את שלוש הנורות:", "SW2 = n1 (LEDG2)     SW1 = n2 (LEDG1)     SW0 = Y (LEDG0)"],
       ["עברו על 8 המצבים והסתכלו על", "n1 (LEDG2)",
        "שער של שתי כניסות: אם הוא כבוי רק ב-2 מצבים - הוא", "NAND",
        "ואם הוא דולק רק ב-2 מצבים - הוא", "NOR",
        "הרימו:", "NAND = SW0 up     NOR = SW0 down"],
       ["מה נכנס ל-", "n1?", "הסתכלו על 2 המצבים המיוחדים שלו: שתי אותיות לא משתנות בהם - הן הכניסות.",
        "NAND:  1 there -> X     0 there -> X'",
        "NOR:   0 there -> X     1 there -> X'",
        "הרימו שני מתגים:", "SW5 = A   SW4 = A'   SW3 = B   SW2 = B'   SW1 = C   SW0 = C'"]]),

"GATES": dict(title="מעגל רב-שלבי: מצאו את השערים",
    B=["A = SW9     B = SW8     C = SW7     D = SW6     answer: SW1 SW0",
       "n1 = G1(A, B) on LEDG2   ->   n2 = G2(n1, C) on LEDG1   ->   Y = G3(n2, D) on LEDG0"],
    S=[["שימו את ארבעת המתגים למטה:", "SW9 SW8 SW7 SW6 = down down down down",
        "העתיקו את שלוש הנורות:", "SW2 = n1 (LEDG2)     SW1 = n2 (LEDG1)     SW0 = Y (LEDG0)"],
       ["השער הראשון: נסו את 4 המצבים ותראו את", "n1 (LEDG2)", "SW9 SW8:   down-down,   down-up,   up-down,   up-up"] +
       GRULE + ["הרימו:"] + GCODE,
       ["השער השני: הכניסות שלו הן", "n1 (LEDG2)  and  C (SW7)", "והיציאה", "n2 (LEDG1)",
        "נסו את 4 הצירופים:"] + GRULE + ["הרימו:"] + GCODE,
       ["השער השלישי: הכניסות שלו הן", "n2 (LEDG1)  and  D (SW6)", "והיציאה", "Y (LEDG0)",
        "נסו את 4 הצירופים:"] + GRULE + ["הרימו:"] + GCODE]),

"BUBBLES": dict(title="דחיפת בועות: איזה מעגל בלוח?",
    B=["A = SW9     B = SW8     C = SW7     D = SW6     Y = LEDG0 (green)     answer: SW1 SW0",
       "n1' = a bubble (NOT) on that input of the last gate"],
    S=[["שני מבטים מהירים. כל המתגים למטה, ואז כולם למעלה:", "SW9..SW6 = all down, then all up",
        "הרימו מתג אם הנורה דלקה:", "SW0 = all down      SW1 = all up"],
       ["המעגלים:", "@P", "איזה מהם בלוח? חשבו את", "Y", "של כל מעגל בכמה מצבים (התחילו מ-0000 ו-1111),",
        "והשוו ללוח עד שנשאר מעגל אחד. שימו את המספר שלו:"] + NUM4]),

"NANDNOR3": dict(title="שתי רמות: שלושה שערים, NAND או NOR",
    B=["A = SW9     B = SW8     C = SW7     n1 = LEDG3   n2 = LEDG2   n3 = LEDG1   Y = LEDG0     answer: SW3..SW0",
       "n1, n2, n3: 2-input NAND or NOR of letters      Y: 3-input NAND or NOR of n1, n2, n3"],
    S=[["שימו את שלושת המתגים למטה:", "SW9 SW8 SW7 = down down down",
        "העתיקו את ארבע הנורות:", "SW3 = n1     SW2 = n2     SW1 = n3     SW0 = Y"],
       ["עברו על 8 המצבים והסתכלו על", "n1 (LEDG3)",
        "כבוי רק ב-2 מצבים -", "NAND", "דולק רק ב-2 מצבים -", "NOR",
        "הרימו:", "NAND = SW0 up     NOR = SW0 down"],
       ["אותו דבר בשביל", "n2, n3",
        "ובשביל", "Y:", "חפשו מצב שבו שלושת הצמתים לא שווים -",
        "NAND gives 1 there     NOR gives 0 there",
        "הרימו:", "SW3 = n1   SW2 = n2   SW1 = n3   SW0 = Y      (1 = NAND, 0 = NOR)"]]),

"BUBBLES8": dict(title="דחיפת בועות: איזה מ-8 מעגלים?",
    B=["A = SW9     B = SW8     C = SW7     D = SW6     Y = LEDG0 (green)     answer: SW2..SW0",
       "n1' = a bubble (NOT) on that input of the last gate"],
    S=[["שני מבטים מהירים. כל המתגים למטה, ואז כולם למעלה:", "SW9..SW6 = all down, then all up",
        "הרימו מתג אם הנורה דלקה:", "SW0 = all down      SW1 = all up"],
       ["המעגלים:", "@P", "איזה מהם בלוח? חשבו את", "Y", "של כל מעגל בכמה מצבים, והשוו ללוח עד שנשאר אחד.",
        "שימו את המספר שלו:"] + NUM8]),

"LATCH": dict(title="קופסה עם זיכרון: מה מדליק ומה מכבה?",
    B=["A = SW9     B = SW8     the box = LEDG0 (green)     answer: SW1 SW0",
       "move ONE switch at a time"],
    S=[["הזיזו מתג אחד בכל פעם ועברו בדרך הזו, תוך כדי הסתכלות על הנורה:",
        "00  ->  01  ->  11  ->  10  ->  00          (SW9 SW8)",
        "הנורה השתנתה לפחות פעם אחת? הרימו:", "SW0"],
       ["רק מצב אחד מדליק את הקופסה. באיזה מצב הייתם כשהנורה נדלקה?", "הרימו:",
        "00 = both down     01 = SW0     10 = SW1     11 = SW1 + SW0"],
       ["ורק מצב אחד מכבה אותה (בשני האחרים היא זוכרת). איזה?", "הרימו:",
        "00 = both down     01 = SW0     10 = SW1     11 = SW1 + SW0"]]),

"DLATCH": dict(title="נועל D: מי האפשור?",
    B=["A = SW9     B = SW8     the box = LEDG0 (green)     answer: SW1 SW0",
       "move ONE switch at a time"],
    S=[["לנועל יש כניסת אפשור וכניסת נתון. כשהאפשור פעיל - הוא מעתיק את הנתון; אחרת - הוא זוכר.",
        "עברו בדרך הזו:", "00  ->  01  ->  11  ->  10  ->  00          (SW9 SW8)",
        "הנורה השתנתה לפחות פעם אחת? הרימו:", "SW0"],
       ["מי האפשור? קבעו כניסה אחת והזיזו את השנייה למעלה ולמטה.",
        "האפשור הוא הכניסה שבאחד המצבים שלה הנורה הולכת אחרי השנייה, ובמצב השני לא זזה.",
        "הרימו:", "A (SW9) = SW1      B (SW8) = SW0"],
       ["האפשור פעיל כשהוא 1 או כשהוא 0?", "הרימו:", "SW0 = 1: active when 1      (SW0 = 0: active when 0)"]]),

"SEQ": dict(title="צירופי או סדרתי? (8 קופסאות)",
    B=["A = SW9     B = SW8     box i = LEDGi (8 boxes)     answer: SW7..SW0",
       "move ONE switch at a time"],
    S=[["קופסה 0 בלי זיכרון. נסו את 4 המצבים ורשמו את", "LEDG0:", "SW9 SW8:   00   01   10   11",
        "לכל מצב שהנורה דלקה - הרימו:", "00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3"],
       ["קופסה 1 זוכרת. התחילו ב-", "00:", "1)  SW8 up, SW8 down      2)  SW9 up, SW9 down",
        "בשתי הפעמים חזרתם ל-00, אבל הנורה שונה - היא זוכרת מה היה קודם.",
        "הרימו מתג אם הנורה דלקה:", "SW1 = after 1)      SW0 = after 2)"],
       ["אילו עוד קופסאות זוכרות? עברו בשתי הדרכים ורשמו את כל הנורות בסוף:",
        "path 1:  00 -> 01 -> 11 -> 10 -> 00",
        "path 2:  00 -> 10 -> 11 -> 01 -> 00",
        "הרימו מתג לכל קופסה שהנורה שלה שונה בסוף:", "LEDGi -> SWi"],
       ["יש קופסאות שזוכרות רק במצב אחר. הגיעו לכל מצב משני השכנים שלו,",
        "ובדקו אם נורה תלויה במאיפה באתם. הרימו מתג לכל קופסה עם זיכרון:", "LEDGi -> SWi"]]),
}

# The data of each question, shown on EVERY step (with the B lines): what the board holds, in one Hebrew line.
DATA = {
    "GATE": ["בלוח מוסתר שער אחד. שתי כניסות, יציאה אחת - הנורה הירוקה."],
    "SIGMA": ["בלוח מוסתרת פונקציה של שלוש כניסות. הפונקציה היא הנורה הירוקה."],
    "TERMS": ["בלוח 4 נורות ירוקות. כל נורה היא איבר אחד (מכפלה או סכום) של שלוש הכניסות."],
    "MATTER": ["בלוח פונקציה של שלוש כניסות - הנורה הירוקה. כניסה אחת לא משפיעה עליה אף פעם."],
    "SIGMA4": ["בלוח פונקציה של ארבע כניסות - הנורה הירוקה. יש לה 16 מצבים."],
    "THEOREMS": ["בלוח 4 טענות מהצורה: צד שמאל = צד ימין. כל טענה מוצגת בשתי נורות."],
    "THEOREMS8": ["בלוח 8 טענות מהצורה: צד שמאל = צד ימין. כל טענה מוצגת בשתי נורות."],
    "MINSOP": ["הפונקציה בשאלה היא הנורה הירוקה. טבלת האמת שלה: הנורה בכל אחד מ-8 המצבים:",
               "SW9 SW8 SW7:   000   001   010   011   100   101   110   111      (0 = down, 1 = up)"],
    "LITERAL": ["הלוח מחשב את הביטוי שלכם, עם האות המוסתרת. התוצאה היא הנורה הירוקה."],
    "STORY": ["בלוח 4 מעגלים של סטודנטים לסיפור שלכם. רק אחד מהם נכון."],
    "DEMORGAN": ["בלוח 4 תשובות של סטודנטים לביטוי שלכם. רק אחת נכונה."],
    "ERRORS": ["בלוח 4 פישוטים של הביטוי שלכם. שניים מהם שגויים."],
    "MULTIPLY": ["בלוח 4 תשובות להכפלה או לפירוק של הביטוי שלכם. שתיים נכונות."],
    "STORY4": ["בלוח 4 מעגלים לסיפור שלכם (ארבע אותיות). רק אחד נכון."],
    "DEMORGAN4": ["בלוח 4 תשובות לביטוי שלכם. אחת או שתיים נכונות."],
    "ERRORS5": ["בלוח 5 פישוטים של הביטוי שלכם. חלקם שגויים."],
    "MULTIPLY4": ["בלוח 6 תשובות להכפלה או לפירוק של הביטוי שלכם. שתיים נכונות."],
    "MUX": ["בלוח מרבב: שני קווי בחירה בוחרים איזו מ-4 הכניסות תגיע לנורה הירוקה."],
    "DECODER": ["בלוח מפענח: בכל מצב דולקת בדיוק נורה אחת, אבל הסדר של הנורות מוסתר."],
    "PRIORITY": ["בלוח מעגל עדיפויות: כשכמה כניסות למעלה, רק החזקה מביניהן מדליקה את הנורה שלה."],
    "MUXLOGIC": ["בלוח פונקציה של שלוש כניסות - הנורה הירוקה. בונים אותה ממרבב עם קווי הבחירה שלכם."],
    "DEC38": ["בלוח מפענח עם 8 יציאות: בכל מצב דולקת נורה אחת, בסדר מוסתר."],
    "NANDNOR": ["בלוח מעגל של שתי רמות: שני שערים ראשונים, ושער אחרון שמקבל אותם."],
    "GATES": ["בלוח שלושה שערים בשרשרת. כל צומת מוצג בנורה."],
    "BUBBLES": ["הלוח מחזיק אחד מארבעת המעגלים שלכם. התוצאה היא הנורה הירוקה."],
    "NANDNOR3": ["בלוח מעגל של שתי רמות: שלושה שערים ראשונים, ושער אחרון שמקבל אותם."],
    "BUBBLES8": ["הלוח מחזיק אחד משמונת המעגלים שלכם. התוצאה היא הנורה הירוקה."],
    "LATCH": ["בלוח קופסה עם זיכרון: מצב אחד מדליק אותה, מצב אחד מכבה, ובשני האחרים היא זוכרת."],
    "DLATCH": ["בלוח נועל: כשהאפשור פעיל הוא מעתיק את הנתון; כשלא - הוא זוכר."],
    "SEQ": ["בלוח 8 קופסאות עם אותן שתי כניסות. לחלק מהן יש זיכרון."],
}

# Only the data a step needs (the user, 2026-10-08): the DATA line goes into the steps listed here (default: all),
# and the student's own text only into steps with an "@P" line - ADD_P adds it where a step uses it.
DATA_STEPS = {"LITERAL": [2, 3], "STORY": [1, 3], "DEMORGAN": [2, 3], "ERRORS": [2, 3], "MULTIPLY": [2, 3],
              "STORY4": [1, 3], "ERRORS5": [2, 3], "MUXLOGIC": [2, 3, 4, 5], "BUBBLES": [2], "BUBBLES8": [2]}
ADD_P = {"LITERAL": {3: "הביטוי שלכם:"}, "STORY": {2: "הסיפור שלכם:", 3: "הסיפור שלכם:"},
         "STORY4": {2: "הסיפור שלכם:", 3: "הסיפור שלכם:"},
         "MUXLOGIC": {2: "קווי הבחירה שלכם:", 3: "קווי הבחירה שלכם:", 4: "קווי הבחירה שלכם:", 5: "קווי הבחירה שלכם:"}}

# personal lines: a Hebrew label line, then the English line(s)
STORY_HE = ["הולכים לפארק אם לא יורד גשם, ויש כריכים או שתייה.",
            "האזעקה מצלצלת כשהדלת פתוחה והמערכת דרוכה, או כשיש עשן.",
            "האור דולק כשחשוך ומישהו זז - אבל אף פעם לא כשהסוללה חלשה.",
            "נכנסים עם כובע ונעליים, או עם כובע ובלי נעליים.",
            "המאוורר פועל כשחם והחלון לא פתוח, או כשילד לוחץ על הכפתור.",
            "מנצחים אם מקבלים מיליון או מחברת - אבל רק אם משחקים."]
STORY_LET = ["P = park   R = rain   S = sandwiches   D = drinks",
             "Y = alarm   D = door open   A = armed   S = smoke",
             "L = light   D = dark   M = someone moves   B = battery low",
             "E = enter   H = hat   S = shoes",
             "F = fan   H = hot   O = window open   K = kid presses",
             "W = win   M = million   N = notepad   P = play"]
STORY4_HE = ["אפשר לאכול אוכל טעים אם מכינים לבד, או שיש שף פרטי מוכשר ולא יקר.",
             "האזעקה מצלצלת כשהדלת פתוחה והמערכת דרוכה, או כשיש עשן ולא מדובר בבדיקה.",
             "עוברים אם הגישו שיעורי בית, ומבחן או מעבדה - אלא אם העתיקו.",
             "האור דולק כשחשוך ומישהו זז, או כשהמתג דלוק - אבל אף פעם לא כשהסוללה חלשה.",
             "נכנסים עם כובע ונעליים, או עם כובע וכרטיס, או אם אתם אורחי כבוד.",
             "המאוורר פועל כשחם והחלון לא פתוח, או כשילד לוחץ על הכפתור."]
STORY4_LET = ["E = eat   M = make it yourself   C = chef   T = talented   X = expensive",
              "Y = alarm   D = door open   A = armed   S = smoke   T = test",
              "P = pass   H = homework   E = exam   L = lab   C = cheated",
              "Y = light   D = dark   M = moves   S = switch   B = battery low",
              "E = enter   H = hat   S = shoes   T = ticket   V = VIP",
              "F = fan   H = hot   O = window open   K = kid   B = button"]

def after(line, mark):
    i = line.find(mark)
    return line[i:].strip() if i >= 0 else line.strip()

def personal(name, P):
    out = {}
    for k, ls in P.items():
        first = ls[0]
        if name in ("THEOREMS", "THEOREMS8"):
            out[k] = [first.split(":", 1)[1].strip()]
        elif name in ("LITERAL",):
            out[k] = [after(first, "Y =").split("  ")[0].strip(), "? = A, A', B, B', C or C'"]
        elif name in ("DEMORGAN", "DEMORGAN4"):
            out[k] = [after(first, "Y =")]
        elif name in ("ERRORS", "ERRORS5"):
            out[k] = [after(first, "Y =")]
        elif name in ("MULTIPLY", "MULTIPLY4"):
            out[k] = [after(first, "Y =")]
        elif name == "STORY":
            out[k] = [STORY_HE[k], STORY_LET[k], ls[1].replace("Letters:", "switches:")]
        elif name == "STORY4":
            out[k] = [STORY4_HE[k], STORY4_LET[k], ls[1].replace("Letters:", "switches:")]
        elif name == "DECODER":
            out[k] = [first.split(":", 1)[1].strip()]
        elif name == "MUXLOGIC":
            out[k] = ["קווי הבחירה של המרבב שלכם:", first.split(":", 1)[1].strip()]
        elif name == "DEC38":
            out[k] = [first.split(":", 1)[1].strip()]
        elif name in ("BUBBLES", "BUBBLES8"):
            out[k] = [l.strip() for l in ls[1:]]
        else:
            out[k] = ls
    return out

def apply_hebrew(questions):
    for q in questions:
        h = HE.get(q.name)
        if not h:
            continue
        assert len(h["S"]) == len(q.steps), (q.id, q.name, len(h["S"]), len(q.steps))
        q.title = h["title"]
        q.B = h["B"]
        q.P = personal(q.name, q.P) if q.P else {}
        steps = []
        for k, (lines, (_, fn)) in enumerate(zip(h["S"], q.steps), 1):
            pre = DATA[q.name] if k in DATA_STEPS.get(q.name, range(1, 9)) else []
            if k in ADD_P.get(q.name, {}):
                pre = pre + [ADD_P[q.name][k], "@P"]
            steps.append((pre + lines, fn))
        q.steps = steps
        if q.P:		# a question with personal data must show it somewhere
            assert any("@P" in ls for ls, _ in q.steps), q.name
        for lines in h["S"]:
            for l in lines:
                he = any("֐" <= c <= "׿" for c in l)
                lat = any(c.isascii() and c.isalpha() for c in l)
                assert not (he and lat), (q.name, l)
