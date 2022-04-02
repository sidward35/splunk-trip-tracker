# Splunk Trip Tracker

<img src="https://raw.githubusercontent.com/sidward35/splunk-trip-tracker/main/images/Trip%20Tracker.png"/>

## Splunk Setup

### App Installation

1. Download [trip_tracker.spl](https://github.com/sidward35/splunk-trip-tracker/releases/download/v1.0.0/trip_tracker.spl).

2. In Splunk, click on the `Apps` dropdown menu (top left) > `Manage Apps` > `Install app from file` (top right).

3. Upload the downloaded `trip_tracker.spl` file.

### HEC Input Setup

4. In the top right go to `Settings` > `Data Inputs` > `HTTP Event Collector` > `Global Settings`.

5. Set "All Tokens" to `Enabled`, uncheck "Enable SSL", and ensure that "HTTP Port Number" is set to `8088`. Click `Save`.

6. Click `New Token` and on the next page, enter a name for the input in the corresponding box (e.g. `TripTracker`). Click `Next`.

7. In the "Select Allowed Indexes" section, select `main`. Click `Review` > `Submit`.

8. Copy/save the HEC token that should now be displayed. This will be used by the Python script we will run later.

## Trip Tracking and Export to Splunk

9. Download the [Geo Tracker - GPS tracker](https://play.google.com/store/apps/details?id=com.ilyabogdanovich.geotracker) app and record some trips.

10. Once a trip is recorded, export the trip files (from the sidebar on the left) **in GPX format**. Copy that file onto your computer. (Or, alternatively, setup [Termux](https://termux.com) to [run Python scripts right from your phone](https://wiki.termux.com/wiki/Python).)

<img src="https://raw.githubusercontent.com/sidward35/splunk-trip-tracker/main/images/trip_export.png" width=400px/>

11. Download [parse_gpx.py](https://raw.githubusercontent.com/sidward35/splunk-trip-tracker/main/parse_gpx.py). Edit line 64 and replace SPLUNK_IP and HEC_TOKEN with the IP address of your Splunk instance and the HEC token you created earlier.
```python
parseXML(new_file, 'SPLUNK_IP', 'HEC_TOKEN', 'geotracker')
```

12. Run `python parse_gpx.py TRIP_GPX_FILE` where TRIP_GPX_FILE is the GPX file you exported from the mobile app. (To take this one step further and [automatically run this command](#automate-gpx-parsing-and-ingesting) through Termux upon exporting your GPX file, setup an action on Llamalab's Automate.)

13. And that's it! Head into the Trip Tracker app in Splunk to take a look at the OOTB dashboards, which should now be populated with data.


## Automate GPX Parsing and Ingesting
#### Using [Termux](https://termux.com) and [Llamalab's Automate](https://llamalab.com/automate), the process of parsing your exported GPX file and sending it to Splunk can be automated.

1. In the home folder of your phone's storage (where the DCIM, Documents, Downloads, etc. folders are located), create a new folder `MyMaps` if it doesn't already exist. Inside that, create a new folder `gpx`. Download [parse_gpx.py](https://raw.githubusercontent.com/sidward35/splunk-trip-tracker/main/parse_gpx.py) and move it inside the `gpx` folder.

2. Download [Termux](https://termux.com) and [Llamalab's Automate](https://llamalab.com/automate). Termux, if possible, should be downloaded from F-Droid rather than the Play Store, for the most up-to-date version.

3. Install Python on Termux by following the steps [here](https://wiki.termux.com/wiki/Python). Then run `pip install requests`.

4. Download this [Termux plugin](https://llamalab.com/automate/community/flows/38833) for the Automate app and follow the steps listed there. Then run
```bash
termux-setup-storage
nano ~/.termux/tasker/splunk.sh
```
and add the following to the file
```bash
cd storage/shared/MyMaps/gpx
python parse_gpx.py $(basename ${1})
```
and then finally run
```bash
chmod u+x ~/.termux/splunk.sh
```

5. Open up Automate, and create a new flow. Swipe from the right to view the list of blocks, and under `File & storage` select `File monitor`. Select the new block and set the "Path" to `MyMaps/gpx`, "Events" to `File created`, and the output variable "Path of alteration" to `new_file`. Click `Save`.

6. Swipe from the right again and under `Apps`, select `Plug-in action`. Tap the new block to configure, and set the "Plug-in" to `Termux`. Under the "Plug-in" field, tap `Configure`.

7. For "Executable file", enter `splunk.sh`. "Arguments" should be set to `%new_file`. Leave the rest as-is, and ensure `Execute in a terminal session` and `Wait for result for commands` are checked. Click the save button at the top right. Then on the "Plug-in action" setup screen, click `Save` again.

8. Finally, "wire" the flow blocks together as shown in the image below. Press the back button and click `Start`. 

<img src="https://raw.githubusercontent.com/sidward35/splunk-trip-tracker/main/images/automation_flow.png" width=300px/>

9. The GPX export directory will now be monitored for any new files, which will automatically get parsed and sent to Splunk. To test this, simply record a trip and click the download/export button, and then watch the automation go!
