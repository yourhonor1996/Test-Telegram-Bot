USE 'konkur_quiz_bot';

CREATE TABLE `questions` (
  `id` INT NOT NULL,
  `text` VARCHAR(1000) NOT NULL,
  `choice_1` VARCHAR(500) NOT NULL,
  `choice_2` VARCHAR(500) NOT NULL,
  `choice_3` VARCHAR(500) NOT NULL,
  `choice_4` VARCHAR(500) NOT NULL,
  `right_choice` TINYINT(1) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_persian_ci;


INSERT INTO `questions` VALUES ('1', 'question 1', '1', '2', '3', '4', '1');
INSERT INTO `questions` VALUES ('2', 'question 2', '1', '2', '3', '4', '2');
INSERT INTO `questions` VALUES ('3', 'question 3', '1', '2', '3', '4', '2');
INSERT INTO `questions` VALUES ('4', 'question 4', '1', '2', '3', '4', '2');
INSERT INTO `questions` VALUES ('5', 'question 5', '1', '2', '3', '4', '3');
INSERT INTO `questions` VALUES ('6', 'question 6', '1', '2', '3', '4', '3');
INSERT INTO `questions` VALUES ('7', 'question 7', '1', '2', '3', '4', '3');
INSERT INTO `questions` VALUES ('8', 'question 8', '1', '2', '3', '4', '3');
INSERT INTO `questions` VALUES ('9', 'question 9', '1', '2', '3', '4', '2');
INSERT INTO `questions` VALUES ('10', 'question 10', '1', '2', '3', '4', '2');
INSERT INTO `questions` VALUES ('11', 'question 11', '1', '2', '3', '4', '4');
INSERT INTO `questions` VALUES ('12', 'question 12', '1', '2', '3', '4', '4');
INSERT INTO `questions` VALUES ('13', 'question 13', '1', '2', '3', '4', '4');
INSERT INTO `questions` VALUES ('14', 'question 14', '1', '2', '3', '4', '4');
INSERT INTO `questions` VALUES ('15', 'question 15', '1', '2', '3', '4', '2');
INSERT INTO `questions` VALUES ('16', 'question 16', '1', '2', '3', '4', '1');
INSERT INTO `questions` VALUES ('17', 'question 17', '1', '2', '3', '4', '1');
INSERT INTO `questions` VALUES ('18', 'question 18', '1', '2', '3', '4', '1');
INSERT INTO `questions` VALUES ('19', 'question 19', '1', '2', '3', '4', '1');
INSERT INTO `questions` VALUES ('20', 'question 20', '1', '2', '3', '4', '4');
