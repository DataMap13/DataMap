#!/usr/bin/python
import subprocess
import os
import re
import time

########################
# Andrew W.E. McDonald #
########################

"""
Modified by Riju Singh to enable sudo without console input. 
Uses Raw password. The assumption is that if the user is here, he/she already knows the password

Note: this function, 'extract_signal_levels_and_frequencies',  is designed to extract the frequency of the network with the highest signal strength out of the networks in the input source. The input source is expected to have this format (the next line should be the first line in the input file):
                    Frequency:2.412 GHz (Channel 1)
                    Quality=27/70  Signal level=-83 dBm  
                    Encryption key:off
                    ESSID:"drexelguest"
--
                    Frequency:2.412 GHz (Channel 1)
                    Quality=16/70  Signal level=-94 dBm  
                    Encryption key:off
                    ESSID:"drexelguest"
(The above line should be the last line in the input source -- number of networks in the file is unimportant, but the format must match the above snippet)

One could generate this source and save it to a file by running the following two commands (wireless card must be in "Managed" mode):

~$ sudo iwlist wlan0 scanning > wifi.txt
~$ grep -B 3 drexelguest wifi.txt > grepped_wifi.txt

"grepped_wifi.txt" will be formatted like the snippet above, and then the below function may be called with that as the input.

each block in 'grepped_wifi.txt' would be formatted like so:

line 0 => Frequency...
line 1 => Quality ...
line 2 => Encryption...
line 3 => ESSID...

The funciton returns a 2d list. Each row is a different access point, col. 0 is the signal level for that AP, and col. 1 is its frequency.
"""

def extract_signal_levels_and_frequencies(input_source):
	count = -1
	choices = []
	input_source = input_source.split('\n')
	for line in input_source:
		print line
		count += 1
		if count == 0:
			# get frequency 
			this_freq = re.search('\d\.\d+',line)
			if this_freq is None:
				print "Frequency not where it should be! Aborting..."
				return None
		elif count == 1:
			# get signal level, will be in group '2' (just the numbers, with the 'minus' sign, if it exists.)
			this_signal_level = re.search('(level=)(-?\d+)',line)		
			if (this_signal_level is None) or (len(this_signal_level.groups()) < 2):
				print "Signal level not where it should be! Aborting..."
				return None
		elif count == 4:
			# append an array such that col 0 => signal level (converted to int), and col 1 => frequency (converted to float)
			choices.append([int(this_signal_level.group(2)),float(this_freq.group(0))])
			count = -1
	# append the last one, because the count never reaches '4' for the last access point, as there is no line with "--" after its 4 lines of data.
	choices.append([int(this_signal_level.group(2)),float(this_freq.group(0))])
	#print choices
	return choices

"""
This will return the n'th unique strongest signal. So, if the first three strongest signals are on freq w.xyz, and the fourth is on a.bcd, and 'n' was '1' (so, the second strongest, because the first strongest is '0' to reduce confusion with indices), then the fourth strongest signal's freq will be returned, a.bcd (because it is the second strongest signal that is unique).

If 'n' is larger than the number of distinct frequencies, the frequency with the weakest 
"""
def get_freq_of_nth_strongest_signal(n,choices):
	unique_options = []
	choices.sort(key=lambda x: x[0])
	num_choices = len(choices)
	start_at = num_choices - 1
	# because the list is sorted in increasing signal strength, if we start from the end, and work back, we guarantee that if we find a duplicate of a frequency, the greatest signal strength for that frequency has already been saved in the unique_options list, so we can ignore any repeats of that frequency
	for i in range(start_at,-1,-1):
		is_here = False	
		this_choice = choices[i]
		#print
		#print "choice: ",this_choice," unique_options (freq. only): ",
		for opt in unique_options:
			#print opt[1]," ",
			if opt[1] == this_choice[1]:
				is_here = True
				break
		if is_here is False:
			unique_options.append(this_choice)
	#print
	# because the sort will organize least to greatest, and then we traversed the list backwards, index '0' of unique_options will hold the frequency with the greatest signal strength.
	num_options = len(unique_options)
	if n >= num_options:
		return str(unique_options[num_options-1][1]) # this is the frequency with the weakest signal  
	print "unique options (sorted): ",unique_options
	#print "choice: ",unique_options[n][1]
	return str(unique_options[n][1])# the n'th strongest unique signal's frequency.	



