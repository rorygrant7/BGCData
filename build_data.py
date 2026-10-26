#!/usr/bin/env python3
"""
Board Game Club (BGC) Data Aggregation & Query Pipeline
Ingests:
  1. Google Sheet CSV (Live export)
  2. message_1.json (Facebook Messenger chat archive)
Outputs:
  bgc_data.js (window.BGC_DATA = { ... })
"""

import urllib.request
import csv
import io
import json
import re
import os
from datetime import datetime
from collections import Counter, defaultdict

# ------------------------------------------------------------------------------
# 1. CONFIGURATION & TIME BOUNDARIES
# ------------------------------------------------------------------------------
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRVYFs2AgGNfSwItq0R1fkB4yK9kF-Bn-AbphiZeCVgZw0V57Q0sSyGp9OMMr26j0PpSKdZf5NIFAES/pub?gid=0&single=true&output=csv"
JSON_FILE = "message_1.json"
OUTPUT_JS = "bgc_data.js"

Y1_START = datetime(2023, 10, 4)
Y2_START = datetime(2024, 10, 4)
Y3_START = datetime(2025, 10, 4)
Y3_END   = datetime(2026, 10, 5) # inclusive of Oct 4, 2026

# Milliseconds for JSON timestamp comparisons
Y1_START_MS = int(Y1_START.timestamp() * 1000)
Y2_START_MS = int(Y2_START.timestamp() * 1000)
Y3_START_MS = int(Y3_START.timestamp() * 1000)
Y3_END_MS   = int(Y3_END.timestamp() * 1000)

# Canonical Member Name Mapping
ALIAS_MAP = {
    "Masean Gun Kelly": "Sean Kirschner",
    "J-Bug": "Joseph Sanfilippo",
    "Nilf": "Nils Gritters",
    "M@ckzzz": "Max Berger",
    "Leeza Rg": "Leeza Rg",
    "Robbie": "Robbie Grant",
    "Rory": "Rory Grant",
    "Daniel": "Daniel Fishbayn",
    "Galen": "Galen Voysey",
    "Chandler": "Chandler Buchanan",
    "Andrew": "Andrew Luba",
    "Auguste": "Auguste Nahas",
    "Ben": "Ben Mayer-Goodman",
    "Kailee": "Kailee Mandel",
    "Vesela": "Vesela Ivanova",
    "Dani Castellanos": "Dani Castellanos",
    "Daniela Castellanos": "Dani Castellanos",
    "Kathryn Nicole": "Kathryn Pierce",
    "Kathryn Pierce": "Kathryn Pierce"
}

def canonicalize_name(raw_name):
    if not raw_name:
        return "Unknown"
    cleaned = raw_name.strip()
    return ALIAS_MAP.get(cleaned, cleaned)

def decode_mojibake(text):
    if not text:
        return ""
    try:
        return text.encode("latin1").decode("utf-8")
    except Exception:
        return text

def parse_date(d_str):
    if not d_str:
        return None
    cleaned = d_str.strip()
    for fmt in ["%b %d, %Y", "%b %d, %y", "%B %d, %Y", "%B %d, %y"]:
        try:
            return datetime.strptime(cleaned, fmt)
        except ValueError:
            pass
    return None

def get_year_bucket(dt):
    if not dt:
        return "all"
    if Y1_START <= dt < Y2_START:
        return "y1"
    elif Y2_START <= dt < Y3_START:
        return "y2"
    elif Y3_START <= dt <= Y3_END:
        return "y3"
    elif dt > Y3_END:
        return "y3" # include ongoing meetings in current cycle
    return "all"

def get_ms_year_bucket(ts_ms):
    if Y1_START_MS <= ts_ms < Y2_START_MS:
        return "y1"
    elif Y2_START_MS <= ts_ms < Y3_START_MS:
        return "y2"
    elif Y3_START_MS <= ts_ms <= Y3_END_MS:
        return "y3"
    elif ts_ms > Y3_END_MS:
        return "y3"
    return "y1" if ts_ms < Y1_START_MS else "all"

# ------------------------------------------------------------------------------
# 2. INGEST GOOGLE SHEET DATA
# ------------------------------------------------------------------------------
print("Fetching Google Sheet CSV...")
csv_text = urllib.request.urlopen(SHEET_URL).read().decode("utf-8")
reader = list(csv.DictReader(io.StringIO(csv_text)))

all_meetings = []
first_seen_member = {}

