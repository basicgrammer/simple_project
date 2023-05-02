-- test_db.platform_app_product definition

CREATE TABLE `platform_app_product` (
  `p_pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `p_category` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `p_price` int(11) NOT NULL,
  `p_cost` int(11) NOT NULL,
  `p_name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `p_subscription` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `p_barcode` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `p_expire_date` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `p_size` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `p_delete_check` tinyint(1) NOT NULL,
  `p_regi_user` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `p_regi_date` datetime(6) NOT NULL,
  `p_fix_date` datetime(6) NOT NULL,
  `p_keyword` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`p_pk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;