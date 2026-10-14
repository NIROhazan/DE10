// Israeli hardware startup news, two slides per course week (2-11): the story with a question, then the answer, in the style of L1_2026.pptx (4:3, black band, amber title, Hebrew RTL).
const pptxgen = require("pptxgenjs");
const { applyTheme } = require("./apply_theme.js");

const OUT = process.argv[2] || "news_weeks.pptx";
const THEME = {
  name: "DE10 news",
  headFontFace: "Arial",
  bodyFontFace: "Arial",
  colors: {
    dk1: "000000", lt1: "FFFFFF", dk2: "2B2B2B", lt2: "FFF4CC",
    accent1: "FFC700", accent2: "60B5CC", accent3: "E66C7D", accent4: "6BB76D", accent5: "E88651", accent6: "5A6378",
    hlink: "1F5FA8", folHlink: "5A6378",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_4x3";              // 10 x 7.5 in, like the lecture decks
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "חדשות מסטארטאפים ישראליים - שבוע אחר שבוע";
pres.author = "Digital Systems course";
pres.rtlMode = true;
const C = pres.SchemeColor;
const HE = { rtlMode: true, lang: "he-IL", align: "right" };

pres.defineSlideMaster({
  title: "NEWS",
  background: { color: C.background1 },
  objects: [
    { rect: { x: 0, y: 0, w: 10, h: 1.5, fill: { color: C.text1 } } },
    { placeholder: { options: { name: "kicker", type: "body", x: 0.5, y: 0.18, w: 9, h: 0.4, fontSize: 14, color: C.background1, align: "right", rtlMode: true, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.55, w: 9, h: 0.8, fontSize: 30, bold: true, color: C.accent1, align: "right", rtlMode: true, margin: 0, valign: "middle" }, text: "" } },
  ],
  slideNumber: { x: 9.2, y: 7.05, w: 0.5, h: 0.3, fontSize: 10, color: C.accent6 },
});

// ---- the ten stories. Every fact on a slide is from the source in `notes`; the link to the week is ours, and says so.
// Each week has two slides: the story with a question (week N), and the answer with the reason (shown at the start of week N+1).
const S = [
  {
    week: 2, topic: "בינארי, מספרים עם סימן, שערים וטרנזיסטורים",
    riddle: "63 ועוד 1 יוצא מינוס 64. איך?",
    company: "Hailo", title: "Hailo: אותם 8 ביטים, שתי משמעויות",
    what: "Microchip השלימה בספטמבר 2026 את רכישת Hailo הישראלית, שמפתחת שבבי בינה מלאכותית למצלמות ולרכבים. השבבים של Hailo מחשבים במספרים שלמים קטנים: המשקלים של הרשת נשמרים כמספרים עם סימן, והערכים שעוברים בין השכבות כמספרים בלי סימן.",
    stat: "INT8", statLabel: "משקלים עם סימן, ערכים בלי סימן (מסמכי Hailo)",
    link: "השבוע: מספרים בינאריים עם סימן ובלי סימן. אותם 8 ביטים הם 0 עד 255 כמספר בלי סימן, או מינוס 128 עד 127 כמספר עם סימן. החומרה לא יודעת מה הם, רק הדרך שבה קוראים אותם קובעת.",
    q: "מה הערך של 11111111 כמספר בלי סימן? ומה כמספר עם סימן?",
    ans: "255 בלי סימן, ומינוס 1 עם סימן.",
    why: "בלי סימן, כל ביט שווה חזקה של 2: 128 + 64 + ... + 1 = 255. במשלים ל 2 לביט העליון יש משקל שלילי: מינוס 128 ועוד 127 = מינוס 1. אותו מעגל מחבר את שניהם, רק הפירוש שונה, ולכן Hailo רושמת ליד כל מספר אם הוא עם סימן. וזו גם החידה: ב 7 ביטים עם סימן, 0111111 ועוד 1 = 1000000, וזה מינוס 64.",
    url: "https://hailo.ai/de/developer-zone/training-and-support/hailo-quantization-scheme-2/",
    notes: "Hailo quantization scheme (hailo.ai): weights are signed int4/int8/int16, activations unsigned uint8/uint16 with a zero point. Microchip completed the acquisition of Hailo on 21.9.2026 (Nasdaq / Microchip press release, https://www.nasdaq.com/articles/microchip-technology-completes-acquisition-hailo). The answer is on the next slide; show it at the start of week 3.",
  },
  {
    week: 3, topic: "טבלאות אמת, דה מורגן, רכיבי בנייה",
    riddle: "שלושה מתגים הופכים שבב אחד למכונות שונות. איך?",
    company: "Xsight Labs", title: "Xsight Labs: מתג שמשנה תפקיד",
    what: "Xsight Labs הישראלית גייסה ביולי 2026 יותר מ 300 מיליון דולר, לפי שווי של 2.8 מיליארד דולר. המתג שלה, X2, מעביר 12.8 טרה ביט בשנייה בפחות מ 200 וואט, ויש לו נתיב נתונים שאפשר לתכנת מחדש ולהתאים ליישומי רשת שונים תוך כדי עבודה.",
    stat: "$2.8B", statLabel: "שווי, יולי 2026",
    link: "השבוע: טבלאות אמת ורכיבי בנייה כמו הבורר (מרבב). כמה ביטים של בחירה מחליטים איזה מעגל מחובר ליציאה. כך שלושה מתגים בלוח שלכם הופכים את אותו שבב למכונות שונות.",
    q: "לבורר יש 3 קווי בחירה. בין כמה כניסות הוא יכול לבחור?",
    ans: "בין 8 כניסות.",
    why: "כל קו בחירה הוא ביט, ו 3 ביטים נותנים 2 בחזקת 3 = 8 צירופים. כל צירוף מחבר כניסה אחרת ליציאה, ושורה אחרת בטבלת האמת. זו התשובה לחידה: SW9, SW8, SW7 הם 3 קווי בחירה, ולכן בלוח של מעבדה 1 יש 8 קלפים, 8 מעגלים שהבורר בוחר ביניהם. ביט בחירה רביעי היה מכפיל את המספר ל 16.",
    url: "https://siliconangle.com/2026/07/30/programmable-networking-chip-startup-xsight-labs-raises-300m/",
    notes: "SiliconANGLE 30.7.2026: more than $300M at a $2.8B valuation; X2 switch 12.8 Tb/s under 200 W with a 'reprogrammable data plane' that can be 'reconfigured for different network applications on the fly'. That a few configuration bits choose the function is OUR teaching link, not a claim about how X2 is built. Lab 1: SW9..SW7 pick one of 8 cards.",
  },
  {
    week: 4, topic: "מפות קרנו, השהיות, תיאור חומרה",
    riddle: "אותו שבב הפך למשחק. איך הוא נהיה מעגל אחר?",
    company: "NextSilicon", title: "NextSilicon: שבב שמתארגן לפי התוכנית",
    what: "NextSilicon הישראלית השיקה באוקטובר 2025 את Maverick-2. אין בו מונה תוכנית שמריץ פקודה אחרי פקודה: התוכנה של החברה ממפה את החלקים העמוסים של התוכנית על רשת של יחידות חישוב, ומשנה את המיפוי בזמן ריצה. לפי החברה, בבדיקה HPCG הוא מגיע לביצועים של מעבד גרפי בערך בחצי מההספק.",
    stat: "½", statLabel: "מההספק של מעבד גרפי, לפי החברה, אוקטובר 2025",
    link: "השבוע: תיאור חומרה בקוד. הקוד שתכתבו לא רץ על הלוח, הוא הופך לחיבורים בין שערים. כשטוענים קובץ אחר, אותו שבב נהיה מעגל אחר, כמו המשחק בשיעור הראשון.",
    q: "מה ההבדל בין מעבד שמריץ תוכנה לבין FPGA שטוענים לתוכו מעגל חדש?",
    ans: "המעבד נשאר אותו מעגל ומבצע פקודות אחת אחרי השנייה. ב FPGA המעגל עצמו משתנה.",
    why: "ב FPGA יש עשרות אלפי טבלאות אמת קטנות (LUT) ומתגים שמחברים ביניהן. קובץ ה sof קובע מה כתוב בכל טבלה ומה מחובר למה, ולכן אחרי טעינה החיבורים עצמם אחרים: כך אותו שבב נהיה משחק. Maverick-2 באמצע הדרך: יחידות החישוב קבועות, אבל מה שכל אחת מחשבת והחיבורים ביניהן נקבעים לפי התוכנית.",
    url: "https://www.nextsilicon.com/insights/elads-blog-Maverick2-launch/",
    notes: "NextSilicon blog and ServeTheHome (https://www.servethehome.com/nextsilicon-maverick-2-brings-dataflow-and-hbm3e-to-hpc-customers/), October 2025: dataflow architecture, no program counter, software maps hot code onto an ALU grid and re-optimizes at run time. ServeTheHome compares it to an FPGA but it is not one. The HPCG figure (GPU-class performance at about half the power) is a company claim. Note: an earlier draft said Maverick-2 'avoids division by using shifts' - that was wrong and is not on the slide.",
  },
  {
    week: 5, topic: "תפסנים, דלגלגים ואוגרים",
    riddle: "הנורה נשארת דולקת בלי שאף אחד לוחץ. איפה נשמר ה'דולק'?",
    company: "RAAAM", title: "RAAAM: איפה נשמר הביט?",
    what: "RAAAM מפתח תקווה פיתחה זיכרון GCRAM, שמחליף את זיכרון ה SRAM שבתוך שבבים. בספטמבר 2026 הודיעו GlobalFoundries ו RAAAM על פיתוח משותף ועל שבב ניסוי. לפי GlobalFoundries: 40% פחות שטח ועד 60% פחות הספק מ SRAM. בנובמבר 2025 גייסה החברה 17.5 מיליון דולר בהובלת NXP.",
    stat: "40%", statLabel: "פחות שטח מ SRAM, לפי GlobalFoundries",
    link: "השבוע: תפסנים ודלגלגים. תא SRAM שומר ביט בתפסן: שני מהפכים שמזינים זה את זה, כמו הנורה שנשארת דולקת. תא GCRAM שומר את הביט כמטען חשמלי קטן, שדולף לאט, ולכן צריך לרענן אותו מדי פעם.",
    q: "למה תפסן לא צריך רענון, ומטען כן?",
    ans: "בתפסן כל מהפך מחזק מחדש, כל הזמן, את הערך של השני. מטען רק דולף.",
    why: "בתפסן שני מהפכים מחוברים במעגל: 1 ביציאה של האחד מכריח 0 אצל השני, וה 0 מכריח 1 אצל הראשון. כל עוד יש חשמל הם משחזרים את הערך בעצמם, וזו התשובה לחידה: ה'דולק' נשמר בלולאת המשוב. בתא מטען אין משוב, המטען דולף, ולכן צריך לקרוא אותו ולכתוב אותו מחדש מדי פעם. המחיר של התפסן: יותר טרנזיסטורים לכל ביט.",
    url: "https://gf.com/news-and-events/news/gf-and-raaam-memory-technologies-announce-the-joint-development-of-next-generation-gcram-technology-and-test-chip-on-fdx-platform/",
    notes: "GF press release 2.9.2026: joint development and test chip on 22FDX; GCRAM up to 40% smaller area and up to 60% lower power than SRAM. Series A $17.5M led by NXP, November 2025 (Calcalist, https://www.calcalistech.com/ctechnews/article/sjjv3pp1bg). RAAAM says 2-3 transistors per bit vs 6-8 for SRAM (https://alientt.com/client/raaam/). Gain cell = charge storage needing refresh, SRAM = cross-coupled inverters: EPFL (https://infoscience.epfl.ch/handle/20.500.14299/252284).",
  },
  {
    week: 6, topic: "מכונות מצבים ובקר הרמזור",
    riddle: "המחסום יודע ששילמת. איך הוא זוכר מה קרה?",
    company: "Particula", title: "GoChess: לוח שזוכר את כל המשחק",
    what: "Particula הישראלית גייסה 15 מיליון דולר בספטמבר 2026. הלוח שלה, GoChess, מזהה בחיישנים מגנטיים אם יש כלי על כל משבצת, ומדליק נורות שמראות מהלכים. החיישנים לא יודעים איזה כלי עומד שם: הלוח יודע את העמדה רק כי המשחק מתחיל מהעמדה הרגילה, והוא עוקב אחרי כל מהלך מאז.",
    stat: "$15M", statLabel: "גיוס, ספטמבר 2026",
    link: "השבוע: מכונות מצבים. המצב הוא הזיכרון של מה שקרה עד עכשיו. החיישנים של הלוח רואים רק 'יש כלי' או 'אין כלי', כמו שהחיישן של המחסום רואה רק מכונית. שניהם יודעים יותר, כי הם זוכרים.",
    q: "כלי זז ממשבצת אחת לאחרת. החיישנים רואים רק שמשבצת אחת התרוקנה ואחרת התמלאה. מה עוד הלוח צריך כדי לדעת איזה כלי זז?",
    ans: "את המצב הקודם: איזה כלי עמד במשבצת שהתרוקנה.",
    why: "זו מכונת מצבים: המצב הבא הוא פונקציה של המצב הנוכחי ושל הכניסה. הכניסה לבדה (יש כלי, אין כלי) לא מספיקה, צריך את הזיכרון של כל מה שקרה מההתחלה. לכן הלוח חייב להתחיל מעמדה ידועה, כמו שמכונת מצבים מתחילה ממצב reset. וכך המחסום: החיישן רואה רק מכונית, והמצב 'שולם' זוכר את התשלום.",
    url: "https://support.particula-tech.com/hc/en-us/articles/16135035627164-How-does-the-GoChess-board-know-if-it-s-arranged-correctly",
    notes: "Particula support page: magnetic sensors under each square detect presence only; the board knows the pieces because the game starts from the standard position and it tracks every move. $15M round: Calcalist, September 2026 (https://www.calcalistech.com/ctechnews/article/bkj3znn00ze).",
  },
  {
    week: 7, topic: "מור ומילי, תכנון מכונות מצבים",
    riddle: "אותו כפתור, שתי נורות: אחת מיד, אחת מחכה ולפעמים מפספסת. למה?",
    company: "Quantum Source", title: "Quantum Source: לזכור את הראשון, לחכות לשני",
    what: "Quantum Source מרחובות הציגה באוקטובר 2026 את QS-LINK, חיבור בין מחשבים קוונטיים. כל ניסיון לשלוח פוטון מצליח בערך פעם אחת מתוך 100, ולכן שני פוטונים שמגיעים יחד מצליחים בערך פעם אחת מתוך 10,000. QS-LINK שומר את הראשון בזיכרון של אטום ומחכה לשני.",
    stat: "פי 60", statLabel: "פחות ניסיונות, לפי סימולציות של החברה",
    link: "השבוע: מור ומילי. אירוע שצריך לקרות בדיוק יחד עם אירוע אחר כמעט תמיד מתפספס. מכונה שזוכרת שהראשון כבר קרה יכולה לחכות לשני. כך גם הנורה שמחכה לשעון: היא מפספסת לחיצה קצרה שלא נפלה על עליית שעון.",
    q: "איך נוודא שהנורה שמחכה לשעון לא תפספס לחיצה קצרה?",
    ans: "לזכור את הלחיצה: תפסן שנדלק ברגע הלחיצה ונשאר דלוק עד שהמכונה קוראת אותו.",
    why: "הנורה המיידית מחוברת ישר לכפתור, כמו יציאה של מכונת מילי, ולכן מגיבה מיד. הנורה השנייה היא יציאה של מכונת מור: היא משתנה רק בעליית שעון. לחיצה שהתחילה ונגמרה בין שתי עליות לא נראית אף פעם. כשזוכרים שהלחיצה קרתה, היא כבר לא חייבת ליפול על הרגע הנכון. זה גם הרעיון של QS-LINK: לזכור את הראשון, במקום לדרוש ששניהם יגיעו יחד.",
    url: "https://quantumcomputingreport.com/quantum-source-introduces-memory-assisted-photonic-interconnect-to-unify-multi-modal-quantum-computing/",
    notes: "Quantum Computing Report, 8.10.2026: QS-LINK, memory-assisted photonic interconnect. About 1% success per attempt, about 1 in 10,000 for two coincident photons; an atom stores the first and waits; about 60x fewer attempts. These numbers are from the company's modeling, not a demonstration. The Moore/Mealy link is our teaching analogy.",
  },
  {
    week: 8, topic: "זמני התקנה והחזקה, הטיית שעון, מסנכרנים",
    riddle: "שעון מהיר יותר נותן תשובות שגויות, לא רק מהירות יותר. למה?",
    company: "proteanTecs", title: "proteanTecs: כמה זמן נשאר לאות?",
    what: "proteanTecs הישראלית מכניסה לתוך שבבים סוכנים קטנים, שמודדים כל הזמן כמה מרווח זמן נשאר על מסלולים אמיתיים בשבב, ומתריעים לפני שהשבב מתחיל לטעות. במרץ 2026 קיבלה השקעה אסטרטגית מקרן ההון של קבוצת TOPPAN היפנית.",
    stat: "TOPPAN", statLabel: "השקעה אסטרטגית, מרץ 2026",
    link: "השבוע: זמן התקנה. אם האות מגיע לדלגלג מאוחר מדי, נשמרת תשובה שגויה בלי שום הודעת שגיאה. כך עבדה חוגת המהירות במעבדה 1: שעון מהיר יותר, יותר תשובות שגויות.",
    q: "מסלול בין שני דלגלגים לוקח 4 ננו שניות. עד איזה תדר שעון הוא יעבוד נכון?",
    ans: "עד 250 מגה הרץ, ובפועל קצת פחות.",
    why: "מחזור השעון חייב להיות ארוך מזמן המסלול: 1 חלקי 4 ננו שניות = 250 מגה הרץ. צריך להוסיף את זמן ההתקנה של הדלגלג ואת הטיית השעון, ולכן התדר המרבי נמוך יותר. בשעון מהיר יותר הדלגלג דוגם את התוצאה לפני שהיא מוכנה ושומר ערך שגוי, וזו החידה. הסוכנים של proteanTecs מודדים כמה מרווח נשאר, לפני שזה קורה.",
    url: "https://proteantecs.com/news/proteantecs-receives-strategic-investment-from-toppan-group-venture-arm-tgvp",
    notes: "proteanTecs press release, 4.3.2026: strategic investment from TOPPAN Group's venture arm (TGVP). Timing-margin agents in real paths: Semiconductor Engineering (https://semiengineering.com/navigating-timing-margins-like-waze).",
  },
  {
    week: 9, topic: "מחברים, הצצה קדימה, משווים",
    riddle: "החיבור הגדול נכשל לפני החיבור הקטן. למה?",
    company: "Chain Reaction", title: "Chain Reaction: מיליארדי חיבורים בשנייה",
    what: "Chain Reaction הישראלית השיקה באוקטובר 2025 את EL3CTRUM, שבב לכריית ביטקוין בטכנולוגיה של 3 ננומטר. כרייה היא חישוב של הפונקציה SHA-256 שוב ושוב, ו SHA-256 בנויה בעיקר מחיבורים של מספרים בני 32 ביט.",
    stat: "3nm", statLabel: "שבב כרייה, אוקטובר 2025",
    link: "השבוע: מחבר אדווה והצצה קדימה. במחבר אדווה הנשא עובר מביט לביט, ולכן חיבור גדול איטי יותר. במחקרים על שבבי SHA-256, החיבורים הם המסלול האיטי ביותר, ולכן משתמשים בהם במחברים עם הצצה קדימה.",
    q: "במחבר אדווה של 32 ביט, דרך כמה מחברים מלאים עובר הנשא במקרה הגרוע?",
    ans: "דרך כל ה 32.",
    why: "במקרה הגרוע, למשל 11...1 ועוד 1, נשא שנוצר בביט 0 עובר דרך כל המחברים עד הביט העליון, וכל מחבר מוסיף השהיה. לכן הזמן גדל עם מספר הביטים, וחיבור גדול נכשל בשעון שבו חיבור קטן עוד מספיק: זו החידה, וראינו אותה בחוגת המהירות. מחבר עם הצצה קדימה מחשב את הנשאים במקביל, וההשהיה שלו גדלה רק כמו הלוגריתם של מספר הביטים.",
    url: "https://chain-reaction.io/news-medias/el3ctrum-e31-industry-leading-bitcoin-mining-platform/",
    notes: "Chain Reaction, EL3CTRUM launch, 6.10.2025 (8 days more than a year ago). SHA-256 uses 32-bit additions mod 2^32; the adders set the critical path: Dadda et al., DATE 2004 (https://past.date-conference.com/proceedings-archive/2017/pyear/PAPERS/2004/DATE04/DF_FILES/04D_5.PDF); carry-lookahead / carry-reduced adders in SHA-256 ASICs: https://bitslog.com/2015/02/17/faster-sha-256-asics-using-carry-reduced-adders/ . We do not know which adder EL3CTRUM uses.",
  },
  {
    week: 10, topic: "ALU, הזזות, כפל וחילוק",
    riddle: "חלוקה ב 8 רק מזיזה את הנורות, וחלוקה ב 6 מערבבת אותן. למה חילוק יקר?",
    company: "NextSilicon", title: "Arbel: גם במעבד, חילוק הוא תוספת",
    what: "ביוני 2026 הודיעה NextSilicon שתהפוך את ליבת ה RISC-V שלה, Arbel, למעבד שרתים של 64 או 128 ליבות. כל ליבה מבצעת עד 10 פקודות במחזור שעון, ב 3.4 גיגה הרץ. המעבד צפוי ב 2028.",
    stat: "10", statLabel: "פקודות במחזור שעון, בכל ליבה",
    link: "השבוע: ALU, הזזות, כפל וחילוק. בבסיס של RISC-V אין בכלל פקודת כפל או חילוק: הן בהרחבה נפרדת (M). מעבד קטן יכול לוותר עליהן ולחלק בתוכנה, כי מעגל חילוק תופס הרבה שטח ולוקח הרבה זמן.",
    q: "למה חילוק ב 8 הוא רק הזזה של 3 ביטים, וחילוק ב 6 לא?",
    ans: "כי 8 הוא 2 בחזקת 3, ו 6 אינו חזקה של 2.",
    why: "הזזה ימינה בביט אחד היא חילוק ב 2, כמו שמחיקת הספרה האחרונה במספר עשרוני היא חילוק ב 10. לכן חילוק ב 8 הוא רק חיווט: הביטים זזים 3 מקומות, בלי אף שער. חילוק ב 6 דורש לחסר ולהשוות שוב ושוב, ביט אחרי ביט, כמו חילוק ארוך. זו החידה, ולכן RISC-V שם את החילוק בהרחבה שמעבד קטן יכול לוותר עליה.",
    url: "https://www.nextsilicon.com/insights/nextsilicon-productize-arbel-risc-v-core-into-64core-enterprise-processor-for-ai-hpc/",
    notes: "NextSilicon, 10.6.2026: Arbel RISC-V core productized into a 64/128-core enterprise CPU, 10-wide issue, RVA23 profile, 3.4 GHz, expected 2028. RV32I has no multiply/divide; the M extension adds them (https://arxiv.org/pdf/2010.16171). Second NextSilicon story in the deck (also week 4).",
  },
  {
    week: 11, topic: "נקודה קבועה וצפה, מונים ואוגרי הזזה, זיכרונות",
    riddle: "10 כפול 0.1 יוצא 0.976, אבל 4 כפול 0.25 יוצא בדיוק 1. למה?",
    company: "DustPhotonics", title: "DustPhotonics: ביטים באור",
    what: "Credo השלימה במאי 2026 את רכישת DustPhotonics הישראלית, שמפתחת שבבי סיליקון פוטוניקה: שבבים שהופכים אותות חשמליים לאור, במשדרים אופטיים של 800 גיגה עד 1.6 טרה ביט בשנייה במרכזי נתונים.",
    stat: "1.6T", statLabel: "ביט בשנייה במשדר אחד",
    link: "השבוע: מונים ואוגרי הזזה. סיב אופטי מעביר ביט אחרי ביט, והשבב עובד על מילים שלמות. אוגר הזזה הוא הגשר: הוא טוען מילה שלמה ומוציא אותה ביט אחרי ביט, ובצד השני להפך. ומהחידה של השבוע, על נקודה קבועה:",
    q: "כמה ביטים אחרי הנקודה צריך כדי לכתוב בדיוק 0.25? ו 0.1?",
    ans: "ל 0.25 מספיקים 2 ביטים (0.01). את 0.1 אי אפשר לכתוב בדיוק בשום מספר סופי של ביטים.",
    why: "בבינארי, הביטים אחרי הנקודה שווים חצי, רבע, שמינית וכן הלאה. 0.25 הוא בדיוק רבע. 0.1 בבינארי הוא 0.000110011... שחוזר לנצח. עם 8 ביטים אחרי הנקודה, 0.1 נשמר כ 0.0977, והטעות הקטנה מוכפלת ב 10 ונהיית 0.976. 4 כפול 0.25 יוצא בדיוק 1, כי לא הייתה טעות מלכתחילה.",
    url: "https://s205.q4cdn.com/511065572/files/doc_news/Credo-Completes-Acquisition-of-DustPhotonics-2026.pdf",
    notes: "Credo announced the acquisition 13.4.2026 (https://www.businesswire.com/news/home/20260413933103/en/) and completed it 28.5.2026. DustPhotonics: silicon-photonics PICs for 800G to 1.6T optical transceivers; Credo combines them with its SerDes and DSPs. Serializer = shift register is textbook, not a company claim. The question is about the riddle, not the company. 0.1 with 8 fraction bits, truncated: 25/256 = 0.09765625; x10 = 0.977.",
  },
];

// ---- overview slide
{
  pres.addSection({ title: "סקירה" });
  const s = pres.addSlide({ masterName: "NEWS", sectionTitle: "סקירה" });
  s.addText("חדשות מסטארטאפים ישראליים", { placeholder: "kicker", ...HE });
  s.addText("10 חברות, 10 שבועות, 10 חידות", { placeholder: "title", ...HE });
  const rows = S.map((x) => [
    { text: `שבוע ${x.week}`, options: { bold: true, color: C.text1 } },
    { text: x.company, options: { bold: true, rtlMode: false, align: "left" } },
    { text: x.topic },
  ]);
  // cells in screen order, left to right, so the week ends up in the right-hand column
  s.addTable(
    rows.map((r) => r.slice().reverse().map((c) => ({ text: c.text, options: { ...HE, fontSize: 14, valign: "middle", ...c.options } }))),
    { x: 0.5, y: 1.85, w: 9, colW: [5.3, 2.4, 1.3], rowH: 0.47, border: { type: "solid", pt: 0.75, color: "D4D4D6" }, fill: { color: "FFFFFF" }, objectName: "overview table" }
  );
  s.addNotes("Each week has two slides: the news story with a question (show it in that week), and the answer with the reason (show it at the start of the next week).");
}

// the week's riddle from slide 16 of lecture 1, in an amber strip under the title band
function riddleStrip(s, x) {
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 1.5, w: 10, h: 0.5, fill: { color: C.accent1 }, objectName: "riddle strip" });
  s.addText(
    [
      { text: `החידה של שבוע ${x.week}: `, options: { bold: true } },
      { text: x.riddle },
    ],
    { x: 0.5, y: 1.5, w: 9, h: 0.5, fontSize: 14, color: C.text1, valign: "middle", isTextBox: true, objectName: "riddle", ...HE, margin: 0 }
  );
}

