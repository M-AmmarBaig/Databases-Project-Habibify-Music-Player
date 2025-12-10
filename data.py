"""
Sample data for testing admin functions in the Music App
This file contains all the test data for users, songs, reports, and subscriptions
"""

from datetime import datetime, timedelta

# Users Dictionary
# Format: username:  [fullname, password, email, profile_pic_path, usertype, subscription, revenue, date_joined]
Users = {
    "Ammar": ["Muhammad Ammar Baig", "ammarbaig123", "ammar@gmail.com", 
              r"Profile Pictures\Ammar.jpeg", "Admin", "Premium", 0, "2024-01-15"],
    
    "Sarosh": ["Sarosh Mehdi Yousuf", "saroshmehdi123", "sarosh@gmail.com", 
               r"Profile Pictures\Charlie.jpeg", "Admin", "Premium", 0, "2024-01-20"],
    
    "Charlie": ["Sir Christopher Nolan", "christopher123", "christopher@gmail.com", 
                r"Profile Pictures\Christopher.jpeg", "Listener", "Premium", 15.99, "2024-03-10"],
    
    "Ezekiel": ["Ezekiel Woods", "ezekiel123", "ezekiel@gmail.com", 
                r"Profile Pictures\Ezekiel.jpeg", "Listener", "Free", 0, "2024-05-22"],
    
    "Samantha": ["Samantha Williams", "samantha123", "samantha@gmail.com", 
                 r"Profile Pictures\Samantha.jpeg", "Artist", "Artist Pro", 49.99, "2024-02-14"],
    
    "Shawn": ["Shawn Mendes", "shawn123", "shawn@gmail.com", 
              r"Profile Pictures\Shawn.jpeg", "Artist", "Artist Basic", 29.99, "2024-04-01"],
    
    "Taylor": ["Taylor Swift", "taylor123", "taylor@gmail.com", 
               r"Profile Pictures\default. jpg", "Listener", "Premium", 15.99, "2024-06-15"],
    
    "Drake": ["Drake Graham", "drake123", "drake@gmail.com", 
              r"Profile Pictures\default.jpg", "Listener", "Free", 0, "2024-07-20"],
    
    "Adele": ["Adele Adkins", "adele123", "adele@gmail. com", 
              r"Profile Pictures\default.jpg", "Artist", "Artist Pro", 49.99, "2024-03-25"]
}

# Pending Artist Requests
# Format: username: [fullname, email, subscription, date_joined, request_date]
PendingArtistRequests = {
    "JohnDoe": ["John Doe", "john@gmail.com", "Free", "2024-08-01", "2024-10-15"],
    "JaneSmith": ["Jane Smith", "jane@gmail.com", "Premium", "2024-07-10", "2024-10-20"],
    "MikeJohnson": ["Mike Johnson", "mike@gmail.com", "Free", "2024-09-05", "2024-11-01"],
    "EmilyDavis": ["Emily Davis", "emily@gmail.com", "Premium", "2024-06-20", "2024-10-25"]
}

# Pending Songs for Approval
# Format: song_id: [song_name, artist_name, genre, submission_date, file_path, image_path]
PendingSongs = {
    "PS001": ["Summer Vibes", "Samantha", "Pop", "2024-11-01", 
              r"Songs\summer_vibes.mp3", r"Song_images\summer. jpg"],
    
    "PS002": ["Midnight Blues", "Shawn", "Blues", "2024-11-03", 
              r"Songs\midnight_blues.mp3", r"Song_images\blues.jpg"],
    
    "PS003": ["Dance Revolution", "Adele", "Electronic", "2024-11-05", 
              r"Songs\dance_rev.mp3", r"Song_images\dance.jpg"],
    
    "PS004": ["Acoustic Dreams", "Samantha", "Acoustic", "2024-11-07", 
              r"Songs\acoustic. mp3", r"Song_images\acoustic.jpg"],
    
    "PS005": ["Rock Anthem", "Shawn", "Rock", "2024-11-08", 
              r"Songs\rock_anthem.mp3", r"Song_images\rock.jpg"]
}

