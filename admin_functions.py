import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from data import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class AnalyticsGraphDialog(QtWidgets.QDialog):
    """Dialog window to display analytics graphs."""

    def __init__(self,
                 parent,
                 title,
                 data,
                 x_label,
                 y_label,
                 graph_type="line"):
        """
        Args:
            parent: Parent widget
            title: Graph title
            data: 2D array [[x, y], [x, y], ...]
            x_label: Label for x-axis
            y_label: Label for y-axis
            graph_type: 'line' or 'bar'
        """
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(800, 600)

        layout = QtWidgets.QVBoxLayout(self)

        self.canvas = FigureCanvas(Figure(figsize=(8, 5)))
        layout.addWidget(self.canvas)

        self.ax = self.canvas.figure.add_subplot(111)
        self.plot_graph(data, x_label, y_label, title, graph_type)

        close_btn = QtWidgets.QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def plot_graph(self, data, x_label, y_label, title, graph_type):
        self.ax.clear()

        if not data:
            self.ax.text(0.5,
                         0.5,
                         'No data available',
                         ha='center',
                         va='center',
                         fontsize=16)
            self.canvas.draw()
            return

        x_data = [item[0] for item in data]
        y_data = [item[1] for item in data]

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

        if len(x_data) > 5:
            self.ax.tick_params(axis='x', rotation=45)

        self.canvas.figure.tight_layout()
        self.canvas.draw()


