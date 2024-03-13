---> run raw_convert_to_min
---> run min_convert_to_date
---> run raw_convert_to_date
---> run run_adjust_date

-----------raw_convert_to_min-------------
-----------Create Table Byday-------------
DROP TABLE IF EXISTS clean_bymin_from_raw;

CREATE TABLE clean_bymin_from_raw AS
SELECT 
min_convert_from_raw.*
,il."InverterName"
FROM (
--1----globalprosolarmanpv

SELECT 
"Loan","Date","time",
ROUND(SUM(COALESCE(CAST((case when ProductionkW in ('--','','nan') then '0' else ProductionkW end) AS float),0)),2) as "Power(Kw/h)",
ROUND(SUM(ABS(COALESCE(CAST((case when GridkW in ('--','','nan') then '0' else GridkW end) AS float),0))),2) as "Grid Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when ConsumptionkW in ('--','','nan') then '0' else ConsumptionkW end) AS float),0)),2) as "Consumption(Kw/h)",
ROUND(SUM(COALESCE(-CAST((case when ChargekW in ('--','','nan') then '0' else ChargekW end) AS float),0)),2) as "BatteryCharge(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when DischargekW in ('--','','nan') then '0' else DischargekW end) AS float),0)),2) as "BatteryDisCharge(Kw/h)"
FROM min_globalprosolarmanpvcom
GROUP BY "Loan","Date","time"

union all
--2----prosolarmanpvcom

SELECT 
"Loan","Date","time",
ROUND(SUM(COALESCE(CAST((case when ProductionkW in ('--','','nan') then '0' else ProductionkW end) AS float),0)),2) as "Power(Kw/h)",
ROUND(SUM(ABS(COALESCE(CAST((case when GridkW in ('--','','nan') then '0' else GridkW end) AS float),0))),2) as "Grid Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when ConsumptionkW in ('--','','nan') then '0' else ConsumptionkW end) AS float),0)),2) as "Consumption(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when ChargekW in ('--','','nan') then '0' else ChargekW end) AS float),0)),2) as "BatteryCharge(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when DischargekW in ('--','','nan') then '0' else DischargekW end) AS float),0)),2) as "BatteryDisCharge(Kw/h)"
FROM min_prosolarmanpvcom
GROUP BY "Loan","Date","time"

union all
--3----homesolarmanpvcom

SELECT 
"Loan","Date","time",
ROUND(SUM(CAST((case when ProductionPowerW in ('--','','nan') then '0' else ProductionPowerW end) AS float)/1000),2) as "Power(Kw/h)",
ROUND(SUM(ABS(CAST((case when GridPowerW in ('--','','nan') then '0' else GridPowerW end) AS float)/1000)),2) as "Grid Power(Kw/h)",
ROUND(SUM(CAST((case when ConsumptionPowerW in ('--','','nan') then '0' else ConsumptionPowerW end) AS float)/1000),2) as "Consumption(Kw/h)",
ROUND(SUM(ABS(CAST((case when ChargingPowerW in ('--','','nan') then '0' else ChargingPowerW end) AS float)/1000)),2) as  "BatteryCharge(Kw/h)", 
ROUND(SUM(CAST((case when DischargingPowerW in ('--','','nan') then '0' else DischargingPowerW end) AS float)/1000),2) as "BatteryDisCharge(Kw/h)"
FROM min_homesolarmanpvcom 
where  CAST((case when GridPowerW in ('--','','nan') then '0' else GridPowerW end) AS float) < 6000000
GROUP BY "Loan","Date","time"

union all
--4----servergrowattcom

SELECT
"Loan","Date","time",
ROUND(SUM(COALESCE((case when loadconsumption in ('--','','nan') or loadconsumption is null then (CAST("photovoltaicoutput" AS float)) else CAST("photovoltaicoutput" AS float) end),0)),2) as "Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when importedfromgrid in ('--','','nan') then '0' else importedfromgrid end) AS float),0)),2) as "Grid Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when loadconsumption in ('--','','nan') then '0' else loadconsumption end) AS float),0)),2) as "Consumption(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when Charging in ('--','','nan') then '0' else Charging end) AS float),0)),2) as "BatteryCharge(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when Discharging in ('--','','nan') then '0' else Discharging end) AS float),0)),2) as "BatteryDisCharge(Kw/h)"
FROM min_servergrowattcom 
where "photovoltaicoutput" <> ''
GROUP BY "Loan","Date","time"

