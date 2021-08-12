-- DROP TABLE IF EXISTS `konkur_quiz_bot`.`subjects`;
USE 'konkur_quiz_bot';

CREATE TABLE `subjects` (
  `id` INT NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_persian_ci;

INSERT INTO `subjects` VALUES ('1', 'حسابان 1');
INSERT INTO `subjects` VALUES ('2', 'حسابان 2');
INSERT INTO `subjects` VALUES ('3', 'ادبیات');
INSERT INTO `subjects` VALUES ('4', 'زبان');
INSERT INTO `subjects` VALUES ('5', 'دینی');
