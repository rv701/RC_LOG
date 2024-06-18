import sys
import os
import re
file_path = "./Samples/Day.LOG"
if (os.path.isfile(file_path) == True):
	lines = [line.rstrip('\n').rstrip('\r') for line in open(file_path)]
	#print ("File length: ", len(lines))
	
	wp_count = 0
	rider_number = ""
	date = ""
	day = "01"
	month = "01"
	year = "2000"
	
	gpx_text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
	gpx_text += "<gpx xmlns=\"http://www.topografix.com/GPX/1/1\" version=\"1.1\" creator=\"ExpertGPS 6.13 \" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:wptx1=\"http://www.garmin.com/xmlschemas/WaypointExtension/v1\" xmlns:gpxx=\"http://www.garmin.com/xmlschemas/GpxExtensions/v3\" xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.topografix.com/GPX/gpx_style/0/2 http://www.topografix.com/GPX/gpx_style/0/2/gpx_style.xsd http://www.topografix.com/GPX/gpx_overlay/0/3 http://www.topografix.com/GPX/gpx_overlay/0/3/gpx_overlay.xsd http://www.topografix.com/GPX/gpx_modified/0/1 http://www.topografix.com/GPX/gpx_modified/0/1/gpx_modified.xsd http://www.garmin.com/xmlschemas/WaypointExtension/v1 http://www8.garmin.com/xmlschemas/WaypointExtensionv1.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd\">\n"
	
	# Loop to create waypoints
	for index in range(0, len(lines)):
		if re.search("^RallyCompLog", lines[index]) :
			lines[index] = re.sub(',', '', lines[index])
			lines[index] = re.sub(';', '', lines[index])
			words = re.split('\\s+', lines[index])
			#print("Words: " + str(len(words)))
			if (len(words) >= 3):
				rider_number = words[1]
				date = words[2]
				#print(words[0])
				#print(words[1])
				#print(words[2])
				gpx_text += "<metadata>\n  <name>" + rider_number + " Stage Log</name>\n</metadata>\n"
				
				#print("Date: " + date)
				dates = re.split(r' |/|\\', date) # Match regular expression for backslash ?? weird one
				#dates = re.split('\\\\', date)
				#print("Date Length: " + str(len(dates)))
				if (len(dates) >= 3):
					month = dates[0]
					day = dates[1]
					year = "20" + dates[2]	
					#print("month: " + month)
					#print("day: " + day)
					#print("year: " + year)
					
					

		lines[index] = re.sub('\\s', '', lines[index])
		words = re.split(';', lines[index])
		#print("Words: " + str(len(words)))
		if (len(words) >= 6):
			#print(lines[index])
			#print(words[0])
			#print(words[1])
			#print(words[2])
			#print(words[3])
			#print(words[4])
			#print(words[5] + "\n")
			
			tmp = words[4]
			waypoint_name = re.sub('[0-9]+', '', tmp)
			waypoint_number = re.sub('[a-zA-Z]+', '', tmp)
		
			
			lat = words[0]
			lon = words[1]
			time = words[2]
			speed = words[3]
			#waypoint_name = words[4]
			status = words[5]
			wp_count+=1
			
			if re.search("^SSZ", waypoint_name) :
				gpx_text += "<wpt lat=\"" + lat + "\" lon=\"" + lon + "\">\n"
				gpx_text += "  <name>" + waypoint_name + waypoint_number + "(" + speed + "/" + status + ")</name>\n"
				gpx_text += "  <cmt>Speed:" + speed + "/" + status + "</cmt>\n"
				
				if (re.search("[0-9]+", status)) :
					if(int(speed) > int(status)) :
						gpx_text += "  <sym>Navaid, Orange</sym>\n"
						gpx_text += "  <type>Navaid, Orange</type>\n"
					else :
						gpx_text += "  <sym>Navaid, Red/Green</sym>\n"
						gpx_text += "  <type>Navaid, Red/Green</type>\n"
				else :
					gpx_text += "  <sym>Navaid, Red/Green</sym>\n"
					gpx_text += "  <type>Navaid, Red/Green</type>\n"
					
				gpx_text += "  <extensions>\n"
				gpx_text += "    <label xmlns=\"http://www.topografix.com/GPX/gpx_overlay/0/3\">\n"
				gpx_text += "    <label_text>" + waypoint_name + waypoint_number + "(" + speed + "/" + status + ")</label_text>\n"
				gpx_text += "    </label>\n"
				gpx_text += "  </extensions>\n"
				gpx_text += "</wpt>\n"
				
				#<wpt lat="35.36491" lon="-117.98245">
				#<name>SSZ061(27/80)</name>
				#<cmt>Speed:27/80</cmt>
				#<sym>Navaid, Red/Green</sym>
				#<extensions>
				#<label xmlns="http://www.topografix.com/GPX/gpx_overlay/0/3">
				#<label_text>SSZ061(27/80)</label_text>
				#</label>
				#</extensions>
				#</wpt>
				
				#<wpt lat="19.45550" lon="-97.42774;">
				#<name>PM112;(59/0)</name>
				#<cmt>Speed:59/0</cmt>
				#<sym>Navaid, Orange</sym>
				#<extensions>
				#<label xmlns="http://www.topografix.com/GPX/gpx_overlay/0/3">
				#<label_text>PM112;(59/0)</label_text>
				#</label>
				#</extensions>
				#</wpt>
			
				
			if re.search("^CKP", waypoint_name) \
				or re.search("^DSS", waypoint_name) \
				or re.search("^FSS", waypoint_name) \
				or re.search("^FSZ", waypoint_name) \
				or re.search("^GAS", waypoint_name) \
				or re.search("^STP", waypoint_name) \
				or re.search("^WPE", waypoint_name) \
				or re.search("^WPM", waypoint_name) \
				or re.search("^WPS", waypoint_name) :
				gpx_text += "<wpt lat=\"" + lat + "\" lon=\"" + lon + "\">\n"
				gpx_text += "  <name>" + waypoint_name + waypoint_number + "(" + status + ")</name>\n"
				
				if(status == "SKP"):
					gpx_text += "  <cmt>Skipped</cmt>\n"
					gpx_text += "  <sym>Navaid, Red</sym>\n"
					gpx_text += "  <type>Navaid, Red</type>\n"
				if(status == "CLR"):
					gpx_text += "  <cmt>Cleared</cmt>\n"
					gpx_text += "  <sym>Navaid, Green</sym>\n"
					gpx_text += "  <type>Navaid, Green</type>\n"
				if(status == "OPN"):
					gpx_text += "  <cmt>Opened</cmt>\n"
					gpx_text += "  <sym>Navaid, Amber</sym>\n"
					gpx_text += "  <type>Navaid, Amber</type>\n"
					
				gpx_text += "  <extensions>\n"
				gpx_text += "    <label xmlns=\"http://www.topografix.com/GPX/gpx_overlay/0/3\">\n"
				gpx_text += "    <label_text>" + waypoint_name + waypoint_number + "(" + status + ")</label_text>\n"
				gpx_text += "    </label>\n"
				gpx_text += "  </extensions>\n"
				gpx_text += "</wpt>\n"
				
				#<wpt lat="35.39277" lon="-117.79754">
				#<name>STP015(SKP)</name>
				#<cmt>Skipped</cmt>
				#<sym>Navaid, Red</sym>
				#<extensions>
				#<label xmlns="http://www.topografix.com/GPX/gpx_overlay/0/3">
				#<label_text>STP015(SKP)</label_text>
				#</label>
				#</extensions>
				#</wpt>
				
				#<wpt lat="35.38779" lon="-117.82772">
				#<name>CKP018(CLR)</name>
				#<cmt>Cleared</cmt>
				#<sym>Navaid, Green</sym>
				#<extensions>
				#<label xmlns="http://www.topografix.com/GPX/gpx_overlay/0/3">
				#<label_text>CKP018(CLR)</label_text>
				#</label>
				#</extensions>
				#</wpt>
			
			
	# Loop to create track	
	gpx_text += "<trk>\n"
	gpx_text += "  <type>Track Log</type>\n"
	gpx_text += "  <extensions>\n"
	gpx_text += "    <label xmlns=\"http://www.topografix.com/GPX/gpx_overlay/0/3\">\n"
	gpx_text += "    <label_text>RCTrackLog(Day#2)</label_text>\n"
	gpx_text += "    </label>\n"
	gpx_text += "  </extensions>\n"	
	gpx_text += "  <trkseg>\n"
	for index in range(0, len(lines)):
		#print(lines[index])
		lines[index] = re.sub('\\s', '', lines[index])
		words = re.split(';', lines[index])
		#print("Words: " + str(len(words)))
		if (len(words) >= 4):
			#print(lines[index])
			#print(words[0])
			#print(words[1])
			#print(words[2])
			#print(words[3] + "\n")
			
			lat = words[0]
			lon = words[1]
			time = words[2]
			speed = words[3]
			
			
			gpx_text += "    <trkpt lat=\"" + lat + "\" lon=\"" + lon + "\">\n"
			gpx_text += "      <ele>0</ele><time>" + year + "-" + month + "-" + day + "T" + time + "Z</time>\n"
			gpx_text += "    </trkpt>\n"
				
			#<trkseg>
			#<trkpt lat=\"19.35606\" lon=\"-96.78916;\">
			#<ele> 0;</ele><time>2000-01-01T7:07:39;Z</time>
			#</trkpt>
	gpx_text += "  </trkseg>\n"
	gpx_text += "</trk>\n"
	gpx_text += "<extensions>\n"
	gpx_text += "</extensions>\n"





	#print("WP Count: " + str(wp_count))
	
	gpx_text += "</gpx>\n"
	print(gpx_text)
