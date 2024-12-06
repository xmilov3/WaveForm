-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Czas generowania: 06 Gru 2024, 03:07
-- Wersja serwera: 10.4.27-MariaDB
-- Wersja PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `WaveForm_db`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `playlists`
--

CREATE TABLE `playlists` (
  `playlist_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `created_by` varchar(255) NOT NULL,
  `playlist_cover_path` varchar(500) DEFAULT NULL COMMENT 'Path to playlist cover'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Zrzut danych tabeli `playlists`
--

INSERT INTO `playlists` (`playlist_id`, `user_id`, `name`, `description`, `created_at`, `created_by`, `playlist_cover_path`) VALUES
(1, 1, 'Liked Songs', 'Your Liked Songs', '2024-11-29 20:19:29', 'xmilov3', '/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/app/gui/assets/covers/playlist_covers/liked_songs_cover.png');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `playlist_songs`
--

CREATE TABLE `playlist_songs` (
  `playlist_songs_id` int(11) NOT NULL,
  `playlist_id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Zrzut danych tabeli `playlist_songs`
--

INSERT INTO `playlist_songs` (`playlist_songs_id`, `playlist_id`, `song_id`) VALUES
(1, 1, 1),
(2, 1, 3),
(3, 1, 2);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `songs`
--

CREATE TABLE `songs` (
  `song_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `artist` varchar(255) DEFAULT NULL,
  `album` varchar(255) DEFAULT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `file_path` varchar(500) NOT NULL,
  `cover_path` varchar(500) DEFAULT NULL,
  `uploaded_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Zrzut danych tabeli `songs`
--

INSERT INTO `songs` (`song_id`, `user_id`, `title`, `artist`, `album`, `genre`, `file_path`, `cover_path`, `uploaded_at`) VALUES
(1, 1, 'Like a G6', 'MiLo', 'Like a G6', 'House', '/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/Music/MiLo - Like a G6.wav', '/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/app/gui/assets/covers/song_covers/Like_a_G6.jpg', '2024-11-29 20:09:00'),
(2, 1, 'Cocaine VIP', 'MiLo', 'Cocaine VIP', 'Techno', '/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/Music/MiLo - Cocaine VIP.wav', '/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/app/gui/assets/covers/song_covers/COCAINE_COVER_VIP.png', '2024-11-29 22:32:14'),
(3, 1, 'Dziki Bass', 'Enter, MALOS, MATTY, MiLo', NULL, 'Vixa', '/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/Music/Enter - Dziki Bass (MALOS & MATTY BOOTLEG & MILO EDIT 2023cover).mp3', '/Users/bartek/Desktop/Politechnika/Praca inżynierska/WaveForm/app/gui/assets/covers/song_covers/Dziki bass.png', '2024-11-29 22:33:23');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(500) NOT NULL,
  `birth_date` date NOT NULL,
  `gender` enum('men','women') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Zrzut danych tabeli `users`
--

INSERT INTO `users` (`user_id`, `username`, `email`, `password_hash`, `birth_date`, `gender`, `created_at`) VALUES
(1, 'xmilov3', 'xmilov3@gmail.com', 'admin', '2014-11-18', 'men', '2024-11-29 19:03:45'),
(2, 'asdasdas', 'daasda@wp.pl', 'test', '1903-03-04', 'men', '2024-12-01 19:37:48'),
(3, 'bartek', 'bartek@wp.pl', 'admin', '2001-02-02', 'men', '2024-12-01 20:06:25'),
(4, 'test2', 'test2@wp.pl', 'xxxx', '1914-05-06', 'men', '2024-12-02 17:16:30');

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `playlists`
--
ALTER TABLE `playlists`
  ADD PRIMARY KEY (`playlist_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeksy dla tabeli `playlist_songs`
--
ALTER TABLE `playlist_songs`
  ADD PRIMARY KEY (`playlist_songs_id`),
  ADD KEY `playlist_id` (`playlist_id`),
  ADD KEY `song_id` (`song_id`);

--
-- Indeksy dla tabeli `songs`
--
ALTER TABLE `songs`
  ADD PRIMARY KEY (`song_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeksy dla tabeli `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT dla zrzuconych tabel
--

--
-- AUTO_INCREMENT dla tabeli `playlists`
--
ALTER TABLE `playlists`
  MODIFY `playlist_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT dla tabeli `playlist_songs`
--
ALTER TABLE `playlist_songs`
  MODIFY `playlist_songs_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT dla tabeli `songs`
--
ALTER TABLE `songs`
  MODIFY `song_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT dla tabeli `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `playlists`
--
ALTER TABLE `playlists`
  ADD CONSTRAINT `playlists_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Ograniczenia dla tabeli `playlist_songs`
--
ALTER TABLE `playlist_songs`
  ADD CONSTRAINT `playlist_songs_ibfk_1` FOREIGN KEY (`playlist_id`) REFERENCES `playlists` (`playlist_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `playlist_songs_ibfk_2` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`) ON DELETE CASCADE;

--
-- Ograniczenia dla tabeli `songs`
--
ALTER TABLE `songs`
  ADD CONSTRAINT `songs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
