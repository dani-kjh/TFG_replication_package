# TFG_replication_package

### The resulting directory structure

---

The directory structure of the project looks like this:

```
├── README.md <- The top-level README for developers using this project.
│
├── testing
│ ├── main.py <- Script to perform inference on deployed providers
│ ├── requirements.txt <- The requirements file for reproducing the testing environment.
│ └── sentences.txt <- Text file containing the dataset used for the experimentation.
│
│
├── results <- Results from executing the testing script
│ ├── aws <- Results from the aws cloud provider
│ ├── azure <- Results from the azure cloud provider
│ ├── heroku <- Results from the heroku cloud provider.
│ └── railway <- Results from the railway cloud provider.
│
│
├── reports <- Generated analysis as HTML, PDF, LaTeX, etc.
│ ├── analysis.py <- Python script to used to evaluate the results
│ ├── requirements.txt <- The requirements file for reproducing the analysis environment.
│ └── report_figures <- Generated graphics and figures to be used in reporting
│   ├── normality <- Figures and tables to assess normality of distribution
│   ├── significance <- Tables to assess statistically signiffcicant differences.
│   └── summary_table <- Tables of overview measures.
│
│
├── src <- Source code for use in this project.
│ ├── modules <- Python file containing the reference to the model
│ │ └── inference.py
│ │
│ ├── app.py <- Python file containing the declaration of the API.
│ │
│ ├── requirements.txt <- The requirements file for reproducing the application environment
│ │
│ └── Dockerfile <- Dockerfile used to generate the image deployed in cloud providers

```