# Reported Songs
# Format: report_id: [song_id, song_name, artist_name, reported_by, reason, genre, likes, dislikes, total_reports, upload_date]
ReportedSongs = {
    "R001": ["S101", "Controversial Track", "Unknown Artist", "Charlie", 
             "Inappropriate Content", "Hip-Hop", 150, 450, 23, "2024-09-15"],
    
    "R002": ["S102", "Loud Noise", "Samantha", "Ezekiel", 
             "Audio Quality Issues", "Electronic", 50, 200, 15, "2024-10-01"],
    
    "R003": ["S103", "Offensive Lyrics", "Random Artist", "Taylor", 
             "Hate Speech", "Rap", 20, 500, 45, "2024-08-20"],
    
    "R004": ["S104", "Copyright Issue", "Shawn", "Drake", 
             "Copyright Violation", "Pop", 300, 100, 8, "2024-10-10"],
    
    "R005": ["S105", "Disturbing Content", "Unknown", "Charlie", 
             "Violence", "Metal", 80, 350, 30, "2024-09-25"]
}

# Subscription Plans
# Format: plan_id: [plan_name, price, duration, features]
SubscriptionPlans = {
    "SP001": ["Free", 0.00, "Unlimited", "Basic streaming, Ads included"],
    "SP002": ["Premium", 15.99, "Monthly", "Ad-free, High quality audio, Offline downloads"],
}

Genres = {
    "GN001": ["Hip Hop", "Funky 90s music"],
    "GN002": ["Pop", "Catchy and mainstream tunes"],
    "GN003": ["Acoustic", "Soft unplugged melodies and vocals"],
    "GN004": ["Blues", "Soulful rhythm with emotional depth"],
    "GN005":  ["Electronic", "Synth-driven modern beats and EDM vibes"],
    "GN006": ["Rock", "Energetic guitars and powerful vocals"]
}

# Revenue Data (for analytics)
# Format: date:  revenue_amount
RevenueData = {
    "2024-01-01": 1250.50,
    "2024-02-01": 1580.75,
    "2024-03-01": 1890.25,
    "2024-04-01": 2100.00,
    "2024-05-01": 2350.80,
    "2024-06-01": 2580.90,
    "2024-07-01": 2890.50,
    "2024-08-01": 3120.75,
    "2024-09-01": 3450.25,
    "2024-10-01": 3780.00,
    "2024-11-01": 4050.50,
    "2024-12-01": 4320.25
}

# Song Plays Data (for analytics)
# Format: date: total_plays
PlaysData = {
    "2024-01-01": 15000,
    "2024-02-01": 18500,
    "2024-03-01": 22000,
    "2024-04-01": 25600,
    "2024-05-01": 28900,
    "2024-06-01": 32500,
    "2024-07-01": 36800,
    "2024-08-01": 41200,
    "2024-09-01": 45600,
    "2024-10-01": 50200,
    "2024-11-01": 55800,
    "2024-12-01": 61000
}

# Approved Songs (songs that have been accepted)
# Format: song_id: [song_name, artist_name, genre, upload_date, likes, dislikes, file_path]
ApprovedSongs = {
    "S001": ["Perfect Symphony", "Samantha", "Classical", "2024-08-15", 450, 20, r"songs\perfect_symphony.mp3"],
    "S002": ["Electric Heart", "Shawn", "EDM", "2024-09-01", 850, 35, r"songs\electric_heart.mp3"],
    "S003": ["Country Road", "Adele", "Country", "2024-07-20", 320, 15, r"songs\country_road.mp3"],
    "S004": ["Jazz Night", "Samantha", "Jazz", "2024-10-05", 520, 28, r"songs\jazz_night.mp3"],
    "S005": ["Pop Dreams", "Shawn", "Pop", "2024-09-15", 1200, 45, r"songs\pop_dreams.mp3"]
}

# User Playlists
# Format:  username: {playlist_name:  {"songs": [[song_name, artist, genre], ...], "visits": int, "created_date": str}}
UserPlaylists = {
    "Charlie": {
        "My Favorites": {
            "songs": [
                ["Perfect Symphony", "Samantha", "Classical"],
                ["Electric Heart", "Shawn", "EDM"]
            ],
            "visits":  15,
            "created_date": "2024-09-01"
        },
        "Workout Mix": {
            "songs": [
                ["Electric Heart", "Shawn", "EDM"],
                ["Pop Dreams", "Shawn", "Pop"]
            ],
            "visits": 8,
            "created_date":  "2024-10-15"
        }
    },
    "Ezekiel": {
        "Chill Vibes": {
            "songs": [
                ["Jazz Night", "Samantha", "Jazz"],
                ["Country Road", "Adele", "Country"]
            ],
            "visits":  5,
            "created_date":  "2024-11-01"
        }
    }
}