union all
--5----sg5fusionsolarhuaweicom (wrong code date old)

SELECT
"Loan","Date","time",
(ROUND(SUM(COALESCE(CAST((case when productpower in ('--','','nan') then '0' else productpower end) AS float),0)),2)) as "Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when meterActivePower in ('--','','nan') then '0' else meterActivePower end) AS float),0)),2) as "Grid Power(Kw/h)",
(ROUND(SUM(COALESCE(CAST((case when usepower in ('--','','nan') then '0' else usepower end) AS float),0)),2)) as "Consumption(Kw/h)",
(ROUND(SUM(COALESCE(-CAST((case when chargepower in ('--','','nan') then '0' else chargepower end) AS float),0)),2)) as  "BatteryCharge(Kw/h)", 
(ROUND(SUM(COALESCE(CAST((case when dischargepower in ('--','','nan') then '0' else dischargepower end) AS float),0)),2)) as "BatteryDisCharge(Kw/h)"
FROM min_sg5fusionsolarhuaweicom
GROUP BY "Loan","Date","time"

union all
--6----wwwisolarcloudcom

SELECT 
"Loan","Date","time",
ROUND(SUM(COALESCE(CAST((case when PVW in ('--','','nan') then '0' else PVW end) AS float)/1000,0)),2) as "Power(Kw/h)",
ROUND(SUM(ABS(COALESCE(CAST((case when GridW in ('--','','nan') then '0' else GridW end) AS float)/1000,0))),2) as "Grid Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when LoadW in ('--','','nan') then '0' else LoadW end) AS float)/1000,0)),2) as "Consumption(Kw/h)",
0 "BatteryCharge(Kw/h)", 0 "BatteryDisCharge(Kw/h)"
FROM min_wwwisolarcloudcom
GROUP BY "Loan","Date","time"

union all
--7----wwwsemsportalcom

SELECT 
"Loan","Date","time",
ROUND(SUM(COALESCE(CAST((case when PVW in ('','0','nan') then '0' else PVW end) AS float)/1000,0)),2) as "Power(Kw/h)",
ROUND(SUM(ABS(COALESCE(CAST((case when MeterW in ('','0','nan') then '0' else MeterW end) AS float)/1000,0))),2) as "Grid Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when LoadW in ('','0','nan') then '0' else LoadW end) AS float)/1000,0)),2) as "Consumption(Kw/h)",
ROUND(SUM(-COALESCE((case when CAST((case when batteryw in ('','0','nan') then '0' else batteryw end) AS float) < 0 then 
CAST((case when batteryw in ('','0','nan') then '0' else batteryw end) AS float)/1000 else 0 end),0)),2) as "BatteryCharge(Kw/h)",
ROUND(SUM(COALESCE((case when CAST((case when batteryw in ('','0','nan') then '0' else batteryw end) AS float) > 0 then 
CAST((case when batteryw in ('','0','nan') then '0' else batteryw end) AS float)/1000 else 0 end),0)),2) as "BatteryDisCharge(Kw/h)"
FROM min_wwwsemsportalcom
GROUP BY "Loan","Date","time"

union all
--8----serverluxpowertekcom

SELECT  
"Loan","Date","time",
ROUND(SUM(
  COALESCE(CAST((case when ppv1 in ('','0','nan') then '0' else ppv1 end) AS float),0) +
  COALESCE(CAST((case when ppv2 in ('','0','nan') then '0' else ppv2 end) AS float),0) +
  COALESCE(CAST((case when ppv3 in ('','0','nan') then '0' else ppv3 end) AS float),0)
)/1000,2) AS "Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when pToUser in ('','0','nan') then '0' else pToUser end) AS float)/1000,0)),2) as "Grid Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when pLoad in ('','0','nan') then '0' else pLoad end) AS float)/1000,0)),2) as "Consumption(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when pCharge in ('','0','nan') then '0' else pCharge end) AS float)/1000,0)),2) as "BatteryCharge(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when pDisCharge in ('','0','nan') then '0' else pDisCharge end) AS float),0))/1000,2) as "BatteryDisCharge(Kw/h)"
FROM min_serverluxpowertekcom
GROUP BY "Loan","Date","time"

union all
--9----wwwsoliscloudcom

