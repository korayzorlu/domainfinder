# Domain Finder
This is a test project

# Installation & Usage
```bash
$ mkdir ~/newproject

$ cd ~/newproject

$ git clone https://github.com/korayzorlu/domainfinder.git

$ sudo apt install python3-pip python3-venv

$ python3.9 -m venv myenv

$ source myenv/bin/activate

$ cd domainfinder

$ pip install -r requirements.txt

### In this step, Set DB Settings in settings.py

$ python manage.py migrate

$ python manage.py runserver
``` 