# User Queue
# Format: username: [[song_name, artist_name, genre, queue_date], ...]
UserQueue = {
    "Charlie": [
        ["Perfect Symphony", "Samantha", "Classical", "2024-12-01"],
        ["Electric Heart", "Shawn", "EDM", "2024-12-01"]
    ],
    "Ezekiel": [
        ["Jazz Night", "Samantha", "Jazz", "2024-12-02"]
    ]
}

# User Recent Rotation (most played songs this week)
# Format: username: [[song_name, artist_name, play_count], ...]
UserRecentRotation = {
    "Charlie": [
        ["Perfect Symphony", "Samantha", 25],
        ["Electric Heart", "Shawn", 18],
        ["Pop Dreams", "Shawn", 12],
        ["Jazz Night", "Samantha", 8],
        ["Country Road", "Adele", 5]
    ],
    "Ezekiel": [
        ["Jazz Night", "Samantha", 30],
        ["Country Road", "Adele", 22],
        ["Perfect Symphony", "Samantha", 15]
    ],
    "Samantha": [
        ["Electric Heart", "Shawn", 20],
        ["Pop Dreams", "Shawn", 15],
        ["Country Road", "Adele", 10]
    ],
    "Shawn": [
        ["Perfect Symphony", "Samantha", 18],
        ["Jazz Night", "Samantha", 14],
        ["Country Road", "Adele", 8]
    ]
}

# Top Artists Weekly
# Format: [[artist_name, total_listens, best_song], ...]
TopArtistsWeekly = [
    ["Samantha", 5200, "Perfect Symphony"],
    ["Shawn", 4800, "Electric Heart"],
    ["Adele", 3500, "Country Road"],
    ["Drake", 2800, "One Dance"],
    ["Taylor", 2200, "Love Story"]
]

# Top Songs Weekly
# Format: [[song_name, artist_name, total_listens], ...]
TopSongsWeekly = [
    ["Perfect Symphony", "Samantha", 2500],
    ["Electric Heart", "Shawn", 2200],
    ["Country Road", "Adele", 1800],
    ["Pop Dreams", "Shawn", 1500],
    ["Jazz Night", "Samantha", 1200]
]

# Artist Songs (for artists to manage their uploaded songs)
# Format: username: {song_id: [song_name, genre, release_date, likes, dislikes, file_path], ...}
ArtistSongs = {
    "Samantha": {
        "AS001": ["Perfect Symphony", "Classical", "2024-08-15", 450, 20, r"songs\perfect_symphony.mp3"],
        "AS002": ["Jazz Night", "Jazz", "2024-10-05", 520, 28, r"songs\jazz_night.mp3"],
        "AS003":  ["Summer Breeze", "Pop", "2024-11-01", 180, 12, r"songs\summer_breeze.mp3"]
    },
    "Shawn": {
        "AS004": ["Electric Heart", "EDM", "2024-09-01", 850, 35, r"songs\electric_heart.mp3"],
        "AS005":  ["Pop Dreams", "Pop", "2024-09-15", 1200, 45, r"songs\pop_dreams.mp3"]
    },
    "Adele": {
        "AS006":  ["Country Road", "Country", "2024-07-20", 320, 15, r"songs\country_road.mp3"]
    }
}

