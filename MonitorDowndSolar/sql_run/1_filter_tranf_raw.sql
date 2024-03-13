---------FILTER AND TRANSFORM-----
CREATE TABLE IF NOT EXISTS tmp_min_wwwsoliscloudcom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_min_wwwsemsportalcom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_min_wwwisolarcloudcom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_min_sg5fusionsolarhuaweicom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_min_serverluxpowertekcom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_min_servergrowattcom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_min_prosolarmanpvcom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_min_homesolarmanpvcom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_min_globalprosolarmanpvcom("NameFile" TEXT);

CREATE TABLE IF NOT EXISTS tmp_date_wwwsoliscloudcom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_date_wwwsemsportalcom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_date_wwwisolarcloudcom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_date_sg5fusionsolarhuaweicom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_date_serverluxpowertekcom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_date_servergrowattcom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_date_prosolarmanpvcom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_date_homesolarmanpvcom("NameFile" TEXT);
CREATE TABLE IF NOT EXISTS tmp_date_globalprosolarmanpvcom("NameFile" TEXT);
---------------Process By date-----------
DROP TABLE IF EXISTS const;
--CREATE TABLE  const AS SELECT strftime('%Y%m%d',DATE('now','-4 day')) AS rangedate;
CREATE TABLE  const AS SELECT strftime('%Y%m%d',DATE('now')) AS rangedate;
--1----globalprosolarmanpv
--Drop table date_globalprosolarmanpvcom
CREATE TABLE IF NOT EXISTS date_globalprosolarmanpvcom ("id" TEXT,"Loan" TEXT,"Date" TEXT,
"DailyProductionkWh" TEXT,"DailyConsumptionkWh" TEXT,"DailyGridFeedinkWh" TEXT,
"DailyEnergyPurchasedkWh" TEXT,"DailyEnergyChargedkWh" TEXT,"DailyEnergyDischargedkWh" TEXT,
"PeakHoursTodayh" TEXT,"Temperature" TEXT,"Weather" TEXT);

INSERT INTO date_globalprosolarmanpvcom
SELECT
TRIM(substr("NameFile" ,8,8))||TRIM(REPLACE("Time",'/','')) as "id",
TRIM(substr("NameFile" ,8,8)) as "Loan",
TRIM(REPLACE("Time",'/','')) as "Date" ,
"DailyProductionkWh" ,"DailyConsumptionkWh" ,"DailyGridFeedinkWh" ,
"DailyEnergyPurchasedkWh" ,"DailyEnergyChargedkWh" ,"DailyEnergyDischargedkWh" ,
"PeakHoursTodayh" ,"Temperature" ,"Weather"
FROM tmp_date_globalprosolarmanpvcom WHERE ("DailyProductionkWh" != 'nan' or "DailyConsumptionkWh" != 'nan')
and TRIM(substr("NameFile" ,8,8))||TRIM(REPLACE("Time",'/','')) not in (SELECT id FROM date_globalprosolarmanpvcom)
and TRIM(REPLACE("Time",'/','')) != (select const.rangedate from const);

--2----prosolarmanpvcom
--Drop table date_prosolarmanpvcom
CREATE TABLE IF NOT EXISTS date_prosolarmanpvcom ("id" TEXT,"Loan" TEXT,"Date" TEXT,
"DailyProductionkWh" TEXT,"DailyConsumptionkWh" TEXT,"DailyGridFeedinkWh" TEXT,
"DailyEnergyPurchasedkWh" TEXT,"DailyEnergyChargedkWh" TEXT,"DailyEnergyDischargedkWh" TEXT,
"PeakHoursTodayh" TEXT,"Temperature" TEXT,"Weather" TEXT);

