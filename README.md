### `SPAM DETECTOR`
Este proyecto es una plataforma web que detecta si un texto es SPAM o NO SPAM, esto a través de Flask y la base de datos MongoDB. Tiene un diseño amigable e intuitivo al usuario para pegar el texto de
su preferencia y analizarlo para saber si es o no spam. 

`Cabe aclarar que este proyecto solo funcionará en Visual Studio Code, y no en Spyder`
#
### `INSTALACIÓN PREVIA EN PYTHON`
Sigue los pasos a continuación:
```bash
cd Spam_Detector_Flask/
pip install flask scikit-learn pymongo pandas re nltk
```
Solo instalar re y nltk si es necesario, de no serlo puede omitir esto. Una vez instalado vamos al siguiente paso
#
### `"PREPARACIÓN" EN MONGODB`
En sí ya está creado, pero lo primero que tienes que hacer (procura hacerlo) es conectar el MongoDB para que el código pueda guardar los textos en dicha base de datos llamada _"Spam_Detector"_
en la colección _"mensajes"_.
#
Una vez ya listo todo, simplemente tienes que estar en la carpeta `Spam_Detector_Flask` y correr el siguiente comando
```bash
python app.py
```
La página estará en `http://127.0.0.1:5000`
