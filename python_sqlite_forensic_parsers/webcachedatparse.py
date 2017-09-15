#!/usr/bin/env python

# https://jon.glass/


import pyesedb
import csv
from datetime import datetime, timedelta
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-i", dest="infile", help="input dat file to parse")

args = parser.parse_args()

# file_object = open("WebCacheV01.dat", "rb")
file_object = open(args.infile, 'rb')
esedb_file = pyesedb.file()
esedb_file.open_file_object(file_object)
ContainersTable = esedb_file.get_table_by_name("Containers")
WebHistoryTables = []
OutputRecord = 0
Output = []

def convert_timestamp(timestamp):
	epoch_start = datetime(year=1601, month=1,day=1)
	seconds_since_epoch = timestamp/10**7
	return epoch_start + timedelta(seconds=seconds_since_epoch)



for i in range(0,ContainersTable.get_number_of_records()-1):
	Container_Record = ContainersTable.get_record(i)
	ContainerID = Container_Record.get_value_data_as_integer(0)
	Container_Name = Container_Record.get_value_data_as_string(8)
	Container_Directory = Container_Record.get_value_data_as_string(10)
	if Container_Name == "History" and "History.IE5" in Container_Directory:
		WebHistoryTables += [ContainerID]

for i in WebHistoryTables:
	WebHistoryTable = esedb_file.get_table_by_name("Container_"+ str(i))
	for j in range(0,WebHistoryTable.get_number_of_records()-1):
		WebHistoryRecord = WebHistoryTable.get_record(j)
		Output.append({})
		Output[OutputRecord]["EntryId"] = WebHistoryRecord.get_value_data_as_integer(0)
		Output[OutputRecord]["ContainerId"] = WebHistoryRecord.get_value_data_as_integer(1)
		Output[OutputRecord]["CacheId"] = WebHistoryRecord.get_value_data_as_integer(2)
		Output[OutputRecord]["UrlHash"] = WebHistoryRecord.get_value_data_as_integer(3)
		Output[OutputRecord]["SecureDirectory"] = WebHistoryRecord.get_value_data_as_integer(4)
		Output[OutputRecord]["FileSize"] = WebHistoryRecord.get_value_data_as_integer(5)
		Output[OutputRecord]["Type"] = WebHistoryRecord.get_value_data_as_integer(6)
		Output[OutputRecord]["Flags"] = WebHistoryRecord.get_value_data_as_integer(7)
		Output[OutputRecord]["AccessCount"] = WebHistoryRecord.get_value_data_as_integer(8)
		Output[OutputRecord]["SyncTime"] = WebHistoryRecord.get_value_data_as_integer(9)
		Output[OutputRecord]["CreationTime"] = WebHistoryRecord.get_value_data_as_integer(10)
		Output[OutputRecord]["ExpiryTime"] = WebHistoryRecord.get_value_data_as_integer(11)
		Output[OutputRecord]["ModifiedTime"] = WebHistoryRecord.get_value_data_as_integer(12)
		Output[OutputRecord]["AccessedTime"] = WebHistoryRecord.get_value_data_as_integer(13)
		Output[OutputRecord]["PostCheckTime"] = WebHistoryRecord.get_value_data_as_integer(14)
		Output[OutputRecord]["SyncCount"] = WebHistoryRecord.get_value_data_as_integer(15)
		Output[OutputRecord]["ExemptionDelta"] = WebHistoryRecord.get_value_data_as_integer(16)
		if WebHistoryRecord.is_long_value(17):
			Output[OutputRecord]["URL"] = WebHistoryRecord.get_value_data_as_long_value(17).get_data_as_string()
		else:
			Output[OutputRecord]["URL"] = WebHistoryRecord.get_value_data_as_string(17)
		Output[OutputRecord]["Filename"] = WebHistoryRecord.get_value_data_as_string(18)
		Output[OutputRecord]["FileExtension"] = WebHistoryRecord.get_value_data_as_string(19)
		# Output[OutputRecord]["RequestHeaders"] = WebHistoryRecord.get_value_binary_data(20)
		# Output[OutputRecord]["ResponseHeaders"] = WebHistoryRecord.get_value_data_as_string(21)
		# No clue what is going on with the data types here.
		Output[OutputRecord]["RedirectUrl"] = WebHistoryRecord.get_value_data_as_string(22)
		#Output[OutputRecord]["Group"] = WebHistoryRecord.get_value_data_as_integer(23)
		#Output[OutputRecord]["ExtraData"] = WebHistoryRecord.get_value_data_as_string(24)
		# or here
		OutputRecord += 1
esedb_file.close()
with open("parsedwebhistory.csv", "w") as OutputFile:
	csv_file = csv.writer(OutputFile)
	for i in range(len(Output)):
		csv_file.writerow([Output[i]["EntryId"],Output[i]["ContainerId"],Output[i]["CacheId"],Output[i]["UrlHash"],Output[i]["SecureDirectory"],Output[i]["FileSize"],Output[i]["Type"],Output[i]["Flags"],Output[i]["AccessCount"],Output[i]["SyncCount"],convert_timestamp(Output[i]["CreationTime"]),convert_timestamp(Output[i]["ExpiryTime"]),convert_timestamp(Output[i]["ModifiedTime"]),convert_timestamp(Output[i]["AccessedTime"]),Output[i]["PostCheckTime"],Output[i]["SyncCount"],Output[i]["ExemptionDelta"],Output[i]["URL"],Output[i]["Filename"],Output[i]["FileExtension"],Output[i]["RedirectUrl"]