INSERT INTO date_prosolarmanpvcom
SELECT
TRIM(substr("NameFile" ,8,8))||TRIM(REPLACE("Time",'/','')) as "id",
TRIM(substr("NameFile" ,8,8)) as "Loan",
TRIM(REPLACE("Time",'/','')) as "Date" ,
"DailyProductionkWh" ,"DailyConsumptionkWh" ,"DailyGridFeedinkWh" ,
"DailyEnergyPurchasedkWh" ,"DailyEnergyChargedkWh" ,"DailyEnergyDischargedkWh" , 
"PeakHoursTodayh" ,"Temperature" ,"Weather" 
FROM tmp_date_prosolarmanpvcom WHERE ("DailyProductionkWh" != 'nan' or "DailyConsumptionkWh" != 'nan')
and TRIM(substr("NameFile" ,8,8))||TRIM(REPLACE("Time",'/','')) not in (SELECT id FROM date_prosolarmanpvcom)
and TRIM(REPLACE("Time",'/','')) != (select const.rangedate from const);


--3----homesolarmanpvcom
--Drop table date_homesolarmanpvcom
CREATE TABLE IF NOT EXISTS date_homesolarmanpvcom ("id" TEXT,"Loan" TEXT,"Date" TEXT,
"ProductionkWh" TEXT,"ConsumptionkWh" TEXT,"GridFeedinkWh" TEXT,
"EnergyPurchasedkWh" TEXT,"ChargingEnergykWh" TEXT,"DischargingEnergykWh" TEXT,"SelfusedRatio" TEXT,"PlantName" TEXT,"TimeZone" TEXT,
"AnticipatedYieldVND" TEXT);

INSERT INTO date_homesolarmanpvcom
SELECT
TRIM(substr("NameFile" ,10,8))||TRIM(REPLACE("UpdatedTime",'/','')) as "id",
TRIM(substr("NameFile" ,10,8)) as "Loan",
TRIM(REPLACE("UpdatedTime",'/','')) as "Date" ,
"ProductionkWh" ,"ConsumptionkWh" ,"GridFeedinkWh" ,
"EnergyPurchasedkWh" ,"ChargingEnergykWh" ,"DischargingEnergykWh" ,"SelfusedRatio" ,"PlantName" ,"TimeZone" ,
"AnticipatedYieldVND"
FROM tmp_date_homesolarmanpvcom WHERE ("DailyProductionkWh" != 'nan' or "DailyConsumptionkWh" != 'nan')
and TRIM(substr("NameFile" ,8,8))||TRIM(REPLACE("Time",'/','')) not in (SELECT id FROM date_homesolarmanpvcom)
and TRIM(REPLACE("UpdatedTime",'/','')) != (select const.rangedate from const);

--4----servergrowattcom
--Drop table date_servergrowattcom
CREATE TABLE IF NOT EXISTS date_servergrowattcom ("id" TEXT,"Loan" TEXT,"Date" TEXT,
"ProductionkWh" TEXT);

INSERT INTO date_servergrowattcom
SELECT
TRIM(substr("NameFile" ,8,8))||TRIM(substr("NameFile",0,7)||CASE WHEN length("day") < 2 THEN '0'||"day" ELSE "day" END) as "id",
TRIM(substr("NameFile" ,8,8)) as "Loan",
TRIM(substr("NameFile",0,7)||CASE WHEN length("day") < 2 THEN '0'||"day" ELSE "day" END) as "Date" , 
CASE WHEN "day"=PV2kWh THEN PV1kWh ELSE PV2kWh END as "ProductionkWh"
FROM tmp_date_servergrowattcom WHERE 1
and TRIM(substr("NameFile" ,8,8))||TRIM(substr("NameFile",0,7)||CASE WHEN length("day") < 2 THEN '0'||"day" ELSE "day" END)  not in (SELECT id FROM date_servergrowattcom)
and TRIM(substr("NameFile",0,7)||CASE WHEN length("day") < 2 THEN '0'||"day" ELSE "day" END) != (select const.rangedate from const);


--5----sg5fusionsolarhuaweicom
--Drop table date_sg5fusionsolarhuaweicom
CREATE TABLE IF NOT EXISTS date_sg5fusionsolarhuaweicom ("id" TEXT,"Loan" TEXT,"Date" TEXT,
"TotalStringCapacitykWp" TEXT,"PVYieldkWh" TEXT,"InverterYieldkWh" TEXT,"TotalYieldkWh" TEXT,
"ExportkWh" TEXT,"SpecificEnergykWhkWp" TEXT,"ImportkWh" TEXT,"ConsumptionkWh" TEXT,"SelfconsumptionkWh" TEXT,
"PeakPowerkW" TEXT,"COAvoidedt" TEXT,"StandardCoalSavedt" TEXT);

