import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from data import * # Import all data and functions from data.py

class AdminDashboardHandler:
    """
    Handles all logic for the AdminDashboard.
    This class loads data into tables, populates forms when rows are clicked,
    and executes actions (like delete, approve, reject).
    """
    
    def __init__(self, window: QtWidgets.QMainWindow):
        """
        Initialize the handler.
        - window: A reference to the AdminDashboard main window instance.
        """
        self.window = window

    def connect_signals(self):
        """Connects all UI signals (buttons, tables) to their handler methods."""
        
        # --- Artist Requests Page ---
        self.window.artistsRequestTable.cellClicked.connect(self.populate_artist_request_form)
        self.window.RequestS_AcceptBtn.clicked.connect(self.handle_accept_artist_request)
        self.window.Requests_RejectBtn.clicked.connect(self.handle_reject_artist_request)

        # --- Users Management Page ---
        self.window.tableWidget.cellClicked.connect(self.populate_user_form)
        self.window.deleteUserBtn.clicked.connect(self.handle_delete_user)

        # --- Pending Songs Page ---
        self.window.pendingSongsTable.cellClicked.connect(self.populate_pending_song_form)
        self.window.playSongBtn.clicked.connect(self.handle_view_song)
        self.window.acceptSongBtn.clicked.connect(self.handle_approve_song)
        self.window.rejectSongBtn.clicked.connect(self.handle_reject_song)
        
        # --- Reports Page ---
        self.window.reportedSongsTable.cellClicked.connect(self.populate_reported_song_form)
        self.window.DeleteSongBtn.clicked.connect(self.handle_delete_reported_song)
        
        # --- Analytics Page (Subscriptions) ---
        self.window.tableWidget_2.cellClicked.connect(self.populate_subscription_plan_form)
        self.window.AddPlanBtn.clicked.connect(self.handle_add_subscription_plan)
        self.window.AddPlanBtn_2.clicked.connect(self.handle_update_subscription_plan) # 'Update Plan' button

    def load_all_data(self):
        """Loads data into all tables on the dashboard."""
        self.load_artist_requests_table()
        self.load_users_table()
        self.load_pending_songs_table()
        self.load_reported_songs_table()
        self.load_subscription_plans_table()

    # --- Helper to convert string to QDate ---
    def string_to_qdate(self, date_str: str) -> QtCore.QDate:
        """Converts a 'YYYY-MM-DD' string to a QDate object."""
        return QtCore.QDate.fromString(date_str, "yyyy-MM-dd")

    # 1. ARTIST REQUESTS

    def load_artist_requests_table(self):
        """Populates the Pending Artist Requests table."""
        requests = get_pending_requests()
        table = self.window.artistsRequestTable
        table.setRowCount(len(requests))
        
        for row, (username, data) in enumerate(requests.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row + 1)))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(username))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(data[0])) # Full Name
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(data[1])) # Email
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(data[2])) # Subscription
        
        table.resizeColumnsToContents()

    def populate_artist_request_form(self, row, column):
        """Fills the form with data from the clicked row in the artist requests table."""
        table = self.window.artistsRequestTable
        username = table.item(row, 1).text()
        request_data = get_pending_requests().get(username)
        
        if request_data:
            self.window.UsernameLineEdit_2.setText(username)
            self.window.FullNameLineEdit_2.setText(request_data[0]) # Full Name
            self.window.EmailLineEdit_2.setText(request_data[1])     # Email
            self.window.SubscriptionLineEdit_2.setText(request_data[2]) # Subscription
            self.window.dateJoined_2.setDate(self.string_to_qdate(request_data[3])) # Date Joined

    def clear_artist_request_form(self):
        """Clears all fields in the artist request detail form."""
        self.window.UsernameLineEdit_2.clear()
        self.window.FullNameLineEdit_2.clear()
        self.window.EmailLineEdit_2.clear()
        self.window.SubscriptionLineEdit_2.clear()
        self.window.dateJoined_2.setDate(QtCore.QDate.currentDate())
            
    def handle_accept_artist_request(self):
        """Handles the 'Accept' button click for an artist request."""
        username = self.window.UsernameLineEdit_2.text()
        if not username:
            QtWidgets.QMessageBox.warning(self.window, "No User Selected", "Please select an artist request from the table.")
            return

        if accept_artist_request(username):
            QtWidgets.QMessageBox.information(self.window, "Success", f"Artist request for '{username}' has been accepted.")
            self.load_artist_requests_table() # Refresh table
            self.clear_artist_request_form()  # Clear form
        else:
            QtWidgets.QMessageBox.critical(self.window, "Error", f"Could not find or accept request for '{username}'.")

    def handle_reject_artist_request(self):
        """Handles the 'Reject' button click for an artist request."""
        username = self.window.UsernameLineEdit_2.text()
        if not username:
            QtWidgets.QMessageBox.warning(self.window, "No User Selected", "Please select an artist request from the table.")
            return
        
        if reject_artist_request(username):
            QtWidgets.QMessageBox.information(self.window, "Success", f"Artist request for '{username}' has been rejected.")
            self.load_artist_requests_table() # Refresh table
            self.clear_artist_request_form()  # Clear form
        else:
            QtWidgets.QMessageBox.critical(self.window, "Error", f"Could not find or reject request for '{username}'.")


    # 2. USERS MANAGEMENT

    def load_users_table(self):
        """Populates the Users Management table."""
        users = get_all_users()
        table = self.window.tableWidget
        table.setRowCount(len(users))
        
        for row, (username, data) in enumerate(users.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(username))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(data[0])) # Full Name
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(data[2])) # Email
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(data[7])) # Date Joined
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(data[4])) # UserType
        
        table.resizeColumnsToContents()

    def populate_user_form(self, row, column):
        """Fills the form with data from the clicked row in the users table."""
        table = self.window.tableWidget
        username = table.item(row, 0).text()
        user_data = get_user(username)
        
        if user_data:
            self.window.UsernameLineEdit.setText(username)
            self.window.FullNameLineEdit.setText(user_data[0])
            self.window.EmailLineEdit.setText(user_data[2])
            self.window.dateJoined.setDate(self.string_to_qdate(user_data[7]))
            self.window.UserTypeLineEdit.setText(user_data[4])
            self.window.SubscriptionLineEdit.setText(user_data[5])
            self.window.RevenueLineEdit.setText(str(user_data[6]))

    def clear_user_form(self):
        """Clears all fields in the user detail form."""
        self.window.UsernameLineEdit.clear()
        self.window.FullNameLineEdit.clear()
        self.window.EmailLineEdit.clear()
        self.window.dateJoined.setDate(QtCore.QDate.currentDate())
        self.window.UserTypeLineEdit.clear()
        self.window.SubscriptionLineEdit.clear()
        self.window.RevenueLineEdit.clear()

    def handle_delete_user(self):
        """Handles the 'Delete User' button click."""
        username = self.window.UsernameLineEdit.text()
        if not username:
            QtWidgets.QMessageBox.warning(self.window, "No User Selected", "Please select a user from the table to delete.")
            return

        reply = QtWidgets.QMessageBox.question(
            self.window, "Confirm Deletion",
            f"Are you sure you want to delete the user '{username}'? This action cannot be undone.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            if remove_user(username):
                QtWidgets.QMessageBox.information(self.window, "Success", f"User '{username}' has been deleted.")
                self.load_users_table() # Refresh table
                self.clear_user_form()  # Clear form
            else:
                QtWidgets.QMessageBox.critical(self.window, "Error", f"Could not find or delete user '{username}'.")

    # 3. PENDING SONGS

    def load_pending_songs_table(self):
        """Populates the Songs Pending Approval table."""
        songs = get_pending_songs()
        table = self.window.pendingSongsTable
        table.setRowCount(len(songs))
        
        for row, (song_id, data) in enumerate(songs.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(song_id))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(data[0])) # Song Name
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(data[1])) # Artist Name
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(data[2])) # Genre
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(data[3])) # Submission Date
        
        table.resizeColumnsToContents()

    def populate_pending_song_form(self, row, column):
        """Fills the form with data from the clicked row in the pending songs table."""
        table = self.window.pendingSongsTable
        song_id = table.item(row, 0).text()
        song_data = get_pending_songs().get(song_id)
        
        if song_data:
            self.window.PendingsongID.setText(song_id)
            self.window.PendingSongName.setText(song_data[0])
            self.window.ArtistName.setText(song_data[1])
            self.window.genreLineEdit.setText(song_data[2])
            self.window.submissionDate.setDate(self.string_to_qdate(song_data[3]))
            
            # Load song image
            image_path = song_data[5]
            pixmap = QtGui.QPixmap(image_path)
            if pixmap.isNull():
                # Set a default image if path is invalid or image not found
                self.window.songImage.setPixmap(QtGui.QPixmap("Song_images/default_song_image.jpg"))
            else:
                self.window.songImage.setPixmap(pixmap)

    def clear_pending_song_form(self):
        """Clears all fields in the pending song detail form."""
        self.window.PendingsongID.clear()
        self.window.PendingSongName.clear()
        self.window.ArtistName.clear()
        self.window.genreLineEdit.clear()
        self.window.submissionDate.setDate(QtCore.QDate.currentDate())
        self.window.songImage.setPixmap(QtGui.QPixmap("Song_images/default_song_image.jpg"))

    def handle_view_song(self):
        """Handles the 'Play Song' button click."""
        song_id = self.window.PendingsongID.text()
        if not song_id:
            QtWidgets.QMessageBox.warning(self.window, "No Song Selected", "Please select a song from the table to play.")
            return
        
        song_data = get_pending_songs().get(song_id)
        if song_data:
            song_name = song_data[0]
            song_path = song_data[4]
            # This just shows a popup. Real playback would need a media library.
            QtWidgets.QMessageBox.information(self.window, "Playing Song", f"Simulating playback of: {song_name}\n(from {song_path})")
        
    def handle_approve_song(self):
        """Handles the 'Accept' button click for a pending song."""
        song_id = self.window.PendingsongID.text()
        if not song_id:
            QtWidgets.QMessageBox.warning(self.window, "No Song Selected", "Please select a song from the table to approve.")
            return
            
        if approve_song(song_id):
            QtWidgets.QMessageBox.information(self.window, "Success", f"Song has been approved and added to the library.")
            self.load_pending_songs_table() # Refresh table
            self.clear_pending_song_form()  # Clear form
        else:
            QtWidgets.QMessageBox.critical(self.window, "Error", f"Could not find or approve song with ID '{song_id}'.")

    def handle_reject_song(self):
        """Handles the 'Reject' button click for a pending song."""
        song_id = self.window.PendingsongID.text()
        if not song_id:
            QtWidgets.QMessageBox.warning(self.window, "No Song Selected", "Please select a song from the table to reject.")
            return
            
        if reject_song(song_id):
            QtWidgets.QMessageBox.information(self.window, "Success", f"Song has been rejected.")
            self.load_pending_songs_table() # Refresh table
            self.clear_pending_song_form()  # Clear form
        else:
            QtWidgets.QMessageBox.critical(self.window, "Error", f"Could not find or reject song with ID '{song_id}'.")


    # 4. REPORTED SONGS

    def load_reported_songs_table(self):
        """Populates the Reported Songs table."""
        reports = get_reported_songs()
        table = self.window.reportedSongsTable
        table.setRowCount(len(reports))
        
        for row, (report_id, data) in enumerate(reports.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(report_id))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(data[1])) # Song Name
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(data[2])) # Artist Name
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(data[3])) # Reported By
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(data[4])) # Reason
        
        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)


    def populate_reported_song_form(self, row, column):
        """Fills the form with data from the clicked row in the reported songs table."""
        table = self.window.reportedSongsTable
        report_id = table.item(row, 0).text()
        report_data = get_reported_songs().get(report_id)
        
        if report_data:
            self.window.Reports_SongID.setText(report_data[0])
            self.window.Reports_SongName.setText(report_data[1])
            self.window.Reports_ArtistName.setText(report_data[2])
            self.window.Reports_Genre.setText(report_data[5])
            self.window.Reports_Likes.setText(str(report_data[6]))
            self.window.Reports_Dislikes.setText(str(report_data[7]))
            self.window.Reports_Dislikes_2.setText(str(report_data[8])) # Total Reports
            self.window.Reports_UploadDate.setDate(self.string_to_qdate(report_data[9]))

    def clear_reported_song_form(self):
        """Clears all fields in the reported song detail form."""
        self.window.Reports_SongID.clear()
        self.window.Reports_SongName.clear()
        self.window.Reports_ArtistName.clear()
        self.window.Reports_Genre.clear()
        self.window.Reports_Likes.clear()
        self.window.Reports_Dislikes.clear()
        self.window.Reports_Dislikes_2.clear()
        self.window.Reports_UploadDate.setDate(QtCore.QDate.currentDate())

    def handle_delete_reported_song(self):
        """Handles the 'Delete Song' button click from the reports page."""
        song_id = self.window.Reports_SongID.text()
        if not song_id:
            QtWidgets.QMessageBox.warning(self.window, "No Song Selected", "Please select a reported song from the table to delete.")
            return

        reply = QtWidgets.QMessageBox.question(
            self.window, "Confirm Deletion",
            f"Are you sure you want to permanently delete the song with ID '{song_id}'? This action cannot be undone.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            if delete_reported_song(song_id):
                QtWidgets.QMessageBox.information(self.window, "Success", f"Song '{song_id}' has been deleted from the system.")
                self.load_reported_songs_table() # Refresh table
                self.clear_reported_song_form()  # Clear form
            else:
                QtWidgets.QMessageBox.critical(self.window, "Error", f"Could not find or delete song with ID '{song_id}'.")


    # 5. SUBSCRIPTION PLANS

    def load_subscription_plans_table(self):
        """Populates the Subscription Plans table on the Analytics page."""
        plans = get_subscription_plans()
        table = self.window.tableWidget_2
        table.setRowCount(len(plans))
        
        for row, (plan_id, data) in enumerate(plans.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(plan_id))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(data[0])) # Plan Name
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data[1]))) # Price
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(data[2])) # Duration
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(data[3])) # Features
        
        table.resizeColumnsToContents()

    def populate_subscription_plan_form(self, row, column):
        """Fills the form with data from the clicked row in the subscription plans table."""
        table = self.window.tableWidget_2
        # Store plan_id in a dynamic property of the window for update_plan to use
        self.window.current_plan_id = table.item(row, 0).text()
        
        plan_data = get_subscription_plans().get(self.window.current_plan_id)
        
        if plan_data:
            self.window.PlanName.setText(plan_data[0])
            self.window.PlanPrice.setText(str(plan_data[1]))
            self.window.PlanDuration.setText(plan_data[2])
            self.window.PlanFeatures.setText(plan_data[3])

    def clear_subscription_plan_form(self):
        """Clears all fields in the subscription plan form."""
        self.window.PlanName.clear()
        self.window.PlanPrice.clear()
        self.window.PlanDuration.clear()
        self.window.PlanFeatures.clear()
        if hasattr(self.window, "current_plan_id"):
            del self.window.current_plan_id
            
    def handle_add_subscription_plan(self):
        """Handles adding a new subscription plan."""
        # Simple new ID generation
        plan_id = f"SP{len(get_subscription_plans()) + 1:03d}"
        plan_name = self.window.PlanName.text()
        try:
            plan_price = float(self.window.PlanPrice.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self.window, "Invalid Input", "Price must be a valid number.")
            return
            
        plan_duration = self.window.PlanDuration.text()
        plan_features = self.window.PlanFeatures.text()

        if not all([plan_name, plan_duration, plan_features]):
            QtWidgets.QMessageBox.warning(self.window, "Missing Information", "Please fill out all plan fields.")
            return
            
        plan_data = [plan_name, plan_price, plan_duration, plan_features]
        add_subscription_plan(plan_id, plan_data)
        
        QtWidgets.QMessageBox.information(self.window, "Success", f"New plan '{plan_name}' added with ID '{plan_id}'.")
        self.load_subscription_plans_table()
        self.clear_subscription_plan_form()

    def handle_update_subscription_plan(self):
        """Handles updating an existing subscription plan."""
        if not hasattr(self.window, "current_plan_id"):
            QtWidgets.QMessageBox.warning(self.window, "No Plan Selected", "Please select a plan from the table to update.")
            return
            
        plan_id = self.window.current_plan_id
        plan_name = self.window.PlanName.text()
        try:
            plan_price = float(self.window.PlanPrice.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self.window, "Invalid Input", "Price must be a valid number.")
            return
            
        plan_duration = self.window.PlanDuration.text()
        plan_features = self.window.PlanFeatures.text()

        if not all([plan_name, plan_duration, plan_features]):
            QtWidgets.QMessageBox.warning(self.window, "Missing Information", "Please fill out all plan fields.")
            return
            
        plan_data = [plan_name, plan_price, plan_duration, plan_features]
        
        if update_subscription_plan(plan_id, plan_data):
            QtWidgets.QMessageBox.information(self.window, "Success", f"Plan '{plan_name}' (ID: {plan_id}) has been updated.")
            self.load_subscription_plans_table()
            self.clear_subscription_plan_form()
        else:
            QtWidgets.QMessageBox.critical(self.window, "Error", f"Could not find or update plan with ID '{plan_id}'.")