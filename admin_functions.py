import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from data import *  # Import all data and functions from data.py
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, timedelta


class AnalyticsGraphDialog(QtWidgets.QDialog):
    """Dialog window to display analytics graphs."""

    def __init__(self,
                 parent,
                 title,
                 x_data,
                 y_data,
                 x_label,
                 y_label,
                 graph_type="line"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(800, 600)

        layout = QtWidgets.QVBoxLayout(self)

        # Create matplotlib figure
        self.canvas = FigureCanvas(Figure(figsize=(8, 5)))
        layout.addWidget(self.canvas)

        self.ax = self.canvas.figure.add_subplot(111)
        self.plot_graph(x_data, y_data, x_label, y_label, title, graph_type)

        # Close button
        close_btn = QtWidgets.QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def plot_graph(self, x_data, y_data, x_label, y_label, title, graph_type):
        self.ax.clear()

        if graph_type == "line":
            self.ax.plot(x_data,
                         y_data,
                         marker='o',
                         linestyle='-',
                         linewidth=2,
                         color='#1DB954')
            self.ax.fill_between(x_data, y_data, alpha=0.3, color='#1DB954')
        elif graph_type == "bar":
            bars = self.ax.bar(x_data,
                               y_data,
                               color='#1DB954',
                               edgecolor='black')
            # Add value labels on bars
            for bar, val in zip(bars, y_data):
                self.ax.text(bar.get_x() + bar.get_width() / 2,
                             bar.get_height() + 0.5,
                             str(int(val)),
                             ha='center',
                             va='bottom',
                             fontsize=9)

        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.ax.set_xlabel(x_label, fontsize=12)
        self.ax.set_ylabel(y_label, fontsize=12)
        self.ax.grid(True, alpha=0.3)

        # Rotate x-axis labels if there are many
        if len(x_data) > 5:
            self.ax.tick_params(axis='x', rotation=45)

        self.canvas.figure.tight_layout()
        self.canvas.draw()


class AdminDashboardHandler:
    """
    Handles all logic for the AdminDashboard. 
    This class loads data into tables, populates forms when rows are clicked,
    and executes actions (like delete, approve, reject). 
    """

    def __init__(self, window: QtWidgets.QMainWindow):
        self.window = window

    def connect_signals(self):
        """Connects all UI signals (buttons, tables) to their handler methods."""

        # --- Artist Requests Page ---
        self.window.artistsRequestTable.cellClicked.connect(
            self.populate_artist_request_form)
        self.window.RequestS_AcceptBtn.clicked.connect(
            self.handle_accept_artist_request)
        self.window.Requests_RejectBtn.clicked.connect(
            self.handle_reject_artist_request)
        self.window.pushButton.clicked.connect(
            self.handle_search_artist_requests)

        # --- Users Management Page ---
        self.window.tableWidget.cellClicked.connect(self.populate_user_form)
        self.window.deleteUserBtn.clicked.connect(self.handle_delete_user)
        self.window.searchUserBtn.clicked.connect(self.handle_search_users)

        # --- Pending Songs Page ---
        self.window.pendingSongsTable.cellClicked.connect(
            self.populate_pending_song_form)
        self.window.playSongBtn.clicked.connect(self.handle_view_song)
        self.window.acceptSongBtn.clicked.connect(self.handle_approve_song)
        self.window.rejectSongBtn.clicked.connect(self.handle_reject_song)
        self.window.pendingSongBtn.clicked.connect(
            self.handle_search_pending_songs)

        # --- Reports Page ---
        self.window.reportedSongsTable.cellClicked.connect(
            self.populate_reported_song_form)
        self.window.DeleteSongBtn.clicked.connect(
            self.handle_delete_reported_song)
        self.window.searchReportBtn.clicked.connect(self.handle_search_reports)

        # --- Analytics Page (Subscriptions) ---
        self.window.tableWidget_2.cellClicked.connect(
            self.populate_subscription_plan_form)
        self.window.AddPlanBtn.clicked.connect(
            self.handle_add_subscription_plan)
        self.window.AddPlanBtn_2.clicked.connect(
            self.handle_update_subscription_plan)
        self.window.addGenreBtn.clicked.connect(self.handle_add_genre)

        # --- Analytics Page (Revenue, Plays, Users) ---
        self.window.RevenueViewBtn.clicked.connect(self.handle_view_revenue)
        self.window.PlaysViewBtn.clicked.connect(self.handle_view_plays)
        self.window.UsersViewBtn.clicked.connect(self.handle_view_users)

    def load_all_data(self):
        """Loads data into all tables on the dashboard."""
        self.load_artist_requests_table()
        self.load_users_table()
        self.load_pending_songs_table()
        self.load_reported_songs_table()
        self.load_subscription_plans_table()
        self.load_genre_table()

    # --- Helper to convert string to QDate ---
    def string_to_qdate(self, date_str: str) -> QtCore.QDate:
        """Converts a 'YYYY-MM-DD' string to a QDate object."""
        return QtCore.QDate.fromString(date_str, "yyyy-MM-dd")

    def qdate_to_string(self, qdate: QtCore.QDate) -> str:
        """Converts a QDate object to 'YYYY-MM-DD' string."""
        return qdate.toString("yyyy-MM-dd")

    # --- Analytics Helper Methods ---
    def get_selected_grouping(self, day_radio, month_radio, year_radio) -> str:
        """Returns the selected grouping period."""
        if day_radio.isChecked():
            return "day"
        elif month_radio.isChecked():
            return "month"
        elif year_radio.isChecked():
            return "year"
        return "month"  # Default

    def filter_data_by_date_range(self, data_dict: dict, start_date: str,
                                  end_date: str) -> dict:
        """Filters data dictionary by date range."""
        filtered = {}
        for date_str, value in data_dict.items():
            if start_date <= date_str <= end_date:
                filtered[date_str] = value
        return filtered

    def group_data_by_period(self, data_dict: dict, period: str) -> dict:
        """Groups data by the specified period (day, month, year)."""
        grouped = {}

        for date_str, value in sorted(data_dict.items()):
            if period == "day":
                key = date_str
            elif period == "month":
                key = date_str[:7]  # YYYY-MM
            elif period == "year":
                key = date_str[:4]  # YYYY
            else:
                key = date_str

            if key in grouped:
                grouped[key] += value
            else:
                grouped[key] = value

        return grouped

    def filter_users_by_date_range(self, users_dict: dict, start_date: str,
                                   end_date: str) -> dict:
        """Filters users by their join date within the specified range."""
        filtered = {}
        for username, data in users_dict.items():
            join_date = data[7]  # date_joined is at index 7
            if start_date <= join_date <= end_date:
                filtered[username] = data
        return filtered

    def count_users_by_period(self, users_dict: dict, period: str) -> dict:
        """Counts users grouped by the specified period."""
        counts = {}

        for username, data in users_dict.items():
            date_str = data[7]  # date_joined

            if period == "day":
                key = date_str
            elif period == "month":
                key = date_str[:7]  # YYYY-MM
            elif period == "year":
                key = date_str[:4]  # YYYY
            else:
                key = date_str

            if key in counts:
                counts[key] += 1
            else:
                counts[key] = 1

        return dict(sorted(counts.items()))

    # --- Analytics Handlers ---
    def handle_view_revenue(self):
        """Handles the 'View Revenue' button click."""
        # Get date range
        start_date = self.qdate_to_string(self.window.ReveueStartDate.date())
        end_date = self.qdate_to_string(self.window.ReveueEndDate.date())

        # Validate date range
        if start_date > end_date:
            QtWidgets.QMessageBox.warning(
                self.window, "Invalid Date Range",
                "Start date must be before or equal to end date.")
            return

        # Get grouping period
        period = self.get_selected_grouping(self.window.RevenueDay,
                                            self.window.RevenueMonth,
                                            self.window.RevenueYear)

        # Filter and group data
        filtered_data = self.filter_data_by_date_range(RevenueData, start_date,
                                                       end_date)

        if not filtered_data:
            QtWidgets.QMessageBox.information(
                self.window, "No Data",
                "No revenue data found for the selected date range.")
            return

        grouped_data = self.group_data_by_period(filtered_data, period)

        # Prepare data for plotting
        x_data = list(grouped_data.keys())
        y_data = list(grouped_data.values())

        # Show graph dialog
        dialog = AnalyticsGraphDialog(
            self.window,
            f"Revenue Analysis (Grouped by {period. capitalize()})",
            x_data,
            y_data,
            "Date" if period == "day" else period.capitalize(),
            "Revenue ($)",
            graph_type="line")
        dialog.exec_()

    def handle_view_plays(self):
        """Handles the 'View Plays' button click."""
        # Get date range
        start_date = self.qdate_to_string(self.window.PlaysStartDate.date())
        end_date = self.qdate_to_string(self.window.PlaysEndDate.date())

        # Validate date range
        if start_date > end_date:
            QtWidgets.QMessageBox.warning(
                self.window, "Invalid Date Range",
                "Start date must be before or equal to end date.")
            return

        # Get grouping period
        period = self.get_selected_grouping(self.window.PlaysDay,
                                            self.window.PlaysMonth,
                                            self.window.PlaysYear)

        # Filter and group data
        filtered_data = self.filter_data_by_date_range(PlaysData, start_date,
                                                       end_date)

        if not filtered_data:
            QtWidgets.QMessageBox.information(
                self.window, "No Data",
                "No plays data found for the selected date range.")
            return

        grouped_data = self.group_data_by_period(filtered_data, period)

        # Prepare data for plotting
        x_data = list(grouped_data.keys())
        y_data = list(grouped_data.values())

        # Show graph dialog
        dialog = AnalyticsGraphDialog(
            self.window,
            f"Plays Analysis (Grouped by {period. capitalize()})",
            x_data,
            y_data,
            "Date" if period == "day" else period.capitalize(),
            "Total Plays",
            graph_type="line")
        dialog.exec_()

    def handle_view_users(self):
        """Handles the 'View Users' button click."""
        # Get date range
        start_date = self.qdate_to_string(self.window.UsersStartDate.date())
        end_date = self.qdate_to_string(self.window.UsersEndDate.date())

        # Validate date range
        if start_date > end_date:
            QtWidgets.QMessageBox.warning(
                self.window, "Invalid Date Range",
                "Start date must be before or equal to end date.")
            return

        # Get grouping period
        period = self.get_selected_grouping(self.window.UsersDay,
                                            self.window.UsersMonth,
                                            self.window.UsersYear)

        # Filter users by date range
        filtered_users = self.filter_users_by_date_range(
            Users, start_date, end_date)

        if not filtered_users:
            QtWidgets.QMessageBox.information(
                self.window, "No Data",
                "No users joined during the selected date range.")
            return

        # Count users by period
        user_counts = self.count_users_by_period(filtered_users, period)

        # Prepare data for plotting
        x_data = list(user_counts.keys())
        y_data = list(user_counts.values())

        # Show graph dialog
        dialog = AnalyticsGraphDialog(
            self.window,
            f"New Users Analysis (Grouped by {period.capitalize()})",
            x_data,
            y_data,
            "Date" if period == "day" else period.capitalize(),
            "New Users",
            graph_type="bar")
        dialog.exec_()

    # 1.  ARTIST REQUESTS

    def load_artist_requests_table(self, data_source=None):
        """Populates the Pending Artist Requests table."""
        requests = data_source if data_source is not None else get_pending_requests()
        table = self.window.artistsRequestTable
        table.setRowCount(len(requests))

        for row, (username, data) in enumerate(requests.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row + 1)))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(username))
            table.setItem(row, 2,
                          QtWidgets.QTableWidgetItem(data[0]))  # Full Name
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(data[1]))  # Email
            table.setItem(row, 4,
                          QtWidgets.QTableWidgetItem(data[2]))  # Subscription

        table.resizeColumnsToContents()

    def populate_artist_request_form(self, row, column):
        """Fills the form with data from the clicked row in the artist requests table."""
        table = self.window.artistsRequestTable
        username = table.item(row, 1).text()
        request_data = get_pending_requests().get(username)

        if request_data:
            self.window.UsernameLineEdit_2.setText(username)
            self.window.FullNameLineEdit_2.setText(
                request_data[0])  # Full Name
            self.window.EmailLineEdit_2.setText(request_data[1])  # Email
            self.window.SubscriptionLineEdit_2.setText(
                request_data[2])  # Subscription
            self.window.dateJoined_2.setDate(
                self.string_to_qdate(request_data[3]))  # Date Joined

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
            QtWidgets.QMessageBox.warning(
                self.window, "No User Selected",
                "Please select an artist request from the table.")
            return

        if accept_artist_request(username):
            QtWidgets.QMessageBox.information(
                self.window, "Success",
                f"Artist request for '{username}' has been accepted.")
            self.load_artist_requests_table()  # Refresh table
            self.clear_artist_request_form()  # Clear form
        else:
            QtWidgets.QMessageBox.critical(
                self.window, "Error",
                f"Could not find or accept request for '{username}'.")

    def handle_reject_artist_request(self):
        """Handles the 'Reject' button click for an artist request."""
        username = self.window.UsernameLineEdit_2.text()
        if not username:
            QtWidgets.QMessageBox.warning(
                self.window, "No User Selected",
                "Please select an artist request from the table.")
            return

        if reject_artist_request(username):
            QtWidgets.QMessageBox.information(
                self.window, "Success",
                f"Artist request for '{username}' has been rejected.")
            self.load_artist_requests_table()  # Refresh table
            self.clear_artist_request_form()  # Clear form
        else:
            QtWidgets.QMessageBox.critical(
                self.window, "Error",
                f"Could not find or reject request for '{username}'.")

    # 2. USERS MANAGEMENT

    def load_users_table(self, data_source=None):
        """Populates the Users Management table."""
        users = data_source if data_source is not None else get_all_users(
        )  # <-- MODIFY THIS
        table = self.window.tableWidget
        table.setRowCount(len(users))

        for row, (username, data) in enumerate(users.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(username))
            table.setItem(row, 1,
                          QtWidgets.QTableWidgetItem(data[0]))  # Full Name
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(data[2]))  # Email
            table.setItem(row, 3,
                          QtWidgets.QTableWidgetItem(data[7]))  # Date Joined
            table.setItem(row, 4,
                          QtWidgets.QTableWidgetItem(data[4]))  # UserType

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
            QtWidgets.QMessageBox.warning(
                self.window, "No User Selected",
                "Please select a user from the table to delete.")
            return

        reply = QtWidgets.QMessageBox.question(
            self.window, "Confirm Deletion",
            f"Are you sure you want to delete the user '{username}'?  This action cannot be undone.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            if remove_user(username):
                QtWidgets.QMessageBox.information(
                    self.window, "Success",
                    f"User '{username}' has been deleted.")
                self.load_users_table()  # Refresh table
                self.clear_user_form()  # Clear form
            else:
                QtWidgets.QMessageBox.critical(
                    self.window, "Error",
                    f"Could not find or delete user '{username}'.")

    # 3. PENDING SONGS

    def load_pending_songs_table(self, data_source=None):
        """Populates the Songs Pending Approval table."""
        songs = data_source if data_source is not None else get_pending_songs(
        )  # <-- MODIFY THIS
        table = self.window.pendingSongsTable
        table.setRowCount(len(songs))

        for row, (song_id, data) in enumerate(songs.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(song_id))
            table.setItem(row, 1,
                          QtWidgets.QTableWidgetItem(data[0]))  # Song Name
            table.setItem(row, 2,
                          QtWidgets.QTableWidgetItem(data[1]))  # Artist Name
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(data[2]))  # Genre
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(
                data[3]))  # Submission Date

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
            self.window.submissionDate.setDate(
                self.string_to_qdate(song_data[3]))

            # Load song image
            image_path = song_data[5]
            pixmap = QtGui.QPixmap(image_path)
            if pixmap.isNull():
                # Set a default image if path is invalid or image not found
                self.window.songImage.setPixmap(
                    QtGui.QPixmap("Song_images/default_song_image.jpg"))
            else:
                self.window.songImage.setPixmap(pixmap)

    def clear_pending_song_form(self):
        """Clears all fields in the pending song detail form."""
        self.window.PendingsongID.clear()
        self.window.PendingSongName.clear()
        self.window.ArtistName.clear()
        self.window.genreLineEdit.clear()
        self.window.submissionDate.setDate(QtCore.QDate.currentDate())
        self.window.songImage.setPixmap(
            QtGui.QPixmap("Song_images/default_song_image.jpg"))

    def handle_view_song(self):
        """Handles the 'Play Song' button click."""
        song_id = self.window.PendingsongID.text()
        if not song_id:
            QtWidgets.QMessageBox.warning(
                self.window, "No Song Selected",
                "Please select a song from the table to play.")
            return

        song_data = get_pending_songs().get(song_id)
        if song_data:
            song_name = song_data[0]
            song_path = song_data[4]
            # This just shows a popup.  Real playback would need a media library.
            QtWidgets.QMessageBox.information(
                self.window, "Playing Song",
                f"Simulating playback of: {song_name}\n(from {song_path})")

    def handle_approve_song(self):
        """Handles the 'Accept' button click for a pending song."""
        song_id = self.window.PendingsongID.text()
        if not song_id:
            QtWidgets.QMessageBox.warning(
                self.window, "No Song Selected",
                "Please select a song from the table to approve.")
            return

        if approve_song(song_id):
            QtWidgets.QMessageBox.information(
                self.window, "Success",
                f"Song has been approved and added to the library.")
            self.load_pending_songs_table()  # Refresh table
            self.clear_pending_song_form()  # Clear form
        else:
            QtWidgets.QMessageBox.critical(
                self.window, "Error",
                f"Could not find or approve song with ID '{song_id}'.")

    def handle_reject_song(self):
        """Handles the 'Reject' button click for a pending song."""
        song_id = self.window.PendingsongID.text()
        if not song_id:
            QtWidgets.QMessageBox.warning(
                self.window, "No Song Selected",
                "Please select a song from the table to reject.")
            return

        if reject_song(song_id):
            QtWidgets.QMessageBox.information(self.window, "Success",
                                              f"Song has been rejected.")
            self.load_pending_songs_table()  # Refresh table
            self.clear_pending_song_form()  # Clear form
        else:
            QtWidgets.QMessageBox.critical(
                self.window, "Error",
                f"Could not find or reject song with ID '{song_id}'.")

    # 4. REPORTED SONGS

    def load_reported_songs_table(self, data_source=None):
        """Populates the Reported Songs table."""
        reports = data_source if data_source is not None else get_reported_songs(
        )  # <-- MODIFY THIS
        table = self.window.reportedSongsTable
        table.setRowCount(len(reports))

        for row, (report_id, data) in enumerate(reports.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(report_id))
            table.setItem(row, 1,
                          QtWidgets.QTableWidgetItem(data[1]))  # Song Name
            table.setItem(row, 2,
                          QtWidgets.QTableWidgetItem(data[2]))  # Artist Name
            table.setItem(row, 3,
                          QtWidgets.QTableWidgetItem(data[3]))  # Reported By
            table.setItem(row, 4,
                          QtWidgets.QTableWidgetItem(data[4]))  # Reason

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
            self.window.Reports_Dislikes_2.setText(str(
                report_data[8]))  # Total Reports
            self.window.Reports_UploadDate.setDate(
                self.string_to_qdate(report_data[9]))

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
            QtWidgets.QMessageBox.warning(
                self.window, "No Song Selected",
                "Please select a reported song from the table to delete.")
            return

        reply = QtWidgets.QMessageBox.question(
            self.window, "Confirm Deletion",
            f"Are you sure you want to permanently delete the song with ID '{song_id}'? This action cannot be undone.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            if delete_reported_song(song_id):
                QtWidgets.QMessageBox.information(
                    self.window, "Success",
                    f"Song '{song_id}' has been deleted from the system.")
                self.load_reported_songs_table()  # Refresh table
                self.clear_reported_song_form()  # Clear form
            else:
                QtWidgets.QMessageBox.critical(
                    self.window, "Error",
                    f"Could not find or delete song with ID '{song_id}'.")

    # 5. SUBSCRIPTION PLANS

    def load_subscription_plans_table(self):
        """Populates the Subscription Plans table on the Analytics page."""
        plans = get_subscription_plans()
        table = self.window.tableWidget_2
        table.setRowCount(len(plans))

        for row, (plan_id, data) in enumerate(plans.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(plan_id))
            table.setItem(row, 1,
                          QtWidgets.QTableWidgetItem(data[0]))  # Plan Name
            table.setItem(row, 2,
                          QtWidgets.QTableWidgetItem(str(data[1])))  # Price
            table.setItem(row, 3,
                          QtWidgets.QTableWidgetItem(data[2]))  # Duration
            table.setItem(row, 4,
                          QtWidgets.QTableWidgetItem(data[3]))  # Features

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
            QtWidgets.QMessageBox.warning(self.window, "Invalid Input",
                                          "Price must be a valid number.")
            return

        plan_duration = self.window.PlanDuration.text()
        plan_features = self.window.PlanFeatures.text()

        if not all([plan_name, plan_duration, plan_features]):
            QtWidgets.QMessageBox.warning(self.window, "Missing Information",
                                          "Please fill out all plan fields.")
            return

        plan_data = [plan_name, plan_price, plan_duration, plan_features]
        add_subscription_plan(plan_id, plan_data)

        QtWidgets.QMessageBox.information(
            self.window, "Success",
            f"New plan '{plan_name}' added with ID '{plan_id}'.")
        self.load_subscription_plans_table()
        self.clear_subscription_plan_form()

    def handle_update_subscription_plan(self):
        """Handles updating an existing subscription plan."""
        if not hasattr(self.window, "current_plan_id"):
            QtWidgets.QMessageBox.warning(
                self.window, "No Plan Selected",
                "Please select a plan from the table to update.")
            return

        plan_id = self.window.current_plan_id
        plan_name = self.window.PlanName.text()
        try:
            plan_price = float(self.window.PlanPrice.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self.window, "Invalid Input",
                                          "Price must be a valid number.")
            return

        plan_duration = self.window.PlanDuration.text()
        plan_features = self.window.PlanFeatures.text()

        if not all([plan_name, plan_duration, plan_features]):
            QtWidgets.QMessageBox.warning(self.window, "Missing Information",
                                          "Please fill out all plan fields.")
            return

        plan_data = [plan_name, plan_price, plan_duration, plan_features]

        if update_subscription_plan(plan_id, plan_data):
            QtWidgets.QMessageBox.information(
                self.window, "Success",
                f"Plan '{plan_name}' (ID: {plan_id}) has been updated.")
            self.load_subscription_plans_table()
            self.clear_subscription_plan_form()
        else:
            QtWidgets.QMessageBox.critical(
                self.window, "Error",
                f"Could not find or update plan with ID '{plan_id}'.")

    # 6. SEARCH HANDLERS (NEW SECTION)

    def handle_search_artist_requests(self):
        """Filters the artist requests table based on the search input."""
        search_term = self.window.pendingArtistSearch.text().lower()

        # If search term is empty, reload all data
        if not search_term:
            self.load_artist_requests_table()
            return

        all_requests = get_pending_requests()
        # Search by username or full name
        filtered_requests = {
            username: data
            for username, data in all_requests.items()
            if search_term in username.lower()
            or search_term in data[0].lower()  # data[0] is Full Name
        }

        self.load_artist_requests_table(filtered_requests)

    def handle_search_users(self):
        """Filters the users table based on the search input."""
        search_term = self.window.searchUserInput.text().lower()

        if not search_term:
            self.load_users_table()
            return

        all_users = get_all_users()
        # Search by username or full name
        filtered_users = {
            username: data
            for username, data in all_users.items()
            if search_term in username.lower()
            or search_term in data[0].lower()  # data[0] is Full Name
        }

        self.load_users_table(filtered_users)

    def handle_search_pending_songs(self):
        """Filters the pending songs table based on the search input."""
        search_term = self.window.pendingSongSearch.text().lower()

        if not search_term:
            self.load_pending_songs_table()
            return

        all_songs = get_pending_songs()
        # Search by song name or artist name
        filtered_songs = {
            song_id: data
            for song_id, data in all_songs.items()
            if search_term in data[0].lower() or search_term in
            data[1].lower()  # data[0] is Song Name, data[1] is Artist Name
        }

        self.load_pending_songs_table(filtered_songs)

    def handle_search_reports(self):
        """Filters the reported songs table based on the search input."""
        search_term = self.window.searchReportInput.text().lower()

        if not search_term:
            self.load_reported_songs_table()
            return

        all_reports = get_reported_songs()
        # Search by song name or artist name
        filtered_reports = {
            report_id: data
            for report_id, data in all_reports.items()
            if search_term in data[1].lower() or search_term in
            data[2].lower()  # data[1] is Song Name, data[2] is Artist Name
        }

        self.load_reported_songs_table(filtered_reports)

    def load_genre_table(self):

        genres = get_all_genres()
        table = self.window.tableWidget_3  # your QTableWidget for genres
        table.setRowCount(len(genres))

        for row, (genre_id, data) in enumerate(genres.items()):

            table.setItem(row, 0, QtWidgets.QTableWidgetItem(genre_id))
            table.setItem(row, 1,
                          QtWidgets.QTableWidgetItem(data[0]))  # Genre Name
            table.setItem(row, 2,
                          QtWidgets.QTableWidgetItem(data[1]))  # Description
        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)

    def populate_genre_form(self, row, column):

        table = self.window.tableWidget_3

        self.window.current_genre_id = table.item(row, 0).text()

        genre_data = get_all_genres().get(self.window.current_genre_id)

        if genre_data:

            self.window.genreNameLineEdit.setText(genre_data[0])

            self.window.genreDescriptionLineEdit.setText(genre_data[1])

    def clear_genre_form(self):

        self.window.genreNameLineEdit.clear()

        self.window.genreDescriptionLineEdit.clear()

        if hasattr(self.window, "current_genre_id"):

            del self.window.current_genre_id

    def handle_add_genre(self):

        genre_id = f"GN{len(get_all_genres()) + 1:03d}"

        genre_name = self.window.genreNameLineEdit.text()

        description = self.window.genreDescriptionLineEdit.text()

        if not genre_name or not description:

            QtWidgets.QMessageBox.warning(self.window, "Missing Information",
                                          "Please fill out all genre fields.")

            return

        genre_data = [genre_name, description]

        add_genre(genre_id, genre_data)

        QtWidgets.QMessageBox.information(
            self.window, "Success",
            f"New genre '{genre_name}' added with ID '{genre_id}'.")

        self.load_genre_table()

        self.clear_genre_form()
