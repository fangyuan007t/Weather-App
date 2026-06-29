import sys
import requests
from dotenv import load_dotenv
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt

load_dotenv()

API_KEY= os.getenv("API_KEY")

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.discription_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Wather App")
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.discription_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.discription_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.discription_label.setObjectName("discription_label")

        self.setStyleSheet("""
                            QLabel, QPushButton{
                                font-family: calibri;
                           }
                           QLabel#city_label{
                                font-size: 40px;
                                font-style: italic;
                           }
                           QLineEdit#city_input{
                                font-size: 40px;
                           }
                           QPushButton#get_weather_button{
                                font-size: 30px;
                                font-weight: bold;
                           }
                           QLabel#temperature_label{
                                font-size: 75px;
                           }
                           QLabel#emoji_label{
                                font-size: 100px;
                                font-family: Segoe UI emoji;   
                           }
                           QLabel#discription_label{
                                font-size: 50px;   
                           }
                           """)
        
        self.get_weather_button.clicked.connect(self.get_weather)
        
    def get_weather(self):
        api_key = API_KEY
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
            
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error: \n Check your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error: \n Request timed-out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects: \n Check the url")

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request: \n Please Check your input")
                case 401:
                    self.display_error("Unauthorized: \n Invalid API Key")
                case 403:
                    self.display_error("Forbidden: \n Access is Denied!")
                case 404:
                    self.display_error("Not Found: \n City not found")
                case 500:
                    self.display_error("Internal Server Error: \n Try again later")
                case 502:
                    self.display_error("Bad Gateway: \n Invalid response from server")
                case 503:
                    self.display_error("Service unavailable: \n Server is down")
                case 504:
                    self.display_error("Gateway Timeout: \n No response from server")
                case _:
                    self.display_error(f"HTTP Error: {http_error}")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error: \n {req_error}")
        

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)

        # To clean up emoji and weather discription
        self.emoji_label.clear()
        self.discription_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperatire_kelvin = data["main"]["temp"]
        temperatire_celcius = temperatire_kelvin - 273.15

        weatherID = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperatire_celcius:.0f}° C")
        self.emoji_label.setText(self.get_weather_emoji(weatherID))
        self.discription_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weatherID):
        if 200 <= weatherID <= 232:
            return "⛈️"
        elif 300 <= weatherID <= 321:
            return "⛅"
        elif 500 <= weatherID <= 531:
            return "🌧️"
        elif 600 <= weatherID <= 622:
            return "❄️"
        elif 700 <= weatherID <= 741:
            return "🌫️"
        elif weatherID == 762:
            return "🌋"
        elif weatherID == 771:
            return "💨"
        elif weatherID == 781:
            return "🌪️"
        elif weatherID == 800:
            return "🌞"
        elif 801<= weatherID <= 804:
            return "☁️"
        else:
            return ""
        
    
if __name__== "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
