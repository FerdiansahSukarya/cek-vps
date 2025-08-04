-- phpMyAdmin SQL Dump
-- version 5.2.1deb1+deb12u1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 04, 2025 at 01:59 PM
-- Server version: 10.11.11-MariaDB-0+deb12u1
-- PHP Version: 8.2.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sensor_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `evaluasi_tinggi`
--

CREATE TABLE `evaluasi_tinggi` (
  `id` int(11) NOT NULL,
  `tanggal` date NOT NULL,
  `tinggi_cm` float NOT NULL,
  `keterangan` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `log_manual`
--

CREATE TABLE `log_manual` (
  `id` int(11) NOT NULL,
  `waktu` datetime NOT NULL,
  `aksi` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `log_manual`
--

INSERT INTO `log_manual` (`id`, `waktu`, `aksi`) VALUES
(1, '2025-08-04 13:41:40', 'N1_ON');

-- --------------------------------------------------------

--
-- Table structure for table `log_tombol`
--

CREATE TABLE `log_tombol` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `waktu` timestamp NOT NULL,
  `keterangan` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `relay_log`
--

CREATE TABLE `relay_log` (
  `id` int(11) NOT NULL,
  `ph` float NOT NULL,
  `waktu` time NOT NULL,
  `durasi` varchar(20) NOT NULL,
  `pemberian_ulang` varchar(20) NOT NULL,
  `jenis` varchar(10) NOT NULL,
  `status` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `relay_log`
--

INSERT INTO `relay_log` (`id`, `ph`, `waktu`, `durasi`, `pemberian_ulang`, `jenis`, `status`) VALUES
(1, 6.33, '14:17:00', '20 detik', '1 minggu', 'n2', 'on'),
(2, 6.33, '14:17:00', '20 detik', '1 minggu', 'n2', 'off'),
(3, 6.33, '14:21:00', '20 detik', '1 minggu', 'n2', 'on'),
(4, 6.33, '14:21:00', '20 detik', '1 minggu', 'n2', 'off'),
(5, 6.33, '14:31:00', '20 detik', '1 minggu', 'n2', 'on'),
(6, 6.33, '14:31:00', '20 detik', '1 minggu', 'n2', 'off'),
(7, 6.33, '14:36:00', '20 detik', '1 minggu', 'n2', 'on'),
(8, 6.33, '14:36:00', '20 detik', '1 minggu', 'n2', 'off'),
(9, 6.33, '14:36:00', '20 detik', '1 minggu', 'n2', 'on'),
(10, 6.33, '14:36:00', '20 detik', '1 minggu', 'n2', 'off'),
(11, 6.33, '14:52:00', '20 detik', '1 minggu', 'n2', 'on'),
(12, 6.33, '14:52:00', '20 detik', '1 minggu', 'n2', 'off'),
(13, 6.33, '14:53:00', '20 detik', '1 minggu', 'n2', 'on'),
(14, 6.33, '14:53:00', '20 detik', '1 minggu', 'n2', 'off'),
(15, 6.33, '14:54:00', '20 detik', '1 minggu', 'n2', 'on'),
(16, 6.33, '14:54:00', '20 detik', '1 minggu', 'n2', 'off'),
(17, 6.33, '14:54:00', '20 detik', '1 minggu', 'n2', 'on'),
(18, 6.33, '14:56:40', '20 detik', '1 minggu', 'n2', 'on'),
(19, 6.33, '14:56:40', '20 detik', '1 minggu', 'n2', 'off'),
(20, 6.36, '20:30:54', '20 detik', '1 minggu', 'n2', 'on'),
(21, 6.36, '20:45:24', '20 detik', '1 minggu', 'n2', 'on'),
(22, 6.36, '20:45:24', '20 detik', '1 minggu', 'n2', 'off');

-- --------------------------------------------------------

--
-- Table structure for table `sensor_data`
--

CREATE TABLE `sensor_data` (
  `id` int(11) NOT NULL,
  `waktu` datetime NOT NULL,
  `ph` float NOT NULL,
  `tinggi_cm` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sensor_data`
--

INSERT INTO `sensor_data` (`id`, `waktu`, `ph`, `tinggi_cm`) VALUES
(1, '2025-08-03 12:51:04', 6.3, 12),
(2, '2025-08-04 01:49:27', 0, 0),
(3, '2025-08-04 01:49:58', 6.37, 47),
(4, '2025-08-04 01:53:31', 0, 0),
(5, '2025-08-04 01:54:02', 6.31, 48.1),
(6, '2025-08-04 01:54:32', 6.32, 47.5),
(7, '2025-08-04 01:55:03', 6.42, 0),
(8, '2025-08-04 02:04:45', 0, 0),
(9, '2025-08-04 02:05:16', 6.38, 47.7),
(10, '2025-08-04 02:05:51', 6.37, 0),
(11, '2025-08-04 02:11:31', 0, 0),
(12, '2025-08-04 02:12:02', 6.37, 0),
(13, '2025-08-04 02:12:38', 6.41, 0),
(14, '2025-08-04 02:13:13', 6.38, 0),
(15, '2025-08-04 02:13:49', 6.36, 0),
(16, '2025-08-04 02:14:25', 6.37, 0),
(17, '2025-08-04 02:15:02', 6.35, 0),
(18, '2025-08-04 02:15:38', 6.34, 47.3),
(19, '2025-08-04 02:16:13', 6.39, 47.1),
(20, '2025-08-04 02:16:49', 6.38, 0),
(21, '2025-08-04 02:22:45', 0, 0),
(22, '2025-08-04 02:27:32', 0, 0),
(23, '2025-08-04 02:28:03', 6.36, 0),
(24, '2025-08-04 02:28:34', 6.33, 0),
(25, '2025-08-04 20:15:31', 0, 0),
(26, '2025-08-04 20:26:39', 0, 0),
(27, '2025-08-04 20:27:10', 6.4, 0),
(28, '2025-08-04 20:27:46', 6.39, 0),
(29, '2025-08-04 20:28:22', 6.38, 0),
(30, '2025-08-04 20:28:58', 6.36, 0);

-- --------------------------------------------------------

--
-- Table structure for table `tindakan`
--

CREATE TABLE `tindakan` (
  `id` int(11) NOT NULL,
  `waktu_tindakan` datetime NOT NULL,
  `jenis` varchar(20) NOT NULL,
  `durasi_detik` int(11) NOT NULL,
  `deskripsi` text DEFAULT NULL,
  `status` enum('pending','done') DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tindakan`
--

INSERT INTO `tindakan` (`id`, `waktu_tindakan`, `jenis`, `durasi_detik`, `deskripsi`, `status`) VALUES
(1, '2025-08-04 02:27:46', 'relay1', 0, 'User menyalakan relay1 ke ON', 'pending'),
(2, '2025-08-04 02:27:59', 'relay2', 0, 'User menyalakan relay2 ke ON', 'pending'),
(3, '2025-08-04 02:28:01', 'relay2', 0, 'User menyalakan relay2 ke OFF', 'pending'),
(4, '2025-08-04 02:28:07', 'relay2', 0, 'User menyalakan relay2 ke ON', 'pending'),
(5, '2025-08-04 13:32:04', 'START', 0, 'Tombol dijalankan, sistem memeriksa kondisi pH', 'pending'),
(6, '2025-08-04 13:32:04', '-', 0, 'Sistem dijalankan manual melalui tombol, belum tentu memberi POC', 'pending'),
(7, '2025-08-04 14:18:09', 'N1', 20, 'POC otomatis via N1 (a.py)', 'pending'),
(8, '2025-08-04 14:22:20', 'N1', 20, 'POC otomatis via N1 (a.py)', 'pending'),
(9, '2025-08-04 14:31:48', 'N1', 20, 'POC otomatis via N1 (a.py)', 'pending'),
(10, '2025-08-04 14:36:22', 'N1', 20, 'POC otomatis via N1 (a.py)', 'pending'),
(11, '2025-08-04 14:37:10', 'N1', 20, 'POC otomatis via N1 (a.py)', 'pending'),
(12, '2025-08-04 14:52:42', 'N1', 20, 'POC otomatis via N1 (a.py)', 'pending'),
(13, '2025-08-04 14:53:32', 'N1', 20, 'POC otomatis via N1 (a.py)', 'pending'),
(14, '2025-08-04 14:54:23', 'N1', 20, 'POC otomatis via N1 (a.py)', 'pending'),
(15, '2025-08-04 14:55:14', 'N1', 20, 'POC otomatis via N1 (a.py)', 'pending'),
(16, '2025-08-04 14:57:00', 'N1', 20, 'POC otomatis via N1 (a.py)', 'pending'),
(17, '2025-08-04 15:10:59', 'relay1', 0, 'User menyalakan relay1 ke ON', 'pending'),
(18, '2025-08-04 15:11:00', 'relay1', 0, 'User menyalakan relay1 ke OFF', 'pending'),
(19, '2025-08-04 20:29:36', 'N1', 20, 'POC otomatis via N1 (a.py)', 'pending'),
(20, '2025-08-04 20:30:48', 'N1', 20, 'POC otomatis via N1 (a.py)', 'pending'),
(21, '2025-08-04 20:31:14', 'N1', 20, 'POC otomatis via N1 (a.py)', 'pending'),
(22, '2025-08-04 20:31:56', 'relay1', 0, 'User menyalakan relay1 ke OFF', 'pending'),
(23, '2025-08-04 20:31:57', 'relay1', 0, 'User menyalakan relay1 ke ON', 'pending'),
(24, '2025-08-04 20:45:45', 'N1', 20, 'POC otomatis via N1 (a.py)', 'pending');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `evaluasi_tinggi`
--
ALTER TABLE `evaluasi_tinggi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `log_manual`
--
ALTER TABLE `log_manual`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `log_tombol`
--
ALTER TABLE `log_tombol`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `relay_log`
--
ALTER TABLE `relay_log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sensor_data`
--
ALTER TABLE `sensor_data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tindakan`
--
ALTER TABLE `tindakan`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `evaluasi_tinggi`
--
ALTER TABLE `evaluasi_tinggi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `log_manual`
--
ALTER TABLE `log_manual`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `log_tombol`
--
ALTER TABLE `log_tombol`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `relay_log`
--
ALTER TABLE `relay_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `sensor_data`
--
ALTER TABLE `sensor_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `tindakan`
--
ALTER TABLE `tindakan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
