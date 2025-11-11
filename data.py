"""
Sample data for testing admin functions in the Music App
This file contains all the test data for users, songs, reports, and subscriptions
"""

from datetime import datetime, timedelta

# Users Dictionary
# Format: username: [fullname, password, email, profile_pic_path, usertype, subscription, revenue, date_joined]
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
               r"Profile Pictures\default.jpg", "Listener", "Premium", 15.99, "2024-06-15"],
    
    "Drake": ["Drake Graham", "drake123", "drake@gmail.com", 
              r"Profile Pictures\default.jpg", "Listener", "Free", 0, "2024-07-20"],
    
    "Adele": ["Adele Adkins", "adele123", "adele@gmail.com", 
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
              r"Songs\summer_vibes.mp3", r"Song_images\summer.jpg"],
    
    "PS002": ["Midnight Blues", "Shawn", "Blues", "2024-11-03", 
              r"Songs\midnight_blues.mp3", r"Song_images\blues.jpg"],
    
    "PS003": ["Dance Revolution", "Adele", "Electronic", "2024-11-05", 
              r"Songs\dance_rev.mp3", r"Song_images\dance.jpg"],
    
    "PS004": ["Acoustic Dreams", "Samantha", "Acoustic", "2024-11-07", 
              r"Songs\acoustic.mp3", r"Song_images\acoustic.jpg"],
    
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

# Revenue Data (for analytics)
# Format: date: revenue_amount
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
    "2024-11-01": 4050.50
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
    "2024-11-01": 55800
}

# Approved Songs (songs that have been accepted)
ApprovedSongs = {
    "S001": ["Perfect Symphony", "Samantha", "Classical", "2024-08-15", 450, 20],
    "S002": ["Electric Heart", "Shawn", "EDM", "2024-09-01", 850, 35],
    "S003": ["Country Road", "Adele", "Country", "2024-07-20", 320, 15],
    "S004": ["Jazz Night", "Samantha", "Jazz", "2024-10-05", 520, 28],
    "S005": ["Pop Dreams", "Shawn", "Pop", "2024-09-15", 1200, 45]
}

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

def add_user(username, user_data):
    """Add a new user"""
    Users[username] = user_data

def remove_user(username):
    """Remove a user"""
    if username in Users:
        del Users[username]
        return True
    return False

def accept_artist_request(username):
    """Accept an artist request and update user type"""
    if username in PendingArtistRequests:
        # Update user type to Artist
        if username in Users:
            Users[username][4] = "Artist"
        # Remove from pending requests
        del PendingArtistRequests[username]
        return True
    return False

def reject_artist_request(username):
    """Reject an artist request"""
    if username in PendingArtistRequests:
        del PendingArtistRequests[username]
        return True
    return False

def approve_song(song_id):
    """Approve a pending song"""
    if song_id in PendingSongs:
        song_data = PendingSongs[song_id]
        # Add to approved songs
        ApprovedSongs[song_id] = [song_data[0], song_data[1], song_data[2], song_data[3], 0, 0]
        # Remove from pending
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
    # Remove from all song collections
    removed = False
    for report_id, report_data in list(ReportedSongs.items()):
        if report_data[0] == song_id:
            del ReportedSongs[report_id]
            removed = True
    
    if song_id in ApprovedSongs:
        del ApprovedSongs[song_id]
        removed = True
    
    return removed

def add_subscription_plan(plan_id, plan_data):
    """Add a new subscription plan"""
    SubscriptionPlans[plan_id] = plan_data

def update_subscription_plan(plan_id, plan_data):
    """Update an existing subscription plan"""
    if plan_id in SubscriptionPlans:
        SubscriptionPlans[plan_id] = plan_data
        return True
    return False