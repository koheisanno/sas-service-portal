## Venv setup
### Create virtual environment
https://docs.python.org/3/library/venv.html

macOS:
```
python -m venv name-of-venv
```
### Activate virtual environment
```
source name-of-venv/bin/activate
```

### Load environment variables
Add .env file into base directory

### Install packages
#### install backend packages
```
pip install -r requirements.txt
```
#### install frontend packages
cd into frontend
```
npm install
```

### Run backend server
```
python manage.py runserver
```

### Run frontend server
cd into frontend
```
npm run serve
```


