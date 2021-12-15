/*
SQLyog Ultimate v9.50
MySQL - 5.6.10
*********************************************************************
*/
/*!40101 SET NAMES utf8 */;

insert into `flow_status` (`id`, `code`, `desc`) values('20','REJECT','Reject');
insert into `flow_status` (`id`, `code`, `desc`) values('40','DELETE','Delete');
insert into `flow_status` (`id`, `code`, `desc`) values('80','CANCEL','Cancel');
insert into `flow_status` (`id`, `code`, `desc`) values('100','DRAFT','Draft');
insert into `flow_status` (`id`, `code`, `desc`) values('200','CONFIRM','Confirm');
insert into `flow_status` (`id`, `code`, `desc`) values('500','PROCEED','Proceed');
insert into `flow_status` (`id`, `code`, `desc`) values('1000','COMPLETE','Complete');
