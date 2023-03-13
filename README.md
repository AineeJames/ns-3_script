# ns-3 script
![TXPWR_EXAMPLE](./imgs/tx_example.png)
## Description
This script runs the vanet-routing-compare example in ns-3 multiple times. Each time, a script parameter is able to be changed.

<hr>

### Supported parameters
- tx power
- number of cars

<hr>

## Installation
```bash
cd <ns-3 path>
git clone https://github.com/AineeJames/ns-3_script
cd ns-3_script
python3 -m venv venv
source venv/bin/activate
pip install -r "requirements.txt"
python DSRC_script.py --help   # verify install
```

<hr>

## Usage
<details>
<summary>Changing the number of cars</summary>
<br>

```bash
python DSRC_script.py -M cars
```

</details>

<details>
<summary>Changing the tx power</summary>
<br>

```bash
python DSRC_script.py -M txpwr
```

</details>

<details>
<summary>Graphing previous data</summary>
<br>

```bash
python DSRC_script.py -M {cars,txpwr} -P
```

</details>
