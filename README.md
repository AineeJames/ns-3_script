# ns-3 script

runs multiple simulation concurrently and displays output results
clone repo into ns-3 directory
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ns-3_script
python3 DSRC_numcars.py --setup 5,50,200,50 
```

in order to only view graphs run the following:
```bash
python3 DSRC_numcars.py --process-only
```
