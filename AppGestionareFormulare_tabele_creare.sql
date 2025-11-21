use [App-Gestionare-Formulare]

CREATE TABLE Utilizatori (
    ID_Utilizator int PRIMARY KEY IDENTITY (1,1),
    Email nvarchar(100) UNIQUE NOT NULL,
    Parola nvarchar(100) NOT NULL
);

CREATE TABLE Raspunsuri (
    ID_raspuns int PRIMARY KEY IDENTITY (1,1),
	ID_Utilizator int NOT NULL,
    Formular nvarchar(100),
    Camp nvarchar(100),
    Valoare nvarchar(MAX),
    DataRaspuns datetime default GETDATE(),
	FOREIGN KEY(ID_Utilizator) REFERENCES Utilizatori(ID_Utilizator)
);
