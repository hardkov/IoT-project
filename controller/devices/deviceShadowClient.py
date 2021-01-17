from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

def onResponse(payload, responseStatus, token):
    if responseStatus == "accepted":
        print("Shadow client: update accepted")
    elif responseStatus == "rejected":
        print("Shadow client: update rejected")
        print(payload)
    elif responseStatus == "timeout":
        print("Shadow client: time out")

class DeviceShadowClient(object):
    def __init__(self, deviceName):
        self.clientId = deviceName
        self.rootCAPath = "devices/config/root-CA.crt"
        self.privateKeyPath = "devices/config/" + deviceName + ".private.key"
        self.certificatePath = "devices/config/" + deviceName + ".cert.pem"
        self.host = "a3w259c8e2kscd-ats.iot.us-east-1.amazonaws.com"
        self.port = 8883

        self.shadowClient = AWSIoTMQTTShadowClient(self.clientId)
        self.shadowClient.configureEndpoint(self.host, self.port)
        self.shadowClient.configureCredentials(self.rootCAPath, self.privateKeyPath, self.certificatePath)

        self.shadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.shadowClient.configureConnectDisconnectTimeout(10)
        self.shadowClient.configureMQTTOperationTimeout(5)

        self.shadowClient.connect()

        self.handler = self.shadowClient.createShadowHandlerWithName(self.clientId, True)
        self.handler.shadowDelete(onResponse, 5)

    def updateShadow(self, jsonPayload):
        self.handler.shadowUpdate(jsonPayload, onResponse, 5)
