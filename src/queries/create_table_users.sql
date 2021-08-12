-- DROP TABLE IF EXISTS `konkur_quiz_bot`.`subjects`;

CREATE TABLE `konkur_quiz_bot`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `chat_id` BIGINT NOT NULL,
  `first_name` VARCHAR(50) NULL,
  `last_name` VARCHAR(50) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `chat_id_UNIQUE` (`chat_id` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_persian_ci;
