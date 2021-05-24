<img align="right" src="https://github.com/aishux/Srot/blob/master/media/images/logo_smallest.png"> 

## SROT - COVID19 EMERGENCY RESOURCES DIRECTORY



![Issues](https://img.shields.io/github/issues/aishux/Srot.git)
![Forks](https://img.shields.io/github/forks/aishux/Srot.git)
![Stars](https://img.shields.io/github/stars/aishux/Srot.git)
![License](https://img.shields.io/github/license/aishux/Srot.git)
![](https://warehouse-camo.ingress.cmh1.psfhosted.org/582ab2eba9d0e0f4acbea2fd883f604349908147/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f74656e736f72666c6f772e7376673f7374796c653d706c6173746963)

# Description 
<img align="right" src="https://www.who.int/images/default-source/imported/world-health-day-2019-health-is-a-human-right.gif" width = "200" height = "200">
The Corona Virus pandemic has taken a devastating toll on people in India. It is not just a physical one but also has bought in pain, isolation, and death. Srot is an aim to be India's largest Crowd-Sourced Emergency Services Directory and its main objective is to ease the process of finding resources for an Indian citizen in times of crisis. Srot has an exclusive section for verified as well as unverified leads and also a WhatsApp ChatBot who can fetch leads instantly. It is also an initiative to support local food vendors who can provide healthy food to Covid infected people. Srot has a special place for people who would love to volunteer and help verify leads. Last but not the least, Srot's Flask application is incorporated with a Vaccine Notifier Bot who sends email updates as soon as vaccine slots are available on Cowin for the requested Age Group and Pin Code. The best part about Srot is that it can be converted to any desired Indian Language. 

## 👩‍💻 Technology Stack
#### **Tools**

- **Front End** : HTML / CSS / JavaScript / jQuery / AJAX / Bootstrap 

- **Back End** : Django / Flask / Python / SQlite3

- **API's** : Twillio / CoWin 

# Clone and Star the Repository

``` git clone https://github.com/aishux/Srot.git ```

# :star: SROT Website Setup

## To Setup 

1. Go inside the Django directory
``` 	
cd srot_website
``` 

2. Now create and activate an environment

	``` python -m venv django_env``` 

	``` .\django_env\Scripts\activate```  (for Windows) or ``` source django_env/bin/activate```  (on Mac and Linux)

3. Install dependency for python-magic as per your given OS

	Debian/ Ubuntu
	```sudo apt-get install libmagic1```

	Windows
	```pip install python-magic-bin```

	OSX
	```brew install  libmagic```


## Install requirements

	pip install -r requirements.txt

## To run 

	python manage.py runserver 
	

# :star: Vaccine Notifier Setup

## To Setup 

1. Go inside the Flask directory
``` 	
cd vaccine_notifier
``` 

2. Now create and activate an environment

	``` python -m venv flask_env``` 

	``` .\flask_env\Scripts\activate```  (for Windows) or ``` source flask_env/bin/activate```  (on Mac and Linux)

## Install requirements

	pip install -r requirements.txt

## To run 

	python app.py
	
	(Avoid running using flask run which doesn’t allow threads to work efficiently)

# :star: Note

- The WhatsApp bot is configured on the hosted website so changes in local server won't effect the working.
- Change email address and app password to your credentials in the app.py file to send emails.
- Change email and password in srot > settings.py to your credentials for forgot password emails.

# :star: Process Flow

## SROT Website

![Django Process Diagram ](https://user-images.githubusercontent.com/55614782/119251296-95224500-bbc3-11eb-82b8-53f010b7f661.jpg)

## Vaccine Notifier

![Vaccine notifier process](https://user-images.githubusercontent.com/55614782/119254491-37e2bf80-bbd4-11eb-907a-3b70474545d3.jpeg)

<br>
<br>

# :star: DATA FLOW DIAGRAMS

## SROT Website

![User DFD](https://user-images.githubusercontent.com/55614782/119254609-e25ae280-bbd4-11eb-831e-aea80dc1f0e4.jpg)

<br>

![Volunteer DFD](https://user-images.githubusercontent.com/55614782/119254513-547ef780-bbd4-11eb-94a2-066c26bf305b.jpg)

<br>

## Vaccine Notifier

![Flask DFD](https://user-images.githubusercontent.com/61228436/119272987-71441b00-bc26-11eb-8acc-460f4cac8c67.jpeg)

<br>

# :star: Scan the below QR to visit the Website

<!-- ![qrcode](https://user-images.githubusercontent.com/55614782/119258790-dc6efc80-bbe8-11eb-857c-3a2ca2c61852.png) -->
<img src="https://user-images.githubusercontent.com/55614782/119258790-dc6efc80-bbe8-11eb-857c-3a2ca2c61852.png" width="150" height="150">

<a href="https://srot.pythonanywhere.com/" style="text-decoration:none; color:white;">Visit Srot</a>

## The geeks🤓 behind this initiative:

<table>
  <tr>
    <td align="center"><a href="https://github.com/aishux"><img src="https://avatars.githubusercontent.com/u/61228436?v=4" width="200px;" alt=""/><br /><sub><b>Aishwarya Nathani</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/niksm7"><img src="https://avatars.githubusercontent.com/u/55614782?v=4" width="200px;" alt=""/><br /><sub><b>Nikhil Mankani</b></sub></a><br /></td>
  </tr>
</table>
