-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 30, 2018 at 02:56 PM
-- Server version: 5.7.22-0ubuntu18.04.1
-- PHP Version: 7.2.7-0ubuntu0.18.04.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `metablock`
--

-- --------------------------------------------------------

--
-- Table structure for table `stats_rebuild`
--

CREATE TABLE `stats_rebuild` (
  `id` int(7) NOT NULL,
  `key_name` varchar(100) NOT NULL,
  `time_insertion` double NOT NULL,
  `type` varchar(10) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `stats_rebuild`
--

INSERT INTO `stats_rebuild` (`id`, `key_name`, `time_insertion`, `type`) VALUES
(1, 'test_0.txt', 1532962350.425634, 'All'),
(2, 'test_25.txt', 1532962350.584812, 'All'),
(3, 'test_50.txt', 1532962350.596119, 'All'),
(4, 'test_75.txt', 1532962350.639021, 'All'),
(5, 'test_1.txt', 1532962350.661922, 'All'),
(6, 'test_26.txt', 1532962350.715338, 'All'),
(7, 'test_76.txt', 1532962350.764041, 'All'),
(8, 'test_51.txt', 1532962350.792513, 'All'),
(9, 'test_2.txt', 1532962350.815907, 'All'),
(10, 'test_27.txt', 1532962350.890122, 'All'),
(11, 'test_77.txt', 1532962350.908398, 'All'),
(12, 'test_52.txt', 1532962350.955215, 'All'),
(13, 'test_3.txt', 1532962350.993993, 'All'),
(14, 'test_28.txt', 1532962351.17725, 'All'),
(15, 'test_53.txt', 1532962351.38616, 'All'),
(16, 'test_78.txt', 1532962351.99462, 'All'),
(17, 'test_4.txt', 1532962351.137244, 'All'),
(18, 'test_54.txt', 1532962351.17434, 'All'),
(19, 'test_29.txt', 1532962351.186547, 'All'),
(20, 'test_79.txt', 1532962351.248424, 'All'),
(21, 'test_55.txt', 1532962351.30229, 'All'),
(22, 'test_80.txt', 1532962351.334566, 'All'),
(23, 'test_5.txt', 1532962351.355555, 'All'),
(24, 'test_31.txt', 1532962351.416973, 'All'),
(25, 'test_6.txt', 1532962351.424413, 'All'),
(26, 'test_56.txt', 1532962351.453963, 'All'),
(27, 'test_30.txt', 1532962351.518842, 'All'),
(28, 'test_7.txt', 1532962351.659636, 'All'),
(29, 'test_81.txt', 1532962351.659565, 'All'),
(30, 'test_57.txt', 1532962351.682658, 'All'),
(31, 'test_58.txt', 1532962351.723997, 'All'),
(32, 'test_32.txt', 1532962351.749648, 'All'),
(33, 'test_82.txt', 1532962351.753856, 'All'),
(34, 'test_33.txt', 1532962351.79283, 'All'),
(35, 'test_9.txt', 1532962351.822795, 'All'),
(36, 'test_83.txt', 1532962351.852179, 'All'),
(37, 'test_8.txt', 1532962351.879498, 'All'),
(38, 'test_34.txt', 1532962351.907021, 'All'),
(39, 'test_59.txt', 1532962351.998091, 'All'),
(40, 'test_84.txt', 1532962352.4443, 'All'),
(41, 'test_10.txt', 1532962352.68968, 'All'),
(42, 'test_35.txt', 1532962352.7664, 'All'),
(43, 'test_85.txt', 1532962352.132091, 'All'),
(44, 'test_60.txt', 1532962352.201889, 'All'),
(45, 'test_11.txt', 1532962352.215163, 'All'),
(46, 'test_86.txt', 1532962352.25741, 'All'),
(47, 'test_61.txt', 1532962352.291664, 'All'),
(48, 'test_36.txt', 1532962352.313869, 'All'),
(49, 'test_87.txt', 1532962352.376128, 'All'),
(50, 'test_62.txt', 1532962352.405952, 'All'),
(51, 'test_12.txt', 1532962352.443237, 'All'),
(52, 'test_37.txt', 1532962352.460502, 'All'),
(53, 'test_13.txt', 1532962352.497095, 'All'),
(54, 'test_63.txt', 1532962352.543746, 'All'),
(55, 'test_14.txt', 1532962352.551889, 'All'),
(56, 'test_39.txt', 1532962352.569923, 'All'),
(57, 'test_38.txt', 1532962352.56946, 'All'),
(58, 'test_88.txt', 1532962352.604615, 'All'),
(59, 'test_89.txt', 1532962352.674423, 'All'),
(60, 'test_64.txt', 1532962352.727702, 'All'),
(61, 'test_15.txt', 1532962352.737228, 'All'),
(62, 'test_40.txt', 1532962352.780911, 'All'),
(63, 'test_65.txt', 1532962352.800216, 'All'),
(64, 'test_41.txt', 1532962352.866558, 'All'),
(65, 'test_90.txt', 1532962352.876534, 'All'),
(66, 'test_16.txt', 1532962352.920061, 'All'),
(67, 'test_17.txt', 1532962352.971087, 'All'),
(68, 'test_66.txt', 1532962352.97841, 'All'),
(69, 'test_42.txt', 1532962353.2568, 'All'),
(70, 'test_91.txt', 1532962353.37334, 'All'),
(71, 'test_92.txt', 1532962353.52672, 'All'),
(72, 'test_67.txt', 1532962353.52601, 'All'),
(73, 'test_18.txt', 1532962353.11831, 'All'),
(74, 'test_68.txt', 1532962353.222978, 'All'),
(75, 'test_93.txt', 1532962353.258058, 'All'),
(76, 'test_43.txt', 1532962353.265715, 'All'),
(77, 'test_19.txt', 1532962353.295308, 'All'),
(78, 'test_69.txt', 1532962353.321853, 'All'),
(79, 'test_44.txt', 1532962353.348571, 'All'),
(80, 'test_45.txt', 1532962353.386285, 'All'),
(81, 'test_94.txt', 1532962353.418561, 'All'),
(82, 'test_20.txt', 1532962353.437756, 'All'),
(83, 'test_95.txt', 1532962353.543053, 'All'),
(84, 'test_70.txt', 1532962353.543695, 'All'),
(85, 'test_21.txt', 1532962353.620275, 'All'),
(86, 'test_46.txt', 1532962353.647958, 'All'),
(87, 'test_71.txt', 1532962353.646526, 'All'),
(88, 'test_96.txt', 1532962353.684398, 'All'),
(89, 'test_22.txt', 1532962353.727709, 'All'),
(90, 'test_97.txt', 1532962353.762424, 'All'),
(91, 'test_47.txt', 1532962353.794103, 'All'),
(92, 'test_23.txt', 1532962353.80662, 'All'),
(93, 'test_72.txt', 1532962353.847506, 'All'),
(94, 'test_98.txt', 1532962353.910634, 'All'),
(95, 'test_48.txt', 1532962353.914391, 'All'),
(96, 'test_73.txt', 1532962353.91285, 'All'),
(97, 'test_24.txt', 1532962353.935221, 'All'),
(98, 'test_74.txt', 1532962353.953492, 'All'),
(99, 'test_49.txt', 1532962353.954946, 'All'),
(100, 'test_99.txt', 1532962353.966079, 'All');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `stats_rebuild`
--
ALTER TABLE `stats_rebuild`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `stats_rebuild`
--
ALTER TABLE `stats_rebuild`
  MODIFY `id` int(7) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
