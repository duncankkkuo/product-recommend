CREATE TABLE 'recommend' (
      'prod_oid' int(6) DEFAULT NULL,
      'similar_prod_oid' int(6) DEFAULT NULL,
      'score' double DEFAULT NULL,
      'country_cd' varchar(30) DEFAULT NULL,
      'city_cd' varchar(30) DEFAULT NULL,
      'create_time' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