SELECT
"Loan","Date","time",
ROUND(SUM(COALESCE(CAST((case when TotalInverterPowerW in ('','0','nan') then '0' else TotalInverterPowerW end) AS float)/1000,0)),2) as "Power(Kw/h)",
ROUND(SUM(COALESCE(-CAST((case when GridTotalActivePowerW in ('','0','nan') then '0' else GridTotalActivePowerW end) AS float)/1000,0)),2) as "Grid Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when TotalConsumeEnergyPowerW in ('','0','nan') then '0' else TotalConsumeEnergyPowerW end) AS float)/1000,0)),2) as "Consumption(Kw/h)",
ROUND(SUM(COALESCE((case when CAST((case when BatteryPowerW in ('','0','nan') then '0' else BatteryPowerW end) AS float) >= 0 then 
CAST((case when BatteryPowerW in ('','0','nan') then '0' else BatteryPowerW end) AS float)/1000 else 0 end),0)),2) as "BatteryCharge(Kw/h)",
ROUND(SUM(-COALESCE((case when CAST((case when BatteryPowerW in ('','0','nan') then '0' else BatteryPowerW end) AS float)/1000 < 0 then 
CAST((case when BatteryPowerW in ('','0','nan') then '0' else BatteryPowerW end) AS float) else 0 end),0)),2) as "BatteryDisCharge(Kw/h)"
FROM min_wwwsoliscloudcom
GROUP BY "Loan","Date","time"
) as min_convert_from_raw
LEFT JOIN info_loan as il
ON  min_convert_from_raw."Loan" = il."LoanID"
ORDER BY "Date" desc;


-----------min_convert_to_date-------------
-----------Create Table Byday-------------
DROP TABLE IF EXISTS clean_byday_from_min;

CREATE TABLE clean_byday_from_min AS
SELECT 
date_convert_from_min.*,
il."InverterName",
il."Region",
il."installed_capacity"
FROM (
--1----globalprosolarmanpv

SELECT 
"Loan","Date",
ROUND(SUM(COALESCE(CAST((case when ProductionkW in ('--','','nan') then '0' else ProductionkW end) AS float),0)*5/60),2) as "Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when GridkW in ('--','','nan') then '0' else GridkW end) AS float),0)*5/60),2) as "Grid Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when ConsumptionkW in ('--','','nan') then '0' else ConsumptionkW end) AS float),0)*5/60),2) as "Consumption(Kw/h)",
ROUND(SUM(COALESCE(-CAST((case when ChargekW in ('--','','nan') then '0' else ChargekW end) AS float),0)*5/60),2) as "BatteryCharge(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when DischargekW in ('--','','nan') then '0' else DischargekW end) AS float),0)*5/60),2) as "BatteryDisCharge(Kw/h)"
FROM min_globalprosolarmanpvcom
GROUP BY "Loan","Date"

union all
--2----prosolarmanpvcom

SELECT 
"Loan","Date",
ROUND(SUM(COALESCE(CAST((case when ProductionkW in ('--','','nan') then '0' else ProductionkW end) AS float),0)*5/60),2) as "Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when GridkW in ('--','','nan') then '0' else GridkW end) AS float),0)*5/60),2) as "Grid Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when ConsumptionkW in ('--','','nan') then '0' else ConsumptionkW end) AS float),0)*5/60),2) as "Consumption(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when ChargekW in ('--','','nan') then '0' else ChargekW end) AS float),0)*5/60),2) as "BatteryCharge(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when DischargekW in ('--','','nan') then '0' else DischargekW end) AS float),0)*5/60),2) as "BatteryDisCharge(Kw/h)"
FROM min_prosolarmanpvcom
GROUP BY "Loan","Date"

union all
--3----homesolarmanpvcom

SELECT 
"Loan","Date",
ROUND(SUM(CAST((case when ProductionPowerW in ('--','','nan') then '0' else ProductionPowerW end) AS float)*5/60/1000),2) as "Power(Kw/h)",
ROUND(SUM(CAST((case when GridPowerW in ('--','','nan') then '0' else GridPowerW end) AS float)*5/60/1000),2) as "Grid Power(Kw/h)",
ROUND(SUM(CAST((case when ConsumptionPowerW in ('--','','nan') then '0' else ConsumptionPowerW end) AS float)*5/60/1000),2) as "Consumption(Kw/h)",
ROUND(SUM(-CAST((case when ChargingPowerW in ('--','','nan') then '0' else ChargingPowerW end) AS float)*5/60/1000),2) as  "BatteryCharge(Kw/h)", 
ROUND(SUM(CAST((case when DischargingPowerW in ('--','','nan') then '0' else DischargingPowerW end) AS float)*5/60/1000),2) as "BatteryDisCharge(Kw/h)"
FROM min_homesolarmanpvcom 
where  CAST((case when GridPowerW in ('--','','nan') then '0' else GridPowerW end) AS float) < 6000000
GROUP BY "Loan","Date"

