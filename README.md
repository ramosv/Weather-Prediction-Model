# Weather-Prediction-Model

Weather Prediction Model for the State of Colorado

---

### Eddie's notes in how I setup my dev environment

#### Unzip data

> `unzip ./Weather\ Prediction\ Raw\ Data.zip -d ./raw_data`

#### Virtual environment

Run the following commands:

> `source .venv/bin/activate` [^1]

> `pip install pip --upgrade`

> `pip install -r ./requirements.txt`

#### Adding jupyter notebooks to vs code

[Read article here](https://code.visualstudio.com/docs/datascience/jupyter-notebooks#:~:text=Jupyter%20Notebooks%20in%20VS%20Code,and%20through%20Python%20code%20files.)

> Note from Eddie: I didn't need to follow the above steps. Once you get the data unzipped, the virtual env. made, and all the packages installed, you should be able to open the `test.ipynb` and VSCode will have a message box pop-up asking to install extensions for Jupyter notebooks.

[^1]: Note this may be different on Windows!
