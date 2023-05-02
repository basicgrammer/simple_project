-- test_db.auth_app_profile definition

CREATE TABLE `auth_app_profile` (
  `profile_pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_pw` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_num` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `regi_date` datetime(6) NOT NULL,
  PRIMARY KEY (`profile_pk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- test_db.auth_app_token definition

CREATE TABLE `auth_app_token` (
  `token_pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `refresh_token` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `relation_id` int(11) NOT NULL,
  PRIMARY KEY (`token_pk_id`),
  UNIQUE KEY `relation_id` (`relation_id`),
  CONSTRAINT `auth_app_token_relation_id_ae604d94_fk_auth_app_` FOREIGN KEY (`relation_id`) REFERENCES `auth_app_profile` (`profile_pk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;