INSERT INTO date_sg5fusionsolarhuaweicom
SELECT
TRIM(substr("NameFile" ,8,8))||TRIM(REPLACE("StatisticalPeriod",'-','')) as "id",
TRIM(substr("NameFile" ,8,8)) as "Loan",
TRIM(REPLACE("StatisticalPeriod",'-','')) as "Date" ,
"TotalStringCapacitykWp" ,"PVYieldkWh" ,"InverterYieldkWh" ,"TotalYieldkWh" ,
"ExportkWh" ,"SpecificEnergykWhkWp" ,"ImportkWh" ,"ConsumptionkWh" ,"SelfconsumptionkWh" ,
"PeakPowerkW" ,"COAvoidedt" ,"StandardCoalSavedt"
FROM tmp_date_sg5fusionsolarhuaweicom WHERE 1
and TRIM(substr("NameFile" ,8,8))||TRIM(REPLACE("StatisticalPeriod",'-',''))  not in (SELECT id FROM date_sg5fusionsolarhuaweicom)
and TRIM(REPLACE("StatisticalPeriod",'-','')) != (select const.rangedate from const);
 

--6----wwwisolarcloudcom
--Drop table date_wwwisolarcloudcom
CREATE TABLE IF NOT EXISTS date_wwwisolarcloudcom ("id" TEXT,"Loan" TEXT,"Date" TEXT,
"PVkWh" TEXT,"PurchasedEnergykWh" TEXT,"FeedinkWh" TEXT,
"LoadkWh" TEXT,"SelfconsumptionkWh" TEXT);

INSERT INTO date_wwwisolarcloudcom
SELECT
TRIM(substr("NameFile" ,8,8))||TRIM(REPLACE("Time",'-','')) as "id",
TRIM(substr("NameFile" ,8,8)) as "Loan",
TRIM(REPLACE("Time",'-','')) as "Date" ,
"PVkWh" ,"PurchasedEnergykWh" ,"FeedinkWh" ,
"LoadkWh" ,"SelfconsumptionkWh" 
FROM tmp_date_wwwisolarcloudcom WHERE 1
and TRIM(substr("NameFile" ,8,8))||TRIM(REPLACE("Time",'-',''))  not in (SELECT id FROM date_wwwisolarcloudcom)
and TRIM(REPLACE("Time",'-','')) != (select const.rangedate from const);
 
--7----wwwsemsportalcom
--Drop table date_wwwsemsportalcom
CREATE TABLE IF NOT EXISTS date_wwwsemsportalcom ("id" TEXT,"Loan" TEXT,"Date" TEXT,
"Plant" TEXT,"Classification" TEXT,"CapacitykW" TEXT,"PVkWh" TEXT,
"SellkWh" TEXT,"BuykWh" TEXT,"ConsumptionkWh" TEXT,
"InhousekWh" TEXT,"SelfConsRatio" TEXT,"ContributionRatio" TEXT,"IncomeVND" TEXT);

INSERT INTO date_wwwsemsportalcom
SELECT
TRIM(substr("NameFile" ,8,8))||TRIM(substr("Date",7,4)||substr("Date",1,2)||substr("Date",4,2)) as "id",
TRIM(substr("NameFile" ,8,8)) as "Loan",
TRIM(substr("Date",7,4)||substr("Date",1,2)||substr("Date",4,2)) as "Date",
"Plant" ,"Classification" ,
"CapacitykW" ,"PVkWh" ,"SellkWh" ,"BuykWh" ,"ConsumptionkWh" ,
"InhousekWh" ,"SelfConsRatio" ,"ContributionRatio" ,"IncomeVND" 
 FROM tmp_date_wwwsemsportalcom WHERE "Date" != 'TOTAL'
