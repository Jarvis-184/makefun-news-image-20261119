"""
Verified world news data for Thursday 19 November 2026.
Extracted from news-data.md.
"""

HEADER = "Verified world news — Thursday 19 November 2026 (multi-source cross-checked: Democracy Now headlines 2026-11-19, One Turn day page 2026-11-19, Guardian/Hindu/Euronews archives, yesterday's winning entry's date-check notes)"

CARD_STORIES = [
    {
        "rank": 1,
        "category": "ASIA/LEGAL",
        "text": "ICJ finds Myanmar committed genocide against Rohingya in 2017. First time the UN court has held a state responsible for genocide; reports say a 9-6 vote; case brought by The Gambia; refugees in Bangladesh camps cheered.",
        "source": "ICJ/Reuters",
        "full": "1. ASIA/LEGAL — ICJ finds Myanmar committed genocide against Rohingya in 2017. First time the UN court has held a state responsible for genocide; reports say a 9-6 vote; case brought by The Gambia; refugees in Bangladesh camps cheered. Source: ICJ/Reuters."
    },
    {
        "rank": 2,
        "category": "ASIA/DIPLOMACY",
        "text": "Trump, Xi and Putin hold first three-way summit. Four-point \"peace declaration\": nuclear risk, UN reform, oil and gas, court limits. 70 minutes closed; no Ukraine or Iran mention; Merz warns of \"Yalta-style\" split.",
        "source": "AP/AFP",
        "full": "2. ASIA/DIPLOMACY — Trump, Xi and Putin hold first-ever three-way summit in Shenzhen; issue four-point \"peace declaration\" (nuclear risk reduction, UN reform, oil and gas supply, limits on international courts). ~70 minutes closed-door; no mention of Ukraine or Iran wars; Trump called Putin \"my friend\"; Germany's Merz warns of \"Yalta-style\" division. Source: AP/AFP."
    },
    {
        "rank": 3,
        "category": "BUSINESS/TECH",
        "text": "Anthropic debuts up 17% after history's largest IPO. $83 offer, opened ~$111.50, raised ~$81bn, ~$1.5tn valuation; first major AI lab to go public; 3 arrested at Nasdaq protest.",
        "source": "Reuters/CNBC",
        "full": "3. BUSINESS/TECH — Anthropic closes first trading day up 17% after the largest IPO in history ($83 offer, opened ~$111.50, raised ~$81bn, ~$1.5tn valuation); first major AI lab to go public; 3 arrested at Nasdaq protest. Source: Reuters/CNBC."
    },
    {
        "rank": 4,
        "category": "MARKETS",
        "text": "S&P 500 falls 2.02%, fifth straight loss; Nikkei -4.68%; gold -2.42%; US 10-year yield 5.05%; Fed officials flag AI-driven overheating.",
        "source": "Bloomberg/Reuters",
        "full": "4. MARKETS — S&P 500 falls 2.02%, fifth straight loss; Nikkei -4.68%; gold -2.42%; US 10-year yield 5.05%; Fed officials flag AI-driven overheating. Source: Bloomberg/Reuters."
    },
    {
        "rank": 5,
        "category": "EUROPE/WAR",
        "text": "Ukraine hits Crimean Bridge third time in four days. Russia halts traffic; satellite images show span damage; Putin vows response \"far more painful\", rules out sea or energy truce.",
        "source": "AFP",
        "full": "5. EUROPE/WAR — Ukraine strikes Crimean Bridge for third time in four days; Russia halts traffic; satellite images show span damage; Putin vows response \"far more painful\", rules out sea or energy truce. Source: AFP."
    },
    {
        "rank": 6,
        "category": "EUROPE/DIPLOMACY",
        "text": "European allies claim united line for Russia talks. US envoy Kushner: Russia comfortable with Article 5-style guarantees for Ukraine; Macron urges reopening the NATO membership question.",
        "source": "Reuters",
        "full": "6. EUROPE/DIPLOMACY — European allies meeting in Berlin say they have a united position for talks with Russia; US envoy Jared Kushner says Russia is comfortable with NATO Article 5-style guarantees for Ukraine; Macron urges reopening NATO membership question. Source: Reuters."
    },
    {
        "rank": 7,
        "category": "MIDDLE EAST",
        "text": "Houthi missile hits Riyadh's PIF Tower. Windows broken on several floors of the Saudi capital's tallest building, no injuries; Gulf states condemn.",
        "source": "AFP/SPA",
        "full": "7. MIDDLE EAST — Houthi missile damages Riyadh's Public Investment Fund Tower, the Saudi capital's tallest; windows broken on several floors, no injuries; Gulf states condemn. Source: AFP/SPA."
    },
    {
        "rank": 8,
        "category": "MIDDLE EAST/ENERGY",
        "text": "Iran steps up Hormuz attacks. Tanker burns after mine strike; Senate rejects war-powers curb 51-48; Brent $89.72.",
        "source": "Reuters/IEA",
        "full": "8. MIDDLE EAST/ENERGY — Iran intensifies Strait of Hormuz attacks; tanker catches fire after naval mine east of the strait; US Senate rejects war-powers curb 51-48; IEA says the war leaves lasting marks on energy markets; Brent $89.72 (+0.3%). Source: Reuters/IEA."
    },
    {
        "rank": 9,
        "category": "MIDDLE EAST",
        "text": "Israeli ground op crosses \"Yellow Line\". First op past the line since the ceasefire; tunnel dismantled; thousands displaced near Nuseirat; Hamas: violation.",
        "source": "AP",
        "full": "9. MIDDLE EAST — Israel completes first ground operation beyond Gaza's \"Yellow Line\" since the ceasefire; army says a tunnel was dismantled; thousands of Palestinians displaced near Nuseirat; Hamas calls it a flagrant violation. Source: AP."
    },
    {
        "rank": 10,
        "category": "CLIMATE",
        "text": "COP31 draft drops fossil-fuel language. African nations demand more climate finance at the Turkey talks; Greenpeace protests at venue.",
        "source": "Reuters",
        "full": "10. CLIMATE — COP31 draft in Turkey drops all fossil-fuel language; African nations demand more climate finance; Greenpeace protests at venue. Source: Reuters."
    },
    {
        "rank": 11,
        "category": "SPACE",
        "text": "BepiColombo enters Mercury orbit. After 8+ years, only the second mission ever to orbit the planet; will map surface and study its oversized core.",
        "source": "ESA/JAXA",
        "full": "11. SPACE — BepiColombo enters orbit around Mercury after 8+ years; only the second mission ever to orbit the planet; will map surface and study its oversized core. Source: ESA/JAXA."
    },
    {
        "rank": 12,
        "category": "SPACE",
        "text": "Voyager 1 reaches one light-day away. 26bn km out, the farthest human-made object; still sending data after nearly 50 years; Empire State Building lit gold.",
        "source": "NASA",
        "full": "12. SPACE — Voyager 1 now one full light-day from Earth (over 26 billion km), the farthest human-made object; still sending data after nearly 50 years; Empire State Building lit gold. Source: NASA."
    },
    {
        "rank": 13,
        "category": "CULTURE/GAMES",
        "text": "GTA VI on sale after 13-year wait. Estimated 24.58 million copies on day one (~$2.36bn for Take-Two); PlayStation Network outage before release.",
        "source": "Rockstar/industry estimates",
        "full": "13. CULTURE/GAMES — Grand Theft Auto VI goes on sale after a 13-year wait; estimated 24.58 million copies on day one (~$2.36bn for Take-Two); PlayStation Network outage before release. Source: Rockstar/industry estimates."
    },
    {
        "rank": 14,
        "category": "TECH",
        "text": "Nvidia subpoenaed over China chip risk. California AG acts after CEO Huang quit; AMD -7% on short-seller report; 879,000 AI chips cleared for Chinese firms.",
        "source": "Reuters",
        "full": "14. TECH — California attorney general subpoenas Nvidia over China chip-risk disclosures after CEO Jensen Huang's resignation; interim CEO Colette Kress; AMD falls over 7% on short-seller report; House panel says 879,000 AI chips cleared for Chinese firms in six months. Source: Reuters."
    }
]