# Artist Analytics Data (views per day for each artist)
# Format: username:  {date: views, ...}
ArtistViewsData = {
    "Samantha": {
        "2024-10-01": 850, "2024-10-02":  920, "2024-10-03": 780, "2024-10-04":  1050,
        "2024-10-05": 1120, "2024-10-06": 980, "2024-10-07": 1200, "2024-10-08": 1350,
        "2024-10-09": 1100, "2024-10-10": 1280, "2024-10-11": 1400, "2024-10-12": 1150,
        "2024-10-13": 1320, "2024-10-14": 1450, "2024-10-15": 1380, "2024-10-16": 1520,
        "2024-10-17": 1600, "2024-10-18": 1480, "2024-10-19": 1720, "2024-10-20": 1850,
        "2024-10-21": 1680, "2024-10-22": 1920, "2024-10-23": 2050, "2024-10-24": 1880,
        "2024-10-25": 2150, "2024-10-26": 2280, "2024-10-27": 2100, "2024-10-28": 2350,
        "2024-10-29": 2480, "2024-10-30": 2300, "2024-10-31": 2550,
        "2024-11-01": 2680, "2024-11-02": 2520, "2024-11-03": 2850, "2024-11-04": 2980,
        "2024-11-05": 2750, "2024-11-06": 3100, "2024-11-07": 3250, "2024-11-08": 3080,
        "2024-11-09": 3400, "2024-11-10": 3550, "2024-11-11": 3320, "2024-11-12": 3680,
        "2024-11-13": 3850, "2024-11-14": 3620, "2024-11-15": 3980, "2024-11-16": 4150,
        "2024-11-17": 3920, "2024-11-18": 4280, "2024-11-19": 4450, "2024-11-20": 4220,
        "2024-11-21": 4580, "2024-11-22": 4750, "2024-11-23": 4520, "2024-11-24": 4880,
        "2024-11-25": 5050, "2024-11-26": 4820, "2024-11-27": 5180, "2024-11-28": 5350,
        "2024-11-29": 5120, "2024-11-30": 5480,
        "2024-12-01": 5650, "2024-12-02": 5420, "2024-12-03": 5780, "2024-12-04": 5950,
        "2024-12-05": 5720, "2024-12-06": 6080, "2024-12-07": 6250, "2024-12-08": 6020,
        "2024-12-09": 6380, "2024-12-10": 6550
    },
    "Shawn": {
        "2024-10-01": 720, "2024-10-02": 810, "2024-10-03": 680, "2024-10-04": 920,
        "2024-10-05": 980, "2024-10-06": 850, "2024-10-07": 1050, "2024-10-08": 1180,
        "2024-10-09": 950, "2024-10-10": 1120, "2024-10-11": 1250, "2024-10-12": 1020,
        "2024-10-13": 1180, "2024-10-14": 1320, "2024-10-15": 1150, "2024-10-16": 1380,
        "2024-10-17": 1480, "2024-10-18": 1280, "2024-10-19": 1550, "2024-10-20": 1680,
        "2024-10-21": 1480, "2024-10-22": 1750, "2024-10-23": 1880, "2024-10-24": 1680,
        "2024-10-25": 1950, "2024-10-26": 2080, "2024-10-27": 1880, "2024-10-28": 2150,
        "2024-10-29": 2280, "2024-10-30": 2080, "2024-10-31": 2350,
        "2024-11-01": 2480, "2024-11-02": 2280, "2024-11-03": 2650, "2024-11-04": 2780,
        "2024-11-05": 2550, "2024-11-06": 2900, "2024-11-07": 3050, "2024-11-08": 2850,
        "2024-11-09": 3200, "2024-11-10": 3350, "2024-11-11": 3120, "2024-11-12": 3480,
        "2024-11-13": 3650, "2024-11-14": 3420, "2024-11-15": 3780, "2024-11-16": 3950,
        "2024-11-17": 3720, "2024-11-18": 4080, "2024-11-19": 4250, "2024-11-20": 4020,
        "2024-11-21": 4380, "2024-11-22": 4550, "2024-11-23": 4320, "2024-11-24": 4680,
        "2024-11-25": 4850, "2024-11-26": 4620, "2024-11-27": 4980, "2024-11-28": 5150,
        "2024-11-29": 4920, "2024-11-30": 5280,
        "2024-12-01": 5450, "2024-12-02": 5220, "2024-12-03": 5580, "2024-12-04": 5750,
        "2024-12-05": 5520, "2024-12-06": 5880, "2024-12-07": 6050, "2024-12-08": 5820,
        "2024-12-09": 6180, "2024-12-10": 6350
    },
    "Adele": {
        "2024-10-01": 520, "2024-10-02": 580, "2024-10-03": 480, "2024-10-04": 650,
        "2024-10-05": 720, "2024-10-06": 620, "2024-10-07": 780, "2024-10-08": 850,
        "2024-10-09": 720, "2024-10-10": 880, "2024-10-11": 950, "2024-10-12": 820,
        "2024-10-13": 980, "2024-10-14": 1050, "2024-10-15": 920, "2024-10-16": 1120,
        "2024-10-17": 1180, "2024-10-18": 1050, "2024-10-19": 1280, "2024-10-20": 1350,
        "2024-10-21": 1220, "2024-10-22": 1420, "2024-10-23": 1520, "2024-10-24": 1380,
        "2024-10-25": 1620, "2024-10-26": 1720, "2024-10-27": 1580, "2024-10-28": 1820,
        "2024-10-29": 1920, "2024-10-30": 1780, "2024-10-31": 2020,
        "2024-11-01": 2150, "2024-11-02": 1980, "2024-11-03": 2280, "2024-11-04": 2380,
        "2024-11-05": 2220, "2024-11-06": 2520, "2024-11-07": 2650, "2024-11-08": 2480,
        "2024-11-09": 2780, "2024-11-10": 2920, "2024-11-11": 2720, "2024-11-12": 3050,
        "2024-11-13": 3180, "2024-11-14": 2980, "2024-11-15": 3320, "2024-11-16": 3480,
        "2024-11-17": 3250, "2024-11-18": 3620, "2024-11-19": 3780, "2024-11-20": 3550,
        "2024-11-21": 3920, "2024-11-22": 4080, "2024-11-23": 3850, "2024-11-24": 4220,
        "2024-11-25": 4380, "2024-11-26": 4150, "2024-11-27": 4520, "2024-11-28": 4680,
        "2024-11-29": 4450, "2024-11-30": 4820,
        "2024-12-01": 4980, "2024-12-02": 4750, "2024-12-03": 5120, "2024-12-04": 5280,
        "2024-12-05": 5050, "2024-12-06": 5420, "2024-12-07": 5580, "2024-12-08": 5350,
        "2024-12-09": 5720, "2024-12-10": 5880
    }
}