and TRIM(substr("NameFile" ,8,8))||TRIM(substr("Date",7,4)||substr("Date",1,2)||substr("Date",4,2))  not in (SELECT id FROM date_wwwsemsportalcom)
and TRIM(substr("Date",7,4)||substr("Date",1,2)||substr("Date",4,2)) != (select const.rangedate from const);
 
 
--8----wwwsoliscloudcom
--Drop table date_wwwsoliscloudcom
CREATE TABLE IF NOT EXISTS date_wwwsoliscloudcom ("id" TEXT,"Loan" TEXT,"Date" TEXT,
"TodayYieldkWh" TEXT,"TodayFullLoadHoursh" TEXT,"EnergytoGridkWh" TEXT,
"EnergyfromGridkWh" TEXT,"UsekWh" TEXT,"sufficiencykWh" TEXT,"LoadConsumptionkWh" TEXT,"GenerationkWh" TEXT,
"EnergytoBatterykWh" TEXT,"EnergyfromBatterykWh" TEXT);

INSERT INTO date_wwwsoliscloudcom
SELECT
TRIM(substr("NameFile" ,8,8))||TRIM(substr("Time",7,4)||substr("Time",4,2)||substr("Time",1,2)) as "id",
TRIM(substr("NameFile" ,8,8)) as "Loan",
TRIM(substr("Time",7,4)||substr("Time",4,2)||substr("Time",1,2)) as "Date",
"TodayYieldkWh" ,"TodayFullLoadHoursh" ,"EnergytoGridkWh" ,
"EnergyfromGridkWh" ,"UsekWh" ,"sufficiencykWh" ,"LoadConsumptionkWh" ,"GenerationkWh" ,
"EnergytoBatterykWh" ,"EnergyfromBatterykWh" 
FROM tmp_date_wwwsoliscloudcom WHERE 1
and TRIM(substr("NameFile" ,8,8))||TRIM(substr("Time",7,4)||substr("Time",4,2)||substr("Time",1,2))  not in (SELECT id FROM date_wwwsoliscloudcom)
and TRIM(substr("Time",7,4)||substr("Time",4,2)||substr("Time",1,2)) != (select const.rangedate from const);


---------------Process By min-----------

--1----globalprosolarmanpvcom
--Drop table min_globalprosolarmanpvcom
CREATE TABLE IF NOT EXISTS min_globalprosolarmanpvcom ("id" TEXT,"Loan" TEXT,"Date" TEXT,"Time" TEXT,
"ProductionkW" TEXT,"ConsumptionkW" TEXT,"GridkW" TEXT,"PurchasingkW" TEXT,
"FeedinkW" TEXT,"BatterykW" TEXT,"ChargekW" TEXT,"DischargekW" TEXT,"SOC" TEXT,"IrradiancekW" TEXT);

INSERT INTO min_globalprosolarmanpvcom
SELECT
TRIM(substr("NameFile" ,10,8))||TRIM(replace(substr("Time",1,10),'/',''))||TRIM(substr("Time",12,5)) as "id",
TRIM(substr("NameFile" ,10,8)) as "Loan",
TRIM(replace(substr("Time",1,10),'/','')) as "Date",
TRIM(substr("Time",12,5)) as "Time" ,
"ProductionkW" ,"ConsumptionkW" ,"GridkW" ,"PurchasingkW" ,
"FeedinkW" ,"BatterykW" ,"ChargekW" ,"DischargekW" ,"SOC" ,"IrradiancekW"
FROM tmp_min_globalprosolarmanpvcom WHERE "Temperature" = 'nan'
and TRIM(substr("NameFile" ,10,8))||TRIM(replace(substr("Time",1,10),'/',''))||TRIM(substr("Time",12,5))  not in (SELECT id FROM min_globalprosolarmanpvcom)
and TRIM(replace(substr("Time",1,10),'/','')) != (select const.rangedate from const);


--2----homesolarmanpvcom
--Drop table min_homesolarmanpvcom
CREATE TABLE IF NOT EXISTS min_homesolarmanpvcom ("id" TEXT,"Loan" TEXT,"Date" TEXT,"Time" TEXT,
"PlantName" TEXT,"TimeZone" TEXT,"ProductionPowerW" TEXT,
"ConsumptionPowerW" TEXT,"GridPowerW" TEXT,"FeedinPowerW" TEXT,"PurchasingPowerW" TEXT,"BatteryPowerW" TEXT,
"ChargingPowerW" TEXT,"DischargingPowerW" TEXT,"SoC" TEXT);