union all
--4----servergrowattcom

SELECT
"Loan","Date",
ROUND(SUM(COALESCE((case when loadconsumption in ('--','','nan') or loadconsumption is null then (CAST("photovoltaicoutput" AS float)/1000) else CAST("photovoltaicoutput" AS float) end),0)*5/60),2) as "Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when importedfromgrid in ('--','','nan') then '0' else importedfromgrid end) AS float),0)*5/60),2) as "Grid Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when loadconsumption in ('--','','nan') then '0' else loadconsumption end) AS float),0)*5/60),2) as "Consumption(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when Charging in ('--','','nan') then '0' else Charging end) AS float),0)*5/60),2) as "BatteryCharge(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when Discharging in ('--','','nan') then '0' else Discharging end) AS float),0)*5/60),2) as "BatteryDisCharge(Kw/h)"
FROM min_servergrowattcom 
where "photovoltaicoutput" <> ''
GROUP BY "Loan","Date"

union all
--5----sg5fusionsolarhuaweicom (wrong code date old)

SELECT
"Loan","Date",
(ROUND(SUM(COALESCE(CAST((case when productpower in ('--','','nan') then '0' else productpower end) AS float),0)*5/60),2)) as "Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when meterActivePower in ('--','','nan') then '0' else meterActivePower end) AS float),0)*5/60),2) as "Grid Power(Kw/h)",
(ROUND(SUM(COALESCE(CAST((case when usepower in ('--','','nan') then '0' else usepower end) AS float),0)*5/60),2)) as "Consumption(Kw/h)",
(ROUND(SUM(COALESCE(CAST((case when chargepower in ('--','','nan') then '0' else chargepower end) AS float),0)*5/60),2)) as  "BatteryCharge(Kw/h)", 
(ROUND(SUM(COALESCE(CAST((case when dischargepower in ('--','','nan') then '0' else dischargepower end) AS float),0)*5/60),2)) as "BatteryDisCharge(Kw/h)"
FROM min_sg5fusionsolarhuaweicom
GROUP BY "Loan","Date"

union all
--6----wwwisolarcloudcom

SELECT 
"Loan","Date",
ROUND(SUM(COALESCE(CAST((case when PVW in ('--','','nan') then '0' else PVW end) AS float),0)*5/60/1000),2) as "Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when GridW in ('--','','nan') then '0' else GridW end) AS float),0)*5/60/1000),2) as "Grid Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when LoadW in ('--','','nan') then '0' else LoadW end) AS float),0)*5/60/1000),2) as "Consumption(Kw/h)",
0 "BatteryCharge(Kw/h)", 0 "BatteryDisCharge(Kw/h)"
FROM min_wwwisolarcloudcom
GROUP BY "Loan","Date"

union all
--7----wwwsemsportalcom

SELECT 
"Loan","Date",
ROUND(SUM(COALESCE(CAST((case when PVW in ('','0','nan') then '0' else PVW end) AS float),0)*5/60/1000),2) as "Power(Kw/h)",
ROUND(SUM(COALESCE(-CAST((case when MeterW in ('','0','nan') then '0' else MeterW end) AS float),0)*5/60/1000),2) as "Grid Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when LoadW in ('','0','nan') then '0' else LoadW end) AS float),0)*5/60/1000),2) as "Consumption(Kw/h)",
ROUND(SUM(-COALESCE((case when CAST((case when batteryw in ('','0','nan') then '0' else batteryw end) AS float) < 0 then 
CAST((case when batteryw in ('','0','nan') then '0' else batteryw end) AS float) else 0 end),0)*5/60/1000),2) as "BatteryCharge(Kw/h)",
ROUND(SUM(COALESCE((case when CAST((case when batteryw in ('','0','nan') then '0' else batteryw end) AS float) > 0 then 
CAST((case when batteryw in ('','0','nan') then '0' else batteryw end) AS float) else 0 end),0)*5/60/1000),2) as "BatteryDisCharge(Kw/h)"
FROM min_wwwsemsportalcom
GROUP BY "Loan","Date"

