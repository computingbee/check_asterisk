#### Nagios & Icinga 2 plugins for DAHDI and PRI cards on asterisk PBX server

These plugins require:

* Asterisk 1.8.14 
* libpri version: 1.4.12 
* DAHDI Version: 2.6.1
* Python 2.6.5

But should also work with newer versions as long as the output of 'pri show spans' and 'dahdi_scan' is consistent. I tested with icinga2 only. However, it should also work with Nagios and its forks beside icinga.

#### Examples
```sh
./check_asterisk_dahdi
OK: [1] active=yes alarms=OK description=Wildcard TE121 Card 0 name=WCT1/0 manufacturer=Digium devicetype=Wildcard TE121 (VPMOCT032)
OK: [2] active=yes alarms=OK description=Wildcard AEX800 name=WCTDM/0 manufacturer=Digium devicetype=Wildcard AEX800 (VPMADT032)

./check_asterisk_pri                            
OK: PRI span 1/0: Up, Active

Running With NRPE:

/usr/lib/nagios/plugins/check_nrpe -H <asterisk_host> -c 'check_asterisk_dahdi'
OK: [1] active=yes alarms=OK description=Wildcard TE121 Card 0 name=WCT1/0 manufacturer=Digium devicetype=Wildcard TE121 (VPMOCT032)
OK: [2] active=yes alarms=OK description=Wildcard AEX800 name=WCTDM/0 manufacturer=Digium devicetype=Wildcard AEX800 (VPMADT032)

/usr/lib/nagios/plugins/check_nrpe -H <asterisk_host> -c 'check_asterisk_pri'  
OK: PRI span 1/0: Up, Active
```

#### Software & Hardware Requirements
```sh
python, asterisk, libpri, DAHDI, and of course PCI cards
```

#### Usage
```sh
You will need to run these plugins remotely on your PBX eithr with ICINGA2 client or NRPE installed. 
I had to change the permissions on the following Run-Control files to avoid "NRPE: Unable to read output" error:

* chmod 775 /var/run/asterisk/asterisk.ctl
* chmod 666 /dev/dahdi/ctl

These file are not present so you will need to type the full path to see the permissions on these files.
* ls -alh /var/run/asterisk/asterisk.ctl /dev/dahdi/ctl

Here is the NRPE config from /etc/nagios/nrpe.cfg for these checks:

command[check_asterisk_dahdi]=HOME=~nagios /usr/lib/nagios/plugins/check_asterisk_dahdi.py
command[check_asterisk_pri]=HOME=~nagios /usr/lib/nagios/plugins/check_asterisk_pri.py

You may also need to add these to your /etc/sudoers:
nagios ALL=(root) NOPASSWD:/usr/sbin/asterisk -x pri show spans
nagios ALL=(root) NOPASSWD:/usr/lib/nagios/plugins/
nagios ALL=(root) NOPASSWD:/usr/sbin/dahdi_scan
Defaults:nagios !requiretty

Finally, you may also want the NRPE user (nagios) to asterisk group if you have issues.

```