INSERT INTO min_homesolarmanpvcom
SELECT
TRIM(substr("NameFile" ,10,8))||TRIM(replace(substr("UpdatedTime",1,10),'/',''))||TRIM(substr("UpdatedTime",12,5)) as "id",
TRIM(substr("NameFile" ,10,8)) as "Loan",
TRIM(replace(substr("UpdatedTime",1,10),'/','')) as "Date",
TRIM(substr("UpdatedTime",12,5)) as "Time" ,
"PlantName" ,"TimeZone" ,"ProductionPowerW" ,
"ConsumptionPowerW" ,"GridPowerW" ,"FeedinPowerW" ,"PurchasingPowerW" ,"BatteryPowerW" ,
"ChargingPowerW" ,"DischargingPowerW" ,"SoC"	
FROM tmp_min_homesolarmanpvcom WHERE 1
and TRIM(substr("NameFile" ,10,8))||TRIM(replace(substr("UpdatedTime",1,10),'/',''))||TRIM(substr("UpdatedTime",12,5))  not in (SELECT id FROM min_homesolarmanpvcom)
and  TRIM(replace(substr("UpdatedTime",1,10),'/','')) != (select const.rangedate from const);


--3----prosolarmanpvcom
--Drop table min_prosolarmanpvcom
CREATE TABLE IF NOT EXISTS min_prosolarmanpvcom ("id" TEXT,"Loan" TEXT,"Date" TEXT,"Time" TEXT,
"ProductionkW" TEXT,"ConsumptionkW" TEXT,"GridkW" TEXT,"PurchasingkW" TEXT,
"FeedinkW" TEXT,"BatterykW" TEXT,"ChargekW" TEXT,"DischargekW" TEXT,"SOC" TEXT,"IrradiancekW" TEXT);

INSERT INTO min_prosolarmanpvcom
SELECT
TRIM(substr("NameFile" ,10,8))||TRIM(replace(substr("Time",1,10),'/',''))||TRIM(substr("Time",12,5)) as "id",
TRIM(substr("NameFile" ,10,8)) as "Loan",
TRIM(replace(substr("Time",1,10),'/','')) as "Date",
TRIM(substr("Time",12,5)) as "Time" ,
"ProductionkW" ,"ConsumptionkW" ,"GridkW" ,"PurchasingkW" ,
"FeedinkW" ,"BatterykW" ,"ChargekW" ,"DischargekW" ,"SOC" ,"IrradiancekW"
FROM tmp_min_prosolarmanpvcom WHERE "Temperature" = 'nan' 
and TRIM(substr("NameFile" ,10,8))||TRIM(replace(substr("Time",1,10),'/',''))||TRIM(substr("Time",12,5)) not in (SELECT id FROM min_prosolarmanpvcom)
and TRIM(replace(substr("Time",1,10),'/','')) != (select const.rangedate from const);


--4----servergrowattcom
--Drop table min_servergrowattcom
CREATE TABLE IF NOT EXISTS min_servergrowattcom ("id" TEXT,"Loan" TEXT,"Date" TEXT,"Time" TEXT,
"PhotovoltaicOutput" TEXT,"ExportedtoGrid" TEXT,
"ImportedFromGrid" TEXT,"LoadConsumption" TEXT,"Charging" TEXT,"Discharging" TEXT);

INSERT INTO min_servergrowattcom
SELECT
TRIM(substr("NameFile" ,10,8))||TRIM(substr("NameFile",1,8))||TRIM("time") as "id",
TRIM(substr("NameFile" ,10,8)) as "Loan",
TRIM(substr("NameFile",1,8)) as "Date",
TRIM("time") as "Time" ,
"PhotovoltaicOutput" ,"ExportedtoGrid" ,
"ImportedFromGrid" ,"LoadConsumption" ,"Charging" ,"Discharging"
FROM tmp_min_servergrowattcom WHERE 1
and TRIM(substr("NameFile" ,10,8))||TRIM(substr("NameFile",1,8))||TRIM("time")  not in (SELECT id FROM min_servergrowattcom)
and TRIM(substr("NameFile",1,8)) != (select const.rangedate from const);