union all
--8----serverluxpowertekcom

SELECT  
"Loan","Date",
ROUND(SUM(
  COALESCE(CAST((case when ppv1 in ('','0','nan') then '0' else ppv1 end) AS float),0)*5/60/1000 +
  COALESCE(CAST((case when ppv2 in ('','0','nan') then '0' else ppv2 end) AS float),0)*5/60/1000 +
  COALESCE(CAST((case when ppv3 in ('','0','nan') then '0' else ppv3 end) AS float),0)*5/60/1000
),2) AS "Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when pToUser in ('','0','nan') then '0' else pToUser end) AS float),0)*5/60/1000),2) as "Grid Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when pLoad in ('','0','nan') then '0' else pLoad end) AS float),0)*5/60/1000),2) as "Consumption(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when pCharge in ('','0','nan') then '0' else pCharge end) AS float),0)*5/60/1000),2) as "BatteryCharge(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when pDisCharge in ('','0','nan') then '0' else pDisCharge end) AS float),0)*5/60/1000),2) as "BatteryDisCharge(Kw/h)"
FROM min_serverluxpowertekcom
GROUP BY "Loan","Date"

union all
--9----wwwsoliscloudcom

SELECT
"Loan","Date",
ROUND(SUM(COALESCE(CAST((case when TotalInverterPowerW in ('','0','nan') then '0' else TotalInverterPowerW end) AS float),0)*5/60/1000),2) as "Power(Kw/h)",
ROUND(SUM(COALESCE(-CAST((case when GridTotalActivePowerW in ('','0','nan') then '0' else GridTotalActivePowerW end) AS float),0)*5/60/1000),2) as "Grid Power(Kw/h)",
ROUND(SUM(COALESCE(CAST((case when TotalConsumeEnergyPowerW in ('','0','nan') then '0' else TotalConsumeEnergyPowerW end) AS float),0)*5/60/1000),2) as "Consumption(Kw/h)",
ROUND(SUM(COALESCE((case when CAST((case when BatteryPowerW in ('','0','nan') then '0' else BatteryPowerW end) AS float) >= 0 then 
CAST((case when BatteryPowerW in ('','0','nan') then '0' else BatteryPowerW end) AS float) else 0 end),0)*5/60/1000),2) as "BatteryCharge(Kw/h)",
ROUND(SUM(-COALESCE((case when CAST((case when BatteryPowerW in ('','0','nan') then '0' else BatteryPowerW end) AS float) < 0 then 
CAST((case when BatteryPowerW in ('','0','nan') then '0' else BatteryPowerW end) AS float) else 0 end),0)*5/60/1000),2) as "BatteryDisCharge(Kw/h)"
FROM min_wwwsoliscloudcom
GROUP BY "Loan","Date"
) as date_convert_from_min 
LEFT JOIN info_loan as il
ON  date_convert_from_min."Loan" = il."LoanID"
ORDER BY "Date" desc;


-----------raw_convert_to_date-------------
-----------Create Table Byday from raw date-------------
DROP TABLE IF EXISTS clean_byday_from_raw;

