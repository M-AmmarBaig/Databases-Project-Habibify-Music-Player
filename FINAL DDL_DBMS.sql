-- Create Database
CREATE DATABASE HabibifyDatabase;
GO

USE HabibifyDatabase;
GO

-- Create Users Table
CREATE TABLE Users (
    Username VARCHAR(50) PRIMARY KEY,
    Password VARCHAR(255) NOT NULL,
    UserType VARCHAR(20) NOT NULL,
    EmailAddress VARCHAR(100) NOT NULL,
    UserStatus VARCHAR(20) NOT NULL CHECK (UserStatus IN ('Active', 'Banned', 'Deleted')),
    PhoneNo VARCHAR(20),
    FullName VARCHAR(100),
    DateJoined DATE DEFAULT GETDATE()
);
GO

-- Create Genre Table
CREATE TABLE Genre (
    GenreID INT PRIMARY KEY,
    GenreName VARCHAR(50) NOT NULL
);
GO

-- Create Plans Table
CREATE TABLE Plans (
    PlanID INT PRIMARY KEY,
    PlanName VARCHAR(100) NOT NULL,
    PlanPrice DECIMAL(10, 2) NOT NULL
);
GO

-- Create SongDetails Table
CREATE TABLE SongDetails (
    SongID INT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL,
    SongName VARCHAR(200) NOT NULL,
    Likes INT DEFAULT 0,
    Dislikes INT DEFAULT 0,
    Listens INT DEFAULT 0,
    ReleaseDate DATE,
    MetaData VARCHAR(MAX),
    SongStatus VARCHAR(20) DEFAULT 'Pending' CHECK (SongStatus IN ('Pending', 'Active', 'Rejected', 'Deleted')),
    FOREIGN KEY (Username) REFERENCES Users(Username)
);
GO

-- Create Playlist Table
CREATE TABLE Playlist (
    PlaylistID INT PRIMARY KEY,
    PlaylistName VARCHAR(100) NOT NULL,
    Username VARCHAR(50) NOT NULL,
    DateOfCreation DATE NOT NULL,
    Visits INT DEFAULT 0,
    FOREIGN KEY (Username) REFERENCES Users(Username)
);
GO

-- Create Queue Table
CREATE TABLE Queue (
    QueueID INT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL,
    QueueTimeDate DATETIME NOT NULL,
    FOREIGN KEY (Username) REFERENCES Users(Username)
);
GO

-- Create Subscription Table
CREATE TABLE Subscription (
    SubscriptionID INT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL,
    PlanID INT NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE,
    FOREIGN KEY (Username) REFERENCES Users(Username),
    FOREIGN KEY (PlanID) REFERENCES Plans(PlanID)
);
GO

-- Create BillingRecord Table
CREATE TABLE BillingRecord (
    Username VARCHAR(50) NOT NULL,
    SubscriptionID INT NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    PaymentDate DATE NOT NULL,
    PRIMARY KEY (Username, SubscriptionID, PaymentDate),
    FOREIGN KEY (Username) REFERENCES Users(Username),
    FOREIGN KEY (SubscriptionID) REFERENCES Subscription(SubscriptionID)
);
GO

-- Create PlayHistory Table
CREATE TABLE PlayHistory (
    Username VARCHAR(50) NOT NULL,
    SongID INT NOT NULL,
    PlayDate DATETIME NOT NULL,
    PRIMARY KEY (Username, SongID, PlayDate),
    FOREIGN KEY (Username) REFERENCES Users(Username),
    FOREIGN KEY (SongID) REFERENCES SongDetails(SongID)
);
GO

-- Create PlaylistSong Table (Junction)
CREATE TABLE PlaylistSong (
    PlaylistID INT NOT NULL,
    SongID INT NOT NULL,
    PRIMARY KEY (PlaylistID, SongID),
    FOREIGN KEY (PlaylistID) REFERENCES Playlist(PlaylistID),
    FOREIGN KEY (SongID) REFERENCES SongDetails(SongID)
);
GO

-- Create QueueContains Table (Junction)
CREATE TABLE QueueContains (
    QueueID INT NOT NULL,
    SongID INT NOT NULL,
    PRIMARY KEY (QueueID, SongID),
    FOREIGN KEY (QueueID) REFERENCES Queue(QueueID),
    FOREIGN KEY (SongID) REFERENCES SongDetails(SongID)
);
GO

-- Create Reaction Table
CREATE TABLE Reaction (
    Username VARCHAR(50) NOT NULL,
    SongID INT NOT NULL,
    ReactionType VARCHAR(20) NOT NULL,
    PRIMARY KEY (Username, SongID),
    FOREIGN KEY (Username) REFERENCES Users(Username),
    FOREIGN KEY (SongID) REFERENCES SongDetails(SongID)
);
GO

-- Create Reports Table
CREATE TABLE Reports (
    Username VARCHAR(50) NOT NULL,
    SongID INT NOT NULL,
    ReportReason VARCHAR(500) NOT NULL,
    PRIMARY KEY (Username, SongID),
    FOREIGN KEY (Username) REFERENCES Users(Username),
    FOREIGN KEY (SongID) REFERENCES SongDetails(SongID)
);
GO

-- Create SongGenre Table (Junction)
CREATE TABLE SongGenre (
    SongID INT NOT NULL,
    GenreID INT NOT NULL,
    PRIMARY KEY (SongID, GenreID),
    FOREIGN KEY (SongID) REFERENCES SongDetails(SongID),
    FOREIGN KEY (GenreID) REFERENCES Genre(GenreID)
);
GO