--5----serverluxpowertekcom
--Drop table min_serverluxpowertekcom
CREATE TABLE IF NOT EXISTS min_serverluxpowertekcom ("id" TEXT,"Loan" TEXT,"Date" TEXT,"Time" TEXT,
"Serialnumber" TEXT,
"vpv1" TEXT,"vpv2" TEXT,"vpv3" TEXT,"vBat" TEXT,"soc" TEXT,
"ppv1" TEXT,"ppv2" TEXT,"ppv3" TEXT,"pCharge" TEXT,"pDisCharge" TEXT,
"vacr" TEXT,"vacs" TEXT,"vact" TEXT,"fac" TEXT,"pinv" TEXT,"pToGrid" TEXT,"pToUser" TEXT,
"pLoad" TEXT,"ePv1Day" TEXT,"ePv2Day" TEXT,"ePv3Day" TEXT,"eInvDay" TEXT,"eRecDay" TEXT,
"eChgDay" TEXT,"eDisChgDay" TEXT,"eEpsDay" TEXT,"eToGridDay" TEXT,
"eToUserDay" TEXT,"ePv1All" TEXT,"ePv2All" TEXT,"ePv3All" TEXT,"eInvAll" TEXT,
"eRecAll" TEXT,"eChgAll" TEXT,"eDisChgAll" TEXT,"eEpsAll" TEXT,"eToGridAll" TEXT,"eToUserAll" TEXT,
"chargeVoltRef" TEXT,"dischgCutVolt" TEXT,"BatCurrent" TEXT,
"CycleCnt" TEXT,"Vbat_Inv" TEXT,"genPower" TEXT,"eGenDay" TEXT);

INSERT INTO min_serverluxpowertekcom
SELECT
TRIM(substr("NameFile" ,10,8))||TRIM(replace(substr("Time",1,10),'-',''))||TRIM(substr("Time",12,5)) as "id",
TRIM(substr("NameFile" ,10,8)) as "Loan",
TRIM(replace(substr("Time",1,10),'-','')) as "Date",
TRIM(substr("Time",12,5)) as "Time" ,
"Serialnumber" ,
"vpv1" ,"vpv2" ,"vpv3" ,"vBat" ,"soc" ,
"ppv1" ,"ppv2" ,"ppv3" ,"pCharge" ,"pDisCharge" ,
"vacr" ,"vacs" ,"vact" ,"fac" ,"pinv" ,"pToGrid" ,"pToUser" ,
"pLoad" ,"ePv1Day" ,"ePv2Day" ,"ePv3Day" ,"eInvDay" ,"eRecDay" ,
"eChgDay" ,"eDisChgDay" ,"eEpsDay" ,"eToGridDay" ,
"eToUserDay" ,"ePv1All" ,"ePv2All" ,"ePv3All" ,"eInvAll" ,
"eRecAll" ,"eChgAll" ,"eDisChgAll" ,"eEpsAll" ,"eToGridAll" ,"eToUserAll" ,
"chargeVoltRef" ,"dischgCutVolt" ,"BatCurrent" ,
"CycleCnt" ,"Vbat_Inv" ,"genPower" ,"eGenDay"
FROM tmp_min_serverluxpowertekcom WHERE 1
and TRIM(substr("NameFile" ,10,8))||TRIM(replace(substr("Time",1,10),'-',''))||TRIM(substr("Time",12,5))  not in (SELECT id FROM min_serverluxpowertekcom)
and TRIM(replace(substr("Time",1,10),'-','')) != (select const.rangedate from const);