# Artist Revenue Data (revenue per day for each artist)
# Format: username: {date: revenue, ... }
ArtistRevenueData = {
    "Samantha": {
        "2024-10-01": 42.50, "2024-10-02": 46.00, "2024-10-03": 39.00, "2024-10-04": 52.50,
        "2024-10-05": 56.00, "2024-10-06": 49.00, "2024-10-07": 60.00, "2024-10-08": 67.50,
        "2024-10-09": 55.00, "2024-10-10": 64.00, "2024-10-11": 70.00, "2024-10-12": 57.50,
        "2024-10-13": 66.00, "2024-10-14": 72.50, "2024-10-15":  69.00, "2024-10-16": 76.00,
        "2024-10-17": 80.00, "2024-10-18": 74.00, "2024-10-19": 86.00, "2024-10-20": 92.50,
        "2024-10-21": 84.00, "2024-10-22": 96.00, "2024-10-23": 102.50, "2024-10-24": 94.00,
        "2024-10-25": 107.50, "2024-10-26": 114.00, "2024-10-27": 105.00, "2024-10-28": 117.50,
        "2024-10-29": 124.00, "2024-10-30": 115.00, "2024-10-31": 127.50,
        "2024-11-01": 134.00, "2024-11-02": 126.00, "2024-11-03": 142.50, "2024-11-04": 149.00,
        "2024-11-05": 137.50, "2024-11-06": 155.00, "2024-11-07":  162.50, "2024-11-08": 154.00,
        "2024-11-09": 170.00, "2024-11-10": 177.50, "2024-11-11": 166.00, "2024-11-12": 184.00,
        "2024-11-13": 192.50, "2024-11-14": 181.00, "2024-11-15": 199.00, "2024-11-16": 207.50,
        "2024-11-17": 196.00, "2024-11-18": 214.00, "2024-11-19":  222.50, "2024-11-20": 211.00,
        "2024-11-21": 229.00, "2024-11-22": 237.50, "2024-11-23": 226.00, "2024-11-24": 244.00,
        "2024-11-25": 252.50, "2024-11-26": 241.00, "2024-11-27": 259.00, "2024-11-28":  267.50,
        "2024-11-29": 256.00, "2024-11-30": 274.00,
        "2024-12-01": 282.50, "2024-12-02": 271.00, "2024-12-03": 289.00, "2024-12-04":  297.50,
        "2024-12-05": 286.00, "2024-12-06": 304.00, "2024-12-07": 312.50, "2024-12-08":  301.00,
        "2024-12-09": 319.00, "2024-12-10": 327.50
    },
    "Shawn": {
        "2024-10-01": 36.00, "2024-10-02": 40.50, "2024-10-03": 34.00, "2024-10-04": 46.00,
        "2024-10-05": 49.00, "2024-10-06": 42.50, "2024-10-07": 52.50, "2024-10-08": 59.00,
        "2024-10-09": 47.50, "2024-10-10": 56.00, "2024-10-11": 62.50, "2024-10-12": 51.00,
        "2024-10-13": 59.00, "2024-10-14": 66.00, "2024-10-15": 57.50, "2024-10-16": 69.00,
        "2024-10-17": 74.00, "2024-10-18": 64.00, "2024-10-19": 77.50, "2024-10-20": 84.00,
        "2024-10-21": 74.00, "2024-10-22": 87.50, "2024-10-23": 94.00, "2024-10-24": 84.00,
        "2024-10-25": 97.50, "2024-10-26": 104.00, "2024-10-27": 94.00, "2024-10-28": 107.50,
        "2024-10-29": 114.00, "2024-10-30": 104.00, "2024-10-31": 117.50,
        "2024-11-01": 124.00, "2024-11-02": 114.00, "2024-11-03": 132.50, "2024-11-04": 139.00,
        "2024-11-05": 127.50, "2024-11-06": 145.00, "2024-11-07": 152.50, "2024-11-08":  142.50,
        "2024-11-09": 160.00, "2024-11-10":  167.50, "2024-11-11": 156.00, "2024-11-12": 174.00,
        "2024-11-13": 182.50, "2024-11-14": 171.00, "2024-11-15": 189.00, "2024-11-16":  197.50,
        "2024-11-17": 186.00, "2024-11-18": 204.00, "2024-11-19":  212.50, "2024-11-20": 201.00,
        "2024-11-21": 219.00, "2024-11-22": 227.50, "2024-11-23": 216.00, "2024-11-24": 234.00,
        "2024-11-25": 242.50, "2024-11-26": 231.00, "2024-11-27": 249.00, "2024-11-28":  257.50,
        "2024-11-29": 246.00, "2024-11-30": 264.00,
        "2024-12-01": 272.50, "2024-12-02": 261.00, "2024-12-03": 279.00, "2024-12-04":  287.50,
        "2024-12-05": 276.00, "2024-12-06": 294.00, "2024-12-07":  302.50, "2024-12-08": 291.00,
        "2024-12-09": 309.00, "2024-12-10": 317.50
    },
    "Adele": {
        "2024-10-01": 26.00, "2024-10-02": 29.00, "2024-10-03": 24.00, "2024-10-04": 32.50,
        "2024-10-05": 36.00, "2024-10-06": 31.00, "2024-10-07": 39.00, "2024-10-08": 42.50,
        "2024-10-09": 36.00, "2024-10-10": 44.00, "2024-10-11":  47.50, "2024-10-12": 41.00,
        "2024-10-13": 49.00, "2024-10-14": 52.50, "2024-10-15": 46.00, "2024-10-16":  56.00,
        "2024-10-17": 59.00, "2024-10-18": 52.50, "2024-10-19": 64.00, "2024-10-20": 67.50,
        "2024-10-21": 61.00, "2024-10-22": 71.00, "2024-10-23": 76.00, "2024-10-24": 69.00,
        "2024-10-25":  81.00, "2024-10-26": 86.00, "2024-10-27": 79.00, "2024-10-28":  91.00,
        "2024-10-29": 96.00, "2024-10-30": 89.00, "2024-10-31": 101.00,
        "2024-11-01": 107.50, "2024-11-02": 99.00, "2024-11-03": 114.00, "2024-11-04": 119.00,
        "2024-11-05": 111.00, "2024-11-06": 126.00, "2024-11-07": 132.50, "2024-11-08": 124.00,
        "2024-11-09": 139.00, "2024-11-10": 146.00, "2024-11-11": 136.00, "2024-11-12": 152.50,
        "2024-11-13": 159.00, "2024-11-14": 149.00, "2024-11-15": 166.00, "2024-11-16": 174.00,
        "2024-11-17": 162.50, "2024-11-18": 181.00, "2024-11-19": 189.00, "2024-11-20": 177.50,
        "2024-11-21": 196.00, "2024-11-22": 204.00, "2024-11-23": 192.50, "2024-11-24": 211.00,
        "2024-11-25": 219.00, "2024-11-26": 207.50, "2024-11-27": 226.00, "2024-11-28": 234.00,
        "2024-11-29": 222.50, "2024-11-30": 241.00,
        "2024-12-01": 249.00, "2024-12-02": 237.50, "2024-12-03":  256.00, "2024-12-04": 264.00,
        "2024-12-05": 252.50, "2024-12-06": 271.00, "2024-12-07": 279.00, "2024-12-08":  267.50,
        "2024-12-09": 286.00, "2024-12-10": 294.00
    }
}


