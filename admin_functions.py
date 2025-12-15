import sys
import pyodbc
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# ==================== DATABASE CONNECTION ====================

server = 'SAROSH-PC\SQLSERVERSEM3'
database = 'HabibifyDatabase'
use_windows_authentication = True
username = 'your_username'
password = 'your_password'


def get_connection():
    if use_windows_authentication:
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    else:
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    return pyodbc.connect(connection_string)


def execute_query(query,
                  params=None,
                  fetch_one=False,
                  fetch_all=True,
                  commit=False):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if commit:
            connection.commit()
            return cursor.rowcount
        elif fetch_one:
            return cursor.fetchone()
        elif fetch_all:
            return cursor.fetchall()
        else:
            return None

    except pyodbc.Error as e:
        print(f"Database error:  {e}")
        if connection:
            connection.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


class AnalyticsGraphDialog(QtWidgets.QDialog):

    def __init__(self,
                 parent,
                 title,
                 data,
                 x_label,
                 y_label,
                 graph_type="line"):
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

        x_data = [str(item[0]) for item in data]
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


# ==================== ADMIN DASHBOARD HANDLER ====================


class AdminDashboardHandler:

    def __init__(self, window: QtWidgets.QMainWindow):
        self.window = window

    def connect_signals(self):
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
        try:
            self.load_artist_requests_table()
            self.load_users_table()
            self.load_pending_songs_table()
            self.load_reported_songs_table()
            self.load_subscription_plans_table()
            self.load_genre_table()
        except Exception as e:
            self.show_error(f"Failed to load data from database:\n{str(e)}")

    # ==================== UTILITY METHODS ====================

    def string_to_qdate(self, date_val) -> QtCore.QDate:
        if date_val is None:
            return QtCore.QDate.currentDate()
        if isinstance(date_val, str):
            return QtCore.QDate.fromString(date_val, "yyyy-MM-dd")
        return QtCore.QDate(date_val.year, date_val.month, date_val.day)

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

    def show_error(self, message):
        QtWidgets.QMessageBox.critical(self.window, "Error", message)

    def show_success(self, message):
        QtWidgets.QMessageBox.information(self.window, "Success", message)

    def show_warning(self, message):
        QtWidgets.QMessageBox.warning(self.window, "Warning", message)

    # ==================== DATABASE QUERIES ====================

    def db_get_all_users(self):
        query = """
            SELECT Username, Password, UserType, EmailAddress, UserStatus, 
                   PhoneNo, FullName, DateJoined
            FROM Users
            WHERE UserStatus != 'Deleted'
            ORDER BY Username
        """
        return execute_query(query)

    def db_get_user(self, username):
        query = """
            SELECT Username, Password, UserType, EmailAddress, UserStatus, 
                   PhoneNo, FullName, DateJoined
            FROM Users 
            WHERE Username = ?
        """
        return execute_query(query, (username, ), fetch_one=True)

    def db_search_users(self, search_term):
        query = """
            SELECT Username, Password, UserType, EmailAddress, UserStatus, 
                   PhoneNo, FullName, DateJoined
            FROM Users
            WHERE (Username LIKE ? OR EmailAddress LIKE ?  OR FullName LIKE ?)
              AND UserStatus != 'Deleted'
            ORDER BY Username
        """
        pattern = f"%{search_term}%"
        return execute_query(query, (pattern, pattern, pattern))

    def db_delete_user(self, username):
        query = "UPDATE Users SET UserStatus = 'Deleted' WHERE Username = ?"
        return execute_query(query, (username, ), commit=True) > 0

    def db_get_pending_artist_requests(self):
        query = """
            SELECT u.Username, u.FullName, u.EmailAddress,
                   ISNULL(p.PlanName, 'Free') as Subscription,
                   u.DateJoined
            FROM Users u
            LEFT JOIN Subscription s ON u.Username = s.Username
            LEFT JOIN [Plans] p ON s.PlanID = p.PlanID
            WHERE u.UserType = 'PendingArtist' AND u.UserStatus = 'Active'
            ORDER BY u.DateJoined DESC
        """
        return execute_query(query)

    def db_search_artist_requests(self, search_term):
        query = """
            SELECT u.Username, u.FullName, u.EmailAddress,
                   ISNULL(p.PlanName, 'Free') as Subscription,
                   u.DateJoined
            FROM Users u
            LEFT JOIN Subscription s ON u. Username = s.Username
            LEFT JOIN [Plans] p ON s. PlanID = p.PlanID
            WHERE u.UserType = 'PendingArtist' AND u.UserStatus = 'Active'
              AND (u.Username LIKE ? OR u.FullName LIKE ?  OR u.EmailAddress LIKE ?)
            ORDER BY u.DateJoined DESC
        """
        pattern = f"%{search_term}%"
        return execute_query(query, (pattern, pattern, pattern))

    def db_accept_artist_request(self, username):
        query = "UPDATE Users SET UserType = 'Artist' WHERE Username = ?  AND UserType = 'PendingArtist'"
        return execute_query(query, (username, ), commit=True) > 0

    def db_reject_artist_request(self, username):
        query = "UPDATE Users SET UserType = 'Listener' WHERE Username = ? AND UserType = 'PendingArtist'"
        return execute_query(query, (username, ), commit=True) > 0

    def db_get_pending_songs(self):
        query = """
            SELECT sd.SongID, sd.SongName, sd.Username as ArtistName,
                   ISNULL(STRING_AGG(g.GenreName, ', '), 'Unknown') as Genres,
                   sd.ReleaseDate, sd.MetaData
            FROM SongDetails sd
            LEFT JOIN SongGenre sg ON sd.SongID = sg.SongID
            LEFT JOIN Genre g ON sg.GenreID = g.GenreID
            WHERE sd.SongStatus = 'Pending'
            GROUP BY sd.SongID, sd.SongName, sd.Username, sd.ReleaseDate, sd.MetaData
            ORDER BY sd.ReleaseDate DESC
        """
        return execute_query(query)

    def db_search_pending_songs(self, search_term):
        query = """
            SELECT sd.SongID, sd. SongName, sd.Username as ArtistName,
                   ISNULL(STRING_AGG(g.GenreName, ', '), 'Unknown') as Genres,
                   sd. ReleaseDate, sd.MetaData
            FROM SongDetails sd
            LEFT JOIN SongGenre sg ON sd.SongID = sg.SongID
            LEFT JOIN Genre g ON sg.GenreID = g.GenreID
            WHERE sd.SongStatus = 'Pending'
              AND (sd.SongName LIKE ? OR sd.Username LIKE ?)
            GROUP BY sd.SongID, sd.SongName, sd.Username, sd.ReleaseDate, sd.MetaData
            ORDER BY sd.ReleaseDate DESC
        """
        pattern = f"%{search_term}%"
        return execute_query(query, (pattern, pattern))

    def db_approve_song(self, song_id):
        query = "UPDATE SongDetails SET SongStatus = 'Active' WHERE SongID = ?  AND SongStatus = 'Pending'"
        return execute_query(query, (song_id, ), commit=True) > 0

    def db_reject_song(self, song_id):
        query = "UPDATE SongDetails SET SongStatus = 'Rejected' WHERE SongID = ?  AND SongStatus = 'Pending'"
        return execute_query(query, (song_id, ), commit=True) > 0

    def db_get_reported_songs(self):
        query = """
            SELECT sd.SongID, sd.SongName, sd.Username as ArtistName,
                   r.Username as ReportedBy, r.ReportReason,
                   ISNULL(STRING_AGG(g.GenreName, ', '), 'Unknown') as Genres,
                   sd. Likes, sd.Dislikes,
                   (SELECT COUNT(*) FROM Reports WHERE SongID = sd.SongID) as TotalReports,
                   sd.ReleaseDate
            FROM Reports r
            JOIN SongDetails sd ON r.SongID = sd.SongID
            LEFT JOIN SongGenre sg ON sd.SongID = sg.SongID
            LEFT JOIN Genre g ON sg.GenreID = g.GenreID
            WHERE sd.SongStatus = 'Active'
            GROUP BY sd.SongID, sd.SongName, sd.Username, r.Username, r.ReportReason,
                     sd.Likes, sd.Dislikes, sd.ReleaseDate
            ORDER BY TotalReports DESC
        """
        return execute_query(query)

    def db_search_reported_songs(self, search_term):
        query = """
            SELECT sd.SongID, sd.SongName, sd.Username as ArtistName,
                   r.Username as ReportedBy, r.ReportReason,
                   ISNULL(STRING_AGG(g. GenreName, ', '), 'Unknown') as Genres,
                   sd.Likes, sd.Dislikes,
                   (SELECT COUNT(*) FROM Reports WHERE SongID = sd.SongID) as TotalReports,
                   sd.ReleaseDate
            FROM Reports r
            JOIN SongDetails sd ON r.SongID = sd.SongID
            LEFT JOIN SongGenre sg ON sd.SongID = sg.SongID
            LEFT JOIN Genre g ON sg. GenreID = g.GenreID
            WHERE sd.SongStatus = 'Active'
              AND (sd.SongName LIKE ? OR sd.Username LIKE ?)
            GROUP BY sd. SongID, sd.SongName, sd.Username, r. Username, r.ReportReason,
                     sd.Likes, sd.Dislikes, sd.ReleaseDate
            ORDER BY TotalReports DESC
        """
        pattern = f"%{search_term}%"
        return execute_query(query, (pattern, pattern))

    def db_delete_reported_song(self, song_id):
        execute_query("DELETE FROM Reports WHERE SongID = ?", (song_id, ),
                      commit=True)
        query = "UPDATE SongDetails SET SongStatus = 'Deleted' WHERE SongID = ?"
        return execute_query(query, (song_id, ), commit=True) > 0

    def db_get_all_genres(self):
        query = "SELECT GenreID, GenreName FROM Genre ORDER BY GenreName"
        return execute_query(query)

    def db_add_genre(self, genre_name):
        result = execute_query("SELECT ISNULL(MAX(GenreID), 0) + 1 FROM Genre",
                               fetch_one=True)
        new_id = result[0]
        query = "INSERT INTO Genre (GenreID, GenreName) VALUES (?, ?)"
        return execute_query(query, (new_id, genre_name), commit=True) > 0

    def db_get_all_plans(self):
        query = "SELECT PlanID, PlanName, PlanPrice FROM [Plans] ORDER BY PlanPrice"
        return execute_query(query)

    def db_add_plan(self, plan_name, plan_price):
        result = execute_query(
            "SELECT ISNULL(MAX(PlanID), 0) + 1 FROM [Plans]", fetch_one=True)
        new_id = result[0]
        query = "INSERT INTO [Plans] (PlanID, PlanName, PlanPrice) VALUES (?, ?, ?)"
        return execute_query(query, (new_id, plan_name, plan_price),
                             commit=True) > 0

    def db_update_plan(self, plan_id, plan_name, plan_price):
        query = "UPDATE [Plans] SET PlanName = ?, PlanPrice = ? WHERE PlanID = ?"
        return execute_query(query, (plan_name, plan_price, plan_id),
                             commit=True) > 0

    def db_get_revenue_analytics(self, start_date, end_date, group_by='month'):
        if group_by == 'day':
            date_format = "CONVERT(varchar, PaymentDate, 23)"
        elif group_by == 'month':
            date_format = "FORMAT(PaymentDate, 'yyyy-MM')"
        else:
            date_format = "CAST(YEAR(PaymentDate) AS varchar)"

        query = f"""
            SELECT {date_format} as Period, SUM(Amount) as TotalRevenue
            FROM BillingRecord
            WHERE PaymentDate BETWEEN ?  AND ?
            GROUP BY {date_format}
            ORDER BY Period
        """
        results = execute_query(query, (start_date, end_date))
        return [[str(row[0]), float(row[1])]
                for row in results] if results else []

    def db_get_plays_analytics(self, start_date, end_date, group_by='month'):
        if group_by == 'day':
            date_format = "CONVERT(varchar, PlayDate, 23)"
        elif group_by == 'month':
            date_format = "FORMAT(PlayDate, 'yyyy-MM')"
        else:
            date_format = "CAST(YEAR(PlayDate) AS varchar)"

        query = f"""
            SELECT {date_format} as Period, COUNT(*) as TotalPlays
            FROM PlayHistory
            WHERE PlayDate BETWEEN ?  AND ?
            GROUP BY {date_format}
            ORDER BY Period
        """
        results = execute_query(query, (start_date, end_date))
        return [[str(row[0]), row[1]] for row in results] if results else []

    def db_get_user_analytics(self, start_date, end_date, group_by='month'):
        if group_by == 'day':
            date_format = "CONVERT(varchar, DateJoined, 23)"
        elif group_by == 'month':
            date_format = "FORMAT(DateJoined, 'yyyy-MM')"
        else:
            date_format = "CAST(YEAR(DateJoined) AS varchar)"

        query = f"""
            SELECT {date_format} as Period, COUNT(*) as NewUsers
            FROM Users
            WHERE DateJoined BETWEEN ? AND ? 
              AND UserStatus != 'Deleted'
            GROUP BY {date_format}
            ORDER BY Period
        """
        results = execute_query(query, (start_date, end_date))
        return [[str(row[0]), row[1]] for row in results] if results else []

    # ==================== ANALYTICS HANDLERS ====================

    def handle_view_revenue(self):
        try:
            start_date = self.qdate_to_string(
                self.window.ReveueStartDate.date())
            end_date = self.qdate_to_string(self.window.ReveueEndDate.date())

            if start_date > end_date:
                self.show_warning(
                    "Start date must be before or equal to end date.")
                return

            period = self.get_selected_grouping(self.window.RevenueDay,
                                                self.window.RevenueMonth,
                                                self.window.RevenueYear)

            data = self.db_get_revenue_analytics(start_date, end_date, period)

            if not data:
                self.show_warning(
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

        except Exception as e:
            self.show_error(f"Failed to load revenue data:\n{str(e)}")

    def handle_view_plays(self):
        try:
            start_date = self.qdate_to_string(
                self.window.PlaysStartDate.date())
            end_date = self.qdate_to_string(self.window.PlaysEndDate.date())

            if start_date > end_date:
                self.show_warning(
                    "Start date must be before or equal to end date.")
                return

            period = self.get_selected_grouping(self.window.PlaysDay,
                                                self.window.PlaysMonth,
                                                self.window.PlaysYear)

            data = self.db_get_plays_analytics(start_date, end_date, period)

            if not data:
                self.show_warning(
                    "No plays data found for the selected date range.")
                return

            dialog = AnalyticsGraphDialog(
                self.window,
                f"Plays Analysis (Grouped by {period.capitalize()})",
                data,
                period.capitalize() if period != "day" else "Date",
                "Total Plays",
                graph_type="line")
            dialog.exec_()

        except Exception as e:
            self.show_error(f"Failed to load plays data:\n{str(e)}")

    def handle_view_users(self):
        try:
            start_date = self.qdate_to_string(
                self.window.UsersStartDate.date())
            end_date = self.qdate_to_string(self.window.UsersEndDate.date())

            if start_date > end_date:
                self.show_warning(
                    "Start date must be before or equal to end date.")
                return

            period = self.get_selected_grouping(self.window.UsersDay,
                                                self.window.UsersMonth,
                                                self.window.UsersYear)

            data = self.db_get_user_analytics(start_date, end_date, period)

            if not data:
                self.show_warning(
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

        except Exception as e:
            self.show_error(f"Failed to load user data:\n{str(e)}")

    # ==================== ARTIST REQUESTS ====================

    def load_artist_requests_table(self, data=None):
        try:
            requests = data if data is not None else self.db_get_pending_artist_requests(
            )
            table = self.window.artistsRequestTable
            table.setRowCount(len(requests) if requests else 0)

            if requests:
                for row, request in enumerate(requests):
                    table.setItem(row, 0,
                                  QtWidgets.QTableWidgetItem(str(row + 1)))
                    table.setItem(
                        row, 1,
                        QtWidgets.QTableWidgetItem(str(request[0] or '')))
                    table.setItem(
                        row, 2,
                        QtWidgets.QTableWidgetItem(str(request[1] or '')))
                    table.setItem(
                        row, 3,
                        QtWidgets.QTableWidgetItem(str(request[2] or '')))
                    table.setItem(
                        row, 4,
                        QtWidgets.QTableWidgetItem(str(request[3] or '')))

            table.resizeColumnsToContents()

        except Exception as e:
            self.show_error(f"Failed to load artist requests:\n{str(e)}")

    def populate_artist_request_form(self, row, column):
        try:
            table = self.window.artistsRequestTable
            username = table.item(row, 1).text()

            requests = self.db_get_pending_artist_requests()
            request_data = next((r for r in requests if r[0] == username),
                                None)

            if request_data:
                self.window.UsernameLineEdit_2.setText(
                    str(request_data[0] or ''))
                self.window.FullNameLineEdit_2.setText(
                    str(request_data[1] or ''))
                self.window.EmailLineEdit_2.setText(str(request_data[2] or ''))
                self.window.SubscriptionLineEdit_2.setText(
                    str(request_data[3] or ''))
                if request_data[4]:
                    self.window.dateJoined_2.setDate(
                        self.string_to_qdate(request_data[4]))

        except Exception as e:
            self.show_error(f"Failed to load request details:\n{str(e)}")

    def clear_artist_request_form(self):
        self.window.UsernameLineEdit_2.clear()
        self.window.FullNameLineEdit_2.clear()
        self.window.EmailLineEdit_2.clear()
        self.window.SubscriptionLineEdit_2.clear()
        self.window.dateJoined_2.setDate(QtCore.QDate.currentDate())

    def handle_accept_artist_request(self):
        username = self.window.UsernameLineEdit_2.text()
        if not username:
            self.show_warning(
                "Please select an artist request from the table.")
            return

        try:
            if self.db_accept_artist_request(username):
                self.show_success(
                    f"Artist request for '{username}' has been accepted.")
                self.load_artist_requests_table()
                self.clear_artist_request_form()
            else:
                self.show_error(f"Could not accept request for '{username}'.")
        except Exception as e:
            self.show_error(f"Database error:\n{str(e)}")

    def handle_reject_artist_request(self):
        username = self.window.UsernameLineEdit_2.text()
        if not username:
            self.show_warning(
                "Please select an artist request from the table.")
            return

        try:
            if self.db_reject_artist_request(username):
                self.show_success(
                    f"Artist request for '{username}' has been rejected.")
                self.load_artist_requests_table()
                self.clear_artist_request_form()
            else:
                self.show_error(f"Could not reject request for '{username}'.")
        except Exception as e:
            self.show_error(f"Database error:\n{str(e)}")

    def handle_search_artist_requests(self):
        search_term = self.window.pendingArtistSearch.text().strip()

        try:
            if not search_term:
                self.load_artist_requests_table()
            else:
                results = self.db_search_artist_requests(search_term)
                self.load_artist_requests_table(results)
        except Exception as e:
            self.show_error(f"Search failed:\n{str(e)}")

    # ==================== USERS MANAGEMENT ====================

    def load_users_table(self, data=None):
        try:
            users = data if data is not None else self.db_get_all_users()
            table = self.window.tableWidget
            table.setRowCount(len(users) if users else 0)

            if users:
                for row, user in enumerate(users):
                    table.setItem(
                        row, 0, QtWidgets.QTableWidgetItem(str(user[0] or '')))
                    table.setItem(
                        row, 1, QtWidgets.QTableWidgetItem(str(user[6] or '')))
                    table.setItem(
                        row, 2, QtWidgets.QTableWidgetItem(str(user[3] or '')))
                    table.setItem(
                        row, 3,
                        QtWidgets.QTableWidgetItem(
                            str(user[7]) if user[7] else ''))
                    table.setItem(
                        row, 4, QtWidgets.QTableWidgetItem(str(user[2] or '')))

            table.resizeColumnsToContents()

        except Exception as e:
            self.show_error(f"Failed to load users:\n{str(e)}")

    def populate_user_form(self, row, column):
        try:
            table = self.window.tableWidget
            username = table.item(row, 0).text()
            user_data = self.db_get_user(username)

            if user_data:
                self.window.UsernameLineEdit.setText(str(user_data[0] or ''))
                self.window.FullNameLineEdit.setText(str(user_data[6] or ''))
                self.window.EmailLineEdit.setText(str(user_data[3] or ''))
                self.window.UserTypeLineEdit.setText(str(user_data[2] or ''))

                if user_data[7]:
                    self.window.dateJoined.setDate(
                        self.string_to_qdate(user_data[7]))

        except Exception as e:
            self.show_error(f"Failed to load user details:\n{str(e)}")

    def clear_user_form(self):
        self.window.UsernameLineEdit.clear()
        self.window.FullNameLineEdit.clear()
        self.window.EmailLineEdit.clear()
        self.window.dateJoined.setDate(QtCore.QDate.currentDate())
        self.window.UserTypeLineEdit.clear()
        if hasattr(self.window, 'SubscriptionLineEdit'):
            self.window.SubscriptionLineEdit.clear()
        if hasattr(self.window, 'RevenueLineEdit'):
            self.window.RevenueLineEdit.clear()

    def handle_delete_user(self):
        username = self.window.UsernameLineEdit.text()
        if not username:
            self.show_warning("Please select a user from the table to delete.")
            return

        reply = QtWidgets.QMessageBox.question(
            self.window, "Confirm Deletion",
            f"Are you sure you want to delete '{username}'?  This cannot be undone.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                if self.db_delete_user(username):
                    self.show_success(f"User '{username}' has been deleted.")
                    self.load_users_table()
                    self.clear_user_form()
                else:
                    self.show_error(f"Could not delete user '{username}'.")
            except Exception as e:
                self.show_error(f"Database error:\n{str(e)}")

    def handle_search_users(self):
        search_term = self.window.searchUserInput.text().strip()

        try:
            if not search_term:
                self.load_users_table()
            else:
                results = self.db_search_users(search_term)
                self.load_users_table(results)
        except Exception as e:
            self.show_error(f"Search failed:\n{str(e)}")

    # ==================== PENDING SONGS ====================

    def load_pending_songs_table(self, data=None):
        try:
            songs = data if data is not None else self.db_get_pending_songs()
            table = self.window.pendingSongsTable
            table.setRowCount(len(songs) if songs else 0)

            if songs:
                for row, song in enumerate(songs):
                    table.setItem(
                        row, 0, QtWidgets.QTableWidgetItem(str(song[0] or '')))
                    table.setItem(
                        row, 1, QtWidgets.QTableWidgetItem(str(song[1] or '')))
                    table.setItem(
                        row, 2, QtWidgets.QTableWidgetItem(str(song[2] or '')))
                    table.setItem(
                        row, 3, QtWidgets.QTableWidgetItem(str(song[3] or '')))
                    table.setItem(
                        row, 4,
                        QtWidgets.QTableWidgetItem(
                            str(song[4]) if song[4] else ''))

            table.resizeColumnsToContents()

        except Exception as e:
            self.show_error(f"Failed to load pending songs:\n{str(e)}")

    def populate_pending_song_form(self, row, column):
        try:
            table = self.window.pendingSongsTable

            self.window.PendingsongID.setText(table.item(row, 0).text())
            self.window.PendingSongName.setText(table.item(row, 1).text())
            self.window.ArtistName.setText(table.item(row, 2).text())
            self.window.genreLineEdit.setText(table.item(row, 3).text())

            date_str = table.item(row, 4).text()
            if date_str:
                self.window.submissionDate.setDate(
                    self.string_to_qdate(date_str))

            self.window.songImage.setPixmap(
                QtGui.QPixmap("Song_images/default_song_image.jpg"))

        except Exception as e:
            self.show_error(f"Failed to load song details:\n{str(e)}")

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
            self.show_warning("Please select a song from the table.")
            return

        song_name = self.window.PendingSongName.text()
        QtWidgets.QMessageBox.information(
            self.window, "Playing Song",
            f"Simulating playback of:  {song_name}")

    def handle_approve_song(self):
        song_id = self.window.PendingsongID.text()
        if not song_id:
            self.show_warning("Please select a song to approve.")
            return

        try:
            if self.db_approve_song(int(song_id)):
                self.show_success("Song has been approved.")
                self.load_pending_songs_table()
                self.clear_pending_song_form()
            else:
                self.show_error(f"Could not approve song '{song_id}'.")
        except Exception as e:
            self.show_error(f"Database error:\n{str(e)}")

    def handle_reject_song(self):
        song_id = self.window.PendingsongID.text()
        if not song_id:
            self.show_warning("Please select a song to reject.")
            return

        try:
            if self.db_reject_song(int(song_id)):
                self.show_success("Song has been rejected.")
                self.load_pending_songs_table()
                self.clear_pending_song_form()
            else:
                self.show_error(f"Could not reject song '{song_id}'.")
        except Exception as e:
            self.show_error(f"Database error:\n{str(e)}")

    def handle_search_pending_songs(self):
        search_term = self.window.pendingSongSearch.text().strip()

        try:
            if not search_term:
                self.load_pending_songs_table()
            else:
                results = self.db_search_pending_songs(search_term)
                self.load_pending_songs_table(results)
        except Exception as e:
            self.show_error(f"Search failed:\n{str(e)}")

    # ==================== REPORTED SONGS ====================

    def load_reported_songs_table(self, data=None):
        try:
            reports = data if data is not None else self.db_get_reported_songs(
            )
            table = self.window.reportedSongsTable
            table.setRowCount(len(reports) if reports else 0)

            if reports:
                for row, report in enumerate(reports):
                    table.setItem(
                        row, 0, QtWidgets.QTableWidgetItem(str(report[0]
                                                               or '')))
                    table.setItem(
                        row, 1, QtWidgets.QTableWidgetItem(str(report[1]
                                                               or '')))
                    table.setItem(
                        row, 2, QtWidgets.QTableWidgetItem(str(report[2]
                                                               or '')))
                    table.setItem(
                        row, 3, QtWidgets.QTableWidgetItem(str(report[3]
                                                               or '')))
                    table.setItem(
                        row, 4, QtWidgets.QTableWidgetItem(str(report[4]
                                                               or '')))

            table.resizeColumnsToContents()
            table.horizontalHeader().setStretchLastSection(True)

        except Exception as e:
            self.show_error(f"Failed to load reported songs:\n{str(e)}")

    def populate_reported_song_form(self, row, column):
        try:
            table = self.window.reportedSongsTable
            song_id = table.item(row, 0).text()

            reports = self.db_get_reported_songs()
            report_data = next((r for r in reports if str(r[0]) == song_id),
                               None)

            if report_data:
                self.window.Reports_SongID.setText(str(report_data[0] or ''))
                self.window.Reports_SongName.setText(str(report_data[1] or ''))
                self.window.Reports_ArtistName.setText(
                    str(report_data[2] or ''))
                self.window.Reports_Genre.setText(str(report_data[5] or ''))
                self.window.Reports_Likes.setText(str(report_data[6] or 0))
                self.window.Reports_Dislikes.setText(str(report_data[7] or 0))
                self.window.Reports_Dislikes_2.setText(str(report_data[8]
                                                           or 0))

                if report_data[9]:
                    self.window.Reports_UploadDate.setDate(
                        self.string_to_qdate(report_data[9]))

        except Exception as e:
            self.show_error(f"Failed to load report details:\n{str(e)}")

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
            self.show_warning("Please select a reported song to delete.")
            return

        reply = QtWidgets.QMessageBox.question(
            self.window, "Confirm Deletion",
            f"Permanently delete song '{song_id}'? This cannot be undone.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                if self.db_delete_reported_song(int(song_id)):
                    self.show_success(f"Song '{song_id}' has been deleted.")
                    self.load_reported_songs_table()
                    self.clear_reported_song_form()
                else:
                    self.show_error(f"Could not delete song '{song_id}'.")
            except Exception as e:
                self.show_error(f"Database error:\n{str(e)}")

    def handle_search_reports(self):
        search_term = self.window.searchReportInput.text().strip()

        try:
            if not search_term:
                self.load_reported_songs_table()
            else:
                results = self.db_search_reported_songs(search_term)
                self.load_reported_songs_table(results)
        except Exception as e:
            self.show_error(f"Search failed:\n{str(e)}")

    # ==================== SUBSCRIPTION PLANS ====================

    def load_subscription_plans_table(self):
        try:
            plans = self.db_get_all_plans()
            table = self.window.tableWidget_2
            table.setRowCount(len(plans) if plans else 0)

            if plans:
                for row, plan in enumerate(plans):
                    table.setItem(
                        row, 0, QtWidgets.QTableWidgetItem(str(plan[0] or '')))
                    table.setItem(
                        row, 1, QtWidgets.QTableWidgetItem(str(plan[1] or '')))
                    table.setItem(
                        row, 2, QtWidgets.QTableWidgetItem(str(plan[2] or '')))

            table.resizeColumnsToContents()

        except Exception as e:
            self.show_error(f"Failed to load plans:\n{str(e)}")

    def populate_subscription_plan_form(self, row, column):
        try:
            table = self.window.tableWidget_2

            self.window.current_plan_id = table.item(row, 0).text()
            self.window.PlanName.setText(table.item(row, 1).text())
            self.window.PlanPrice.setText(table.item(row, 2).text())

        except Exception as e:
            self.show_error(f"Failed to load plan details:\n{str(e)}")

    def clear_subscription_plan_form(self):
        self.window.PlanName.clear()
        self.window.PlanPrice.clear()
        if hasattr(self.window, 'PlanDuration'):
            self.window.PlanDuration.clear()
        if hasattr(self.window, 'PlanFeatures'):
            self.window.PlanFeatures.clear()
        if hasattr(self.window, "current_plan_id"):
            del self.window.current_plan_id

    def handle_add_subscription_plan(self):
        plan_name = self.window.PlanName.text().strip()

        try:
            plan_price = float(self.window.PlanPrice.text())
        except ValueError:
            self.show_warning("Price must be a valid number.")
            return

        if not plan_name:
            self.show_warning("Please enter a plan name.")
            return

        try:
            if self.db_add_plan(plan_name, plan_price):
                self.show_success(f"New plan '{plan_name}' added.")
                self.load_subscription_plans_table()
                self.clear_subscription_plan_form()
            else:
                self.show_error("Could not add plan.")
        except Exception as e:
            self.show_error(f"Database error:\n{str(e)}")

    def handle_update_subscription_plan(self):
        if not hasattr(self.window, "current_plan_id"):
            self.show_warning("Please select a plan to update.")
            return

        plan_id = int(self.window.current_plan_id)
        plan_name = self.window.PlanName.text().strip()

        try:
            plan_price = float(self.window.PlanPrice.text())
        except ValueError:
            self.show_warning("Price must be a valid number.")
            return

        if not plan_name:
            self.show_warning("Please enter a plan name.")
            return

        try:
            if self.db_update_plan(plan_id, plan_name, plan_price):
                self.show_success(f"Plans '{plan_name}' updated.")
                self.load_subscription_plans_table()
                self.clear_subscription_plan_form()
            else:
                self.show_error("Could not update plan.")
        except Exception as e:
            self.show_error(f"Database error:\n{str(e)}")

    # ==================== GENRES ====================

    def load_genre_table(self):
        try:
            genres = self.db_get_all_genres()
            table = self.window.tableWidget_3
            table.setRowCount(len(genres) if genres else 0)

            if genres:
                for row, genre in enumerate(genres):
                    table.setItem(
                        row, 0, QtWidgets.QTableWidgetItem(str(genre[0]
                                                               or '')))
                    table.setItem(
                        row, 1, QtWidgets.QTableWidgetItem(str(genre[1]
                                                               or '')))

            table.resizeColumnsToContents()
            table.horizontalHeader().setStretchLastSection(True)

        except Exception as e:
            self.show_error(f"Failed to load genres:\n{str(e)}")

    def handle_add_genre(self):
        genre_name = self.window.genreNameLineEdit.text().strip()

        if not genre_name:
            self.show_warning("Please enter a genre name.")
            return

        try:
            if self.db_add_genre(genre_name):
                self.show_success(f"New genre '{genre_name}' added.")
                self.load_genre_table()
                self.window.genreNameLineEdit.clear()
                if hasattr(self.window, 'genreDescriptionLineEdit'):
                    self.window.genreDescriptionLineEdit.clear()
            else:
                self.show_error("Could not add genre.")
        except Exception as e:
            self.show_error(f"Database error:\n{str(e)}")