--6----sg5fusionsolarhuaweicom
--Drop table min_sg5fusionsolarhuaweicom
CREATE TABLE IF NOT EXISTS min_sg5fusionsolarhuaweicom ("id" TEXT,"Loan" TEXT,"Date" TEXT,"Time" TEXT,
"onGridPowerRatio" TEXT,"selfUsePower" TEXT,"selfUsePowerRatioByUse" TEXT,
"stationTimezone" TEXT,"totalBuyPower" TEXT,"existEnergyStore" TEXT,"totalProductPower" TEXT,
"dischargePower" TEXT,"radiationDosePower" TEXT,"mainsUsePower" TEXT,"buyPowerRatio" TEXT,
"selfUsePowerRatioByProduct" TEXT,"totalSelfUsePower" TEXT,"chargePower" TEXT,
"onGridPower" TEXT,"dieselProductPower" TEXT,"stationDn" TEXT,"disGridPower" TEXT,
"selfProvide" TEXT,"productPower" TEXT,"usePower" TEXT,"meterActivePower" TEXT,
"totalUsePower" TEXT,"chargeAndDisChargePower" TEXT,"totalOnGridPower" TEXT);

INSERT INTO min_sg5fusionsolarhuaweicom
SELECT
TRIM(substr("NameFile" ,10,8))||TRIM(replace(substr("xAxis",1,10),'-',''))||TRIM(substr("xAxis",12,5)) as "id",
TRIM(substr("NameFile" ,10,8)) as "Loan",
TRIM(replace(substr("xAxis",1,10),'-','')) as "Date",
TRIM(substr("xAxis",12,5)) as "Time" ,
"onGridPowerRatio","selfUsePower","selfUsePowerRatioByUse",
"stationTimezone","totalBuyPower","existEnergyStore","totalProductPower",
"dischargePower","radiationDosePower","mainsUsePower","buyPowerRatio",
"selfUsePowerRatioByProduct","totalSelfUsePower","chargePower",
"onGridPower","dieselProductPower","stationDn","disGridPower",
"selfProvide","productPower","usePower","meterActivePower",
"totalUsePower","chargeAndDisChargePower","totalOnGridPower"
FROM tmp_min_sg5fusionsolarhuaweicom WHERE 1
and TRIM(substr("NameFile" ,10,8))||TRIM(replace(substr("xAxis",1,10),'-',''))||TRIM(substr("xAxis",12,5))  not in (SELECT id FROM min_sg5fusionsolarhuaweicom)
and TRIM(replace(substr("xAxis",1,10),'-','')) != (select const.rangedate from const);

--7----wwwisolarcloudcom
--Drop table min_wwwisolarcloudcom
CREATE TABLE IF NOT EXISTS min_wwwisolarcloudcom ("id" TEXT,"Loan" TEXT,"Date" TEXT,"Time" TEXT,
"PVW" TEXT,"GridW" TEXT,"LoadW" TEXT);

INSERT INTO min_wwwisolarcloudcom
SELECT
TRIM(substr("NameFile" ,10,8))||TRIM(replace(substr("Time",1,10),'-',''))||TRIM(substr("Time",12,5)) as "id",
TRIM(substr("NameFile" ,10,8)) as "Loan",
TRIM(replace(substr("Time",1,10),'-','')) as "Date",
TRIM(substr("Time",12,5)) as "Time" ,
"PVW","GridW","LoadW"
FROM tmp_min_wwwisolarcloudcom WHERE 1
and TRIM(substr("NameFile" ,10,8))||TRIM(replace(substr("Time",1,10),'-',''))||TRIM(substr("Time",12,5))  not in (SELECT id FROM min_wwwisolarcloudcom)
and TRIM(replace(substr("Time",1,10),'-','')) != (select const.rangedate from const);

--8----wwwsemsportalcom
--Drop table min_wwwsemsportalcom
CREATE TABLE IF NOT EXISTS min_wwwsemsportalcom ("id" TEXT,"Loan" TEXT,"Date" TEXT,"Time" TEXT,
"PVW" TEXT,"SOC" TEXT,"BatteryW" TEXT,
"MeterW" TEXT,"LoadW" TEXT);

