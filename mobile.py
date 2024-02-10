import RPi.GPIO as GPIO
import time
import requests
from threading import Thread

# Define your GPIO setup
ENA = 16
IN1 = 20
IN2 = 21
IN3 = 13
IN4 = 19
ENB = 26



GPIO.cleanup()
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)  # Added this line for IN2
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)  # Added this line for IN4
GPIO.setup(ENB, GPIO.OUT)

pwm_a = GPIO.PWM(ENA, 10)
pwm_b = GPIO.PWM(ENB, 10)
pwm_a.start(0)
pwm_b.start(0)

GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)  # Added this line for IN2
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.LOW)  # Added this line for IN4

def run_motors(run_value,ena_SPEED,enb_SPEED,ENAFREQUENCY,ENBFREQUENCY):
    if run_value != 1:
        pwm_a.ChangeFrequency(ENAFREQUENCY)
        pwm_b.ChangeFrequency(ENBFREQUENCY)
        
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)  # Added this line for IN2
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)  # Added this line for IN4
        pwm_a.ChangeDutyCycle(ena_SPEED)
        pwm_b.ChangeDutyCycle(enb_SPEED)
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)  # Added this line for IN2
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)  # Added this line for IN4


def fetch_and_run():
    headers = {'API-Key': 'getyourapifromrrn'}
    while True:
        try:
            response = requests.get('https://remoteresearchnetwork.com/machine/mobiletask',headers=headers, verify=False)
            #print ("Response content: ", response.text)
            if response.status_code == 200:
                data = response.json()
                print("Data Receviced",data)
                run_value = float(data.get('run', 0))
                
                ena_SPEED = float(data.get('ENASPEED', 0))
                enb_SPEED = float(data.get('ENBSPEED', 0))
                #print (enb_SPEED)
                
                ENAFREQUENCY = float(data.get('ENAFREQUENCY', 0))
                ENBFREQUENCY = float(data.get('ENAFREQUENCY', 0))
                run_motors(run_value,ena_SPEED,enb_SPEED,ENAFREQUENCY,ENBFREQUENCY)
                
            else:
                print("Failed to fetch data. Status Code:", response.status_code)
        except Exception as e:
            print("Error fetching data:", e)
        time.sleep(1)  # Add a delay to avoid overwhelming the server

if __name__ == '__main__':
    fetch_thread = Thread(target=fetch_and_run)
    fetch_thread.start()
    fetch_thread.join()
