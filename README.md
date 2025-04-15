# 25W_CST8916_Final_Project_Assignment
## 1. Scenario Description
Ottawa's Rideau Canal is transformed into the world's largest outdoor ice skating rink each year for thousands of tourists. But for it to stay skater-friendly, there has to be ongoing ice and weather monitoring. This project replicates a real-time monitoring system using virtual IoT sensors installed at three key locations—Dow's Lake, Fifth Avenue, and the NAC. They track ice thickness, surface temperature, and snowfall. The data is streamed into Azure IoT Hub, analyzed in real-time through Azure Stream Analytics, and stored in Azure Blob Storage. The goal is to support city planners with speedy, smart safety decisions.

## 2. System Architecture Diagram
![Image](https://github.com/user-attachments/assets/2c09b92b-608f-466b-bcb3-36309465aff9)

## 3. Implementation Details
### IoT Sensor Simulation and Script
The project simulates three IoT sensors placed at key positions along the Rideau Canal Skateway:

-> DowsLakeSensor (Dow's Lake) ```
-> FifthaveSensor (Fifth Avenue) ``` 
-> NACSensor (National Arts Centre) ```

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

## 4. Usage Instructions
## 5. Results
## 6. Reflection