for (const x of S) {
  const sec = `שבוע ${x.week}`;
  pres.addSection({ title: sec });

  // ---- slide 1: the story and the question (week N)
  {
    const s = pres.addSlide({ masterName: "NEWS", sectionTitle: sec });
    s.addText(`שבוע ${x.week} · ${x.topic}`, { placeholder: "kicker", ...HE });
    s.addText(x.title, { placeholder: "title", ...HE });
    riddleStrip(s, x);

    s.addText(
      [
        { text: "מה קרה?", options: { bold: true, fontSize: 17, color: C.text1, breakLine: true } },
        { text: x.what, options: { fontSize: 14, color: C.text1 } },
      ],
      { x: 3.5, y: 2.2, w: 6.0, h: 2.35, valign: "top", paraSpaceAfter: 4, isTextBox: true, objectName: "what happened", ...HE, margin: 0 }
    );

    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 2.25, w: 2.75, h: 2.25, rectRadius: 0.12, fill: { color: C.text2 }, objectName: "stat card" });
    s.addText(x.stat, { x: 0.6, y: 2.35, w: 2.55, h: 1.15, fontSize: 40, bold: true, color: C.accent1, align: "center", valign: "middle", isTextBox: true, objectName: "stat" });
    s.addText(x.statLabel, { x: 0.65, y: 3.5, w: 2.45, h: 0.9, fontSize: 12, color: C.background1, align: "center", valign: "top", rtlMode: true, lang: "he-IL", isTextBox: true, objectName: "stat label" });

    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 4.7, w: 9, h: 2.2, rectRadius: 0.12, fill: { color: C.background2 }, objectName: "link card" });
    s.addText(
      [
        { text: `ומה זה קשור לשבוע ${x.week}?`, options: { bold: true, fontSize: 15, breakLine: true } },
        { text: x.link, options: { fontSize: 14, breakLine: true } },
        { text: "שאלה: ", options: { bold: true, fontSize: 14 } },
        { text: x.q, options: { fontSize: 15 } },
      ],
      { x: 0.75, y: 4.8, w: 8.5, h: 2.0, valign: "top", color: C.text1, paraSpaceAfter: 5, isTextBox: true, objectName: "link text", ...HE, margin: 0 }
    );

    s.addText(x.url, { x: 0.5, y: 6.98, w: 8.5, h: 0.3, fontSize: 8, color: C.accent6, align: "left", hyperlink: { url: x.url }, isTextBox: true, objectName: "source", margin: 0 });
    s.addNotes(x.notes);
  }

  // ---- slide 2: the answer (start of week N+1)
  {
    const s = pres.addSlide({ masterName: "NEWS", sectionTitle: sec });
    s.addText(`תשובה לשאלה של שבוע ${x.week} · ${x.company}`, { placeholder: "kicker", ...HE });
    s.addText("השאלה מהשבוע שעבר", { placeholder: "title", ...HE });
    riddleStrip(s, x);

    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 2.2, w: 9, h: 0.95, rectRadius: 0.12, fill: { color: C.background2 }, objectName: "question card" });
    s.addText(
      [
        { text: "שאלה: ", options: { bold: true } },
        { text: x.q },
      ],
      { x: 0.75, y: 2.2, w: 8.5, h: 0.95, fontSize: 16, color: C.text1, valign: "middle", isTextBox: true, objectName: "question", ...HE, margin: 0 }
    );

    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 3.3, w: 9, h: 1.0, rectRadius: 0.12, fill: { color: C.text2 }, objectName: "answer card" });
    s.addText(
      [
        { text: "תשובה: ", options: { bold: true } },
        { text: x.ans },
      ],
      { x: 0.75, y: 3.3, w: 8.5, h: 1.0, fontSize: 17, color: C.accent1, valign: "middle", isTextBox: true, objectName: "answer", ...HE, margin: 0 }
    );

    s.addText(
      [
        { text: "למה?", options: { bold: true, fontSize: 17, breakLine: true } },
        { text: x.why, options: { fontSize: 16 } },
      ],
      { x: 0.5, y: 4.5, w: 9, h: 2.5, valign: "top", color: C.text1, paraSpaceAfter: 5, isTextBox: true, objectName: "why", ...HE, margin: 0 }
    );
    s.addNotes(`Show at the start of week ${x.week + 1}. ` + x.notes);
  }
}