class AdminDashboardHandler:
    """Handles all logic for the Admin Dashboard."""

    def __init__(self, window: QtWidgets.QMainWindow):
        self.window = window

    def connect_signals(self):
        """Connects all UI signals to their handler methods."""
        # Artist Requests Page
        self.window.artistsRequestTable.cellClicked.connect(
            self.populate_artist_request_form)
        self.window.RequestS_AcceptBtn.clicked.connect(
            self.handle_accept_artist_request)
        self.window.Requests_RejectBtn.clicked.connect(
            self.handle_reject_artist_request)
        self.window.pushButton.clicked.connect(
            self.handle_search_artist_requests)

        # Users Management Page
        self.window.tableWidget.cellClicked.connect(self.populate_user_form)
        self.window.deleteUserBtn.clicked.connect(self.handle_delete_user)
        self.window.searchUserBtn.clicked.connect(self.handle_search_users)

        # Pending Songs Page
        self.window.pendingSongsTable.cellClicked.connect(
            self.populate_pending_song_form)
        self.window.playSongBtn.clicked.connect(self.handle_view_song)
        self.window.acceptSongBtn.clicked.connect(self.handle_approve_song)
        self.window.rejectSongBtn.clicked.connect(self.handle_reject_song)
        self.window.pendingSongBtn.clicked.connect(
            self.handle_search_pending_songs)

        # Reports Page
        self.window.reportedSongsTable.cellClicked.connect(
            self.populate_reported_song_form)
        self.window.DeleteSongBtn.clicked.connect(
            self.handle_delete_reported_song)
        self.window.searchReportBtn.clicked.connect(self.handle_search_reports)

        # Analytics Page (Subscriptions & Genres)
        self.window.tableWidget_2.cellClicked.connect(
            self.populate_subscription_plan_form)
        self.window.AddPlanBtn.clicked.connect(
            self.handle_add_subscription_plan)
        self.window.AddPlanBtn_2.clicked.connect(
            self.handle_update_subscription_plan)
        self.window.addGenreBtn.clicked.connect(self.handle_add_genre)

        # Analytics Page (Graphs)
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

    # ==================== UTILITY METHODS ====================

    def string_to_qdate(self, date_str: str) -> QtCore.QDate:
        return QtCore.QDate.fromString(date_str, "yyyy-MM-dd")

    def qdate_to_string(self, qdate: QtCore.QDate) -> str:
        return qdate.toString("yyyy-MM-dd")

    def get_selected_grouping(self, day_radio, month_radio, year_radio) -> str:
        if day_radio.isChecked():
            return "day"
        elif month_radio.isChecked():
            return "month"
        elif year_radio.isChecked():
            return "year"
        return "month"

    def get_analytics_data(self, raw_data: dict, start_date: str,
                           end_date: str, period: str) -> list:
        """
        Filters and groups analytics data, returns 2D array [[x, y], ...]
        
        Args:
            raw_data: Dictionary {date_string: value}
            start_date: Start date string (YYYY-MM-DD)
            end_date: End date string (YYYY-MM-DD)
            period: 'day', 'month', or 'year'
        
        Returns:
            List of [x, y] pairs
        """
        # Filter by date range
        filtered = {
            k: v
            for k, v in raw_data.items() if start_date <= k <= end_date
        }

        if not filtered:
            return []

        # Group by period
        grouped = {}
        for date_str, value in sorted(filtered.items()):
            if period == "day":
                key = date_str
            elif period == "month":
                key = date_str[:7]
            elif period == "year":
                key = date_str[:4]
            else:
                key = date_str

            grouped[key] = grouped.get(key, 0) + value

        return [[k, v] for k, v in sorted(grouped.items())]

    def get_user_count_data(self, start_date: str, end_date: str,
                            period: str) -> list:
        """
        Counts users by join date, returns 2D array [[x, y], ...]
        """
        users = get_all_users()
        counts = {}

        for username, data in users.items():
            join_date = data[7]
            if not (start_date <= join_date <= end_date):
                continue

            if period == "day":
                key = join_date
            elif period == "month":
                key = join_date[:7]
            elif period == "year":
                key = join_date[:4]
            else:
                key = join_date

            counts[key] = counts.get(key, 0) + 1

        return [[k, v] for k, v in sorted(counts.items())]

    # ==================== ANALYTICS HANDLERS ====================

    def handle_view_revenue(self):
        start_date = self.qdate_to_string(self.window.ReveueStartDate.date())
        end_date = self.qdate_to_string(self.window.ReveueEndDate.date())

        if start_date > end_date:
            QtWidgets.QMessageBox.warning(
                self.window, "Invalid Date Range",
                "Start date must be before or equal to end date.")
            return

        period = self.get_selected_grouping(self.window.RevenueDay,
                                            self.window.RevenueMonth,
                                            self.window.RevenueYear)

        data = self.get_analytics_data(RevenueData, start_date, end_date,
                                       period)

        if not data:
            QtWidgets.QMessageBox.information(
                self.window, "No Data",
                "No revenue data found for the selected date range.")
            return

        dialog = AnalyticsGraphDialog(
            self.window,
            f"Revenue Analysis (Grouped by {period. capitalize()})",
            data,
            period.capitalize() if period != "day" else "Date",
            "Revenue ($)",
            graph_type="line")
        dialog.exec_()

    def handle_view_plays(self):
        start_date = self.qdate_to_string(self.window.PlaysStartDate.date())
        end_date = self.qdate_to_string(self.window.PlaysEndDate.date())

        if start_date > end_date:
            QtWidgets.QMessageBox.warning(
                self.window, "Invalid Date Range",
                "Start date must be before or equal to end date.")
            return

        period = self.get_selected_grouping(self.window.PlaysDay,
                                            self.window.PlaysMonth,
                                            self.window.PlaysYear)

        data = self.get_analytics_data(PlaysData, start_date, end_date, period)

        if not data:
            QtWidgets.QMessageBox.information(
                self.window, "No Data",
                "No plays data found for the selected date range.")
            return

        dialog = AnalyticsGraphDialog(
            self.window,
            f"Plays Analysis (Grouped by {period. capitalize()})",
            data,
            period.capitalize() if period != "day" else "Date",
            "Total Plays",
            graph_type="line")
        dialog.exec_()

    def handle_view_users(self):
        start_date = self.qdate_to_string(self.window.UsersStartDate.date())
        end_date = self.qdate_to_string(self.window.UsersEndDate.date())

        if start_date > end_date:
            QtWidgets.QMessageBox.warning(
                self.window, "Invalid Date Range",
                "Start date must be before or equal to end date.")
            return

        period = self.get_selected_grouping(self.window.UsersDay,
                                            self.window.UsersMonth,
                                            self.window.UsersYear)

        data = self.get_user_count_data(start_date, end_date, period)

        if not data:
            QtWidgets.QMessageBox.information(
                self.window, "No Data",
                "No users joined during the selected date range.")
            return

        dialog = AnalyticsGraphDialog(
            self.window,
            f"New Users Analysis (Grouped by {period.capitalize()})",
            data,
            period.capitalize() if period != "day" else "Date",
            "New Users",
            graph_type="bar")
        dialog.exec_()

    # ==================== ARTIST REQUESTS ====================

    def load_artist_requests_table(self, data_source=None):
        requests = data_source if data_source is not None else get_pending_requests(
        )
        table = self.window.artistsRequestTable
        table.setRowCount(len(requests))

        for row, (username, data) in enumerate(requests.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row + 1)))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(username))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(data[0]))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(data[1]))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(data[2]))

        table.resizeColumnsToContents()

    def populate_artist_request_form(self, row, column):
        table = self.window.artistsRequestTable
        username = table.item(row, 1).text()
        request_data = get_pending_requests().get(username)

        if request_data:
            self.window.UsernameLineEdit_2.setText(username)
            self.window.FullNameLineEdit_2.setText(request_data[0])
            self.window.EmailLineEdit_2.setText(request_data[1])
            self.window.SubscriptionLineEdit_2.setText(request_data[2])
            self.window.dateJoined_2.setDate(
                self.string_to_qdate(request_data[3]))

    def clear_artist_request_form(self):
        self.window.UsernameLineEdit_2.clear()
        self.window.FullNameLineEdit_2.clear()
        self.window.EmailLineEdit_2.clear()
        self.window.SubscriptionLineEdit_2.clear()
        self.window.dateJoined_2.setDate(QtCore.QDate.currentDate())

    def handle_accept_artist_request(self):
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
            self.load_artist_requests_table()
            self.clear_artist_request_form()
        else:
            QtWidgets.QMessageBox.critical(
                self.window, "Error",
                f"Could not accept request for '{username}'.")

    def handle_reject_artist_request(self):
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
            self.load_artist_requests_table()
            self.clear_artist_request_form()
        else:
            QtWidgets.QMessageBox.critical(
                self.window, "Error",
                f"Could not reject request for '{username}'.")

    def handle_search_artist_requests(self):
        search_term = self.window.pendingArtistSearch.text().lower()

        if not search_term:
            self.load_artist_requests_table()
            return

        all_requests = get_pending_requests()
        filtered = {
            u: d
            for u, d in all_requests.items()
            if search_term in u.lower() or search_term in d[0].lower()
        }
        self.load_artist_requests_table(filtered)

    # ==================== USERS MANAGEMENT ====================

    def load_users_table(self, data_source=None):
        users = data_source if data_source is not None else get_all_users()
        table = self.window.tableWidget
        table.setRowCount(len(users))

        for row, (username, data) in enumerate(users.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(username))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(data[0]))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(data[2]))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(data[7]))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(data[4]))

        table.resizeColumnsToContents()

    def populate_user_form(self, row, column):
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
        self.window.UsernameLineEdit.clear()
        self.window.FullNameLineEdit.clear()
        self.window.EmailLineEdit.clear()
        self.window.dateJoined.setDate(QtCore.QDate.currentDate())
        self.window.UserTypeLineEdit.clear()
        self.window.SubscriptionLineEdit.clear()
        self.window.RevenueLineEdit.clear()

    def handle_delete_user(self):
        username = self.window.UsernameLineEdit.text()
        if not username:
            QtWidgets.QMessageBox.warning(
                self.window, "No User Selected",
                "Please select a user from the table to delete.")
            return

        reply = QtWidgets.QMessageBox.question(
            self.window, "Confirm Deletion",
            f"Are you sure you want to delete '{username}'?  This cannot be undone.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            if remove_user(username):
                QtWidgets.QMessageBox.information(
                    self.window, "Success",
                    f"User '{username}' has been deleted.")
                self.load_users_table()
                self.clear_user_form()
            else:
                QtWidgets.QMessageBox.critical(
                    self.window, "Error",
                    f"Could not delete user '{username}'.")

    def handle_search_users(self):
        search_term = self.window.searchUserInput.text().lower()

        if not search_term:
            self.load_users_table()
            return

        all_users = get_all_users()
        filtered = {
            u: d
            for u, d in all_users.items()
            if search_term in u.lower() or search_term in d[0].lower()
        }
        self.load_users_table(filtered)

    # ==================== PENDING SONGS ====================

    def load_pending_songs_table(self, data_source=None):
        songs = data_source if data_source is not None else get_pending_songs()
        table = self.window.pendingSongsTable
        table.setRowCount(len(songs))

        for row, (song_id, data) in enumerate(songs.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(song_id))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(data[0]))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(data[1]))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(data[2]))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(data[3]))

        table.resizeColumnsToContents()

    def populate_pending_song_form(self, row, column):
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

            pixmap = QtGui.QPixmap(song_data[5])
            if pixmap.isNull():
                pixmap = QtGui.QPixmap("Song_images/default_song_image.jpg")
            self.window.songImage.setPixmap(pixmap)

    def clear_pending_song_form(self):
        self.window.PendingsongID.clear()
        self.window.PendingSongName.clear()
        self.window.ArtistName.clear()
        self.window.genreLineEdit.clear()
        self.window.submissionDate.setDate(QtCore.QDate.currentDate())
        self.window.songImage.setPixmap(
            QtGui.QPixmap("Song_images/default_song_image.jpg"))

    def handle_view_song(self):
        song_id = self.window.PendingsongID.text()
        if not song_id:
            QtWidgets.QMessageBox.warning(
                self.window, "No Song Selected",
                "Please select a song from the table.")
            return

        song_data = get_pending_songs().get(song_id)
        if song_data:
            QtWidgets.QMessageBox.information(
                self.window, "Playing Song",
                f"Simulating playback of:  {song_data[0]}\n(from {song_data[4]})"
            )

    def handle_approve_song(self):
        song_id = self.window.PendingsongID.text()
        if not song_id:
            QtWidgets.QMessageBox.warning(self.window, "No Song Selected",
                                          "Please select a song to approve.")
            return

        if approve_song(song_id):
            QtWidgets.QMessageBox.information(self.window, "Success",
                                              "Song has been approved.")
            self.load_pending_songs_table()
            self.clear_pending_song_form()
        else:
            QtWidgets.QMessageBox.critical(
                self.window, "Error", f"Could not approve song '{song_id}'.")

    def handle_reject_song(self):
        song_id = self.window.PendingsongID.text()
        if not song_id:
            QtWidgets.QMessageBox.warning(self.window, "No Song Selected",
                                          "Please select a song to reject.")
            return

        if reject_song(song_id):
            QtWidgets.QMessageBox.information(self.window, "Success",
                                              "Song has been rejected.")
            self.load_pending_songs_table()
            self.clear_pending_song_form()
        else:
            QtWidgets.QMessageBox.critical(
                self.window, "Error", f"Could not reject song '{song_id}'.")

    def handle_search_pending_songs(self):
        search_term = self.window.pendingSongSearch.text().lower()

        if not search_term:
            self.load_pending_songs_table()
            return

        all_songs = get_pending_songs()
        filtered = {
            sid: d
            for sid, d in all_songs.items()
            if search_term in d[0].lower() or search_term in d[1].lower()
        }
        self.load_pending_songs_table(filtered)

    # ==================== REPORTED SONGS ====================

    def load_reported_songs_table(self, data_source=None):
        reports = data_source if data_source is not None else get_reported_songs(
        )
        table = self.window.reportedSongsTable
        table.setRowCount(len(reports))

        for row, (report_id, data) in enumerate(reports.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(report_id))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(data[1]))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(data[2]))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(data[3]))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(data[4]))

        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)

    def populate_reported_song_form(self, row, column):
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
            self.window.Reports_Dislikes_2.setText(str(report_data[8]))
            self.window.Reports_UploadDate.setDate(
                self.string_to_qdate(report_data[9]))

    def clear_reported_song_form(self):
        self.window.Reports_SongID.clear()
        self.window.Reports_SongName.clear()
        self.window.Reports_ArtistName.clear()
        self.window.Reports_Genre.clear()
        self.window.Reports_Likes.clear()
        self.window.Reports_Dislikes.clear()
        self.window.Reports_Dislikes_2.clear()
        self.window.Reports_UploadDate.setDate(QtCore.QDate.currentDate())

    def handle_delete_reported_song(self):
        song_id = self.window.Reports_SongID.text()
        if not song_id:
            QtWidgets.QMessageBox.warning(
                self.window, "No Song Selected",
                "Please select a reported song to delete.")
            return

        reply = QtWidgets.QMessageBox.question(
            self.window, "Confirm Deletion",
            f"Permanently delete song '{song_id}'? This cannot be undone.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            if delete_reported_song(song_id):
                QtWidgets.QMessageBox.information(
                    self.window, "Success",
                    f"Song '{song_id}' has been deleted.")
                self.load_reported_songs_table()
                self.clear_reported_song_form()
            else:
                QtWidgets.QMessageBox.critical(
                    self.window, "Error",
                    f"Could not delete song '{song_id}'.")

    def handle_search_reports(self):
        search_term = self.window.searchReportInput.text().lower()

        if not search_term:
            self.load_reported_songs_table()
            return

        all_reports = get_reported_songs()
        filtered = {
            rid: d
            for rid, d in all_reports.items()
            if search_term in d[1].lower() or search_term in d[2].lower()
        }
        self.load_reported_songs_table(filtered)

    # ==================== SUBSCRIPTION PLANS ====================

    def load_subscription_plans_table(self):
        plans = get_subscription_plans()
        table = self.window.tableWidget_2
        table.setRowCount(len(plans))

        for row, (plan_id, data) in enumerate(plans.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(plan_id))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(data[0]))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data[1])))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(data[2]))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(data[3]))

        table.resizeColumnsToContents()

    def populate_subscription_plan_form(self, row, column):
        table = self.window.tableWidget_2
        self.window.current_plan_id = table.item(row, 0).text()
        plan_data = get_subscription_plans().get(self.window.current_plan_id)

        if plan_data:
            self.window.PlanName.setText(plan_data[0])
            self.window.PlanPrice.setText(str(plan_data[1]))
            self.window.PlanDuration.setText(plan_data[2])
            self.window.PlanFeatures.setText(plan_data[3])

    def clear_subscription_plan_form(self):
        self.window.PlanName.clear()
        self.window.PlanPrice.clear()
        self.window.PlanDuration.clear()
        self.window.PlanFeatures.clear()
        if hasattr(self.window, "current_plan_id"):
            del self.window.current_plan_id

    def handle_add_subscription_plan(self):
        plan_id = f"SP{len(get_subscription_plans()) + 1: 03d}"
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

        add_subscription_plan(
            plan_id, [plan_name, plan_price, plan_duration, plan_features])
        QtWidgets.QMessageBox.information(self.window, "Success",
                                          f"New plan '{plan_name}' added.")
        self.load_subscription_plans_table()
        self.clear_subscription_plan_form()

    def handle_update_subscription_plan(self):
        if not hasattr(self.window, "current_plan_id"):
            QtWidgets.QMessageBox.warning(self.window, "No Plan Selected",
                                          "Please select a plan to update.")
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

        if update_subscription_plan(
                plan_id,
            [plan_name, plan_price, plan_duration, plan_features]):
            QtWidgets.QMessageBox.information(self.window, "Success",
                                              f"Plan '{plan_name}' updated.")
            self.load_subscription_plans_table()
            self.clear_subscription_plan_form()
        else:
            QtWidgets.QMessageBox.critical(
                self.window, "Error", f"Could not update plan '{plan_id}'.")

    # ==================== GENRES ====================

    def load_genre_table(self):
        genres = get_all_genres()
        table = self.window.tableWidget_3
        table.setRowCount(len(genres))

        for row, (genre_id, data) in enumerate(genres.items()):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(genre_id))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(data[0]))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(data[1]))

        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)

    def handle_add_genre(self):
        genre_id = f"GN{len(get_all_genres()) + 1:03d}"
        genre_name = self.window.genreNameLineEdit.text()
        description = self.window.genreDescriptionLineEdit.text()

        if not genre_name or not description:
            QtWidgets.QMessageBox.warning(self.window, "Missing Information",
                                          "Please fill out all genre fields.")
            return

        add_genre(genre_id, [genre_name, description])
        QtWidgets.QMessageBox.information(self.window, "Success",
                                          f"New genre '{genre_name}' added.")
        self.load_genre_table()
        self.window.genreNameLineEdit.clear()
        self.window.genreDescriptionLineEdit.clear()