for idx, row in enumerate(reader):
    d_raw = row.get("Date", "").strip()
    dt = parse_date(d_raw)
    if not dt:
        continue
    
    y_bucket = get_year_bucket(dt)
    activity_raw = row.get("Activity", "").strip()
    attendees_raw = row.get("Attendees", "").strip()
    cooks_raw = row.get("Cooks", "").strip()
    food_raw = row.get("Food", "").strip()
    location_raw = row.get("Location", "").strip()
    notes_raw = row.get("Notes/Title", "").strip()
    count_raw = row.get("#", "").strip()
    
    is_cancelled = False
    if not attendees_raw or count_raw in ["0", ""]:
        is_cancelled = True
        
    attendees = []
    if not is_cancelled and attendees_raw:
        for a in attendees_raw.split(","):
            c_name = canonicalize_name(a)
            if c_name:
                attendees.append(c_name)
                if c_name not in first_seen_member:
                    first_seen_member[c_name] = dt
                    
    cooks = []
    if cooks_raw:
        for c in cooks_raw.split(","):
            c_name = canonicalize_name(c)
            if c_name:
                cooks.append(c_name)
                
    games = []
    if activity_raw:
        for g in activity_raw.split(","):
            g_clean = g.strip()
            if g_clean:
                games.append(g_clean)
                
    count = int(count_raw) if count_raw.isdigit() else len(attendees)
    
    meeting_obj = {
        "id": idx + 1,
        "date_raw": d_raw,
        "date_iso": dt.strftime("%Y-%m-%d"),
        "timestamp_ms": int(dt.timestamp() * 1000),
        "year": y_bucket,
        "is_cancelled": is_cancelled,
        "cancellation_reason": notes_raw if is_cancelled else "",
        "games": games,
        "attendees": attendees,
        "count": count,
        "cooks": cooks,
        "food": food_raw,
        "location": location_raw,
        "notes": notes_raw
    }
    all_meetings.append(meeting_obj)

print(f"Parsed {len(all_meetings)} meetings from Google Sheets.")

# ------------------------------------------------------------------------------
# 3. INGEST FACEBOOK MESSENGER DATA
# ------------------------------------------------------------------------------
print("Loading message_1.json...")
with open(JSON_FILE, "r", encoding="utf-8") as f:
    raw_messenger = json.load(f)

messages_raw = raw_messenger.get("messages", [])

POLL_RE = re.compile(r"(voted for .* in the poll|created a poll:)", re.IGNORECASE)
REACTION_ALERT_RE = re.compile(r"reacted .* to (your|their own) message", re.IGNORECASE)
SYS_EVENT_RE = re.compile(r"(named the group|changed the group|added .* to the group|left the group|removed .* from the group|started an audio call|started a video call)", re.IGNORECASE)

clean_messages = []
for m in messages_raw:
    sender = canonicalize_name(m.get("sender_name", "Unknown"))
    ts_ms = m.get("timestamp_ms", 0)
    y_bucket = get_ms_year_bucket(ts_ms)
    content_raw = m.get("content", "")
    content_clean = decode_mojibake(content_raw)
    
    is_poll = bool(POLL_RE.search(content_clean))
    is_reaction_alert = bool(REACTION_ALERT_RE.search(content_clean))
    is_sys = bool(SYS_EVENT_RE.search(content_clean))
    
    # Pure chat is genuine conversational banter
    is_pure_chat = (not is_poll) and (not is_reaction_alert) and (not is_sys)
    
    # Media attachments
    photos = [p.get("uri", "").split("/")[-1] for p in m.get("photos", []) if p.get("uri")]
    videos = [v.get("uri", "").split("/")[-1] for v in m.get("videos", []) if v.get("uri")]
    gifs = [g.get("uri", "").split("/")[-1] for g in m.get("gifs", []) if g.get("uri")]
    audio = [a.get("uri", "").split("/")[-1] for a in m.get("audio_files", []) if a.get("uri")]
    
    # Reactions
    reactions_clean = []
    for r in m.get("reactions", []):
        actor = canonicalize_name(r.get("actor", "Unknown"))
        emoji = decode_mojibake(r.get("reaction", ""))
        reactions_clean.append({"actor": actor, "emoji": emoji})
        
    msg_obj = {
        "sender": sender,
        "timestamp_ms": ts_ms,
        "year": y_bucket,
        "content": content_clean,
        "is_pure_chat": is_pure_chat,
        "is_poll": is_poll,
        "photos": photos,
        "videos": videos,
        "gifs": gifs,
        "audio": audio,
        "reactions": reactions_clean,
        "reaction_count": len(reactions_clean)
    }
    clean_messages.append(msg_obj)

print(f"Parsed {len(clean_messages)} messenger objects.")

