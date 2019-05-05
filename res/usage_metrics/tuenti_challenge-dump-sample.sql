-- MySQL dump 10.17  Distrib 10.3.12-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: tuenti_challenge
-- ------------------------------------------------------
-- Server version	10.3.12-MariaDB-1:10.3.12+maria~bionic

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activity`
--

DROP TABLE IF EXISTS `activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activity` (
  `date_time` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `action` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity`
--

LOCK TABLES `activity` WRITE;
/*!40000 ALTER TABLE `activity` DISABLE KEYS */;
INSERT INTO `activity` VALUES ('2018-02-21 15:53:48',96,'close'),('2018-02-21 15:53:44',96,'action2'),('2018-02-21 16:29:22',122,'close'),('2018-02-21 15:51:51',96,'open'),('2018-02-21 15:52:57',96,'action6'),('2018-02-21 16:29:19',122,'open'),('2018-02-21 16:29:20',122,'action1'),('2018-02-21 16:50:00',122,'open'),('2018-02-21 16:50:20',122,'action1'),('2018-02-21 16:50:40',122,'action2'),('2018-02-21 08:00:00',101,'open'),('2018-02-21 08:00:30',101,'action1'),('2018-02-21 08:01:00',101,'action2'),('2018-02-21 08:02:00',101,'close'),('2018-02-21 08:15:00',101,'action1'),('2018-02-21 08:17:00',101,'action3'),('2018-02-21 09:00:00',101,'open'),('2018-02-21 09:00:28',101,'action1'),('2018-02-21 09:03:00',101,'action2'),('2018-02-21 10:00:00',101,'open'),('2018-02-21 10:00:30',101,'action1'),('2018-02-21 10:01:00',101,'action2'),('2018-02-21 10:02:00',101,'close'),('2018-02-21 11:00:00',101,'action1'),('2018-02-21 11:02:15',101,'action2'),('2018-02-21 11:03:45',101,'close'),('2018-02-21 12:00:00',101,'action1'),('2018-02-21 12:02:20',101,'action2'),('2018-02-21 11:00:00',201,'action2'),('2018-02-21 11:00:00',201,'action2'),('2018-02-21 11:00:00',202,'action4');
/*!40000 ALTER TABLE `activity_sample` ENABLE KEYS */;
UNLOCK TABLES;


/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-09 21:39:52
