# Loading Synthetic Patient Data into FHIR

## Quickstart

### Install Dependencies

1. Make sure Java 1.8 or above is already installed (this is a requirement for running Synthea).
2. Create and activate a virtual environment: `python3 -m venv venv && source venv/bin/activate`
3. Install dependencies: `(venv) pip install --upgrade pip && pip install -r requirements.txt`

### Generate Synthetic Patient Data

1. Run the following command: `./script/generate_synthetic_data.sh`
2. The above command will create sub-directories named after state names under `/synthetic-data` (e.g. `/synthetic-data/Alabama`).
3. Data from 48 states will be generated (Alaska, Vermont, and West Virginia have 0 population).

### Load Generated Researces into FHIR

1. Make sure tunneling to a proper Kids First bastion host is set up.
2. The FHIR server's request validation should be turned off.
3. Execute `(venv) jupyter lab` and run `load_synthetic_data.ipynb`