NUMBERS_BAND = [
    "S&P 500 -2.02% (5th loss)",
    "Nikkei -4.68%",
    "Brent $89.72",
    "24.58M GTA VI copies day one",
    "589M children in conflict zones (23.4%)",
    "9-6 ICJ vote",
    "~$81bn Anthropic raise",
    "26bn km Voyager 1",
    "51-48 Senate war-powers vote",
    "879,000 AI chips to China"
]

NUMBERS_BAND_RAW = "S&P 500 -2.02% (5th loss) · Nikkei -4.68% · Brent $89.72 · 24.58M GTA VI copies day one · 589M children in conflict zones (23.4%) · 9-6 ICJ vote · ~$81bn Anthropic raise · 26bn km Voyager 1 · 51-48 Senate war-powers vote · 879,000 AI chips to China"

EXTRAS = [
    "Cox's Bazar: Rohingya refugees cheer ICJ verdict in camps",
    "The Hague: ruling may shape pending genocide cases, incl. Gaza",
    "Gaza: Israeli court extends hospital director Abu Safiya's detention by 6 months",
    "Washington: Democrats grill DHS chief Mullin over FAA stop, ICE deaths",
    "Washington: CISA urges immediate Java patch after AI-found flaw (startup Calif)",
    "San Francisco: study (Vals AI) finds advanced AI models flag civilian sites as military targets",
    "Dhaka: Hasina supporters torch property; ~300 arrests; wage protests",
    "Caracas: US and Venezuela sign military cooperation deal (Hegseth, Rodríguez)",
    "Port-au-Prince: Haitian police say 34 gang members killed in Martissant raid",
    "Dakar: dozens missing after migrant boat capsizes off Senegal",
    "Nairobi: US consortium wins Mrima Hill critical-minerals contract (~$60bn)",
    "Copenhagen: Denmark's parliament unanimously ratifies US-Greenland security deal",
    "Geneva: Save the Children — 589 million children (23.4%) live in conflict zones",
    "Madrid: Sánchez admits mistakes in debate with Feijóo; Spain votes 29 November",
    "Buenos Aires: Milei's bill to suspend 2027 primaries clears committee",
    "Cairo: IMF deal unlocks $2.3bn for Egypt",
    "Bangkok: Iran keeper Beiranvand named AFC Player of the Year; Foord top woman",
    "Mirpur: Litton Das sets Test record — 8 dismissals in one innings (6 catches, 2 stumpings)",
    "Turin: Alcaraz beats Medvedev 6-2, 6-4 at ATP Finals despite medical timeout",
    "London: Chelsea beat PSG 1-0 to top Women's Champions League (Buurman 87')",
    "Hobart: England win ODI series in Australia; Duckett century",
    "Wolverhampton: Wattimena knocks champion Littler out of Grand Slam of Darts 10-8",
    "Manchester: Pochettino starts as Man United head coach; Liverpool Sunday",
    "Miami: Giannis scores 27 in first game against former franchise",
    "Juneau: Mary Peltola wins Alaska Senate seat; Democrats reach 56-seat majority",
    "Nashville: Ella Langley sweeps CMA Awards (entertainer, album, single)",
    "New York: Hannah Lillith Assadi wins National Book Award for Paradiso 17",
    "Cambridge: dictionary names \"human\" word of the year, citing AI",
    "Paris: 24-month Comté named world's best cheese",
    "Washington: Trump posthumously pardons baseball's Pete Rose",
    "Cincinnati: Fiona the hippo dies after swallowing a hat",
    "Green Bank: Fermi open data yields pulsar-finding method ~1,000,000x faster",
    "Space: Webb confirms rare supergiant/sun-like star merger; Hera at DART site",
    "Cyclone Akvan: Odisha evacuations continue ahead of Friday landfall"
]

DATE_CHECK = [
    "Jeffries wins Democratic speaker nomination 251-11 (vote was Wed 18)",
    "US loses measles elimination status (announced Wed 18)",
    "Xi greets Trump on the tarmac (arrival, Wed 18)",
    "Cyclone Akvan's landfall itself (expected Fri 20)",
    "COP31 closing outcome (talks end Fri 20)"
]

SOURCE_CREDITS = [
    "Democracy Now",
    "One Turn",
    "Reuters",
    "AP",
    "AFP",
    "BBC",
    "NASA",
    "ESA",
    "ICJ",
    "AFC",
    "IEA",
    "Save the Children"
]

SOURCE_CREDITS_RAW = "Democracy Now, One Turn, Reuters, AP, AFP, BBC, NASA, ESA, ICJ, AFC, IEA, Save the Children."