'''
returns a string that is the freq of the access point with the strongest signal strength
'''
def get_freq_to_listen_on( interface ):
	# get a list of the access points within range, create a pipe to recieve the output
	shell_cmds = "echo s3tt0p! | sudo -S iwlist " + interface + " scanning | grep -B 3 drexelguest"
	# wifi_signals = subprocess.Popen(["sudo","iwlist",interface,"scanning"],stdout=subprocess.PIPE)#subprocess.PIPE)
	# # use grep to filter what isn't needed, and produce a 'file' with the formatting needed for 'extract_signal_levels_and_frequencies'
	# grepped_wifi = subprocess.Popen(["grep","-B","3","drexelguest"],stdin=wifi_signals.stdout,stdout=subprocess.PIPE)
	# # get signal levels and frequencies, and then call '' to sort the list and get the freq to listen on (the one with the greatest signal strength)
	# wifi_signals.stdout.close()
	grepped_wifi = ''
	for i in range(0,3):
		grepped_wifi += subprocess.check_output( shell_cmds, stderr = subprocess.STDOUT, shell = True )[26:] + "--\n" # run 3 times to make sure we get all networks, and cut off the "[sudo] enter password" (or something similar) line that is in the first 26 characters of the string, also, add the delimeter that grep adds.
		time.sleep(.04)
	grepped_wifi = grepped_wifi[:-3]
	print  grepped_wifi	
	choices = extract_signal_levels_and_frequencies(grepped_wifi)
	# grepped_wifi.stdout.close()
	chosen_freq = get_freq_of_nth_strongest_signal(0,choices)
	print 'chosen freq: ',chosen_freq
	return chosen_freq
	
def set_iface_to_freq_with_strongest_signal( interface ):
	# bring the target interface down
	subprocess.call(["sudo","ifconfig",interface,"down"])
	# set its mode to 'Managed' to allow scanning network
	subprocess.call(["sudo","iwconfig",interface,"mode","Managed"])
	# bring the target interface back up
	subprocess.call(["sudo","ifconfig",interface,"up"])
	# get the freq to listen on 
	freq_to_listen_on = get_freq_to_listen_on( interface )
	# freq_to_listen_on = get_freq_to_listen_on()
	# set its mode to 'Managed' to allow scanning network, but first we must add a 'G' to the frequency so that iwconfig knows its x.yz gigahertz
	the_freq = freq_to_listen_on + "G"
	subprocess.call(["sudo","iwconfig",interface,"freq",the_freq])
	attempts = 0
	while attempts < 500:
		subprocess.call(["sudo","iwconfig",interface,"ESSID","drexelguest"])
		success = subprocess.Popen(["iwconfig"],stdout=subprocess.PIPE)	
		result = str(success.communicate())
		#print result
		if "Not-Associated" in result:
			time.sleep(.040)
			#print "!!!!!!!!!!!!!!!! Not Associated !!!!!!!!!!!!!!!!!!!"
		else:
			print "interface '" + interface + "' set to frequency: '" + the_freq
			break
		attempts += 1

	if attempts >= 500:		
		print "ERROR: Could not associate with an access point!!!"
		### todo: We should make it choose a different frequency!!!
		exit()



command = "echo s3tt0p! | sudo -S ifconfig wlan0 up"
subprocess.check_output(command,stderr = None, shell = True )
set_iface_to_freq_with_strongest_signal("wlan0")
#subprocess.call(["sudo","mkdir","/etc/testDep"])