// pptxgenjs sets rtl="1" on only some paragraphs, and the theme has no font for Hebrew (complex script):
// every paragraph with Hebrew letters becomes right to left, and the theme's cs font becomes Arial.
async function fixHebrew(file) {
  const fs = require("fs");
  const JSZip = require("jszip");
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  for (const name of Object.keys(zip.files)) {
    if (/^ppt\/theme\/theme\d+\.xml$/.test(name)) {
      const xml = await zip.file(name).async("string");
      zip.file(name, xml.replace(/<a:cs typeface=""/g, '<a:cs typeface="Arial"').replace(/(<a:font script="Hebr" typeface=")[^"]*"/g, "$1Arial\""));
    } else if (/^ppt\/(slides|slideLayouts)\/[^/]+\.xml$/.test(name)) {
      const xml = await zip.file(name).async("string");
      const out = xml.replace(/<a:p>([\s\S]*?)<\/a:p>/g, (p, body) => {
        if (!/[֐-׿]/.test(body)) return p;
        // PowerPoint orders a run by its language: in a he-IL run, "NR1" shows as "1NR". English words get their own
        // en-US runs (as PowerPoint itself stores mixed text), Hebrew and plain numbers stay he-IL.
        body = body.replace(/<a:r><a:rPr ([^>]*?)(\/?)>([\s\S]*?)<a:t>([^<]*)<\/a:t><\/a:r>/g, (m, attrs, slash, inner, t) => {
          if (!/lang="he-IL"/.test(attrs) || !/[A-Za-z]/.test(t)) return m;
          const run = (s, lang) => `<a:r><a:rPr ${attrs.replace(/lang="[^"]*"/, `lang="${lang}"`)}${slash}>${inner}<a:t>${s}</a:t></a:r>`;
          const parts = t.split(/((?<![&#\w])[A-Za-z][A-Za-z0-9-]*(?:\s+[A-Za-z0-9][A-Za-z0-9-]*)*)/);
          return parts.map((s, i) => (s === "" ? "" : run(s, i % 2 ? "en-US" : "he-IL"))).join("");
        });
        if (/^<a:pPr\b/.test(body)) {
          return "<a:p>" + body.replace(/^<a:pPr\b([^>]*?)(\/?)>/, (m, attrs, slash) =>
            /\brtl=/.test(attrs) ? m : `<a:pPr rtl="1"${attrs}${slash}>`) + "</a:p>";
        }
        return '<a:p><a:pPr rtl="1"/>' + body + "</a:p>";
      });
      zip.file(name, out);
    }
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  await fixHebrew(OUT);
  console.log("wrote " + OUT);
})();
