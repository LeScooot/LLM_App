#Just testing - functionality will be implemented soon

class Assistant:

    def decision_tree(self, code):
        if(code == '[tv_on]'):
            print("TV IS TURNED ON")
        elif(code == '[fan_on]'):
            print("FAN IS TURNED ON")
        elif(code == '[lights_off]'):
            print("LIGHT IS TURNED OFF")
        elif(code == "[garage_close]"):
            print("GARAGE IS CLOSED")
        elif(code == "[no_code]"):
            print("\"[no_code]\" provided")
        else:
            print("INVALIDE CODE")

