-- TPC-H Query
SELECT `l_orderkey`
     , SUM(`l_extendedprice` * (1 - `l_discount`)) AS `revenue`
     , `o_orderdate`
     , `o_shippriority`
  FROM `customer` AS `c`
  JOIN `orders` AS `o`
    ON `c`.`c_custkey` = `o`.`o_custkey`
  JOIN `lineitem` AS `l`
    ON `l`.`l_orderkey` = `o`.`o_orderkey`
 WHERE `c`.`c_mktsegment` = 'BUILDING'
    AND `o`.`o_orderdate` < DATE '1995-03-15'
    AND `l`.`l_shipdate` > DATE '1995-03-15'
GROUP BY `l_orderkey`
         , `o_orderdate`
       , `o_shippriority`
ORDER BY `revenue` DESC
       , `o_orderdate`
LIMIT 10;