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
<pre>