# ==================== GETTER FUNCTIONS ====================

def get_user(username):
    """Get user data by username"""
    return Users.get(username)

def get_all_users():
    """Get all users"""
    return Users

def get_pending_requests():
    """Get all pending artist requests"""
    return PendingArtistRequests

def get_pending_songs():
    """Get all pending songs"""
    return PendingSongs

def get_reported_songs():
    """Get all reported songs"""
    return ReportedSongs

def get_subscription_plans():
    """Get all subscription plans"""
    return SubscriptionPlans

def get_all_genres():
    return Genres

def get_approved_songs():
    """Get all approved songs"""
    return ApprovedSongs

def get_user_playlists(username):
    """Get playlists for a specific user"""
    return UserPlaylists.get(username, {})

def get_user_queue(username):
    """Get queue for a specific user"""
    return UserQueue.get(username, [])

def get_user_recent_rotation(username):
    """Get recent rotation for a specific user"""
    return UserRecentRotation.get(username, [])

def get_top_artists_weekly():
    """Get top artists of the week"""
    return TopArtistsWeekly

def get_top_songs_weekly():
    """Get top songs of the week"""
    return TopSongsWeekly

def get_artist_songs(username):
    """Get songs uploaded by an artist"""
    return ArtistSongs.get(username, {})

