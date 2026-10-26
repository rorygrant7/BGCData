================================================================================
           BOARD GAME CLUB (BGC) CHRONICLE & AWARDS PRESENTATION
                    PROJECT SPECIFICATION & ARCHITECTURE
                               "README.TXT"
================================================================================
Version:        1.1.0
Date Updated:   October 2026
Workspace:      /Users/rgrant/Desktop/BGCData
Target Output:  Interactive Slide Deck Web Application (HTML / CSS / JS)
Design Theme:   Blood on the Clocktower (BOTC) Gothic Grimoire Aesthetic
Base Color:     Deep Gothic Purple (#12041D / #1F082F / #2C0D42)

--------------------------------------------------------------------------------
TABLE OF CONTENTS
--------------------------------------------------------------------------------
1. PROJECT OVERVIEW & CORE OBJECTIVES
2. TEMPORAL PARTITIONING & DYNAMIC FILTERING ENGINE
   2.1. Year 1, Year 2, Year 3, and All-Time Date Boundaries
   2.2. Interactive Horizon Filter Specification (UI & Code Architecture)
   2.3. Year-over-Year (YoY) Change Calculation Rules (+Green / -Red)
3. INPUT DATA ARCHITECTURE & INGESTION RULES
   3.1. Google Sheets ("Board Game Club Meeting Tracking")
   3.2. Facebook Messenger History ("message_1.json" & Media Folders)
   3.3. The "Pure Chat" vs. "Poll Response" Distinction (MANDATORY RULE)
   3.4. Messenger Unicode / Mojibake Sanitization Guide
   3.5. Member Alias & Nickname Resolution Dictionary
4. UNIFIED DATABASE SCHEMAS & ENTITY RELATIONSHIP MODEL
   4.1. Entity: Member
   4.2. Entity: Meeting
   4.3. Entity: Game
   4.4. Entity: ChatMessage
   4.5. Entity: Reaction
   4.6. Entity: PollVote
   4.7. Entity: Location
5. DATA PIPELINE & QUERY SPECIFICATION (REUSABLE ENGINE)
   5.1. Pipeline Architecture vs. One-Time Static Generation
   5.2. Core Query Interface Definitions
6. SLIDE DECK BLUEPRINT: "STATS" & "AWARDS"
   6.1. Part 1: "Stats" (Group-Level Comparison & Trends)
        - Average Attendance Comparison by Year (with YoY %)
        - Unique Attendees Comparison by Year (with YoY %)
        - New Attendees Comparison by Year (with YoY %)
        - Games Breakdown & BOTC Script Analysis
        - Cooking & Feast Chronicles
        - Messaging Banter & Activity Trends
   6.2. Part 2: "Awards" (Default: Year 3 Honors)
        - Award 1: Most Popular Post (Most Reacted Message)
        - Award 2: Photographer (Most Photos Posted)
        - Award 3: Videographer (Most Videos Posted)
        - Award 4: Busiest Location (Highest Avg Attendance by Location)
        - Award 5: Busiest Week (Highest Single-Session Turnout)
        - Award 6: Most Popular Emoji (Reaction Frequency & Glyph Display)
        - Award 7: The Grimoire Titan (Top Attendance)
        - Award 8: The Iron Chef (Top Dinners Cooked)
        - Award 9: The Town Crier (Most Pure Chat Messages)
        - Award 10: The Hype Beast (Most Reactions Given)
   6.3. The 4-Stage Podium Reveal Specification (CRITICAL REQUIREMENT)
7. BLOOD ON THE CLOCKTOWER (BOTC) DETAILED STYLE GUIDE
   7.1. Visual Philosophy & Grimoire Atmosphere
   7.2. Master Color Palette (Deep Purple Base + Section Jewel Tones)
   7.3. Textures, Borders, Filigree, and Graphic Elements
   7.4. Typography Hierarchy
   7.5. Motion, Lighting Effects, and Particle Fanfare
8. TECHNICAL IMPLEMENTATION & CODE ARCHITECTURE GUIDELINES
   8.1. Single-File vs. Modular HTML Presentation Engine
   8.2. Slide & Sub-Step State Machine
   8.3. Local Media Asset Resolution
   8.4. Build & Ingestion Pipeline Workflow
9. RULES OF ENGAGEMENT FOR ALL FUTURE AI PROMPTS


================================================================================
1. PROJECT OVERVIEW & CORE OBJECTIVES
================================================================================
The Board Game Club (BGC) Chronicle is a multi-year data-driven celebration and
awards presentation commemorating three complete years of board game sessions,
banquets, group lore, and messaging banter (October 4, 2023 – October 4, 2026).

The ultimate output is an interactive, highly polished HTML slide deck that presents:
1. "Stats": Comparative metrics spanning Year 1, Year 2, and Year 3, displaying
   attendance averages, unique members, new recruits, game counts, and chat trends
   with color-coded Year-over-Year (+Green / -Red) percentage changes.
2. "Awards": Dramatic, category-by-category podium presentations celebrating
   the #3 (Bronze), #2 (Silver), and #1 (Gold) winners. By default, the awards
   focus exclusively on Year 3 (the culmination year), but the underlying code
   must support dynamic filtering for Year 1, Year 2, or All-Time.

This ReadMe.txt is the Single Source of Truth (SSOT). All subsequent HTML code,
data scripts, and styling must adhere strictly to the guidelines herein.


================================================================================
2. TEMPORAL PARTITIONING & DYNAMIC FILTERING ENGINE
================================================================================
The entire history of BGC is strictly divided into three annual cycles:

--------------------------------------------------------------------------------
2.1. Year 1, Year 2, Year 3, and All-Time Date Boundaries
--------------------------------------------------------------------------------
- Year 1 (The Genesis):
  * Start Date: October 4, 2023 (First ever meeting at 115 Highbourne)
  * End Date:   October 3, 2024
  * Total Meetings: 53 (52 Completed, 1 Cancelled)
  * Epoch Range (ms): 1696392000000 <= timestamp < 1727928000000

- Year 2 (The Expansion):
  * Start Date: October 4, 2024
  * End Date:   October 3, 2025
  * Total Meetings: 52 (48 Completed, 4 Cancelled)
  * Epoch Range (ms): 1727928000000 <= timestamp < 1759464000000

- Year 3 (The Golden Era / Culmination):
  * Start Date: October 4, 2025
  * End Date:   October 4, 2026 (inclusive)
  * Total Meetings: 52 (49 Completed, 3 Cancelled)
  * Epoch Range (ms): 1759464000000 <= timestamp <= 1791086400000

- All-Time:
  * October 4, 2023 – October 4, 2026+ (Complete dataset)
  * Total Meetings: 160 (149 Completed, 11 Cancelled / Special)

--------------------------------------------------------------------------------
2.2. Interactive Horizon Filter Specification (UI & Code Architecture)
--------------------------------------------------------------------------------
The presentation web application must incorporate a global or per-slide
temporal filter component:
  [ ALL TIME | YEAR 1 | YEAR 2 | YEAR 3 ]

UI Filter Component Requirements:
- Visual Style: Ornate gothic brass/gold pill buttons styled with deep purple velvet
  backgrounds and glowing amber borders.
- State Sync: When a user selects a horizon:
  * For "Stats" slides: Visualizations instantly update or highlight the selected
    period while showing comparative YoY context.
  * For "Awards" slides: The podium recalculates the top 3 rankings for that
    specific period (Defaulting on load to "Year 3").

--------------------------------------------------------------------------------
2.3. Year-over-Year (YoY) Change Calculation Rules (+Green / -Red)
--------------------------------------------------------------------------------
Whenever a stat is compared to the preceding year, calculate the relative delta:
  Delta = ((Current_Year_Value - Previous_Year_Value) / Previous_Year_Value) * 100

Display Rules:
- Positive Change (> 0%):
  * Prefix: "+"
  * Format: "+X.X%"
  * Color: Glowing Emerald Green (#10B981 / #34D399)
- Negative Change (< 0%):
  * Prefix: "-"
  * Format: "-X.X%"
  * Color: Crimson / Blood Red (#EF4444 / #F87171)
- Neutral / Baseline:
  * Display: "Baseline" or "N/A" (in Muted Silver #94A3B8) for Year 1.


================================================================================
3. INPUT DATA ARCHITECTURE & INGESTION RULES
================================================================================
The project ingests data from two primary inputs located in the workspace:

--------------------------------------------------------------------------------
3.1. Google Sheets ("Board Game Club Meeting Tracking")
--------------------------------------------------------------------------------
- Live Public URL:
  https://docs.google.com/spreadsheets/d/e/2PACX-1vRVYFs2AgGNfSwItq0R1fkB4yK9kF-Bn-AbphiZeCVgZw0V57Q0sSyGp9OMMr26j0PpSKdZf5NIFAES/pubhtml?gid=0&single=true

- Live Direct CSV Export Endpoint:
  https://docs.google.com/spreadsheets/d/e/2PACX-1vRVYFs2AgGNfSwItq0R1fkB4yK9kF-Bn-AbphiZeCVgZw0V57Q0sSyGp9OMMr26j0PpSKdZf5NIFAES/pub?gid=0&single=true&output=csv

- Raw Headers:
  Date | Activity | Attendees | # | Cooks | Food | Location | Notes/Title

- Field Ingestion & Parsing Specifications:
  1. Date (String -> Date Object):
     - Format varies across rows: "Oct 4, 2023", "Dec 6, 23", "Oct 2, 24", "Jun 25, 2025".
     - Parser normalizes all 2-digit and 4-digit years to ISO YYYY-MM-DD.
  2. Cancellation Detection (CRITICAL):
     - If Attendees is empty, whitespace-only, or # is 0/empty, the meeting
       was CANCELLED (e.g. low turnout, no host available, group went to trivia).
     - The "Notes/Title" field provides the cancellation reason.
     - Cancelled meetings must NOT be counted toward member attendance tallies,
       but MUST be tracked in group statistics (e.g., "Held vs Cancelled").
  3. Attendees (String -> Array of Strings):
     - Comma-separated member names.
     - Handles parenthetical guests: "Avery (Lucas's Cousin)", "Mike (Joseph)",
       "Kevin (Natalie Smith)", "Dani (Dani)", "Akshaan (Julia)".
  4. Activity (String -> Array of Strings):
     - Comma-delimited list of games played that night.
  5. Cooks & Food:
     - Cooks: Comma-separated list of chefs.
     - Food: Description of dishes prepared or ordered.
  6. Location:
     - Venue address: "115 Highbourne Road", "103-70 Heath Street W", "35 Hayden Street",
       "136 Glendale", "617 Gladstone Ave", "843 Gerrard Street East", etc.

--------------------------------------------------------------------------------
3.2. Facebook Messenger Export ("message_1.json" & Media Folders)
--------------------------------------------------------------------------------
- Location:
  * Workspace root: message_1.json (67,617 lines, 5,785 total entries)
  * Media directories:
    - ./audio/  (Voice memos, e.g. 26127610053561130.mp4)
    - ./gifs/   (20 animated GIF files)
    - ./photos/ (220 JPG/PNG images)
    - ./videos/ (73 MP4 video clips)

- Media URI Resolution:
  The URI string in the JSON (e.g. `your_facebook_activity/.../photos/1534396821777786.jpg`)
  maps directly to the local folder: `./photos/1534396821777786.jpg`.

--------------------------------------------------------------------------------
3.3. The "Pure Chat" vs. "Poll Response" Distinction (MANDATORY RULE)
--------------------------------------------------------------------------------
Facebook Messenger exports include synthetic notification messages that inflate
message counts by over 120% if unfiltered!

CRITICAL FILTERING RULE FOR CHAT LEADERBOARDS:
When querying "Who messages the most?", "Chat volume", or "Top chatter awards",
the query MUST STRICTLY FILTER OUT:
1. Poll Votes:
   Regex: `r'voted for .* in the poll\.'`
   Example: 'Vesela voted for "Sun Oct 25" in the poll.'
2. Poll Creations:
   Regex: `r'created a poll:'`
   Example: 'Rory created a poll: Who is coming this week?'
3. Reaction Notifications:
   Regex: `r'reacted .* to (your|their own) message'`
   Example: 'J-Bug reacted ðŸ¥³ to your message '
4. Group Administration Events:
   Regex: `r'(named the group|changed the group|added .* to the group|left the group|removed .* from the group|started an audio call|started a video call)'`

DATA BREAKDOWN:
- Total Raw Messenger Entries: 5,785
- Automated Notifications (Polls, Reaction alerts, System): ~3,185
- Pure Conversational Messages: ~2,600

--------------------------------------------------------------------------------
3.4. Messenger Unicode / Mojibake Sanitization Guide
--------------------------------------------------------------------------------
Facebook exports encode UTF-8 bytes as Latin-1 escape sequences.
Sanitization Algorithm:
- In Python: `raw_string.encode('latin1').decode('utf-8', errors='ignore')`
- In JavaScript: `decodeURIComponent(escape(raw_string))`
Every text string from message_1.json MUST be sanitized prior to rendering.

--------------------------------------------------------------------------------
3.5. Member Alias & Nickname Resolution Dictionary
--------------------------------------------------------------------------------
The pipeline unifies all names using this canonical mapping:
  Raw Name / Nickname               Canonical Member Name
  --------------------------------  --------------------------------
  Masean Gun Kelly                  Sean Kirschner
  Sean Kirschner                    Sean Kirschner
  J-Bug                             Joseph Sanfilippo
  Joseph Sanfilippo                 Joseph Sanfilippo
  Nilf                              Nils Gritters
  Nils Gritters                     Nils Gritters
  M@ckzzz                           Max Berger
  Max Berger                        Max Berger
  Leeza Rg                          Leeza Rg
  Robbie / Robbie Grant             Robbie Grant
  Rory / Rory Grant                 Rory Grant
  Daniel / Daniel Fishbayn          Daniel Fishbayn
  Galen / Galen Voysey              Galen Voysey
  Chandler / Chandler Buchanan      Chandler Buchanan
  Andrew / Andrew Luba              Andrew Luba
  Auguste / Auguste Nahas           Auguste Nahas
  Ben / Ben Mayer-Goodman           Ben Mayer-Goodman
  Kailee / Kailee Mandel            Kailee Mandel
  Vesela / Vesela Ivanova           Vesela Ivanova
  Dani Castellanos / Daniela C.     Dani Castellanos
  Nathalie Rose                     Nathalie Rose
  Kathryn Pierce / Kathryn Nicole   Kathryn Pierce
  Julia St Louis                    Julia St Louis


================================================================================
4. UNIFIED DATABASE SCHEMAS & ENTITY RELATIONSHIP MODEL
================================================================================
The relational model consists of 7 normalized entities:

4.1. Entity: Member
     - member_id (String slug, e.g. "joseph_sanfilippo")
     - canonical_name (String)
     - aliases (Array of Strings)
     - attendance_by_year (Dict: { "Y1": int, "Y2": int, "Y3": int, "all": int })
     - cooking_by_year (Dict: { "Y1": int, "Y2": int, "Y3": int, "all": int })
     - pure_chat_by_year (Dict: { "Y1": int, "Y2": int, "Y3": int, "all": int })
     - poll_votes_by_year (Dict: { "Y1": int, "Y2": int, "Y3": int, "all": int })
     - reactions_given_by_year (Dict: { "Y1": int, "Y2": int, "Y3": int, "all": int })
     - reactions_received_by_year (Dict: { "Y1": int, "Y2": int, "Y3": int, "all": int })
     - photos_posted_by_year (Dict: { "Y1": int, "Y2": int, "Y3": int, "all": int })
     - videos_posted_by_year (Dict: { "Y1": int, "Y2": int, "Y3": int, "all": int })

4.2. Entity: Meeting
     - meeting_id (Integer, 1..N)
     - date_raw (String)
     - date_iso (String YYYY-MM-DD)
     - year_bucket ("Y1" | "Y2" | "Y3")
     - status ("COMPLETED" | "CANCELLED")
     - cancellation_reason (String or null)
     - games_played (Array of Game Refs)
     - attendees (Array of Member Refs)
     - attendee_count (Integer)
     - cooks (Array of Member Refs)
     - food_description (String)
     - location_raw (String)
     - location_normalized (String)
     - notes_lore (String)

4.3. Entity: Game
     - game_id (String slug)
     - title (String)
     - is_botc (Boolean)
     - botc_edition ("Trouble Brewing" | "Bad Moon Rising" | "Sects & Violets" | "Experimental" | null)
     - plays_by_year (Dict: { "Y1": int, "Y2": int, "Y3": int, "all": int })

4.4. Entity: ChatMessage
     - message_id (String hash)
     - sender_id (Member Ref)
     - timestamp_ms (Integer)
     - year_bucket ("Y1" | "Y2" | "Y3")
     - content_clean (String)
     - is_pure_chat (Boolean)
     - photos (Array of local paths)
     - videos (Array of local paths)
     - gifs (Array of local paths)
     - audio (Array of local paths)
     - reaction_count (Integer)
     - reactions (Array of { actor_id: Member Ref, emoji: String })

4.5. Entity: Reaction
     - reaction_id (String)
     - target_message_id (ChatMessage Ref)
     - actor_id (Member Ref)
     - recipient_id (Member Ref)
     - emoji_glyph (String, sanitized unicode)
     - timestamp_ms (Integer)
     - year_bucket ("Y1" | "Y2" | "Y3")

4.6. Entity: PollVote
     - vote_id (String)
     - voter_id (Member Ref)
     - option_text (String)
     - timestamp_ms (Integer)
     - year_bucket ("Y1" | "Y2" | "Y3")

4.7. Entity: Location
     - location_id (String slug)
     - address (String)
     - meetings_by_year (Dict: { "Y1": int, "Y2": int, "Y3": int, "all": int })
     - attendee_counts_by_year (Dict: { "Y1": [int], "Y2": [int], "Y3": [int], "all": [int] })


================================================================================
5. DATA PIPELINE & QUERY SPECIFICATION (REUSABLE ENGINE)
================================================================================
Rather than hardcoding static numbers, the project utilizes an automated data
pipeline that executes parameterized queries:

--------------------------------------------------------------------------------
5.1. Pipeline Architecture vs. One-Time Static Generation
--------------------------------------------------------------------------------
- Input: Google Sheet CSV + `message_1.json` + media directories.
- Intermediate: Normalized SQLite in-memory database or structured JS/Python Dataframe.
- Output: Standardized `bgc_data.json` containing pre-computed data structures for
  "all", "Y1", "Y2", and "Y3", enabling instantaneous client-side filter switching.

--------------------------------------------------------------------------------
5.2. Core Query Interface Definitions
--------------------------------------------------------------------------------
1. `getAttendanceComparison(yearFilter)`
   Returns: { avgAttendance, uniqueAttendees, newAttendees, meetingsHeld, cancelledCount, yoyDeltas }

2. `getTopAttendees(yearFilter, limit=3)`
   Returns: Ranked list of members with attendance count.

3. `getTopCooks(yearFilter, limit=3)`
   Returns: Ranked list of members with dinner cooking count.

4. `getTopPureChatters(yearFilter, limit=3)`
   Returns: Ranked list of members with pure conversational messages sent (polls excluded).

5. `getMostPopularPost(yearFilter, limit=3)`
   Returns: Ranked list of messages with reaction count, text snippet, attached media, and sender.

6. `getTopMediaPosters(yearFilter, mediaType="photos"|"videos", limit=3)`
   Returns: Ranked list of photographers / videographers.

7. `getBusiestLocations(yearFilter, minMeetings=2, limit=3)`
   Returns: Locations ranked by average attendee count.

8. `getBusiestWeeks(yearFilter, limit=3)`
   Returns: Individual meetings ranked by highest total attendance count.

9. `getMostPopularEmojis(yearFilter, limit=5)`
   Returns: Emojis ranked by frequency of use as reactions.


================================================================================
6. SLIDE DECK BLUEPRINT: "STATS" & "AWARDS"
================================================================================

--------------------------------------------------------------------------------
6.1. Part 1: "Stats" (Group-Level Comparison & Trends)
--------------------------------------------------------------------------------
The Stats section highlights the club's growth, consistency, and hilarious patterns.
Each card displays the Year 1, Year 2, and Year 3 comparisons along with color-coded
YoY percentage changes (+Green / -Red):

1. Average Attendance Comparison:
   - Year 1 (2023-2024): 9.87 attendees / meeting (Baseline)
   - Year 2 (2024-2025): 11.27 attendees / meeting (+14.2% [GREEN])
   - Year 3 (2025-2026): 10.96 attendees / meeting (-2.7% [RED])
   - All-Time Average:  10.70 attendees / meeting

2. Unique Attendees Comparison:
   - Year 1 (2023-2024): 46 unique attendees (Baseline)
   - Year 2 (2024-2025): 72 unique attendees (+56.5% [GREEN])
   - Year 3 (2025-2026): 61 unique attendees (-15.3% [RED])
   - All-Time Unique:   115+ different humans hosted!

3. New Attendees Recruited Comparison (First-Time Attendees):
   - Year 1 (2023-2024): 46 new members (The Genesis Cohort)
   - Year 2 (2024-2025): 41 new members (-10.9% [RED])
   - Year 3 (2025-2026): 28 new members (-31.7% [RED])

4. The Grimoire of Games (Ludography Breakdown):
   - Blood on the Clocktower Dominance:
     * Trouble Brewing: 86 sessions (The club's heartbeat)
     * Experimental BOTC: 24 sessions
     * Bad Moon Rising & Sects & Violets: 14+ sessions
     * Combined BOTC: Over 75% of all game nights!
   - Secondary Classics: Top Four (12), Hide and Seek (10), Traitor Tennis (10),
     Clubs Diamonds Hearts Spades (9), Back to Back Finals (9), Captain Sonar (6),
     Tortuga (6), Unlock (5).

5. The Feast & Fellowship (Culinary Records):
   - Over 140 home-cooked multi-course banquets!
   - Top All-Time Chefs: Rory Grant (91), Andrew Luba (51), Lucas Kirschner (32),
     Kailee Mandel (23), Joseph Sanfilippo (22).
   - Signature Dishes: Mushroom Risotto, Big Curry, Night Baker Cookies, Gourmet Soups.

6. The Sanctuaries (Venues):
   - 115 Highbourne Road: The Spiritual Home (Over 70+ meetings)
   - 103-70 Heath Street W: The West-End Citadel (50+ meetings)
   - Summer Park Sessions: Christie Pitts & Casaloma

7. The Whispers (Messenger Chatter & Cadence):
   - Conversational chat cadence vs. 2,365 poll votes
   - Peak chat activity heatmap: Wednesday 3:00 PM - 6:00 PM (pre-game frenzy)
   - Media shared: 220 photos, 73 videos, 20 GIFs, 1 voice note

--------------------------------------------------------------------------------
6.2. Part 2: "Awards" (Default: Year 3 Honors)
--------------------------------------------------------------------------------
By default, the Awards section honors the heroes of Year 3 (the culmination year),
utilizing the 4-Stage Podium Reveal for every single category:

Award 1: "The Most Popular Post" (Most Reacted to Messages in Year 3)
- #3: Rory Grant - 16 reactions ("We just sang 🎵 Happy being an autonomous psychologist...")
- #2: Rory Grant - 16 reactions ("20/20 Vision as of my 24 hour follow-up!")
- #1: Rory Grant - 22 reactions ("Jenny and I are having a debate: Is 9 months 'almost a year'?")

Award 2: "The Photographer" (Most Photos Posted to the Chat in Year 3)
- #3: Chandler Buchanan - 9 photos
- #2: Rory Grant - 11 photos
- #1: Joseph Sanfilippo - 19 photos (The Official Club Archivist)

Award 3: "The Videographer" (Most Videos Posted to the Chat in Year 3)
- #3: Daniela Castellanos - 2 videos
- #2: Joseph Sanfilippo - 2 videos
- #1: Chandler Buchanan - 6 videos (Master of Motion)

Award 4: "The Busiest Location" (Highest Average Attendance in Year 3)
- #3: 843 Gerrard Street East - Avg 10.50 attendees (6 meetings)
- #2: 617 Gladstone Ave - Avg 11.50 attendees (4 meetings)
- #1: 115 Highbourne Road - Avg 11.54 attendees across 24 meetings!

Award 5: "The Busiest Week" (Highest Single-Session Turnout in Year 3)
- #3: Dec 17, 2025 & Mar 18, 2026 - 16 attendees
- #2: (Tie for 2nd) - 16 attendees
- #1: March 25, 2026 - 18 attendees! (BOTC Trouble Brewing, Experimental, Knives Out)

Award 6: "The Most Popular Emoji" (Reaction Glyphs in Year 3)
- #5: 🥳 Party Face - 18 uses
- #4: 😮 Wow Face - 56 uses
- #3: 👍 Thumbs Up - 67 uses
- #2: 😆 Laughing Face - 161 uses
- #1: ❤️ Red Heart - 1,116 uses! (Displayed as giant glowing heart glyph)

Award 7: "The Grimoire Titan" (Top In-Person Attendance in Year 3)
- #3: Mara Waters - 37 meetings
- #2: Lucas Kirschner & Kathryn Pierce (TIE) - 41 meetings
- #1: Joseph Sanfilippo - 46 meetings! (94% Year 3 attendance)

Award 8: "The Iron Chef" (Most Times Cooking Dinner in Year 3)
- #3: Mara Waters & Galen Voysey (TIE) - 9 dinners
- #2: Kailee Mandel - 10 dinners
- #1: Rory Grant - 25 dinners! (Master Chef of Year 3)

Award 9: "The Town Crier" (Most Pure Chat Messages Sent in Year 3 - Polls Excluded)
- #3: Leeza Rg - 121 pure messages
- #2: Rory Grant - 129 pure messages
- #1: Joseph Sanfilippo - 163 pure messages (The Chatbox Sovereign)

Award 10: "The Hype Beast" (Most Reactions Given in Year 3)
- #3: Galen Voysey
- #2: Lucas Kirschner
- #1: Andrew Luba (The Constant Reaction Machine)

--------------------------------------------------------------------------------
6.3. The 4-Stage Podium Reveal Specification (CRITICAL REQUIREMENT)
--------------------------------------------------------------------------------
Every single award slide must NEVER show all winners immediately.
It operates as a strict 4-stage progressive reveal state machine:

  [ STATE 0: EMPTY PODIUM ]
  - Suspenseful ambiance, category title, and empty 3-tier gothic podium.
  - Pedestals #3, #2, and #1 are shadowed in candlelight.
        |
        v (User advances / Spacebar)
  [ STATE 1: BRONZE REVEAL (#3 ONLY) ]
  - Bronze pedestal illuminates with antique bronze flame.
  - #3 Winner slides in: Name, Stat, Avatar/Photo, Bronze Medal.
  - Pedestals #2 and #1 remain veiled.
        |
        v (User advances / Spacebar)
  [ STATE 2: SILVER REVEAL (#3 AND #2) ]
  - #3 Winner remains visible on the bronze pedestal.
  - Silver pedestal illuminates with polished mithril glow.
  - #2 Winner slides in: Name, Stat, Avatar/Photo, Silver Medal.
  - #1 Champion remains hidden in suspense.
        |
        v (User advances / Spacebar)
  [ STATE 3: COMPLETE PODIUM (#3, #2, AND #1 CHAMPION!) ]
  - #3 and #2 winners remain proudly displayed.
  - Center elevated Gold pedestal ignites with royal golden flame!
  - #1 Champion bursts onto the screen with Golden Laurel, Stat, Avatar.
  - Fanfare particle burst / gold & purple confetti explosion!


================================================================================
7. BLOOD ON THE CLOCKTOWER (BOTC) DETAILED STYLE GUIDE
================================================================================

--------------------------------------------------------------------------------
7.1. Visual Philosophy & Grimoire Atmosphere
--------------------------------------------------------------------------------
- Gothic Grimoire Meets Tabletop Festivity:
  Dark mystery, candlelight, antique woodblock linocut inking, and high-contrast
  craftsmanship combined with celebratory jewel tones, witty group humor, and
  vibrant data charts.
- No corporate flat design! Every container resembles an artifact from the
  Storyteller's Grimoire: deckled parchment paper, gold foil filigree, wax seals,
  and concentric occult medallions.

--------------------------------------------------------------------------------
7.2. Master Color Palette
--------------------------------------------------------------------------------
A. Universal Base Color (MANDATORY & CONSISTENT THROUGHOUT ENTIRE PROJECT):
   Deep Gothic Purple
   - Canvas Deep Background:   #12041D  (The Midnight Void)
   - Grimoire Velvet Surface:  #1F082F  (Rich Imperial Violet)
   - Card / Container Base:    #2C0D42  (Elevated Velvet Purple)
   - Border / Filigree Muted:  #4A1D6D  (Purple Shadow Trim)
   - Glowing Violet Accent:    #9D4EDD  (Arcane Orchid Glow)

B. Section-Specific Accent Colors (Jewel Tones):
   Each section is anchored by the deep purple canvas AND enhanced by a distinct
   edition-inspired jewel accent:

   1. Attendance & Trouble Brewing Theme:
      Accent: Blood Velvet Crimson (#8B0000 / #B91C1C / #EF4444)
      Secondary: Bone Ash Parchment (#F5EBE0)

   2. Cooking & Bad Moon Rising Theme:
      Accent: Alchemical Amber & Ochre Gold (#C5832B / #E59819 / #FBBF24)
      Secondary: Warm Sourdough Cream (#FFFBEB)

   3. Chat & Sects & Violets Theme:
      Accent: Radiant Amethyst / Toxic Lavender (#7E22CE / #A855F7 / #D8B4FE)
      Secondary: Electric Cyan Highlight (#06B6D4)

   4. Venues & Night Phase Theme:
      Accent: Midnight Cobalt / Indigo (#1E3A8A / #3B82F6 / #60A5FA)
      Secondary: Moonlit Slate (#94A3B8)

   5. Year-over-Year Delta Metrics:
      - Positive YoY: Emerald Green (#10B981 / #34D399)
      - Negative YoY: Crimson Red (#EF4444 / #F87171)

   6. Awards Podium Metallics:
      - 1st Place (Gold):   #F59E0B / #FCD34D / #78350F (Imperial Gold)
      - 2nd Place (Silver): #94A3B8 / #E2E8F0 / #334155 (Mithril Silver)
      - 3rd Place (Bronze): #B45309 / #D97706 / #451A03 (Antique Bronze)

--------------------------------------------------------------------------------
7.3. Textures, Borders, Filigree, and Graphic Elements
--------------------------------------------------------------------------------
- Grimoire Borders (styleReferences/page_1, page_47):
  Double-line brass borders with filigree corners and fleur-de-lis accents.
- Concentric Occult Medallions (styleReferences/page_19, page_23, page_47):
  Circular geometric seals and astrological rings as ambient card watermarks.
- Woodblock Linocut Ink Style (styleReferences/page_13, page_22):
  High-contrast two-tone lithographs (aged bone on deep violet).
- Aged Parchment Texture (styleReferences/page_4, page_28):
  Subtle radial vignette shading simulating torchlight on leather.

--------------------------------------------------------------------------------
7.4. Typography Hierarchy
--------------------------------------------------------------------------------
- Titles & Headers:
  'Cinzel Decorative', 'MedievalSharp', or 'Pirata One'
  Color: Burnished Antique Gold (#F3CE72) with deep text-shadows.
- Subheadings & Category Labels:
  'Cinzel', 'IM Fell English', or 'Crimson Pro'
  Color: Section jewel accent (Crimson, Amber, Lavender, or Gold).
- Body Text, Data Values & Tabular Numerals:
  'Spectral', 'Cinzel', or clean sans-serif 'Plus Jakarta Sans' / 'Inter'
  Color: Ivory / Off-White (#E2D9F3) with crystal-clear legibility.

--------------------------------------------------------------------------------
7.5. Motion, Lighting Effects, and Particle Fanfare
--------------------------------------------------------------------------------
- Candlelight flicker animations (`box-shadow: 0 0 25px rgba(...)`).
- Spring cubic-bezier transitions for pedestal reveals.
- Particle burst confetti (canvas-confetti) when #1 Champion is crowned.


================================================================================
8. TECHNICAL IMPLEMENTATION & CODE ARCHITECTURE GUIDELINES
================================================================================

--------------------------------------------------------------------------------
8.1. Single-File vs. Modular HTML Presentation Engine
--------------------------------------------------------------------------------
- Recommended Production Format:
  A single, standalone, offline-ready `index.html` file containing:
  1. Embedded CSS (Design system, BOTC styles, typography, animations).
  2. Embedded Clean JSON Dataset (Pre-sanitized data for All-Time, Y1, Y2, Y3).
  3. Presentation Engine JavaScript (Slide controller, horizon filter, keyboard
     shortcuts, 4-stage podium state machine, and interactive charts).
- Advantage: Zero server or CORS issues; can be opened immediately in any browser
  via `open index.html`.

--------------------------------------------------------------------------------
8.2. Slide & Sub-Step State Machine
--------------------------------------------------------------------------------
- Navigation Controller manages:
  * `currentSlideIndex` (0 to N-1)
  * `currentStepIndex` (0 to 3 for Award slides; 0 for standard Stats slides)
  * `currentHorizon` ("y3" by default for awards; toggleable to "all", "y1", "y2")
- Keybindings:
  * ArrowRight / Spacebar: Advances step (0 -> 1 -> 2 -> 3) or advances slide.
  * ArrowLeft: Steps backward or returns to previous slide.
  * Key 'F': Toggle Fullscreen.
  * Key 'T': Toggle Table of Contents / Slide Drawer.
  * Keys '1', '2', '3', '0': Quick switch between Y1, Y2, Y3, and All-Time horizons.

--------------------------------------------------------------------------------
8.3. Local Media Asset Resolution
--------------------------------------------------------------------------------
- Images, photos, and GIFs render via relative paths:
  `photos/<filename>.jpg`, `gifs/<filename>.gif`.
- When winner avatars are shown on the podium, link to their real photo from
  the chat archives or fall back to an elegant BOTC grimoire character portrait.

--------------------------------------------------------------------------------
8.4. Build & Ingestion Pipeline Workflow
--------------------------------------------------------------------------------
A lightweight Python build script (e.g. `build_data.py`) prepares the data:
1. Ingests Google Sheet CSV + `message_1.json`.
2. Applies Latin-1 -> UTF-8 decoding.
3. Filters out poll responses, poll creations, and reaction alerts from chat tallies.
4. Partitions metrics into Y1, Y2, Y3, and All-Time.
5. Computes YoY percentage deltas for stats.
6. Computes top 3 rankings for all award categories.
7. Emits or injects the sanitized JSON into `index.html`.


================================================================================
9. RULES OF ENGAGEMENT FOR ALL FUTURE AI PROMPTS
================================================================================
When generating code, slides, or visualizations in future prompts, the AI MUST
strictly adhere to these 8 rules:

RULE 1: STRICT PURITY OF CHAT COUNTS
- Never include poll voting text or reaction alerts in chat message tallies.
- Conversational chat awards must reflect pure text banter.

RULE 2: THE DEEP PURPLE CANVAS IS IMMUTABLE
- The universal background must always remain the deep gothic purple (#12041D
  to #2C0D42). Never revert to white or generic gray.

RULE 3: MANDATORY 4-STAGE REVEALS FOR EVERY AWARD
- Never display all 3 podium winners simultaneously upon slide entry.
- Every award must progress strictly: State 0 -> State 1 -> State 2 -> State 3.

RULE 4: YEAR 3 AWARDS DEFAULT WITH DYNAMIC HORIZON FILTERING
- Awards default to Year 3 stats, but the UI and data structures must allow
  switching to Year 1, Year 2, or All-Time.

RULE 5: COLOR-CODED YOY DELTAS
- All comparative stats must display percentage changes formatted as:
  +X.X% in Emerald Green (#10B981) or -X.X% in Crimson Red (#EF4444).

RULE 6: UNICODE MOJIBAKE SANITIZATION
- Clean all Facebook escape sequences so that emojis (❤️, 🥳, 😂) and
  special characters display natively without question marks or corruption.

RULE 7: ZERO DATA HALLUCINATION
- All attendance, cooking, voting, and chat numbers must come from the actual
  dataset queries.

RULE 8: RESPONSIVE 16:9 PRESENTATION GEOMETRY
- Slides must scale cleanly to 16:9 aspect ratio for laptop, monitor, and
  projector presentation.

================================================================================
END OF SPECIFICATION FILE (ReadMe.txt v1.1.0)
================================================================================
