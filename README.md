# 25W_CST8916_Final_Project_Assignment
## 1. Scenario Description
Ottawa's Rideau Canal is transformed into the world's largest outdoor ice skating rink each year for thousands of tourists. But for it to stay skater-friendly, there has to be ongoing ice and weather monitoring. This project replicates a real-time monitoring system using virtual IoT sensors installed at three key locations—Dow's Lake, Fifth Avenue, and the NAC. They track ice thickness, surface temperature, and snowfall. The data is streamed into Azure IoT Hub, analyzed in real-time through Azure Stream Analytics, and stored in Azure Blob Storage. The goal is to support city planners with speedy, smart safety decisions.

## 2. System Architecture Diagram
![Image](https://github.com/user-attachments/assets/2c09b92b-608f-466b-bcb3-36309465aff9)

## 3. Implementation Details
### IoT Sensor Simulation and Script
The project simulates three IoT sensors placed at key positions along the Rideau Canal Skateway:<br></br>
<li>DowsLakeSensor (Dow's Lake)  </li>
<li>FifthaveSensor (Fifth Avenue)  </li>
<li>NACSensor (National Arts Centre)  </li>  
<br></br>

Sample JSON script used is below :-  
```
{
  "location": "Dow's Lake",
  "iceThickness": 27,
  "surfaceTemperature": -1,
  "snowAccumulation": 8,
  "externalTemperature": -4,
  "timestamp": "2025-04-09T22:32:19.612150Z"
}
```
The script uses the Azure IoT Hub Device SDK to send telemetry to the Rideau-IOT-Hub.

### Azure IoT Hub Configuration

IoT Hub Name : Rideau-IOT-Hub  
Resource Group : FinalRTRD  
Region : Canada Central  
Tier : Free (daily message quota: 8,000)  

The three devices (DowsLakeSensor, FifthaveSensor, NACSensor) were each added manually using the Azure portal. Authentication is handled using Shared Access Signature (SAS) keys, which were inserted into the simulation script for each device.  

No routes or custom endpoints were present — default settings are used.  

### Azure Stream Analytics Job

Job Name : RideauAnalyticJob  
Status : Created (configured but not yet started)  
Region : Canada Central  
Input : IoT Hub (Rideau-IOT-Hub)  
Output : Azure Blob Storage (streamcontainer in rideaucanalstorageacc)  

Logic Query :-  
```
SELECT
  System.Timestamp AS WindowEnd,
  location,
  AVG(iceThickness) AS AvgIceThickness,
  MAX(snowAccumulation) AS MaxSnowAccumulation
INTO
  [YourBlobOutputAlias]
FROM
  [Rideau-IOT-Hub]
TIMESTAMP BY timestamp
GROUP BY
  TUMBLINGWINDOW(minute, 5), location

```
This aggregates each location's data over a 5-minute window to :  
<li>Calculate average ice thickness.</li>  
<li>Find the maximum snow accumulation.</li>  

### Azure Blob Storage  

Storage Account : rideaucanalstorageacc  
Container : streamcontainer  
Access Tier : Hot (default)  
Replication : Locally-redundant (LRS)  

The Stream Analytics job will output processed data into this container. File format is expected to be JSON by default, depending on Stream Analytics job settings.

Files are named automatically and organized by date/hour/minute structure inside the container.
## 4. Usage Instructions
# 1. Running the IoT Sensor Simulation  

To simulate sensor data from Dow's Lake, Fifth Avenue, and NAC locations:  

1. Open Visual Studio Code.  
2. Ensure Python 3.11 or above is installed.  
3. Install the required Azure IoT Device SDK using pip:  
```
pip install azure-iot-device
```
4. Navigate to the folder containing simulate_sensors.py.  
5. Make sure your simulate_sensors.py contains device connection strings for:  
<li>DowsLakeSensor</li>  
<li>FifthaveSensor</li>  
<li>NACSensor</li>  
6. Run the simulation script:
```
python simulate_sensors.py
```

The script will start generating telemetry data every 10 seconds and send it to Rideau-IOT-Hub.  

## 5. Results
## 6. Reflection