# ------------------------------------------------------------------------------
# 4. QUERY ENGINE: AGGREGATE PER YEAR (Y1, Y2, Y3, ALL)
# ------------------------------------------------------------------------------
def compute_period_stats(meetings, messages, period_key):
    # Filter meetings
    p_meetings = [m for m in meetings if (period_key == "all" or m["year"] == period_key)]
    held_meetings = [m for m in p_meetings if not m["is_cancelled"]]
    cancelled_meetings = [m for m in p_meetings if m["is_cancelled"]]
    
    # Filter messages
    p_messages = [m for m in messages if (period_key == "all" or m["year"] == period_key)]
    pure_chat_messages = [m for m in p_messages if m["is_pure_chat"]]
    
    # Attendance
    attendee_counts = [m["count"] for m in held_meetings]
    avg_attendance = round(sum(attendee_counts) / len(attendee_counts), 2) if attendee_counts else 0.0
    
    unique_attendees = set()
    new_attendees = set()
    attendee_freq = Counter()
    cook_freq = Counter()
    game_freq = Counter()
    loc_stats = defaultdict(list)
    busiest_weeks = []
    
    for m in held_meetings:
        count = m["count"]
        busiest_weeks.append({
            "date": m["date_raw"],
            "count": count,
            "location": m["location"],
            "games": ", ".join(m["games"][:3])
        })
        for a in m["attendees"]:
            unique_attendees.add(a)
            attendee_freq[a] += 1
            if period_key == "all":
                new_attendees.add(a)
            elif period_key == "y1" and first_seen_member.get(a) and first_seen_member[a] < Y2_START:
                new_attendees.add(a)
            elif period_key == "y2" and first_seen_member.get(a) and Y2_START <= first_seen_member[a] < Y3_START:
                new_attendees.add(a)
            elif period_key == "y3" and first_seen_member.get(a) and first_seen_member[a] >= Y3_START:
                new_attendees.add(a)
                
        for c in m["cooks"]:
            cook_freq[c] += 1
            
        for g in m["games"]:
            game_freq[g] += 1
            
        if m["location"]:
            loc_stats[m["location"]].append(count)

    busiest_weeks.sort(key=lambda x: x["count"], reverse=True)
    
    # Location ranking
    location_rankings = []
    for loc, counts in loc_stats.items():
        avg_c = round(sum(counts) / len(counts), 2)
        location_rankings.append({
            "location": loc,
            "avg_attendance": avg_c,
            "total_meetings": len(counts),
            "total_attendees": sum(counts)
        })
    location_rankings.sort(key=lambda x: (x["avg_attendance"], x["total_meetings"]), reverse=True)
    
    # Games classification
    botc_games = Counter()
    non_botc_games = Counter()
    for g, cnt in game_freq.items():
        if "botc" in g.lower() or "trouble brewing" in g.lower() or "bad moon" in g.lower() or "sects" in g.lower() or "experimental" in g.lower():
            botc_games[g] += cnt
        else:
            non_botc_games[g] += cnt
            
    # Chat analytics
    pure_chat_senders = Counter()
    poll_voters = Counter()
    reactions_given = Counter()
    reactions_received = Counter()
    photo_posters = Counter()
    video_posters = Counter()
    emoji_counts = Counter()
    
    for m in p_messages:
        sender = m["sender"]
        if m["is_pure_chat"]:
            pure_chat_senders[sender] += 1
        if m["is_poll"]:
            poll_voters[sender] += 1
        if m["photos"]:
            photo_posters[sender] += len(m["photos"])
        if m["videos"]:
            video_posters[sender] += len(m["videos"])
            
        for r in m["reactions"]:
            actor = r["actor"]
            emoji = r["emoji"]
            reactions_given[actor] += 1
            reactions_received[sender] += 1
            if emoji:
                emoji_counts[emoji] += 1
                
    # Most popular posts (most reacted messages)
    reacted_posts = []
    for m in p_messages:
        if m["reaction_count"] > 0:
            preview = m["content"]
            if len(preview) > 90:
                preview = preview[:87] + "..."
            reacted_posts.append({
                "sender": m["sender"],
                "content": preview,
                "full_content": m["content"],
                "reaction_count": m["reaction_count"],
                "photos": m["photos"],
                "videos": m["videos"],
                "timestamp_ms": m["timestamp_ms"],
                "date_str": datetime.fromtimestamp(m["timestamp_ms"]/1000).strftime("%b %d, %Y")
            })
    reacted_posts.sort(key=lambda x: x["reaction_count"], reverse=True)
    
    return {
        "period": period_key,
        "meetings_held": len(held_meetings),
        "meetings_cancelled": len(cancelled_meetings),
        "cancelled_details": [m["cancellation_reason"] for m in cancelled_meetings if m["cancellation_reason"]],
        "avg_attendance": avg_attendance,
        "unique_attendees_count": len(unique_attendees),
        "new_attendees_count": len(new_attendees),
        "top_attendees": [{"name": k, "count": v} for k, v in attendee_freq.most_common(10)],
        "top_cooks": [{"name": k, "count": v} for k, v in cook_freq.most_common(10)],
        "busiest_weeks": busiest_weeks[:5],
        "busiest_locations": location_rankings[:6],
        "top_games": [{"game": k, "count": v} for k, v in game_freq.most_common(12)],
        "botc_breakdown": [{"edition": k, "count": v} for k, v in botc_games.most_common()],
        "non_botc_breakdown": [{"game": k, "count": v} for k, v in non_botc_games.most_common(8)],
        "pure_chat_count": len(pure_chat_messages),
        "top_pure_chatters": [{"name": k, "count": v} for k, v in pure_chat_senders.most_common(10)],
        "top_poll_voters": [{"name": k, "count": v} for k, v in poll_voters.most_common(5)],
        "top_reactions_given": [{"name": k, "count": v} for k, v in reactions_given.most_common(10)],
        "top_reactions_received": [{"name": k, "count": v} for k, v in reactions_received.most_common(10)],
        "top_photographers": [{"name": k, "count": v} for k, v in photo_posters.most_common(6)],
        "top_videographers": [{"name": k, "count": v} for k, v in video_posters.most_common(6)],
        "top_emojis": [{"emoji": k, "count": v} for k, v in emoji_counts.most_common(8)],
        "most_popular_posts": reacted_posts[:6]
    }

