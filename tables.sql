CREATE USER 'admin_cp'@'localhost' IDENTIFIED BY 'qwer1234';
GRANT ALL PRIVILEGES ON stats.* TO 'admin_cp'@'localhost';

CREATE DATABASE  IF NOT EXISTS `stats` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `stats`;
-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: stats
-- ------------------------------------------------------
-- Server version	5.7.40-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `abusers`
--

DROP TABLE IF EXISTS `abusers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `abusers` (
  `gp_id` varchar(24) NOT NULL,
  PRIMARY KEY (`gp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `abusers`
--

LOCK TABLES `abusers` WRITE;
/*!40000 ALTER TABLE `abusers` DISABLE KEYS */;
/*!40000 ALTER TABLE `abusers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_details`
--

DROP TABLE IF EXISTS `account_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_details` (
  `gp_id` varchar(24) NOT NULL,
  `nickname` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`gp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_details`
--

LOCK TABLES `account_details` WRITE;
/*!40000 ALTER TABLE `account_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `coalesced_history`
--

DROP TABLE IF EXISTS `coalesced_history`;
/*!50001 DROP VIEW IF EXISTS `coalesced_history`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `coalesced_history` AS SELECT 
 1 AS `aggregated_at`,
 1 AS `gp_id`,
 1 AS `total_bet`,
 1 AS `total_win`,
 1 AS `profit`,
 1 AS `rtp`,
 1 AS `bet_count`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `coalesced_stats`
--

DROP TABLE IF EXISTS `coalesced_stats`;
/*!50001 DROP VIEW IF EXISTS `coalesced_stats`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `coalesced_stats` AS SELECT 
 1 AS `gp_id`,
 1 AS `num_days_won`,
 1 AS `total_days`,
 1 AS `win_percentage`,
 1 AS `profit`,
 1 AS `bet_count`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `win_history`
--

DROP TABLE IF EXISTS `win_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `win_history` (
  `aggregated_at` date NOT NULL,
  `gp_id` varchar(24) NOT NULL,
  `game_code` varchar(64) NOT NULL,
  `total_bet` float DEFAULT NULL,
  `total_win` float DEFAULT NULL,
  `profit` float DEFAULT NULL,
  `rtp` float DEFAULT NULL,
  `bet_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`aggregated_at`,`gp_id`,`game_code`),
  UNIQUE KEY `aggregation_key` (`aggregated_at`,`gp_id`,`game_code`),
  KEY `idx_rtps` (`aggregated_at`,`gp_id`,`game_code`,`profit`,`bet_count`),
  KEY `idx_rtps1` (`aggregated_at`,`gp_id`,`game_code`,`rtp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `win_history`
--

LOCK TABLES `win_history` WRITE;
/*!40000 ALTER TABLE `win_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `win_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `coalesced_history`
--

/*!50001 DROP VIEW IF EXISTS `coalesced_history`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `coalesced_history` AS (select `win_history`.`aggregated_at` AS `aggregated_at`,`win_history`.`gp_id` AS `gp_id`,round(sum(`win_history`.`total_bet`),2) AS `total_bet`,round(sum(`win_history`.`total_win`),2) AS `total_win`,round(sum(`win_history`.`profit`),2) AS `profit`,round((sum(`win_history`.`total_win`) / sum(`win_history`.`total_bet`)),2) AS `rtp`,sum(`win_history`.`bet_count`) AS `bet_count` from `win_history` group by `win_history`.`gp_id`,`win_history`.`aggregated_at` order by `win_history`.`gp_id`,`win_history`.`aggregated_at` desc) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `coalesced_stats`
--

/*!50001 DROP VIEW IF EXISTS `coalesced_stats`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `coalesced_stats` AS (select `coalesced_history`.`gp_id` AS `gp_id`,sum(if((`coalesced_history`.`rtp` >= 1),1,0)) AS `num_days_won`,count(0) AS `total_days`,(sum(if((`coalesced_history`.`rtp` >= 1),1,0)) / count(0)) AS `win_percentage`,round(sum(`coalesced_history`.`profit`),2) AS `profit`,sum(`coalesced_history`.`bet_count`) AS `bet_count` from `coalesced_history` group by `coalesced_history`.`gp_id`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-05  0:20:02