def get_artist_views_data(username):
    """Get views data for an artist"""
    return ArtistViewsData.get(username, {})

def get_artist_revenue_data(username):
    """Get revenue data for an artist"""
    return ArtistRevenueData.get(username, {})


# ==================== ANALYTICS FUNCTIONS ====================

def get_analytics_data(username, analytics_type, group_by, start_date, end_date):
    """
    Get analytics data for an artist. 
    
    Args:
        username: The artist's username
        analytics_type:  'views' or 'revenue'
        group_by: 'day', 'month', or 'year'
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
    
    Returns:
        Dictionary with grouped data {label: value, ...}
    """
    from datetime import datetime
    from collections import defaultdict
    
    # Get raw data based on type
    if analytics_type == "views":
        raw_data = get_artist_views_data(username)
    else: 
        raw_data = get_artist_revenue_data(username)
    
    if not raw_data:
        return {}
    
    # Filter by date range
    filtered_data = {}
    for date_str, value in raw_data.items():
        if start_date <= date_str <= end_date:
            filtered_data[date_str] = value
    
    if not filtered_data:
        return {}
    
    # Group data
    if group_by == "day": 
        return dict(sorted(filtered_data.items()))
    
    elif group_by == "month":
        monthly_data = defaultdict(float)
        for date_str, value in filtered_data.items():
            month_key = date_str[: 7]  # YYYY-MM
            monthly_data[month_key] += value
        return dict(sorted(monthly_data.items()))
    
    elif group_by == "year":
        yearly_data = defaultdict(float)
        for date_str, value in filtered_data.items():
            year_key = date_str[:4]  # YYYY
            yearly_data[year_key] += value
        return dict(sorted(yearly_data.items()))
    
    return filtered_data


# ==================== USER MANAGEMENT FUNCTIONS ====================

def add_user(username, user_data):
    """Add a new user"""
    Users[username] = user_data