periods = ["all", "y1", "y2", "y3"]
aggregated_data = {}

for p in periods:
    print(f"Aggregating data for period: {p}...")
    aggregated_data[p] = compute_period_stats(all_meetings, clean_messages, p)

# ------------------------------------------------------------------------------
# 5. COMPUTE YEAR-OVER-YEAR (YoY) DELTAS
# ------------------------------------------------------------------------------
def calc_pct(current, previous):
    if not previous or previous == 0:
        return {"val": "Baseline", "num": 0.0, "is_pos": None}
    delta = ((current - previous) / previous) * 100
    is_pos = delta >= 0
    sign = "+" if is_pos else ""
    return {
        "val": f"{sign}{delta:.1f}%",
        "num": round(delta, 1),
        "is_pos": is_pos
    }

yoy_data = {
    "y1": {
        "avg_attendance_delta": {"val": "Baseline", "num": 0.0, "is_pos": None},
        "unique_attendees_delta": {"val": "Baseline", "num": 0.0, "is_pos": None},
        "new_attendees_delta": {"val": "Baseline", "num": 0.0, "is_pos": None}
    },
    "y2": {
        "avg_attendance_delta": calc_pct(aggregated_data["y2"]["avg_attendance"], aggregated_data["y1"]["avg_attendance"]),
        "unique_attendees_delta": calc_pct(aggregated_data["y2"]["unique_attendees_count"], aggregated_data["y1"]["unique_attendees_count"]),
        "new_attendees_delta": calc_pct(aggregated_data["y2"]["new_attendees_count"], aggregated_data["y1"]["new_attendees_count"])
    },
    "y3": {
        "avg_attendance_delta": calc_pct(aggregated_data["y3"]["avg_attendance"], aggregated_data["y2"]["avg_attendance"]),
        "unique_attendees_delta": calc_pct(aggregated_data["y3"]["unique_attendees_count"], aggregated_data["y2"]["unique_attendees_count"]),
        "new_attendees_delta": calc_pct(aggregated_data["y3"]["new_attendees_count"], aggregated_data["y2"]["new_attendees_count"])
    }
}

final_output = {
    "metadata": {
        "generated_at": datetime.now().isoformat(),
        "total_meetings_tracked": len(all_meetings),
        "total_messages_tracked": len(clean_messages),
        "base_color": "#12041D",
        "theme": "Blood on the Clocktower Gothic Grimoire"
    },
    "periods": aggregated_data,
    "yoy": yoy_data,
    "meetings_chronology": all_meetings[:15] # sample snippet for timeline
}

# Write to bgc_data.js
js_content = f"window.BGC_DATA = {json.dumps(final_output, indent=2)};\n"
with open(OUTPUT_JS, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Successfully generated {OUTPUT_JS} ({os.path.getsize(OUTPUT_JS)} bytes).")