CREATE TABLE clean_byday_from_raw AS
SELECT * FROM (

--1----globalprosolarmanpv
SELECT
"Loan","Date",
ROUND(COALESCE(CAST((case when DailyProductionkWh in ('--','','nan') then '0' else DailyProductionkWh end) AS float),0),2) as "Power(Kw/h)",
ROUND(COALESCE(CAST((case when DailyEnergyPurchasedkWh in ('--','','nan') then '0' else DailyEnergyPurchasedkWh end) AS float),0),2) as "Grid Power(Kw/h)",
ROUND(COALESCE(CAST((case when DailyConsumptionkWh in ('--','','nan') then '0' else DailyConsumptionkWh end) AS float),0),2) as "Consumption(Kw/h)",
ROUND(COALESCE(CAST((case when DailyEnergyChargedkWh in ('--','','nan') then '0' else DailyEnergyChargedkWh end) AS float),0),2) as "BatteryCharge(Kw/h)",
ROUND(COALESCE(CAST((case when DailyEnergyDischargedkWh in ('--','','nan') then '0' else DailyEnergyDischargedkWh end) AS float),0),2) as "BatteryDisCharge(Kw/h)"
FROM date_globalprosolarmanpvcom
GROUP BY "Loan","Date"

union all
--2----prosolarmanpvcom

SELECT 
"Loan","Date",
ROUND(COALESCE(CAST((case when DailyProductionkWh in ('--','','nan') then '0' else DailyProductionkWh end) AS float),0),2) as "Power(Kw/h)",
ROUND(COALESCE(CAST((case when DailyEnergyPurchasedkWh in ('--','','nan') then '0' else DailyEnergyPurchasedkWh end) AS float),0),2) as "Grid Power(Kw/h)",
ROUND(COALESCE(CAST((case when DailyConsumptionkWh in ('--','','nan') then '0' else DailyConsumptionkWh end) AS float),0),2) as "Consumption(Kw/h)",
ROUND(COALESCE(CAST((case when DailyEnergyChargedkWh in ('--','','nan') then '0' else DailyEnergyChargedkWh end) AS float),0),2) as "BatteryCharge(Kw/h)",
ROUND(COALESCE(CAST((case when DailyEnergyDischargedkWh in ('--','','nan') then '0' else DailyEnergyDischargedkWh end) AS float),0),2) as "BatteryDisCharge(Kw/h)"
FROM date_prosolarmanpvcom
GROUP BY "Loan","Date"

union all
--3----homesolarmanpvcom

SELECT 
"Loan","Date",
ROUND(CAST((case when ProductionkWh in ('--','','nan') then '0' else ProductionkWh end) AS float),2) as "Power(Kw/h)",
ROUND(CAST((case when EnergyPurchasedkWh in ('--','','nan') then '0' else EnergyPurchasedkWh end) AS float),2) as "Grid Power(Kw/h)",
ROUND(CAST((case when ConsumptionkWh in ('--','','nan') then '0' else ConsumptionkWh end) AS float),2) as "Consumption(Kw/h)",
ROUND(-CAST((case when ChargingEnergykWh in ('--','','nan') then '0' else ChargingEnergykWh end) AS float),2) as  "BatteryCharge(Kw/h)", 
ROUND(CAST((case when DischargingEnergykWh in ('--','','nan') then '0' else DischargingEnergykWh end) AS float),2) as "BatteryDisCharge(Kw/h)"
FROM date_homesolarmanpvcom 
where  CAST((case when EnergyPurchasedkWh in ('--','','nan') then '0' else EnergyPurchasedkWh end) AS float) < 6000000
GROUP BY "Loan","Date"

union all
--4----servergrowattcom

SELECT
"Loan","Date",
ROUND(CAST((case when ProductionkWh in ('--','','nan') then '0' else ProductionkWh end) AS float),2) as "Power(Kw/h)",
ROUND(CAST(('0') AS float),2) as "Grid Power(Kw/h)",
ROUND(CAST(('0') AS float),2) as "Consumption(Kw/h)",
ROUND(CAST(('0') AS float),2) as "BatteryCharge(Kw/h)",
ROUND(CAST(('0') AS float),2) as "BatteryDisCharge(Kw/h)"
FROM date_servergrowattcom 
GROUP BY "Loan","Date"

union all
--5----sg5fusionsolarhuaweicom (wrong code date old)

SELECT
"Loan","Date",
(ROUND(COALESCE(CAST((case when PVYieldkWh in ('--','','nan') then '0' else PVYieldkWh end) AS float),0),2)) as "Power(Kw/h)",
ROUND(COALESCE(CAST((case when ImportkWh in ('--','','nan') then '0' else ImportkWh end) AS float),0),2) as "Grid Power(Kw/h)",
(ROUND(COALESCE(CAST((case when ConsumptionkWh in ('--','','nan') then '0' else ConsumptionkWh end) AS float),0),2)) as "Consumption(Kw/h)",
(ROUND(CAST('0' AS float),2)) as  "BatteryCharge(Kw/h)", 
(ROUND(CAST('0' AS float),2)) as "BatteryDisCharge(Kw/h)"
FROM date_sg5fusionsolarhuaweicom
GROUP BY "Loan","Date"

union all
--6----wwwisolarcloudcom

SELECT 
"Loan","Date",
ROUND(COALESCE(CAST((case when PVkWh in ('--','','nan') then '0' else PVkWh end) AS float),0),2) as "Power(Kw/h)",
ROUND(COALESCE(CAST((case when PurchasedEnergykWh in ('--','','nan') then '0' else PurchasedEnergykWh end) AS float),0),2) as "Grid Power(Kw/h)",
ROUND(COALESCE(CAST((case when LoadkWh in ('--','','nan') then '0' else LoadkWh end) AS float),0),2) as "Consumption(Kw/h)",
0 "BatteryCharge(Kw/h)", 0 "BatteryDisCharge(Kw/h)"
FROM date_wwwisolarcloudcom
GROUP BY "Loan","Date"

union all
--7----wwwsemsportalcom

SELECT 
"Loan","Date",
ROUND(COALESCE(CAST((case when PVkWh in ('','0','nan') then '0' else PVkWh end) AS float),0),2) as "Power(Kw/h)",
ROUND(COALESCE(CAST((case when BuykWh in ('','0','nan') then '0' else BuykWh end) AS float),0),2) as "Grid Power(Kw/h)",
ROUND(COALESCE(CAST((case when ConsumptionkWh in ('','0','nan') then '0' else ConsumptionkWh end) AS float),0),2) as "Consumption(Kw/h)",
ROUND(COALESCE(CAST(('0') AS float),0),2) as "BatteryCharge(Kw/h)",
ROUND(COALESCE(CAST(('0') AS float),0),2) as "BatteryDisCharge(Kw/h)"
FROM date_wwwsemsportalcom
GROUP BY "Loan","Date"

union all
--9----wwwsoliscloudcom

SELECT
"Loan","Date",
ROUND(COALESCE(CAST((case when TodayYieldkWh in ('','0','nan') then '0' else TodayYieldkWh end) AS float),0),2) as "Power(Kw/h)",
ROUND(COALESCE(CAST((case when EnergyfromGridkWh in ('','0','nan') then '0' else EnergyfromGridkWh end) AS float),0),2) as "Grid Power(Kw/h)",
ROUND(COALESCE(CAST((case when LoadConsumptionkWh in ('','0','nan') then '0' else LoadConsumptionkWh end) AS float),0),2) as "Consumption(Kw/h)",
ROUND(COALESCE(CAST((case when EnergytoBatterykWh in ('','0','nan') then '0' else EnergytoBatterykWh end) AS float),0),2) as "BatteryCharge(Kw/h)",
ROUND(COALESCE(CAST((case when EnergyfromBatterykWh in ('','0','nan') then '0' else EnergyfromBatterykWh end) AS float),0),2) as "BatteryDisCharge(Kw/h)"
FROM date_wwwsoliscloudcom
GROUP BY "Loan","Date"
) as date_convert_from_raw ORDER BY "Date" desc;


