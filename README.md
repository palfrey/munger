munger
======
[![Build Status](https://travis-ci.com/palfrey/munger.svg?branch=master)](https://travis-ci.com/palfrey/munger)

Scan-to-cloud for local scanners.

This is based on the [Fujitsu ScanSnap S1300i](https://www.fujitsu.com/uk/products/computing/peripheral/scanners/scansnap/s1300i/), which despite it's marketing info saying "Scan to Cloud", doesn't. The "ScanSnap Cloud" software is meant to be able to do scan-to-Dropbox, but doesn't. Also, even if it did, it needs to be rigged up to a Windows or Mac machine, and I don't have a spare one of those to have.

Munger enables the use of a Raspberry Pi for scan-to-cloud, along with a convertor component for running elsewhere if you've got an older slower Pi that can't really do the conversion stuff.

![full setup](images/full%20setup.jpg)

Install steps
--------------
1. Acquire a Pi (I'm using an original Model B, so probably anything except the Pi Zero will work for this), a screen (I've got a cheap knockoff of the [AdaFruit 2.8" 320x240 TFT](https://www.adafruit.com/product/1601)), and a USB scanner ([Fujitsu ScanSnap S1300i](https://www.fujitsu.com/uk/products/computing/peripheral/scanners/scansnap/s1300i/) is what I've got, but anything that's compatible with [SANE](http://www.sane-project.org/) and [scanbd](https://wiki.archlinux.org/index.php/Scanner_Button_Daemon) should work)

2. Do the [raspberry-chef](https://github.com/palfrey/raspberry-chef) install, using the following settings:
  - `chef-url` - `https://github.com/palfrey/munger.git`
  - `chef-cookbook` - `munger`
  - `chef-directory` - `device`

3. Download `https://raw.githubusercontent.com/palfrey/munger/master/device/drive.yaml.example` to `/etc/scanner/drive.yaml` on the Pi and edit it to your local settings. In the example config, I've got another checkout of munger on the server in `src/munger` and we're dumping the scans under that. `mount_folder` is the actual folder to mount and `scans_folder` is a subfolder of that to store things in. When the raspberry-chef updater runs again, you should now have a mounted folder.

4. At this point you should be able to open up your scanner and see "Scanner on" display, and then push the physical "scan" button and get the scanner to scan images to the folder you configured in `drive.yaml`

5. You now need another machine (or in theory the Pi itself could do this, but it's really slow on the Pi 1 I'm using, so mostly untested recently). Checkout a copy of this repo there.

6. Build the server docker image `docker build -t munger server`

7. Run it, replacing `<scans folder>` with a path to the `scans folder` from step 3, and `<output folder>` to wherever the end files go (I suggest a local Dropbox folder or similar) `docker run --rm -v <scans folder>:/scans -v <output folder>:/output munger /output /scans`

At this point, when you do a scan it should go through the following steps:

1. Open the scanner and insert the pages
![scanner on](images/scanner%20on.jpg)
2. Push the scan button
![scanning](images/scanning.jpg)
3. Wait for it to finish scanning and uploading
![copying](images/copying.jpg)
4. Wait for the server side work to make the PDF