INSERT INTO min_wwwsemsportalcom
SELECT
TRIM(substr("NameFile" ,10,8))||CASE WHEN "LoadW" = 'nan' THEN TRIM(substr("Time",7,4)||substr("Time",4,2))||substr("Time",1,2) ELSE TRIM(substr("Time",7,4)||substr("Time",1,2)||substr("Time",4,2)) END||TRIM(substr("Time",12,5)) as "id",
TRIM(substr("NameFile" ,10,8)) as "Loan",
TRIM(substr("Time",7,4)||substr("Time",1,2)||substr("Time",4,2)) as "Date",
TRIM(substr("Time",12,5)) as "Time" ,
"PVW" ,
"SOC" ,"BatteryW" ,
"MeterW" ,"LoadW"
FROM tmp_min_wwwsemsportalcom WHERE 1
and TRIM(substr("Time",7,4)||substr("Time",1,2)||substr("Time",4,2)) ||TRIM(substr("Time",12,5))
not in (SELECT id FROM min_wwwsemsportalcom)
and TRIM(substr("Time",7,4)||substr("Time",1,2)||substr("Time",4,2)) != (select const.rangedate from const);


--9----wwwsoliscloudcom
--Drop table min_wwwsoliscloudcom
CREATE TABLE IF NOT EXISTS min_wwwsoliscloudcom ("id" TEXT,"Loan" TEXT,"Date" TEXT,"Time" TEXT,
"WorkingState" TEXT,
"AlarmCode" TEXT,
"TotalInverterPowerW" TEXT,
"GridTotalActivePowerW"	TEXT,
"TotalConsumeEnergyPowerW" TEXT,
"BatteryPowerW" TEXT);

INSERT INTO min_wwwsoliscloudcom
SELECT
TRIM(substr("NameFile" ,10,8))||TRIM(substr("Time",7,4)||substr("Time",4,2))||substr("Time",1,2)||TRIM(substr("Time",12,5)) as "id",
TRIM(substr("NameFile" ,10,8)) as "Loan",
TRIM(substr("Time",7,4)||substr("Time",4,2))||substr("Time",1,2) as "Date",
TRIM(substr("Time",12,5)) as "Time" ,
"WorkingState" ,
"AlarmCode" ,
"TotalInverterPowerW" ,
"GridTotalActivePowerW"	,
"TotalConsumeEnergyPowerW",
"BatteryPowerW"
FROM tmp_min_wwwsoliscloudcom  WHERE 1
and TRIM(substr("NameFile" ,10,8))||TRIM(substr("Time",7,4)||substr("Time",4,2))||substr("Time",1,2)||TRIM(substr("Time",12,5))  not in (SELECT id FROM min_wwwsoliscloudcom)
and TRIM(substr("Time",7,4)||substr("Time",4,2))||substr("Time",1,2) != (select const.rangedate from const);

DROP TABLE IF EXISTS const;


---------FILTER AND TRANSFORM-----
DROP TABLE IF EXISTS tmp_min_wwwsoliscloudcom;
DROP TABLE IF EXISTS tmp_min_wwwsemsportalcom;
DROP TABLE IF EXISTS tmp_min_wwwisolarcloudcom;
DROP TABLE IF EXISTS tmp_min_sg5fusionsolarhuaweicom;
DROP TABLE IF EXISTS tmp_min_serverluxpowertekcom;
DROP TABLE IF EXISTS tmp_min_servergrowattcom;
DROP TABLE IF EXISTS tmp_min_prosolarmanpvcom;
DROP TABLE IF EXISTS tmp_min_homesolarmanpvcom;
DROP TABLE IF EXISTS tmp_min_globalprosolarmanpvcom;

DROP TABLE IF EXISTS tmp_date_wwwsoliscloudcom;
DROP TABLE IF EXISTS tmp_date_wwwsemsportalcom;
DROP TABLE IF EXISTS tmp_date_wwwisolarcloudcom;
DROP TABLE IF EXISTS tmp_date_sg5fusionsolarhuaweicom;
DROP TABLE IF EXISTS tmp_date_serverluxpowertekcom;
DROP TABLE IF EXISTS tmp_date_servergrowattcom;
DROP TABLE IF EXISTS tmp_date_prosolarmanpvcom;
DROP TABLE IF EXISTS tmp_date_homesolarmanpvcom;
DROP TABLE IF EXISTS tmp_date_globalprosolarmanpvcom;
--END CODE SQL-----------------------------------------