-----------run_adjust_date-------------
--------------CREATE TABLE AJUST MIN--------------------
DROP TABLE IF EXISTS adjust_bymin;

CREATE TABLE adjust_bymin AS
SELECT
cmr."Loan",
cmr."Date",
cmr."time",
cmr."Power(Kw/h)",
CAST(ifnull(cmr."Power(Kw/h)"/adj.adjust,cmr."Power(Kw/h)") AS float) AS "Power(Kw/h) with adjust",
ROUND((CAST(ifnull(cmr."Power(Kw/h)"/adj.adjust,cmr."Power(Kw/h)") AS float)*5/60),4) AS "Power(Kw/h) convert to date",
adj."InverterName",
adj."Region",
adj."installed_capacity"
FROM clean_bymin_from_raw cmr 
LEFT JOIN (
SELECT
cdm."Loan",
cdm."Date",
CAST(ifnull(cdm."Power(Kw/h)"/cdr."Power(Kw/h)",1) AS float) as adjust,
il."InverterName",
il."Region",
il."installed_capacity"
FROM clean_byday_from_min cdm 
LEFT JOIN clean_byday_from_raw cdr on (cdm."Loan"||cdm."Date")=(cdr."Loan"||cdr."Date")
LEFT JOIN info_loan il on cdm."Loan" == il."LoanID"
) adj on (cmr."Loan"||cmr."Date")=(adj."Loan"||adj."Date");

------------------------------------END CODE--------------------------------------------