def remove_user(username):
    """Remove a user"""
    if username in Users:
        del Users[username]
        # Also clean up related data
        if username in UserPlaylists:
            del UserPlaylists[username]
        if username in UserQueue:
            del UserQueue[username]
        if username in UserRecentRotation:
            del UserRecentRotation[username]
        if username in ArtistSongs:
            del ArtistSongs[username]
        return True
    return False

def accept_artist_request(username):
    """Accept an artist request and update user type"""
    if username in PendingArtistRequests: 
        if username in Users:
            Users[username][4] = "Artist"
        del PendingArtistRequests[username]
        return True
    return False

def reject_artist_request(username):
    """Reject an artist request"""
    if username in PendingArtistRequests:
        del PendingArtistRequests[username]
        return True
    return False


# ==================== SONG MANAGEMENT FUNCTIONS ====================

def approve_song(song_id):
    """Approve a pending song"""
    if song_id in PendingSongs:
        song_data = PendingSongs[song_id]
        ApprovedSongs[song_id] = [song_data[0], song_data[1], song_data[2], song_data[3], 0, 0, song_data[4]]
        del PendingSongs[song_id]
        return True
    return False

def reject_song(song_id):
    """Reject a pending song"""
    if song_id in PendingSongs: 
        del PendingSongs[song_id]
        return True
    return False

def delete_reported_song(song_id):
    """Delete a reported song"""
    removed = False
    for report_id, report_data in list(ReportedSongs.items()):
        if report_data[0] == song_id: 
            del ReportedSongs[report_id]
            removed = True
    
    if song_id in ApprovedSongs:
        del ApprovedSongs[song_id]
        removed = True
    
    return removed


# ==================== SUBSCRIPTION FUNCTIONS ====================

def add_subscription_plan(plan_id, plan_data):
    """Add a new subscription plan"""
    SubscriptionPlans[plan_id] = plan_data

def update_subscription_plan(plan_id, plan_data):
    """Update an existing subscription plan"""
    if plan_id in SubscriptionPlans:
        SubscriptionPlans[plan_id] = plan_data
        return True
    return False


# ==================== GENRE FUNCTIONS ====================

def add_genre(genre_id, genre_data):
    Genres[genre_id] = genre_data


# ==================== PLAYLIST FUNCTIONS ====================

def add_user_playlist(username, playlist_name, playlist_data):
    """Add a new playlist for a user"""
    if username not in UserPlaylists: 
        UserPlaylists[username] = {}
    UserPlaylists[username][playlist_name] = playlist_data

def delete_user_playlist(username, playlist_name):
    """Delete a user's playlist"""
    if username in UserPlaylists and playlist_name in UserPlaylists[username]: 
        del UserPlaylists[username][playlist_name]
        return True
    return False

def add_song_to_playlist(username, playlist_name, song_data):
    """Add a song to a user's playlist"""
    if username in UserPlaylists and playlist_name in UserPlaylists[username]: 
        UserPlaylists[username][playlist_name]["songs"].append(song_data)
        return True
    return False

def increment_playlist_visits(username, playlist_name):
    """Increment visit count for a playlist"""
    if username in UserPlaylists and playlist_name in UserPlaylists[username]:
        UserPlaylists[username][playlist_name]["visits"] += 1
        return True
    return False


# ==================== QUEUE FUNCTIONS ====================

def add_to_user_queue(username, song_data):
    """Add a song to user's queue"""
    if username not in UserQueue:
        UserQueue[username] = []
    UserQueue[username].append(song_data)

def remove_from_user_queue(username, index):
    """Remove a song from user's queue by index"""
    if username in UserQueue and 0 <= index < len(UserQueue[username]):
        return UserQueue[username].pop(index)
    return None

def clear_user_queue(username):
    """Clear all songs from user's queue"""
    if username in UserQueue:
        UserQueue[username] = []


# ==================== ARTIST SONG FUNCTIONS ====================

def add_artist_song(username, song_id, song_data):
    """Add a song for an artist"""
    if username not in ArtistSongs: 
        ArtistSongs[username] = {}
    ArtistSongs[username][song_id] = song_data

def delete_artist_song(username, song_id):
    """Delete an artist's song"""
    if username in ArtistSongs and song_id in ArtistSongs[username]:
        del ArtistSongs[username][song_id]
        return True
    return False