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
# 2. Configuring Azure Services  
a. Azure IoT Hub Setup  
   1. Go to Azure Portal.  
   2. Navigate to Resource Group ➝ FinalRTRD.  
   3. Open Rideau-IOT-Hub.  
   4. Under Devices, create three devices:  
DowsLakeSensor  
FifthaveSensor  
NACSensor  
   5. Copy each device’s connection string and update them in the simulation script accordingly.  

b. Azure Stream Analytics Job  
   1. Navigate to RideauAnalyticJob in the FinalRTRD resource group.  
   2. Configure Input :  

          Source Type : IoT Hub
          IoT Hub : Rideau-IOT-Hub
          Consumer Group : $Default
          Shared Access Policy : iothubowner  

   3. Configure Output :  

          Output to Azure Blob Storage  
          Storage Account : rideaucanalstorageacc  
          Container : streamcontainer  
          File Format: JSON  
    
   4. Create and enter the Query :    
```
SELECT
  System.Timestamp AS WindowEnd,
  location,
  AVG(iceThickness) AS AvgIceThickness,
  MAX(snowAccumulation) AS MaxSnowAccumulation
INTO
  [BlobOutput]
FROM
  [Rideau-IOT-Hub]
TIMESTAMP BY timestamp
GROUP BY
  TUMBLINGWINDOW(minute, 5), location
```
   5. Click Start Job to begin streaming and processing real-time sensor data.  
## 3. Accessing Stored Data  

   1. Navigate to Storage Accounts > rideaucanalstorageacc.  
   2. Click on Containers, then select streamcontainer.  
   3. View the output files (in .json format) generated by the Stream Analytics job.  
   4. Each file represents a 5-minute window of aggregated data per location, including :  
<li>avgIceThickness</li>
<li>maxSnow</li> 
<li>location</li>
<li>windowEnd</li>

## 5. Results  
The real-time monitoring system for the Rideau Canal Skateway successfully simulated sensor data, processed it using Azure Stream Analytics, and stored the aggregated output in Azure Blob Storage.  

# Aggregated Data Outputs  
Using a tumbling window of 5 minutes, the Stream Analytics job computed the following for each location (Dow's Lake, Fifth Avenue, NAC):  

<li>Average Ice Thickness</li>
<li>Maximum Snow Accumulation</li>  

These metrics are crucial for determining safe skating conditions and understanding snow impact across different points on the canal.  

# Example Aggregated Output (JSON format)  
```
{
  "location": "NAC",
  "windowEnd": "2025-04-09T22:35:00Z",
  "avgIceThickness": 28.5,
  "maxSnow": 12
}
```
Each record in the container streamcontainer corresponds to one location and a 5-minute window of data.  

# Sample Output Files  
Processed results are saved in Azure Blob Storage at:  

<li>Storage Account : rideaucanalstorageacc</li>  
<li>Container : streamcontainer</li>  

Each file is stored in .json format and contains :  

<li>Aggregated data for all three sensors.</li>  
<li>Timestamps showing when each aggregation window ended.</li>  
<li>Location-specific insights.</li>  

## 6. Reflection
# Challenges Faced  
1. Device-to-Hub Connectivity  

<li>Initially, some of the IoT devices failed to send data due to incorrect device connection strings.</li>  
<li>Resolution: Verified and updated device-specific connection strings from Azure IoT Hub into the simulation script.</li>   

2. Stream Analytics Job Delays  

<li>There was a noticeable delay between data ingestion and storage output during testing.</li>  
<li>Resolution: Tuned the tumbling window to 5 minutes and ensured timestamp alignment (TIMESTAMP BY timestamp) to improve consistency.</li>  

3. Data Format Conflicts  

<li>During early testing, inconsistencies in the JSON payload structure (e.g., missing timestamp or location) caused ingestion failures.</li>  
<li>Resolution: Standardized the payload structure and added logging to the simulation script to validate output.</li>  

4. Blob Storage Output Issues

<li>The Stream Analytics job didn’t create output files initially because of permission issues with the container.</li>  
<li>Resolution: Corrected storage access roles and confirmed the output path and format (JSON) were properly configured.</li>  

# Lessons Learned
Gained hands-on experience working with real-time Azure services, especially how to interconnect IoT Hub, Stream Analytics, and Blob Storage.
Understood the importance of timestamp synchronization and windowing when aggregating real-time data.
Learned how to troubleshoot and debug Azure service configurations, such as verifying routing paths, input/output bindings, and service health.

