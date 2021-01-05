# IoT Project - Smart Home

## Policy
**theme-controller-Policy** and **theme-application-Policy**
<pre>   
{  
  "Version": "2012-10-17",  
  "Statement": [  
    {  
      "Effect": "Allow",  
      "Action": [  
        "iot:Publish",  
        "iot:Receive"  
      ],  
      "Resource": [  
        "arn:aws:iot:us-east-1:478545304112:topic/theme/sensors/reported",  
        "arn:aws:iot:us-east-1:478545304112:topic/theme/actuators/desired"  
      ]  
    },  
    {  
      "Effect": "Allow",  
      "Action": [  
        "iot:Subscribe"  
      ],  
      "Resource": [  
        "arn:aws:iot:us-east-1:478545304112:topicfilter/theme/sensors/reported",  
        "arn:aws:iot:us-east-1:478545304112:topicfilter/theme/actuators/desired"  
      ]  
    },  
    {  
      "Effect": "Allow",  
      "Action": [  
        "iot:Connect"  
      ],  
      "Resource": [  
        "arn:aws:iot:us-east-1:478545304112:client/theme-controller",  
        "arn:aws:iot:us-east-1:478545304112:client/theme-application"  
      ]  
    }  
  ]  
}  
</pre>

## Devices 
* Lamp - https://www.zigbee2mqtt.io/devices/AU-A1GSZ9RGBW.html
* Thermostat - https://www.zigbee2mqtt.io/devices/Zen-01-W.html
* Curtains - https://www.zigbee2mqtt.io/devices/W40CZ.html
* Speaker - https://www.mediaexpert.pl/komputery-i-tablety/akcesoria-komputerowe/glosniki-komputerowe/glosniki-trust-remo-2-0-speaker-set?gclid=CjwKCAiAudD_BRBXEiwAudakX1TzMnU0TK4Qkwo9jno1q-ObeIbjTx-fI241vYgENOZcuECtPQPCXhoCSGoQAvD_BwE